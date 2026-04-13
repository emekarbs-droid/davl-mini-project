import React, { createContext, useContext, useState, useCallback } from "react";
import Papa from "papaparse";
import { analyzeCSV } from "@/lib/api";
import type { AnalysisResults } from "@/lib/types";


export type DataRow = Record<string, string | number>;

interface DataState {
  fileName: string | null;
  data: DataRow[];
  columns: string[];
  numericColumns: string[];
  analysis: AnalysisResults | null;
  isLoading: boolean;
  loadingStep: string;
  error: string | null;
}

interface DataContextType extends DataState {
  uploadCSV: (file: File) => void;
}

const DataContext = createContext<DataContextType | null>(null);

export const useData = () => {
  const ctx = useContext(DataContext);
  if (!ctx) throw new Error("useData must be used within DataProvider");
  return ctx;
};

const STEPS = [
  "Parsing CSV",
  "Standardizing features",
  "Running PCA",
  "Running LDA",
  "Factor Analysis",
  "Training models",
  "Generating insights",
];

export const DataProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [state, setState] = useState<DataState>({
    fileName: null,
    data: [],
    columns: [],
    numericColumns: [],
    analysis: null,
    isLoading: false,
    loadingStep: "",
    error: null,
  });

  const uploadCSV = useCallback((file: File) => {
  if (file.size > 10 * 1024 * 1024) {
    console.warn("File is larger than 10MB — processing may be slow.");
  }

  setState(s => ({ ...s, isLoading: true, loadingStep: STEPS[0], error: null }));

  // Parse just for column preview and validation
  Papa.parse(file, {
    header: true,
    dynamicTyping: true,
    skipEmptyLines: true,
    preview: 20, // only parse first 20 rows for preview
    complete: async (results) => {
      const data = results.data as DataRow[];
      const columns = results.meta.fields || [];

      const numericColumns = columns.filter(col =>
        data.some(row => typeof row[col] === "number" && !isNaN(row[col] as number))
      );

      if (numericColumns.length < 2) {
        setState(s => ({
          ...s,
          isLoading: false,
          error: "CSV must have at least 2 numeric columns for analysis.",
        }));
        return;
      }


        setState(s => ({ ...s, data, columns, numericColumns, fileName: file.name }));
        // Run pipeline with progress updates
try {
  let stepIdx = 1;
  const updateStep = () => {
    if (stepIdx < STEPS.length) {
      setState(s => ({ ...s, loadingStep: STEPS[stepIdx] }));
      stepIdx++;
    }
  };
  const interval = setInterval(updateStep, 600);

  const analysis = await analyzeCSV(file); // send raw file to Python

  clearInterval(interval);
  setState(s => ({
    ...s,
    analysis,
    isLoading: false,
    loadingStep: "",
  }));
} catch (e: any) {
  setState(s => ({
    ...s,
    isLoading: false,
    error: `Analysis failed: ${e.message}`,
  }));
}
      },
      error: (err) => {
        setState(s => ({ ...s, isLoading: false, error: `Parse error: ${err.message}` }));
      },
    });
  }, []);

  return (
    <DataContext.Provider value={{ ...state, uploadCSV }}>
      {children}
    </DataContext.Provider>
  );
};
