import SiteLayout from "@/components/SiteLayout";
import { Dices, Swords, Hammer, Users, TrendingUp, Zap } from "lucide-react";

const SECTIONS = [
    {
        icon: Dices,
        title: "The D6 Fate System",
        body: "Every action — attacking, crafting, gathering, fleeing — is resolved by a single six-sided die. Your stats shift the target number, not the outcome count. Six faces, each with its own narrative: Critical Success, Success, Partial Success, Failure, Critical Failure, and Catastrophe. Over 20 unique narrative strings per outcome, so no two rolls feel the same.",
        points: ["Stats modify the target, not the die", "6 outcomes with 20+ narratives each", "Higher stats = better odds, never guarantees"],
    },
    {
        icon: Swords,
        title: "Turn-Based Combat",
        body: "Combat is automatic but tactical. Your character auto-selects skills based on situation, but you can manually override when the stakes are high. Skills trigger item effects, status applications, and dice rolls. Enemies use the same system — fair, brutal, and readable.",
        points: ["Auto-skill selection with manual override", "Status effects: bleed, poison, stun, bless, focus, more", "Items trigger automatically in combat"],
    },
    {
        icon: Hammer,
        title: "Crafting & Rarity",
        body: "Gather materials from biomes across all 11 continents. Six rarity tiers from Common to Mythic. Recipes are continent-specific — craft in towns, queue multiple items, and discover rare recipes from skillbooks and teachers.",
        points: ["6 rarity tiers: Common → Mythic", "Continent-specific recipes", "Crafting queue with timers"],
    },
    {
        icon: Users,
        title: "Guilds & Hall Buffs",
        body: "Found a guild for 5,000g or join an existing one. Recruit 3+ members to unlock the Guild Hall, where the Grandmaster can spend treasury gold on server-wide buffs for all members: combat XP, crafting success, gather yield, trade profit, and expedition speed.",
        points: ["Found or join guilds (max 30 members)", "Hall unlocks at 3+ members", "5 purchasable buffs, 24h duration, treasury-funded"],
    },
    {
        icon: TrendingUp,
        title: "Progression",
        body: "Level up through combat, crafting, and exploration. Each level raises your mastery's signature stats. Learn skills from wandering teachers or rare skillbook drops. Masteries define your playstyle — Knight, Mage, Rogue, Druid, and more.",
        points: ["Mastery-based stat growth per level", "Skillbooks drop from monsters", "Teachers in towns teach rare skills"],
    },
    {
        icon: Zap,
        title: "Status Effects",
        body: "Over 15 status effects split between buffs and debuffs. Bleeding, poisoned, burning, stunned, ensnared on the dark side. Blessed, focused, warded, hidden, evasive on the light. Each has a description, effect, and type — all visible in your Journal Codex.",
        points: ["10+ debuffs: bleed, poison, burn, stun, blind, more", "5+ buffs: bless, focus, ward, hide, evade", "Durations tick per action, not per turn"],
    },
];

export default function Mechanics() {
    return (
        <SiteLayout>
            {/* Hero */}
            <section className="relative px-6 md:px-16 py-20 border-b border-border overflow-hidden">
                <div className="absolute inset-0 opacity-15" style={{
                    backgroundImage: "url(https://images.unsplash.com/photo-1605806616949-1e87b487cb2a?q=80&w=2000&auto=format&fit=crop)",
                    backgroundSize: "cover", backgroundPosition: "center",
                }} />
                <div className="relative max-w-4xl">
                    <div className="stat-label text-primary/70 mb-2 flex items-center gap-2"><Swords size={14} /> MECHANICS</div>
                    <h1 className="font-pixel text-4xl md:text-6xl uppercase text-primary tracking-wider mb-4">How Erchis Works</h1>
                    <p className="narr text-lg md:text-xl text-muted-foreground max-w-2xl">
                        A dice-driven RPG where stats tilt the odds, gear opens new paths, and the story between rolls is yours to write.
                    </p>
                </div>
            </section>

            <div className="max-w-4xl mx-auto px-4 md:px-6 py-12">
                <div className="space-y-12">
                    {SECTIONS.map((s, i) => {
                        const Ic = s.icon;
                        return (
                            <section key={i} className="panel p-6 md:p-8">
                                <div className="flex items-center gap-3 mb-4">
                                    <Ic size={28} className="text-primary" />
                                    <h2 className="font-pixel text-2xl uppercase text-primary tracking-wider">{s.title}</h2>
                                </div>
                                <p className="narr text-sm text-foreground/85 leading-relaxed mb-4">{s.body}</p>
                                <ul className="space-y-1.5">
                                    {s.points.map((p, j) => (
                                        <li key={j} className="text-sm text-muted-foreground flex items-start gap-2">
                                            <span className="text-primary mt-0.5">▸</span> {p}
                                        </li>
                                    ))}
                                </ul>
                            </section>
                        );
                    })}
                </div>
            </div>
        </SiteLayout>
    );
}
