import { useState, useMemo } from "react";
import { api, extractError } from "@/lib/api";
import { useGameData, RARITY_TEXT, RARITY_CLASS } from "@/data/gameData";
import { toast } from "sonner";
import { Search, X, Sparkles, ChevronDown, ChevronUp } from "lucide-react";

const MAX_RUNE_SLOTS = 10;

const RUNESMITH_NPC = {
    name: "Thalos Runeweaver",
    title: "Master Runesmith",
    desc: "A weathered half-elf whose fingers glow faintly with traced sigils. He reads runes the way others read faces — and charges accordingly.",
    greeting: "Bring me your blade, your shield, your ring — I will carve it full of power. Every rune you've collected finds its home here.",
};

export default function RunesmithPanel({ character, onCharacterUpdate }) {
    const gd = useGameData();
    const [selectedItem, setSelectedItem] = useState(null);
    const [showItemPicker, setShowItemPicker] = useState(false);
    const [itemSearch, setItemSearch] = useState("");
    const [runeSlots, setRuneSlots] = useState(Array(MAX_RUNE_SLOTS).fill(null));
    const [activeSlot, setActiveSlot] = useState(null);
    const [runeSearch, setRuneSearch] = useState("");
    const [busy, setBusy] = useState(false);

    const itemInstances = character?.item_instances || [];
    const inventory = character?.inventory || [];

    const runesById = gd.runesById || {};

    const runesInInventory = useMemo(() => {
        return inventory
            .filter((inv) => {
                const def = runesById[inv.item_id];
                return def && inv.quantity > 0;
            })
            .map((inv) => ({
                ...runesById[inv.item_id],
                quantity: inv.quantity,
                item_id: inv.item_id,
            }));
    }, [inventory, runesById]);

    const upgradableItems = useMemo(() => {
        return itemInstances.filter((inst) => {
            if (!inst.instance_id) return false;
            const kind = inst.kind;
            if (!["weapon", "armor", "trinket", "relic"].includes(kind)) return false;
            const count = inst.upgrades?.count ?? 0;
            const max = inst.upgrades?.max ?? MAX_RUNE_SLOTS;
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

    const filteredRunes = useMemo(() => {
        if (!runeSearch) return runesInInventory;
        const q = runeSearch.toLowerCase();
        return runesInInventory.filter((r) =>
            (r.name || "").toLowerCase().includes(q) ||
            (r.effect_type || "").toLowerCase().includes(q)
        );
    }, [runesInInventory, runeSearch]);

    const currentItemUpgradeCount = selectedItem?.upgrades?.count ?? 0;
    const currentItemMax = selectedItem?.upgrades?.max ?? MAX_RUNE_SLOTS;
    const remainingSlots = currentItemMax - currentItemUpgradeCount;
    const selectedRunes = runeSlots.filter((r) => r !== null);
    const canForge = selectedItem && selectedRunes.length > 0 && selectedRunes.length <= remainingSlots && !busy;

    const handleSelectItem = (item) => {
        setSelectedItem(item);
        setShowItemPicker(false);
        setItemSearch("");
        setRuneSlots(Array(MAX_RUNE_SLOTS).fill(null));
    };

    const handleSelectRune = (rune) => {
        if (activeSlot === null) return;
        const newSlots = [...runeSlots];
        newSlots[activeSlot] = rune;
        setRuneSlots(newSlots);
        setActiveSlot(null);
        setRuneSearch("");
    };

    const handleRemoveRune = (slotIdx) => {
        const newSlots = [...runeSlots];
        newSlots[slotIdx] = null;
        setRuneSlots(newSlots);
    };

    const handleForge = async () => {
        if (!selectedItem || selectedRunes.length === 0) return;
        setBusy(true);
        try {
            const runeIds = selectedRunes.map((r) => r.id);
            const { data } = await api.post("/game/item/runesmith", {
                instance_id: selectedItem.instance_id,
                rune_ids: runeIds,
            });
            onCharacterUpdate?.(data.character);
            const socketed = data.socketed?.length || 0;
            const failed = data.failed?.length || 0;
            if (socketed > 0) {
                toast.success(`Runesmith: Socketed ${socketed} rune(s) into ${selectedItem.name}!`);
            }
            if (failed > 0) {
                toast.warning(`${failed} rune(s) could not be socketed.`);
            }
            setSelectedItem(data.item);
            setRuneSlots(Array(MAX_RUNE_SLOTS).fill(null));
        } catch (e) {
            toast.error(extractError(e));
        } finally {
            setBusy(false);
        }
    };

    return (
        <div className="space-y-4" data-testid="runesmith-panel">
            {/* NPC header */}
            <div className="panel p-6">
                <div className="stat-label text-primary/70">RUNESMITH</div>
                <h2 className="font-pixel text-3xl uppercase text-primary">{RUNESMITH_NPC.name}</h2>
                <div className="stat-label text-primary/80">{RUNESMITH_NPC.title}</div>
                <p className="narr text-muted-foreground mt-2">{RUNESMITH_NPC.desc}</p>
                <div className="border-t border-border mt-3 pt-3">
                    <p className="narr text-sm text-foreground/85 italic">&ldquo;{RUNESMITH_NPC.greeting}&rdquo;</p>
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
                            data-testid="runesmith-item-select"
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
                                            data-testid={`runesmith-item-${it.instance_id}`}
                                            onClick={() => handleSelectItem(it)}
                                            className="block w-full text-left p-2 hover:bg-primary/10 border-b border-border/50"
                                        >
                                            <div className={`font-pixel text-xs uppercase ${RARITY_TEXT[it.rarity] || ""}`}>
                                                {it.name}
                                            </div>
                                            <div className="stat-label text-muted-foreground">
                                                {it.kind} · {it.slot || ""} · Upgrades: {it.upgrades?.count || 0}/{it.upgrades?.max || MAX_RUNE_SLOTS}
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
                            {(selectedItem.upgrades?.runes || []).length > 0 ? (
                                <div className="space-y-1">
                                    {(selectedItem.upgrades.runes).map((r, i) => (
                                        <div key={i} className="stat-label text-foreground/80">
                                            <span className="text-rarity-epic">●</span> {r.type} (+{(r.value * 100).toFixed(1)}%)
                                        </div>
                                    ))}
                                </div>
                            ) : (
                                <div className="stat-label text-muted-foreground italic">No runes socketed yet.</div>
                            )}
                            {(selectedItem.upgrades?.gems || []).length > 0 && (
                                <div className="mt-2 pt-2 border-t border-border">
                                    <div className="stat-label text-primary/70 mb-1">GEMS</div>
                                    {(selectedItem.upgrades.gems).map((g, i) => (
                                        <div key={i} className="stat-label text-foreground/80">
                                            <span className="text-rarity-rare">●</span> {g.stat} (+{g.value})
                                        </div>
                                    ))}
                                </div>
                            )}
                        </div>
                    )}
                </div>

                {/* Right: Rune slots */}
                <div className="panel p-4">
                    <div className="stat-label text-primary/70 mb-2">
                        RUNE SLOTS ({selectedRunes.length}/{remainingSlots} available)
                    </div>

                    {/* 10 rune slot boxes */}
                    <div className="grid grid-cols-5 gap-2">
                        {runeSlots.map((rune, idx) => (
                            <div key={idx}>
                                {rune ? (
                                    <div
                                        className="relative border-2 border-primary/60 p-2 min-h-[60px] flex flex-col items-center justify-center"
                                    >
                                        <button
                                            onClick={() => handleRemoveRune(idx)}
                                            className="absolute -top-1 -right-1 text-muted-foreground hover:text-destructive"
                                            data-testid={`runesmith-rune-remove-${idx}`}
                                        >
                                            <X size={12} />
                                        </button>
                                        <div className="text-rarity-epic text-lg leading-none">◈</div>
                                        <div className="stat-label text-[10px] text-center mt-1 leading-tight">
                                            {rune.effect_type.replace(/_/g, " ")}
                                        </div>
                                        <div className="stat-label text-[10px] text-primary/70">
                                            +{(rune.value * 100).toFixed(1)}%
                                        </div>
                                    </div>
                                ) : (
                                    <button
                                        data-testid={`runesmith-slot-${idx}`}
                                        onClick={() => setActiveSlot(activeSlot === idx ? null : idx)}
                                        className={`border-2 ${activeSlot === idx ? "border-primary bg-primary/10" : "border-border hover:border-primary/60"} p-2 min-h-[60px] flex items-center justify-center`}
                                    >
                                        <span className="stat-label text-muted-foreground/50">+</span>
                                    </button>
                                )}
                            </div>
                        ))}
                    </div>

                    {/* Rune picker dropdown */}
                    {activeSlot !== null && (
                        <div className="mt-3 border-2 border-primary bg-background shadow-lg max-h-[250px] overflow-y-auto">
                            <div className="sticky top-0 bg-background border-b border-border p-2">
                                <div className="flex items-center gap-2">
                                    <Search size={12} className="text-muted-foreground" />
                                    <input
                                        type="text"
                                        value={runeSearch}
                                        onChange={(e) => setRuneSearch(e.target.value)}
                                        placeholder="Search runes..."
                                        className="bg-transparent border-none outline-none text-sm w-full"
                                        autoFocus
                                    />
                                </div>
                            </div>
                            {filteredRunes.length === 0 ? (
                                <div className="stat-label text-muted-foreground p-3">No runes in inventory.</div>
                            ) : (
                                filteredRunes.map((r) => (
                                    <button
                                        key={r.id}
                                        data-testid={`runesmith-pick-rune-${r.id}`}
                                        onClick={() => handleSelectRune(r)}
                                        className="block w-full text-left p-2 hover:bg-primary/10 border-b border-border/50"
                                    >
                                        <div className="flex justify-between items-center">
                                            <div>
                                                <div className="font-pixel text-xs uppercase text-rarity-epic">{r.name}</div>
                                                <div className="stat-label text-muted-foreground">
                                                    {r.effect_type.replace(/_/g, " ")} · +{(r.value * 100).toFixed(1)}% · x{r.quantity}
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
                        data-testid="runesmith-forge"
                        disabled={!canForge}
                        onClick={handleForge}
                        className="press-btn font-pixel text-sm uppercase mt-4 w-full px-4 py-2 border-2 border-primary text-primary hover:bg-primary hover:text-primary-foreground disabled:opacity-40 disabled:cursor-not-allowed flex items-center justify-center gap-2"
                    >
                        <Sparkles size={14} /> {busy ? "Forging..." : "Forge Runes"}
                    </button>
                    {!selectedItem && (
                        <div className="stat-label text-muted-foreground text-center mt-2">Select an item to begin.</div>
                    )}
                    {selectedItem && selectedRunes.length === 0 && (
                        <div className="stat-label text-muted-foreground text-center mt-2">Click empty slots to assign runes.</div>
                    )}
                </div>
            </div>
        </div>
    );
}
