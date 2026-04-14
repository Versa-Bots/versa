"""HTTP healthcheck server for DB and Discord readiness, ratelimit, and heartbeat probes."""

import asyncio
import json
import logging
import math
from contextlib import suppress
from typing import Any

import discord
from tortoise import Tortoise
from tortoise.exceptions import ConfigurationError, DBConnectionError, OperationalError

logger = logging.getLogger(__name__)

_REQUEST_TIMEOUT_SECONDS = 5
_MAX_HEARTBEAT_LATENCY_SECONDS = 10


class HealthcheckServer:
    """Serve HTTP healthcheck responses for runtime dependency status."""

    def __init__(
        self,
        bot: discord.Bot,
        *,
        host: str,
        port: int,
        path: str = "/",
    ) -> None:
        """
        Initialize the healthcheck server.

        :param bot: Discord bot instance used for runtime status checks.
        :param host: Interface address for the healthcheck listener.
        :param port: TCP port for the healthcheck listener.
        :param path: HTTP path that serves health responses.
        """
        self.bot = bot
        self.host = host
        self.port = port
        self.path = path
        self._server: asyncio.AbstractServer | None = None

    async def start(self) -> None:
        """Start listening for healthcheck HTTP requests."""
        self._server = await asyncio.start_server(self._handle_connection, host=self.host, port=self.port)
        logger.info("Healthcheck server listening on http://%s:%s%s", self.host, self.port, self.path)

    async def stop(self) -> None:
        """Stop the healthcheck listener if it is running."""
        if self._server is None:
            return

        self._server.close()
        await self._server.wait_closed()
        self._server = None

    async def _handle_connection(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
        """
        Process a single HTTP request and return a JSON response.

        :param reader: Stream reader for the client connection.
        :param writer: Stream writer for the client connection.
        """
        response_status = 500
        response_body: dict[str, Any] = {"status": "error"}

        try:
            request_line = await asyncio.wait_for(reader.readline(), timeout=_REQUEST_TIMEOUT_SECONDS)
            if not request_line:
                return

            method, raw_target, _ = request_line.decode("utf-8", errors="replace").strip().split(maxsplit=2)
            await self._consume_headers(reader)

            target = raw_target.split("?", maxsplit=1)[0]
            if method != "GET":
                response_status = 405
                response_body = {"status": "error", "reason": "method_not_allowed"}
            elif target != self.path:
                response_status = 404
                response_body = {"status": "error", "reason": "not_found"}
            else:
                response_status, response_body = await self._health_response()
        except (UnicodeDecodeError, ValueError):
            response_status = 400
            response_body = {"status": "error", "reason": "bad_request"}
        except TimeoutError:
            response_status = 408
            response_body = {"status": "error", "reason": "request_timeout"}
        finally:
            writer.write(self._build_response(response_status, response_body))
            with suppress(ConnectionError):
                await writer.drain()

            writer.close()
            with suppress(ConnectionError):
                await writer.wait_closed()

    async def _health_response(self) -> tuple[int, dict[str, Any]]:
        """Build the current health payload and matching HTTP status code."""
        db_connected = await self._is_db_connected()
        discord_connected = self._is_discord_connected()
        discord_unrate_limited = self._is_discord_unrate_limited()
        discord_heartbeat_ok = self._is_discord_heartbeat_healthy()

        checks = {
            "database_connected": db_connected,
            "discord_connected": discord_connected,
            "discord_no_global_ratelimit": discord_unrate_limited,
            "discord_heartbeats_healthy": discord_heartbeat_ok,
        }
        healthy = all(checks.values())
        return (
            200 if healthy else 503,
            {
                "status": "ok" if healthy else "degraded",
                "checks": checks,
            },
        )

    async def _is_db_connected(self) -> bool:
        """Return whether the configured database connection is responsive."""
        try:
            connection = Tortoise.get_connection("default")
            await connection.execute_query("SELECT 1")
        except (ConfigurationError, DBConnectionError, OperationalError):
            return False
        return True

    def _is_discord_connected(self) -> bool:
        """Return whether the Discord client is ready and not closed."""
        return self.bot.is_ready() and not self.bot.is_closed()

    def _is_discord_unrate_limited(self) -> bool:
        """Return whether the Discord websocket is not globally ratelimited."""
        return not self.bot.is_ws_ratelimited()

    def _is_discord_heartbeat_healthy(self) -> bool:
        """Return whether Discord heartbeat latencies are within the healthy threshold."""
        if isinstance(self.bot, discord.AutoShardedClient):
            return all(
                math.isfinite(latency) and 0 <= latency <= _MAX_HEARTBEAT_LATENCY_SECONDS
                for _, latency in self.bot.latencies
            )

        return math.isfinite(self.bot.latency) and 0 <= self.bot.latency <= _MAX_HEARTBEAT_LATENCY_SECONDS

    @staticmethod
    async def _consume_headers(reader: asyncio.StreamReader) -> None:
        """
        Read request headers until an empty line is reached.

        :param reader: Stream reader for the client connection.
        """
        while True:
            line = await asyncio.wait_for(reader.readline(), timeout=_REQUEST_TIMEOUT_SECONDS)
            if not line or line in {b"\r\n", b"\n"}:
                return

    @staticmethod
    def _build_response(status_code: int, body: dict[str, Any]) -> bytes:
        """
        Build a raw HTTP JSON response payload.

        :param status_code: HTTP status code to emit.
        :param body: Response body content.
        :returns: Serialized HTTP response bytes.
        """
        status_text = {
            200: "OK",
            400: "Bad Request",
            404: "Not Found",
            405: "Method Not Allowed",
            408: "Request Timeout",
            500: "Internal Server Error",
            503: "Service Unavailable",
        }.get(status_code, "Internal Server Error")
        payload = json.dumps(body, separators=(",", ":"), sort_keys=True).encode()
        headers = (
            f"HTTP/1.1 {status_code} {status_text}\r\n"
            "Content-Type: application/json\r\n"
            f"Content-Length: {len(payload)}\r\n"
            "Connection: close\r\n"
            "\r\n"
        ).encode()
        return headers + payload
