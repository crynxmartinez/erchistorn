"use client";

import { useEffect, useRef, useState } from "react";

/**
 * A d6 that either rolls once and settles, or cycles 1 → 6 → 1 forever.
 *
 * The weighted six-sided die is the game's central mechanic, so it doubles as the
 * logo and as the hero's only piece of "art" — no asset pipeline required. Pips are
 * squares, not circles, to match the site's global `border-radius: 0`.
 *
 * Three modes:
 *   `loop`             — count up 1..6, wrap to 1, keep going. The hero uses this.
 *   `roll` (default)   — one decelerating tumble that settles on `face`.
 *   neither            — static. The nav and footer marks use this: a logo that
 *                        animates in a sticky header is a distraction, not a brand.
 *
 * Honours `prefers-reduced-motion` in every mode: those users get the settled face
 * immediately and no timers are started. The loop also pauses while the tab is
 * hidden — a background timer repainting an offscreen die is pure waste.
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

/** Milliseconds each face is held while looping. */
const LOOP_MS = 850;

export default function Die({
    size = 240,
    face = 6,
    roll = true,
    loop = false,
    className = "",
}) {
    const reduced =
        typeof window !== "undefined" &&
        window.matchMedia?.("(prefers-reduced-motion: reduce)").matches;

    // Animated modes start at 1 and count/tumble up; static mode shows `face`.
    const animated = (loop || roll) && !reduced;
    const [shown, setShown] = useState(animated ? 1 : face);
    const [pulse, setPulse] = useState(false);
    const [tumbling, setTumbling] = useState(roll && !loop && !reduced);
    const timer = useRef(null);

    // ---- looping: 1..6, then back to 1 ----
    useEffect(() => {
        if (!loop || reduced) return;

        let cancelled = false;
        const tick = () => {
            if (cancelled) return;
            setShown((n) => (n >= 6 ? 1 : n + 1));
            // A brief settle on each change. Without it the pips just swap and the
            // die reads as a counter rather than something being thrown.
            setPulse(true);
            setTimeout(() => !cancelled && setPulse(false), 200);
            timer.current = setTimeout(tick, LOOP_MS);
        };

        const start = () => {
            clearTimeout(timer.current);
            timer.current = setTimeout(tick, LOOP_MS);
        };
        const stop = () => clearTimeout(timer.current);

        const onVisibility = () => (document.hidden ? stop() : start());
        document.addEventListener("visibilitychange", onVisibility);
        if (!document.hidden) start();

        return () => {
            cancelled = true;
            stop();
            document.removeEventListener("visibilitychange", onVisibility);
        };
    }, [loop, reduced]);

    // ---- one-shot roll ----
    useEffect(() => {
        if (loop || reduced || !roll) return;
        let ticks = 0;
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
    }, [face, roll, loop, reduced]);

    const pips = FACES[shown] || FACES[6];
    const unit = 100 / 3;

    return (
        <svg
            viewBox="0 0 100 100"
            width={size}
            height={size}
            className={`${className} ${tumbling ? "animate-die-tumble" : ""} ${
                pulse ? "animate-die-settle" : ""
            }`}
            role="img"
            aria-label={`Six-sided die showing ${shown}`}
            style={{ overflow: "visible" }}
        >
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
