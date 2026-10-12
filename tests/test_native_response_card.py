"""Regression tests for native intent cards and existing display routing."""

from types import SimpleNamespace
from unittest.mock import Mock, patch

import pytest
from custom_components.view_assist.devices.entity_listeners import (
    EntityStateChangedHandler,
)
from homeassistant.core import Event, State

MODULE = "custom_components.view_assist.devices.entity_listeners"
CARD = {"title": "Recipe", "content": "First prepare the ingredients. Then cook."}


@pytest.fixture
def display():
    """Use a minimal device config and capture actual navigation/update ordering."""
    config = SimpleNamespace(
        entry_id="test",
        options={},
        runtime_data=SimpleNamespace(
            core=SimpleNamespace(),
            dashboard=SimpleNamespace(intent="custom/intent", list_view="custom/list"),
            extra_data={},
        ),
    )
    hass = Mock()
    handler = EntityStateChangedHandler(hass, config)
    navigation = Mock()
    navigation.browser_navigate.side_effect = lambda _path: (
        config.runtime_data.extra_data.update(title="")
    )
    with (
        patch(f"{MODULE}.NavigationManager.get", return_value=navigation),
        patch(f"{MODULE}.async_dispatcher_send") as dispatcher,
    ):
        yield handler, config.runtime_data.extra_data, navigation, dispatcher


def intent_event(speech="Short speech", card=CARD, success=None, local=False, old=None):
    """Build the same result envelope used by the intent sensor."""
    response = {"card": {"simple": card}, "data": {"success": success or []}}
    if speech is not None:
        response["speech"] = {"plain": {"speech": speech}}
    return Event(
        "state_changed",
        data={
            "new_state": State(
                "sensor.intent",
                speech or "",
                attributes={
                    "intent_output": {"response": response},
                    "processed_locally": local,
                },
            ),
            "old_state": old,
        },
    )


@pytest.mark.parametrize("speech", ["Short speech", None, "*"])
@pytest.mark.parametrize("local", [False, True])
def test_native_card(display, speech, local):
    """Native display text is independent of speech and local processing."""
    handler, updates, navigation, dispatcher = display
    handler._async_on_intent_device_change(intent_event(speech=speech, local=local))
    assert updates["title"] == CARD["title"]
    assert updates["message"] == CARD["content"]
    assert updates["message_font_size"] == "8vw"
    assert updates.get("last_said") == speech
    navigation.browser_navigate.assert_called_once_with("view-assist/info")
    dispatcher.assert_called_once()


@pytest.mark.parametrize(
    "card",
    [
        None,
        {},
        [],
        "invalid",
        {"title": "x"},
        {"title": "x", "content": 5},
        {"title": "x", "content": " "},
        {"title": None, "content": "text"},
    ],
)
def test_speech_fallback(display, card):
    """Missing or malformed cards retain speech, title, sizing and Info navigation."""
    handler, updates, navigation, _ = display
    handler._async_on_intent_device_change(intent_event(card=card))
    assert updates["title"] == "AI Response"
    assert updates["message"] == "Short speech"
    assert updates["last_said"] == "Short speech"
    navigation.browser_navigate.assert_called_once_with("view-assist/info")


@pytest.mark.parametrize(
    "speech,local", [(None, False), ("*", False), ("Short speech", True)]
)
def test_no_speech_display(display, speech, local):
    """Empty, sentinel and local speech do not force a display change."""
    handler, updates, navigation, _ = display
    handler._async_on_intent_device_change(
        intent_event(speech=speech, card=None, local=local)
    )
    assert "message" not in updates
    navigation.browser_navigate.assert_not_called()


@pytest.mark.parametrize(
    "success,path,key",
    [
        (
            [{"id": "light.kitchen"}, {"id": "todo.shopping"}],
            "custom/intent",
            "intent_entities",
        ),
        ([{"id": "todo.shopping"}], "custom/list", "list"),
    ],
)
def test_intent_priority(display, success, path, key):
    """Successful entity commands and todo lists take precedence over native cards."""
    handler, updates, navigation, _ = display
    handler._async_on_intent_device_change(intent_event(success=success))
    assert key in updates
    assert "message" not in updates
    assert updates["last_said"] == "Short speech"
    navigation.browser_navigate.assert_called_once_with(path)


def test_card_change_with_same_speech(display):
    """Attribute-only changes update the card even when spoken text repeats."""
    handler, updates, navigation, _ = display
    old = intent_event(card={"title": "Old", "content": "Old content"}).data[
        "new_state"
    ]
    handler._async_on_intent_device_change(intent_event(old=old))
    assert updates["message"] == CARD["content"]
    navigation.browser_navigate.assert_called_once()


def test_duplicate_result(display):
    """An unchanged result does not navigate again."""
    handler, updates, navigation, _ = display
    old = intent_event().data["new_state"]
    handler._async_on_intent_device_change(intent_event(old=old))
    assert updates == {}
    navigation.browser_navigate.assert_not_called()


def test_other_success_keeps_existing_fallback(display):
    """Unrecognized successful entity types without a card still do not open Info."""
    handler, updates, navigation, _ = display
    handler._async_on_intent_device_change(
        intent_event(card=None, success=[{"id": "media_player.kitchen"}])
    )
    assert "message" not in updates
    navigation.browser_navigate.assert_not_called()


def test_conversation_event(display):
    """The custom conversation event uses the same native card path."""
    handler, updates, navigation, _ = display
    result = intent_event().data["new_state"].attributes["intent_output"]
    with (
        patch(
            f"{MODULE}.get_sensor_entity_from_instance", return_value="sensor.display"
        ),
        patch(
            f"{MODULE}.get_entity_id_from_conversation_device_id",
            return_value="sensor.display",
        ),
    ):
        handler._async_cc_on_conversation_ended_handler(
            Event("conversation_ended", data={"device_id": "mic", "result": result})
        )
    assert updates["message"] == CARD["content"]
    navigation.browser_navigate.assert_called_once_with("view-assist/info")
