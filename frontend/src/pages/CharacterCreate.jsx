import { useEffect, useMemo, useState } from "react";
import { useNavigate } from "react-router-dom";
import { api, extractError } from "@/lib/api";
import { useAuth } from "@/contexts/AuthContext";
import { Input } from "@/components/ui/input";
import { toast } from "sonner";
import { Check, ChevronRight, ChevronLeft } from "lucide-react";

const STEPS = ["Race", "Role", "Mastery", "Portrait", "Name & Oath"];

export default function CharacterCreate() {
    const [step, setStep] = useState(0);
    const [races, setRaces] = useState([]);
    const [roles, setRoles] = useState([]);
    const [masteries, setMasteries] = useState([]);
    const [portraits, setPortraits] = useState([]);
    const [busy, setBusy] = useState(false);
    const navigate = useNavigate();
    const { refresh } = useAuth();

    // selections
    const [race, setRace] = useState(null);
    const [role, setRole] = useState(null);
    const [mastery, setMastery] = useState(null);
    const [portraitId, setPortraitId] = useState(null);
    const [name, setName] = useState("");
    const [oath, setOath] = useState("");
    const [heritage, setHeritage] = useState("");

    useEffect(() => {
        (async () => {
            try {
                const [r, ro, m, p] = await Promise.all([
                    api.get("/game/data/races"),
                    api.get("/game/data/roles"),
                    api.get("/game/data/masteries"),
                    api.get("/game/data/portraits"),
                ]);
                setRaces(r.data.races);
                setRoles(ro.data.roles);
                setMasteries(m.data.masteries);
                setPortraits(p.data.portraits);
            } catch (e) {
                toast.error(extractError(e));
            }
        })();
    }, []);

    const filteredRoles = useMemo(
        () => (race ? roles.filter((r) => race.roles.includes(r.id)) : roles),
        [race, roles],
    );
    const filteredMasteries = useMemo(
        () => (race ? masteries.filter((m) => race.masteries.includes(m.id)) : masteries),
        [race, masteries],
    );
    const filteredPortraits = useMemo(
        () => (race ? portraits.filter((p) => p.race === race.id) : portraits),
        [race, portraits],
    );

    const canNext = () => {
        if (step === 0) return !!race;
        if (step === 1) return !!role;
        if (step === 2) return !!mastery;
        if (step === 3) return !!portraitId;
        if (step === 4) {
            if (!name.trim()) return false;
            if (race?.id === "human" && !oath.trim()) return false;
            if (race?.id === "half_elf" && !heritage) return false;
            return true;
        }
        return false;
    };

    const submit = async () => {
        setBusy(true);
        try {
            await api.post("/game/character", {
                name: name.trim(),
                race: race.id,
                role: role.id,
                mastery: mastery.id,
                portrait_id: portraitId,
                oath: race.id === "human" ? oath.trim() : null,
                heritage: race.id === "half_elf" ? heritage : null,
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

    return (
        <div className="min-h-screen p-4 md:p-8" data-testid="character-create-root">
            {/* stepper */}
            <div className="max-w-6xl mx-auto mb-8">
                <div className="stat-label text-primary/70 mb-3">CHARACTER FORGE · STEP {step + 1} OF {STEPS.length}</div>
                <div className="flex items-center gap-2 flex-wrap">
                    {STEPS.map((s, i) => (
                        <div key={s} className="flex items-center gap-2">
                            <div
                                data-testid={`step-indicator-${i}`}
                                className={`font-pixel text-lg uppercase px-3 py-1 border-2 ${
                                    i === step
                                        ? "bg-primary text-primary-foreground border-primary"
                                        : i < step
                                          ? "border-primary text-primary"
                                          : "border-border text-muted-foreground"
                                }`}
                            >
                                {i < step ? <Check size={16} /> : i + 1}. {s}
                            </div>
                            {i < STEPS.length - 1 && (
                                <ChevronRight className="text-border" size={16} />
                            )}
                        </div>
                    ))}
                </div>
            </div>

            <div className="max-w-6xl mx-auto grid grid-cols-1 lg:grid-cols-5 gap-6">
                {/* LEFT: Selection lore preview */}
                <div className="lg:col-span-2 panel p-6 min-h-[420px]">
                    {step === 0 && race ? (
                        <RaceDetail race={race} />
                    ) : step === 1 && role ? (
                        <SimpleDetail title={role.name} tag="ROLE" desc={role.desc} />
                    ) : step === 2 && mastery ? (
                        <SimpleDetail title={mastery.name} tag="MASTERY" desc={mastery.desc} />
                    ) : step === 3 && portraitId ? (
                        <PortraitPreview portrait={filteredPortraits.find(p => p.id === portraitId)} race={race} />
                    ) : step === 4 ? (
                        <IdentityPreview race={race} role={role} mastery={mastery} name={name} portraits={portraits} portraitId={portraitId} />
                    ) : (
                        <div className="stat-label text-muted-foreground">Make a selection to see details…</div>
                    )}
                </div>

                {/* RIGHT: Selection grid */}
                <div className="lg:col-span-3 panel p-6">
                    {step === 0 && (
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

                    {step === 1 && (
                        <div>
                            <h2 className="font-pixel text-3xl uppercase text-primary mb-2">Choose your Role</h2>
                            <div className="stat-label mb-4 text-muted-foreground">Only roles suited to {race?.name}s.</div>
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
                                    </button>
                                ))}
                            </div>
                        </div>
                    )}

                    {step === 2 && (
                        <div>
                            <h2 className="font-pixel text-3xl uppercase text-primary mb-2">Choose your Mastery</h2>
                            <div className="stat-label mb-4 text-muted-foreground">Only masteries recommended for {race?.name}s.</div>
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
                                        <div className="stat-label mt-2">
                                            Skills: {m.starting_skills.map(s => s.replace(/_/g, ' ')).join(", ")}
                                        </div>
                                    </button>
                                ))}
                            </div>
                        </div>
                    )}

                    {step === 3 && (
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

                    {step === 4 && (
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
                                        A promise you carry through the world. Fulfilling it restores Drive.
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
                                {busy ? "…" : "Enter Erchis"}
                            </button>
                        )}
                    </div>
                </div>
            </div>
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
                <div className="stat-label mb-2">STARTING STATS</div>
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

function SimpleDetail({ title, tag, desc }) {
    return (
        <div>
            <div className="stat-label text-primary/70 mb-2">{tag}</div>
            <h3 className="font-pixel text-3xl uppercase text-primary mb-2">{title}</h3>
            <div className="narr text-sm text-foreground/85">{desc}</div>
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

function IdentityPreview({ race, role, mastery, name, portraits, portraitId }) {
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
        </div>
    );
}
