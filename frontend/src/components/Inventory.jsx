import { api, extractError } from "@/lib/api";
import { toast } from "sonner";
import { RARITY_CLASS, RARITY_TEXT } from "@/data/gameData";

export default function Inventory({ character, itemsById, onCharacterUpdate }) {
    const inv = character.inventory || [];
    const equipped = character.equipped || {};

    const equip = async (item_id, slot) => {
        try {
            const { data } = await api.post("/game/equip", { item_id, slot });
            onCharacterUpdate?.(data.character);
            toast.success("Equipped");
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
            onCharacterUpdate?.(data.character);
            toast.success(`Learned ${teaches.replace(/_/g, " ")}!`);
        } catch (e) {
            toast.error(extractError(e));
        }
    };

    if (!inv.length) {
        return (
            <div className="panel p-6" data-testid="inventory">
                <h3 className="font-pixel text-2xl uppercase text-primary mb-2">Inventory</h3>
                <div className="stat-label text-muted-foreground">Empty pouch. Go find something.</div>
            </div>
        );
    }

    return (
        <div className="panel p-6" data-testid="inventory">
            <h3 className="font-pixel text-2xl uppercase text-primary mb-4">Inventory</h3>
            <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-3">
                {inv.map((slot, i) => {
                    const def = itemsById?.[slot.item_id];
                    if (!def) return null;
                    const isEquipped =
                        equipped.weapon === slot.item_id ||
                        equipped.armor === slot.item_id ||
                        equipped.trinket === slot.item_id;
                    return (
                        <div
                            key={`${slot.item_id}-${i}`}
                            data-testid={`inv-item-${slot.item_id}`}
                            className={`panel p-2 ${RARITY_CLASS[def.rarity]}`}
                        >
                            <div className="sprite-slot text-xs mb-2">{def.name.charAt(0).toUpperCase()}</div>
                            <div className={`font-pixel text-sm uppercase truncate ${RARITY_TEXT[def.rarity]}`}>
                                {def.name}
                            </div>
                            <div className="flex justify-between stat-label mt-1">
                                <span className="uppercase">{def.rarity}</span>
                                <span>× {slot.quantity}</span>
                            </div>
                            {def.kind === "weapon" && (
                                <button
                                    data-testid={`equip-weapon-${slot.item_id}`}
                                    disabled={isEquipped}
                                    onClick={() => equip(slot.item_id, "weapon")}
                                    className="press-btn w-full mt-2 stat-label border border-primary text-primary hover:bg-primary hover:text-primary-foreground disabled:opacity-40"
                                >
                                    {isEquipped ? "EQUIPPED" : "EQUIP"}
                                </button>
                            )}
                            {def.kind === "armor" && (
                                <button
                                    data-testid={`equip-armor-${slot.item_id}`}
                                    disabled={isEquipped}
                                    onClick={() => equip(slot.item_id, "armor")}
                                    className="press-btn w-full mt-2 stat-label border border-primary text-primary hover:bg-primary hover:text-primary-foreground disabled:opacity-40"
                                >
                                    {isEquipped ? "EQUIPPED" : "EQUIP"}
                                </button>
                            )}
                            {def.kind === "skillbook" && (
                                <button
                                    data-testid={`learn-book-${slot.item_id}`}
                                    onClick={() => learnFromBook(slot.item_id, def.teaches)}
                                    className="press-btn w-full mt-2 stat-label border border-primary text-primary hover:bg-primary hover:text-primary-foreground"
                                >
                                    STUDY
                                </button>
                            )}
                        </div>
                    );
                })}
            </div>
        </div>
    );
}
