# Patch validation

Validated on 12 October 2026 against upstream `main` at
`6e77c688a416cd7c47caded72993e0ee3720ee41`, using Home Assistant Core development
source at `9942caba481e51760915abb788620bf25e492104` and Linux Python 3.14.8.

- `python -m pytest -q tests/test_native_response_card.py`: **23 passed**.
- Ruff checks on the new test files: passed.
- Ruff syntax/error checks (`E9,F63,F7,F82`) on the changed runtime module: passed.
- Ruff formatting checks on the changed runtime module and tests: passed.
- Python 3.14 compilation and `git diff --check`: passed.

The tests execute the actual event callbacks with a minimal device config and
mock navigation/dispatcher boundaries. They verify title assignment after
navigation clears it, card-based font sizing, separate speech, configured
entity/todo destinations and priority, local/sentinel/absent speech, malformed
cards, repeat speech with changed cards, unchanged results, and the custom
conversation-ended event.

No real microphone, browser dashboard or Gemini account was used. Follow
`NATIVE_RESPONSE_CARDS.md` for installation and the hardware test checklist.
