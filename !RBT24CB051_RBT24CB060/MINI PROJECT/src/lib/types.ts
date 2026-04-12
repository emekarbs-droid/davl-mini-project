export interface AnalysisResults {
  correlation: {
    matrix: number[][];
    columns: string[];
    topPair: [string, string, number];
    highCorrCount: number;
    topPredictorOfTarget: [string, number];
  };
  pca: {
    projected: number[][];
    varianceExplained: number[];
    totalVariance: number;
  };
  lda: {
    projected: number[];
    labels: number[];
    accuracy: number;
    threshold: number;
    ldComponents: number;
  };
  factorAnalysis: {
    loadings: number[][];
    topFeaturePerFactor: [string, number][];
  };
  regression: {
    predictions: number[];
    actuals: number[];
    mse: number;
    rmse: number;
    r2: number;
  };
  classification: {
    models: { name: string; accuracy: number }[];
  };
  target: {
    mean: number;
    std: number;
    skew: number;
    values: number[];
    name: string;
  };
  missingValues: Record<string, number>;
  totalRows: number;
  totalColumns: number;
  totalMissing: number;
}