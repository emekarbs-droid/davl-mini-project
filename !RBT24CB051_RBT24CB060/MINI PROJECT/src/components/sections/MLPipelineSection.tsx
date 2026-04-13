import React from "react";
import { useData } from "@/context/DataContext";
import {
  ResponsiveContainer,
  ScatterChart,
  Scatter,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  BarChart,
  Bar,
  ReferenceLine,
  Cell,
} from "recharts";

function gradientColor(t: number): string {
  const clamp = Math.max(0, Math.min(1, t));
  if (clamp < 0.5) {
    const s = clamp * 2;
    return `rgb(${Math.round(123 + (232 - 123) * s)},${Math.round(31 + (87 - 31) * s)},${Math.round(10 + (26 - 10) * s)})`;
  } else {
    const s = (clamp - 0.5) * 2;
    return `rgb(${Math.round(232 + (245 - 232) * s)},${Math.round(87 + (185 - 87) * s)},${Math.round(26 + (66 - 26) * s)})`;
  }
}

const tooltipStyle = {
  contentStyle: { backgroundColor: "#181916", border: "1px solid #252620", borderRadius: 10 },
  labelStyle: { color: "#F0EEE8" },
};

const ChartCard: React.FC<{ title: string; sub: string; children: React.ReactNode }> = ({ title, sub, children }) => (
  <div className="card-surface p-5">
    <h3 className="font-heading text-[15px] font-bold mb-0.5">{title}</h3>
    <p className="label-mono mb-3">{sub}</p>
    {children}
  </div>
);

const MiniMetric: React.FC<{ label: string; value: string; sub?: string }> = ({ label, value, sub }) => (
  <div className="card-surface p-4 text-center">
    <p className="label-mono mb-1">{label}</p>
    <p className="font-heading text-xl font-bold text-primary">{value}</p>
    {sub && <p className="text-[10px] font-mono text-muted-foreground mt-0.5">{sub}</p>}
  </div>
);

