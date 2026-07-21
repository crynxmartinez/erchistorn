import { useEffect, useMemo, useState } from "react";
import { useNavigate } from "react-router-dom";
import { api, extractError } from "@/lib/api";
import { useAuth } from "@/contexts/AuthContext";
import { Input } from "@/components/ui/input";
import { toast } from "sonner";
import { Check, ChevronRight, ChevronLeft, Sparkles } from "lucide-react";

const BASE_STEPS = ["Race", "Role", "Mastery", "Origin", "Portrait", "Name", "Summary"];

const buildSteps = (raceId) => {
    if (raceId === "wildblood") return ["Race", "Role", "Mastery", "Origin", "Aspect", "Portrait", "Name", "Summary"];
    if (raceId === "hyliondrian") return ["Race", "Role", "Mastery", "Origin", "Adaptation", "Portrait", "Name", "Summary"];
    return BASE_STEPS;
};

export default function CharacterCreate() {
    const [step, setStep] = useState(0);
    const [races, setRaces] = useState([]);
    const [roles, setRoles] = useState([]);
    const [masteries, setMasteries] = useState([]);
    const [origins, setOrigins] = useState([]);
    const [portraits, setPortraits] = useState([]);
    const [beastAspects, setBeastAspects] = useState([]);
    const [marineAdaptations, setMarineAdaptations] = useState([]);
    const [busy, setBusy] = useState(false);
    const navigate = useNavigate();
    const { refresh } = useAuth();

    // selections
    const [race, setRace] = useState(null);
    const [role, setRole] = useState(null);
    const [mastery, setMastery] = useState(null);
    const [origin, setOrigin] = useState(null);
    const [portraitId, setPortraitId] = useState(null);
    const [name, setName] = useState("");
    const [oath, setOath] = useState("");
    const [heritage, setHeritage] = useState("");
    const [beastAspect, setBeastAspect] = useState(null);
    const [marineAdaptation, setMarineAdaptation] = useState(null);

    const STEPS = useMemo(() => buildSteps(race?.id), [race?.id]);
    const stepName = STEPS[step];

    useEffect(() => {
        (async () => {
            try {
                const [r, ro, m, p, o, ba, ma] = await Promise.all([
                    api.get("/game/data/races"),
                    api.get("/game/data/roles"),
                    api.get("/game/data/masteries"),
                    api.get("/game/data/portraits"),
                    api.get("/game/data/origins"),
                    api.get("/game/data/beast_aspects"),
                    api.get("/game/data/marine_adaptations"),
                ]);
                setRaces(r.data.races);
                setRoles(ro.data.roles);
                setMasteries(m.data.masteries);
                setPortraits(p.data.portraits);
                setOrigins(o.data.origins);
                setBeastAspects(ba.data.beast_aspects);
                setMarineAdaptations(ma.data.marine_adaptations);
            } catch (e) {
                toast.error(extractError(e));
            }
        })();
    }, []);

    const filteredRoles = useMemo(
        () => (race ? roles.filter((r) => race.roles.includes(r.id)) : roles),
        [race, roles],
    );
    const filteredMasteries = useMemo(() => {
        if (!role) return [];
        return masteries.filter((m) => role.available_masteries?.includes(m.id));
    }, [role, masteries]);
    const filteredOrigins = useMemo(
        () => (mastery ? origins.filter((o) => o.mastery === mastery.id) : []),
        [mastery, origins],
    );
    const filteredPortraits = useMemo(
        () => (race ? portraits.filter((p) => p.race === race.id) : portraits),
        [race, portraits],
    );

    // Live stat computation
    const finalStats = useMemo(() => {
        if (!race) return null;
        const base = {
            vitality: race.starting_stats.vitality,
            cognition: race.starting_stats.cognition,
            essence: race.starting_stats.essence,
            drive: race.starting_stats.drive,
            might: 0, grace: 0, insight: 0,
            armor_bonus: 0, evasion_mod: 0, attack_success_mod: 0,
        };
        if (role?.main_stats) {
            base.might += role.main_stats.might || 0;
            base.grace += role.main_stats.grace || 0;
            base.insight += role.main_stats.insight || 0;
        }
        if (mastery?.main_stats) {
            base.might += mastery.main_stats.might || 0;
            base.grace += mastery.main_stats.grace || 0;
            base.insight += mastery.main_stats.insight || 0;
        }
        if (origin) {
            for (const [k, v] of Object.entries(origin.bonus || {})) base[k] = (base[k] || 0) + v;
            for (const [k, v] of Object.entries(origin.drawback || {})) base[k] = (base[k] || 0) + v;
        }
        for (const k of ["vitality","cognition","essence","drive","might","grace","insight"]) {
            if (base[k] < 1) base[k] = 1;
        }
        return base;
    }, [race, role, mastery, origin]);

    const canNext = () => {
        switch (stepName) {
            case "Race":     return !!race;
            case "Role":     return !!role;
            case "Mastery":  return !!mastery;
            case "Origin":   return !!origin;
            case "Aspect":   return !!beastAspect;
            case "Adaptation": return !!marineAdaptation;
            case "Portrait": return !!portraitId;
            case "Name":
                if (!name.trim()) return false;
                if (race?.id === "human" && !oath.trim()) return false;
                if (race?.id === "half_elf" && !heritage) return false;
                return true;
            case "Summary":  return true;
            default:         return false;
        }
    };

    const submit = async () => {
        setBusy(true);
        try {
            await api.post("/game/character", {
                name: name.trim(),
                race: race.id,
                role: role.id,
                mastery: mastery.id,
                origin: origin.id,
                portrait_id: portraitId,
                oath: race.id === "human" ? oath.trim() : null,
                heritage: race.id === "half_elf" ? heritage : null,
                beast_aspect: race.id === "wildblood" ? beastAspect : null,
                marine_adaptation: race.id === "hyliondrian" ? marineAdaptation : null,
            });
            await refresh();
            toast.success("Your saga begins in Erchis!");
            navigate("/game");
        } catch (e) {
            toast.error(extractError(e));
        } finally {
            setBusy(false);
        }
    };

    // Reset dependent selections when parents change
    useEffect(() => {
        setRole(null); setMastery(null); setOrigin(null); setPortraitId(null);
        setBeastAspect(null); setMarineAdaptation(null);
        setStep(0);
    }, [race]);
    useEffect(() => { setMastery(null); setOrigin(null); }, [role]);
    useEffect(() => { setOrigin(null); }, [mastery]);

    return (
        <div className="min-h-screen p-4 md:p-8" data-testid="character-create-root">
            <div className="max-w-6xl mx-auto mb-6">
                <div className="stat-label text-primary/70 mb-3">CHARACTER FORGE · STEP {step + 1} OF {STEPS.length}</div>
                <div className="flex items-center gap-1 flex-wrap">
                    {STEPS.map((s, i) => (
                        <div key={s} className="flex items-center gap-1">
                            <div
                                data-testid={`step-indicator-${i}`}
                                className={`font-pixel text-sm uppercase px-2 py-1 border-2 ${
                                    i === step
                                        ? "bg-primary text-primary-foreground border-primary"
                                        : i < step
                                          ? "border-primary text-primary"
                                          : "border-border text-muted-foreground"
                                }`}
                            >
                                {i < step ? <Check size={12} /> : i + 1}. {s}
                            </div>
                            {i < STEPS.length - 1 && <ChevronRight className="text-border" size={12} />}
                        </div>
                    ))}
                </div>
            </div>

            <div className="max-w-6xl mx-auto grid grid-cols-1 lg:grid-cols-5 gap-6">
                {/* LEFT preview / detail */}
                <div className="lg:col-span-2 panel p-6 min-h-[520px]">
                    {stepName === "Race" && race ? <RaceDetail race={race} /> :
                     stepName === "Role" && role ? <RoleDetail role={role} /> :
                     stepName === "Mastery" && mastery ? <MasteryDetail mastery={mastery} /> :
                     stepName === "Origin" && origin ? <OriginDetail origin={origin} /> :
                     stepName === "Aspect" && beastAspect ? <AspectDetail aspect={beastAspects.find(a => a.id === beastAspect)} kind="beast" /> :
                     stepName === "Adaptation" && marineAdaptation ? <AspectDetail aspect={marineAdaptations.find(a => a.id === marineAdaptation)} kind="marine" /> :
                     stepName === "Portrait" && portraitId ? <PortraitPreview portrait={filteredPortraits.find(p => p.id === portraitId)} race={race} /> :
                     stepName === "Name" ? <IdentityPreview race={race} role={role} mastery={mastery} origin={origin} name={name} portraits={portraits} portraitId={portraitId} /> :
                     stepName === "Summary" ? <StatBreakdown race={race} role={role} mastery={mastery} origin={origin} stats={finalStats} /> :
                     <div className="stat-label text-muted-foreground">Make a selection to see details…</div>
                    }
                </div>

                {/* RIGHT selection */}
                <div className="lg:col-span-3 panel p-6">
                    {/* STEP — RACE */}
                    {stepName === "Race" && (
                        <div>
                            <h2 className="font-pixel text-3xl uppercase text-primary mb-4">Choose your Race</h2>
                            <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
                                {races.map((r) => (
                                    <button
                                        key={r.id}
                                        data-testid={`race-select-${r.id}`}
                                        onClick={() => setRace(r)}
                                        className={`press-btn p-3 text-left border-2 transition-colors ${
                                            race?.id === r.id
                                                ? "border-primary bg-primary/10"
                                                : "border-border hover:border-primary/60"
                                        }`}
                                    >
                                        <div className="font-pixel text-xl uppercase text-primary">{r.name}</div>
                                        <div className="stat-label mt-1 truncate">{r.perk.name}</div>
                                    </button>
                                ))}
                            </div>
                        </div>
                    )}

                    {/* STEP — ROLE */}
                    {stepName === "Role" && (
                        <div>
                            <h2 className="font-pixel text-3xl uppercase text-primary mb-2">Choose your Role</h2>
                            <div className="stat-label mb-4 text-muted-foreground">Roles recommended for {race?.name}s. Sets Main Stats.</div>
                            <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                                {filteredRoles.map((r) => (
                                    <button
                                        key={r.id}
                                        data-testid={`role-select-${r.id}`}
                                        onClick={() => setRole(r)}
                                        className={`press-btn p-4 text-left border-2 transition-colors ${
                                            role?.id === r.id ? "border-primary bg-primary/10" : "border-border hover:border-primary/60"
                                        }`}
                                    >
                                        <div className="font-pixel text-xl uppercase text-primary">{r.name}</div>
                                        <div className="text-xs text-muted-foreground mt-1">{r.desc}</div>
                                        <div className="stat-label mt-2 text-primary/80">
                                            MGT {r.main_stats?.might} · GRC {r.main_stats?.grace} · INS {r.main_stats?.insight}
                                        </div>
                                    </button>
                                ))}
                            </div>
                        </div>
                    )}

                    {/* STEP — MASTERY */}
                    {stepName === "Mastery" && (
                        <div>
                            <h2 className="font-pixel text-3xl uppercase text-primary mb-2">Choose your Mastery</h2>
                            <div className="stat-label mb-4 text-muted-foreground">Masteries available to {role?.name}s.</div>
                            {filteredMasteries.length === 0 && (
                                <div className="stat-label text-muted-foreground">No masteries. Try a different Role.</div>
                            )}
                            <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                                {filteredMasteries.map((m) => (
                                    <button
                                        key={m.id}
                                        data-testid={`mastery-select-${m.id}`}
                                        onClick={() => setMastery(m)}
                                        className={`press-btn p-4 text-left border-2 transition-colors ${
                                            mastery?.id === m.id ? "border-primary bg-primary/10" : "border-border hover:border-primary/60"
                                        }`}
                                    >
                                        <div className="font-pixel text-xl uppercase text-primary">{m.name}</div>
                                        <div className="text-xs text-muted-foreground mt-1">{m.desc}</div>
                                        <div className="stat-label mt-2 text-primary/80">
                                            +{m.main_stats?.might || 0} MGT · +{m.main_stats?.grace || 0} GRC · +{m.main_stats?.insight || 0} INS
                                        </div>
                                    </button>
                                ))}
                            </div>
                        </div>
                    )}

                    {/* STEP — ORIGIN */}
                    {stepName === "Origin" && (
                        <div>
                            <h2 className="font-pixel text-3xl uppercase text-primary mb-2">Choose your Origin</h2>
                            <div className="stat-label mb-4 text-muted-foreground">The constellation under which you were born. Bonus + Drawback.</div>
                            <div className="grid grid-cols-1 gap-3">
                                {filteredOrigins.map((o) => (
                                    <button
                                        key={o.id}
                                        data-testid={`origin-select-${o.id}`}
                                        onClick={() => setOrigin(o)}
                                        className={`press-btn p-4 text-left border-2 transition-colors ${
                                            origin?.id === o.id ? "border-primary bg-primary/10" : "border-border hover:border-primary/60"
                                        }`}
                                    >
                                        <div className="flex justify-between items-start">
                                            <div className="font-pixel text-xl uppercase text-primary">{o.name}</div>
                                            <Sparkles size={16} className="text-primary" />
                                        </div>
                                        <div className="narr text-xs text-muted-foreground mt-1">{o.story}</div>
                                        <div className="grid grid-cols-2 gap-3 mt-3 text-xs">
                                            <div>
                                                <div className="stat-label text-primary/70">BONUS</div>
                                                {Object.entries(o.bonus || {}).map(([k, v]) => (
                                                    <div key={k} className="font-mono text-primary">
                                                        +{v} {k.replace(/_/g, " ")}
                                                    </div>
                                                ))}
                                            </div>
                                            <div>
                                                <div className="stat-label text-destructive/70">DRAWBACK</div>
                                                {Object.entries(o.drawback || {}).map(([k, v]) => (
                                                    <div key={k} className="font-mono text-destructive">
                                                        {v} {k.replace(/_/g, " ")}
                                                    </div>
                                                ))}
                                            </div>
                                        </div>
                                    </button>
                                ))}
                            </div>
                        </div>
                    )}

                    {/* STEP — ASPECT (Wildblood only) */}
                    {stepName === "Aspect" && (
                        <div>
                            <h2 className="font-pixel text-3xl uppercase text-primary mb-2">Choose your Beast Aspect</h2>
                            <div className="stat-label mb-4 text-muted-foreground">
                                The animal spirit that walks in your blood. Shapes your instincts and combat gifts.
                            </div>
                            <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                                {beastAspects.map((a) => (
                                    <button
                                        key={a.id}
                                        data-testid={`beast-aspect-select-${a.id}`}
                                        onClick={() => setBeastAspect(a.id)}
                                        className={`press-btn p-4 text-left border-2 transition-colors ${
                                            beastAspect === a.id ? "border-primary bg-primary/10" : "border-border hover:border-primary/60"
                                        }`}
                                    >
                                        <div className="font-pixel text-xl uppercase text-primary">{a.name}</div>
                                        <div className="text-xs text-muted-foreground mt-1 italic">{a.examples}</div>
                                        <div className="stat-label mt-2 text-primary/80">{a.bonus_desc}</div>
                                    </button>
                                ))}
                            </div>
                        </div>
                    )}

                    {/* STEP — ADAPTATION (Hyliondrian only) */}
                    {stepName === "Adaptation" && (
                        <div>
                            <h2 className="font-pixel text-3xl uppercase text-primary mb-2">Choose your Marine Adaptation</h2>
                            <div className="stat-label mb-4 text-muted-foreground">
                                The lineage of the deep that shaped your gills, scales, and instincts.
                            </div>
                            <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                                {marineAdaptations.map((a) => (
                                    <button
                                        key={a.id}
                                        data-testid={`marine-adaptation-select-${a.id}`}
                                        onClick={() => setMarineAdaptation(a.id)}
                                        className={`press-btn p-4 text-left border-2 transition-colors ${
                                            marineAdaptation === a.id ? "border-primary bg-primary/10" : "border-border hover:border-primary/60"
                                        }`}
                                    >
                                        <div className="font-pixel text-xl uppercase text-primary">{a.name}</div>
                                        <div className="stat-label mt-2 text-primary/80">{a.bonus_desc}</div>
                                    </button>
                                ))}
                            </div>
                        </div>
                    )}

                    {/* STEP — PORTRAIT */}
                    {stepName === "Portrait" && (
                        <div>
                            <h2 className="font-pixel text-3xl uppercase text-primary mb-4">Choose your Portrait</h2>
                            <div className="grid grid-cols-3 md:grid-cols-5 gap-3">
                                {filteredPortraits.map((p) => (
                                    <button
                                        key={p.id}
                                        data-testid={`portrait-select-${p.id}`}
                                        onClick={() => setPortraitId(p.id)}
                                        className={`press-btn p-1 border-2 transition-colors ${
                                            portraitId === p.id ? "border-primary" : "border-border hover:border-primary/60"
                                        }`}
                                    >
                                        <img src={p.url} alt={p.seed} className="w-full aspect-square block bg-card" />
                                        <div className="stat-label text-center mt-1 truncate">{p.seed}</div>
                                    </button>
                                ))}
                            </div>
                        </div>
                    )}

                    {/* STEP — NAME / OATH / HERITAGE */}
                    {stepName === "Name" && (
                        <div className="space-y-6">
                            <h2 className="font-pixel text-3xl uppercase text-primary">Your Name in Erchis</h2>
                            <div>
                                <label className="stat-label block mb-1">Character Name</label>
                                <Input
                                    data-testid="char-name-input"
                                    value={name}
                                    onChange={(e) => setName(e.target.value)}
                                    placeholder="What shall the world call you?"
                                    className="bg-background border-border font-mono"
                                    maxLength={30}
                                />
                            </div>
                            {race?.id === "human" && (
                                <div>
                                    <label className="stat-label block mb-1">Sacred Oath</label>
                                    <div className="narr text-sm text-muted-foreground mb-2">
                                        A promise you carry through the world. Fulfilling it grants Oath Progress.
                                    </div>
                                    <Input
                                        data-testid="char-oath-input"
                                        value={oath}
                                        onChange={(e) => setOath(e.target.value)}
                                        placeholder='e.g. "I will avenge my fallen kingdom."'
                                        className="bg-background border-border font-mono"
                                        maxLength={120}
                                    />
                                </div>
                            )}
                            {race?.id === "half_elf" && (
                                <div>
                                    <label className="stat-label block mb-2">Dual Heritage — pick one</label>
                                    <div className="grid grid-cols-2 gap-3">
                                        {[
                                            { id: "human", label: "Human Heritage — Sacred Oath" },
                                            { id: "elf",   label: "Elven Heritage — Sun & Moon" },
                                        ].map((h) => (
                                            <button
                                                key={h.id}
                                                data-testid={`heritage-select-${h.id}`}
                                                onClick={() => setHeritage(h.id)}
                                                className={`press-btn p-3 text-left border-2 ${
                                                    heritage === h.id ? "border-primary bg-primary/10" : "border-border"
                                                }`}
                                            >
                                                <div className="font-pixel text-lg uppercase text-primary">{h.label}</div>
                                            </button>
                                        ))}
                                    </div>
                                </div>
                            )}
                        </div>
                    )}

                    {/* STEP — SUMMARY */}
                    {stepName === "Summary" && (
                        <div>
                            <h2 className="font-pixel text-3xl uppercase text-primary mb-4">Final Summary</h2>
                            <div className="space-y-4">
                                <SummaryRow label="RACE"     value={race?.name} />
                                <SummaryRow label="ROLE"     value={role?.name} />
                                <SummaryRow label="MASTERY"  value={mastery?.name} />
                                <SummaryRow label="ORIGIN"   value={origin?.name} />
                                <SummaryRow label="NAME"     value={name} />
                                {race?.id === "human" && oath && <SummaryRow label="OATH" value={`"${oath}"`} />}
                                {race?.id === "half_elf" && heritage && <SummaryRow label="HERITAGE" value={heritage} />}
                                {race?.id === "wildblood" && beastAspect && (
                                    <SummaryRow label="BEAST ASPECT" value={beastAspects.find(a => a.id === beastAspect)?.name} />
                                )}
                                {race?.id === "hyliondrian" && marineAdaptation && (
                                    <SummaryRow label="ADAPTATION" value={marineAdaptations.find(a => a.id === marineAdaptation)?.name} />
                                )}
                            </div>
                            <div className="border-t border-border mt-6 pt-4 stat-label text-muted-foreground">
                                Review the stat breakdown to the left. Confirm to enter Erchis.
                            </div>
                        </div>
                    )}

                    {/* nav */}
                    <div className="flex justify-between mt-8 pt-4 border-t border-border">
                        <button
                            data-testid="step-back"
                            onClick={() => setStep((s) => Math.max(0, s - 1))}
                            disabled={step === 0}
                            className="press-btn font-pixel text-lg uppercase px-4 py-2 border-2 border-border text-muted-foreground hover:border-primary hover:text-primary transition-colors disabled:opacity-40"
                        >
                            <ChevronLeft size={16} className="inline" /> Back
                        </button>
                        {step < STEPS.length - 1 ? (
                            <button
                                data-testid="step-next"
                                onClick={() => setStep((s) => s + 1)}
                                disabled={!canNext()}
                                className="press-btn font-pixel text-lg uppercase px-6 py-2 bg-primary text-primary-foreground border-2 border-primary hover:bg-transparent hover:text-primary transition-colors disabled:opacity-40 disabled:cursor-not-allowed"
                            >
                                Next <ChevronRight size={16} className="inline" />
                            </button>
                        ) : (
                            <button
                                data-testid="char-create-submit"
                                onClick={submit}
                                disabled={!canNext() || busy}
                                className="press-btn font-pixel text-lg uppercase px-6 py-2 bg-primary text-primary-foreground border-2 border-primary hover:bg-transparent hover:text-primary transition-colors disabled:opacity-40"
                                style={{ boxShadow: "3px 3px 0 0 hsl(var(--destructive))" }}
                            >
                                {busy ? "…" : "Confirm Character"}
                            </button>
                        )}
                    </div>
                </div>
            </div>
        </div>
    );
}

