import React from "react";
import { Crown, Keyboard, Star, Menu, Bookmark } from "lucide-react";
import { useData } from "@/context/DataContext";

interface HeaderProps {
  title: string;
}

export const AppHeader: React.FC<HeaderProps> = ({ title }) => {
  const { fileName } = useData();

  return (
    <header className="sticky top-0 z-30 flex h-14 items-center justify-between border-b border-border bg-background px-6">
      <h1 className="font-heading text-lg font-bold text-foreground">{title}</h1>

      <div className="flex items-center gap-3">
        {fileName && (
          <div className="flex items-center gap-1.5 text-xs font-mono text-muted-foreground">
            <span className="h-2 w-2 rounded-full bg-success" />
            {fileName}
          </div>
        )}

        <div className="pill-badge border border-border text-muted-foreground flex items-center gap-1.5">
          <Crown className="h-3 w-3" />
          <span>Pro member</span>
        </div>

        <div className="pill-badge border border-border text-muted-foreground flex items-center gap-1.5">
          <Keyboard className="h-3 w-3" />
          <span>Shortcuts</span>
        </div>

        <button className="p-1.5 text-muted-foreground hover:text-foreground transition-colors">
          <Bookmark className="h-4 w-4" />
        </button>

        {/* Avatar cluster */}
        <div className="flex -space-x-2">
          <div className="flex h-7 w-7 items-center justify-center rounded-full bg-primary text-[10px] font-mono text-primary-foreground border-2 border-background">
            CM
          </div>
          <div className="flex h-7 w-7 items-center justify-center rounded-full bg-muted text-[10px] font-mono text-muted-foreground border-2 border-background">
            SO
          </div>
        </div>

        <button className="pill-badge border border-border text-muted-foreground text-[11px]">
          Invited +
        </button>

        <button className="p-1.5 text-muted-foreground hover:text-foreground transition-colors">
          <Menu className="h-4 w-4" />
        </button>
      </div>
    </header>
  );
};
