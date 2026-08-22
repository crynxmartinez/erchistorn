/**
 * The eleven masteries, as marketing content.
 *
 * Deliberately a content file rather than an API read. There is no
 * `/public/masteries` endpoint, and adding one would couple landing-page copy to
 * game-data internals — a page that has to rank wants a written hook and a
 * "plays like" line, not a `desc` field. `name`, `resource` and `skills` are taken
 * from `game_data.MASTERIES` so they are accurate; the framing is written for a
 * reader deciding what to play.
 *
 * These eleven pages are the highest-leverage SEO item in the plan: each one is a
 * real long-tail landing page for "<mastery> build" style queries, from copy that
 * mostly already existed in ../MASTERY_PLANS.md.
 */
export const MASTERIES = [
    {
        id: "knight",
        name: "Knight",
        tagline: "The Oathbound",
        resource: "Oath stacks",
        role: "Frontline tank",
        hook:
            "You swear an Oath before the first blow lands, and every turn you keep it makes you harder to kill.",
        desc:
            "Heavy armour, a shield, and a promise. The Knight commits to a sacred Oath at the start of a fight and grows stronger for as long as it holds — five Oaths, each rewriting what your stacks do.",
        plays:
            "Pick a fight you can survive and win it slowly. The Knight is the mastery that rewards patience.",
        skills: ["Shield Bash", "Iron Stance"],
    },
    {
        id: "paladin",
        name: "Paladin",
        tagline: "Oath and light",
        resource: "Faith",
        role: "Divine tank",
        hook: "The closer you are to death, the harder you hit.",
        desc:
            "A holy warrior whose Faith bar climbs as HP falls. At the lowest tier the Paladin is at their most dangerous, which makes every fight a question of how much you are willing to risk.",
        plays: "Deliberately uncomfortable. You have to let the fight get bad.",
        skills: ["Shield of Faith", "Blessed Strike"],
    },
    {
        id: "lancer",
        name: "Lancer",
        tagline: "The Elemental Lance Master",
        resource: "Elemental imbues",
        role: "Reach fighter",
        hook: "One weapon, five different fights depending on what you put into it.",
        desc:
            "The Lancer imbues their lance with an element, and each imbue changes what their strikes actually do — not just the damage number. Overload spends everything at once.",
        plays: "Read the enemy, then choose the element. Wrong choice, wasted turn.",
        skills: ["Thrust", "Flame Imbue"],
    },
    {
        id: "rogue",
        name: "Rogue",
        tagline: "The Adaptive Trickster",
        resource: "Innate slots",
        role: "Dirty fighter",
        hook: "You build the kit. The game does not hand it to you.",
        desc:
            "The Rogue customises their own passive loadout through innate skill slots, then fights with misdirection, traps and counters. Two Rogues at the same level can play nothing alike.",
        plays: "For people who read the whole skill list before choosing.",
        skills: ["Dirty Trick", "Hidden Blade"],
    },
    {
        id: "bard",
        name: "Bard",
        tagline: "The Master of Control",
        resource: "Crescendo",
        role: "Controller",
        hook: "In Song you change the rules. In Dance you change what the enemy does.",
        desc:
            "Two modes, switched mid-fight. Song rewrites the rules for your side; Dance takes the enemy's turn away from them. Crescendo builds as you perform and pays out at thresholds.",
        plays: "The mastery that wins fights it should have lost.",
        skills: ["Song of Heroes", "Mocking Verse"],
    },
    {
        id: "alchemist",
        name: "Alchemist",
        tagline: "The Transmuter",
        resource: "Combo Flow",
        role: "Close-range striker",
        hook: "Land strikes in sequence and the katar starts doing something else entirely.",
        desc:
            "A katar fighter who imbues skills directly onto the blade and accumulates Combo Flow with consecutive strikes. Break the chain and you start again from nothing.",
        plays: "Rhythm. Miss once and the whole turn structure resets.",
        skills: ["Acid Bomb", "Quick Jab"],
    },
    {
        id: "mage",
        name: "Mage",
        tagline: "Arcane fire, arcane cost",
        resource: "Arcane Library",
        role: "Burst caster",
        hook: "Everything is available. Almost nothing is affordable.",
        desc:
            "The Mage builds a library of spells across schools and pays for reach with fragility. Glass Cannon is not a warning label, it is a strategy.",
        plays: "High ceiling, thin floor. You will die to things a Knight ignores.",
        skills: ["Arcane Bolt", "Ward"],
    },
    {
        id: "priest",
        name: "Priest",
        tagline: "Hand of mercy",
        resource: "Sanctity",
        role: "Support and denial",
        hook: "You decide whether the enemy is allowed to heal.",
        desc:
            "Shield walls, delayed heals, heal-locks and smite. The Priest is the only mastery that can take an option away from the other side entirely.",
        plays: "Patient, defensive, and quietly the most controlling kit in the game.",
        skills: ["Divine Light", "Purge"],
    },
    {
        id: "druid",
        name: "Druid",
        tagline: "The wild answers",
        resource: "Summons and fusion",
        role: "Summoner",
        hook: "Tame something, then become it.",
        desc:
            "The Druid tames creatures from the bestiary, summons them to fight alongside, and can fuse with a summon to take on its abilities for a limited number of turns.",
        plays: "Two fights at once. You are managing a creature as well as yourself.",
        skills: ["Thornlash", "Beast Call"],
    },
    {
        id: "assassin",
        name: "Assassin",
        tagline: "The Shadow Reaper",
        resource: "Shadows",
        role: "Burst glass cannon",
        hook: "Shadows accumulate. At a hundred, something dies.",
        desc:
            "Every kill and every exchange feeds the shadow pool. Reaching the cap unleashes it all at once — and the Assassin has almost nothing to fall back on if the burst does not land.",
        plays: "All-in. The mastery with the least margin for a bad roll.",
        skills: ["Shadow Strike", "Smoke Veil"],
    },
    {
        id: "hunter",
        name: "Hunter",
        tagline: "The Master of Precision",
        resource: "Spirit Guidance",
        role: "Ranged killer",
        hook: "It is not the first shot that kills you. It is the tenth.",
        desc:
            "Spirit Guidance builds with every hit and transforms the Hunter's skills outright at ten stacks. Range control decides whether you ever get there.",
        plays: "Keep distance, stack, and do not get caught in melee.",
        skills: ["Rapid Shot", "Camouflage"],
    },
];

export const MASTERIES_BY_ID = Object.fromEntries(MASTERIES.map((m) => [m.id, m]));