function SummaryRow({ label, value }) {
    return (
        <div className="flex justify-between border-b border-border/40 pb-2">
            <span className="stat-label">{label}</span>
            <span className="font-pixel text-lg uppercase text-primary">{value || "—"}</span>
        </div>
    );
}

function RaceDetail({ race }) {
    return (
        <div>
            <div className="stat-label text-primary/70 mb-2">RACE</div>
            <h3 className="font-pixel text-3xl uppercase text-primary mb-1">{race.name}</h3>
            <div className="stat-label text-muted-foreground mb-4">{race.title}</div>
            <div className="narr text-sm text-foreground/85 leading-relaxed mb-4">{race.story}</div>
            <div className="border-t border-border pt-3 mt-4">
                <div className="stat-label mb-1">RACIAL PERK — {race.perk.name}</div>
                <div className="text-sm text-foreground/80">{race.perk.desc}</div>
            </div>
            <div className="border-t border-border pt-3 mt-4">
                <div className="stat-label mb-2">LIFE STATS</div>
                <div className="grid grid-cols-2 gap-2 font-mono text-sm">
                    {Object.entries(race.starting_stats).map(([k, v]) => (
                        <div key={k} className="flex justify-between border-b border-border/50 pb-1">
                            <span className="uppercase text-muted-foreground">{k}</span>
                            <span className="text-primary">{v}</span>
                        </div>
                    ))}
                </div>
            </div>
        </div>
    );
}

