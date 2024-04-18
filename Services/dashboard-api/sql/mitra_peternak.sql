-- -------------------------------------------------------------
-- TablePlus 5.9.6(546)
--
-- https://tableplus.com/
--
-- Database: postgres
-- Generation Time: 2024-04-18 07:44:23.9120
-- -------------------------------------------------------------


-- This script only contains the table creation statements and does not fully represent the table in the database. Do not use it as a backup.

-- Sequence and defined type
CREATE SEQUENCE IF NOT EXISTS mitra_peternak_id_seq;

-- Table Definition
CREATE TABLE "public"."mitra_peternak" (
    "id" int8 NOT NULL DEFAULT nextval('mitra_peternak_id_seq'::regclass),
    "nama_mitra" varchar(255) NOT NULL,
    "nama_pemilik" varchar(255) NOT NULL,
    "jenkel" varchar(255) NOT NULL CHECK ((jenkel)::text = ANY (ARRAY[('Pria'::character varying)::text, ('Wanita'::character varying)::text])),
    "pendidikan" varchar(255) CHECK ((pendidikan)::text = ANY (ARRAY[('Sekolah Dasar'::character varying)::text, ('Sekolah Menengah Pertama'::character varying)::text, ('Sekolah Menengah Atas'::character varying)::text, ('Strata 1 / Sarjana'::character varying)::text, ('Strata 2 / Magister'::character varying)::text, ('Strata 3'::character varying)::text])),
    "tgl_lahir" date,
    "latitude" numeric(10,8),
    "longitude" numeric(11,8),
    "provinsi_id" varchar(64) NOT NULL,
    "kota_id" varchar(64) NOT NULL,
    "kecamatan_id" varchar(64) NOT NULL,
    "kelurahan_id" varchar(64),
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
    "id_unit_ternak" int8 NOT NULL,
    CONSTRAINT "mitra_peternak_id_unit_ternak_foreign" FOREIGN KEY ("id_unit_ternak") REFERENCES "public"."unit_ternak"("id"),
    PRIMARY KEY ("id")
);

