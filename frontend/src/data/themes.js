const CONTINENT_THEMES = {
    valeria: {
        primary: "46 65% 52%",
        accent: "46 65% 52%",
        background: "30 15% 4%",
        card: "30 12% 10%",
        border: "30 15% 20%",
        secondary: "30 14% 15%",
    },
    mushkara: {
        primary: "0 65% 45%",
        accent: "25 75% 45%",
        background: "0 12% 8%",
        card: "0 12% 12%",
        border: "0 20% 20%",
        secondary: "0 14% 15%",
    },
    concordia: {
        primary: "180 45% 55%",
        accent: "210 60% 65%",
        background: "210 15% 8%",
        card: "210 14% 12%",
        border: "210 20% 22%",
        secondary: "210 14% 15%",
    },
    khardrum: {
        primary: "30 60% 45%",
        accent: "35 70% 45%",
        background: "35 15% 8%",
        card: "35 14% 12%",
        border: "35 20% 22%",
        secondary: "35 14% 15%",
    },
    haya: {
        primary: "190 70% 60%",
        accent: "260 60% 70%",
        background: "240 20% 10%",
        card: "240 16% 14%",
        border: "240 20% 24%",
        secondary: "240 16% 15%",
    },
    gennel: {
        primary: "120 40% 45%",
        accent: "60 60% 45%",
        background: "60 15% 8%",
        card: "60 14% 12%",
        border: "60 20% 22%",
        secondary: "60 14% 15%",
    },
    hylion: {
        primary: "200 70% 55%",
        accent: "170 60% 55%",
        background: "210 30% 8%",
        card: "210 25% 12%",
        border: "210 30% 22%",
        secondary: "210 25% 15%",
    },
    daw_ul_talalu: {
        primary: "140 50% 50%",
        accent: "280 40% 55%",
        background: "140 20% 8%",
        card: "140 16% 12%",
        border: "140 20% 22%",
        secondary: "140 16% 15%",
    },
};

const BIOME_HUES = {
    golden_plains: 45,
    crownwood_forest: 120,
    imperial_riverlands: 200,
    ashen_border: 20,
    red_steppe: 0,
    iron_scar: 0,
    ash_barrens: 30,
    demonfall_crater: 280,
    mosaic_coast: 190,
    amber_vineyards: 45,
    silverroad: 210,
    diplomats_highlands: 220,
    granite_foothills: 35,
    ember_mines: 25,
    crystal_caverns: 260,
    deep_forges: 15,
    sunlit_canopy: 60,
    moonveil_woods: 220,
    celestial_lake: 200,
    starfall_cliffs: 270,
    blooming_desert: 40,
    beastwood: 90,
    roaring_savanna: 45,
    ancient_den: 35,
    coral_gardens: 330,
    kelp_forest: 160,
    storm_reefs: 210,
    abyssal_trench: 240,
    mistwood: 140,
    thorn_labyrinth: 320,
    lumina_grove: 150,
    elderroot_hollow: 120,
};

export function getThemeVars(continentId, biomeId) {
    const base = CONTINENT_THEMES[continentId] || { ...CONTINENT_THEMES.valeria };
    const hue = BIOME_HUES[biomeId];
    const override = hue
        ? {
              background: `${hue} 20% 8%`,
              card: `${hue} 16% 12%`,
              border: `${hue} 20% 22%`,
              accent: `${hue} 55% 55%`,
              secondary: `${hue} 16% 15%`,
          }
        : {};
    const merged = { ...base, ...override };
    const style = {};
    for (const [k, v] of Object.entries(merged)) {
        style[`--${k}`] = v;
    }
    return style;
}
