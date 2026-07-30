import { useMemo } from "react";

const GRID = 14;

const RARITY_PALETTE = {
    common:    { main: "#9ca3af", accent: "#d1d5db", dark: "#6b7280", highlight: "#f3f4f6" },
    uncommon:  { main: "#4ade80", accent: "#86efac", dark: "#16a34a", highlight: "#bbf7d0" },
    rare:      { main: "#60a5fa", accent: "#93c5fd", dark: "#2563eb", highlight: "#bfdbfe" },
    epic:      { main: "#c084fc", accent: "#d8b4fe", dark: "#9333ea", highlight: "#e9d5ff" },
    legendary: { main: "#fbbf24", accent: "#fcd34d", dark: "#d97706", highlight: "#fef3c7" },
    mythic:    { main: "#fb7185", accent: "#fda4af", dark: "#e11d48", highlight: "#fecdd3" },
    exotic:    { main: "#2dd4bf", accent: "#5eead4", dark: "#0d9488", highlight: "#99f6e4" },
};

const TYPE_PATTERNS = {
    weapon: [
        "......M......",
        "......M......",
        "......M......",
        "......M......",
        "......M......",
        "......M......",
        "......M......",
        "..DMMMMMMMMD.",
        "......D......",
        "......D......",
        "......D......",
        "...D.D.D.D...",
        ".............",
        ".............",
    ],
    armor: [
        "..MMMMMMM....",
        ".MAAAAAAAM...",
        "MAHHHHHHHAM..",
        "MAHHHHHHHAM..",
        "MAHHHHHHHAM..",
        ".MAAAAAAAM...",
        ".MAAAAAAAM...",
        "..MMMMMMM....",
        "...MMMMM.....",
        "....MMM......",
        ".....M.......",
        ".............",
        ".............",
        ".............",
    ],
    consumable: [
        "....AAA......",
        "....AAA......",
        "....AAA......",
        "..MMMMMMM....",
        ".MAAAAAAAM...",
        "MAHHHHHHHAM..",
        "MAHHHHHHHAM..",
        "MAHHHHHHHAM..",
        ".MAAAAAAAM...",
        "..MMMMM......",
        "...MMM.......",
        ".............",
        ".............",
        ".............",
    ],
    material: [
        "...MMM.......",
        "..MAAAM......",
        ".MAHHAAM.....",
        "MAHHHHAAM....",
        "MAHHHHHAAM...",
        ".MAHHHAAM....",
        "..MAHAAM.....",
        "...MAAM......",
        "....M........",
        ".............",
        ".............",
        ".............",
        ".............",
        ".............",
    ],
    skillbook: [
        ".DDDDDDDDD...",
        ".DAAAAAAAD...",
        ".DAHHHHHAD...",
        ".DAHHHHHAD...",
        ".DAHHHHHAD...",
        ".DAHHHHHAD...",
        ".DAHHHHHAD...",
        ".DAAAAAAAD...",
        ".DAAAAAAAD...",
        ".DDDDDDDDD...",
        ".............",
        ".............",
        ".............",
        ".............",
    ],
    relic: [
        "......M......",
        ".....HAM.....",
        "....HAHAM....",
        "...HAHHAHAM..",
        "..HAHHHHAHAM.",
        "...HAHHAHAM..",
        "....HAHAM....",
        ".....HAM.....",
        "......M......",
        ".............",
        ".............",
        ".............",
        ".............",
        ".............",
    ],
};

function hashStr(s) {
    let h = 0;
    for (let i = 0; i < s.length; i++) {
        h = ((h << 5) - h + s.charCodeAt(i)) | 0;
    }
    return Math.abs(h);
}

const TOOL_TYPES = {
    pickaxe: "weapon",
    herbalist_knife: "weapon",
    logging_axe: "weapon",
    hunting_bow: "weapon",
    fishing_rod: "weapon",
    excavator_brush: "relic",
};

function kindToType(def) {
    if (def.tool_id && TOOL_TYPES[def.tool_id]) return TOOL_TYPES[def.tool_id];
    if (def.kind === "weapon") return "weapon";
    if (def.kind === "armor") return "armor";
    if (def.kind === "trinket") return "relic";
    if (def.kind === "consumable") return "consumable";
    if (def.kind === "material") return "material";
    if (def.kind === "skillbook") return "skillbook";
    if (def.kind === "relic") return "relic";
    return "material";
}

export default function PixelSprite({ item, size = 48, className = "" }) {
    const sprite = useMemo(() => {
        const def = item?.def || item;
        const name = def?.name || def?.id || "unknown";
        const rarity = def?.rarity || "common";
        const type = kindToType(def);
        const palette = RARITY_PALETTE[rarity] || RARITY_PALETTE.common;
        const pattern = TYPE_PATTERNS[type] || TYPE_PATTERNS.material;
        const h = hashStr(name);

        const colorMap = {
            M: palette.main,
            A: palette.accent,
            D: palette.dark,
            H: palette.highlight,
        };

        const pixels = [];
        for (let row = 0; row < GRID; row++) {
            for (let col = 0; col < GRID; col++) {
                const ch = pattern[row]?.[col] || ".";
                if (ch === "." || ch === " ") continue;
                let color = colorMap[ch] || palette.main;

                if (ch === "H") {
                    const variant = h >> ((row + col) % 8) & 1;
                    if (variant) color = palette.accent;
                }

                pixels.push(
                    <rect
                        key={`${row}-${col}`}
                        x={col}
                        y={row}
                        width={1}
                        height={1}
                        fill={color}
                    />
                );
            }
        }

        const sparkles = (h % 4) + 1;
        for (let i = 0; i < sparkles; i++) {
            const sr = (h >> (i * 4)) % GRID;
            const sc = (h >> (i * 4 + 2)) % GRID;
            const baseCh = pattern[sr]?.[sc] || ".";
            if (baseCh === "." || baseCh === " ") {
                pixels.push(
                    <rect
                        key={`spark-${i}`}
                        x={sc}
                        y={sr}
                        width={1}
                        height={1}
                        fill={palette.highlight}
                        opacity={0.5}
                    />
                );
            }
        }

        return pixels;
    }, [item]);

    return (
        <svg
            viewBox={`0 0 ${GRID} ${GRID}`}
            width={size}
            height={size}
            className={className}
            style={{ imageRendering: "pixelated", shapeRendering: "crispEdges" }}
        >
            {sprite}
        </svg>
    );
}
