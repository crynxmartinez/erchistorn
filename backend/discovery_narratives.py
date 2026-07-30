"""Rich, varied narrative templates for exploration discoveries.
Templates are categorized by discovery kind AND profession for flavor appropriateness.
Each template uses {name} as a placeholder for the discovered entity name.
"""
import random

# ── General discovery templates (work for any kind) ──
_GENERAL = [
    "You stumble upon {name} — half-hidden by the terrain, as if it had been waiting for you.",
    "Something catches your eye through the gloom. You push aside brush and debris: {name}.",
    "The light shifts, and for a moment a shadow resolves into shape. {name} stands before you, unmistakable.",
    "Your foot catches on something solid. You dig down, brush away dirt and old leaves — {name}.",
    "A sound, or maybe a smell, draws you forward. You round a boulder and find {name}.",
    "You almost walk past it. But a glint, a texture, a wrongness in the air stops you. {name}.",
    "The ground dips beneath your boot and you slide down a short embankment. At the bottom: {name}.",
    "You've been walking for what feels like hours. The terrain blurs — and then, suddenly, {name}, clear as day.",
    "A break in the canopy lets a shaft of light fall perfectly on {name}, as if the world itself is showing you the way.",
    "You crest a ridge and pause. Below, in a hollow you hadn't noticed before, lies {name}.",
    "Your hand brushes a wall of stone and you feel carving beneath your fingers. You trace it out — {name}.",
    "The wind dies. The birds go silent. And in that stillness, you see {name} for the first time.",
    "You follow a trail of disturbed earth and broken branches. At the end of it: {name}.",
    "Something about this spot feels different. You kneel, brush away the surface, and uncover {name}.",
    "You take a wrong turn around a blind corner and nearly trip over {name}. Fate or luck — you decide.",
    "The fog thins for just a heartbeat, and in that gap you see {name}. You commit the location to memory before the mist closes again.",
    "You've passed this way before, you're sure of it. But you've never seen {name} until now. It was hiding in plain sight.",
    "A strange warmth radiates from the ground. You follow it, step by step, until you're standing over {name}.",
    "You duck under a low branch and straighten up into a clearing. {name} occupies the center, patient and ancient.",
    "Your breath fogs in the sudden cold. Ice crystals cling to {name}, glittering as you approach.",
]

# ── Monster discovery templates ──
_MONSTER = [
    "Tracks in the soft earth — fresh, deliberate. You follow them to a clearing. {name} lifts its head and regards you with cold, knowing eyes.",
    "The undergrowth rustles. You freeze. {name} emerges from the shadows, larger than the stories suggested.",
    "A low growl reverberates through the ground beneath your feet. You turn slowly. {name} is there, watching, patient.",
    "You smell it before you see it — musk and iron. {name} steps into the open, blocking your path.",
    "Something massive moves in the treeline. You catch a flash of hide, a glint of eye. {name} has found you.",
    "The birds scatter from the canopy in a single panicked wave. You look up. {name} is perched above, silent and still.",
    "You hear bones crack underfoot and look down — a midden of old kills. {name} is close. Too close. You look up and meet its gaze.",
    "A shadow detaches itself from the rocks and resolves into {name}. It does not flee. It does not charge. It simply acknowledges you.",
    "The hair on your arms stands on end. You turn — {name} is there, having approached without a single sound.",
    "You find a lair: bones, scratch marks, old scent markings. A shape shifts in the darkness within. {name} stirs.",
    "Claw marks raked deep into a tree trunk — chest-height. Whatever left them was enormous. You follow the trail and find {name}.",
    "A puddle ripples with no wind to disturb it. You look up from the water and find {name} watching you from the far bank.",
]

