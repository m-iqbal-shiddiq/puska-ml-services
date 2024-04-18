-- -------------------------------------------------------------
-- TablePlus 5.9.6(546)
--
-- https://tableplus.com/
--
-- Database: postgres
-- Generation Time: 2024-04-18 07:44:46.5500
-- -------------------------------------------------------------


-- This script only contains the table creation statements and does not fully represent the table in the database. Do not use it as a backup.

-- Sequence and defined type
CREATE SEQUENCE IF NOT EXISTS pencatatan_ternak_keluar_id_seq;

-- Table Definition
CREATE TABLE "public"."pencatatan_ternak_keluar" (
    "id" int8 NOT NULL DEFAULT nextval('pencatatan_ternak_keluar_id_seq'::regclass),
    "tgl_pencatatan" date NOT NULL,
    "jenis_mitra_penerima" varchar(255) NOT NULL,
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
    CONSTRAINT "pencatatan_ternak_keluar_id_peternak_foreign" FOREIGN KEY ("id_peternak") REFERENCES "public"."mitra_peternak"("id"),
    PRIMARY KEY ("id")
);

INSERT INTO "public"."pencatatan_ternak_keluar" ("id", "tgl_pencatatan", "jenis_mitra_penerima", "jml_pedaging_jantan", "jml_pedaging_betina", "jml_pedaging_anakan_jantan", "jml_pedaging_anakan_betina", "jml_perah_jantan", "jml_perah_betina", "jml_perah_anakan_jantan", "jml_perah_anakan_betina", "created_at", "updated_at", "deleted_at", "created_by", "updated_by", "deleted_by", "id_peternak") VALUES
(1, '2023-02-19', 'Pengepul', 2, 3, 5, 2, 4, 2, 3, 1, '2023-02-19 16:07:15', '2023-02-19 16:07:15', NULL, NULL, NULL, NULL, 18),
(2, '2023-02-19', 'Peternakan Sendiri', 0, 0, 0, 0, 0, 0, 0, 0, '2023-02-19 16:15:37', '2023-02-19 16:15:37', NULL, NULL, NULL, NULL, 17),
(3, '2023-02-20', 'Pengepul', 2, 2, 1, 0, 0, 0, 0, 1, '2023-02-20 00:58:22', '2023-02-20 00:58:22', NULL, NULL, NULL, NULL, 12),
(4, '2023-02-20', 'Peternakan Sendiri', 0, 0, 0, 0, 0, 0, 1, 0, '2023-02-20 00:58:42', '2023-02-20 00:58:42', NULL, NULL, NULL, NULL, 12),
(5, '2023-02-20', 'Peternakan Lain', 0, 2, 0, 0, 0, 0, 0, 0, '2023-02-20 01:59:15', '2023-02-20 01:59:15', NULL, NULL, NULL, NULL, 10),
(6, '2023-02-20', 'Peternakan Lain', 0, 0, 0, 0, 0, 0, 1, 1, '2023-02-20 06:09:13', '2023-02-20 06:09:13', NULL, NULL, NULL, NULL, 13),
(7, '2023-02-20', 'Pengepul', 0, 0, 0, 0, 0, 0, 1, 1, '2023-02-20 06:09:26', '2023-02-20 06:09:26', NULL, NULL, NULL, NULL, 13),
(8, '2023-02-20', 'Peternakan Sendiri', 1, 1, 1, 1, 2, 2, 1, 1, '2023-02-20 09:22:56', '2023-02-20 09:22:56', NULL, NULL, NULL, NULL, 15),
(9, '2023-02-20', 'Peternakan Lain', 1, 1, 1, 1, 2, 2, 1, 1, '2023-02-20 09:23:26', '2023-02-20 09:23:26', NULL, NULL, NULL, NULL, 15),
(10, '2023-02-20', 'Peternakan Lain', 1, 1, 1, 1, 2, 2, 1, 1, '2023-02-20 09:29:13', '2023-02-20 09:29:13', NULL, NULL, NULL, NULL, 16),
(11, '2023-02-21', 'Peternakan Sendiri', 5, 5, 2, 1, 1, 2, 6, 2, '2023-02-21 15:58:34', '2023-02-21 15:58:34', NULL, NULL, NULL, NULL, 17),
(12, '2023-03-15', 'Peternakan Sendiri', 0, 1, 0, 0, 1, 0, 0, 1, '2023-03-14 17:28:29', '2023-03-14 17:28:29', NULL, NULL, NULL, NULL, 9),
(13, '2023-04-16', 'Peternakan Sendiri', 0, 1, 0, 0, 1, 0, 0, 1, '2023-03-14 17:28:29', '2023-03-14 17:28:29', NULL, NULL, NULL, NULL, 7),
(14, '2023-04-18', 'Peternakan Sendiri', 2, 1, 2, 2, 1, 0, 0, 1, '2023-03-14 17:28:29', '2023-03-14 17:28:29', NULL, NULL, NULL, NULL, 7),
(16, '2023-07-04', 'Peternakan Sendiri', 1, 2, 3, 5, 1, 1, 2, 3, '2023-07-04 10:28:42', '2023-07-04 10:28:42', NULL, NULL, NULL, NULL, 17),
(17, '2023-07-04', 'Peternakan Sendiri', 1, 1, 3, 4, 1, 2, 3, 4, '2023-07-04 15:37:34', '2023-07-04 15:37:34', NULL, NULL, NULL, NULL, 24),
(18, '2023-07-18', 'Peternakan Sendiri', 1, 1, 4, 3, 3, 3, 1, 1, '2023-07-18 15:06:58', '2023-07-18 15:06:58', NULL, NULL, NULL, NULL, 17),
(19, '2023-07-18', 'Peternakan Sendiri', 1, 1, 4, 2, 2, 2, 1, 2, '2023-07-18 15:10:50', '2023-07-18 15:10:50', NULL, NULL, NULL, NULL, 24),
(20, '2023-07-21', 'Peternakan Sendiri', 1, 2, 3, 4, 1, 1, 2, 2, '2023-07-21 14:43:04', '2023-07-21 14:43:04', NULL, NULL, NULL, NULL, 17),
(21, '2023-07-29', 'Peternakan Sendiri', 1, 1, 3, 2, 2, 3, 4, 5, '2023-07-29 11:53:56', '2023-07-29 11:53:56', NULL, NULL, NULL, NULL, 17),
(22, '2023-07-29', 'Peternakan Sendiri', 5, 4, 1, 2, 3, 2, 1, 1, '2023-07-29 11:59:36', '2023-07-29 11:59:36', NULL, NULL, NULL, NULL, 24),
(23, '2023-08-04', 'Peternakan Sendiri', 1, 1, 1, 4, 3, 2, 2, 5, '2023-08-04 12:39:40', '2023-08-04 12:39:40', NULL, NULL, NULL, NULL, 17),
(24, '2023-08-04', 'Peternakan Sendiri', 2, 3, 4, 2, 2, 1, 1, 1, '2023-08-04 12:49:53', '2023-08-04 12:49:53', NULL, NULL, NULL, NULL, 24),
(25, '2023-08-12', 'Peternakan Sendiri', 5, 4, 3, 4, 2, 1, 2, 3, '2023-08-12 11:49:23', '2023-08-12 11:49:23', NULL, NULL, NULL, NULL, 17),
(26, '2023-08-12', 'Peternakan Sendiri', 2, 4, 3, 1, 1, 2, 3, 2, '2023-08-12 11:59:36', '2023-08-12 11:59:36', NULL, NULL, NULL, NULL, 24),
(27, '2023-08-19', 'Peternakan Sendiri', 1, 2, 2, 3, 3, 3, 4, 1, '2023-08-19 11:29:45', '2023-08-19 11:29:45', NULL, NULL, NULL, NULL, 17),
(28, '2023-08-19', 'Peternakan Sendiri', 4, 3, 1, 2, 1, 1, 3, 2, '2023-08-19 11:35:50', '2023-08-19 11:35:50', NULL, NULL, NULL, NULL, 10),
(29, '2023-08-26', 'Peternakan Sendiri', 2, 3, 4, 2, 1, 3, 3, 4, '2023-08-26 12:16:48', '2023-08-26 12:16:48', NULL, NULL, NULL, NULL, 17),
(30, '2023-08-26', 'Peternakan Sendiri', 5, 4, 1, 1, 2, 2, 4, 3, '2023-08-26 12:24:03', '2023-08-26 12:24:03', NULL, NULL, NULL, NULL, 9),
(31, '2023-09-02', 'Peternakan Sendiri', 1, 4, 4, 3, 2, 2, 1, 1, '2023-09-02 14:02:33', '2023-09-02 14:02:33', NULL, NULL, NULL, NULL, 17),
(32, '2023-09-02', 'Peternakan Sendiri', 2, 3, 2, 2, 4, 1, 3, 3, '2023-09-02 14:08:16', '2023-09-02 14:08:16', NULL, NULL, NULL, NULL, 24),
(33, '2023-09-09', 'Peternakan Sendiri', 3, 2, 4, 5, 5, 1, 2, 3, '2023-09-09 12:25:47', '2023-09-09 12:25:47', NULL, NULL, NULL, NULL, 17),
(34, '2023-09-09', 'Peternakan Sendiri', 3, 1, 1, 1, 5, 2, 4, 3, '2023-09-09 13:09:37', '2023-09-09 13:09:37', NULL, NULL, NULL, NULL, 24),
(35, '2023-09-16', 'Peternakan Sendiri', 3, 3, 2, 1, 4, 3, 5, 1, '2023-09-16 11:23:24', '2023-09-16 11:23:24', NULL, NULL, NULL, NULL, 17),
(36, '2023-09-16', 'Peternakan Sendiri', 3, 1, 2, 4, 5, 1, 2, 2, '2023-09-16 11:30:33', '2023-09-16 11:30:33', NULL, NULL, NULL, NULL, 10),
(37, '2023-09-23', 'Peternakan Sendiri', 3, 4, 4, 5, 3, 2, 1, 2, '2023-09-23 14:14:32', '2023-09-23 14:14:32', NULL, NULL, NULL, NULL, 17),
(38, '2023-09-23', 'Peternakan Sendiri', 4, 2, 3, 3, 2, 1, 5, 2, '2023-09-23 14:20:58', '2023-09-23 14:20:58', NULL, NULL, NULL, NULL, 24),
(39, '2023-09-30', 'Peternakan Sendiri', 4, 1, 2, 2, 3, 1, 2, 5, '2023-09-30 09:12:40', '2023-09-30 09:12:40', NULL, NULL, NULL, NULL, 17),
(40, '2023-09-30', 'Peternakan Sendiri', 4, 1, 3, 2, 5, 2, 4, 3, '2023-09-30 09:17:22', '2023-09-30 09:17:22', NULL, NULL, NULL, NULL, 9),
(41, '2023-10-08', 'Peternakan Sendiri', 2, 4, 1, 3, 2, 2, 4, 3, '2023-10-07 17:02:24', '2023-10-07 17:02:24', NULL, NULL, NULL, NULL, 17),
(42, '2023-10-08', 'Peternakan Sendiri', 3, 2, 4, 1, 5, 2, 3, 1, '2023-10-07 17:07:53', '2023-10-07 17:07:53', NULL, NULL, NULL, NULL, 10),
(43, '2023-10-14', 'Peternakan Sendiri', 4, 2, 1, 2, 2, 3, 3, 4, '2023-10-14 14:24:31', '2023-10-14 14:24:31', NULL, NULL, NULL, NULL, 17),
(44, '2023-10-14', 'Peternakan Sendiri', 3, 4, 2, 3, 3, 3, 4, 1, '2023-10-14 15:19:30', '2023-10-14 15:19:30', NULL, NULL, NULL, NULL, 24),
(45, '2023-10-21', 'Peternakan Sendiri', 4, 2, 5, 1, 3, 4, 2, 1, '2023-10-21 11:50:13', '2023-10-21 11:50:13', NULL, NULL, NULL, NULL, 17),
(46, '2023-10-21', 'Peternakan Sendiri', 5, 3, 3, 3, 5, 2, 1, 2, '2023-10-21 11:55:05', '2023-10-21 11:55:05', NULL, NULL, NULL, NULL, 24);
