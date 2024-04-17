-- -------------------------------------------------------------
-- TablePlus 5.9.6(546)
--
-- https://tableplus.com/
--
-- Database: postgres
-- Generation Time: 2024-04-15 22:56:50.3370
-- -------------------------------------------------------------


-- This script only contains the table creation statements and does not fully represent the table in the database. Do not use it as a backup.

-- Sequence and defined type
CREATE SEQUENCE IF NOT EXISTS produksi_ternak_id_seq;

-- Table Definition
CREATE TABLE "public"."produksi_ternak" (
    "id" int8 NOT NULL DEFAULT nextval('produksi_ternak_id_seq'::regclass),
    "tgl_produksi" date NOT NULL,
    "jumlah" numeric(8,2) NOT NULL,
    "satuan" varchar(255) NOT NULL,
    "sumber_pasokan" varchar(255) NOT NULL CHECK ((sumber_pasokan)::text = ANY (ARRAY[('Peternakan Sendiri'::character varying)::text, ('Peternakan Lain'::character varying)::text, ('Pengepul'::character varying)::text])),
    "created_at" timestamp(0),
    "updated_at" timestamp(0),
    "deleted_at" timestamp(0),
    "created_by" int8,
    "updated_by" int8,
    "deleted_by" int8,
    "id_unit_ternak" int8 NOT NULL,
    "id_jenis_produk" int8 NOT NULL,
    CONSTRAINT "produksi_ternak_id_unit_ternak_foreign" FOREIGN KEY ("id_unit_ternak") REFERENCES "public"."unit_ternak"("id"),
    CONSTRAINT "produksi_ternak_id_jenis_produk_foreign" FOREIGN KEY ("id_jenis_produk") REFERENCES "public"."jenis_produk"("id"),
    PRIMARY KEY ("id")
);

INSERT INTO "public"."produksi_ternak" ("id", "tgl_produksi", "jumlah", "satuan", "sumber_pasokan", "created_at", "updated_at", "deleted_at", "created_by", "updated_by", "deleted_by", "id_unit_ternak", "id_jenis_produk") VALUES
(1, '2023-02-18', 5.00, 'ekor', 'Peternakan Sendiri', '2023-02-19 16:08:20', '2023-02-19 16:08:20', NULL, NULL, NULL, NULL, 12, 1),
(2, '2023-02-18', 4.00, 'ekor', 'Pengepul', '2023-02-20 00:39:12', '2023-02-20 00:39:12', NULL, NULL, NULL, NULL, 15, 1),
(3, '2023-02-19', 15.00, 'kg', 'Peternakan Sendiri', '2023-02-20 00:39:52', '2023-02-20 00:39:52', NULL, NULL, NULL, NULL, 15, 2),
(4, '2023-02-19', 4.00, 'ekor', 'Pengepul', '2023-02-20 00:40:38', '2023-02-20 00:40:38', NULL, NULL, NULL, NULL, 15, 1),
(5, '2023-02-18', 15.00, 'kg', 'Peternakan Sendiri', '2023-02-20 00:41:03', '2023-02-20 00:41:03', NULL, NULL, NULL, NULL, 15, 2),
(6, '2023-02-20', 15.00, 'kg', 'Peternakan Sendiri', '2023-02-20 01:16:33', '2023-02-20 01:16:33', NULL, NULL, NULL, NULL, 4, 1),
(7, '2023-02-20', 2.00, 'ekor', 'Peternakan Sendiri', '2023-02-20 01:16:44', '2023-02-20 01:16:44', NULL, NULL, NULL, NULL, 4, 2),
(8, '2023-02-18', 2.00, 'ekor', 'Pengepul', '2023-02-20 01:49:36', '2023-02-20 01:49:36', NULL, NULL, NULL, NULL, 14, 1),
(9, '2023-02-20', 2.00, 'ekor', 'Peternakan Sendiri', '2023-02-20 01:50:29', '2023-02-20 01:50:29', NULL, NULL, NULL, NULL, 14, 1),
(10, '2023-02-18', 2.00, 'ekor', 'Peternakan Sendiri', '2023-02-20 01:51:03', '2023-02-20 01:51:03', NULL, NULL, NULL, NULL, 4, 1),
(11, '2023-02-19', 10.00, 'kg', 'Peternakan Lain', '2023-02-20 01:52:19', '2023-02-20 01:52:19', NULL, NULL, NULL, NULL, 14, 2),
(12, '2023-02-21', 5.00, 'ekor', 'Peternakan Sendiri', '2023-02-21 15:49:12', '2023-02-21 15:49:12', NULL, NULL, NULL, NULL, 12, 1),
(13, '2023-02-21', 20.00, 'kg', 'Peternakan Lain', '2023-02-21 15:49:35', '2023-02-21 15:49:35', NULL, NULL, NULL, NULL, 4, 2),
(14, '2023-03-29', 1.00, 'ekor', 'Peternakan Sendiri', '2023-03-28 22:46:47', '2023-03-28 22:46:47', NULL, NULL, NULL, NULL, 1, 1),
(15, '2023-04-04', 2.00, 'ekor', 'Peternakan Sendiri', '2023-04-03 22:05:16', '2023-04-03 22:05:16', NULL, NULL, NULL, NULL, 4, 1),
(16, '2023-05-07', 15.00, 'kg', 'Peternakan Sendiri', '2023-05-07 03:02:45', '2023-05-07 03:02:45', NULL, NULL, NULL, NULL, 4, 1),
(17, '2023-06-16', 12.00, 'ekor', 'Peternakan Sendiri', '2023-06-16 15:09:02', '2023-06-16 15:09:02', NULL, NULL, NULL, NULL, 32, 1),
(18, '2023-06-30', 25.00, 'ekor', 'Peternakan Sendiri', '2023-07-01 05:12:43', '2023-07-01 05:12:43', NULL, NULL, NULL, NULL, 18, 1),
(19, '2023-07-01', 1.00, 'ekor', 'Peternakan Sendiri', '2023-07-04 02:22:52', '2023-07-04 02:22:52', NULL, NULL, NULL, NULL, 18, 2),
(20, '2023-07-30', 5.00, 'ekor', 'Peternakan Sendiri', '2023-07-30 01:32:16', '2023-07-30 01:32:16', NULL, NULL, NULL, NULL, 4, 2);