INSERT INTO "public"."mitra_peternak" ("id", "nama_mitra", "nama_pemilik", "jenkel", "pendidikan", "tgl_lahir", "latitude", "longitude", "provinsi_id", "kota_id", "kecamatan_id", "kelurahan_id", "jml_pedaging_jantan", "jml_pedaging_betina", "jml_pedaging_anakan_jantan", "jml_pedaging_anakan_betina", "jml_perah_jantan", "jml_perah_betina", "jml_perah_anakan_jantan", "jml_perah_anakan_betina", "created_at", "updated_at", "deleted_at", "created_by", "updated_by", "deleted_by", "id_unit_ternak") VALUES
(2, 'Goatzilla Farm', 'Luthfi Andi Z', 'Pria', 'Sekolah Menengah Atas', '1980-11-18', NULL, NULL, '44156', '46199', '46315', '46321', 5, 50, 5, 5, 1, 5, 5, 5, '2022-11-18 07:25:08', '2022-11-18 07:25:08', NULL, NULL, NULL, NULL, 3),
(3, 'Joko Farm', 'Joko Tingkir', 'Pria', 'Strata 1 / Sarjana', '1985-11-18', NULL, NULL, '44156', '46199', '46315', '46319', 5, 10, 1, 5, 5, 10, 1, 5, '2022-11-18 07:30:59', '2022-11-18 07:30:59', NULL, NULL, NULL, NULL, 3),
(4, 'Nama Mitra freetext', 'Freetext', 'Pria', 'Strata 2 / Magister', '2023-01-28', NULL, NULL, '1', '2', '11', '13', 1, 1, 1, 2, 3, 4, 5, 6, '2023-01-28 01:04:47', '2023-01-28 01:04:47', NULL, NULL, NULL, NULL, 1),
(5, 'Mizan Farm', 'Khaizuran Rafif Hamizan', 'Pria', 'Sekolah Menengah Atas', '2023-01-28', NULL, NULL, '6812', '7049', '7082', '7085', 4, 4, 4, 4, 4, 4, 4, 4, '2023-01-28 01:06:05', '2023-01-28 01:06:05', NULL, NULL, NULL, NULL, 1),
(6, 'Peternakan Bebek athar', 'Atharizky', 'Pria', 'Strata 2 / Magister', '2023-01-28', NULL, NULL, '6812', '7049', '7050', '7051', 3, 3, 3, 3, 3, 3, 3, 3, '2023-01-28 03:58:43', '2023-01-28 03:58:43', NULL, NULL, NULL, NULL, 3),
(7, 'Jorginho Farm', 'Jorginho', 'Pria', 'Sekolah Dasar', '2023-01-31', NULL, NULL, '1', '2', '3', '4', 2, 2, 2, 2, 3, 3, 3, 3, '2023-01-31 16:38:49', '2023-01-31 16:38:49', NULL, NULL, NULL, NULL, 1),
(8, 'Peternakan Ap01', 'Arin', 'Pria', 'Sekolah Menengah Pertama', '2023-02-01', NULL, NULL, '44156', '46199', '46315', '46316', 2, 5, 2, 1, 0, 5, 0, 1, '2023-02-01 06:00:43', '2023-02-01 06:00:43', NULL, NULL, NULL, NULL, 5),
(9, 'agusfarm', 'Agus Waluyo', 'Pria', 'Strata 3', '2022-01-04', NULL, NULL, '44156', '44341', '44342', '44343', 9, 5, 7, 5, 4, 3, 2, 1, '2023-02-01 08:16:21', '2023-02-01 08:16:21', NULL, NULL, NULL, NULL, 4),
(10, 'susanfarm', 'susan', 'Wanita', 'Sekolah Menengah Pertama', '2023-02-03', NULL, NULL, '44156', '46199', '46200', '46202', 10, 15, 10, 11, 7, 8, 5, 5, '2023-02-03 14:43:48', '2023-02-03 14:43:48', NULL, NULL, NULL, NULL, 4),
(11, 'ABC Farm', 'Anto Beri Cahyo', 'Pria', 'Sekolah Menengah Atas', '1980-02-07', NULL, NULL, '44156', '47346', '47347', '47348', 20, 15, 6, 5, 3, 2, 1, 3, '2023-02-07 06:35:09', '2023-02-07 06:35:09', NULL, NULL, NULL, NULL, 6),
(12, 'Rohman Farm', 'Rohman', 'Pria', 'Sekolah Menengah Atas', '2023-02-19', NULL, NULL, '44156', '47346', '47415', '47428', 5, 5, 3, 10, 3, 7, 3, 2, '2023-02-19 15:04:22', '2023-02-19 15:04:22', NULL, NULL, NULL, NULL, 15),
(13, 'Sholikin Farm', 'Sholikin', 'Pria', 'Sekolah Menengah Pertama', '2023-02-19', NULL, NULL, '44156', '46199', '46315', '46319', 5, 5, 3, 10, 3, 7, 3, 2, '2023-02-19 15:22:20', '2023-02-19 15:22:20', NULL, NULL, NULL, NULL, 9),
(14, 'Nurcholis Farm', 'Nurcholis', 'Pria', 'Sekolah Menengah Atas', '2023-02-19', NULL, NULL, '44156', '46199', '46315', '46319', 3, 6, 4, 8, 2, 6, 3, 3, '2023-02-19 15:24:06', '2023-02-19 15:24:06', NULL, NULL, NULL, NULL, 9),
(15, 'Rafi Farm', 'Rafi Al-Mutawakil', 'Pria', 'Sekolah Menengah Atas', '2023-02-19', NULL, NULL, '44156', '47346', '47447', '47448', 4, 10, 3, 5, 3, 6, 2, 1, '2023-02-19 15:24:16', '2023-02-19 15:24:16', NULL, NULL, NULL, NULL, 14),
(16, 'Dicky Farm', 'Dicky Dwi Yanto', 'Pria', 'Sekolah Menengah Atas', '2023-02-19', NULL, NULL, '44156', '47346', '47447', '47448', 4, 9, 3, 8, 2, 12, 2, 6, '2023-02-19 15:27:52', '2023-02-19 15:27:52', NULL, NULL, NULL, NULL, 14),
(17, 'Imron Farm', 'Mohammad Imron', 'Pria', 'Sekolah Menengah Atas', '2023-02-19', NULL, NULL, '44156', '47346', '47588', '47595', 3, 7, 3, 2, 3, 2, 1, 2, '2023-02-19 15:39:32', '2023-02-19 15:39:32', NULL, NULL, NULL, NULL, 12),
(18, 'Wasuli farm', 'Achmad wasuli', 'Pria', 'Sekolah Menengah Atas', '2023-02-19', NULL, NULL, '44156', '46199', '46315', '46316', 4, 10, 3, 5, 3, 6, 2, 1, '2023-02-19 15:48:22', '2023-02-19 15:48:22', NULL, NULL, NULL, NULL, 8),
(19, 'Siam farm', 'Saiful siam', 'Pria', 'Sekolah Menengah Pertama', '2023-02-19', NULL, NULL, '44156', '46199', '46315', '46316', 1, 9, 3, 8, 2, 12, 2, 6, '2023-02-19 16:17:27', '2023-02-19 16:17:27', NULL, NULL, NULL, NULL, 8),
(20, 'Khairul Farm', 'KHAIRUL ANWAR', 'Pria', 'Sekolah Menengah Pertama', '2023-02-20', NULL, NULL, '44156', '46199', '46315', '46321', 3, 7, 3, 2, 3, 2, 1, 2, '2023-02-20 00:00:29', '2023-02-20 00:00:29', NULL, NULL, NULL, NULL, 7),
(21, 'Aam Ganteng', 'Farham', 'Pria', 'Sekolah Menengah Atas', '2023-05-29', NULL, NULL, '27530', '27696', '27720', '27724', 10, 10, 20, 30, 40, 50, 60, 70, '2023-05-28 23:37:42', '2023-05-28 23:37:42', NULL, NULL, NULL, NULL, 1),
(24, 'Reffan farm', 'Reffan Maulada', 'Pria', 'Sekolah Menengah Atas', '2023-06-09', NULL, NULL, '27530', '27772', '27788', '27789', 5, 1, 8, 2, 1, 2, 2, 1, '2023-06-09 08:18:52', '2023-06-09 08:18:52', NULL, NULL, NULL, NULL, 4),
(25, 'Hasan tambelan', 'nur hasan', 'Pria', 'Sekolah Menengah Atas', '2023-06-12', NULL, NULL, '44156', '47346', '47432', '47436', 4, 10, 5, 10, 0, 5, 0, 8, '2023-06-12 05:12:29', '2023-06-12 05:12:29', NULL, NULL, NULL, NULL, 18),
(26, 'yes farm', 'septyan hidayat', 'Pria', 'Sekolah Dasar', '2023-06-12', NULL, NULL, '44156', '47346', '47538', '47547', 6, 5, 5, 0, 0, 0, 3, 5, '2023-06-12 05:12:44', '2023-06-12 05:12:44', NULL, NULL, NULL, NULL, 20),
(33, 'tumpibalapfarm', 'Muchamad Rudi Hamsyah', 'Pria', 'Sekolah Menengah Atas', '2023-06-14', NULL, NULL, '44156', '46199', '46315', '46321', 1, 0, 4, 5, 0, 20, 5, 0, '2023-06-14 04:48:04', '2023-06-14 04:48:04', NULL, NULL, NULL, NULL, 36),
(35, 'singo joyo', 'anton novel', 'Pria', 'Sekolah Menengah Atas', '2023-06-14', NULL, NULL, '44156', '46199', '46315', '46321', 0, 0, 0, 0, 0, 15, 0, 0, '2023-06-14 16:14:56', '2023-06-14 16:14:56', NULL, NULL, NULL, NULL, 35),
(36, 'gatot koco', 'ripin', 'Pria', 'Sekolah Menengah Atas', '2023-06-15', NULL, NULL, '44156', '46199', '46315', '46321', 0, 0, 0, 0, 0, 30, 0, 0, '2023-06-14 17:25:33', '2023-06-14 17:25:33', NULL, NULL, NULL, NULL, 35),
(42, 'sumardifarm', 'sumardi', 'Pria', 'Sekolah Menengah Atas', '2023-07-03', NULL, NULL, '44156', '46199', '46315', '46320', 1, 0, 0, 0, 0, 30, 0, 2, '2023-07-03 01:08:08', '2023-07-03 01:08:08', NULL, NULL, NULL, NULL, 32),
(51, 'roy farm', 'bu sudar', 'Wanita', 'Sekolah Dasar', '2023-08-04', NULL, NULL, '44156', '46199', '46315', '46320', 1, 10, 2, 4, 0, 15, 0, 2, '2023-08-04 03:26:44', '2023-08-04 03:26:44', NULL, NULL, NULL, NULL, 32);
