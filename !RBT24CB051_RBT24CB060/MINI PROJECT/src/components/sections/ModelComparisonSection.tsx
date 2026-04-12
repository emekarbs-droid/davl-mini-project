import React, { useEffect, useState } from "react";
import { useData } from "@/context/DataContext";
import {
  ResponsiveContainer, BarChart, Bar, XAxis, YAxis, Tooltip, CartesianGrid, ReferenceLine, Cell,
} from "recharts";

const tooltipStyle = {
  contentStyle: { backgroundColor: "#181916", border: "1px solid #252620", borderRadius: 10 },
  labelStyle: { color: "#F0EEE8" },
};

export const ModelComparisonSection: React.FC = () => {
  const { analysis } = useData();
  const [animatedAcc, setAnimatedAcc] = useState(0);

  const bestModel = analysis?.classification.models[0];
  const bestAcc = bestModel?.accuracy || 0;

  useEffect(() => {
    if (!bestAcc) return;
    let start = 0;
    const target = bestAcc * 100;
    const duration = 800;
    const startTime = performance.now();
    const animate = (now: number) => {
      const elapsed = now - startTime;
      const progress = Math.min(elapsed / duration, 1);
      setAnimatedAcc(progress * target);
      if (progress < 1) requestAnimationFrame(animate);
    };
    requestAnimationFrame(animate);
  }, [bestAcc]);

  if (!analysis) return <p className="text-muted-foreground">Upload a CSV first.</p>;

  const models = analysis.classification.models;
  const chartData = models.map(m => ({ name: m.name, accuracy: m.accuracy }));

  // Circular progress
  const radius = 58;
  const circumference = 2 * Math.PI * radius;
  const strokeDash = (animatedAcc / 100) * circumference;

  return (
    <div className="space-y-4">
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
        {/* Leaderboard */}
        <div className="card-surface p-6">
          <h3 className="font-heading text-[15px] font-bold mb-0.5">Model Leaderboard</h3>
          <p className="label-mono mb-5">Ranked by classification accuracy</p>

          {/* Circular progress */}
          <div className="flex justify-center mb-6">
            <div className="relative">
              <svg width={140} height={140}>
                <circle cx={70} cy={70} r={radius} fill="none" stroke="hsl(53,6%,14%)" strokeWidth={6} />
                <circle
                  cx={70} cy={70} r={radius} fill="none" stroke="#E8571A" strokeWidth={6}
                  strokeDasharray={circumference}
                  strokeDashoffset={circumference - strokeDash}
                  strokeLinecap="round"
                  transform="rotate(-90 70 70)"
                  className="transition-all duration-200"
                />
              </svg>
              <div className="absolute inset-0 flex flex-col items-center justify-center">
                <span className="font-heading text-2xl font-bold text-foreground">
                  {animatedAcc.toFixed(1)}%
                </span>
                <span className="text-[10px] font-mono text-muted-foreground">Best Model</span>
              </div>
            </div>
          </div>

          <div className="space-y-4">
            {models.map((m, i) => (
              <div key={m.name} className="flex items-center gap-3">
                <span className="font-mono text-sm text-muted-foreground w-6">#{i + 1}</span>
                <div className="flex-1">
                  <div className="flex items-center gap-2 mb-1">
                    <span className="text-sm font-medium text-foreground">{m.name}</span>
                    {i === 0 && (
                      <span className="pill-badge bg-primary text-primary-foreground text-[9px] py-0.5">BEST</span>
                    )}
                  </div>
                  <div className="h-1.5 bg-muted rounded-full overflow-hidden">
                    <div
                      className="h-full rounded-full bg-primary transition-all duration-500"
                      style={{ width: `${m.accuracy * 100}%` }}
                    />
                  </div>
                </div>
                <span className="font-mono text-sm text-primary font-medium w-16 text-right">
                  {(m.accuracy * 100).toFixed(1)}%
                </span>
              </div>
            ))}
          </div>
        </div>

        {/* Bar chart */}
        <div className="card-surface p-6">
          <h3 className="font-heading text-[15px] font-bold mb-0.5">Accuracy Comparison</h3>
          <p className="label-mono mb-4">Classification accuracy scores</p>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={chartData}>
              <CartesianGrid strokeDasharray="3 3" stroke="hsl(53,6%,14%)" />
              <XAxis dataKey="name" tick={{ fontSize: 10, fill: "#7A7870" }} />
              <YAxis domain={[0, 1]} tick={{ fontSize: 10, fill: "#7A7870" }} />
              <Tooltip {...tooltipStyle} />
              <ReferenceLine y={0.5} stroke="#3E3D38" strokeDasharray="4 4" />
              <Bar dataKey="accuracy" radius={[6, 6, 0, 0]}>
                {chartData.map((_, i) => (
                  <Cell key={i} fill={i === 0 ? "#E8571A" : "#2A2D24"} />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
};
