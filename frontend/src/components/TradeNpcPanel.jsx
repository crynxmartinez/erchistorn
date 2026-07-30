import { useEffect, useState } from "react";
import { useGameData } from "@/data/gameData";
import { api } from "@/lib/api";
import ProfessionsPanel from "@/components/ProfessionsPanel";
import CraftingPanel from "@/components/CraftingPanel";

export default function TradeNpcPanel({ town, character, onCharacterUpdate }) {
    const gd = useGameData();
    const tradeNpc = town?.trade_npc;
    const [professions, setProfessions] = useState([]);
    const [professionsLoading, setProfessionsLoading] = useState(true);

    const reloadProfessions = async () => {
        try {
            const { data } = await api.get("/game/professions/mine");
            setProfessions(data.professions || []);
        } catch { /* ignore */ }
        finally { setProfessionsLoading(false); }
    };

    useEffect(() => { reloadProfessions(); }, [character?.professions]);

    const handleCharacterUpdate = (ch) => {
        onCharacterUpdate?.(ch);
        reloadProfessions();
    };

    if (!tradeNpc) {
        return (
            <div className="panel p-6">
                <div className="stat-label text-muted-foreground">No trade master in this town.</div>
            </div>
        );
    }

    const fmt = (id) => id.replace(/_/g, " ");

    return (
        <div className="space-y-4" data-testid="trade-npc-panel">
            <div className="panel p-6 mb-4">
                <div className="stat-label text-primary/70">TRADE MASTER</div>
                <h2 className="font-pixel text-3xl uppercase text-primary">{tradeNpc.name}</h2>
                <div className="stat-label text-primary/80">{tradeNpc.title}</div>
                <p className="narr text-muted-foreground mt-2">{tradeNpc.desc}</p>
                <div className="mt-4 flex flex-wrap gap-2">
                    {tradeNpc.specialties.map((s) => (
                        <span key={s} className="px-2 py-1 border border-primary/40 text-primary text-xs font-pixel uppercase">
                            {fmt(s)}
                        </span>
                    ))}
                </div>
            </div>

            <ProfessionsPanel character={character} onChanged={handleCharacterUpdate} />

            <CraftingPanel
                character={character}
                itemsById={gd.itemsById}
                onCharacterUpdate={handleCharacterUpdate}
                professions={professions}
                professionsLoading={professionsLoading}
            />
        </div>
    );
}
