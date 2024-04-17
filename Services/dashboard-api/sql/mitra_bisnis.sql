-- -------------------------------------------------------------
-- TablePlus 5.9.6(546)
--
-- https://tableplus.com/
--
-- Database: postgres
-- Generation Time: 2024-04-15 22:48:35.6230
-- -------------------------------------------------------------


-- This script only contains the table creation statements and does not fully represent the table in the database. Do not use it as a backup.

-- Sequence and defined type
CREATE SEQUENCE IF NOT EXISTS mitra_bisnis_id_seq;

-- Table Definition
CREATE TABLE "public"."mitra_bisnis" (
    "id" int8 NOT NULL DEFAULT nextval('mitra_bisnis_id_seq'::regclass),
    "nama_mitra" varchar(255) NOT NULL,
    "provinsi_id" varchar(64) NOT NULL,
    "kota_id" varchar(64) NOT NULL,
    "kecamatan_id" varchar(64) NOT NULL,
    "kelurahan_id" varchar(64),
    "created_at" timestamp(0),
    "updated_at" timestamp(0),
    "deleted_at" timestamp(0),
    "created_by" int8,
    "updated_by" int8,
    "deleted_by" int8,
    "id_unit_ternak" int8 NOT NULL,
    "id_kategori_mitra" int8 NOT NULL,
    CONSTRAINT "mitra_bisnis_id_unit_ternak_foreign" FOREIGN KEY ("id_unit_ternak") REFERENCES "public"."unit_ternak"("id"),
    CONSTRAINT "mitra_bisnis_id_kategori_mitra_foreign" FOREIGN KEY ("id_kategori_mitra") REFERENCES "public"."kategori_mitra"("id"),
    PRIMARY KEY ("id")
);

