import { Tent, Coins, Star, Sparkles, MapPin, X, ScrollText } from "lucide-react";

const RANK_LABEL = {
    novice: "Novice",
    skilled: "Skilled",
    veteran: "Veteran",
    elite: "Elite",
};

const SPECIALTY_META = {
    hunting: { label: "Hunter", color: "text-red-400", icon: "🗡" },
    gathering: { label: "Gatherer", color: "text-green-400", icon: "🌿" },
    fishing: { label: "Fisher", color: "text-blue-400", icon: "🎣" },
};

const QUIRK_META = {
    lucky: { label: "Lucky", desc: "+10% rare drop chance" },
    greedy: { label: "Greedy", desc: "+50% cost, +20% yield" },
    night_owl: { label: "Night Owl", desc: "+30% yield on 4+ hr trips" },
    scout: { label: "Scout", desc: "+5% biome exploration per trip" },
};

export default function ExpeditionCollectModal({ result, onClose }) {
    if (!result) return null;

    const mercName = result.merc_name || "The mercenary";
    const mercDesc = result.merc_desc || "";
    const specialty = SPECIALTY_META[result.merc_specialty] || SPECIALTY_META.gathering;
    const quirk = QUIRK_META[result.merc_quirk];
    const rank = RANK_LABEL[result.merc_rank] || "";
    const loot = result.loot || [];
    const rareFound = result.rare_found;
    const xpGain = result.xp_gain || 0;
    const explorationGain = result.exploration_gain || 0;
    const loyaltyHires = result.loyalty_hires || 0;
    const narrative = result.narrative || "";

    return (
        <div
            className="fixed inset-0 z-[70] flex items-center justify-center bg-black/70 p-4"
            data-testid="expedition-collect-modal"
            onClick={onClose}
        >
            <div
                className="relative w-full max-w-lg border-2 border-primary bg-background shadow-2xl"
                onClick={(e) => e.stopPropagation()}
            >
                {/* Close button */}
                <button
                    onClick={onClose}
                    className="absolute right-0 top-0 z-10 flex items-center justify-center w-10 h-10 border border-l-0 border-b-0 border-primary bg-background text-primary hover:text-foreground"
                    aria-label="Close"
                >
                    <X size={18} />
                </button>

                {/* Header */}
                <div className="bg-primary/10 border-b border-primary/30 p-5 flex items-center gap-3">
                    <div className="w-14 h-14 rounded-full bg-primary/20 flex items-center justify-center shrink-0">
                        <Tent size={24} className="text-primary" />
                    </div>
                    <div className="flex-1 min-w-0">
                        <h2 className="font-pixel text-xl uppercase text-primary truncate">{mercName}</h2>
                        <div className="stat-label text-primary/70 text-[10px] mt-0.5">
                            {rank} <span className={specialty.color}>{specialty.label}</span>
                            {quirk && (
                                <span className="ml-1 text-amber-500">· {quirk.label}</span>
                            )}
                        </div>
                    </div>
                </div>

                {/* Body */}
                <div className="p-5 space-y-4 max-h-[calc(100vh-12rem)] overflow-y-auto">
                    {/* Narrative */}
                    {narrative && (
                        <div className="border-l-2 border-primary/40 pl-3 py-1">
                            <div className="flex items-center gap-1.5 mb-1">
                                <ScrollText size={12} className="text-primary/60" />
                                <span className="stat-label text-primary/60 text-[10px] uppercase">The Report</span>
                            </div>
                            <p className="text-sm text-foreground/90 italic leading-relaxed">
                                {narrative}
                            </p>
                        </div>
                    )}

                    {/* Merc description */}
                    {mercDesc && (
                        <p className="text-xs text-muted-foreground italic">{mercDesc}</p>
                    )}

                    {/* Loot */}
                    <div>
                        <div className="stat-label text-primary mb-2 flex items-center gap-1.5">
                            <Sparkles size={12} /> HAUL
                        </div>
                        {loot.length > 0 ? (
                            <div className="grid grid-cols-2 gap-2">
                                {loot.map((l) => (
                                    <div
                                        key={l.item_id}
                                        className={`flex items-center justify-between border p-2 ${
                                            rareFound && l.item_id === rareFound
                                                ? "border-amber-500/60 bg-amber-500/10"
                                                : "border-border bg-card/40"
                                        }`}
                                    >
                                        <span className="text-xs uppercase truncate">
                                            {l.item_id.replace(/_/g, " ")}
                                            {rareFound && l.item_id === rareFound && (
                                                <span className="ml-1 text-amber-500">★</span>
                                            )}
                                        </span>
                                        <span className="font-pixel text-sm text-primary ml-2">×{l.quantity}</span>
                                    </div>
                                ))}
                            </div>
                        ) : (
                            <div className="text-xs text-muted-foreground italic">No items recovered.</div>
                        )}
                    </div>

                    {/* Rewards summary */}
                    {(xpGain > 0 || explorationGain > 0 || loyaltyHires > 0) && (
                        <div className="flex flex-wrap gap-3 pt-2 border-t border-border/50">
                            {xpGain > 0 && (
                                <div className="flex items-center gap-1.5 text-xs">
                                    <Star size={12} className="text-amber-500" />
                                    <span className="text-amber-500 font-pixel">+{xpGain} XP</span>
                                </div>
                            )}
                            {explorationGain > 0 && (
                                <div className="flex items-center gap-1.5 text-xs">
                                    <MapPin size={12} className="text-green-500" />
                                    <span className="text-green-500 font-pixel">+{explorationGain}% Exploration</span>
                                </div>
                            )}
                            {loyaltyHires > 0 && (
                                <div className="flex items-center gap-1.5 text-xs">
                                    <Coins size={12} className="text-primary" />
                                    <span className="text-primary font-pixel">{loyaltyHires} total hires</span>
                                </div>
                            )}
                        </div>
                    )}
                </div>

                {/* Footer */}
                <div className="border-t border-border p-4 flex justify-end">
                    <button
                        onClick={onClose}
                        data-testid="expedition-collect-close"
                        className="press-btn font-pixel text-xs uppercase px-5 py-2 border-2 border-primary text-primary hover:bg-primary hover:text-primary-foreground"
                    >
                        Done
                    </button>
                </div>
            </div>
        </div>
    );
}
