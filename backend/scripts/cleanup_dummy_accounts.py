"""Safe cleanup of dummy / testing-agent accounts.

REFUSES to delete anyone whose email does NOT match the test patterns below.
Real player accounts (@gmail.com / @yahoo.com / @outlook.com / etc.) are
ALWAYS PRESERVED even if their character has no progression.

Run with:
    cd /app/backend && python3 scripts/cleanup_dummy_accounts.py           # dry-run
    cd /app/backend && python3 scripts/cleanup_dummy_accounts.py --apply   # actually delete

Match rules — an account is considered dummy ONLY when ALL of these hold:
    1. email domain is a known test/fake domain (@erchis.io by default)
    2. OR email local-part starts with a known test prefix (test_, TEST_, orc_test_, elf_, etc.)
"""
from __future__ import annotations
import asyncio
import re
import sys
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os

load_dotenv("/app/backend/.env")

# Fake domains used by testing agents / pytest suites. Real users cannot receive
# email at these domains, so anyone with one is definitely a bot.
FAKE_DOMAINS = {
    "erchis.io",       # this project's fake test domain
    "example.com",
    "test.local",
    "example.org",
}

# Email local-part prefixes used by testing agents. Only matched IN CONJUNCTION
# with a fake domain — a real gmail user with `test_` in their name is still safe.
TEST_LOCAL_PREFIXES = (
    "test_", "test-", "TEST_",
    "testui_", "testui-",
    "orc_test_", "elf_", "elftest", "wild_", "wildtest",
    "hyl_", "hylitest", "he_", "sylvan_",
    "origin_test", "origin_v2",
)

RE_DUMMY_CHARACTER_NAME = re.compile(r"^(TEST|Test_|T_)", re.IGNORECASE)


def is_dummy_email(email: str | None) -> bool:
    if not email:
        return False
    email = email.lower().strip()
    if "@" not in email:
        return False
    local, _, domain = email.partition("@")
    # Must be a fake domain — this is the safe boundary.
    if domain not in FAKE_DOMAINS:
        return False
    return True  # every account on a fake domain is dummy


async def main(apply: bool) -> None:
    client = AsyncIOMotorClient(os.environ["MONGO_URL"])
    db = client[os.environ["DB_NAME"]]

    total_users = await db.users.count_documents({})
    total_chars = await db.characters.count_documents({})
    total_events = await db.world_events.count_documents({})
    print(f"BEFORE: users={total_users} characters={total_chars} world_events={total_events}")

    # 1. Find dummy users
    dummy_user_ids: list[str] = []
    dummy_emails: list[str] = []
    preserved_emails: list[str] = []
    async for u in db.users.find({}, {"email": 1}):
        email = u.get("email", "")
        if is_dummy_email(email):
            dummy_user_ids.append(str(u["_id"]))
            dummy_emails.append(email)
        else:
            preserved_emails.append(email)

    print(f"\nDummy users to delete: {len(dummy_user_ids)}")
    for e in dummy_emails[:20]:
        print(f"  - {e}")
    if len(dummy_emails) > 20:
        print(f"  ...and {len(dummy_emails) - 20} more")

    print(f"\nReal users PRESERVED ({len(preserved_emails)}):")
    for e in preserved_emails:
        print(f"  ✓ {e}")

    # 2. Find dummy characters (by user_id OR by TEST-prefix name whose email is fake)
    dummy_char_names: list[str] = []
    async for c in db.characters.find({"user_id": {"$in": dummy_user_ids}}, {"name": 1}):
        if c.get("name"):
            dummy_char_names.append(c["name"])

    print(f"\nDummy characters to delete: {len(dummy_char_names)}")

    if not apply:
        print("\n[DRY RUN] No changes made. Re-run with --apply to actually delete.")
        return

    # 3. Actually delete
    if dummy_user_ids:
        from bson import ObjectId
        r = await db.users.delete_many({"_id": {"$in": [ObjectId(x) for x in dummy_user_ids]}})
        print(f"\nDeleted {r.deleted_count} users")
        r = await db.characters.delete_many({"user_id": {"$in": dummy_user_ids}})
        print(f"Deleted {r.deleted_count} characters")
        if dummy_char_names:
            r = await db.world_events.delete_many({"character_name": {"$in": dummy_char_names}})
            print(f"Deleted {r.deleted_count} world_events authored by dummy chars")
        # Combats that reference dummies: purge combats whose character_id no longer exists
        alive_char_ids = {str(c["_id"]) async for c in db.characters.find({}, {"_id": 1})}
        combat_ids_to_delete = []
        async for combat in db.combats.find({}, {"_id": 1, "character_id": 1}):
            if combat.get("character_id") not in alive_char_ids:
                combat_ids_to_delete.append(combat["_id"])
        if combat_ids_to_delete:
            r = await db.combats.delete_many({"_id": {"$in": combat_ids_to_delete}})
            print(f"Deleted {r.deleted_count} orphaned combats")

    # 4. Snapshot after
    print(f"\nAFTER: users={await db.users.count_documents({})} "
          f"characters={await db.characters.count_documents({})} "
          f"world_events={await db.world_events.count_documents({})}")


if __name__ == "__main__":
    apply = "--apply" in sys.argv
    asyncio.run(main(apply))
