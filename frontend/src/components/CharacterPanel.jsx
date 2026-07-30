import { User, BookOpen, Package } from "lucide-react";
import CollapsibleSection from "@/components/CollapsibleSection";
import CharacterSheet from "@/components/CharacterSheet";
import RacialAbilityPanel from "@/components/RacialAbilityPanel";
import SkillsPanel from "@/components/SkillsPanel";
import Inventory from "@/components/Inventory";

export default function CharacterPanel({ character, portraits, race, role, mastery, itemsById, skillsById, rogueInnateSkills, roguePassives, masteryPassives, timeOfDay, onCharacterUpdate, onDeleteCharacter }) {
    return (
        <div className="space-y-0">
            <CollapsibleSection title="Hero" icon={User} defaultOpen={true}>
                <CharacterSheet
                    character={character}
                    portraits={portraits}
                    race={race}
                    role={role}
                    mastery={mastery}
                    itemsById={itemsById}
                    timeOfDay={timeOfDay}
                    onDeleteCharacter={onDeleteCharacter}
                />
                <div className="panel p-4 mt-3">
                    <RacialAbilityPanel character={character} onCharacterUpdate={onCharacterUpdate} timeOfDay={timeOfDay} />
                </div>
            </CollapsibleSection>

            <CollapsibleSection title="Skills" icon={BookOpen} defaultOpen={false}>
                <SkillsPanel
                    character={character}
                    skillsById={skillsById}
                    rogueInnateSkills={rogueInnateSkills}
                    roguePassives={roguePassives}
                    masteryPassives={masteryPassives}
                    onCharacterUpdate={onCharacterUpdate}
                />
            </CollapsibleSection>

            <CollapsibleSection title="Inventory" icon={Package} defaultOpen={false}>
                <Inventory
                    character={character}
                    itemsById={itemsById}
                    onCharacterUpdate={onCharacterUpdate}
                />
            </CollapsibleSection>
        </div>
    );
}
