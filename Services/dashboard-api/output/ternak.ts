interface MasterData {
  ternak_potong: {
    produksi: number;
    distribusi: number;
    persentase: number;
  };
  daging_ternak: {
    produksi: number;
    distribusi: number;
    persentase: number;
  };
  susu_segar: {
    produksi: number;
    distribusi: number;
    persentase: number;
  };
  pro_dis_ternak_potong: {
    label: string;
    value: number;
  }[];
  pro_dis_daging_ternak: {
    label: string;
    value: number;
  }[];
  pro_dis_susu_segar: {
    label: string;
    value: number;
  }[];
  sebaran_populasi: {
    coord: [number, number];
    title: string;
  }[];
  ringkasan_populasi: {
    jumlah_perah_dewasa: {
      produksi: number;
      distribusi: number;
    };
    jumlah_perah_anakan: {
      produksi: number;
      distribusi: number;
    };
    jumlah_pedaging_dewasa: {
      produksi: number;
      distribusi: number;
    };
    jumlah_pedaging_anakan: {
      produksi: number;
      distribusi: number;
    };
  };
  table: {
    wilayah: string;
    perah_dewasa_jantan: number;
    perah_dewasa_betina: number;
    perah_anakan_jantan: number;
    perah_anakan_betina: number;
    pedaging_dewasa_jantan: number;
    pedaging_dewasa_betina: number;
    pedaging_anakan_jantan: number;
    pedaging_anakan_betina: number;
  }[];
}