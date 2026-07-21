import { useState } from "react";
import { api, extractError } from "@/lib/api";
import { toast } from "sonner";
import Dice from "@/components/Dice";
import { RARITY_TEXT } from "@/data/gameData";

export default function CraftingPanel({ character, recipes, itemsById, onCharacterUpdate }) {
    const [rolling, setRolling] = useState(false);
    const [lastCraft, setLastCraft] = useState(null);

    const invMap = Object.fromEntries((character.inventory || []).map(i => [i.item_id, i.quantity]));

    const canCraft = (recipe) => {
        if (character.level < (recipe.min_level || 1)) return false;
        if (recipe.profession_req?.length) {
            if (!recipe.profession_req.includes(character.role) && !recipe.profession_req.includes(character.mastery)) return false;
        }
        for (const [mat, q] of recipe.materials) {
            if ((invMap[mat] || 0) < q) return false;
        }
        return true;
    };

    const craft = async (recipe_id) => {
        setRolling(true);
        setLastCraft(null);
        try {
            const { data } = await api.post("/game/craft", { recipe_id });
            onCharacterUpdate?.(data.character);
            setLastCraft(data.result);
        } catch (e) {
            toast.error(extractError(e));
        } finally {
            setRolling(false);
        }
    };

    return (
        <div className="panel p-6" data-testid="crafting-panel">
            <h3 className="font-pixel text-2xl uppercase text-primary mb-2">Forge & Alchemy</h3>
            <div className="stat-label text-muted-foreground mb-4">
                Every craft is a dice roll. Quality tiers: Crude · Fine · Masterwork.
            </div>

            {lastCraft && (
                <div className="mb-4 p-3 border border-primary bg-primary/5 flex items-center gap-4">
                    <Dice result={lastCraft.outcome} rolling={false} size={64} />
                    <div>
                        <div className="stat-label uppercase text-primary">
                            {lastCraft.tier.toUpperCase()}
                        </div>
                        <div className="narr text-sm text-foreground/85">{lastCraft.narrative}</div>
                        {lastCraft.output_item && (
                            <div className="stat-label mt-1">
                                Produced: {itemsById?.[lastCraft.output_item]?.name || lastCraft.output_item}
                            </div>
                        )}
                    </div>
                </div>
            )}

            <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                {recipes.map((r) => {
                    const output = itemsById?.[r.output_by_tier?.fine || r.output_by_tier?.crude];
                    const okay = canCraft(r);
                    return (
                        <div key={r.id} data-testid={`recipe-${r.id}`} className={`panel p-3 ${!okay ? "opacity-60" : ""}`}>
                            <div className="flex justify-between mb-1">
                                <div className={`font-pixel text-lg uppercase ${RARITY_TEXT[output?.rarity || "common"]}`}>
                                    {r.name}
                                </div>
                                <div className="stat-label">Lv {r.min_level}+</div>
                            </div>
                            {r.profession_req?.length > 0 && (
                                <div className="stat-label text-primary/60 mb-1">
                                    Needs: {r.profession_req.join(", ")}
                                </div>
                            )}
                            <div className="text-xs font-mono mb-2 space-y-0.5">
                                {r.materials.map(([mat, q]) => {
                                    const have = invMap[mat] || 0;
                                    return (
                                        <div key={mat} className="flex justify-between">
                                            <span className="text-muted-foreground">
                                                {itemsById?.[mat]?.name || mat}
                                            </span>
                                            <span className={have >= q ? "text-primary" : "text-destructive"}>
                                                {have}/{q}
                                            </span>
                                        </div>
                                    );
                                })}
                            </div>
                            <button
                                data-testid={`craft-btn-${r.id}`}
                                disabled={!okay || rolling}
                                onClick={() => craft(r.id)}
                                className="press-btn w-full font-pixel text-sm uppercase py-1.5 bg-primary/10 border border-primary text-primary hover:bg-primary hover:text-primary-foreground disabled:opacity-40"
                            >
                                Craft
                            </button>
                        </div>
                    );
                })}
            </div>
        </div>
    );
}
