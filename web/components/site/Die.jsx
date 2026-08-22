"use client";

import { useEffect, useRef, useState } from "react";

/**
 * A d6 that rolls once on mount and settles.
 *
 * The weighted six-sided die is the game's central mechanic, so it doubles as the
 * logo and as the hero's only piece of "art" — no asset pipeline required. Pips
 * are squares, not circles, to match the site's global `border-radius: 0`.
 *
 * Honours `prefers-reduced-motion`: those users get the settled face immediately
 * with no tumble.
 */

// Which pip positions light up for each face. Grid is 3x3, indices 0-8.
const FACES = {
    1: [4],
    2: [0, 8],
    3: [0, 4, 8],
    4: [0, 2, 6, 8],
    5: [0, 2, 4, 6, 8],
    6: [0, 2, 3, 5, 6, 8],
};

export default function Die({ size = 240, face = 6, roll = true, className = "" }) {
    const reduced =
        typeof window !== "undefined" &&
        window.matchMedia?.("(prefers-reduced-motion: reduce)").matches;

    const [shown, setShown] = useState(reduced || !roll ? face : 1);
    const [tumbling, setTumbling] = useState(roll && !reduced);
    const timer = useRef(null);

    useEffect(() => {
        if (reduced || !roll) return;
        let ticks = 0;
        // Decelerating roll: fast at first, slowing into the settle.
        const step = () => {
            ticks += 1;
            setShown(1 + Math.floor(Math.random() * 6));
            if (ticks < 14) {
                timer.current = setTimeout(step, 60 + ticks * 18);
            } else {
                setShown(face);
                setTumbling(false);
            }
        };
        timer.current = setTimeout(step, 220);
        return () => clearTimeout(timer.current);
    }, [face, roll, reduced]);

    const pips = FACES[shown] || FACES[6];
    const unit = 100 / 3;

    return (
        <svg
            viewBox="0 0 100 100"
            width={size}
            height={size}
            className={`${className} ${tumbling ? "animate-die-tumble" : ""}`}
            role="img"
            aria-label={`Six-sided die showing ${shown}`}
            style={{ overflow: "visible" }}
        >
            {/* Soft amber bloom so the die reads as lit rather than pasted on. */}
            <defs>
                <radialGradient id="die-glow" cx="50%" cy="50%" r="50%">
                    <stop offset="0%" stopColor="hsl(var(--primary))" stopOpacity="0.20" />
                    <stop offset="100%" stopColor="hsl(var(--primary))" stopOpacity="0" />
                </radialGradient>
            </defs>
            <rect x="-25" y="-25" width="150" height="150" fill="url(#die-glow)" />

            <rect
                x="4"
                y="4"
                width="92"
                height="92"
                fill="hsl(var(--card))"
                stroke="hsl(var(--primary))"
                strokeWidth="3"
            />
            {pips.map((i) => {
                const col = i % 3;
                const row = Math.floor(i / 3);
                const s = 12;
                return (
                    <rect
                        key={i}
                        x={unit * col + unit / 2 - s / 2}
                        y={unit * row + unit / 2 - s / 2}
                        width={s}
                        height={s}
                        fill="hsl(var(--primary))"
                    />
                );
            })}
        </svg>
    );
}
