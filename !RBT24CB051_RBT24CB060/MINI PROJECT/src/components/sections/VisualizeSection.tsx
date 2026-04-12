import React, { useState } from "react";
import { useData } from "@/context/DataContext";
import {
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  ScatterChart,
  Scatter,
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

const ChartCard: React.FC<{ title: string; sub: string; children: React.ReactNode }> = ({ title, sub, children }) => (
  <div className="card-surface p-5">
    <h3 className="font-heading text-[15px] font-bold mb-0.5">{title}</h3>
    <p className="label-mono mb-4">{sub}</p>
    {children}
  </div>
);

const tooltipStyle = {
  contentStyle: { backgroundColor: "#181916", border: "1px solid #252620", borderRadius: 10 },
  labelStyle: { color: "#F0EEE8" },
};

export const VisualizeSection: React.FC = () => {
  const { analysis, data, numericColumns, columns } = useData();
  const [histCol, setHistCol] = useState(numericColumns[0] || "");
  const [scatterX, setScatterX] = useState(numericColumns[0] || "");
  const [scatterY, setScatterY] = useState(numericColumns[1] || "");

  if (!analysis) return <p className="text-muted-foreground">Upload a CSV first.</p>;

  // Histogram data — correct field is "count"
  const colVals = data.map((r) => Number(r[histCol])).filter((v) => !isNaN(v) && isFinite(v));
  const hMin = colVals.length > 0 ? Math.min(...colVals) : 0;
  const hMax = colVals.length > 0 ? Math.max(...colVals) : 1;
  const hBins = 15;
  const hBinW = (hMax - hMin) / hBins || 1;
  const histData = Array.from({ length: hBins }, (_, i) => {
    const lo = hMin + i * hBinW;
    const hi = lo + hBinW;
    return {
      bin: ((lo + hi) / 2).toFixed(1),
      count: colVals.filter((v) => v >= lo && (i === hBins - 1 ? v <= hi : v < hi)).length,
    };
  });

  // Scatter data
  const scatterData = data.slice(0, 500).map((r, i) => ({
    x: Number(r[scatterX]) || 0,
    y: Number(r[scatterY]) || 0,
    t: i / Math.min(data.length - 1, 499),
  }));

  // Missing values — correct field is "pct"
  const missingData = columns
    .map((col) => ({
      col: col.slice(0, 12),
      pct: (analysis.missingValues[col] / analysis.totalRows) * 100,
    }))
    .sort((a, b) => b.pct - a.pct)
    .slice(0, 10);

  // Box plot
  const sorted = [...colVals].sort((a, b) => a - b);
  const q1 = sorted[Math.floor(sorted.length * 0.25)] || 0;
  const median = sorted[Math.floor(sorted.length * 0.5)] || 0;
  const q3 = sorted[Math.floor(sorted.length * 0.75)] || 0;
  const iqr = q3 - q1;
  const whiskerLow = Math.max(hMin, q1 - 1.5 * iqr);
  const whiskerHigh = Math.min(hMax, q3 + 1.5 * iqr);

  const Select: React.FC<{ value: string; onChange: (v: string) => void }> = ({ value, onChange }) => (
    <select
      value={value}
      onChange={(e) => onChange(e.target.value)}
      className="bg-accent border border-border rounded-md px-2 py-1 text-xs font-mono text-foreground"
    >
      {numericColumns.map((c) => <option key={c} value={c}>{c}</option>)}
    </select>
  );

  return (
    <div className="space-y-4">
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">

        {/* Histogram — dataKey="count" */}
        <ChartCard title="Histogram" sub="Distribution of selected column">
          <Select value={histCol} onChange={setHistCol} />
          <ResponsiveContainer width="100%" height={220} className="mt-3">
            <BarChart data={histData}>
              <CartesianGrid strokeDasharray="3 3" stroke="hsl(53,6%,14%)" />
              <XAxis dataKey="bin" tick={{ fontSize: 10, fill: "#7A7870" }} />
              <YAxis tick={{ fontSize: 10, fill: "#7A7870" }} />
              <Tooltip {...tooltipStyle} />
              <Bar dataKey="count" radius={[4, 4, 0, 0]}>
                {histData.map((_, i) => (
                  <Cell key={i} fill={gradientColor(i / Math.max(histData.length - 1, 1))} />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </ChartCard>

        {/* Box Plot */}
        <ChartCard title="Box Plot" sub={`${histCol} — Q1, Median, Q3, Whiskers`}>
          <svg viewBox="0 0 300 80" className="w-full h-[220px]">
            <line x1={30} y1={40} x2={270} y2={40} stroke="#3E3D38" strokeWidth={1} />
            <line
              x1={30 + ((whiskerLow - hMin) / (hMax - hMin || 1)) * 240} y1={25}
              x2={30 + ((whiskerLow - hMin) / (hMax - hMin || 1)) * 240} y2={55}
              stroke="#7A7870" strokeWidth={1.5}
            />
            <line
              x1={30 + ((whiskerHigh - hMin) / (hMax - hMin || 1)) * 240} y1={25}
              x2={30 + ((whiskerHigh - hMin) / (hMax - hMin || 1)) * 240} y2={55}
              stroke="#7A7870" strokeWidth={1.5}
            />
            <rect
              x={30 + ((q1 - hMin) / (hMax - hMin || 1)) * 240}
              y={20}
              width={Math.max(2, ((q3 - q1) / (hMax - hMin || 1)) * 240)}
              height={40}
              fill={gradientColor(0.5)}
              opacity={0.75}
              rx={4}
            />
            <line
              x1={30 + ((median - hMin) / (hMax - hMin || 1)) * 240} y1={18}
              x2={30 + ((median - hMin) / (hMax - hMin || 1)) * 240} y2={62}
              stroke="#F0EEE8" strokeWidth={2}
            />
          </svg>
        </ChartCard>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">

        {/* Scatter Plot */}
        <ChartCard title="Scatter Plot" sub="Feature relationship">
          <div className="flex gap-2 mb-3">
            <div className="flex items-center gap-1 text-xs text-muted-foreground">
              X: <Select value={scatterX} onChange={setScatterX} />
            </div>
            <div className="flex items-center gap-1 text-xs text-muted-foreground">
              Y: <Select value={scatterY} onChange={setScatterY} />
            </div>
          </div>
          <ResponsiveContainer width="100%" height={220}>
            <ScatterChart>
              <CartesianGrid strokeDasharray="3 3" stroke="hsl(53,6%,14%)" />
              <XAxis dataKey="x" tick={{ fontSize: 10, fill: "#7A7870" }} name={scatterX} tickFormatter={(v) => Number(v).toFixed(1)} />
              <YAxis dataKey="y" tick={{ fontSize: 10, fill: "#7A7870" }} name={scatterY} tickFormatter={(v) => Number(v).toFixed(1)} />
              <Tooltip {...tooltipStyle} />
              <Scatter data={scatterData} opacity={0.75} r={3}>
                {scatterData.map((d, i) => (
                  <Cell key={i} fill={gradientColor(d.t)} />
                ))}
              </Scatter>
            </ScatterChart>
          </ResponsiveContainer>
        </ChartCard>

        {/* Missing Values — dataKey="pct" */}
        <ChartCard title="Missing Values" sub="Percentage missing per column">
          <ResponsiveContainer width="100%" height={220}>
            <BarChart data={missingData} layout="vertical">
              <CartesianGrid strokeDasharray="3 3" stroke="hsl(53,6%,14%)" />
              <XAxis type="number" tick={{ fontSize: 10, fill: "#7A7870" }} domain={[0, 100]} unit="%" />
              <YAxis type="category" dataKey="col" tick={{ fontSize: 10, fill: "#7A7870" }} width={80} />
              <Tooltip {...tooltipStyle} />
              <Bar dataKey="pct" radius={[0, 4, 4, 0]}>
                {missingData.map((_, i) => (
                  <Cell key={i} fill={gradientColor(i / Math.max(missingData.length - 1, 1))} />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </ChartCard>

      </div>
    </div>
  );
};