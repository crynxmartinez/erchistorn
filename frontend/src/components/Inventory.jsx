import { useMemo, useState } from "react";
import { api, extractError } from "@/lib/api";
import { toast } from "sonner";
import { Star, Trash2, Swords, Shield, Sparkles, Zap, BookOpen, Coins, Search, ArrowUpDown, ChevronDown, X } from "lucide-react";
import { RARITY_CLASS, RARITY_TEXT } from "@/data/gameData";
import { Tooltip, TooltipTrigger, TooltipContent, TooltipProvider } from "@/components/ui/tooltip";
import PixelSprite from "@/components/PixelSprite";
import ItemTooltip from "@/components/ItemTooltip";

const CATEGORIES = [
    { id: "all", label: "All" },
    { id: "weapon", label: "Weapons" },
    { id: "armor", label: "Armor" },
    { id: "consumable", label: "Consumables" },
    { id: "material", label: "Materials" },
    { id: "tool", label: "Tools" },
    { id: "skillbook", label: "Skillbooks" },
    { id: "relic", label: "Relics" },
    { id: "gem", label: "Gems" },
    { id: "rune", label: "Runes" },
];

const EQUIP_SLOTS = [
    "head", "body", "left_hand", "right_hand",
    "legs", "feet", "hands", "earring_l", "earring_r",
    "ring_l", "ring_r", "neck", "back",
];

const SLOT_LABELS = {
    head: "Head", body: "Body", left_hand: "L.Hand", right_hand: "R.Hand",
    legs: "Legs", feet: "Feet", hands: "Hands",
    earring_l: "Ear L", earring_r: "Ear R",
    ring_l: "Ring L", ring_r: "Ring R", neck: "Neck", back: "Back",
};

const SLOT_ICONS = {
    head: Shield, body: Shield, left_hand: Swords, right_hand: Swords,
    legs: Shield, feet: Shield, earring_l: Sparkles, earring_r: Sparkles,
    ring_l: Sparkles, ring_r: Sparkles, neck: Sparkles, back: Shield,
};

const RARITY_ORDER = { common: 0, uncommon: 1, rare: 2, epic: 3, legendary: 4, mythic: 5, exotic: 6, normal: 0, magic: 1, unique: 3, set: 4 };

const SORT_OPTIONS = [
    { id: "rarity_desc", label: "Rarity ↓" },
    { id: "rarity_asc", label: "Rarity ↑" },
    { id: "name_az", label: "Name A-Z" },
    { id: "qty_desc", label: "Quantity ↓" },
    { id: "type", label: "Type" },
];

