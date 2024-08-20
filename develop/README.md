<!--
 Copyright 2024 ECSDevs
 
 Licensed under the Apache License, Version 2.0 (the "License");
 you may not use this file except in compliance with the License.
 You may obtain a copy of the License at
 
     https://www.apache.org/licenses/LICENSE-2.0
 
 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing permissions and
 limitations under the License.
-->

# Syncfile

- Current Version (this tag/branch): `v3-0.3.1.2`
- Current Status: `Beta`
- Published at: [PyPI](https://pypi.org/project/syncfile/)

## Notice

The original `MCSMT` project has been renamed to `Syncfile`.

**TRY `MCSMT v3-0.2.13.6` INSTEAD OF THIS**:
```sh
python -m pip install --user --force-reinstall mcsmt==0.2.13.6 -i https://mirrors.tuna.tsinghua.edu.cn/pypi/simple
```

The following versions of `Syncfile` has been `yanked`:
- `0.2.13.0` ~ `0.2.13.1` (PyPI version)

## Changes
All changes in this release are **breaking and completely refactored** (refactored project architecture, removed redundant code, but core implementation principles remain unchanged).
Users of previous versions of the program may need to change their strategies to adapt to these changes and to receive subsequent security and feature updates.

### Specific Changes
- Removed all code from the original `SyncfileApi`
- Created `__main__.py` and added documentation
- Included GPL license declaration
- Moved `client/main.py` to `client.py`
- Moved `mixed/down.py` to `down.py`
- Merged `mixed/ezdns.py` into `down.py`
- Moved `server/gen.py` to `server.py`
- Removed other code (binary builds, Watchdog, EZDNS, etc.)

## Trends
Expected new features:
- Current nothing

Expected removals:
- Current nothing

## Disclaimer
Due to limited resources, bugs may not be fixed in a timely manner, please do not use for production purposes!

## Others
- **Wiki for old versions**: [Github Wiki](https://github.com/ECSDevs/Syncfile/wiki/)
- **Wiki for new versions(v3X) (Chinese)**: [v3x.sf.ptoe.cc](https://v3x.sf.ptoe.cc/)
