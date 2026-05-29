import pytest

pytest.importorskip("PySide6")

from PySide6 import QtTest

from app.gui_qt.telemetry.cards_model import TelemetryCardsModel


def _card(card_id: str, pct: int) -> dict:
    return {
        "id": card_id,
        "label": card_id,
        "valueText": f"{pct}%",
        "sub": "—",
        "pct": pct,
        "color": "#3fae6e",
        "warn": False,
        "variant": "local",
    }


def test_set_cards_updates_in_place_when_ids_stable():
    model = TelemetryCardsModel()
    model.set_cards([_card("cpu", 10), _card("ram", 20)])

    reset_spy = QtTest.QSignalSpy(model.modelReset)
    changed_spy = QtTest.QSignalSpy(model.dataChanged)

    model.set_cards([_card("cpu", 55), _card("ram", 60)])

    assert reset_spy.count() == 0
    assert changed_spy.count() == 2
    assert model.as_list()[0]["pct"] == 55
    assert model.as_list()[1]["pct"] == 60


def test_set_cards_resets_when_structure_changes():
    model = TelemetryCardsModel()
    model.set_cards([_card("cpu", 10)])

    reset_spy = QtTest.QSignalSpy(model.modelReset)

    model.set_cards([_card("cpu", 10), _card("ram", 20)])

    assert reset_spy.count() == 1
    assert model.count == 2
