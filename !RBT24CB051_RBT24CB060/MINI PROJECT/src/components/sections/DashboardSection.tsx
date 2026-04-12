import React from "react";
import { useData } from "@/context/DataContext";
import { UploadZone } from "@/components/UploadZone";
import { TrendingUp, TrendingDown } from "lucide-react";
import {
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  Cell,
} from "recharts";

// Gradient utility: deep crimson → orange → amber
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

const StatCard: React.FC<{
  label: string;
  value: string;
  badge?: string;
  badgeColor?: string;
  sub?: string;
  delay?: number;
}> = ({ label, value, badge, badgeColor = "bg-success", sub, delay = 0 }) => (
  <div
    className="card-surface p-5 opacity-0 animate-fade-up"
    style={{ animationDelay: `${delay}ms`, animationFillMode: "forwards" }}
  >
    <p className="label-mono mb-1">{label}</p>
    <p className="stat-number">{value}</p>
    {badge && (
      <span
        className={`pill-badge text-[10px] mt-2 inline-block ${badgeColor} text-primary-foreground`}
      >
        {badge}
      </span>
    )}
    {sub && (
      <p className="text-[10px] font-mono text-muted-foreground mt-1">{sub}</p>
    )}
  </div>
);

export const DashboardSection: React.FC = () => {
  const { analysis, data, columns, numericColumns, fileName } = useData();

  if (!analysis) return <UploadZone />;

  // Target distribution
  const targetVals = analysis.target.values;
  const min = Math.min(...targetVals);
  const max = Math.max(...targetVals);
  const bins = 20;
  const binWidth = (max - min) / bins || 1;
  const histogram = Array.from({ length: bins }, (_, i) => {
    const lo = min + i * binWidth;
    const hi = lo + binWidth;
    const count = targetVals.filter(
      (v) => v >= lo && (i === bins - 1 ? v <= hi : v < hi),
    ).length;
    return { x: Math.round(((lo + hi) / 2) * 100) / 100, count };
  });

  // Correlation heatmap data
  const corrData = analysis.correlation;
  const cols = corrData.columns;
  const maxLen = Math.min(cols.length, 8);
  const displayCols = cols.slice(0, maxLen);

  // Top correlations to target
  const targetIdx = cols.length - 1;
  const topCorrs = cols
    .slice(0, -1)
    .map((col, i) => ({ col, corr: corrData.matrix[i][targetIdx] }))
    .sort((a, b) => Math.abs(b.corr) - Math.abs(a.corr))
    .slice(0, 6);

  return (
    <div className="space-y-6">
      {/* Stat cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <StatCard
          label="Total Records"
          value={analysis.totalRows.toLocaleString()}
          badge="Loaded"
          delay={0}
        />
        <StatCard
          label="Columns"
          value={analysis.totalColumns.toString()}
          badge={`${numericColumns.length} numeric`}
          badgeColor="bg-primary"
          delay={40}
        />
        <StatCard
          label="Active Dataset"
          value={fileName || "—"}
          sub="uploaded · ready for ML"
          delay={80}
        />
        <StatCard
          label="Data Quality"
          value={analysis.totalMissing.toString()}
          badge={
            analysis.totalMissing > 0
              ? `${analysis.totalMissing} missing`
              : "Clean"
          }
          badgeColor={
            analysis.totalMissing > 0 ? "bg-destructive" : "bg-success"
          }
          sub="missing values"
          delay={120}
        />
      </div>

      {/* Charts row 1 */}
      <div className="grid grid-cols-1 lg:grid-cols-5 gap-4">
        {/* Correlation Heatmap */}
        <div className="card-surface p-5 lg:col-span-3">
          <h3 className="font-heading text-[15px] font-bold mb-0.5">
            Feature Correlation
          </h3>
          <p className="label-mono mb-4">Pearson coefficient matrix</p>
          <div className="overflow-x-auto">
            <table className="w-full text-[10px] font-mono">
              <thead>
                <tr>
                  <th />
                  {displayCols.map((c) => (
                    <th
                      key={c}
                      className="px-1 py-1 text-muted-foreground truncate max-w-[60px]"
                    >
                      {c.slice(0, 8)}
                    </th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {displayCols.map((row, i) => (
                  <tr key={row}>
                    <td className="pr-2 text-muted-foreground truncate max-w-[60px]">
                      {row.slice(0, 8)}
                    </td>
                    {displayCols.map((_, j) => {
                      const val = corrData.matrix[i][j];
                      const intensity = Math.abs(val);
                      const isPositive = val >= 0;
                      const bg = isPositive
                        ? `rgba(232, 87, 26, ${intensity * 0.85})`
                        : `rgba(59, 130, 246, ${intensity * 0.7})`;
                      return (
                        <td
                          key={j}
                          className="px-1 py-1 text-center rounded-sm"
                          style={{
                            backgroundColor: bg,
                            color:
                              intensity > 0.4 ? "#fff" : "hsl(48, 6%, 47%)",
                          }}
                        >
                          {val.toFixed(2)}
                        </td>
                      );
                    })}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* Target Distribution */}
        <div className="card-surface p-5 lg:col-span-2">
          <h3 className="font-heading text-[15px] font-bold mb-0.5">
            Target Distribution
          </h3>
          <p className="label-mono mb-4">{analysis.target.name}</p>
          <ResponsiveContainer width="100%" height={200}>
            <BarChart data={histogram}>
              <CartesianGrid strokeDasharray="3 3" stroke="hsl(53, 6%, 14%)" />
              <XAxis
                dataKey="x"
                tick={{ fontSize: 10, fill: "hsl(48, 6%, 47%)" }}
              />
              <YAxis tick={{ fontSize: 10, fill: "hsl(48, 6%, 47%)" }} />
              <Tooltip
                contentStyle={{
                  backgroundColor: "#181916",
                  border: "1px solid #252620",
                  borderRadius: 10,
                }}
                labelStyle={{ color: "#F0EEE8" }}
              />
              <Bar dataKey="count" radius={[4, 4, 0, 0]}>
                {histogram.map((_, index) => (
                  <Cell
                    key={index}
                    fill={gradientColor(index / (histogram.length - 1))}
                  />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Charts row 2 */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
        {/* Top correlations to target */}
        <div className="card-surface p-5">
          <h3 className="font-heading text-[15px] font-bold mb-0.5">
            Top Feature Correlations to Target
          </h3>
          <p className="label-mono mb-4">
            Strongest predictors of {analysis.target.name}
          </p>
          <div className="space-y-3">
            {topCorrs.map(({ col, corr }) => (
              <div key={col} className="flex items-center gap-3">
                <div
                  className="h-4 w-4 rounded-sm shrink-0"
                  style={{ backgroundColor: gradientColor(Math.abs(corr)) }}
                />
                <span className="text-sm text-foreground flex-1 truncate">
                  {col}
                </span>
                <span className="font-mono text-sm font-bold text-foreground">
                  {corr.toFixed(2)}
                </span>
                <div className="w-24 h-1.5 bg-muted rounded-full overflow-hidden">
                  <div
                    className="h-full rounded-full"
                    style={{
                      width: `${Math.abs(corr) * 100}%`,
                      backgroundColor: gradientColor(Math.abs(corr)),
                    }}
                  />
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Data preview */}
        <div className="card-surface p-5 overflow-hidden">
          <h3 className="font-heading text-[15px] font-bold mb-0.5">
            Dataset Preview
          </h3>
          <p className="label-mono mb-4">First 8 rows</p>
          <div className="overflow-x-auto">
            <table className="w-full text-[11px]">
              <thead>
                <tr>
                  {columns.slice(0, 6).map((c) => (
                    <th
                      key={c}
                      className="px-2 py-1.5 text-left label-mono bg-accent"
                    >
                      {c.slice(0, 12)}
                    </th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {data.slice(0, 8).map((row, i) => (
                  <tr key={i} className={i % 2 === 0 ? "" : "bg-accent/30"}>
                    {columns.slice(0, 6).map((c) => (
                      <td
                        key={c}
                        className="px-2 py-1 font-mono text-muted-foreground"
                      >
                        {typeof row[c] === "number"
                          ? (row[c] as number).toFixed(2)
                          : String(row[c] ?? "")}
                      </td>
                    ))}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  );
};
