"""DQN distributed: снимок ростера в train-context (ПК1) и чтение на ПК2.

Цель — убрать `env_contract_hash mismatch`: ПК2 строит env из РОВНО того же
ростера, что ПК1, а не из своего локального runtime/state/data.json.
"""

import json

import train


def test_jsonable_roster_is_json_serializable_with_list_weapons():
    roster = train._load_roster_config()
    jsonable = train._jsonable_roster(roster)

    # json.dumps не должен падать (кортежи weapons → списки).
    dumped = json.dumps(jsonable, ensure_ascii=False)
    assert isinstance(dumped, str)

    for unit in jsonable["enemy_units"] + jsonable["model_units"]:
        assert isinstance(unit["weapons"], list)


def test_roster_survives_context_roundtrip():
    roster = train._load_roster_config()

    # ПК1: ростер → JSON-снимок в контексте.
    ctx_json = json.dumps({"roster": train._jsonable_roster(roster)}, ensure_ascii=False)
    # ПК2: контекст → ростер.
    ctx = json.loads(ctx_json)
    restored = train._roster_from_context(ctx)

    assert restored == roster


def test_roster_from_context_returns_none_when_absent():
    # Старый ПК1 (без снимка) → ПК2 падает на локальный data.json.
    assert train._roster_from_context({}) is None
    assert train._roster_from_context({"roster": None}) is None
