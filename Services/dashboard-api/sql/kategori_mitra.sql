-- -------------------------------------------------------------
-- TablePlus 5.9.6(546)
--
-- https://tableplus.com/
--
-- Database: postgres
-- Generation Time: 2024-04-15 22:50:57.1510
-- -------------------------------------------------------------


-- This script only contains the table creation statements and does not fully represent the table in the database. Do not use it as a backup.

-- Sequence and defined type
CREATE SEQUENCE IF NOT EXISTS kategori_mitra_id_seq;

-- Table Definition
CREATE TABLE "public"."kategori_mitra" (
    "id" int8 NOT NULL DEFAULT nextval('kategori_mitra_id_seq'::regclass),
    "nama_kategori" varchar(255) NOT NULL,
    PRIMARY KEY ("id")
);

INSERT INTO "public"."kategori_mitra" ("id", "nama_kategori") VALUES
(1, 'Pabrik Susu Bubuk'),
(2, 'Pabrik Kosmetik'),
(3, 'Pabrik Bahan Makanan'),
(4, 'Pabrik Daging'),
(5, 'Pabrik Farmasi'),
(6, 'Koperasi'),
(7, 'Konsumen/warga'),
(8, 'Pasar Hewan'),
(9, 'Rumah Makan/ Restoran'),
(10, 'Home Industri');
