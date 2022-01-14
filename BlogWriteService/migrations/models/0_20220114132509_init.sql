-- upgrade --
CREATE TABLE IF NOT EXISTS "post" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "creator_id" CHAR(36) NOT NULL,
    "content" TEXT NOT NULL,
    "picture_url" VARCHAR(300),
    "picture_path" VARCHAR(300),
    "date_created" TIMESTAMP NOT NULL  DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS "comment" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "creator_id" CHAR(36) NOT NULL,
    "content" TEXT NOT NULL,
    "date_created" TIMESTAMP NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "post_id" INT NOT NULL REFERENCES "post" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "tag" (
    "name" VARCHAR(30) NOT NULL  PRIMARY KEY,
    "date_created" TIMESTAMP NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "popularity" INT NOT NULL  DEFAULT 0
);
CREATE TABLE IF NOT EXISTS "publishedevent" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "name" VARCHAR(60) NOT NULL,
    "date_created" TIMESTAMP NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "body" TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS "receivedevent" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "message_id" INT NOT NULL,
    "date_received" TIMESTAMP NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "domain" VARCHAR(30) NOT NULL
);
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(20) NOT NULL,
    "content" JSON NOT NULL
);
CREATE TABLE IF NOT EXISTS "post_tag" (
    "post_id" INT NOT NULL REFERENCES "post" ("id") ON DELETE CASCADE,
    "tag_id" VARCHAR(30) NOT NULL REFERENCES "tag" ("name") ON DELETE CASCADE
);
