# MCSMT ( Minecraft Server Manage Tool)
Version 3
0.3.1 (v3X)

## Changes
All changes in this release are **breaking and completely refactored** (refactored project architecture, removed redundant code, core implementation principles remain unchanged).
Users of previous versions of the program may need to change their strategies to adapt to these changes and to receive subsequent security and feature updates.

### Specific Changes
- Removed all code from the original `MCSMTApi`
- Created `__main__.py` and added documentation
- Included GPL license declaration
- Moved `client/main.py` to `client.py`
- Moved `mixed/down.py` to `down.py`
- Merged `mixed/ezdns.py` into `down.py`
- Moved `server/gen.py` to `server.py`
- Removed other code (binary builds, Watchdog, EZDNS, etc.)

## Trends
Expected upcoming merges/removals:
- Merge all code in `down.py` into one place and integrate into `client.py`

## Disclaimer
Due to limited resources, bugs may not be fixed in a timely manner, please do not use for production purposes!

## Others
[Github Wiki](https://github.com/ECSDevs/MCSMT/wiki/)

