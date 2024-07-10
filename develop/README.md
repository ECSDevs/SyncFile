# Syncfile

- Current Version (this tag/branch): `v3-0.3.1.2`
- Current Status: `Beta`
- Published at: [PyPI](https://pypi.org/project/syncfile/)

## Notice

The original `Syncfile` project has been renamed to `Syncfile`.

**TRY `Syncfile v3-0.2.13.6` INSTEAD OF THIS**:
```sh
python -m pip install --user --force-reinstall Syncfile==0.2.13.6 -i https://mirrors.tuna.tsinghua.edu.cn/pypi/simple
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
