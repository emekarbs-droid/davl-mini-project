import React, { useState, useCallback } from "react";
import {
  Home, BarChart2, GitBranch, Trophy, Table, Lightbulb,
  Search, Upload
} from "lucide-react";
import { useData } from "@/context/DataContext";

const navItems = [
  { id: "dashboard", label: "Dashboard", icon: Home },
  { id: "visualize", label: "Visualize", icon: BarChart2 },
  { id: "ml-pipeline", label: "ML Pipeline", icon: GitBranch },
  { id: "model-comparison", label: "Model Comparison", icon: Trophy },
  { id: "data-explorer", label: "Data Explorer", icon: Table },
  { id: "insights", label: "Insights", icon: Lightbulb },
];

interface SidebarProps {
  activeSection: string;
  onNavigate: (id: string) => void;
}

export const AppSidebar: React.FC<SidebarProps> = ({ activeSection, onNavigate }) => {
  const [collapsed, setCollapsed] = useState(false);
  const { uploadCSV, fileName } = useData();

  const handleFileChange = useCallback(
    (e: React.ChangeEvent<HTMLInputElement>) => {
      const file = e.target.files?.[0];
      if (file) uploadCSV(file);
    },
    [uploadCSV]
  );

  return (
    <>
      <aside
        className={`fixed left-0 top-0 bottom-0 z-40 flex flex-col border-r border-border bg-background transition-all duration-200
          ${collapsed ? "w-[60px]" : "w-[220px]"}
        `}
      >
        {/* Logo */}
        <div className="flex items-center gap-2.5 px-4 py-5">
          <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-md bg-primary text-background font-heading text-sm font-bold">
            ◈
          </div>
          {!collapsed && (
            <span className="font-heading text-[15px] font-bold text-foreground tracking-tight">
              DAVL Studio
            </span>
          )}
        </div>

        {/* Upload CSV button */}
        <div className="px-3 pb-2">
          <label
            className={`flex items-center gap-2 cursor-pointer rounded-md bg-primary/10 border border-primary/30 px-3 py-2 hover:bg-primary/20 transition-colors ${collapsed ? "justify-center" : ""}`}
          >
            <Upload className="h-4 w-4 text-primary shrink-0" />
            {!collapsed && (
              <span className="text-xs font-medium text-primary truncate">
                {fileName || "Upload CSV"}
              </span>
            )}
            <input type="file" accept=".csv" onChange={handleFileChange} className="hidden" />
          </label>
        </div>

        {/* Search */}
        {!collapsed && (
          <div className="px-3 pb-3">
            <div className="flex items-center gap-2 rounded-md border border-border bg-accent/50 px-3 py-2">
              <Search className="h-3.5 w-3.5 text-muted-foreground" />
              <span className="text-xs text-muted-foreground">Search</span>
            </div>
          </div>
        )}

        {/* Nav items */}
        <nav className="flex-1 px-2 space-y-1">
          {navItems.map(item => {
            const active = activeSection === item.id;
            return (
              <button
                key={item.id}
                onClick={() => onNavigate(item.id)}
                className={`nav-item w-full ${active ? "nav-item-active" : "nav-item-inactive"}`}
              >
                <item.icon className="h-4 w-4 shrink-0" />
                {!collapsed && <span>{item.label}</span>}
              </button>
            );
          })}
        </nav>

        {/* Version */}
        {!collapsed && (
          <div className="px-4 py-3 text-[10px] font-mono text-muted-foreground/50">
            Hackathon 2025
          </div>
        )}
      </aside>

      {/* Spacer */}
      <div className={`shrink-0 ${collapsed ? "w-[60px]" : "w-[220px]"} transition-all duration-200`} />
    </>
  );
};
