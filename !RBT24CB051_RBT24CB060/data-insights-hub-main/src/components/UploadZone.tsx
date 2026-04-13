import React, { useCallback } from "react";
import { Upload } from "lucide-react";
import { useData } from "@/context/DataContext";

export const UploadZone: React.FC = () => {
  const { uploadCSV } = useData();

  const handleDrop = useCallback(
    (e: React.DragEvent) => {
      e.preventDefault();
      const file = e.dataTransfer.files[0];
      if (file?.name.endsWith(".csv")) uploadCSV(file);
    },
    [uploadCSV]
  );

  const handleChange = useCallback(
    (e: React.ChangeEvent<HTMLInputElement>) => {
      const file = e.target.files?.[0];
      if (file) uploadCSV(file);
    },
    [uploadCSV]
  );

  return (
    <div className="flex items-center justify-center min-h-[60vh]">
      <div
        onDrop={handleDrop}
        onDragOver={e => e.preventDefault()}
        className="card-surface border-2 border-dashed border-primary/30 p-12 text-center max-w-md w-full"
      >
        <div className="mx-auto mb-4 flex h-14 w-14 items-center justify-center rounded-lg bg-primary/10">
          <span className="text-2xl text-primary font-heading">◈</span>
        </div>
        <h2 className="font-heading text-xl font-bold text-foreground mb-2">
          Drop your CSV to begin
        </h2>
        <p className="text-sm text-muted-foreground mb-6">
          Upload a CSV file and DAVL Studio will automatically run statistical analysis and ML pipelines.
        </p>
        <label className="inline-flex items-center gap-2 cursor-pointer rounded-pill bg-primary px-6 py-2.5 text-sm font-medium text-primary-foreground hover:bg-secondary transition-colors">
          <Upload className="h-4 w-4" />
          Upload CSV
          <input type="file" accept=".csv" onChange={handleChange} className="hidden" />
        </label>
      </div>
    </div>
  );
};
