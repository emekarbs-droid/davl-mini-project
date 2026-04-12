import React from "react";
import { useData } from "@/context/DataContext";

export const DataExplorerSection: React.FC = () => {
  const { analysis, data, columns } = useData();

  if (!analysis) return <p className="text-muted-foreground">Upload a CSV first.</p>;

  return (
    <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
      {/* Dataset preview */}
      <div className="card-surface p-5 lg:col-span-2 overflow-hidden">
        <h3 className="font-heading text-[15px] font-bold mb-0.5">Dataset Preview</h3>
        <p className="label-mono mb-4">First 10 rows</p>
        <div className="overflow-x-auto">
          <table className="w-full text-[11px]">
            <thead>
              <tr>
                {columns.map(c => (
                  <th key={c} className="px-3 py-2 text-left label-mono bg-accent whitespace-nowrap">{c}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {data.slice(0, 10).map((row, i) => (
                <tr key={i} className={i % 2 === 0 ? "" : "bg-accent/30"}>
                  {columns.map(c => (
                    <td key={c} className="px-3 py-1.5 font-mono text-muted-foreground whitespace-nowrap">
                      {typeof row[c] === "number" ? (row[c] as number).toFixed(2) : String(row[c] ?? "")}
                    </td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Missing values audit */}
      <div className="card-surface p-5">
        <h3 className="font-heading text-[15px] font-bold mb-0.5">Missing Values Audit</h3>
        <p className="label-mono mb-4">Per-column analysis</p>
        <div className="overflow-y-auto max-h-[500px]">
          <table className="w-full text-[11px]">
            <thead>
              <tr>
                <th className="px-2 py-2 text-left label-mono bg-accent">Column</th>
                <th className="px-2 py-2 text-right label-mono bg-accent">Missing</th>
                <th className="px-2 py-2 text-right label-mono bg-accent">Status</th>
              </tr>
            </thead>
            <tbody>
              {columns.map((col, i) => {
                const missing = analysis.missingValues[col] || 0;
                const pct = (missing / analysis.totalRows) * 100;
                return (
                  <tr key={col} className={i % 2 === 0 ? "" : "bg-accent/30"}>
                    <td className="px-2 py-1.5 font-mono text-muted-foreground truncate max-w-[120px]">{col}</td>
                    <td className="px-2 py-1.5 font-mono text-muted-foreground text-right">{missing}</td>
                    <td className="px-2 py-1.5 text-right">
                      {missing === 0 ? (
                        <span className="pill-badge bg-success/20 text-success text-[9px] py-0.5">Clean</span>
                      ) : (
                        <span className="pill-badge bg-destructive/20 text-destructive text-[9px] py-0.5">
                          {pct.toFixed(1)}%
                        </span>
                      )}
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};
