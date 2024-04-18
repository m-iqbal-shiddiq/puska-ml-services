-- -------------------------------------------------------------
-- TablePlus 5.9.6(546)
--
-- https://tableplus.com/
--
-- Database: postgres
-- Generation Time: 2024-04-18 07:42:54.5910
-- -------------------------------------------------------------


-- This script only contains the table creation statements and does not fully represent the table in the database. Do not use it as a backup.

-- Sequence and defined type
CREATE SEQUENCE IF NOT EXISTS history_kelahiran_kematian_id_seq;

-- Table Definition
CREATE TABLE "public"."history_kelahiran_kematian" (
    "id" int8 NOT NULL DEFAULT nextval('history_kelahiran_kematian_id_seq'::regclass),
    "tgl_pencatatan" date NOT NULL,
    "jml_lahir_pedaging_jantan" int4 NOT NULL DEFAULT 0,
    "jml_lahir_pedaging_betina" int4 NOT NULL DEFAULT 0,
    "jml_lahir_perah_jantan" int4 NOT NULL DEFAULT 0,
    "jml_lahir_perah_betina" int4 NOT NULL DEFAULT 0,
    "jml_mati_pedaging_jantan" int4 NOT NULL DEFAULT 0,
    "jml_mati_pedaging_betina" int4 NOT NULL DEFAULT 0,
    "jml_mati_perah_jantan" int4 NOT NULL DEFAULT 0,
    "jml_mati_perah_betina" int4 NOT NULL DEFAULT 0,
    "jml_mati_pedaging_anakan_jantan" int4 NOT NULL DEFAULT 0,
    "jml_mati_pedaging_anakan_betina" int4 NOT NULL DEFAULT 0,
    "jml_mati_perah_anakan_jantan" int4 NOT NULL DEFAULT 0,
    "jml_mati_perah_anakan_betina" int4 NOT NULL DEFAULT 0,
    "created_at" timestamp(0),
    "updated_at" timestamp(0),
    "deleted_at" timestamp(0),
    "created_by" int8,
    "updated_by" int8,
    "deleted_by" int8,
    "id_peternak" int8 NOT NULL,
    CONSTRAINT "history_kelahiran_kematian_id_peternak_foreign" FOREIGN KEY ("id_peternak") REFERENCES "public"."mitra_peternak"("id"),
    PRIMARY KEY ("id")
);

