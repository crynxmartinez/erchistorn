import { Heart, Zap, Coins, Star } from "lucide-react";
import RacialPanel from "@/components/RacialPanel";

export default function CharacterSheet({ character, portraits, race, role, mastery, itemsById, timeOfDay }) {
    if (!character) return null;
    const portrait = portraits?.find((p) => p.id === character.portrait_id);
    const hpPct = Math.round((character.hp / Math.max(1, character.max_hp)) * 100);
    const xpNext = 100 + (character.level - 1) * 40;
    const xpPct = Math.round((character.xp / xpNext) * 100);
    const weaponItem = character.equipped?.weapon ? itemsById?.[character.equipped.weapon] : null;
    const armorItem = character.equipped?.armor ? itemsById?.[character.equipped.armor] : null;

    return (
        <div className="panel p-4 space-y-4" data-testid="character-sheet">
            <div className="flex gap-3">
                {portrait ? (
                    <img
                        src={portrait.url}
                        alt={character.name}
                        className="w-20 h-20 border border-primary bg-card"
                        data-testid="char-portrait"
                    />
                ) : (
                    <div className="sprite-slot w-20 h-20">?</div>
                )}
                <div className="min-w-0 flex-1">
                    <div className="font-pixel text-xl uppercase text-primary truncate" data-testid="char-name">
                        {character.name}
                    </div>
                    <div className="stat-label truncate">
                        {race?.name} · {role?.name}
                    </div>
                    <div className="stat-label truncate text-muted-foreground">{mastery?.name}</div>
                    <div className="flex items-center gap-1 mt-1 stat-label">
                        <Star size={10} className="text-primary" /> LVL {character.level}
                    </div>
                </div>
            </div>

            {/* HP bar */}
            <div>
                <div className="flex justify-between stat-label mb-1">
                    <span className="flex items-center gap-1"><Heart size={10} className="text-destructive" /> HP</span>
                    <span className="text-foreground" data-testid="hp-numeric">
                        {character.hp}/{character.max_hp}
                    </span>
                </div>
                <div className="h-3 bg-background border border-border relative">
                    <div className="h-full bg-destructive transition-all" style={{ width: `${hpPct}%` }} />
                </div>
            </div>

            {/* XP bar */}
            <div>
                <div className="flex justify-between stat-label mb-1">
                    <span className="flex items-center gap-1"><Zap size={10} className="text-primary" /> XP</span>
                    <span className="text-foreground">{character.xp}/{xpNext}</span>
                </div>
                <div className="h-2 bg-background border border-border relative">
                    <div className="h-full bg-primary transition-all" style={{ width: `${xpPct}%` }} />
                </div>
            </div>

            {/* Gold */}
            <div className="flex justify-between items-center stat-label">
                <span className="flex items-center gap-1"><Coins size={12} className="text-primary" /> GOLD</span>
                <span className="text-primary font-mono" data-testid="char-gold">{character.gold}</span>
            </div>

            {/* Stats */}
            <div className="border-t border-border pt-3">
                <div className="stat-label mb-2">MAIN STATS</div>
                <div className="grid grid-cols-3 gap-1 font-mono text-xs">
                    {["might", "grace", "insight"].map((k) => (
                        <div key={k} className="text-center border-b border-border/40 pb-1">
                            <div className="stat-label">{k.slice(0, 3).toUpperCase()}</div>
                            <div className="text-primary text-lg">{character.stats?.[k] ?? 0}</div>
                        </div>
                    ))}
                </div>
                <div className="stat-label mt-3 mb-2">LIFE STATS</div>
                <div className="grid grid-cols-2 gap-1 font-mono text-xs">
                    {["vitality", "cognition", "essence", "drive"].map((k) => (
                        <div key={k} className="flex justify-between border-b border-border/40 pb-0.5">
                            <span className="text-muted-foreground uppercase">{k.slice(0, 3)}</span>
                            <span className="text-primary">{character.stats?.[k] ?? 0}</span>
                        </div>
                    ))}
                </div>
                {(character.stats?.armor_bonus || character.stats?.evasion_mod) ? (
                    <div className="grid grid-cols-2 gap-1 font-mono text-xs mt-2">
                        {character.stats?.armor_bonus ? (
                            <div className="flex justify-between border-b border-border/40 pb-0.5">
                                <span className="text-muted-foreground">ARMOR+</span>
                                <span className="text-primary">+{character.stats.armor_bonus}</span>
                            </div>
                        ) : null}
                        {character.stats?.evasion_mod ? (
                            <div className="flex justify-between border-b border-border/40 pb-0.5">
                                <span className="text-muted-foreground">EVA</span>
                                <span className={character.stats.evasion_mod < 0 ? "text-destructive" : "text-primary"}>
                                    {character.stats.evasion_mod >= 0 ? "+" : ""}{character.stats.evasion_mod}
                                </span>
                            </div>
                        ) : null}
                    </div>
                ) : null}
            </div>

            {/* Equipped */}
            <div className="border-t border-border pt-3">
                <div className="stat-label mb-2">EQUIPPED</div>
                <div className="space-y-1 text-xs font-mono">
                    <div className="flex justify-between">
                        <span className="text-muted-foreground">WPN</span>
                        <span className="text-foreground">{weaponItem?.name || "—"}</span>
                    </div>
                    <div className="flex justify-between">
                        <span className="text-muted-foreground">ARM</span>
                        <span className="text-foreground">{armorItem?.name || "—"}</span>
                    </div>
                </div>
            </div>

            {/* Statuses */}
            {(character.statuses || []).length > 0 && (
                <div className="border-t border-border pt-3">
                    <div className="stat-label mb-2">STATUS</div>
                    <div className="flex flex-wrap gap-1">
                        {character.statuses.map((s, i) => (
                            <span
                                key={`${s.id}-${i}`}
                                data-testid={`status-${s.id}`}
                                className={`stat-label px-2 py-0.5 border ${
                                    s.kind === "buff"
                                        ? "border-primary text-primary"
                                        : "border-destructive text-destructive"
                                }`}
                            >
                                {s.name}
                            </span>
                        ))}
                    </div>
                </div>
            )}

            {character.oath && (
                <div className="border-t border-border pt-3">
                    <div className="stat-label mb-1">SACRED OATH</div>
                    <div className="narr text-xs text-foreground/85">&ldquo;{character.oath}&rdquo;</div>
                </div>
            )}

            <RacialPanel character={character} timeOfDay={timeOfDay} />
        </div>
    );
}
