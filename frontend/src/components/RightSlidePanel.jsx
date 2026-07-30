import { useEffect, useState } from "react";
import { ChevronLeft, ChevronRight } from "lucide-react";

export default function RightSlidePanel({ tabs }) {
    const [open, setOpen] = useState(false);
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

    return (
        <div
            className={`fixed top-20 right-0 z-40 h-[calc(100vh-5rem)] w-80 border-l border-y border-border bg-background shadow-xl transform transition-transform duration-300 ease-in-out ${
                open ? "translate-x-0" : "translate-x-[calc(100%-2.5rem)]"
            }`}
        >
            {/* Toggle handle */}
            <button
                onClick={() => setOpen((o) => !o)}
                className="absolute left-0 top-4 z-50 flex items-center justify-center w-10 h-12 border border-r-0 border-primary bg-background text-primary hover:text-foreground shadow-md"
                aria-label={open ? "Close side panel" : "Open side panel"}
            >
                {open ? <ChevronRight size={22} /> : <ChevronLeft size={22} />}
            </button>

            {/* Tab bar */}
            <div className="ml-10 flex border-b border-border">
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
            <div className="ml-10 h-[calc(100%-2.75rem)] overflow-y-auto p-4">
                {activeTab?.content}
            </div>
        </div>
    );
}
