/*
 Navicat Premium Data Transfer

 Source Server         : dayone
 Source Server Type    : SQLite
 Source Server Version : 3008004
 Source Database       : main

 Target Server Type    : SQLite
 Target Server Version : 3008004
 File Encoding         : utf-8

 Date: 11/02/2015 22:14:11 PM
*/

PRAGMA foreign_keys = false;

-- ----------------------------
--  Table structure for Dayone_entry
-- ----------------------------
DROP TABLE IF EXISTS "Dayone_entry";
CREATE VIRTUAL TABLE  "Dayone_entry" USING fts4("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
"uuid" varchar(32) NOT NULL UNIQUE, "date" datetime NOT NULL, "text" text NOT NULL, tokenize=unicode61);

-- ----------------------------
--  Table structure for Dayone_entry_tags
-- ----------------------------
DROP TABLE IF EXISTS "Dayone_entry_tags";
CREATE TABLE "Dayone_entry_tags" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "entry_id" integer NOT NULL REFERENCES "Dayone_entry" ("id"), "tag_id" integer NOT NULL REFERENCES "Dayone_tag" ("id"), UNIQUE ("entry_id", "tag_id"));

-- ----------------------------
--  Table structure for Dayone_tag
-- ----------------------------
DROP TABLE IF EXISTS "Dayone_tag";
CREATE TABLE "Dayone_tag" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "name" varchar(255) NOT NULL);

-- ----------------------------
--  Indexes structure for table Dayone_entry_tags
-- ----------------------------
CREATE INDEX "Dayone_entry_tags_b64a62ea" ON "Dayone_entry_tags" ("entry_id");
CREATE INDEX "Dayone_entry_tags_76f094bc" ON "Dayone_entry_tags" ("tag_id");

PRAGMA foreign_keys = true;
