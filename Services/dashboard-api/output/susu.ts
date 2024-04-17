interface Color {
  bgColor: string;
  borderColor: string;
}

interface ProduksiDistribusi {
  produksi: number;
  distribusi: number;
}

interface PrediksiProduksi {
  graph: object; // Since the actual structure is unknown, we use object
  timestamp: string;
  liter_prediction: number;
}

interface PieChartItem {
  no: number;
  label: string;
  bgColor: string;
  borderColor: string;
}

interface HargaSusu {
  mean: string;
  min: string;
  max: string;
}

type masterData = {
  prod_dis: {
    susu_segar_liter: ProduksiDistribusi;
    susu_pasteurisasi_liter: ProduksiDistribusi;
    kefir_liter: ProduksiDistribusi;
    yogurt_liter: ProduksiDistribusi;
    keju_kg: ProduksiDistribusi;
  };
  prediksi_produksi_susu_segar: {
    label: string;
    value: number;
  }[];
  prediksi_produksi: PrediksiProduksi;
  pie_prod_per_produk: PieChartItem[];
  pie_dis_per_produk: PieChartItem[];
  pro_dis_susu: {
    label: string;
    value: number;
  }[];
  graph_bar_permintaan_susu: {
    labels: string[];
    datasets: {
      label: string;
      data: number[];
      backgroundColor: string;
    }[];
  };
  persentase_distribusi_pct: number;
  total_pendapatan_idr: string;
  harga_susu: HargaSusu;
}
