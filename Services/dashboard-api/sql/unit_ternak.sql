-- -------------------------------------------------------------
-- TablePlus 5.9.6(546)
--
-- https://tableplus.com/
--
-- Database: postgres
-- Generation Time: 2024-04-15 22:49:10.8260
-- -------------------------------------------------------------


-- This script only contains the table creation statements and does not fully represent the table in the database. Do not use it as a backup.

-- Sequence and defined type
CREATE SEQUENCE IF NOT EXISTS unit_ternak_id_seq;

-- Table Definition
CREATE TABLE "public"."unit_ternak" (
    "id" int8 NOT NULL DEFAULT nextval('unit_ternak_id_seq'::regclass),
    "nama_unit" varchar(255) NOT NULL,
    "alamat" text NOT NULL,
    "provinsi_id" varchar(64) NOT NULL,
    "kota_id" varchar(64) NOT NULL,
    "kecamatan_id" varchar(64) NOT NULL,
    "kelurahan_id" varchar(64),
    "latitude" numeric(10,8),
    "longitude" numeric(11,8),
    "created_at" timestamp(0),
    "updated_at" timestamp(0),
    "deleted_at" timestamp(0),
    "created_by" int8,
    "updated_by" int8,
    "deleted_by" int8,
    PRIMARY KEY ("id")
);

