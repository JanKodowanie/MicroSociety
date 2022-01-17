-- upgrade --
CREATE TABLE IF NOT EXISTS "account" (
    "id" CHAR(36) NOT NULL  PRIMARY KEY,
    "username" VARCHAR(20) NOT NULL UNIQUE,
    "email" VARCHAR(60) NOT NULL UNIQUE,
    "password" VARCHAR(128) NOT NULL,
    "date_joined" TIMESTAMP NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "gender" VARCHAR(6) NOT NULL  /* MALE: male\nFEMALE: female */,
    "status" VARCHAR(8) NOT NULL  DEFAULT 'active' /* ACTIVE: active\nINACTIVE: inactive\nBANNED: banned */,
    "role" VARCHAR(13) NOT NULL  DEFAULT 'standard' /* STANDARD: standard\nMODERATOR: moderator\nADMINISTRATOR: administrator */
);
CREATE TABLE IF NOT EXISTS "passwordresetcode" (
    "code" CHAR(36) NOT NULL  PRIMARY KEY,
    "exp" TIMESTAMP NOT NULL  DEFAULT '2022-01-18T19:32:44.570422+00:00',
    "user_id" CHAR(36) NOT NULL UNIQUE REFERENCES "account" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "refreshtoken" (
    "id" CHAR(36) NOT NULL  PRIMARY KEY,
    "user_id" CHAR(36) NOT NULL REFERENCES "account" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "bloguser" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "picture_url" VARCHAR(300),
    "picture_path" VARCHAR(300),
    "bio" TEXT,
    "points" INT NOT NULL  DEFAULT 0,
    "rank" VARCHAR(6) NOT NULL  DEFAULT 'rank_1' /* RANK_1: rank_1\nRANK_2: rank_2\nRANK_3: rank_3 */,
    "account_id" CHAR(36) NOT NULL UNIQUE REFERENCES "account" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "employee" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "firstname" VARCHAR(30) NOT NULL,
    "lastname" VARCHAR(30) NOT NULL,
    "phone_number" VARCHAR(9) NOT NULL,
    "account_id" CHAR(36) NOT NULL UNIQUE REFERENCES "account" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "publishedevent" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "name" VARCHAR(60) NOT NULL,
    "date_created" TIMESTAMP NOT NULL  DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS "receivedevent" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "message_id" INT NOT NULL,
    "date_received" TIMESTAMP NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "name" VARCHAR(60) NOT NULL,
    "domain" VARCHAR(30) NOT NULL
);
CREATE TABLE IF NOT EXISTS "fulllogoutevent" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "user_id" CHAR(36) NOT NULL,
    "logout_date" TIMESTAMP NOT NULL
);
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(20) NOT NULL,
    "content" JSON NOT NULL
);
