from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "guild" (
    "discord_id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL
);
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSON NOT NULL
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """


MODELS_STATE = (
    "eJzVlVFr2zAUhf9KyFMH3UidpE73lgTaZWwptN0olGIUW3FEZMmVrreWkv9eXdmxHDsxHQ"
    "zavsXn3Cvd+/mYPHcTGVGuv1xkjEfdr53nriAJNT92jeNOl6Spk1EAsuC2Mi5LFhoUCcGI"
    "S8I1NVJEdahYCkwKo4qMcxRlaAqZiJ2UCfaQ0QBkTGFFlTHu7o3MREQfqd4+putgyWht0I"
    "jpUKooYHYG6wfwlFpvwuKZgHPbgxcvglDyLBHNvvQJVlKUjUwAqjEVVBGgeCOoDDfCgYvN"
    "t0vmw7uSfOpKT0SXJONQIfBKLKEUiNRMo+3OMd7y+czz+n3f6/VPR8OB7w9HvZGptSM1LX"
    "+TL+7A5EdZPLOL2fwGF5XmveVvE4WN7SFA8q6S/3JdExYkXP8lBmLDkZ48VNu0Ei+pK0SQ"
    "2CJEEjhOkccxVSxc7Utq4bRGlbiaN8nqvoweDOjHC6Z3MvAHo/7poMxjqbTF8FDkHLc/VG"
    "kcqQFvuiJqP71KSw2hGbyOcAusjeFWcBBdcP4TxYQ8BpyKGDDg3nDYwuz3+Gr6bXx1ZKo+"
    "7X7A88Lycg/BOpD4afwDxKL8YwI86fVeAdBUHQRovV2A5kag+Te4C/H79eV8P8RKSw3kL2"
    "EWvItYCMcdzjTcv0+sLRRxaxw60fqBV+Ed/Rzf1rlOf1xOLAWpIVb2FHvAxDB+07+XzQsl"
    "094c"
)
