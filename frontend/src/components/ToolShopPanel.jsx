import { useEffect, useState } from "react";
import { api, extractError } from "@/lib/api";
import { toast } from "sonner";
import { Wrench, Coins } from "lucide-react";
import PixelSprite from "@/components/PixelSprite";

export default function ToolShopPanel({ character, onCharacterUpdate }) {
    const [tools, setTools] = useState([]);
    const [loading, setLoading] = useState(true);
    const [busy, setBusy] = useState(null);

    const load = async () => {
        try {
            const { data } = await api.get("/game/tools/all");
            setTools(data.tools || []);
        } catch (e) {
            toast.error(extractError(e));
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => { load(); }, []);

    const repair = async (profession_id) => {
        setBusy(profession_id);
        try {
            const { data } = await api.post("/game/tools/repair", { profession_id });
            onCharacterUpdate?.(data.character);
            toast.success(`Repaired ${tools.find(t => t.profession_id === profession_id)?.tool_name} — ${data.paid}g`);
            await load();
        } catch (e) {
            toast.error(extractError(e));
        } finally {
            setBusy(null);
        }
    };

    const buy = async (profession_id) => {
        setBusy(profession_id);
        try {
            const { data } = await api.post("/game/tools/buy", { profession_id });
            onCharacterUpdate?.(data.character);
            toast.success(`Bought ${data.tool_name} — ${data.paid}g`);
            await load();
        } catch (e) {
            toast.error(extractError(e));
        } finally {
            setBusy(null);
        }
    };

    if (loading) {
        return <div className="stat-label text-muted-foreground py-4">Loading tools...</div>;
    }

    const ownedTools = tools.filter(t => t.owned);
    const buyableTools = tools.filter(t => !t.owned);

    return (
        <div className="space-y-6">
            {/* Repair section */}
            {ownedTools.length > 0 && (
                <div>
                    <h3 className="font-pixel text-xl uppercase text-primary mb-3 flex items-center gap-2">
                        <Wrench size={16} /> Tool Repair
                    </h3>
                    <div className="space-y-2">
                        {ownedTools.map(t => {
                            const pct = Math.round((t.durability / t.max_durability) * 100);
                            const needsRepair = t.durability < t.max_durability;
                            const lowDur = pct < 20;
                            return (
                                <div key={t.profession_id} className="panel p-3 flex items-center gap-3">
                                    <PixelSprite item={{ name: t.tool_name, tool_id: t.tool_id, rarity: "common" }} size={36} />
                                    <div className="flex-1 min-w-0">
                                        <div className="flex justify-between items-center mb-1">
                                            <div className="font-pixel text-sm uppercase text-primary">
                                                {t.tool_name}
                                            </div>
                                            <div className={`stat-label text-xs ${lowDur ? "text-destructive" : "text-muted-foreground"}`}>
                                                {t.durability}/{t.max_durability}
                                            </div>
                                        </div>
                                        <div className="h-2 bg-background border border-border">
                                            <div
                                                className={`h-full transition-all ${lowDur ? "bg-destructive" : pct < 50 ? "bg-amber-400" : "bg-primary"}`}
                                                style={{ width: `${pct}%` }}
                                            />
                                        </div>
                                        <div className="stat-label text-[10px] text-muted-foreground mt-1">
                                            {t.profession}
                                        </div>
                                    </div>
                                    <button
                                        data-testid={`repair-tool-${t.profession_id}`}
                                        disabled={!needsRepair || busy === t.profession_id || character.gold < t.repair_cost}
                                        onClick={() => repair(t.profession_id)}
                                        className="press-btn stat-label px-3 py-2 border border-primary text-primary hover:bg-primary hover:text-primary-foreground disabled:opacity-40 flex items-center gap-1 whitespace-nowrap"
                                    >
                                        <Coins size={12} />
                                        {needsRepair ? `REPAIR ${t.repair_cost}g` : "FULL"}
                                    </button>
                                </div>
                            );
                        })}
                    </div>
                </div>
            )}

            {/* Buy tools section */}
            {buyableTools.length > 0 && (
                <div>
                    <h3 className="font-pixel text-xl uppercase text-primary mb-3 flex items-center gap-2">
                        <Coins size={16} /> Basic Tools
                    </h3>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
                        {buyableTools.map(t => (
                            <div key={t.profession_id} className="panel p-3 flex items-center justify-between gap-3">
                                <PixelSprite item={{ name: t.tool_name, tool_id: t.tool_id, rarity: "common" }} size={36} />
                                <div className="flex-1 min-w-0">
                                    <div className="font-pixel text-sm uppercase text-primary">
                                        {t.tool_name}
                                    </div>
                                    <div className="stat-label text-[10px] text-muted-foreground">
                                        {t.profession} · {t.max_durability} max dur
                                    </div>
                                </div>
                                <button
                                    data-testid={`buy-tool-${t.profession_id}`}
                                    disabled={busy === t.profession_id || character.gold < t.purchase_cost}
                                    onClick={() => buy(t.profession_id)}
                                    className="press-btn stat-label px-3 py-2 border border-primary text-primary hover:bg-primary hover:text-primary-foreground disabled:opacity-40 flex items-center gap-1 whitespace-nowrap"
                                >
                                    <Coins size={12} /> {t.purchase_cost}g
                                </button>
                            </div>
                        ))}
                    </div>
                </div>
            )}

            {tools.length === 0 && (
                <div className="stat-label text-muted-foreground py-4">
                    No tools available.
                </div>
            )}
        </div>
    );
}