export const MLPipelineSection: React.FC = () => {
  const { analysis } = useData();

  if (!analysis) return <p className="text-muted-foreground">Upload a CSV first.</p>;

  const { pca, lda, factorAnalysis, regression, correlation } = analysis;

  // PCA — normalize target for color gradient
  const tVals = analysis.target.values;
  const tMin = Math.min(...tVals);
  const tMax = Math.max(...tVals);
  const pcaData = pca.projected.map((p, i) => ({
    x: p[0] || 0,
    y: p[1] || 0,
    t: tMax === tMin ? 0.5 : (tVals[i] - tMin) / (tMax - tMin),
  })).slice(0, 500);

  // Predicted vs Actual
  const predActual = regression.predictions.map((p, i) => ({
    actual: regression.actuals[i],
    predicted: p,
    t: i / Math.max(regression.predictions.length - 1, 1),
  }));

  // LDA — jitter centered so dots don't clip
  const ldaBelow = lda.projected
    .map((v, i) => ({ x: v, y: 0.15 + Math.random() * 0.35, label: lda.labels[i] }))
    .filter((d) => d.label === 0)
    .slice(0, 500);
  const ldaAbove = lda.projected
    .map((v, i) => ({ x: v, y: 0.15 + Math.random() * 0.35, label: lda.labels[i] }))
    .filter((d) => d.label === 1)
    .slice(0, 500);

  // Factor Analysis — name is a string, don't tickFormatter it
  const featureCols = correlation.columns.slice(0, -1);
  const faData = featureCols.slice(0, 8).map((col, i) => ({
    name: col.slice(0, 8),
    factor1: factorAnalysis.loadings[i]?.[0] ?? 0,
    factor2: factorAnalysis.loadings[i]?.[1] ?? 0,
  }));

  const numFmt = (v: any) => {
    const n = Number(v);
    return isNaN(n) ? "" : n.toFixed(2);
  };

  return (
    <div className="space-y-4">
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">

        {/* PCA */}
        <ChartCard
          title="PCA Projection"
          sub={`PC1 · ${pca.varianceExplained[0]?.toFixed(1)}% — PC2 · ${pca.varianceExplained[1]?.toFixed(1)}%`}
        >
          <ResponsiveContainer width="100%" height={240}>
            <ScatterChart>
              <CartesianGrid strokeDasharray="3 3" stroke="hsl(53,6%,14%)" />
              <XAxis dataKey="x" tick={{ fontSize: 10, fill: "#7A7870" }} name="PC1" tickFormatter={numFmt} />
              <YAxis dataKey="y" tick={{ fontSize: 10, fill: "#7A7870" }} name="PC2" tickFormatter={numFmt} />
              <Tooltip {...tooltipStyle} />
              <Scatter data={pcaData} opacity={0.8} r={3}>
                {pcaData.map((d, i) => (
                  <Cell key={i} fill={gradientColor(d.t)} />
                ))}
              </Scatter>
            </ScatterChart>
          </ResponsiveContainer>
        </ChartCard>

        {/* Predicted vs Actual */}
        <ChartCard title="Predicted vs Actual" sub="Linear regression test set">
          <ResponsiveContainer width="100%" height={240}>
            <ScatterChart>
              <CartesianGrid strokeDasharray="3 3" stroke="hsl(53,6%,14%)" />
              <XAxis dataKey="actual" tick={{ fontSize: 10, fill: "#7A7870" }} name="Actual" tickFormatter={numFmt} />
              <YAxis dataKey="predicted" tick={{ fontSize: 10, fill: "#7A7870" }} name="Predicted" tickFormatter={numFmt} />
              <Tooltip {...tooltipStyle} />
              <Scatter data={predActual} opacity={0.75} r={3}>
                {predActual.map((d, i) => (
                  <Cell key={i} fill={gradientColor(d.t)} />
                ))}
              </Scatter>
              <ReferenceLine
                segment={[
                  { x: Math.min(...regression.actuals), y: Math.min(...regression.actuals) },
                  { x: Math.max(...regression.actuals), y: Math.max(...regression.actuals) },
                ]}
                stroke="#3E3D38"
                strokeDasharray="4 4"
              />
            </ScatterChart>
          </ResponsiveContainer>
        </ChartCard>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">

        {/* LDA */}
        <ChartCard title="LDA Projection" sub={`Accuracy: ${(lda.accuracy * 100).toFixed(1)}%`}>
          <ResponsiveContainer width="100%" height={240}>
            <ScatterChart>
              <CartesianGrid strokeDasharray="3 3" stroke="hsl(53,6%,14%)" />
              <XAxis dataKey="x" tick={{ fontSize: 10, fill: "#7A7870" }} name="LD1" tickFormatter={numFmt} />
              <YAxis
                dataKey="y"
                tick={false}
                axisLine={false}
                tickLine={false}
                domain={[0, 0.6]}
              />
              <Tooltip {...tooltipStyle} />
              <Scatter data={ldaBelow} opacity={0.8} r={3} name="Below Mean">
                {ldaBelow.map((_, i) => (
                  <Cell key={i} fill={gradientColor(0.15)} />
                ))}
              </Scatter>
              <Scatter data={ldaAbove} opacity={0.8} r={3} name="Above Mean">
                {ldaAbove.map((_, i) => (
                  <Cell key={i} fill={gradientColor(0.85)} />
                ))}
              </Scatter>
            </ScatterChart>
          </ResponsiveContainer>
          <div className="flex gap-4 mt-2 text-[10px] font-mono text-muted-foreground">
            <span className="flex items-center gap-1">
              <span className="h-2 w-2 rounded-full" style={{ backgroundColor: gradientColor(0.15) }} />
              Below Mean
            </span>
            <span className="flex items-center gap-1">
              <span className="h-2 w-2 rounded-full" style={{ backgroundColor: gradientColor(0.85) }} />
              Above Mean
            </span>
          </div>
        </ChartCard>

        {/* Factor Analysis — NO tickFormatter on XAxis (names are strings) */}
        <ChartCard title="Factor Analysis Loadings" sub="Top features per factor">
          <ResponsiveContainer width="100%" height={240}>
            <BarChart data={faData}>
              <CartesianGrid strokeDasharray="3 3" stroke="hsl(53,6%,14%)" />
              <XAxis dataKey="name" tick={{ fontSize: 9, fill: "#7A7870" }} />
              <YAxis tick={{ fontSize: 10, fill: "#7A7870" }} tickFormatter={numFmt} />
              <Tooltip {...tooltipStyle} />
              <ReferenceLine y={0} stroke="#3E3D38" />
              <Bar dataKey="factor1" fill={gradientColor(0.5)} name="Factor 1" radius={[3, 3, 0, 0]} />
              <Bar dataKey="factor2" fill={gradientColor(0.85)} name="Factor 2" radius={[3, 3, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </ChartCard>
      </div>

      {/* Metric cards */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        <MiniMetric label="MSE" value={regression.mse.toFixed(3)} sub="Mean Squared Error" />
        <MiniMetric label="RMSE" value={regression.rmse.toFixed(3)} sub="Root MSE" />
        <MiniMetric label="PCA Variance" value={`${pca.totalVariance.toFixed(1)}%`} sub="PC1 + PC2" />
        <MiniMetric label="LDA Accuracy" value={`${(lda.accuracy * 100).toFixed(1)}%`} sub="Train accuracy" />
      </div>
    </div>
  );
};