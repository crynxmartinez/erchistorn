import { useEffect, useState } from "react";
import { ChevronLeft, ChevronRight } from "lucide-react";

export default function SlidePanel({ tabs, side = "right", defaultOpen = false, open: controlledOpen, onOpenChange }) {
    const [internalOpen, setInternalOpen] = useState(defaultOpen);
    const open = controlledOpen !== undefined ? controlledOpen : internalOpen;
    const setOpen = (val) => {
        if (onOpenChange) onOpenChange(val);
        else setInternalOpen(val);
    };
    const [active, setActive] = useState(tabs[0]?.id ?? null);

    const activeTab = tabs.find((t) => t.id === active) || tabs[0];

    useEffect(() => {
        const onKey = (e) => {
            if (e.key === "Escape") setOpen(false);
        };
        document.addEventListener("keydown", onKey);
        return () => document.removeEventListener("keydown", onKey);
    }, []);

    const handleTab = (id) => {
        setActive(id);
        if (!open) setOpen(true);
    };

    const isLeft = side === "left";

    const panelClass = isLeft
        ? `fixed top-20 left-0 z-40 h-[calc(100vh-5rem)] w-80 border-r border-y border-border bg-background shadow-xl transform transition-transform duration-300 ease-in-out ${
              open ? "translate-x-0" : "-translate-x-[calc(100%-2.5rem)]"
          }`
        : `fixed top-20 right-0 z-40 h-[calc(100vh-5rem)] w-80 border-l border-y border-border bg-background shadow-xl transform transition-transform duration-300 ease-in-out ${
              open ? "translate-x-0" : "translate-x-[calc(100%-2.5rem)]"
          }`;

    const handleClass = isLeft
        ? "absolute right-0 top-4 z-50 flex items-center justify-center w-10 h-12 border border-l-0 border-primary bg-background text-primary hover:text-foreground shadow-md"
        : "absolute left-0 top-4 z-50 flex items-center justify-center w-10 h-12 border border-r-0 border-primary bg-background text-primary hover:text-foreground shadow-md";

    const contentMargin = isLeft ? "mr-10" : "ml-10";

    return (
        <div className={panelClass}>
            {/* Toggle handle */}
            <button
                onClick={() => setOpen((o) => !o)}
                className={handleClass}
                aria-label={open ? "Close side panel" : "Open side panel"}
            >
                {isLeft
                    ? open ? <ChevronLeft size={22} /> : <ChevronRight size={22} />
                    : open ? <ChevronRight size={22} /> : <ChevronLeft size={22} />}
            </button>

            {/* Tab bar */}
            <div className={`${contentMargin} flex border-b border-border`}>
                {tabs.map((t) => {
                    const Icon = t.icon;
                    const isActive = active === t.id;
                    return (
                        <button
                            key={t.id}
                            onClick={() => handleTab(t.id)}
                            className={`flex-1 flex items-center justify-center gap-1 p-2 font-pixel text-xs uppercase border-r border-border last:border-r-0 transition-colors ${
                                isActive
                                    ? "text-primary bg-primary/10"
                                    : "text-muted-foreground hover:text-foreground"
                            }`}
                        >
                            <Icon size={14} /> {t.label}
                        </button>
                    );
                })}
            </div>

            {/* Panel content */}
            <div
                className={`${contentMargin} h-[calc(100%-2.75rem)] overflow-y-auto p-4 ${isLeft ? "scrollbar-left" : ""}`}
            >
                {activeTab?.content}
            </div>
        </div>
    );
}
