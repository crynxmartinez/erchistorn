import { useEffect, useState } from "react";
import { api, extractError } from "@/lib/api";
import { toast } from "sonner";
import { Hammer, Sprout, Anchor, X, Wrench } from "lucide-react";

const CONTINENT_LABEL = {
    valeria: "Valeria", mushkara: "Mushkara", concordia: "Concordia", khardrum: "Khardrum",
    haya: "Haya", gennel: "Gennel", hylion: "Hylion", daw_ul_talalu: "Daw'ul Talalu",
    azurea: "Azurea", vael_turog: "Vael'Turog", orinth: "Orinth",
};
const prettifyContinents = (arr) => (arr || []).map((c) => CONTINENT_LABEL[c] || c).join(", ");

/**
 * ProfessionsPanel — Codex-tab-style view of the character's 3 profession slots
 * plus the full catalog. First slot at Lv 1, second at Lv 10, third at Lv 25.
 */
export default function ProfessionsPanel({ character, onChanged }) {
    const [catalog, setCatalog] = useState([]);
    const [ranks, setRanks] = useState([]);
    const [mine, setMine] = useState([]);
    const [tools, setTools] = useState([]);
    const [busy, setBusy] = useState(false);
    const currentTown = character?.current_town;

    const reload = async () => {
        try {
            const [c, m, t] = await Promise.all([
                api.get("/game/professions/catalog"),
                api.get("/game/professions/mine"),
                api.get("/game/tools"),
            ]);
            setCatalog(c.data.catalog);
            setRanks(c.data.ranks);
            setMine(m.data.professions);
            setTools(t.data.tools);
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
                    <h2 className="font-pixel text-3xl uppercase text-primary">Specialties</h2>
                <div className="narr text-sm text-muted-foreground mt-1">
                    Learn and rank up professions offered by this town's trade master.
                </div>
            </div>

            {/* Learned professions */}
            <div className="border-t border-border pt-3 mb-4">
                <div className="stat-label text-primary/70 mb-2">YOUR PROFESSIONS</div>
                {mine.length === 0 && <div className="stat-label text-muted-foreground">None yet. Pick one below.</div>}
                <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
                    {mine.map((p) => {
                        const tool = tools.find((t) => t.profession_id === p.id);
                        const rankIdx = ranks.findIndex((r) => r.id === p.rank);
                        const nextXp = rankIdx >= 0 && rankIdx < ranks.length - 1 ? ranks[rankIdx + 1].xp : null;
                        const prevXp = rankIdx > 0 ? ranks[rankIdx].xp : 0;
                        const pct = nextXp ? Math.min(100, Math.max(0, ((p.xp - prevXp) / (nextXp - prevXp)) * 100)) : 100;
                        return (
                            <div key={p.id} className="border border-border p-3 flex justify-between items-start" data-testid={`prof-active-${p.id}`}>
                                <div className="flex-1">
                                    <div className="font-pixel text-lg uppercase text-primary flex items-center gap-1.5">{kindIcon(p.kind)} {p.name}</div>
                                    <div className="stat-label text-muted-foreground">{p.rank.toUpperCase()} · {p.xp} xp</div>
                                    {nextXp && (
                                        <div className="mt-2">
                                            <div className="h-1.5 bg-background border border-border">
                                                <div className="h-full bg-primary" style={{ width: `${pct}%` }} />
                                            </div>
                                            <div className="text-[10px] text-muted-foreground mt-0.5">{nextXp - p.xp} xp to {ranks[rankIdx + 1]?.name}</div>
                                        </div>
                                    )}
                                    {tool && (
                                        <div className={`text-[10px] mt-1.5 flex items-center gap-1 ${tool.durability < tool.max_durability * 0.2 ? "text-destructive" : "text-muted-foreground"}`}>
                                            <Wrench size={10} /> {tool.tool_name}: {tool.durability}/{tool.max_durability}
                                        </div>
                                    )}
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
                        );
                    })}
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
                                const availableHere = !!currentTown;
                                return (
                                    <div key={p.id} className="border border-border/60 p-3" data-testid={`prof-cat-${p.id}`}>
                                        <div className="flex justify-between items-baseline">
                                            <div className="font-pixel text-sm uppercase text-primary">{p.name}</div>
                                            {owned
                                                ? <div className="stat-label text-primary/80">· LEARNED</div>
                                                : (
                                                    <button
                                                        onClick={() => learn(p.id)}
                                                        disabled={busy || !availableHere}
                                                        data-testid={`prof-learn-${p.id}`}
                                                        className="stat-label text-primary hover:text-primary/70 disabled:opacity-40"
                                                    >
                                                        {currentTown ? "LEARN →" : "IN TOWN"}
                                                    </button>
                                                )}
                                        </div>
                                        <div className="text-xs text-muted-foreground mt-1">{p.desc}</div>
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
