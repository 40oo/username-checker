<div align="center">

<img src="preview.png" alt="checker preview" width="700"/>

<br/>

# username-checker

**Multi-platform username checker — find available usernames fast**

[![Python](https://img.shields.io/badge/Python-3.7+-blue?style=flat-square&logo=python)](https://python.org)
[![Platforms](https://img.shields.io/badge/Platforms-8-cyan?style=flat-square)](#platforms)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)](#)
[![Discord](https://img.shields.io/badge/Discord-Join-7289da?style=flat-square&logo=discord)](https://discord.gg/c95uE5ejff)

<br/>

[**Download**](#installation) • [**Platforms**](#platforms) • [**Usage**](#usage) • [**Discord**](https://discord.gg/c95uE5ejff)

</div>

---

## preview

<div align="center">
<img src="preview.png" alt="checker running" width="650"/>
</div>

---

## video tutorial

<div align="center">

[![Watch Tutorial](https://img.shields.io/badge/Watch%20Tutorial-YouTube-red?style=for-the-badge&logo=youtube)](YOUR_YOUTUBE_LINK)

</div>

---

## platforms

| Platform | Method | Min Length | Speed |
|----------|--------|------------|-------|
| Roblox | Official API | 3 letters | Fast |
| Minecraft | Mojang API | 3 letters | Fast |
| TikTok | Profile pages | 4 letters | Medium |
| YouTube | Profile pages | 4 letters | Medium |
| Twitch | Profile pages | 4 letters | Fast |
| GitHub | Official API | 3 letters | Slow (rate limited) |
| Twitter / X | Profile pages | 4 letters | Slow (rate limited) |
| guns.lol | Profile pages | 3 letters | Fast |

---

## features

- 8 platforms supported in one tool
- 3, 4, 5 and 6 letter username checking
- letters only / letters + numbers / letters + underscore / all combined
- multithreaded — up to 50 threads
- auto saves results to a separate file per platform
- colored terminal UI
- works on Windows, Mac and Linux

---

## installation

**1. clone the repo**
```
git clone https://github.com/40oo/username-checker.git
cd username-checker
```

**2. install dependencies**
```
pip install requests colorama
```

> on Linux / Mac use `pip3` instead of `pip`

**3. run**
```
python username_checker.py
```

> on Linux / Mac use `python3` instead of `python`

---

## usage

when you run the tool it asks you step by step:

```
[ Platform ]    pick which platform to check
[ Length ]      3, 4, 5 or 6 letters
[ Charset ]     letters / letters+numbers / letters+underscore / all
[ Speed ]       normal / fast / turbo
```

press `ENTER` to start — hits get printed live and saved automatically.
press `Ctrl+C` at any time to stop, results already found are kept.

**output files:**
```
available_roblox.txt
available_minecraft.txt
available_tiktok.txt
available_youtube.txt
available_twitch.txt
available_github.txt
available_twitter.txt
available_gunslol.txt
```

---

## tips

- for **GitHub** and **Twitter** use normal speed — they rate limit hard
- for **Roblox** 3-letter names use letters+numbers, pure letters are mostly gone
- results are random every run so everyone checks different names
- if you get lots of `[ERR]` try lowering the thread count

---

## discord

<div align="center">

[![Discord Server](https://img.shields.io/badge/Join%20the%20Discord-7289da?style=for-the-badge&logo=discord&logoColor=white)](https://discord.gg/c95uE5ejff)

join for help, updates and to share your finds

</div>

---

## credits

<div align="center">

made by [40oo](https://github.com/40oo)

</div>
