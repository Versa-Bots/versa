from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "guild" (
    "id" CHAR(36) NOT NULL PRIMARY KEY,
    "discord_id" BIGINT NOT NULL UNIQUE
);
CREATE TABLE IF NOT EXISTS "user" (
    "id" CHAR(36) NOT NULL PRIMARY KEY,
    "discord_id" BIGINT NOT NULL UNIQUE
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
    "eJztlW1v2jAUhf8KyqdW6hANL2HTNAmY1jFtVOrGNKmqIhObYOHYaWxvrRD/fb5OICSBqK"
    "02jUl84eXcY3zvo3vIyokEJkw2rzRl2HnTWDkcRcR8KBYuGg6K41wGQaEZs85wa5lJlaBA"
    "GXGOmCRGwkQGCY0VFdyoXDMGogiMkfIwlzSn95r4SoRELUhiCrd3RqYckwciN1/jpT+npN"
    "QotXdb3VePsdWm0/H7D9YJ1838QDAd8dwdP6qF4Fu71hQ34QzUQsJJghTBO2NAl9m4Gynt"
    "2Agq0WTbKs4FTOZIM4DhvJ1rHgCDBtzUa8Kr9855Bp9AcGBLuQIYq3U6Vj60VR24a/RxcH"
    "PW7p3bMYVUYWKLFomztgeRQulRCzYniakMRIL9fUSHNBxztZ9p8VyJrWn571DdwHoZQdOQ"
    "eXv12nXbbc9ttXv9bsfzuv1W33htS9WSV4N9OL4aT77BpMJEIA0GCOs1LO58uQMchBkKlr"
    "+QYVapCFcc8lZLkRuVFcRRaIHB3NBwFuSptLGqBNzqtfnWG8cp3qd4n+J9nPEekIQGi30B"
    "zyq1EUe552hCfnAfn7qH2UodwRq6lx2v02/3Otvt2yp1S5cuWF2kf5JEQksVeKMFSvbT2z"
    "lSQmgaf0mUN0IOMV+cP0QxQg8+IzxUsOBut1vD7Pvgxv5FGtd5Ma6TrOSmNQCbg4RoPANi"
    "Zv8/AV62Wk8AaFwHAdpaEaC5UZE0g0WIn75eT/ZD3DlSAjnlZsBbTAN10WBUqrvjxFpDEa"
    "aGpiMp79kuvLMvgx9lrqPP18Py8xx+YPivHy/r3+NBfF8="
)