# ── Mining node templates ──
_MINING = [
    "You notice an unusual color in the soil ahead. Kneeling, you confirm it — {name}, rich and untouched.",
    "A faint shimmer catches the light between the rocks. You chip away the surface and expose {name}.",
    "The ground here is different — harder, denser, alive with mineral veins. You've found {name}.",
    "Old tool marks on a nearby stone suggest someone worked this spot before. You follow the seam and find {name}, still plentiful.",
    "You break through a crust of lichen and dead moss. Beneath it: {name}, gleaming in the dim light.",
    "You almost dismiss the outcrop as ordinary stone. But the weight, the grain, the faint resonance — {name}, without a doubt.",
    "Roots have split the rock over centuries, exposing {name} in a natural wedge. Nature did the mining for you.",
    "The air tastes different here — metallic, sharp. You follow the scent to a seam of {name} running through the cliff face.",
    "A streak of color in the rock face stops you. You scrape away the weathered surface and {name} gleams beneath, fresh as the day it formed.",
    "Your hammer rings differently against this section of wall — denser, more resonant. You've struck {name}.",
]

# ── Fishing node templates ──
_FISHING = [
    "The water here is clearer than elsewhere — you can see straight to the bottom. {name} glides beneath the surface, catching light.",
    "A flash of silver beneath the ripples catches your eye. You crouch at the water's edge and watch {name} drift in the current.",
    "The river narrows here, forcing the water faster through a chute of smooth stone. {name} congregates in the calmer pool below.",
    "You notice rings on the surface — feeding fish. You creep closer and identify {name} schooling just beneath.",
    "An old fishing post rots on the bank — someone worked this spot before. You cast your gaze downstream and spot {name} in the shallows.",
    "The water is dark and still here, deep enough to hide something. You wait. A shape surfaces: {name}, rolling once before sinking back.",
    "You skip a stone across the water and it plops near a reed bed. The disturbance flushes {name} from cover, briefly visible before they dart away.",
    "Dragonflies hover above the surface, and where they dip, {name} rises to meet them. You mark the spot.",
    "The tide pool is alive with movement — small crabs, anemones, and there, in the deepest pocket, {name}.",
    "You wade in to your knees and feel something brush your ankle. You look down. {name} swirls around your legs in a silver cloud.",
]

# ── Herbalism node templates ──
_HERBALISM = [
    "A scent on the wind — green, sharp, unfamiliar. You follow it to a sheltered hollow and find {name} growing in thick clusters.",
    "You brush through tall grass and notice your boots are stained with pollen. You look down: {name}, blooming here in abundance.",
    "The ground is damp here, fed by a hidden seep. The moisture has drawn {name} up in a lush carpet of color.",
    "A break in the canopy lets sunlight fall on a single patch of earth, and there — {name}, turning its leaves toward the warmth.",
    "You kneel to retie your boot and notice the plant beside you isn't like the others. The leaf shape, the stem — {name}. You've walked past it twice without seeing.",
    "Bees drone lazily around a thicket you'd dismissed as weeds. You look closer. {name}, flowering in the dappled shade.",
    "The soil here is dark and rich, different from the surrounding ground. You part the ferns and find {name} thriving in the loam.",
    "An old stump, half-rotted, serves as a nursery for {name} — its roots threading through the dead wood, drawing life from decay.",
    "You notice a patch of ground where nothing else grows — and yet {name} flourishes there alone, as if the soil belongs to it.",
    "Frost clings to the hollows here, but {name} is somehow untouched — green and vital despite the cold, as if it carries its own warmth.",
]

# ── Logging node templates ──
_LOGGING = [
    "You hear the groan of old wood before you see it — a stand of trees leaning against each other, heavy with age. {name} towers among them.",
    "The axe marks on a nearby stump are old and weathered. You follow the felled timber trail and find {name}, still standing, still prime.",
    "A fallen log blocks your path. You step over it — and notice the grain. Dense, straight, dark. {name}, worth more than the whole forest around it.",
    "The canopy opens here, and a single colossal tree dominates the clearing. {name}, its bark thick and its limbs broad as roads.",
    "You've been walking through scrub for an hour when the trees change — taller, older, darker-barked. You've entered {name} territory.",
    "A woodcutter's cairn marks a fork in the trail. You take the overgrown path and it leads you to {name}, untouched by axe or fire.",
    "The ground is carpeted with distinctive leaves — broader, darker than the rest. You look up and find {name} arching overhead.",
    "You test a low branch for handhold and it doesn't give. The density, the weight — this is {name}. You follow the trunk up into the canopy.",
]

