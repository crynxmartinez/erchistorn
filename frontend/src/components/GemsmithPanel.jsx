import { useState, useMemo } from "react";
import { api, extractError } from "@/lib/api";
import { useGameData, RARITY_TEXT, RARITY_CLASS } from "@/data/gameData";
import { toast } from "sonner";
import { Search, X, Sparkles, ChevronDown, ChevronUp, Gem } from "lucide-react";

const MAX_GEM_SLOTS = 10;

const GEMSMITH_NPC = {
    name: "Aelira Sunstone",
    title: "Master Gemsmith",
    desc: "A serene elf whose eyes shimmer with the facets of a thousand cut stones. She reads gems the way scholars read scrolls — and polishes them into power.",
    greeting: "Bring me your blade, your amulet, your ring — I will set it aglow with the light of cut gems. Every gem you've collected finds its brilliance here.",
};

export default function GemsmithPanel({ character, onCharacterUpdate }) {
    const gd = useGameData();
    const [selectedItem, setSelectedItem] = useState(null);
    const [showItemPicker, setShowItemPicker] = useState(false);
    const [itemSearch, setItemSearch] = useState("");
    const [gemSlots, setGemSlots] = useState(Array(MAX_GEM_SLOTS).fill(null));
    const [activeSlot, setActiveSlot] = useState(null);
    const [gemSearch, setGemSearch] = useState("");
    const [busy, setBusy] = useState(false);

    const itemInstances = character?.item_instances || [];
    const inventory = character?.inventory || [];

    const gemsById = gd.gemsById || {};

    const gemsInInventory = useMemo(() => {
        return inventory
            .filter((inv) => {
                const def = gemsById[inv.item_id];
                return def && inv.quantity > 0;
            })
            .map((inv) => ({
                ...gemsById[inv.item_id],
                quantity: inv.quantity,
                item_id: inv.item_id,
            }));
    }, [inventory, gemsById]);

    const upgradableItems = useMemo(() => {
        return itemInstances.filter((inst) => {
            if (!inst.instance_id) return false;
            const kind = inst.kind;
            if (!["weapon", "armor", "trinket", "relic"].includes(kind)) return false;
            const count = inst.upgrades?.count ?? 0;
            const max = inst.upgrades?.max ?? MAX_GEM_SLOTS;
            return count < max;
        });
    }, [itemInstances]);

    const filteredItems = useMemo(() => {
        if (!itemSearch) return upgradableItems;
        const q = itemSearch.toLowerCase();
        return upgradableItems.filter((it) =>
            (it.name || "").toLowerCase().includes(q)
        );
    }, [upgradableItems, itemSearch]);

    const filteredGems = useMemo(() => {
        if (!gemSearch) return gemsInInventory;
        const q = gemSearch.toLowerCase();
        return gemsInInventory.filter((g) =>
            (g.name || "").toLowerCase().includes(q) ||
            (g.stat || "").toLowerCase().includes(q)
        );
    }, [gemsInInventory, gemSearch]);

    const currentItemUpgradeCount = selectedItem?.upgrades?.count ?? 0;
    const currentItemMax = selectedItem?.upgrades?.max ?? MAX_GEM_SLOTS;
    const remainingSlots = currentItemMax - currentItemUpgradeCount;
    const selectedGems = gemSlots.filter((g) => g !== null);
    const canForge = selectedItem && selectedGems.length > 0 && selectedGems.length <= remainingSlots && !busy;

    const handleSelectItem = (item) => {
        setSelectedItem(item);
        setShowItemPicker(false);
        setItemSearch("");
        setGemSlots(Array(MAX_GEM_SLOTS).fill(null));
    };

    const handleSelectGem = (gem) => {
        if (activeSlot === null) return;
        const newSlots = [...gemSlots];
        newSlots[activeSlot] = gem;
        setGemSlots(newSlots);
        setActiveSlot(null);
        setGemSearch("");
    };

    const handleRemoveGem = (slotIdx) => {
        const newSlots = [...gemSlots];
        newSlots[slotIdx] = null;
        setGemSlots(newSlots);
    };

    const handleForge = async () => {
        if (!selectedItem || selectedGems.length === 0) return;
        setBusy(true);
        try {
            const gemIds = selectedGems.map((g) => g.id);
            const { data } = await api.post("/game/item/gemsmith", {
                instance_id: selectedItem.instance_id,
                gem_ids: gemIds,
            });
            onCharacterUpdate?.(data.character);
            const socketed = data.socketed?.length || 0;
            const failed = data.failed?.length || 0;
            if (socketed > 0) {
                toast.success(`Gemsmith: Socketed ${socketed} gem(s) into ${selectedItem.name}!`);
            }
            if (failed > 0) {
                toast.warning(`${failed} gem(s) could not be socketed.`);
            }
            setSelectedItem(data.item);
            setGemSlots(Array(MAX_GEM_SLOTS).fill(null));
        } catch (e) {
            toast.error(extractError(e));
        } finally {
            setBusy(false);
        }
    };

    return (
        <div className="space-y-4" data-testid="gemsmith-panel">
            {/* NPC header */}
            <div className="panel p-6">
                <div className="stat-label text-primary/70">GEMSMITH</div>
                <h2 className="font-pixel text-3xl uppercase text-primary">{GEMSMITH_NPC.name}</h2>
                <div className="stat-label text-primary/80">{GEMSMITH_NPC.title}</div>
                <p className="narr text-muted-foreground mt-2">{GEMSMITH_NPC.desc}</p>
                <div className="border-t border-border mt-3 pt-3">
                    <p className="narr text-sm text-foreground/85 italic">&ldquo;{GEMSMITH_NPC.greeting}&rdquo;</p>
                </div>
            </div>

            {/* Two-box layout */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {/* Left: Item selection */}
                <div className="panel p-4">
                    <div className="stat-label text-primary/70 mb-2">SELECT ITEM TO UPGRADE</div>

                    {/* Item box */}
                    <div className="relative">
                        <button
                            data-testid="gemsmith-item-select"
                            onClick={() => setShowItemPicker(!showItemPicker)}
                            className="w-full border-2 border-border p-3 hover:border-primary text-left min-h-[80px] flex items-center justify-between"
                        >
                            {selectedItem ? (
                                <div className="flex items-center gap-3">
                                    <div>
                                        <div className={`font-pixel text-sm uppercase ${RARITY_TEXT[selectedItem.rarity] || ""}`}>
                                            {selectedItem.name}
                                        </div>
                                        <div className="stat-label text-muted-foreground">
                                            {selectedItem.kind} · {selectedItem.slot || ""}
                                        </div>
                                        <div className="stat-label text-primary/70">
                                            Upgrades: {currentItemUpgradeCount}/{currentItemMax}
                                        </div>
                                    </div>
                                </div>
                            ) : (
                                <div className="stat-label text-muted-foreground">Click to choose an item...</div>
                            )}
                            {showItemPicker ? <ChevronUp size={16} /> : <ChevronDown size={16} />}
                        </button>

                        {/* Item dropdown with search */}
                        {showItemPicker && (
                            <div className="absolute z-10 mt-1 w-full bg-background border-2 border-primary shadow-lg max-h-[300px] overflow-y-auto">
                                <div className="sticky top-0 bg-background border-b border-border p-2">
                                    <div className="flex items-center gap-2">
                                        <Search size={12} className="text-muted-foreground" />
                                        <input
                                            type="text"
                                            value={itemSearch}
                                            onChange={(e) => setItemSearch(e.target.value)}
                                            placeholder="Search items..."
                                            className="bg-transparent border-none outline-none text-sm w-full"
                                            autoFocus
                                        />
                                    </div>
                                </div>
                                {filteredItems.length === 0 ? (
                                    <div className="stat-label text-muted-foreground p-3">No upgradable items found.</div>
                                ) : (
                                    filteredItems.map((it) => (
                                        <button
                                            key={it.instance_id}
                                            data-testid={`gemsmith-item-${it.instance_id}`}
                                            onClick={() => handleSelectItem(it)}
                                            className="block w-full text-left p-2 hover:bg-primary/10 border-b border-border/50"
                                        >
                                            <div className={`font-pixel text-xs uppercase ${RARITY_TEXT[it.rarity] || ""}`}>
                                                {it.name}
                                            </div>
                                            <div className="stat-label text-muted-foreground">
                                                {it.kind} · {it.slot || ""} · Upgrades: {it.upgrades?.count || 0}/{it.upgrades?.max || MAX_GEM_SLOTS}
                                            </div>
                                        </button>
                                    ))
                                )}
                            </div>
                        )}
                    </div>

                    {/* Current upgrade summary */}
                    {selectedItem && (
                        <div className="mt-3 border border-border p-3">
                            <div className="stat-label text-primary/70 mb-1">CURRENT UPGRADES</div>
                            {(selectedItem.upgrades?.gems || []).length > 0 ? (
                                <div className="space-y-1">
                                    {(selectedItem.upgrades.gems).map((g, i) => (
                                        <div key={i} className="stat-label text-foreground/80">
                                            <span className="text-rarity-rare">●</span> {g.stat} (+{g.value})
                                        </div>
                                    ))}
                                </div>
                            ) : (
                                <div className="stat-label text-muted-foreground italic">No gems socketed yet.</div>
                            )}
                            {(selectedItem.upgrades?.runes || []).length > 0 && (
                                <div className="mt-2 pt-2 border-t border-border">
                                    <div className="stat-label text-primary/70 mb-1">RUNES</div>
                                    {(selectedItem.upgrades.runes).map((r, i) => (
                                        <div key={i} className="stat-label text-foreground/80">
                                            <span className="text-rarity-epic">●</span> {r.type} (+{(r.value * 100).toFixed(1)}%)
                                        </div>
                                    ))}
                                </div>
                            )}
                        </div>
                    )}
                </div>

                {/* Right: Gem slots */}
                <div className="panel p-4">
                    <div className="stat-label text-primary/70 mb-2">
                        GEM SLOTS ({selectedGems.length}/{remainingSlots} available)
                    </div>

                    {/* 10 gem slot boxes */}
                    <div className="grid grid-cols-5 gap-2">
                        {gemSlots.map((gem, idx) => (
                            <div key={idx}>
                                {gem ? (
                                    <div
                                        className="relative border-2 border-primary/60 p-2 min-h-[60px] flex flex-col items-center justify-center"
                                    >
                                        <button
                                            onClick={() => handleRemoveGem(idx)}
                                            className="absolute -top-1 -right-1 text-muted-foreground hover:text-destructive"
                                            data-testid={`gemsmith-gem-remove-${idx}`}
                                        >
                                            <X size={12} />
                                        </button>
                                        <Gem size={14} className="text-rarity-rare" />
                                        <div className="stat-label text-[10px] text-center mt-1 leading-tight">
                                            {gem.stat}
                                        </div>
                                        <div className="stat-label text-[10px] text-primary/70">
                                            +{gem.value}
                                        </div>
                                    </div>
                                ) : (
                                    <button
                                        data-testid={`gemsmith-slot-${idx}`}
                                        onClick={() => setActiveSlot(activeSlot === idx ? null : idx)}
                                        className={`border-2 ${activeSlot === idx ? "border-primary bg-primary/10" : "border-border hover:border-primary/60"} p-2 min-h-[60px] flex items-center justify-center`}
                                    >
                                        <span className="stat-label text-muted-foreground/50">+</span>
                                    </button>
                                )}
                            </div>
                        ))}
                    </div>

                    {/* Gem picker dropdown */}
                    {activeSlot !== null && (
                        <div className="mt-3 border-2 border-primary bg-background shadow-lg max-h-[250px] overflow-y-auto">
                            <div className="sticky top-0 bg-background border-b border-border p-2">
                                <div className="flex items-center gap-2">
                                    <Search size={12} className="text-muted-foreground" />
                                    <input
                                        type="text"
                                        value={gemSearch}
                                        onChange={(e) => setGemSearch(e.target.value)}
                                        placeholder="Search gems..."
                                        className="bg-transparent border-none outline-none text-sm w-full"
                                        autoFocus
                                    />
                                </div>
                            </div>
                            {filteredGems.length === 0 ? (
                                <div className="stat-label text-muted-foreground p-3">No gems in inventory.</div>
                            ) : (
                                filteredGems.map((g) => (
                                    <button
                                        key={g.id}
                                        data-testid={`gemsmith-pick-gem-${g.id}`}
                                        onClick={() => handleSelectGem(g)}
                                        className="block w-full text-left p-2 hover:bg-primary/10 border-b border-border/50"
                                    >
                                        <div className="flex justify-between items-center">
                                            <div>
                                                <div className="font-pixel text-xs uppercase text-rarity-rare">{g.name}</div>
                                                <div className="stat-label text-muted-foreground">
                                                    {g.stat} · +{g.value} · x{g.quantity}
                                                </div>
                                            </div>
                                        </div>
                                    </button>
                                ))
                            )}
                        </div>
                    )}

                    {/* Forge button */}
                    <button
                        data-testid="gemsmith-forge"
                        disabled={!canForge}
                        onClick={handleForge}
                        className="press-btn font-pixel text-sm uppercase mt-4 w-full px-4 py-2 border-2 border-primary text-primary hover:bg-primary hover:text-primary-foreground disabled:opacity-40 disabled:cursor-not-allowed flex items-center justify-center gap-2"
                    >
                        <Sparkles size={14} /> {busy ? "Setting..." : "Set Gems"}
                    </button>
                    {!selectedItem && (
                        <div className="stat-label text-muted-foreground text-center mt-2">Select an item to begin.</div>
                    )}
                    {selectedItem && selectedGems.length === 0 && (
                        <div className="stat-label text-muted-foreground text-center mt-2">Click empty slots to assign gems.</div>
                    )}
                </div>
            </div>
        </div>
    );
}