function RoleDetail({ role }) {
    return (
        <div>
            <div className="stat-label text-primary/70 mb-2">ROLE</div>
            <h3 className="font-pixel text-3xl uppercase text-primary mb-2">{role.name}</h3>
            <div className="narr text-sm text-foreground/85 mb-4">{role.desc}</div>
            <div className="border-t border-border pt-3">
                <div className="stat-label mb-2">MAIN STATS (starting)</div>
                <div className="grid grid-cols-3 gap-2 font-mono text-sm">
                    <div className="text-center"><div className="stat-label">MIGHT</div><div className="text-primary text-xl">{role.main_stats?.might}</div></div>
                    <div className="text-center"><div className="stat-label">GRACE</div><div className="text-primary text-xl">{role.main_stats?.grace}</div></div>
                    <div className="text-center"><div className="stat-label">INSIGHT</div><div className="text-primary text-xl">{role.main_stats?.insight}</div></div>
                </div>
            </div>
        </div>
    );
}

function MasteryDetail({ mastery }) {
    return (
        <div>
            <div className="stat-label text-primary/70 mb-2">MASTERY</div>
            <h3 className="font-pixel text-3xl uppercase text-primary mb-2">{mastery.name}</h3>
            <div className="narr text-sm text-foreground/85 mb-4">{mastery.desc}</div>
            <div className="border-t border-border pt-3">
                <div className="stat-label mb-2">MAIN STATS BONUS</div>
                <div className="grid grid-cols-3 gap-2 font-mono text-sm">
                    <div className="text-center"><div className="stat-label">MIGHT</div><div className="text-primary text-xl">+{mastery.main_stats?.might || 0}</div></div>
                    <div className="text-center"><div className="stat-label">GRACE</div><div className="text-primary text-xl">+{mastery.main_stats?.grace || 0}</div></div>
                    <div className="text-center"><div className="stat-label">INSIGHT</div><div className="text-primary text-xl">+{mastery.main_stats?.insight || 0}</div></div>
                </div>
            </div>
            <div className="stat-label mt-3">
                Starting skills: {mastery.starting_skills?.map(s => s.replace(/_/g, ' ')).join(", ")}
            </div>
        </div>
    );
}

