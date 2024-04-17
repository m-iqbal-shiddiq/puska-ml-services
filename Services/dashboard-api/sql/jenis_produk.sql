-- -------------------------------------------------------------
-- TablePlus 5.9.6(546)
--
-- https://tableplus.com/
--
-- Database: postgres
-- Generation Time: 2024-04-15 22:48:52.2260
-- -------------------------------------------------------------


-- This script only contains the table creation statements and does not fully represent the table in the database. Do not use it as a backup.

-- Sequence and defined type
CREATE SEQUENCE IF NOT EXISTS jenis_produk_id_seq;

-- Table Definition
CREATE TABLE "public"."jenis_produk" (
    "id" int8 NOT NULL DEFAULT nextval('jenis_produk_id_seq'::regclass),
    "nama_produk" varchar(255) NOT NULL,
    "satuan" varchar(255) NOT NULL,
    "kategori" varchar(255) NOT NULL,
    PRIMARY KEY ("id")
);

INSERT INTO "public"."jenis_produk" ("id", "nama_produk", "satuan", "kategori") VALUES
(1, 'Daging Ternak', 'kg', 'ternak'),
(2, 'Ternak Potong', 'ekor', 'ternak'),
(3, 'Susu Segar', 'liter', 'susu'),
(4, 'Susu Pasteurisasi', 'liter', 'susu'),
(5, 'Susu Kefir', 'liter', 'susu'),
(6, 'Yogurt', 'liter', 'susu'),
(7, 'Keju', 'kg', 'susu');
