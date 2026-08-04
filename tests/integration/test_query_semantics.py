"""Pin down how Mongo treats absent fields, and assert our queries match intent.

The single worst bug of the audit was not a typo — it was a wrong mental model.
`{"$lt": n}` does **not** match documents where the field is missing, so the
schema migration's `{"schema_version": {"$lt": 2}}` matched none of the characters
it existed to upgrade: every pre-existing character has no `schema_version` at all.
Measured on real data, the old query matched 0 of 2 legacy characters and the
fixed one matched both.

A mock would have happily reproduced the bug, so these run against real Mongo.

The asymmetry is the part worth remembering:
    $lt / $lte / $gt / $gte / $in   ->  absent field does NOT match
    $ne / $nin                      ->  absent field DOES match
Both directions are surprising, in opposite ways, and the codebase depends on
each of them in a different place.
"""
from __future__ import annotations

import os

import pytest

pytestmark = pytest.mark.integration

MONGO_URL = os.environ.get("MONGO_URL", "mongodb://127.0.0.1:27017")
DB = "erchis_query_semantics_test"


@pytest.fixture
def coll():
    pymongo = pytest.importorskip("pymongo")
    try:
        client = pymongo.MongoClient(MONGO_URL, serverSelectionTimeoutMS=3000)
        client.admin.command("ping")
    except Exception as exc:  # noqa: BLE001
        pytest.skip(f"no Mongo at {MONGO_URL} ({type(exc).__name__})")
    c = client[DB]["docs"]
    c.delete_many({})
    c.insert_many([
        {"name": "has_it_low", "schema_version": 1},
        {"name": "has_it_current", "schema_version": 2},
        {"name": "field_is_null", "schema_version": None},
        {"name": "field_absent"},  # the shape every legacy character has
    ])
    yield c
    client.drop_database(DB)
    client.close()


def _names(cursor):
    return sorted(d["name"] for d in cursor)


def test_lt_does_not_match_an_absent_field(coll):
    """The exact bug. If this ever passes with field_absent included, the
    surprise has gone away and the $or guards can be simplified."""
    got = _names(coll.find({"schema_version": {"$lt": 2}}))
    assert got == ["has_it_low"], (
        "$lt matched something other than the one document that has a lower "
        f"value: {got}. Absent and null must both be excluded."
    )
    assert "field_absent" not in got
    assert "field_is_null" not in got


def test_the_migration_query_shape_matches_every_upgradable_document(coll):
    """The fix that made the migration actually run."""
    query = {"$or": [
        {"schema_version": {"$exists": False}},
        {"schema_version": None},
        {"schema_version": {"$lt": 2}},
    ]}
    got = _names(coll.find(query))
    assert got == ["field_absent", "field_is_null", "has_it_low"], got
    assert "has_it_current" not in got, "an up-to-date document must not re-migrate"


def test_ne_does_match_an_absent_field(coll):
    """The opposite trap, which /combat/start now relies on deliberately.

    Cleaning up finished combats uses `{"state.active": {"$ne": True}}` rather
    than `== False` precisely so a document missing the field is still collected.
    """
    got = _names(coll.find({"schema_version": {"$ne": 2}}))
    assert "field_absent" in got, (
        "$ne no longer matches absent fields — the combat cleanup filter in "
        "/game/combat/start depends on it and would start leaking documents"
    )
    assert "field_is_null" in got
    assert "has_it_current" not in got


def test_in_does_not_match_an_absent_field(coll):
    """Why the sanctuary roster's `current_town: {$in: [...]}` is correct: a
    character wandering the wilderness has no current_town and must not appear."""
    got = _names(coll.find({"schema_version": {"$in": [1, 2]}}))
    assert got == ["has_it_current", "has_it_low"], got
    assert "field_absent" not in got


def test_equality_on_false_misses_an_absent_field(coll):
    """The reason the combat cleanup uses $ne instead of == False."""
    coll.insert_many([{"name": "active_true", "active": True},
                      {"name": "active_false", "active": False},
                      {"name": "active_missing"}])
    strict = _names(coll.find({"active": False}))
    loose = _names(coll.find({"active": {"$ne": True}}))
    assert strict == ["active_false"]
    assert "active_missing" in loose, (
        "the $ne form must sweep up documents with no `active` field, or finished "
        "combats written without it would never be deleted"
    )