function OriginDetail({ origin }) {
    return (
        <div>
            <div className="stat-label text-primary/70 mb-2">ORIGIN · {origin.mythicode}</div>
            <h3 className="font-pixel text-3xl uppercase text-primary mb-2">{origin.name}</h3>
            <div className="narr text-sm text-foreground/85 mb-4">{origin.story}</div>
            <div className="stat-label text-primary/80 mb-3">BEST FOR: {origin.best_for}</div>
            <div className="grid grid-cols-2 gap-4 border-t border-border pt-4">
                <div>
                    <div className="stat-label text-primary/70 mb-2">BONUS</div>
                    {Object.entries(origin.bonus || {}).map(([k, v]) => (
                        <div key={k} className="font-mono text-primary text-sm">
                            +{v} {k.replace(/_/g, " ")}
                        </div>
                    ))}
                </div>
                <div>
                    <div className="stat-label text-destructive/70 mb-2">DRAWBACK</div>
                    {Object.entries(origin.drawback || {}).map(([k, v]) => (
                        <div key={k} className="font-mono text-destructive text-sm">
                            {v} {k.replace(/_/g, " ")}
                        </div>
                    ))}
                </div>
            </div>
        </div>
    );
}

function AspectDetail({ aspect, kind }) {
    if (!aspect) return null;
    return (
        <div>
            <div className="stat-label text-primary/70 mb-2">{kind === "beast" ? "BEAST ASPECT" : "MARINE ADAPTATION"}</div>
            <h3 className="font-pixel text-3xl uppercase text-primary mb-2">{aspect.name}</h3>
            {aspect.examples && (
                <div className="narr text-sm text-muted-foreground italic mb-4">Kin of {aspect.examples}</div>
            )}
            <div className="border-t border-border pt-3">
                <div className="stat-label mb-2">GIFTS OF THIS ASPECT</div>
                <div className="text-sm text-foreground/85 leading-relaxed">{aspect.bonus_desc}</div>
            </div>
            <div className="border-t border-border pt-3 mt-4 stat-label text-muted-foreground">
                {kind === "beast"
                    ? "Your Beast Aspect shapes how your Inner Blood surges when Exhaustion peaks."
                    : "Your Adaptation defines your bloodline's tide when standing in salt water."}
            </div>
        </div>
    );
}