INSERT INTO "public"."mitra_bisnis" ("id", "nama_mitra", "provinsi_id", "kota_id", "kecamatan_id", "kelurahan_id", "created_at", "updated_at", "deleted_at", "created_by", "updated_by", "deleted_by", "id_unit_ternak", "id_kategori_mitra") VALUES
(3, 'Pengepul 1', '44156', '46199', '46315', '46319', '2022-11-18 07:32:07', '2022-11-18 07:32:07', NULL, NULL, NULL, NULL, 3, 1),
(4, 'Mitra Bisnis 2', '1', '281', '311', '313', '2022-12-29 16:14:23', '2022-12-29 16:14:23', NULL, NULL, NULL, NULL, 1, 4),
(5, 'Mitra Bisnis 3', '13411', '13610', '13623', '13625', '2022-12-29 16:14:46', '2022-12-29 16:14:46', NULL, NULL, NULL, NULL, 3, 3),
(6, 'Mitra 4', '14769', '15251', '15308', '15310', '2022-12-29 16:15:11', '2022-12-29 16:15:11', NULL, NULL, NULL, NULL, 3, 2),
(7, 'Mitra 3', '1', '683', '684', '685', '2023-01-31 17:51:01', '2023-01-31 17:51:01', NULL, NULL, NULL, NULL, 1, 1),
(8, 'bisnisin aja', '27530', '27696', '27759', '27760', '2023-02-01 04:46:02', '2023-02-01 04:46:02', NULL, NULL, NULL, NULL, 4, 1),
(9, 'Senduro Farm', '44156', '46199', '46315', '46319', '2023-02-01 05:10:57', '2023-02-01 05:10:57', NULL, NULL, NULL, NULL, 5, 10),
(10, 'PB Farm', '44156', '47346', '47347', '47354', '2023-02-01 05:14:52', '2023-02-01 05:14:52', NULL, NULL, NULL, NULL, 5, 1),
(11, 'Koperasi Rakyat Jogoyudan', '44156', '46199', '46294', '46298', '2023-02-01 05:16:50', '2023-02-01 05:16:50', NULL, NULL, NULL, NULL, 5, 6),
(12, 'mitra sejati', '44156', '47346', '47447', '47448', '2023-02-03 14:39:12', '2023-02-03 14:39:12', NULL, NULL, NULL, NULL, 4, 4),
(13, 'Mitra O', '44156', '52318', '52460', '52461', '2023-02-19 15:12:11', '2023-02-19 15:12:11', NULL, NULL, NULL, NULL, 15, 6),
(14, 'Mitra P', '44156', '47346', '47636', '47637', '2023-02-19 15:12:56', '2023-02-19 15:12:56', NULL, NULL, NULL, NULL, 15, 1),
(15, 'Mitra E', '44156', '44842', '44858', '44861', '2023-02-19 15:25:23', '2023-02-19 15:25:23', NULL, NULL, NULL, NULL, 9, 10),
(16, 'Mitra f', '44156', '44842', '44858', '44863', '2023-02-19 15:25:50', '2023-02-19 15:25:50', NULL, NULL, NULL, NULL, 9, 6),
(17, 'Mitra M', '44156', '47346', '47447', '47448', '2023-02-19 15:32:52', '2023-02-19 15:32:52', NULL, NULL, NULL, NULL, 14, 2),
(18, 'Mitra M', '44156', '47346', '47447', '47448', '2023-02-19 15:33:00', '2023-02-19 15:33:00', NULL, NULL, NULL, NULL, 14, 2),
(19, 'Mitra N', '44156', '44842', '44876', '44878', '2023-02-19 15:34:18', '2023-02-19 15:34:18', NULL, NULL, NULL, NULL, 14, 10),
(20, 'Mitra G', '44156', '46949', '47039', '47040', '2023-02-19 15:57:33', '2023-02-19 15:57:33', NULL, NULL, NULL, NULL, 12, 1),
(21, 'Mitra H', '44156', '44842', '44858', '44859', '2023-02-19 15:58:28', '2023-02-19 15:58:28', NULL, NULL, NULL, NULL, 12, 4),
(22, 'Mitra A', '44156', '45133', '45192', '45198', '2023-02-20 00:22:45', '2023-02-20 00:22:45', NULL, NULL, NULL, NULL, 7, 1),
(23, 'CV Food Andi', '44156', '46199', '46315', '46319', '2023-03-01 18:10:06', '2023-03-01 18:10:06', NULL, NULL, NULL, NULL, 5, 3),
(24, 'CV Food Andi', '44156', '46199', '46315', '46319', '2023-03-01 18:10:19', '2023-03-01 18:10:19', NULL, NULL, NULL, NULL, 5, 3),
(25, 'Konsumen', '44156', '46199', '46294', '46305', '2023-03-01 18:26:36', '2023-03-01 18:26:36', NULL, NULL, NULL, NULL, 5, 7),
(31, 'Agus', '44156', '47346', '47432', '47437', '2023-07-04 02:15:27', '2023-07-04 02:15:27', NULL, NULL, NULL, NULL, 18, 7),
(32, 'Agus', '44156', '47346', '47432', '47437', '2023-07-04 02:16:05', '2023-07-04 02:16:05', NULL, NULL, NULL, NULL, 18, 7),
(33, 'vilda', '44156', '53148', '53160', '53166', '2023-07-04 02:17:47', '2023-07-04 02:17:47', NULL, NULL, NULL, NULL, 18, 7),
(35, 'Pesona etawa', '44156', '45133', '45176', '45185', '2023-07-05 01:17:32', '2023-07-05 01:17:32', NULL, NULL, NULL, NULL, 18, 1),
(36, 'Pesona etawa', '44156', '45133', '45176', '45185', '2023-07-05 01:18:10', '2023-07-05 01:18:10', NULL, NULL, NULL, NULL, 18, 1),
(37, 'anton novel', '44156', '46199', '46315', '46321', '2023-07-07 02:50:35', '2023-07-07 02:50:35', NULL, NULL, NULL, NULL, 35, 1);
