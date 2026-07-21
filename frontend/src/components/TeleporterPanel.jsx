import { useEffect, useState } from "react";
import { api, extractError } from "@/lib/api";
import { toast } from "sonner";
import { Sparkles, ArrowRight, Coins } from "lucide-react";

/**
 * TeleporterPanel — inline Grand Teleporter interface.
 * Shows the 8 accessible continents + hometowns, fee, cooldown timer.
 */
export default function TeleporterPanel({ character, onTraveled }) {
    const [dests, setDests] = useState([]);
    const [meta, setMeta] = useState({ cooldown_secs: 600, fee_base: 100 });
    const [busy, setBusy] = useState(false);
    const [cdText, setCdText] = useState("");

    useEffect(() => {
        (async () => {
            try {
                const r = await api.get("/game/teleporter/destinations");
                setDests(r.data.destinations);
                setMeta({ cooldown_secs: r.data.cooldown_secs, fee_base: r.data.fee_base });
            } catch (e) { toast.error(extractError(e)); }
        })();
    }, [character?.current_continent, character?.gold]);

    useEffect(() => {
        const t = setInterval(() => {
            if (!character?.teleporter_last_used) { setCdText(""); return; }
            const last = new Date(character.teleporter_last_used).getTime();
            const secs = Math.max(0, meta.cooldown_secs - Math.floor((Date.now() - last) / 1000));
            if (secs <= 0) setCdText("");
            else setCdText(`${Math.floor(secs / 60)}m ${secs % 60}s`);
        }, 1000);
        return () => clearInterval(t);
    }, [character?.teleporter_last_used, meta.cooldown_secs]);

    const travel = async (continentId) => {
        setBusy(true);
        try {
            const r = await api.post("/game/teleporter/travel", { continent_id: continentId });
            toast.success(r.data.narrative || "The world folds.");
            onTraveled?.(r.data.character);
        } catch (e) { toast.error(extractError(e)); }
        finally { setBusy(false); }
    };

    return (
        <div data-testid="teleporter-panel">
            <div className="mb-4">
                <div className="stat-label text-primary/70">A HUB THAT SPANS ERCHIS</div>
                <h2 className="font-pixel text-3xl uppercase text-primary">The Grand Teleporter</h2>
                <div className="narr text-sm text-muted-foreground mt-1">
                    A ring of sun-warmed stones, thrumming quiet. Choose a continent; step through; be somewhere new.
                </div>
                <div className="stat-label mt-2 text-primary/80 flex items-center gap-3">
                    <span>FEE: <Coins size={10} className="inline text-primary" /> {meta.fee_base}g / hop</span>
                    <span>·</span>
                    <span>COOLDOWN: {Math.floor(meta.cooldown_secs / 60)}m</span>
                    {cdText && <span className="text-destructive">· recharging {cdText}</span>}
                </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                {dests.map((d) => (
                    <button
                        key={d.continent_id}
                        data-testid={`teleporter-dest-${d.continent_id}`}
                        disabled={busy || d.is_current || !!cdText || (character?.gold ?? 0) < d.fee}
                        onClick={() => travel(d.continent_id)}
                        className={`press-btn p-3 text-left border-2 transition-colors flex items-center justify-between ${
                            d.is_current
                                ? "border-primary/40 bg-primary/5 text-muted-foreground cursor-default"
                                : "border-border hover:border-primary text-foreground hover:text-primary disabled:opacity-40 disabled:hover:border-border disabled:hover:text-foreground disabled:cursor-not-allowed"
                        }`}
                    >
                        <div>
                            <div className="font-pixel text-lg uppercase">{d.continent_name}</div>
                            <div className="stat-label text-muted-foreground">Arrive at {d.hometown_name}</div>
                        </div>
                        <div className="stat-label text-primary flex items-center gap-1">
                            {d.is_current ? "· HERE ·" : (
                                <>
                                    <Coins size={10} /> {d.fee}g <ArrowRight size={12} />
                                </>
                            )}
                        </div>
                    </button>
                ))}
            </div>

            <div className="stat-label text-muted-foreground mt-4 italic flex items-center gap-1">
                <Sparkles size={10} className="text-primary" /> You always arrive at a continent&apos;s main hometown. From there, walk or use a Waystone.
            </div>
        </div>
    );
}
