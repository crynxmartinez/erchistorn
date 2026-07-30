import { useState } from "react";
import { ChevronDown } from "lucide-react";

export default function CollapsibleSection({ title, icon: Icon, defaultOpen = false, children }) {
    const [open, setOpen] = useState(defaultOpen);

    return (
        <div className="border-b border-border/50">
            <button
                onClick={() => setOpen((o) => !o)}
                className="w-full flex items-center justify-between py-2 px-1 hover:bg-primary/5 transition-colors"
            >
                <span className="flex items-center gap-2 font-pixel text-sm uppercase text-primary">
                    {Icon && <Icon size={14} />}
                    {title}
                </span>
                <ChevronDown
                    size={16}
                    className={`text-primary/60 transition-transform duration-200 ${open ? "rotate-180" : ""}`}
                />
            </button>
            <div
                className="overflow-hidden transition-all duration-200"
                style={{ maxHeight: open ? "9999px" : "0px" }}
            >
                <div className="py-2">
                    {children}
                </div>
            </div>
        </div>
    );
}
