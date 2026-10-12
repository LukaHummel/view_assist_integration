# Native Home Assistant response cards

View Assist now displays `intent_output.response.card.simple.title` and `.content`
on the existing `view-assist/info` screen. Card content determines the message font
size, while `last_said` remains the spoken response. Navigation still happens
before setting the title/message, preserving title clearing and the usual revert
timer. No dashboard changes are needed.

Successful light/switch/cover/boolean/input_boolean/fan results still open the
configured intent view. Todo results still open the configured list view. These
take priority over the card, with entity results taking priority over todo results.
A card is displayable even for a locally processed response or when speech is
absent/`*`. Missing, unsupported or malformed cards use the existing non-local
speech fallback; empty speech and `*` do not navigate to Info. Attribute-only card
changes are processed even when the spoken text is unchanged.
Successful results for other entity types without a card retain the existing
behavior of not forcing the speech fallback onto the Info screen.

Both the configured intent sensor and the custom conversation-ended event use
this handling. The upstream integration's existing microphone/event wiring still
determines which device receives the result. This patch does not add an intent
sensor or make a new satellite integration emit conversation events.

## Install

For a test Home Assistant instance, download the feature branch or clone it:

```sh
git clone --branch feature/native-simple-response-cards https://github.com/LukaHummel/view_assist_integration.git
```

Back up the existing `config/custom_components/view_assist` directory. Replace it
with the complete `custom_components/view_assist` directory from this checkout,
then restart Home Assistant. Keep your existing View Assist configuration and
dashboard. Use manual installation for this feature branch: HACS may otherwise
install a release or the default branch instead. To uninstall, restore the saved
integration directory and restart.

For Gemini-generated cards, also install the Core fork's
`feature/gemini-intent-response-cards` branch and enable **Separate spoken and
display responses** on the Google Gemini conversation agent. See that fork's
`STRUCTURED_RESPONSES.md` for source-install instructions. This View Assist patch
also works with other agents that already return native simple cards.

## Verify

1. Ask for a detailed answer. Verify Info shows the card title and detailed text,
   while the sensor's `last_said` and TTS contain the concise spoken answer.
2. Turn on an exposed light and modify a todo list. Verify the existing configured
   intent/list views win, even if a native card is present.
3. Test a normal agent response without a card. Verify the existing “AI Response”
   display, speech font sizing, navigation and view timeout still work.
4. Inspect your intent sensor's `intent_output` attribute to confirm that the
   complete `response.card.simple` is reaching View Assist. For event-driven
   microphones, inspect their existing conversation-ended event instead.

The callback regression tests can run in a Linux Python environment with the
matching Home Assistant Core development version, this integration's manifest
requirements and pytest installed. From this checkout:

```sh
python3 -m pytest -q tests/test_native_response_card.py
```

They exercise actual callback navigation/update behavior, entity/todo priority,
malformed/missing cards, missing speech, sentinel/local speech, repeat speech with
changed cards, duplicate events and the custom conversation event path.

See `PATCH_VALIDATION.md` for checks actually run.
