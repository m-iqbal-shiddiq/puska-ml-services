-- -------------------------------------------------------------
-- TablePlus 5.9.6(546)
--
-- https://tableplus.com/
--
-- Database: postgres
-- Generation Time: 2024-04-18 07:43:16.4490
-- -------------------------------------------------------------


-- This script only contains the table creation statements and does not fully represent the table in the database. Do not use it as a backup.

-- Sequence and defined type
CREATE SEQUENCE IF NOT EXISTS history_populasi_id_seq;

-- Table Definition
CREATE TABLE "public"."history_populasi" (
    "id" int8 NOT NULL DEFAULT nextval('history_populasi_id_seq'::regclass),
    "tgl_pencatatan" date NOT NULL,
    "jml_pedaging_jantan" int4 NOT NULL DEFAULT 0,
    "jml_pedaging_betina" int4 NOT NULL DEFAULT 0,
    "jml_pedaging_anakan_jantan" int4 NOT NULL DEFAULT 0,
    "jml_pedaging_anakan_betina" int4 NOT NULL DEFAULT 0,
    "jml_perah_jantan" int4 NOT NULL DEFAULT 0,
    "jml_perah_betina" int4 NOT NULL DEFAULT 0,
    "jml_perah_anakan_jantan" int4 NOT NULL DEFAULT 0,
    "jml_perah_anakan_betina" int4 NOT NULL DEFAULT 0,
    "created_at" timestamp(0),
    "updated_at" timestamp(0),
    "deleted_at" timestamp(0),
    "created_by" int8,
    "updated_by" int8,
    "deleted_by" int8,
    "id_peternak" int8 NOT NULL,
    CONSTRAINT "history_populasi_id_peternak_foreign" FOREIGN KEY ("id_peternak") REFERENCES "public"."mitra_peternak"("id"),
    PRIMARY KEY ("id")
);

