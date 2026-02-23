from tortoise import fields
from tortoise.models import Model


class Guild(Model):
    discord_id: fields.Field[int] = fields.BigIntField(pk=True)


__all__ = ["Guild"]