function PortraitPreview({ portrait, race }) {
    if (!portrait) return null;
    return (
        <div>
            <div className="stat-label text-primary/70 mb-2">PORTRAIT</div>
            <img src={portrait.url} alt={portrait.seed} className="w-48 h-48 mx-auto border border-primary bg-card" />
            <div className="text-center mt-3 font-pixel text-2xl text-primary">{portrait.seed}</div>
            <div className="text-center stat-label">{race?.name}</div>
        </div>
    );
}

function IdentityPreview({ race, role, mastery, origin, name, portraits, portraitId }) {
    const p = portraits.find(x => x.id === portraitId);
    return (
        <div>
            <div className="stat-label text-primary/70 mb-2">YOUR CHARACTER</div>
            {p && <img src={p.url} alt={p.seed} className="w-40 h-40 mx-auto border border-primary bg-card mb-4" />}
            <h3 className="font-pixel text-3xl uppercase text-primary text-center">
                {name || "..."}
            </h3>
            <div className="text-center stat-label mt-2">
                {race?.name} · {role?.name} · {mastery?.name}
            </div>
            <div className="text-center stat-label text-primary/70 mt-1">{origin?.name}</div>
        </div>
    );
}

function StatBreakdown({ race, role, mastery, origin, stats }) {
    if (!stats) return null;
    const R = race?.starting_stats || {};
    const RO = role?.main_stats || {};
    const MA = mastery?.main_stats || {};
    const OB = origin?.bonus || {};
    const OD = origin?.drawback || {};

    const line = (key) => {
        const parts = [];
        if (R[key]) parts.push(`Race ${R[key]}`);
        if (RO[key]) parts.push(`Role ${RO[key]}`);
        if (MA[key]) parts.push(`Mastery +${MA[key]}`);
        if (OB[key]) parts.push(`Origin +${OB[key]}`);
        if (OD[key]) parts.push(`Origin ${OD[key]}`);
        return parts.join(" · ");
    };

    return (
        <div>
            <div className="stat-label text-primary/70 mb-2">FINAL STATS</div>
            <h3 className="font-pixel text-2xl uppercase text-primary mb-4">Stat Breakdown</h3>
            <div className="space-y-2 text-xs">
                {["vitality","cognition","essence","drive","might","grace","insight"].map((k) => (
                    <div key={k} className="border-b border-border/40 pb-1.5">
                        <div className="flex justify-between font-mono">
                            <span className="uppercase text-muted-foreground">{k}</span>
                            <span className="text-primary font-pixel text-lg" data-testid={`final-stat-${k}`}>{stats[k]}</span>
                        </div>
                        <div className="stat-label text-muted-foreground/80">{line(k) || "—"}</div>
                    </div>
                ))}
                <div className="border-b border-border/40 pb-1.5 pt-2">
                    <div className="flex justify-between font-mono">
                        <span className="uppercase text-muted-foreground">Armor bonus</span>
                        <span className="text-primary font-pixel" data-testid="final-armor">+{stats.armor_bonus}</span>
                    </div>
                </div>
                <div className="border-b border-border/40 pb-1.5">
                    <div className="flex justify-between font-mono">
                        <span className="uppercase text-muted-foreground">Evasion mod</span>
                        <span className={`font-pixel ${stats.evasion_mod < 0 ? "text-destructive" : "text-primary"}`} data-testid="final-evasion">
                            {stats.evasion_mod >= 0 ? "+" : ""}{stats.evasion_mod}
                        </span>
                    </div>
                </div>
            </div>
        </div>
    );
}
