import asyncio
import json
import logging
from contextlib import suppress
from typing import Any

import discord
from tortoise import Tortoise
from tortoise.exceptions import ConfigurationError, DBConnectionError, OperationalError

logger = logging.getLogger(__name__)

_REQUEST_TIMEOUT_SECONDS = 5


class HealthcheckServer:
    def __init__(
        self,
        bot: discord.Bot,
        *,
        host: str,
        port: int,
        path: str = "/",
    ) -> None:
        self.bot = bot
        self.host = host
        self.port = port
        self.path = path
        self._server: asyncio.AbstractServer | None = None

    async def start(self) -> None:
        self._server = await asyncio.start_server(self._handle_connection, host=self.host, port=self.port)
        logger.info("Healthcheck server listening on http://%s:%s%s", self.host, self.port, self.path)

    async def stop(self) -> None:
        if self._server is None:
            return

        self._server.close()
        await self._server.wait_closed()
        self._server = None

    async def _handle_connection(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
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
        db_connected = await self._is_db_connected()
        discord_connected = self._is_discord_connected()
        discord_unrate_limited = self._is_discord_unrate_limited()

        checks = {
            "database_connected": db_connected,
            "discord_connected": discord_connected,
            "discord_no_global_ratelimit": discord_unrate_limited,
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
        try:
            connection = Tortoise.get_connection("default")
            await connection.execute_query("SELECT 1")
        except (ConfigurationError, DBConnectionError, OperationalError):
            return False
        return True

    def _is_discord_connected(self) -> bool:
        return self.bot.is_ready() and not self.bot.is_closed()

    def _is_discord_unrate_limited(self) -> bool:
        global_rate_limit_gate = getattr(self.bot.http, "_global_over", None)
        if isinstance(global_rate_limit_gate, asyncio.Event):
            return global_rate_limit_gate.is_set()
        return not self.bot.is_ws_ratelimited()

    async def _consume_headers(self, reader: asyncio.StreamReader) -> None:
        while True:
            line = await asyncio.wait_for(reader.readline(), timeout=_REQUEST_TIMEOUT_SECONDS)
            if not line or line in {b"\r\n", b"\n"}:
                return

    def _build_response(self, status_code: int, body: dict[str, Any]) -> bytes:
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
