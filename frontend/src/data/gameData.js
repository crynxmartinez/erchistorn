import { useEffect, useState } from "react";
import { api } from "@/lib/api";

/** Global loader for mostly-static game reference data. */
export function useGameData() {
    const [data, setData] = useState({ ready: false });

    useEffect(() => {
        let mounted = true;
        (async () => {
            try {
                const [races, roles, masteries, portraits, continents, items, skills, recipes, teachers, monsters] =
                    await Promise.all([
                        api.get("/game/data/races"),
                        api.get("/game/data/roles"),
                        api.get("/game/data/masteries"),
                        api.get("/game/data/portraits"),
                        api.get("/game/data/continents"),
                        api.get("/game/data/items"),
                        api.get("/game/data/skills"),
                        api.get("/game/data/recipes"),
                        api.get("/game/data/teachers"),
                        api.get("/game/data/monsters"),
                    ]);
                if (!mounted) return;
                const itemsList = items.data.items;
                const skillsList = skills.data.skills;
                setData({
                    ready: true,
                    races: races.data.races,
                    roles: roles.data.roles,
                    masteries: masteries.data.masteries,
                    portraits: portraits.data.portraits,
                    continents: continents.data.continents,
                    items: itemsList,
                    itemsById: Object.fromEntries(itemsList.map((i) => [i.id, i])),
                    skills: skillsList,
                    skillsById: Object.fromEntries(skillsList.map((s) => [s.id, s])),
                    recipes: recipes.data.recipes,
                    teachers: teachers.data.teachers,
                    monsters: monsters.data.monsters,
                });
            } catch {
                if (mounted) setData({ ready: false, error: true });
            }
        })();
        return () => { mounted = false; };
    }, []);

    return data;
}

export const RARITY_LABEL = {
    common: "Common",
    uncommon: "Uncommon",
    rare: "Rare",
    epic: "Epic",
    legendary: "Legendary",
    mythic: "Mythic",
};

export const RARITY_CLASS = {
    common: "rarity-common",
    uncommon: "rarity-uncommon",
    rare: "rarity-rare",
    epic: "rarity-epic",
    legendary: "rarity-legendary",
    mythic: "rarity-mythic",
};

export const RARITY_TEXT = {
    common: "text-rarity-common",
    uncommon: "text-rarity-uncommon",
    rare: "text-rarity-rare",
    epic: "text-rarity-epic",
    legendary: "text-rarity-legendary",
    mythic: "text-rarity-mythic",
};
