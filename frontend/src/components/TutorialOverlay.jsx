import { useState } from "react";
import { api } from "@/lib/api";

const STEPS = [
    { title: "Welcome to Erchis", body: "This world runs on the throw of a die. Every action you take rolls a d6 — six possible outcomes, twenty possible stories." },
    { title: "Your Vitals", body: "Watch your HP, gold, XP, and status effects on the left panel. Level up by acting decisively." },
    { title: "Choose Your Biome", body: "Select a biome and take an action: Hunt monsters, Gather materials, Explore for treasure, or Loot ancient ruins." },
    { title: "Fortune Weighs the Dice", body: "Your Power (stats + level + gear) shifts the odds. Stronger foes are harder to crit; weaker foes fall easily." },
    { title: "Combat Is a Story", body: "When you Hunt, combat begins. Skills auto-select from what you've learned; items trigger by condition. Override manually anytime." },
    { title: "Craft, Learn, Explore", body: "Craft items with dice-graded quality. Learn skills from NPC teachers or rare skillbooks. Daily missions and login rewards keep the pouches heavy." },
];

export default function TutorialOverlay({ character, onComplete }) {
    const [step, setStep] = useState(character.tutorial_step || 0);

    if (character.tutorial_complete) return null;

    const advance = async () => {
        const next = step + 1;
        if (next >= STEPS.length) {
            await api.post("/game/character/tutorial", { step: next, complete: true });
            onComplete?.();
            return;
        }
        await api.post("/game/character/tutorial", { step: next, complete: false });
        setStep(next);
    };

    const skip = async () => {
        await api.post("/game/character/tutorial", { step: STEPS.length, complete: true });
        onComplete?.();
    };

    const cur = STEPS[Math.min(step, STEPS.length - 1)];

    return (
        <div className="fixed inset-0 z-50 bg-black/85 flex items-center justify-center p-4" data-testid="tutorial-overlay">
            <div className="panel max-w-lg w-full p-8">
                <div className="stat-label text-primary/70 mb-2">TUTORIAL · {step + 1}/{STEPS.length}</div>
                <h2 className="font-pixel text-3xl uppercase text-primary mb-4">{cur.title}</h2>
                <p className="narr text-lg text-foreground/90 leading-relaxed mb-8">{cur.body}</p>
                <div className="flex justify-between items-center">
                    <button
                        data-testid="tutorial-skip"
                        onClick={skip}
                        className="stat-label text-muted-foreground hover:text-primary"
                    >
                        SKIP TUTORIAL
                    </button>
                    <button
                        data-testid="tutorial-next"
                        onClick={advance}
                        className="press-btn font-pixel text-lg uppercase px-6 py-2 bg-primary text-primary-foreground border-2 border-primary hover:bg-transparent hover:text-primary transition-colors"
                    >
                        {step + 1 >= STEPS.length ? "Begin" : "Next →"}
                    </button>
                </div>
            </div>
        </div>
    );
}
