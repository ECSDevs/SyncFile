# MCSMT (Minecraft Server Management Tool)

[Chinese/中文](README.md)

Discussion in QQ channel: Channel number: r2mjr3649b, Channel name: RIAN Really Plays, discuss in the 【Project-related】 section

## How to Run

.whl File:
```bash
pip install <whl file path> --force-reinstall
```
New versions can only be installed using .whl/.tar.gz

**2023/9/7 Update: Full support for MCSMTApi, start with MCSMT CLI**

## Server Side

1. First, generate the server configuration with `python -m mcsmt server genconf`

2.1. Static Server Side

2.1.1. Run `python -m mcsmt server gen`, package and send it after generation, then upload it to the server

2.2. Dynamic Server Side

2.2.1. Directly start `python -m http.server <port>` to start a convenient server (2023/9/7 Change: The built-in simple server has been removed, please use Python's own server or IIS, etc.)

2.2.3. Automatically generated: Start `python -m mcsmt server wdgen` to automatically detect changes in files and generate them (currently unstable)

## Client
Write a `Cconfig.json` like this:
```json
{
    "requestURL": "http://api.example.com/"
}
```
Start `python -m mcsmt client main` to sync

## Tools

### mod Downloader

A mod downloader, you need to apply for a developer account ondocs.curseforge.com yourself. After logging in, copy the token on the left side of the API, paste it into the tool, and then start it. Run mode: `python -m mcsmt mixed moddown`

### Extension Downloader

`python -m mcsmt mixed extdown`

## MCSMTApi

Since Alpha Version 3.0.2.12.0, MCSMT has started to use MCSMTApi as the new calling method, and the old python module calling method has been retired.

For more information, please see the QQ channel.