# ── Hunting node templates ──
_HUNTING = [
    "You find a wallow — mud churned by heavy bodies, hair caught on nearby branches. {name} uses this ground regularly.",
    "A midden of shells and bones sits at the base of a rock. You crouch and study the remains — {name} feeds here, and often.",
    "You flush a covey from the underbrush and they scatter in a burst of wings. But one holds tight — {name}, nesting in the thorns.",
    "The grass here is flattened in a wide circle — a resting spot. You measure the depression. {name}, by the size of it.",
    "You find a game trail — narrow, well-worn, fresh droppings along its length. You follow it to a clearing and find {name} grazing.",
    "A burrow entrance, freshly dug, the soil still damp. You back away quietly — {name} is home, and you'd rather not meet at the door.",
    "You spot a nest in the high grass — woven, lined with down. {name} has been breeding here, undisturbed by the world.",
    "The snap of a twig. You turn. {name} bolts through the brush, and you mark the direction — you'll return better prepared.",
]

# ── Excavation node templates ──
_EXCAVATION = [
    "You notice a depression in the earth — too regular to be natural. You clear the topsoil and find {name} buried beneath.",
    "Old stones, arranged in a line too straight for nature. You scrape away the dirt and uncover {name} — a remnant of something older than memory.",
    "The ground here is sunken, collapsed. You peer into the depression and see {name} half-submerged in the rubble.",
    "A farmer's plough must have hit something here, long ago — the furrow is scarred and redirected. You dig where the plough turned and find {name}.",
    "You find shards of old pottery scattered across the surface. You follow the scatter to its source and unearth {name}.",
    "The wind has eroded a small ridge, exposing layers of sediment — and there, wedged between them, {name}.",
    "A cairn of weathered stones stands at a crossroads no one travels anymore. You dismantle it and find {name} sealed beneath.",
    "You trip over something hard in the loose soil. You dig with your hands and pull {name} free of the earth that swallowed it centuries ago.",
]

# ── Waystone discovery templates ──
_WAYSTONE = [
    "A low hum teases the edge of your hearing. You follow it to a ring of ancient stone — {name}, dormant but not dead.",
    "The ground beneath your feet vibrates with a rhythm too steady to be natural. You look down. {name} pulses faintly beneath the moss.",
    "You brush aside creeping vines and your fingers find carved grooves — ancient, deliberate. {name} reveals itself, patient as the mountain.",
    "A warmth spreads through your chest as you step into the clearing. {name} stands at its center, and something in you recognizes it before your eyes do.",
    "Lightning never strikes the same place twice — but the scorched ring around {name} tells a different story. The stone hums, waiting.",
    "You dream of a road you've never walked, and when you wake, your feet have carried you to {name}. Coincidence is a coward's word.",
    "The old markers on your map end here, at a blank space. But the blank space is no longer blank. {name} rises from the earth like a forgotten tooth.",
    "You feel watched. Not threatened — observed. You turn and find {name}, its carved face weathered but aware, as if it has been tracking your approach for miles.",
]


_PROFESSION_TEMPLATES = {
    "mining": _MINING,
    "fishing": _FISHING,
    "herbalism": _HERBALISM,
    "logging": _LOGGING,
    "hunting": _HUNTING,
    "excavation": _EXCAVATION,
}


def discovery_narrative(discoveries: list[dict]) -> str:
    """Generate immersive narrative text for a list of discoveries.
    Returns a string to append to the action narrative.
    Each discovery gets a template matched to its kind and profession.
    """
    if not discoveries:
        return ""

    parts: list[str] = []
    for d in discoveries:
        kind = d.get("kind", "")
        name = d.get("name", "something")
        profession = d.get("profession", "")

        if kind == "monster":
            template = random.choice(_MONSTER)
        elif kind == "waystone":
            template = random.choice(_WAYSTONE)
        elif kind == "node":
            prof_pool = _PROFESSION_TEMPLATES.get(profession)
            if prof_pool:
                template = random.choice(prof_pool)
            else:
                template = random.choice(_GENERAL)
        else:
            template = random.choice(_GENERAL)

        parts.append(template.format(name=name))

    return " " + " ".join(parts)
