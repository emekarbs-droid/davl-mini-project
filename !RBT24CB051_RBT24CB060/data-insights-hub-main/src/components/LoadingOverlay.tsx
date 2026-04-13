import React from "react";
import { Loader2 } from "lucide-react";

export const LoadingOverlay: React.FC<{ step: string }> = ({ step }) => (
  <div className="fixed inset-0 z-50 flex items-center justify-center bg-background/80 backdrop-blur-sm">
    <div className="card-surface p-8 text-center max-w-sm">
      <Loader2 className="h-8 w-8 animate-spin text-primary mx-auto mb-4" />
      <p className="font-heading text-lg font-bold text-foreground mb-1">Processing…</p>
      <p className="text-sm font-mono text-primary">{step}</p>
    </div>
  </div>
);