INSERT INTO "public"."history_kelahiran_kematian" ("id", "tgl_pencatatan", "jml_lahir_pedaging_jantan", "jml_lahir_pedaging_betina", "jml_lahir_perah_jantan", "jml_lahir_perah_betina", "jml_mati_pedaging_jantan", "jml_mati_pedaging_betina", "jml_mati_perah_jantan", "jml_mati_perah_betina", "jml_mati_pedaging_anakan_jantan", "jml_mati_pedaging_anakan_betina", "jml_mati_perah_anakan_jantan", "jml_mati_perah_anakan_betina", "created_at", "updated_at", "deleted_at", "created_by", "updated_by", "deleted_by", "id_peternak") VALUES
(1, '2023-02-19', 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, '2023-02-19 16:04:22', '2023-02-19 16:04:22', NULL, NULL, NULL, NULL, 18),
(2, '2023-02-19', 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, '2023-02-19 16:14:08', '2023-02-19 16:14:08', NULL, NULL, NULL, NULL, 17),
(3, '2023-02-20', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, '2023-02-20 00:49:44', '2023-02-20 00:49:44', NULL, NULL, NULL, NULL, 13),
(4, '2023-02-20', 1, 2, 2, 1, 3, 1, 1, 0, 0, 0, 0, 0, '2023-02-20 00:56:22', '2023-02-20 00:56:22', NULL, NULL, NULL, NULL, 12),
(5, '2023-02-20', 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, '2023-02-20 01:57:31', '2023-02-20 01:57:31', NULL, NULL, NULL, NULL, 10),
(6, '2023-02-20', 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, '2023-02-20 05:40:50', '2023-02-20 05:40:50', NULL, NULL, NULL, NULL, 13),
(7, '2023-02-20', 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, '2023-02-20 05:43:18', '2023-02-20 05:43:18', NULL, NULL, NULL, NULL, 13),
(8, '2023-02-20', 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, '2023-02-20 05:49:32', '2023-02-20 05:49:32', NULL, NULL, NULL, NULL, 14),
(9, '2023-02-20', 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, '2023-02-20 05:49:48', '2023-02-20 05:49:48', NULL, NULL, NULL, NULL, 14),
(10, '2023-02-20', 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, '2023-02-20 09:18:07', '2023-02-20 09:18:07', NULL, NULL, NULL, NULL, 15),
(11, '2023-02-20', 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, '2023-02-20 09:18:58', '2023-02-20 09:18:58', NULL, NULL, NULL, NULL, 15),
(12, '2023-02-20', 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, '2023-02-20 09:27:37', '2023-02-20 09:27:37', NULL, NULL, NULL, NULL, 16),
(13, '2023-02-21', 1, 1, 1, 1, 3, 1, 0, 2, 0, 0, 0, 0, '2023-02-21 15:57:03', '2023-02-21 15:57:03', NULL, NULL, NULL, NULL, 17),
(14, '2023-03-15', 0, 1, 0, 2, 0, 1, 1, 0, 0, 0, 0, 0, '2023-03-14 17:14:41', '2023-03-14 17:14:41', NULL, NULL, NULL, NULL, 9),
(16, '2023-04-01', 0, 2, 3, 0, 1, 0, 0, 0, 1, 0, 0, 0, '2023-04-01 17:14:41', '2023-04-01 17:14:41', NULL, NULL, NULL, NULL, 5),
(17, '2023-04-01', 3, 2, 1, 3, 2, 1, 1, 1, 1, 1, 0, 0, '2023-04-01 17:14:41', '2023-04-01 17:14:41', NULL, NULL, NULL, NULL, 7),
(18, '2023-04-08', 0, 3, 0, 3, 0, 1, 2, 0, 0, 1, 1, 1, '2023-04-08 17:14:41', '2023-04-08 17:14:41', NULL, NULL, NULL, NULL, 7),
(21, '2023-07-04', 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, '2023-07-04 10:27:29', '2023-07-04 10:27:29', NULL, NULL, NULL, NULL, 17),
(22, '2023-07-04', 1, 1, 2, 1, 0, 0, 0, 0, 0, 0, 0, 0, '2023-07-04 15:36:45', '2023-07-04 15:36:45', NULL, NULL, NULL, NULL, 24),
(23, '2023-07-18', 1, 2, 3, 4, 0, 0, 0, 0, 0, 0, 0, 0, '2023-07-18 15:06:14', '2023-07-18 15:06:14', NULL, NULL, NULL, NULL, 17),
(24, '2023-07-18', 2, 3, 1, 4, 0, 0, 0, 0, 0, 0, 0, 0, '2023-07-18 15:10:08', '2023-07-18 15:10:08', NULL, NULL, NULL, NULL, 24),
(25, '2023-07-21', 2, 4, 3, 2, 0, 0, 0, 0, 0, 0, 0, 0, '2023-07-21 14:42:20', '2023-07-21 14:42:20', NULL, NULL, NULL, NULL, 17),
(26, '2023-07-29', 2, 5, 3, 4, 0, 0, 0, 0, 0, 0, 0, 0, '2023-07-29 11:53:23', '2023-07-29 11:53:23', NULL, NULL, NULL, NULL, 17),
(27, '2023-07-29', 1, 1, 5, 2, 0, 0, 0, 0, 0, 0, 0, 0, '2023-07-29 11:59:03', '2023-07-29 11:59:03', NULL, NULL, NULL, NULL, 24),
(28, '2023-08-04', 5, 2, 3, 4, 0, 0, 0, 0, 0, 0, 0, 0, '2023-08-04 12:38:56', '2023-08-04 12:38:56', NULL, NULL, NULL, NULL, 17),
(29, '2023-08-04', 1, 2, 3, 5, 0, 0, 0, 0, 0, 0, 0, 0, '2023-08-04 12:49:04', '2023-08-04 12:49:04', NULL, NULL, NULL, NULL, 24),
(30, '2023-08-12', 1, 2, 3, 4, 0, 0, 0, 0, 0, 0, 0, 0, '2023-08-12 11:48:41', '2023-08-12 11:48:41', NULL, NULL, NULL, NULL, 17),
(31, '2023-08-12', 2, 3, 4, 2, 0, 0, 0, 0, 0, 0, 0, 0, '2023-08-12 11:58:56', '2023-08-12 11:58:56', NULL, NULL, NULL, NULL, 24),
(32, '2023-08-19', 2, 4, 3, 4, 0, 0, 0, 0, 0, 0, 0, 0, '2023-08-19 11:29:04', '2023-08-19 11:29:04', NULL, NULL, NULL, NULL, 17),
(33, '2023-08-19', 5, 1, 4, 2, 0, 0, 0, 0, 0, 0, 0, 0, '2023-08-19 11:35:06', '2023-08-19 11:35:06', NULL, NULL, NULL, NULL, 10),
(34, '2023-08-26', 2, 3, 5, 2, 0, 0, 0, 0, 0, 0, 0, 0, '2023-08-26 12:16:13', '2023-08-26 12:16:13', NULL, NULL, NULL, NULL, 17),
(35, '2023-08-26', 2, 5, 5, 2, 0, 0, 0, 0, 0, 0, 0, 0, '2023-08-26 12:23:26', '2023-08-26 12:23:26', NULL, NULL, NULL, NULL, 9),
(36, '2023-09-02', 5, 4, 3, 2, 0, 0, 0, 0, 0, 0, 0, 0, '2023-09-02 14:01:59', '2023-09-02 14:01:59', NULL, NULL, NULL, NULL, 17),
(37, '2023-09-02', 3, 4, 5, 2, 1, 1, 0, 3, 0, 0, 0, 0, '2023-09-02 14:07:40', '2023-09-02 14:07:40', NULL, NULL, NULL, NULL, 24),
(38, '2023-09-09', 3, 1, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, '2023-09-09 12:25:18', '2023-09-09 12:25:18', NULL, NULL, NULL, NULL, 17),
(39, '2023-09-09', 3, 1, 3, 3, 2, 1, 0, 0, 0, 0, 0, 0, '2023-09-09 13:09:07', '2023-09-09 13:09:07', NULL, NULL, NULL, NULL, 24),
(40, '2023-09-16', 3, 5, 2, 4, 0, 0, 0, 0, 0, 0, 0, 0, '2023-09-16 11:22:46', '2023-09-16 11:22:46', NULL, NULL, NULL, NULL, 17),
(41, '2023-09-16', 3, 4, 5, 2, 0, 0, 0, 0, 0, 0, 0, 0, '2023-09-16 11:29:53', '2023-09-16 11:29:53', NULL, NULL, NULL, NULL, 10),
(42, '2023-09-23', 5, 1, 4, 3, 0, 0, 0, 0, 0, 0, 0, 0, '2023-09-23 14:13:52', '2023-09-23 14:13:52', NULL, NULL, NULL, NULL, 17),
(43, '2023-09-23', 4, 5, 3, 3, 0, 0, 0, 0, 0, 0, 0, 0, '2023-09-23 14:20:29', '2023-09-23 14:20:29', NULL, NULL, NULL, NULL, 24),
(44, '2023-09-30', 4, 2, 3, 2, 0, 0, 0, 0, 0, 0, 0, 0, '2023-09-30 09:12:09', '2023-09-30 09:12:09', NULL, NULL, NULL, NULL, 17),
(45, '2023-09-30', 4, 5, 2, 5, 0, 0, 0, 0, 0, 0, 0, 0, '2023-09-30 09:16:48', '2023-09-30 09:16:48', NULL, NULL, NULL, NULL, 9),
(46, '2023-10-08', 2, 2, 4, 2, 3, 4, 0, 0, 0, 0, 0, 0, '2023-10-07 17:01:49', '2023-10-07 17:01:49', NULL, NULL, NULL, NULL, 17),
(47, '2023-10-08', 3, 2, 2, 5, 4, 0, 0, 0, 0, 0, 0, 0, '2023-10-07 17:07:16', '2023-10-07 17:07:16', NULL, NULL, NULL, NULL, 10),
(48, '2023-10-14', 2, 3, 5, 2, 0, 0, 0, 0, 0, 0, 0, 0, '2023-10-14 14:24:02', '2023-10-14 14:24:02', NULL, NULL, NULL, NULL, 17),
(49, '2023-10-14', 2, 5, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0, '2023-10-14 15:18:56', '2023-10-14 15:18:56', NULL, NULL, NULL, NULL, 24),
(50, '2023-10-21', 4, 3, 5, 3, 0, 0, 0, 0, 0, 0, 0, 0, '2023-10-21 11:49:37', '2023-10-21 11:49:37', NULL, NULL, NULL, NULL, 17),
(51, '2023-10-21', 4, 5, 1, 4, 3, 2, 0, 0, 0, 0, 0, 0, '2023-10-21 11:54:32', '2023-10-21 11:54:32', NULL, NULL, NULL, NULL, 24),
(52, '2024-02-23', 40, 45, 12, 13, 5, 4, 23, 24, 0, 0, 0, 0, '2024-02-23 14:28:11', '2024-02-23 14:28:11', NULL, NULL, NULL, NULL, 4);
