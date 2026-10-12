# Welcome

[![hacs_badge](https://img.shields.io/badge/HACS-Default-orange.svg?style=for-the-badge)](https://github.com/hacs/integration)
[![version](https://shields.io/github/v/release/dinki/view_assist_integration?style=for-the-badge)](https://github.com/dinki/view_assist_integration)
[![Latest Release](https://img.shields.io/badge/dynamic/json?style=for-the-badge&color=41BDF5&logo=home-assistant&label=integration%20usage&suffix=%20installs&cacheSeconds=15600&url=https://analytics.home-assistant.io/custom_integrations.json&query=$.view_assist.total)](https://analytics.home-assistant.io/custom_integrations.json)

Welcome to the long awaited, much anticipated View Assist integration!  

A HUGE thank you goes out to Mark Parker @msp1974 for his MASSIVE help with making this a reality.  Mark has written the majority of the integration with my guidance.  You should check out his [Home Assistant Integration Examples](https://github.com/msp1974/HAIntegrationExamples) Github if you are intestered in creating your own integration.  His work has propelled View Assist to first class in very short order.  We would not be where we are today without his continued efforts and the hours and hours he has put in to make View Assist better!  Thanks again Mark!


# Installing the View Assist Integration

[![Image](https://img.youtube.com/vi/cYqGGknf4C8/mqdefault.jpg)](https://www.youtube.com/watch?v=cYqGGknf4C8)


Watch Video: https://www.youtube.com/watch?v=cYqGGknf4C8


## HACS
* Install HACS if you have not already
* Open HACS and click three dots in right corner -> Custom Repositories -> then paste `https://github.com/dinki/view_assist_integration/` in 'Repository' and choose type 'Integration' then click 'Add'
* Now search for 'View Assist' in HACS
* Click "Add" to confirm, and then click "Download" to download and install the integration
Restart Home Assistant
* Search for "View Assist" in HACS and install then restart
* In Home Assistant go to Settings -> Devices and Services -> Add integration -> Search for View Assist and add
* Configure the device(s)

## Manual Install

This integration can be installed by downloading the [view_assist](https://github.com/dinki/view_assist_integration/tree/main/custom_components) directory into your Home Assistant /config/custom_components directory and then restart Home Assistant.  We have plans to make this easier through HACS but are waiting for acceptance.

Questions, problems, concerns?  Reach out to us on Discord or use the 'Issues' above

## View Assist Companion App

We strongly suggest Android users use our [View Assist Companion App](https://github.com/msp1974/ViewAssist_Companion_App) in conjunction with the View Assist Integration.  This app greatly simplifies the process of get things goiung.  Follow the link for more information.

## Native response cards

When a conversation agent returns a native Home Assistant simple card, View
Assist displays its title and content on the Info screen. The card text controls
font sizing, while `last_said` remains the spoken response. Cards also work with
local responses or absent speech, and changed cards update even if speech repeats.

Successful supported entity commands and todo results keep their configured
intent/list views and take priority over cards. Missing or malformed cards retain
the usual non-local speech fallback. Both the configured intent sensor and the
custom conversation-ended event support cards through their existing device
routing. The usual view timeout still applies.

## Development tests

Use Linux with Python **3.14.8**. The test requirements pin Home Assistant Core to
commit `9942caba481e51760915abb788620bf25e492104` and include the integration's
dependencies, pytest and Ruff. From the repository root:

```sh
python3.14 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements-test.txt
python -m pytest -q
python -m ruff check --select E9,F63,F7,F82 custom_components/view_assist/devices/entity_listeners.py
python -m ruff check tests
python -m ruff format --check custom_components/view_assist/devices/entity_listeners.py tests
```

GitHub Actions runs these checks with the same Python version and requirements.
The callback tests cover cards, speech fallback, entity/todo priority, repeated
speech, duplicate results and conversation events. They mock navigation and
dispatcher boundaries; microphone input, TTS, rendering and view reversion still
require a running Home Assistant instance.

To update the dependency pins, edit `requirements-test.in` and regenerate
`requirements-test.txt` with the pinned environment's uv:

```sh
uv pip compile --python 3.14.8 requirements-test.in --output-file requirements-test.txt
```

# Help

Need help?  Check our [View Assist Wiki](https://dinki.github.io/View-Assist/) for the most up-to-date documentation.  You can also hop on our [View Assist Discord Server](https://discord.gg/3WXXfGAf8T) and we'll give you a boost!
