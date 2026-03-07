from uuid import UUID

from tortoise import fields
from tortoise.models import Model
from uuid6 import uuid7


class Guild(Model):
    id: fields.Field[UUID] = fields.UUIDField(pk=True, default=uuid7)
    discord_id: fields.Field[int] = fields.BigIntField(unique=True)


__all__ = ["Guild"]
