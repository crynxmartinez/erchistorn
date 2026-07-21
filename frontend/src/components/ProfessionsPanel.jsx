import { useEffect, useState } from "react";
import { api, extractError } from "@/lib/api";
import { toast } from "sonner";
import { Hammer, Sprout, Anchor, X } from "lucide-react";

/**
 * ProfessionsPanel — Codex-tab-style view of the character's 3 profession slots
 * plus the full catalog. First slot at Lv 1, second at Lv 10, third at Lv 25.
 */
export default function ProfessionsPanel({ character, onChanged }) {
    const [catalog, setCatalog] = useState([]);
    const [ranks, setRanks] = useState([]);
    const [mine, setMine] = useState([]);
    const [slots, setSlots] = useState(1);
    const [busy, setBusy] = useState(false);

    const reload = async () => {
        try {
            const [c, m] = await Promise.all([
                api.get("/game/professions/catalog"),
                api.get("/game/professions/mine"),
            ]);
            setCatalog(c.data.catalog);
            setRanks(c.data.ranks);
            setSlots(c.data.slots_unlocked);
            setMine(m.data.professions);
        } catch (e) { toast.error(extractError(e)); }
    };
    useEffect(() => { reload(); }, [character?.level]);

    const learn = async (id) => {
        setBusy(true);
        try {
            const r = await api.post("/game/professions/learn", { profession_id: id });
            toast.success(r.data.message);
            onChanged?.(r.data.character);
            await reload();
        } catch (e) { toast.error(extractError(e)); }
        finally { setBusy(false); }
    };
    const abandon = async (id) => {
        setBusy(true);
        try {
            const r = await api.post("/game/professions/abandon", { profession_id: id });
            toast(r.data.message);
            onChanged?.(r.data.character);
            await reload();
        } catch (e) { toast.error(extractError(e)); }
        finally { setBusy(false); }
    };

    const kindIcon = (kind) => {
        if (kind === "gathering") return <Sprout size={12} className="text-primary" />;
        if (kind === "crafting")  return <Hammer size={12} className="text-primary" />;
        return <Anchor size={12} className="text-primary" />;
    };

    return (
        <div data-testid="professions-panel">
            <div className="mb-4">
                <div className="stat-label text-primary/70">CRAFT · GATHER · SERVE</div>
                <h2 className="font-pixel text-3xl uppercase text-primary">Professions</h2>
                <div className="narr text-sm text-muted-foreground mt-1">
                    A hero may hold up to three trades in their hands. Choose them slowly — every abandonment costs.
                </div>
                <div className="stat-label text-primary/80 mt-2">SLOTS UNLOCKED: {slots}/3 · next unlock at Lv {slots === 1 ? 10 : slots === 2 ? 25 : "—"}</div>
            </div>

            {/* Learned professions */}
            <div className="border-t border-border pt-3 mb-4">
                <div className="stat-label text-primary/70 mb-2">YOUR PROFESSIONS</div>
                {mine.length === 0 && <div className="stat-label text-muted-foreground">None yet. Pick one below.</div>}
                <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
                    {mine.map((p) => (
                        <div key={p.id} className="border border-border p-3 flex justify-between items-start" data-testid={`prof-active-${p.id}`}>
                            <div>
                                <div className="font-pixel text-lg uppercase text-primary flex items-center gap-1.5">{kindIcon(p.kind)} {p.name}</div>
                                <div className="stat-label text-muted-foreground">{p.rank.toUpperCase()} · {p.xp} xp</div>
                            </div>
                            <button
                                onClick={() => abandon(p.id)}
                                disabled={busy}
                                data-testid={`prof-abandon-${p.id}`}
                                className="stat-label text-destructive hover:text-destructive/70 flex items-center gap-1 disabled:opacity-40"
                                title="Abandon (keeps 25% xp for relearn)"
                            >
                                <X size={12} /> ABANDON
                            </button>
                        </div>
                    ))}
                </div>
            </div>

            {/* Full catalog */}
            <div className="border-t border-border pt-3">
                <div className="stat-label text-primary/70 mb-2">FULL CATALOG</div>
                {["gathering", "crafting", "service"].map((kind) => (
                    <div key={kind} className="mb-4">
                        <div className="font-pixel text-lg uppercase text-primary mb-1">{kind}</div>
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
                            {catalog.filter((p) => p.kind === kind).map((p) => {
                                const owned = mine.some((m) => m.id === p.id);
                                return (
                                    <div key={p.id} className="border border-border/60 p-3" data-testid={`prof-cat-${p.id}`}>
                                        <div className="flex justify-between items-baseline">
                                            <div className="font-pixel text-sm uppercase text-primary">{p.name}</div>
                                            {owned
                                                ? <div className="stat-label text-primary/80">· LEARNED</div>
                                                : (
                                                    <button
                                                        onClick={() => learn(p.id)}
                                                        disabled={busy || mine.length >= slots}
                                                        data-testid={`prof-learn-${p.id}`}
                                                        className="stat-label text-primary hover:text-primary/70 disabled:opacity-40"
                                                    >
                                                        LEARN →
                                                    </button>
                                                )}
                                        </div>
                                        <div className="text-xs text-muted-foreground mt-1">{p.desc}</div>
                                        {p.best_continents?.length > 0 && (
                                            <div className="stat-label text-primary/60 mt-1">Best in: {p.best_continents.join(", ")}</div>
                                        )}
                                    </div>
                                );
                            })}
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
}
