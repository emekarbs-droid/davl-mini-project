import React, { useState } from "react";
import { DataProvider, useData } from "@/context/DataContext";
import { AppSidebar } from "@/components/AppSidebar";
import { LoadingOverlay } from "@/components/LoadingOverlay";
import { DashboardSection } from "@/components/sections/DashboardSection";
import { VisualizeSection } from "@/components/sections/VisualizeSection";
import { MLPipelineSection } from "@/components/sections/MLPipelineSection";
import { ModelComparisonSection } from "@/components/sections/ModelComparisonSection";
import { DataExplorerSection } from "@/components/sections/DataExplorerSection";
import { InsightsSection } from "@/components/sections/InsightsSection";

const DashboardContent: React.FC = () => {
  const [activeSection, setActiveSection] = useState("dashboard");
  const { isLoading, loadingStep, error } = useData();

  return (
    <div className="flex min-h-screen w-full bg-background">
      {isLoading && <LoadingOverlay step={loadingStep} />}
      <AppSidebar activeSection={activeSection} onNavigate={setActiveSection} />
      <div className="flex-1 flex flex-col min-w-0">
        <main className="flex-1 p-7 overflow-auto">
          {error && (
            <div className="card-surface border-destructive border p-5 mb-4">
              <p className="text-destructive font-mono text-sm">{error}</p>
            </div>
          )}
          {activeSection === "dashboard" && <DashboardSection />}
          {activeSection === "visualize" && <VisualizeSection />}
          {activeSection === "ml-pipeline" && <MLPipelineSection />}
          {activeSection === "model-comparison" && <ModelComparisonSection />}
          {activeSection === "data-explorer" && <DataExplorerSection />}
          {activeSection === "insights" && <InsightsSection />}
        </main>
      </div>
    </div>
  );
};

const Index: React.FC = () => (
  <DataProvider>
    <DashboardContent />
  </DataProvider>
);

export default Index;
