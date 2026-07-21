import { useEffect, useRef, useState } from "react";

/** Rolling d6 dice component. Emits onResult when caller sets result prop. */
export default function Dice({ result, rolling, size = 96, testId = "dice-face" }) {
    const [display, setDisplay] = useState(result || "?");
    const intervalRef = useRef(null);

    useEffect(() => {
        if (rolling) {
            let i = 0;
            intervalRef.current = setInterval(() => {
                setDisplay(((i++ % 6) + 1).toString());
            }, 70);
        } else {
            if (intervalRef.current) clearInterval(intervalRef.current);
            setDisplay(result ? result.toString() : "?");
        }
        return () => {
            if (intervalRef.current) clearInterval(intervalRef.current);
        };
    }, [rolling, result]);

    const outcomeColor = (n) => {
        if (n === 1) return "text-rarity-mythic";
        if (n === 2) return "text-rarity-legendary";
        if (n === 3) return "text-muted-foreground";
        if (n === 4) return "text-rarity-uncommon";
        if (n === 5) return "text-primary";
        if (n === 6) return "text-rarity-legendary";
        return "text-primary";
    };

    return (
        <div
            data-testid={testId}
            className={`inline-flex items-center justify-center border-2 border-primary bg-background font-pixel select-none ${
                rolling ? "dice-shake" : ""
            }`}
            style={{
                width: size,
                height: size,
                fontSize: size * 0.55,
                boxShadow: rolling ? "0 0 24px hsl(var(--primary) / 0.5)" : "4px 4px 0 0 hsl(var(--destructive))",
            }}
        >
            <span className={outcomeColor(Number(display))}>{display}</span>
        </div>
    );
}