INSERT INTO "public"."history_populasi" ("id", "tgl_pencatatan", "jml_pedaging_jantan", "jml_pedaging_betina", "jml_pedaging_anakan_jantan", "jml_pedaging_anakan_betina", "jml_perah_jantan", "jml_perah_betina", "jml_perah_anakan_jantan", "jml_perah_anakan_betina", "created_at", "updated_at", "deleted_at", "created_by", "updated_by", "deleted_by", "id_peternak") VALUES
(1, '2023-02-19', 4, 10, 3, 5, 3, 6, 2, 1, '2023-02-19 16:00:23', '2023-02-19 16:00:23', NULL, NULL, NULL, NULL, 18),
(2, '2023-02-19', 3, 7, 3, 2, 3, 2, 1, 2, '2023-02-19 16:13:10', '2023-02-19 16:13:10', NULL, NULL, NULL, NULL, 17),
(3, '2023-02-19', 1, 9, 3, 8, 2, 12, 2, 6, '2023-02-19 16:19:12', '2023-02-19 16:19:12', NULL, NULL, NULL, NULL, 19),
(4, '2023-02-20', 2, 6, 2, 1, 2, 1, 0, 1, '2023-02-20 00:30:49', '2023-02-20 00:30:49', NULL, NULL, NULL, NULL, 20),
(5, '2023-02-20', 5, 5, 3, 10, 3, 7, 3, 2, '2023-02-20 00:54:30', '2023-02-20 00:54:30', NULL, NULL, NULL, NULL, 12),
(6, '2023-02-20', 9, 9, 15, 11, 7, 5, 8, 5, '2023-02-20 01:57:06', '2023-02-20 01:57:06', NULL, NULL, NULL, NULL, 10),
(7, '2023-02-20', 5, 5, 3, 10, 3, 7, 3, 2, '2023-02-20 05:38:08', '2023-02-20 05:38:08', NULL, NULL, NULL, NULL, 13),
(8, '2023-02-20', 3, 6, 4, 8, 2, 6, 3, 3, '2023-02-20 05:39:06', '2023-02-20 05:39:06', NULL, NULL, NULL, NULL, 13),
(9, '2023-02-20', 5, 5, 3, 10, 3, 7, 3, 2, '2023-02-20 05:45:02', '2023-02-20 05:45:02', NULL, NULL, NULL, NULL, 14),
(10, '2023-02-20', 3, 6, 4, 8, 2, 6, 3, 3, '2023-02-20 05:47:06', '2023-02-20 05:47:06', NULL, NULL, NULL, NULL, 14),
(11, '2023-02-20', 4, 10, 3, 5, 3, 6, 2, 1, '2023-02-20 09:12:29', '2023-02-20 09:12:29', NULL, NULL, NULL, NULL, 15),
(12, '2023-02-20', 4, 9, 3, 8, 2, 12, 2, 6, '2023-02-20 09:16:32', '2023-02-20 09:16:32', NULL, NULL, NULL, NULL, 15),
(13, '2023-02-20', 3, 6, 4, 8, 2, 6, 3, 3, '2023-02-20 09:17:39', '2023-02-20 09:17:39', NULL, NULL, NULL, NULL, 12),
(14, '2023-02-20', 4, 9, 3, 8, 2, 12, 2, 6, '2023-02-20 09:26:00', '2023-02-20 09:26:00', NULL, NULL, NULL, NULL, 16),
(15, '2023-02-20', 4, 10, 3, 5, 3, 6, 2, 1, '2023-02-20 09:26:54', '2023-02-20 09:26:54', NULL, NULL, NULL, NULL, 7),
(16, '2023-02-21', 3, 7, 3, 2, 3, 2, 1, 2, '2023-02-21 15:55:59', '2023-02-21 15:55:59', NULL, NULL, NULL, NULL, 17),
(17, '2023-03-02', 3, 2, 2, 1, 1, 1, 1, 1, '2023-03-02 04:13:45', '2023-03-02 04:13:45', NULL, NULL, NULL, NULL, 10),
(18, '2023-03-02', 0, 0, 0, 0, 0, 0, 0, 0, '2023-03-02 16:45:31', '2023-03-02 16:45:31', NULL, NULL, NULL, NULL, 9),
(19, '2023-03-06', 10, 9, 8, 7, 6, 5, 4, 3, '2023-03-05 17:49:57', '2023-03-05 17:49:57', NULL, NULL, NULL, NULL, 4),
(20, '2023-04-04', 3, 6, 2, 1, 2, 5, 1, 2, '2023-04-03 22:08:48', '2023-04-03 22:08:48', NULL, NULL, NULL, NULL, 7),
(21, '2023-05-07', 4, 5, 1, 1, 2, 10, 1, 1, '2023-05-07 03:05:53', '2023-05-07 03:05:53', NULL, NULL, NULL, NULL, 9),
(22, '2023-06-10', 10, 2, 2, 3, 0, 10, 0, 2, '2023-06-10 09:20:20', '2023-06-10 09:20:20', NULL, NULL, NULL, NULL, 8),
(23, '2023-07-01', 2, 20, 0, 0, 1, 10, 0, 0, '2023-07-01 05:20:40', '2023-07-01 05:20:40', NULL, NULL, NULL, NULL, 25),
(24, '2023-07-04', 5, 7, 3, 2, 3, 2, 1, 2, '2023-07-04 10:26:46', '2023-07-04 10:26:46', NULL, NULL, NULL, NULL, 17),
(25, '2023-07-04', 3, 2, 1, 5, 1, 2, 1, 1, '2023-07-04 15:36:21', '2023-07-04 15:36:21', NULL, NULL, NULL, NULL, 24),
(26, '2023-07-18', 1, 2, 3, 2, 2, 1, 1, 1, '2023-07-18 15:05:47', '2023-07-18 15:05:47', NULL, NULL, NULL, NULL, 17),
(27, '2023-07-18', 2, 5, 4, 3, 1, 3, 5, 2, '2023-07-18 15:09:51', '2023-07-18 15:09:51', NULL, NULL, NULL, NULL, 24),
(28, '2023-07-21', 1, 2, 2, 4, 1, 1, 3, 2, '2023-07-21 14:42:05', '2023-07-21 14:42:05', NULL, NULL, NULL, NULL, 17),
(29, '2023-07-29', 1, 2, 3, 4, 5, 1, 1, 1, '2023-07-29 11:53:10', '2023-07-29 11:53:10', NULL, NULL, NULL, NULL, 17),
(30, '2023-07-29', 1, 1, 5, 4, 3, 1, 2, 4, '2023-07-29 11:58:51', '2023-07-29 11:58:51', NULL, NULL, NULL, NULL, 24),
(31, '2023-08-04', 5, 2, 2, 4, 1, 3, 4, 2, '2023-08-04 12:38:38', '2023-08-04 12:38:38', NULL, NULL, NULL, NULL, 17),
(32, '2023-08-04', 5, 2, 5, 1, 2, 3, 4, 1, '2023-08-04 12:48:53', '2023-08-04 12:48:53', NULL, NULL, NULL, NULL, 24),
(33, '2023-08-12', 3, 4, 1, 1, 2, 3, 1, 5, '2023-08-12 11:48:23', '2023-08-12 11:48:23', NULL, NULL, NULL, NULL, 17),
(34, '2023-08-12', 1, 3, 2, 5, 4, 3, 1, 2, '2023-08-12 11:58:43', '2023-08-12 11:58:43', NULL, NULL, NULL, NULL, 24),
(35, '2023-08-19', 2, 3, 3, 4, 1, 2, 2, 5, '2023-08-19 11:28:49', '2023-08-19 11:28:49', NULL, NULL, NULL, NULL, 17),
(36, '2023-08-19', 2, 4, 1, 1, 3, 4, 2, 1, '2023-08-19 11:34:54', '2023-08-19 11:34:54', NULL, NULL, NULL, NULL, 10),
(37, '2023-08-26', 5, 4, 1, 3, 3, 2, 1, 4, '2023-08-26 12:15:56', '2023-08-26 12:15:56', NULL, NULL, NULL, NULL, 17),
(38, '2023-08-26', 2, 3, 4, 2, 3, 4, 4, 1, '2023-08-26 12:23:12', '2023-08-26 12:23:12', NULL, NULL, NULL, NULL, 9),
(39, '2023-09-02', 2, 3, 4, 1, 2, 2, 5, 1, '2023-09-02 14:01:45', '2023-09-02 14:01:45', NULL, NULL, NULL, NULL, 17),
(40, '2023-09-02', 5, 2, 3, 2, 1, 1, 4, 5, '2023-09-02 14:07:23', '2023-09-02 14:07:23', NULL, NULL, NULL, NULL, 24),
(41, '2023-09-09', 1, 3, 4, 1, 2, 2, 3, 4, '2023-09-09 12:24:54', '2023-09-09 12:24:54', NULL, NULL, NULL, NULL, 17),
(42, '2023-09-09', 2, 3, 1, 1, 2, 3, 4, 1, '2023-09-09 13:08:48', '2023-09-09 13:08:48', NULL, NULL, NULL, NULL, 24),
(43, '2023-09-16', 1, 2, 3, 4, 5, 1, 2, 2, '2023-09-16 11:22:36', '2023-09-16 11:22:36', NULL, NULL, NULL, NULL, 17),
(44, '2023-09-16', 1, 3, 2, 4, 2, 2, 3, 4, '2023-09-16 11:29:35', '2023-09-16 11:29:35', NULL, NULL, NULL, NULL, 10),
(45, '2023-09-23', 2, 3, 4, 1, 2, 4, 2, 5, '2023-09-23 14:13:40', '2023-09-23 14:13:40', NULL, NULL, NULL, NULL, 17),
(46, '2023-09-23', 3, 4, 2, 1, 5, 3, 4, 4, '2023-09-23 14:20:15', '2023-09-23 14:20:15', NULL, NULL, NULL, NULL, 24),
(47, '2023-09-30', 2, 5, 3, 4, 1, 2, 1, 4, '2023-09-30 09:11:56', '2023-09-30 09:11:56', NULL, NULL, NULL, NULL, 17),
(48, '2023-09-30', 3, 4, 2, 5, 2, 2, 1, 4, '2023-09-30 09:16:37', '2023-09-30 09:16:37', NULL, NULL, NULL, NULL, 9),
(49, '2023-10-08', 1, 3, 2, 4, 5, 1, 4, 2, '2023-10-07 17:01:30', '2023-10-07 17:01:30', NULL, NULL, NULL, NULL, 17),
(50, '2023-10-08', 2, 2, 3, 1, 4, 2, 5, 1, '2023-10-07 17:07:00', '2023-10-07 17:07:00', NULL, NULL, NULL, NULL, 10),
(51, '2023-10-14', 2, 4, 2, 2, 3, 4, 5, 1, '2023-10-14 14:23:53', '2023-10-14 14:23:53', NULL, NULL, NULL, NULL, 17),
(52, '2023-10-14', 3, 4, 2, 1, 4, 3, 2, 2, '2023-10-14 15:18:42', '2023-10-14 15:18:42', NULL, NULL, NULL, NULL, 24),
(53, '2023-10-21', 2, 3, 5, 1, 2, 2, 4, 3, '2023-10-21 11:49:26', '2023-10-21 11:49:26', NULL, NULL, NULL, NULL, 17),
(54, '2023-10-21', 4, 1, 5, 3, 2, 4, 1, 3, '2023-10-21 11:54:18', '2023-10-21 11:54:18', NULL, NULL, NULL, NULL, 24);
