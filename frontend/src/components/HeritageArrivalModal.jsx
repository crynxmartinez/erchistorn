import { useState } from "react";
import { api } from "@/lib/api";
import { Crown, Coins, Swords, ShoppingBag, ScrollText, X } from "lucide-react";

const CONTINENT_NAMES = {
    valeria: "Valeria", mushkara: "Mushkara", concordia: "Concordia",
    khardrum: "Khardrum", haya: "Haya", gennel: "Gennel",
    hylion: "Hylion", daw_ul_talalu: "Daw'ul Talalu",
};

export default function HeritageArrivalModal({ character, continent, heritageData, onClose, onCharacterUpdate }) {
    const [dontShow, setDontShow] = useState(false);
    if (!heritageData) return null;

    const name = heritageData.name || "Heritage Festival";
    const desc = heritageData.desc || "";
    const bonuses = heritageData.bonuses || {};
    const continentName = CONTINENT_NAMES[continent] || continent;
    const year = new Date().getFullYear();

    const handleClose = async () => {
        if (dontShow) {
            try {
                await api.post("/game/heritage/dismiss", { continent, year });
                onCharacterUpdate?.({
                    ...character,
                    heritage_dismissed: [...(character?.heritage_dismissed || []), `${continent}_${year}`],
                });
            } catch (e) {}
        }
        onClose();
    };

    return (
        <div className="fixed inset-0 z-[60] flex items-center justify-center bg-black/70" data-testid="heritage-arrival-modal">
            <div className="relative w-full max-w-2xl mx-4 border-2 border-primary bg-background shadow-2xl">
                {/* Close button */}
                <button
                    onClick={handleClose}
                    className="absolute top-2 right-2 z-10 p-1 text-muted-foreground hover:text-foreground"
                    aria-label="Close"
                >
                    <X size={20} />
                </button>

                {/* Header banner */}
                <div className="bg-primary/10 border-b border-primary/30 p-6 text-center">
                    <Crown size={40} className="mx-auto text-primary mb-2" />
                    <h2 className="font-pixel text-2xl uppercase text-primary">{name}</h2>
                    <p className="stat-label text-primary/70 mt-1">{continentName} Heritage Month</p>
                </div>

                {/* Body */}
                <div className="p-6 space-y-4 max-h-[60vh] overflow-y-auto">
                    <p className="text-base text-foreground/90 italic leading-relaxed">{desc}</p>

                    {/* Bonuses */}
                    {bonuses.desc && (
                        <div className="border border-border p-4 bg-primary/5">
                            <h3 className="font-pixel text-sm uppercase text-primary mb-2 flex items-center gap-1">
                                <Coins size={16} /> Active Bonuses
                            </h3>
                            <p className="text-sm text-foreground/80">{bonuses.desc}</p>
                            <div className="mt-3 grid grid-cols-2 gap-1">
                                {bonuses.gather_yield_mult > 1.0 && (
                                    <div className="stat-label text-primary">+{Math.round((bonuses.gather_yield_mult - 1) * 100)}% Gather Yield</div>
                                )}
                                {bonuses.combat_xp_mult > 1.0 && (
                                    <div className="stat-label text-primary">+{Math.round((bonuses.combat_xp_mult - 1) * 100)}% Combat XP</div>
                                )}
                                {bonuses.craft_success_bonus > 0 && (
                                    <div className="stat-label text-primary">+{Math.round(bonuses.craft_success_bonus * 100)}% Craft Success</div>
                                )}
                                {bonuses.market_discount > 0 && (
                                    <div className="stat-label text-primary">{Math.round(bonuses.market_discount * 100)}% Market Discount</div>
                                )}
                                {bonuses.free_travel && (
                                    <div className="stat-label text-primary">Free Travel to/from {continentName}</div>
                                )}
                            </div>
                        </div>
                    )}

                    {/* Events summary */}
                    <div className="border border-border p-4 space-y-2">
                        <h3 className="font-pixel text-sm uppercase text-primary flex items-center gap-1">
                            <ScrollText size={16} /> Festival Events
                        </h3>
                        <div className="flex items-start gap-2">
                            <Swords size={12} className="text-primary flex-shrink-0 mt-0.5" />
                            <div className="text-xs text-foreground/80">Heritage Boss available — challenge for tokens</div>
                        </div>
                        <div className="flex items-start gap-2">
                            <ScrollText size={12} className="text-primary flex-shrink-0 mt-0.5" />
                            <div className="text-xs text-foreground/80">3 Daily Heritage Quests — earn bonus tokens</div>
                        </div>
                        <div className="flex items-start gap-2">
                            <ShoppingBag size={12} className="text-primary flex-shrink-0 mt-0.5" />
                            <div className="text-xs text-foreground/80">Heritage Vendor — spend tokens on exclusive items</div>
                        </div>
                        <div className="flex items-start gap-2">
                            <Crown size={12} className="text-primary flex-shrink-0 mt-0.5" />
                            <div className="text-xs text-foreground/80">Ladder ranking — compete for top spots</div>
                        </div>
                    </div>

                    {/* Don't show again */}
                    <label className="flex items-center gap-2 cursor-pointer select-none">
                        <input
                            type="checkbox"
                            checked={dontShow}
                            onChange={(e) => setDontShow(e.target.checked)}
                            className="w-4 h-4 accent-primary"
                        />
                        <span className="stat-label text-muted-foreground">Don't show this again for {continentName} {year}</span>
                    </label>
                </div>

                {/* Footer */}
                <div className="border-t border-border p-4">
                    <button
                        onClick={handleClose}
                        className="press-btn w-full font-pixel text-base uppercase py-3 border-2 border-primary text-primary hover:bg-primary hover:text-primary-foreground"
                    >
                        Explore the Festival
                    </button>
                </div>
            </div>
        </div>
    );
}