INSERT INTO "public"."unit_ternak" ("id", "nama_unit", "alamat", "provinsi_id", "kota_id", "kecamatan_id", "kelurahan_id", "latitude", "longitude", "created_at", "updated_at", "deleted_at", "created_by", "updated_by", "deleted_by") VALUES
(1, 'Paguyuban Ternak', 'Jl TB Simatupang no.15 A', '27530', '27696', '27720', '27721', NULL, NULL, '2022-11-02 06:11:25', NULL, NULL, 1, NULL, NULL),
(2, 'Intan Farm', 'Senduro', '44156', '46199', '46315', '46319', NULL, NULL, '2023-05-28 10:28:37', '2023-05-28 10:28:37', NULL, NULL, NULL, NULL),
(3, 'Goatzilla Farm Demo', 'Graud zamzam rowobuyiel labuk lor lungiang', '44156', '46199', '46315', '46321', NULL, NULL, '2022-11-18 07:19:27', '2022-11-18 07:19:27', NULL, NULL, NULL, NULL),
(4, 'Paguyuban Intan', 'Jawa Timur', '44156', '47701', '47810', '47811', NULL, NULL, '2023-02-01 04:29:10', '2023-02-01 04:29:10', NULL, NULL, NULL, NULL),
(5, 'Paguyuban Alusyanti', 'Jawa Timur', '44156', '44842', '44843', '44851', NULL, NULL, '2023-02-01 04:29:47', '2023-02-01 04:29:47', NULL, NULL, NULL, NULL),
(6, 'Perkumpulan Unindras', 'Jalan TB Simatupang no 58 C', '27530', '27696', '27759', '27760', NULL, NULL, '2023-02-07 06:31:06', '2024-01-17 11:28:05', NULL, NULL, NULL, NULL),
(7, 'Ferdiansyah', 'Senduro Lumajang', '44156', '46199', '46315', '46319', NULL, NULL, '2023-02-19 14:08:40', '2023-02-19 14:08:40', NULL, NULL, NULL, NULL),
(8, 'Ghifa Farm', 'Senduro Lumajang', '44156', '46199', '46315', '46319', NULL, NULL, '2023-02-19 14:23:31', '2023-02-19 14:23:31', NULL, NULL, NULL, NULL),
(9, 'Afik Farm', 'Senduro Lumajang', '44156', '46199', '46315', '46319', NULL, NULL, '2023-02-19 14:25:39', '2023-02-19 14:25:39', NULL, NULL, NULL, NULL),
(10, 'Zahran Farm', 'Senduro Lumajang', '44156', '46199', '46315', '46319', NULL, NULL, '2023-02-19 14:29:16', '2023-02-19 14:29:16', NULL, NULL, NULL, NULL),
(11, 'Wily Farm', 'Probolinggo', '44156', '47346', '47415', '47417', NULL, NULL, '2023-02-19 14:30:25', '2023-02-19 14:30:25', NULL, NULL, NULL, NULL),
(12, 'Zahran Farming', 'Maron Probolinggo', '44156', '47346', '47588', '47590', NULL, NULL, '2023-02-19 14:32:28', '2023-02-19 14:32:28', NULL, NULL, NULL, NULL),
(13, 'Laili Farm', 'Banyuanyar Probolinggo', '44156', '47346', '47400', '47403', NULL, NULL, '2023-02-19 14:33:28', '2023-02-19 14:33:28', NULL, NULL, NULL, NULL),
(14, 'Retno Farm', 'Gading Probolinggo', '44156', '47346', '47447', '47465', NULL, NULL, '2023-02-19 14:34:57', '2023-02-19 14:34:57', NULL, NULL, NULL, NULL),
(15, 'Rizky Agung Farm', 'Banyuanyar Probolinggo', '44156', '47346', '47400', '47403', NULL, NULL, '2023-02-19 14:36:44', '2023-02-19 14:36:44', NULL, NULL, NULL, NULL),
(17, 'Kampong Embik', '-', '44156', '47346', '47347', '47359', NULL, NULL, '2023-06-12 04:54:33', '2023-06-12 04:54:33', NULL, NULL, NULL, NULL),
(18, 'NYX Farm', '-', '44156', '47346', '47415', '47427', NULL, NULL, '2023-06-12 04:56:44', '2023-06-12 04:56:44', NULL, NULL, NULL, NULL),
(19, 'Barkah Ratu Farm', '-', '44156', '47346', '47400', '47407', NULL, NULL, '2023-06-12 04:58:21', '2023-06-12 04:58:21', NULL, NULL, NULL, NULL),
(20, 'Yes Farm', '-', '44156', '47346', '47538', '47547', NULL, NULL, '2023-06-12 05:01:08', '2023-06-12 05:01:08', NULL, NULL, NULL, NULL),
(21, 'Fauzi Farm', '-', '44156', '47346', '47557', '47561', NULL, NULL, '2023-06-12 05:05:15', '2023-06-12 05:05:15', NULL, NULL, NULL, NULL),
(22, 'MWR Farm', '-', '44156', '47346', '47557', '47561', NULL, NULL, '2023-06-12 05:08:26', '2023-06-12 05:08:26', NULL, NULL, NULL, NULL),
(23, 'PROF Farm', '-', '44156', '47346', '47400', '47404', NULL, NULL, '2023-06-12 05:11:16', '2023-06-12 05:11:16', NULL, NULL, NULL, NULL),
(24, 'Roza Farm', '-', '44156', '47346', '47588', '47589', NULL, NULL, '2023-06-12 05:16:45', '2023-06-12 05:16:45', NULL, NULL, NULL, NULL),
(25, 'Barokah Jaya Farm', '-', '44156', '47346', '47557', '47564', NULL, NULL, '2023-06-12 05:26:13', '2023-06-12 05:26:13', NULL, NULL, NULL, NULL),
(26, 'Sapto Sukses Farm', '-', '44156', '47346', '47538', '47539', NULL, NULL, '2023-06-12 05:29:37', '2023-06-12 05:29:37', NULL, NULL, NULL, NULL),
(27, 'Lancar Jaya', '-', '44156', '47346', '47447', '47453', NULL, NULL, '2023-06-12 05:31:17', '2023-06-12 05:31:17', NULL, NULL, NULL, NULL),
(28, 'Hayat Berkah Jaya', '-', '44156', '47346', '47499', '47500', NULL, NULL, '2023-06-12 05:32:47', '2023-06-12 05:32:47', NULL, NULL, NULL, NULL),
(29, 'Zaini Farm', '-', '44156', '47346', '47538', '47547', NULL, NULL, '2023-06-12 05:37:02', '2023-06-12 05:37:02', NULL, NULL, NULL, NULL),
(30, 'Rikman Puskeswan', 'Senduro', '44156', '46199', '46315', '46319', NULL, NULL, '2023-06-14 04:20:17', '2023-06-14 04:20:17', NULL, NULL, NULL, NULL),
(31, 'Edwin DKPP Lumajang', '-', '44156', '46199', '46359', '46362', NULL, NULL, '2023-06-14 04:22:24', '2023-06-14 04:22:24', NULL, NULL, NULL, NULL),
(32, 'Mantri Balap Farm', '-', '44156', '46199', '46315', '46320', NULL, NULL, '2023-06-14 04:23:42', '2023-06-14 04:23:42', NULL, NULL, NULL, NULL),
(33, 'Eko Farm', '-', '44156', '46199', '46315', '46322', NULL, NULL, '2023-06-14 04:26:10', '2023-06-14 04:26:10', NULL, NULL, NULL, NULL),
(34, 'EL Farm', '-', '44156', '46199', '46315', '46322', NULL, NULL, '2023-06-14 04:28:20', '2023-06-14 04:28:20', NULL, NULL, NULL, NULL),
(35, 'Sumber Mas Kandangtepus', '-', '44156', '46199', '46315', '46322', NULL, NULL, '2023-06-14 04:30:59', '2023-06-14 04:30:59', NULL, NULL, NULL, NULL),
(36, 'Tumpi Balap Farm', '-', '44156', '46199', '46315', '46321', NULL, NULL, '2023-06-14 04:33:32', '2023-06-14 04:33:32', NULL, NULL, NULL, NULL),
(37, 'Susu Wedos Farm', '-', '44156', '46199', '46315', '46321', NULL, NULL, '2023-06-14 04:36:52', '2023-06-14 04:36:52', NULL, NULL, NULL, NULL),
(38, 'Jiwo Etawa', '-', '44156', '46199', '46307', '46309', NULL, NULL, '2023-06-14 04:40:59', '2023-06-14 04:40:59', NULL, NULL, NULL, NULL),
(39, 'Sumber Mas Telutur', '-', '44156', '46199', '46315', '46322', NULL, NULL, '2023-06-14 04:44:30', '2023-06-14 04:44:30', NULL, NULL, NULL, NULL),
(40, 'Sumber Mas Jambekumbu', '-', '44156', '46199', '46307', '46309', NULL, NULL, '2023-06-14 04:46:09', '2023-06-14 04:46:09', NULL, NULL, NULL, NULL),
(41, 'Goatzilla Farm', '-', '44156', '46199', '46315', '46321', NULL, NULL, '2023-06-14 04:48:13', '2023-06-14 04:48:13', NULL, NULL, NULL, NULL),
(42, 'Amir Farm', 'Senduro', '44156', '46199', '46315', '46319', NULL, NULL, '2023-07-07 03:03:26', '2023-07-07 03:03:26', NULL, NULL, NULL, NULL);
