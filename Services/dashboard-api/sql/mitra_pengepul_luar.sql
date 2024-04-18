-- -------------------------------------------------------------
-- TablePlus 5.9.6(546)
--
-- https://tableplus.com/
--
-- Database: postgres
-- Generation Time: 2024-04-18 07:44:06.9780
-- -------------------------------------------------------------


-- This script only contains the table creation statements and does not fully represent the table in the database. Do not use it as a backup.

-- Sequence and defined type
CREATE SEQUENCE IF NOT EXISTS mitra_pengepul_luar_id_seq;

-- Table Definition
CREATE TABLE "public"."mitra_pengepul_luar" (
    "id" int8 NOT NULL DEFAULT nextval('mitra_pengepul_luar_id_seq'::regclass),
    "nama_pengepul" varchar(255) NOT NULL,
    "jenkel" varchar(255) NOT NULL CHECK ((jenkel)::text = ANY (ARRAY[('Pria'::character varying)::text, ('Wanita'::character varying)::text])),
    "pendidikan" varchar(255) CHECK ((pendidikan)::text = ANY (ARRAY[('Sekolah Dasar'::character varying)::text, ('Sekolah Menengah Pertama'::character varying)::text, ('Sekolah Menengah Atas'::character varying)::text, ('Strata 1 / Sarjana'::character varying)::text, ('Strata 2 / Magister'::character varying)::text, ('Strata 3'::character varying)::text])),
    "tgl_lahir" date,
    "jenis_pengepul" varchar(255) NOT NULL CHECK ((jenis_pengepul)::text = ANY (ARRAY[('Ternak Potong'::character varying)::text, ('Susu'::character varying)::text])),
    "provinsi_id" varchar(64) NOT NULL,
    "kota_id" varchar(64) NOT NULL,
    "kecamatan_id" varchar(64) NOT NULL,
    "created_at" timestamp(0),
    "updated_at" timestamp(0),
    "deleted_at" timestamp(0),
    "created_by" int8,
    "updated_by" int8,
    "deleted_by" int8,
    "id_unit_ternak" int8 NOT NULL,
    CONSTRAINT "mitra_pengepul_luar_id_unit_ternak_foreign" FOREIGN KEY ("id_unit_ternak") REFERENCES "public"."unit_ternak"("id"),
    PRIMARY KEY ("id")
);

INSERT INTO "public"."mitra_pengepul_luar" ("id", "nama_pengepul", "jenkel", "pendidikan", "tgl_lahir", "jenis_pengepul", "provinsi_id", "kota_id", "kecamatan_id", "created_at", "updated_at", "deleted_at", "created_by", "updated_by", "deleted_by", "id_unit_ternak") VALUES
(1, 'Pengepul M', 'Pria', 'Sekolah Menengah Atas', '2023-02-19', 'Ternak Potong', '44156', '47346', '47447', '2023-02-19 15:45:06', '2023-02-19 15:45:06', NULL, NULL, NULL, NULL, 14),
(2, 'Pengepul N', 'Wanita', 'Sekolah Menengah Atas', '2023-02-19', 'Ternak Potong', '44156', '47346', '47447', '2023-02-19 15:46:40', '2023-02-19 15:46:40', NULL, NULL, NULL, NULL, 14),
(3, 'Pengepul G', 'Pria', 'Sekolah Menengah Atas', '2023-02-19', 'Ternak Potong', '44156', '47346', '47588', '2023-02-19 16:00:07', '2023-02-19 16:00:07', NULL, NULL, NULL, NULL, 12),
(4, 'Pengepul A', 'Pria', 'Sekolah Menengah Pertama', '2023-02-20', 'Susu', '44156', '46199', '46315', '2023-02-20 00:14:59', '2023-02-20 00:14:59', NULL, NULL, NULL, NULL, 7),
(5, 'Budi Farm', 'Pria', 'Sekolah Menengah Atas', '2023-02-20', 'Susu', '44156', '46199', '46200', '2023-02-20 01:18:08', '2023-02-20 01:18:08', NULL, NULL, NULL, NULL, 4),
(6, 'Pengepul E', 'Pria', 'Sekolah Menengah Pertama', '2023-02-20', 'Susu', '44156', '46199', '46315', '2023-02-20 05:53:22', '2023-02-20 05:53:22', NULL, NULL, NULL, NULL, 9),
(7, 'Pengepul f', 'Wanita', 'Sekolah Menengah Atas', '2023-02-20', 'Susu', '44156', '46199', '46315', '2023-02-20 05:53:53', '2023-02-20 05:53:53', NULL, NULL, NULL, NULL, 9),
(8, 'Pengepul O', 'Pria', 'Sekolah Menengah Atas', '2023-02-20', 'Ternak Potong', '44156', '47346', '47415', '2023-02-20 09:24:53', '2023-02-20 09:24:53', NULL, NULL, NULL, NULL, 15),
(9, 'Andi', 'Pria', 'Sekolah Menengah Atas', '2023-03-02', 'Susu', '44156', '46199', '46294', '2023-03-01 18:06:46', '2023-03-01 18:06:46', NULL, NULL, NULL, NULL, 5),
(10, 'Budiman', 'Pria', 'Sekolah Menengah Atas', '2023-03-02', 'Susu', '44156', '46199', '46294', '2023-03-01 18:08:29', '2023-03-01 18:08:29', NULL, NULL, NULL, NULL, 5),
(11, 'Pak Apud', 'Pria', 'Sekolah Menengah Atas', '2000-10-10', 'Ternak Potong', '44156', '53021', '53049', '2023-05-30 17:39:18', '2023-05-30 17:39:18', NULL, NULL, NULL, NULL, 1),
(12, 'Wiro Asep', 'Pria', 'Sekolah Menengah Atas', '2023-06-10', 'Susu', '44156', '46199', '46294', '2023-06-10 09:21:45', '2023-06-10 09:21:45', NULL, NULL, NULL, NULL, 5);
