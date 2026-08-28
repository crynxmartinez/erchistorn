"""Generate ALL_SKILLS.md from game_data.py"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'backend'))

from game_data import SKILLS, SKILLS_BY_ID

RARITY_COST = {"common": 1000, "uncommon": 3000, "rare": 10000, "epic": 25000, "legendary": 1000000}
RARITY_TIME = {"common": 60, "uncommon": 300, "rare": 1800, "epic": 7200, "legendary": 604800}

def fmt_time(s):
    if s >= 86400:
        return f"{s // 86400} day{'s' if s >= 172800 else ''}"
    if s >= 3600:
        return f"{s // 3600} hour{'s' if s >= 7200 else ''}"
    if s >= 60:
        return f"{s // 60} min{'s' if s >= 120 else ''}"
    return f"{s}s"

def fmt_cost(g):
    if g >= 1000000:
        return f"{g // 1000000}m"
    if g >= 1000:
        return f"{g // 1000}k"
    return f"{g}g"

TRIGGER_LABELS = {
    "always": "Always", "low_hp": "Low HP", "opponent_wounded": "Opponent Wounded",
    "opponent_status": "Opponent Status", "opening_move": "Opening Move",
    "self_debuff": "When Debuffed",
}

MASTERY_ORDER = [
    ("General Skills", None),
    ("Alchemist — Transmutation Arts", "alchemist"),
    ("Paladin — Divine Guardian", "paladin"),
    ("Priest — The Holy Judge", "priest"),
    ("Knight — The Oathbound", "knight"),
    ("Lancer — Elemental Lance Master", "lancer"),
    ("Mage — The Architect", "mage"),
    ("Assassin — The Shadow Reaper", "assassin"),
    ("Hunter — Master of Precision", "hunter"),
    ("Rogue — The Adaptive Trickster", "rogue"),
    ("Bard — The Master of Control", "bard"),
    ("Druid — Nature's Voice", "druid"),
]

def get_mastery(skill):
    mr = skill.get("mastery_req", [])
    if isinstance(mr, list):
        return mr[0] if mr else None
    return mr

def stat_mod_str(mod, target):
    if not mod or target not in mod:
        return ""
    parts = []
    for stat, val in mod[target].items():
        stat_name = stat.replace("_", " ").title()
        sign = "+" if val >= 0 else ""
        parts.append(f"{sign}{val} {stat_name}")
    return f"{target.title()}: {', '.join(parts)}"

def skill_block(s):
    lines = []
    sid = s["id"]
    name = s["name"]
    rarity = s.get("rarity", "common")
    lvl = s.get("level_req", 1)
    cost = RARITY_COST.get(rarity, 1000)
    learn = RARITY_TIME.get(rarity, 60)
    
    lines.append(f"### {name}")
    meta_parts = [f"**Rarity:** {rarity}", f"**Level Req:** {lvl}", f"**Cost:** {fmt_cost(cost)}", f"**Learn:** {fmt_time(learn)}"]
    lines.append("- " + " | ".join(meta_parts))
    
    pt = s.get("power_type", "")
    pt_label = {"strike": "Strike", "heal": "Heal", "defend": "Defend", "buff": "Buff",
                "debuff": "Debuff", "imbue": "Imbue", "performance": "Performance",
                "shield_wall": "Shield Wall", "trap": "Trap", "spirit": "Spirit"}.get(pt, pt)
    dt = s.get("damage_type", "")
    type_str = pt_label
    if dt:
        type_str += f" ({dt})"
    
    detail_parts = [f"**Type:** {type_str}"]
    if "cooldown" in s:
        detail_parts.append(f"**Cooldown:** {s['cooldown']} turns")
    if "skill_capacity_cost" in s and s["skill_capacity_cost"]:
        detail_parts.append(f"**SC Cost:** {s['skill_capacity_cost']}")
    if "damage" in s and s["damage"]:
        if pt == "heal":
            detail_parts.append(f"**Heal Power:** {s['damage']}")
        else:
            detail_parts.append(f"**Damage:** {s['damage']}")
    if "hits" in s and s["hits"] > 1:
        detail_parts.append(f"**Hits:** {s['hits']}")
    
    trigger = s.get("trigger", "always")
    detail_parts.append(f"**Trigger:** {TRIGGER_LABELS.get(trigger, trigger)}")
    
    if "status_apply" in s:
        st = s["status_apply"]
        if isinstance(st, list):
            detail_parts.append(f"**Status:** {', '.join(st).title()}")
        else:
            detail_parts.append(f"**Status:** {st.title()}")
    
    if "self_status" in s:
        detail_parts.append(f"**Self Status:** {s['self_status'].title()}")
    
    if "heal_percent" in s:
        detail_parts.append(f"**Heal:** {int(s['heal_percent'] * 100)}%")
    
    lines.append("- " + " | ".join(detail_parts))
    
    # Stat mods
    sm = s.get("stat_mod", {})
    if sm:
        mod_parts = []
        for target in ["self", "enemy", "all_allies"]:
            ms = stat_mod_str(sm, target)
            if ms:
                mod_parts.append(ms)
        if mod_parts:
            lines.append(f"- **Stat Mods:** {'; '.join(mod_parts)}")
    
    if "mod_duration" in s:
        lines.append(f"- **Mod Duration:** {s['mod_duration']} turns")
    
    # Imbue info
    if "imbue_charges" in s:
        imb_parts = [f"{s['imbue_charges']} charges"]
        if "imbue_status" in s:
            imb_parts.append(s["imbue_status"])
        if "blade_shape" in s:
            imb_parts.append(f"Blade: {s['blade_shape']}")
        if "imbue_mini_rule" in s:
            imb_parts.append(f"Rule: {s['imbue_mini_rule']}")
        lines.append(f"- **Imbue:** {', '.join(imb_parts)}")
    
    # Strike rule
    if "strike_rule" in s:
        lines.append(f"- **Strike Rule:** {s['strike_rule']}")
    
    # Legendary rule
    if "legendary_rule" in s:
        lines.append(f"- **Legendary Rule:** {s['legendary_rule']}")
    
    # Quest req
    if "quest_req" in s:
        lines.append(f"- **Quest Required:** {s['quest_req']}")
    
    # Spirit communion (hunter)
    if "spirit_communion" in s:
        lines.append(f"- **Spirit Communion:** {s['spirit_communion']}")
    
    # Mastery/weapon
    mw_parts = []
    mr = s.get("mastery_req", [])
    if mr:
        if isinstance(mr, list):
            mw_parts.append(f"**Mastery:** {', '.join(mr)}")
        else:
            mw_parts.append(f"**Mastery:** {mr}")
    if s.get("weapon_req", "none") != "none":
        mw_parts.append(f"**Weapon:** {s['weapon_req']}")
    if mw_parts:
        lines.append("- " + " | ".join(mw_parts))
    
    # Description
    desc = s.get("desc", "")
    if desc:
        lines.append(f"- **Description:** {desc}")
    
    # Narration
    exec_text = s.get("execution_text", "")
    if exec_text:
        lines.append(f"- **Narration:** *\"{exec_text}\"*")
    
    lines.append("")
    return "\n".join(lines)

# Group skills
general_skills = []
mastery_skills = {}
for s in SKILLS:
    m = get_mastery(s)
    if m is None or (isinstance(s.get("mastery_req", []), list) and len(s.get("mastery_req", [])) > 1):
        general_skills.append(s)
    else:
        mastery_skills.setdefault(m, []).append(s)

# Build doc
out = []
out.append("# Erchistorn — Complete Skill Reference\n")
out.append(f"> **Total Skills:** {len(SKILLS)} across 11 masteries\n")

# Tier table
out.append("> **Proposed Tier System (Option B — flat costs per rarity):**\n")
out.append("> | Tier | Level Req | Rarity | Cost | Learn Time |")
out.append("> |------|-----------|--------|------|------------|")
out.append("> | Basic | Lv 1 | common | 1,000g | 1 minute |")
out.append("> | Novice | Lv 2-3 | uncommon | 3,000g | 5 minutes |")
out.append("> | Intermediate | Lv 3+ | rare | 10,000g | 30 minutes |")
out.append("> | Adept | Lv 4+ | epic | 25,000g | 2 hours |")
out.append("> | Master | Lv 20 | legendary | 1,000,000g | 7 days |\n")

out.append("---\n")
out.append("## Table of Contents\n")
for title, mastery in MASTERY_ORDER:
    anchor = title.lower().replace(" ", "-").replace("—", "--").replace("'", "").replace(",", "").replace(".", "")
    out.append(f"- [{title}](#{anchor})")
out.append("\n---\n")

for title, mastery in MASTERY_ORDER:
    out.append(f"## {title}\n")
    if mastery is None:
        skills = general_skills
    else:
        skills = mastery_skills.get(mastery, [])
    
    if not skills:
        out.append("*No skills found.*\n")
        continue
    
    # Group by tier
    tiers = {}
    for s in skills:
        lvl = s.get("level_req", 1)
        tier_key = lvl
        tiers.setdefault(tier_key, []).append(s)
    
    for lvl in sorted(tiers.keys()):
        tier_names = {1: "Basic Tier (Level 1)", 2: "Novice Tier (Level 2)", 3: "Intermediate Tier (Level 3)",
                      4: "Adept Tier (Level 4)", 8: "Advanced Tier (Level 8)", 15: "Expert Tier (Level 15)",
                      20: "Legendary Tier (Level 20)"}
        tier_name = tier_names.get(lvl, f"Level {lvl}")
        out.append(f"### {tier_name}\n")
        for s in tiers[lvl]:
            out.append(skill_block(s))
    
    out.append("---\n")

content = "\n".join(out)
outpath = os.path.join(os.path.dirname(__file__), "ALL_SKILLS.md")
with open(outpath, "w", encoding="utf-8") as f:
    f.write(content)
print(f"Written {len(content)} chars to {outpath}")
print(f"Total skills: {len(SKILLS)}")
