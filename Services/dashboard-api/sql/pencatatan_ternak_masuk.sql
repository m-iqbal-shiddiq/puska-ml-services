-- -------------------------------------------------------------
-- TablePlus 5.9.6(546)
--
-- https://tableplus.com/
--
-- Database: postgres
-- Generation Time: 2024-04-18 07:44:56.5610
-- -------------------------------------------------------------


-- This script only contains the table creation statements and does not fully represent the table in the database. Do not use it as a backup.

-- Sequence and defined type
CREATE SEQUENCE IF NOT EXISTS pencatatan_ternak_masuk_id_seq;

-- Table Definition
CREATE TABLE "public"."pencatatan_ternak_masuk" (
    "id" int8 NOT NULL DEFAULT nextval('pencatatan_ternak_masuk_id_seq'::regclass),
    "tgl_pencatatan" date NOT NULL,
    "jenis_mitra_pengirim" varchar(255) NOT NULL,
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
    CONSTRAINT "pencatatan_ternak_masuk_id_peternak_foreign" FOREIGN KEY ("id_peternak") REFERENCES "public"."mitra_peternak"("id"),
    PRIMARY KEY ("id")
);

INSERT INTO "public"."pencatatan_ternak_masuk" ("id", "tgl_pencatatan", "jenis_mitra_pengirim", "jml_pedaging_jantan", "jml_pedaging_betina", "jml_pedaging_anakan_jantan", "jml_pedaging_anakan_betina", "jml_perah_jantan", "jml_perah_betina", "jml_perah_anakan_jantan", "jml_perah_anakan_betina", "created_at", "updated_at", "deleted_at", "created_by", "updated_by", "deleted_by", "id_peternak") VALUES
(1, '2023-02-19', 'Pengepul', 2, 1, 3, 2, 5, 1, 4, 1, '2023-02-19 16:06:26', '2023-02-19 16:06:26', NULL, NULL, NULL, NULL, 18),
(2, '2023-02-19', 'Peternakan Sendiri', 0, 0, 0, 0, 0, 0, 0, 0, '2023-02-19 16:15:03', '2023-02-19 16:15:03', NULL, NULL, NULL, NULL, 17),
(3, '2023-02-20', 'Pengepul', 1, 0, 1, 0, 0, 1, 1, 2, '2023-02-20 00:57:09', '2023-02-20 00:57:09', NULL, NULL, NULL, NULL, 12),
(4, '2023-02-20', 'Peternakan Sendiri', 2, 3, 1, 0, 2, 2, 0, 1, '2023-02-20 00:57:34', '2023-02-20 00:57:34', NULL, NULL, NULL, NULL, 12),
(5, '2023-02-20', 'Peternakan Sendiri', 0, 0, 2, 0, 0, 0, 0, 2, '2023-02-20 01:58:16', '2023-02-20 01:58:16', NULL, NULL, NULL, NULL, 10),
(6, '2023-02-20', 'Pengepul', 2, 3, 1, 0, 0, 0, 4, 5, '2023-02-20 06:07:57', '2023-02-20 06:07:57', NULL, NULL, NULL, NULL, 13),
(7, '2023-02-20', 'Peternakan Lain', 2, 3, 0, 0, 4, 3, 1, 2, '2023-02-20 06:08:28', '2023-02-20 06:08:28', NULL, NULL, NULL, NULL, 13),
(8, '2023-02-20', 'Peternakan Sendiri', 1, 1, 1, 1, 2, 2, 1, 1, '2023-02-20 09:21:13', '2023-02-20 09:21:13', NULL, NULL, NULL, NULL, 15),
(9, '2023-02-20', 'Peternakan Lain', 1, 1, 2, 2, 1, 1, 1, 1, '2023-02-20 09:21:52', '2023-02-20 09:21:52', NULL, NULL, NULL, NULL, 15),
(10, '2023-02-20', 'Peternakan Lain', 1, 1, 1, 1, 2, 2, 1, 1, '2023-02-20 09:28:36', '2023-02-20 09:28:36', NULL, NULL, NULL, NULL, 16),
(11, '2023-02-21', 'Peternakan Sendiri', 2, 1, 5, 1, 1, 1, 1, 3, '2023-02-21 15:57:51', '2023-02-21 15:57:51', NULL, NULL, NULL, NULL, 17),
(12, '2023-03-15', 'Peternakan Sendiri', 2, 2, 0, 1, 1, 3, 0, 1, '2023-03-14 17:24:19', '2023-03-14 17:24:19', NULL, NULL, NULL, NULL, 9),
(13, '2023-04-15', 'Peternakan Sendiri', 2, 2, 0, 1, 1, 3, 0, 1, '2023-03-14 17:24:19', '2023-03-14 17:24:19', NULL, NULL, NULL, NULL, 7),
(15, '2023-06-15', 'Peternakan Sendiri', 0, 15, 0, 0, 0, 0, 0, 0, '2023-06-14 17:20:50', '2023-06-14 17:20:50', NULL, NULL, NULL, NULL, 35),
(16, '2023-07-04', 'Peternakan Sendiri', 1, 3, 5, 4, 2, 3, 1, 1, '2023-07-04 10:28:11', '2023-07-04 10:28:11', NULL, NULL, NULL, NULL, 17),
(17, '2023-07-04', 'Peternakan Sendiri', 1, 2, 3, 5, 1, 1, 2, 1, '2023-07-04 15:37:10', '2023-07-04 15:37:10', NULL, NULL, NULL, NULL, 24),
(18, '2023-07-18', 'Peternakan Sendiri', 2, 1, 5, 4, 1, 3, 3, 3, '2023-07-18 15:06:40', '2023-07-18 15:06:40', NULL, NULL, NULL, NULL, 17),
(19, '2023-07-18', 'Peternakan Sendiri', 5, 1, 3, 4, 4, 3, 1, 1, '2023-07-18 15:10:30', '2023-07-18 15:10:30', NULL, NULL, NULL, NULL, 24),
(20, '2023-07-21', 'Peternakan Sendiri', 1, 1, 2, 1, 2, 4, 3, 1, '2023-07-21 14:42:43', '2023-07-21 14:42:43', NULL, NULL, NULL, NULL, 17),
(21, '2023-07-29', 'Peternakan Sendiri', 1, 2, 3, 3, 1, 4, 2, 2, '2023-07-29 11:53:39', '2023-07-29 11:53:39', NULL, NULL, NULL, NULL, 17),
(22, '2023-07-29', 'Peternakan Sendiri', 5, 4, 1, 3, 1, 2, 2, 4, '2023-07-29 11:59:19', '2023-07-29 11:59:19', NULL, NULL, NULL, NULL, 24),
(23, '2023-08-04', 'Peternakan Sendiri', 5, 1, 4, 4, 3, 1, 1, 1, '2023-08-04 12:39:23', '2023-08-04 12:39:23', NULL, NULL, NULL, NULL, 17),
(24, '2023-08-04', 'Peternakan Sendiri', 2, 4, 1, 3, 4, 2, 1, 2, '2023-08-04 12:49:20', '2023-08-04 12:49:20', NULL, NULL, NULL, NULL, 24),
(25, '2023-08-12', 'Peternakan Sendiri', 5, 3, 1, 2, 3, 2, 4, 1, '2023-08-12 11:49:01', '2023-08-12 11:49:01', NULL, NULL, NULL, NULL, 17),
(26, '2023-08-12', 'Peternakan Sendiri', 5, 3, 2, 3, 4, 2, 3, 3, '2023-08-12 11:59:16', '2023-08-12 11:59:16', NULL, NULL, NULL, NULL, 24),
(27, '2023-08-19', 'Peternakan Sendiri', 5, 4, 1, 3, 3, 3, 2, 1, '2023-08-19 11:29:23', '2023-08-19 11:29:23', NULL, NULL, NULL, NULL, 17),
(28, '2023-08-19', 'Peternakan Sendiri', 2, 4, 1, 3, 2, 2, 3, 1, '2023-08-19 11:35:23', '2023-08-19 11:35:23', NULL, NULL, NULL, NULL, 10),
(29, '2023-08-26', 'Peternakan Sendiri', 2, 3, 4, 1, 2, 4, 5, 3, '2023-08-26 12:16:35', '2023-08-26 12:16:35', NULL, NULL, NULL, NULL, 17),
(30, '2023-08-26', 'Peternakan Sendiri', 5, 4, 1, 2, 3, 4, 2, 1, '2023-08-26 12:23:46', '2023-08-26 12:23:46', NULL, NULL, NULL, NULL, 9),
(31, '2023-09-02', 'Peternakan Sendiri', 1, 2, 2, 3, 3, 3, 2, 1, '2023-09-02 14:02:17', '2023-09-02 14:02:17', NULL, NULL, NULL, NULL, 17),
(32, '2023-09-02', 'Peternakan Sendiri', 1, 3, 3, 2, 2, 1, 5, 3, '2023-09-02 14:07:57', '2023-09-02 14:07:57', NULL, NULL, NULL, NULL, 24),
(33, '2023-09-09', 'Peternakan Sendiri', 2, 4, 3, 1, 1, 1, 2, 4, '2023-09-09 12:25:33', '2023-09-09 12:25:33', NULL, NULL, NULL, NULL, 17),
(34, '2023-09-09', 'Peternakan Sendiri', 1, 3, 2, 3, 4, 1, 5, 3, '2023-09-09 13:09:23', '2023-09-09 13:09:23', NULL, NULL, NULL, NULL, 24),
(35, '2023-09-16', 'Peternakan Sendiri', 2, 3, 5, 1, 2, 2, 4, 1, '2023-09-16 11:23:02', '2023-09-16 11:23:02', NULL, NULL, NULL, NULL, 17),
(36, '2023-09-16', 'Peternakan Sendiri', 3, 5, 3, 4, 1, 2, 4, 2, '2023-09-16 11:30:15', '2023-09-16 11:30:15', NULL, NULL, NULL, NULL, 10),
(37, '2023-09-16', 'Peternakan Lain', 6, 0, 0, 0, 0, 5, 0, 0, '2023-09-16 15:19:42', '2023-09-16 15:19:42', NULL, NULL, NULL, NULL, 7),
(38, '2023-09-23', 'Peternakan Sendiri', 4, 3, 1, 2, 5, 4, 3, 3, '2023-09-23 14:14:11', '2023-09-23 14:14:11', NULL, NULL, NULL, NULL, 17),
(39, '2023-09-23', 'Peternakan Sendiri', 4, 1, 2, 3, 3, 3, 5, 2, '2023-09-23 14:20:43', '2023-09-23 14:20:43', NULL, NULL, NULL, NULL, 24),
(40, '2023-09-30', 'Peternakan Sendiri', 4, 1, 2, 3, 4, 5, 3, 3, '2023-09-30 09:12:25', '2023-09-30 09:12:25', NULL, NULL, NULL, NULL, 17),
(41, '2023-09-30', 'Peternakan Sendiri', 4, 2, 5, 3, 3, 3, 2, 1, '2023-09-30 09:17:07', '2023-09-30 09:17:07', NULL, NULL, NULL, NULL, 9),
(42, '2023-10-08', 'Peternakan Sendiri', 2, 4, 3, 2, 1, 2, 3, 2, '2023-10-07 17:02:06', '2023-10-07 17:02:06', NULL, NULL, NULL, NULL, 17),
(43, '2023-10-08', 'Peternakan Sendiri', 3, 2, 4, 1, 3, 2, 4, 1, '2023-10-07 17:07:30', '2023-10-07 17:07:30', NULL, NULL, NULL, NULL, 10),
(44, '2023-10-14', 'Peternakan Sendiri', 4, 2, 2, 4, 5, 1, 2, 3, '2023-10-14 14:24:17', '2023-10-14 14:24:17', NULL, NULL, NULL, NULL, 17),
(45, '2023-10-14', 'Peternakan Sendiri', 4, 1, 3, 2, 3, 4, 5, 1, '2023-10-14 15:19:15', '2023-10-14 15:19:15', NULL, NULL, NULL, NULL, 24),
(46, '2023-10-21', 'Peternakan Sendiri', 4, 2, 5, 1, 3, 3, 4, 2, '2023-10-21 11:49:55', '2023-10-21 11:49:55', NULL, NULL, NULL, NULL, 17),
(47, '2023-10-21', 'Peternakan Sendiri', 4, 3, 3, 3, 2, 5, 1, 3, '2023-10-21 11:54:50', '2023-10-21 11:54:50', NULL, NULL, NULL, NULL, 24);
