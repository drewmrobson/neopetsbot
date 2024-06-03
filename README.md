# Overview

My wife recently resurrected her Neopets account and quickly ran into the problem plaguing all internet games - bots. While this didn't impact her enjoyment of the majority of the game, it made using the Stamp Shop impossible as the bots were faster than her to buy rare Stamps when they became available.

Her solution? Ask me to write a bot to compete in the Stamps Shop. I've built a quick'n'dirty bot that does exactly that, and only that. It uses pytest to execute the logic, and Playwright for browser automation.

# Dependencies

Choco is used to initially install Python. `pip` is then used to install the Python dependencies as below. This solution uses `pytest` as the execution handler, and `playwright` as the browser automation tool.

```
choco install python312 -y
pip install playwright
pip install pytest
pip install pytest-playwright
pip install pytest-playwright playwright -U
```

# Running

See [botbot.bat](./botbot.bat) for a Windows batch script that can be used for automation, e.g. Scheduled Task Manager.

To run locally:

`python -m pytest -rP --headed -s > "C:/Source/log.txt"`

`PWDEBUG=1 pytest -s --headed`
