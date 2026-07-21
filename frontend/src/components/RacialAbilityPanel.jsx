import { useEffect, useState } from "react";
import { api, extractError } from "@/lib/api";
import { toast } from "sonner";
import { Zap } from "lucide-react";

/**
 * RacialAbilityPanel — surfaces the character's active racial cooldown abilities.
 * Currently supports: Human Adaptability Focus, Dwarf Field Repair, Orc Break-the-Chain.
 */
export default function RacialAbilityPanel({ character, onCharacterUpdate }) {
    const [state, setState] = useState({ race: null, abilities: [] });
    const [busy, setBusy] = useState(false);
    const [selectedFocus, setSelectedFocus] = useState("combat");

    const reload = async () => {
        try {
            const r = await api.get("/game/racial/status");
            setState(r.data);
        } catch (e) { toast.error(extractError(e)); }
    };
    useEffect(() => { reload(); }, [character?.race, character?.human_focus, character?.human_focus_last_used, character?.dwarf_field_repair_last_used, character?.orc_break_chain_last_used]);

    const use = async (ability_id, extra = {}) => {
        setBusy(true);
        try {
            const r = await api.post("/game/racial/ability", { ability_id, ...extra });
            toast.success(r.data.message);
            onCharacterUpdate?.(r.data.character);
            await reload();
        } catch (e) { toast.error(extractError(e)); }
        finally { setBusy(false); }
    };

    if (!state.abilities || state.abilities.length === 0) {
        return (
            <div className="stat-label text-muted-foreground italic" data-testid="racial-ability-panel-empty">
                No active racial abilities for your bloodline yet. More coming in a future season.
            </div>
        );
    }

    return (
        <div data-testid="racial-ability-panel">
            <div className="mb-3">
                <div className="stat-label text-primary/70">BLOODLINE ART</div>
                <div className="font-pixel text-2xl uppercase text-primary flex items-center gap-2">
                    <Zap size={16} strokeWidth={1.5} /> Racial Abilities
                </div>
            </div>
            <div className="space-y-3">
                {state.abilities.map((a) => {
                    const remaining = a.seconds_remaining || 0;
                    const mins = Math.floor(remaining / 60);
                    const secs = remaining % 60;
                    return (
                        <div key={a.id} className="border border-border p-3" data-testid={`racial-ability-${a.id}`}>
                            <div className="flex justify-between items-baseline">
                                <div className="font-pixel text-lg uppercase text-primary">{a.name}</div>
                                <div className="stat-label text-primary/70">CD: {a.cooldown_hours}h{a.cost ? ` · costs ${a.cost} ${a.cost_resource}` : ""}</div>
                            </div>
                            {!a.available && a.reason && (
                                <div className="stat-label text-destructive mt-1">
                                    {a.reason}{remaining > 0 ? ` · ${mins}m ${secs}s` : ""}
                                </div>
                            )}

                            {/* Human Focus special: choose one of 5 focuses */}
                            {a.id === "human_focus" && (
                                <>
                                    {a.current_focus && (
                                        <div className="stat-label text-primary/80 mt-1">
                                            Current: <span className="text-primary">{a.focuses[a.current_focus]?.name}</span>
                                        </div>
                                    )}
                                    <div className="grid grid-cols-1 md:grid-cols-2 gap-2 mt-2">
                                        {Object.entries(a.focuses || {}).map(([fid, f]) => (
                                            <button
                                                key={fid}
                                                onClick={() => { setSelectedFocus(fid); use("human_focus", { focus_id: fid }); }}
                                                disabled={busy || !a.available}
                                                data-testid={`human-focus-${fid}`}
                                                className={`press-btn text-left p-2 border-2 ${selectedFocus === fid ? "border-primary" : "border-border/60"} hover:border-primary disabled:opacity-40`}
                                            >
                                                <div className="font-pixel text-sm uppercase text-primary">{f.name}</div>
                                                <div className="text-xs text-muted-foreground">{f.desc}</div>
                                            </button>
                                        ))}
                                    </div>
                                </>
                            )}

                            {a.id === "dwarf_field_repair" && (
                                <button
                                    onClick={() => use("dwarf_field_repair")}
                                    disabled={busy || !a.available}
                                    data-testid="btn-dwarf-field-repair"
                                    className="press-btn font-pixel text-sm uppercase mt-2 px-3 py-1 border-2 border-primary text-primary hover:bg-primary hover:text-primary-foreground disabled:opacity-40"
                                >
                                    Field Repair
                                </button>
                            )}

                            {a.id === "orc_break_chain" && (
                                <button
                                    onClick={() => use("orc_break_chain")}
                                    disabled={busy || !a.available}
                                    data-testid="btn-orc-break-chain"
                                    className="press-btn font-pixel text-sm uppercase mt-2 px-3 py-1 border-2 border-primary text-primary hover:bg-primary hover:text-primary-foreground disabled:opacity-40"
                                >
                                    Break the Chain
                                </button>
                            )}
                        </div>
                    );
                })}
            </div>
        </div>
    );
}