export default function Inventory({ character, itemsById, onCharacterUpdate, onSell }) {
    const inv = character.inventory || [];
    const equipped = character.equipped || {};
    const itemBar = character.item_bar || Array(5).fill(null);
    const itemInstances = character.item_instances || [];
    const [pickingItem, setPickingItem] = useState(null);
    const [search, setSearch] = useState("");
    const [category, setCategory] = useState("all");
    const [sortBy, setSortBy] = useState("rarity_desc");
    const [favsOnly, setFavsOnly] = useState(false);

    // Resolve item by ID: check item_instances first, then itemsById
    const resolveItem = (id) => {
        if (!id) return null;
        const inst = itemInstances.find((i) => i.instance_id === id);
        if (inst) return inst;
        return itemsById?.[id] || null;
    };

    const filteredInv = useMemo(() => {
        let result = inv.filter((slot) => {
            const def = resolveItem(slot.item_id);
            if (!def) return false;
            if ((slot.quantity || 0) <= 0) return false;
            if (favsOnly && !slot.favorite) return false;
            if (category !== "all") {
                if (category === "weapon" && def.kind !== "weapon") return false;
                if (category === "armor" && def.kind !== "armor") return false;
                if (category === "consumable" && def.kind !== "consumable") return false;
                if (category === "material" && def.kind !== "material") return false;
                if (category === "tool" && def.kind !== "tool") return false;
                if (category === "skillbook" && def.kind !== "skillbook") return false;
                if (category === "relic" && def.kind !== "relic") return false;
                if (category === "gem" && def.kind !== "gem") return false;
                if (category === "rune" && def.kind !== "rune") return false;
            }
            if (search) {
                if (!def.name.toLowerCase().includes(search.toLowerCase())) return false;
            }
            return true;
        });
        const sorted = [...result];
        sorted.sort((a, b) => {
            const da = resolveItem(a.item_id);
            const db = resolveItem(b.item_id);
            if (!da || !db) return 0;
            switch (sortBy) {
                case "rarity_desc":
                    return (RARITY_ORDER[db.rarity] || 0) - (RARITY_ORDER[da.rarity] || 0);
                case "rarity_asc":
                    return (RARITY_ORDER[da.rarity] || 0) - (RARITY_ORDER[db.rarity] || 0);
                case "name_az":
                    return da.name.localeCompare(db.name);
                case "qty_desc":
                    return (b.quantity || 0) - (a.quantity || 0);
                case "type":
                    return (da.kind || "").localeCompare(db.kind || "") || da.name.localeCompare(db.name);
                default:
                    return 0;
            }
        });
        // Favorites always float to top within same sort
        if (sortBy !== "type") {
            sorted.sort((a, b) => (b.favorite ? 1 : 0) - (a.favorite ? 1 : 0));
        }
        return sorted;
    }, [inv, itemInstances, itemsById, search, category, sortBy, favsOnly]);

    const refresh = (data) => onCharacterUpdate?.(data.character);

    const assignItem = async (slot, item_id) => {
        try {
            const { data } = await api.post("/game/item/assign", { slot, item_id });
            refresh(data);
            setPickingItem(null);
        } catch (e) {
            toast.error(extractError(e));
        }
    };

    const unassignItem = async (slot) => {
        try {
            const { data } = await api.post("/game/item/unassign", { slot });
            refresh(data);
        } catch (e) {
            toast.error(extractError(e));
        }
    };

    const equip = async (item_id, slot) => {
        try {
            const { data } = await api.post("/game/equip", { item_id, slot });
            refresh(data);
            toast.success("Equipped");
        } catch (e) {
            toast.error(extractError(e));
        }
    };

    const unequip = async (slot) => {
        try {
            const { data } = await api.post("/game/unequip", { slot });
            refresh(data);
            toast.success("Unequipped");
        } catch (e) {
            toast.error(extractError(e));
        }
    };

    const getValidSlots = (def) => {
        const itemSlot = def.slot;
        if (!itemSlot) return [];
        if (itemSlot === "ring_l") return ["ring_l", "ring_r"];
        if (itemSlot === "earring_l") return ["earring_l", "earring_r"];
        if (itemSlot === "left_hand" || itemSlot === "right_hand") {
            const slots = ["left_hand", "right_hand"];
            if (def.is_shield) slots.push("back");
            return slots;
        }
        return [itemSlot];
    };

    const getEquippedSlots = (item_id) => {
        return EQUIP_SLOTS.filter((s) => equipped[s] === item_id);
    };

    const consumeItem = async (item_id) => {
        try {
            const { data } = await api.post("/game/inventory/use", { item_id });
            refresh(data);
            toast.success(data.message || "Used");
        } catch (e) {
            toast.error(extractError(e));
        }
    };

    const trash = async (item_id) => {
        try {
            const { data } = await api.post("/game/inventory/trash", { item_id, quantity: 1 });
            refresh(data);
            toast.success("Trashed");
        } catch (e) {
            toast.error(extractError(e));
        }
    };

    const favorite = async (item_id, isFav) => {
        try {
            const { data } = await api.post("/game/inventory/favorite", { item_id, favorite: !isFav });
            refresh(data);
        } catch (e) {
            toast.error(extractError(e));
        }
    };

    const learnFromBook = async (item_id, teaches) => {
        try {
            const { data } = await api.post("/game/skill/learn", {
                skill_id: teaches,
                skillbook_item_id: item_id,
            });
            refresh(data);
            toast.success(`Learned ${teaches.replace(/_/g, " ")}!`);
        } catch (e) {
            toast.error(extractError(e));
        }
    };

    const statLine = (it) => {
        const parts = [];
        if (it.accuracy) parts.push(`ACC +${it.accuracy}`);
        if (it.evasion) parts.push(`EVA +${it.evasion}`);
        if (it.stats) {
            for (const [k, v] of Object.entries(it.stats)) {
                parts.push(`${k.toUpperCase().slice(0, 3)} +${v}`);
            }
        }
        if (it.base_stats) {
            for (const [k, v] of Object.entries(it.base_stats)) {
                if (v) parts.push(`${k.toUpperCase().slice(0, 3)} +${v}`);
            }
        }
        return parts.join(" · ") || "—";
    };

    if (!inv.length) {
        return (
            <div className="panel p-6" data-testid="inventory">
                <h3 className="font-pixel text-2xl uppercase text-primary mb-2">Inventory</h3>
                <div className="stat-label text-muted-foreground">Empty pouch. Go find something.</div>
            </div>
        );
    }

    const sortIndex = SORT_OPTIONS.findIndex(s => s.id === sortBy);
    const cycleSort = () => setSortBy(SORT_OPTIONS[(sortIndex + 1) % SORT_OPTIONS.length].id);

    const EquipButton = ({ item, def }) => {
        const equippedSlots = getEquippedSlots(item.item_id);
        const isEquipped = equippedSlots.length > 0;
        const [showPicker, setShowPicker] = useState(false);
        const validSlots = getValidSlots(def);

        if (isEquipped) {
            return (
                <button
                    data-testid={`unequip-${item.item_id}`}
                    onClick={() => unequip(equippedSlots[0])}
                    className="press-btn flex-1 stat-label border border-amber-500 text-amber-500 hover:bg-amber-500 hover:text-amber-950 flex items-center justify-center gap-1 py-1"
                >
                    <X size={12} /> UNEQUIP
                </button>
            );
        }

        if (validSlots.length === 1) {
            const slot = validSlots[0];
            const currentId = equipped[slot];
            const current = currentId ? resolveItem(currentId) : null;
            return (
                <Tooltip>
                    <TooltipTrigger asChild>
                        <button
                            data-testid={`equip-${slot}-${item.item_id}`}
                            onClick={() => equip(item.item_id, slot)}
                            className="press-btn flex-1 stat-label border border-primary text-primary hover:bg-primary hover:text-primary-foreground flex items-center justify-center gap-1 py-1"
                        >
                            <Swords size={12} /> EQUIP
                        </button>
                    </TooltipTrigger>
                    <TooltipContent side="bottom" className="max-w-[220px] bg-popover border border-border text-popover-foreground">
                        <div className="font-pixel text-xs uppercase text-primary mb-1">{SLOT_LABELS[slot]}</div>
                        <div className="text-[10px] space-y-1">
                            <div className="text-muted-foreground">Current: {current?.name || "None"}</div>
                            <div className="text-muted-foreground">{statLine(current || {})}</div>
                            <div className="text-primary">New: {def.name}</div>
                            <div className="text-primary">{statLine(def)}</div>
                        </div>
                    </TooltipContent>
                </Tooltip>
            );
        }

        return (
            <div className="relative flex-1">
                <button
                    data-testid={`equip-picker-${item.item_id}`}
                    onClick={() => setShowPicker(!showPicker)}
                    className="press-btn w-full stat-label border border-primary text-primary hover:bg-primary hover:text-primary-foreground flex items-center justify-center gap-1 py-1"
                >
                    <Swords size={12} /> EQUIP <ChevronDown size={12} />
                </button>
                {showPicker && (
                    <div className="absolute bottom-full left-0 right-0 mb-1 bg-popover border border-border z-20 shadow-lg">
                        {validSlots.map((slot) => {
                            const currentId = equipped[slot];
                            const current = currentId ? resolveItem(currentId) : null;
                            const Icon = SLOT_ICONS[slot] || Swords;
                            return (
                                <Tooltip key={slot}>
                                    <TooltipTrigger asChild>
                                        <button
                                            data-testid={`equip-${slot}-${item.item_id}`}
                                            onClick={() => { equip(item.item_id, slot); setShowPicker(false); }}
                                            className="w-full flex items-center gap-1.5 px-2 py-1.5 text-xs hover:bg-primary hover:text-primary-foreground border-b border-border/50 last:border-0"
                                        >
                                            <Icon size={12} className="flex-shrink-0" />
                                            <span className="truncate flex-1 text-left">
                                                {current ? (
                                                    <><span className="text-muted-foreground">Replace </span>{current.name}</>
                                                ) : (
                                                    SLOT_LABELS[slot]
                                                )}
                                            </span>
                                        </button>
                                    </TooltipTrigger>
                                    <TooltipContent side="left" className="max-w-[220px] bg-popover border border-border text-popover-foreground">
                                        <div className="font-pixel text-xs uppercase text-primary mb-1">{SLOT_LABELS[slot]}</div>
                                        <div className="text-[10px] space-y-1">
                                            <div className="text-muted-foreground">Current: {current?.name || "None"}</div>
                                            <div className="text-muted-foreground">{statLine(current || {})}</div>
                                            <div className="text-primary">New: {def.name}</div>
                                            <div className="text-primary">{statLine(def)}</div>
                                        </div>
                                    </TooltipContent>
                                </Tooltip>
                            );
                        })}
                    </div>
                )}
            </div>
        );
    };

    return (
        <TooltipProvider delayDuration={120}>
        <div className="panel p-6" data-testid="inventory">
            <h3 className="font-pixel text-2xl uppercase text-primary mb-4">Inventory</h3>

            {/* Search + sort + favorites toggle */}
            <div className="flex flex-wrap items-center gap-2 mb-3">
                <div className="relative flex-1 min-w-[140px]">
                    <Search size={14} className="absolute left-2 top-1/2 -translate-y-1/2 text-muted-foreground" />
                    <input
                        type="text"
                        value={search}
                        onChange={(e) => setSearch(e.target.value)}
                        placeholder="Search items…"
                        data-testid="inv-search"
                        className="w-full pl-7 pr-2 py-1.5 bg-background border border-border text-sm text-foreground placeholder:text-muted-foreground focus:border-primary outline-none"
                    />
                </div>
                <button
                    onClick={cycleSort}
                    data-testid="inv-sort"
                    className="press-btn flex items-center gap-1 stat-label px-2 py-1.5 border border-border text-muted-foreground hover:border-primary hover:text-primary"
                    title="Cycle sort order"
                >
                    <ArrowUpDown size={14} /> {SORT_OPTIONS[sortIndex].label}
                </button>
                <button
                    onClick={() => setFavsOnly(!favsOnly)}
                    data-testid="inv-favs-toggle"
                    className={`press-btn flex items-center gap-1 stat-label px-2 py-1.5 border ${favsOnly ? "border-amber-400 text-amber-400" : "border-border text-muted-foreground hover:border-amber-400 hover:text-amber-400"}`}
                    title="Show favorites only"
                >
                    <Star size={14} fill={favsOnly ? "currentColor" : "none"} /> FAVS
                </button>
            </div>

            {/* Category tabs */}
            <div className="flex flex-wrap gap-1 mb-4">
                {CATEGORIES.map(c => {
                    const count = c.id === "all" ? inv.length : inv.filter(slot => {
                        const def = resolveItem(slot.item_id);
                        if (!def) return false;
                        if (c.id === "weapon") return def.kind === "weapon";
                        if (c.id === "armor") return def.kind === "armor";
                        if (c.id === "gem") return def.kind === "gem";
                        if (c.id === "rune") return def.kind === "rune";
                        return def.kind === c.id;
                    }).length;
                    if (count === 0 && c.id !== "all") return null;
                    return (
                        <button
                            key={c.id}
                            data-testid={`inv-cat-${c.id}`}
                            onClick={() => setCategory(c.id)}
                            className={`press-btn font-pixel text-xs uppercase px-2.5 py-1 border-2 ${
                                category === c.id
                                    ? "border-primary bg-primary text-primary-foreground"
                                    : "border-border text-muted-foreground hover:border-primary hover:text-primary"
                            }`}
                        >
                            {c.label}{count > 0 && <span className="ml-1 opacity-60">{count}</span>}
                        </button>
                    );
                })}
            </div>

            {/* Result count */}
            <div className="stat-label text-muted-foreground text-[10px] mb-3">
                {filteredInv.length} item{filteredInv.length !== 1 ? "s" : ""}
                {search && ` matching "${search}"`}
                {favsOnly && " ★"}
            </div>

            <div className="mb-4">
                <div className="stat-label mb-2 text-primary/70">HOTBAR</div>
                <div className="flex flex-wrap gap-2">
                    {itemBar.map((iid, idx) => {
                        const def = iid ? resolveItem(iid) : null;
                        const isPicking = pickingItem === idx;
                        const options = inv
                            .filter((i) => resolveItem(i.item_id)?.kind === "consumable" && i.quantity > 0)
                            .map((i) => i.item_id);
                        return (
                            <div key={idx} className="relative">
                                <button
                                    data-testid={`item-slot-${idx}`}
                                    onClick={() => setPickingItem(isPicking ? null : idx)}
                                    className={`w-12 h-12 border flex items-center justify-center text-xs font-pixel uppercase ${iid ? "border-primary text-primary" : "border-border text-muted-foreground hover:border-primary/50"}`}
                                >
                                    {def ? <ItemTooltip item={def}><span><PixelSprite item={def} size={32} /></span></ItemTooltip> : idx + 1}
                                </button>
                                {isPicking && (
                                    <div className="absolute z-10 mt-1 bg-background border border-primary p-2 w-40 max-h-48 overflow-y-auto">
                                        {options.length === 0 && (
                                            <div className="stat-label text-muted-foreground">No consumables</div>
                                        )}
                                        {options.map((id) => {
                                            const it = resolveItem(id);
                                            return (
                                                <button
                                                    key={id}
                                                    onClick={() => assignItem(idx, id)}
                                                    className="flex w-full text-left text-xs font-mono py-1 hover:text-primary items-center gap-1.5"
                                                >
                                                    {it && <PixelSprite item={it} size={18} />}
                                                    {it?.name || id}
                                                </button>
                                            );
                                        })}
                                        {iid && (
                                            <button
                                                onClick={() => unassignItem(idx)}
                                                className="block w-full text-left text-xs text-destructive py-1 hover:underline"
                                            >
                                                Clear slot
                                            </button>
                                        )}
                                    </div>
                                )}
                            </div>
                        );
                    })}
                </div>
            </div>
            <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-3">
                {filteredInv.length === 0 && (
                    <div className="col-span-full stat-label text-muted-foreground text-center py-8">
                        No items match your filters.
                    </div>
                )}
                {filteredInv.map((slot, i) => {
                    const def = resolveItem(slot.item_id);
                    if (!def) return null;
                    const isEquipped = EQUIP_SLOTS.some(s => equipped[s] === slot.item_id);
                    const isFav = slot.favorite;
                    const slotName = def.slot || def.kind;
                    return (
                        <ItemTooltip key={`${slot.item_id}-${i}`} item={def}>
                        <div
                            data-testid={`inv-item-${slot.item_id}`}
                            className={`panel p-2 ${RARITY_CLASS[def.rarity]} relative`}
                        >
                            <div className="flex justify-between items-start mb-1">
                                <div className="flex-shrink-0">
                                    <PixelSprite item={def} size={36} />
                                </div>
                                <button
                                    onClick={() => favorite(slot.item_id, isFav)}
                                    className={`${isFav ? "text-amber-400" : "text-muted-foreground/50 hover:text-amber-400"}`}
                                    title={isFav ? "Unfavorite" : "Favorite"}
                                >
                                    <Star size={14} fill={isFav ? "currentColor" : "none"} />
                                </button>
                            </div>
                            <div className={`font-pixel text-sm uppercase truncate ${RARITY_TEXT[def.rarity]}`}>
                                {def.name}
                            </div>
                            <div className="flex justify-between stat-label mt-1">
                                <span className="uppercase">{def.rarity}</span>
                                <span>× {slot.quantity}</span>
                            </div>
                            {statLine(def) && (
                                <div className="text-[10px] text-muted-foreground mt-1 truncate">{statLine(def)}</div>
                            )}
                            {def.kind === "tool" && slot.durability !== undefined && (
                                <div className={`text-[10px] mt-1 ${slot.durability <= 0 ? "text-destructive" : slot.durability < def.max_durability * 0.2 ? "text-amber-400" : "text-muted-foreground"}`}>
                                    DUR {slot.durability}/{def.max_durability}
                                </div>
                            )}
                            <div className="flex gap-1 mt-2">
                                {(def.kind === "weapon" || def.kind === "armor" || (def.slot && EQUIP_SLOTS.includes(def.slot))) && (
                                    <EquipButton item={slot} def={def} />
                                )}
                                {def.kind === "consumable" && (
                                    <button
                                        data-testid={`use-${slot.item_id}`}
                                        onClick={() => consumeItem(slot.item_id)}
                                        className="press-btn flex-1 stat-label border border-primary text-primary hover:bg-primary hover:text-primary-foreground flex items-center justify-center gap-1 py-1"
                                    >
                                        <Zap size={12} /> USE
                                    </button>
                                )}
                                {def.kind === "skillbook" && (
                                    <button
                                        data-testid={`learn-book-${slot.item_id}`}
                                        onClick={() => learnFromBook(slot.item_id, def.teaches)}
                                        className="press-btn flex-1 stat-label border border-primary text-primary hover:bg-primary hover:text-primary-foreground flex items-center justify-center gap-1 py-1"
                                    >
                                        <BookOpen size={12} /> STUDY
                                    </button>
                                )}
                            </div>
                            {onSell && (
                                <button
                                    data-testid={`sell-${slot.item_id}`}
                                    disabled={isEquipped || isFav}
                                    onClick={() => onSell(slot.item_id)}
                                    className="press-btn w-full mt-1 stat-label border border-primary/50 text-primary/80 hover:bg-primary hover:text-primary-foreground disabled:opacity-40 flex items-center justify-center gap-1 py-1"
                                >
                                    <Coins size={12} /> SELL
                                </button>
                            )}
                            <button
                                data-testid={`trash-${slot.item_id}`}
                                disabled={isEquipped || isFav}
                                onClick={() => trash(slot.item_id)}
                                className="press-btn w-full mt-1 stat-label border border-destructive/50 text-destructive/80 hover:bg-destructive hover:text-destructive-foreground disabled:opacity-40 flex items-center justify-center gap-1 py-1"
                            >
                                <Trash2 size={12} /> TRASH
                            </button>
                        </div>
                        </ItemTooltip>
                    );
                })}
            </div>
        </div>
        </TooltipProvider>
    );
}
