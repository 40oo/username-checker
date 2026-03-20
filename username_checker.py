import requests
import time
import random
import threading
import string
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from datetime import datetime

try:
    from colorama import Fore, Style, init
    init(autoreset=True)
    HAS_COLOR = True
except ImportError:
    HAS_COLOR = False

# settings
THREADS = 25
DELAY = 0.05
RETRIES = 3
VERSION = "1.0"
AUTHOR = "0fbq"

outdir = os.path.dirname(os.path.abspath(__file__))

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"

lock = threading.Lock()
checked = 0
found = 0
errors = 0
total = 0
tlocal = threading.local()

letters = list(string.ascii_lowercase)
digits = list(string.digits)
vowels = list("aeiou")
cons = list("bcdfghjklmnprstvwxyz")

cool_starts = [
    "kr", "dr", "br", "gr", "tr", "pr",
    "bl", "cl", "fl", "gl", "sl",
    "sk", "sp", "st", "sw",
    "zr", "vr", "sh", "ch", "nx", "vx", "zx",
]

pat3 = ["CVC", "CVV", "VCV", "VCC", "CCV", "VVC"]
pat4 = ["CVCC", "CVCV", "CCVC", "VCVC", "CVVC", "VCCV", "CCVV", "VVCV"]
pat5 = ["CVCCV", "CVCVC", "CCVCV", "VCVCV", "CVCVV", "CVVCV", "CCVCC", "VCCVC"]
pat6 = ["CVCCVC", "CVCVCV", "CVVCVC", "CCVCVC", "VCVCVC", "CVCVVC", "CVCCVV"]

# platform definitions
PLATFORMS = {
    "1": {
        "name": "Roblox",
        "file": "available_roblox.txt",
        "check": "roblox",
        "min_len": 3,
        "note": ""
    },
    "2": {
        "name": "Minecraft",
        "file": "available_minecraft.txt",
        "check": "minecraft",
        "min_len": 3,
        "note": ""
    },
    "3": {
        "name": "TikTok",
        "file": "available_tiktok.txt",
        "check": "tiktok",
        "min_len": 4,
        "note": "checks tiktok.com/@username"
    },
    "4": {
        "name": "YouTube",
        "file": "available_youtube.txt",
        "check": "youtube",
        "min_len": 4,
        "note": "checks youtube.com/@username"
    },
    "5": {
        "name": "Twitch",
        "file": "available_twitch.txt",
        "check": "twitch",
        "min_len": 4,
        "note": "checks twitch.tv/username"
    },
    "6": {
        "name": "GitHub",
        "file": "available_github.txt",
        "check": "github",
        "min_len": 3,
        "note": "60 req/hour limit — use normal speed"
    },
    "7": {
        "name": "Twitter / X",
        "file": "available_twitter.txt",
        "check": "twitter",
        "min_len": 4,
        "note": "strict rate limits — use normal speed"
    },
    "8": {
        "name": "guns.lol",
        "file": "available_gunslol.txt",
        "check": "gunslol",
        "min_len": 3,
        "note": "checks guns.lol/username"
    },
}


def col(txt, clr):
    if not HAS_COLOR:
        return txt
    m = {
        "red": Fore.RED,
        "green": Fore.GREEN,
        "yellow": Fore.YELLOW,
        "cyan": Fore.CYAN,
        "white": Fore.WHITE,
        "gray": Fore.WHITE + Style.DIM,
    }
    return m.get(clr, "") + str(txt) + Style.RESET_ALL


def banner():
    os.system("cls" if os.name == "nt" else "clear")
    print()
    print(col("   ██████╗██╗  ██╗███████╗ ██████╗██╗  ██╗███████╗██████╗ ", "cyan"))
    print(col("  ██╔════╝██║  ██║██╔════╝██╔════╝██║ ██╔╝██╔════╝██╔══██╗", "cyan"))
    print(col("  ██║     ███████║█████╗  ██║     █████╔╝ █████╗  ██████╔╝", "cyan"))
    print(col("  ██║     ██╔══██║██╔══╝  ██║     ██╔═██╗ ██╔══╝  ██╔══██╗", "cyan"))
    print(col("  ╚██████╗██║  ██║███████╗╚██████╗██║  ██╗███████╗██║  ██║", "cyan"))
    print(col("   ╚═════╝╚═╝  ╚═╝╚══════╝ ╚═════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝", "cyan"))
    print()
    print(col(f"  Multi-Platform Username Checker v{VERSION}  |  by {AUTHOR}", "gray"))
    print(col("  " + "-" * 55, "gray"))
    print()


def hdr(title):
    print(col(f"\n  [ {title} ]", "cyan"))
    print(col("  " + "-" * 44, "gray"))


def ask(txt):
    return input(col("  > ", "cyan") + col(txt + " ", "white")).strip()


def option(k, lbl, note=""):
    line = col(f"  [{k}]", "yellow") + col(f"  {lbl}", "white")
    if note:
        line += col(f"  ({note})", "gray")
    print(line)


def draw_status(name, res):
    pct = int((checked / total) * 100) if total > 0 else 0
    bar = "#" * (pct // 5) + "-" * (20 - pct // 5)
    if res is True:
        tag = col("  [HIT]  ", "green")
    elif res is False:
        tag = col("  [----] ", "gray")
    else:
        tag = col("  [ERR]  ", "yellow")
    print(
        f"\r{tag}" + col(name.ljust(14), "white")
        + col(f"  [{bar}] {pct}%", "gray")
        + col(f"  {checked}/{total}", "gray")
        + col(f"  hits: {found}", "green"),
        end="", flush=True
    )


def get_sess():
    if not hasattr(tlocal, "sess"):
        s = requests.Session()
        s.headers.update({
            "User-Agent": UA,
            "Accept-Language": "en-US,en;q=0.9",
        })
        adp = HTTPAdapter(
            pool_connections=THREADS,
            pool_maxsize=THREADS,
            max_retries=Retry(total=2, backoff_factor=0.3)
        )
        s.mount("https://", adp)
        tlocal.sess = s
    return tlocal.sess


# ── platform checkers ──────────────────────────────────────────

def check_roblox(name):
    url = "https://auth.roblox.com/v1/usernames/validate"
    p = {"request.username": name, "request.birthday": "2000-01-01", "request.context": "signup"}
    sess = get_sess()
    for attempt in range(RETRIES):
        try:
            r = sess.get(url, params=p, timeout=6)
            if r.status_code == 200:
                code = r.json().get("code", -1)
                if code == 0: return True
                elif code == 1: return False
                else: return None
            elif r.status_code == 429:
                time.sleep(5 * (attempt + 1))
            else:
                return None
        except: time.sleep(1)
    return None


def check_minecraft(name):
    sess = get_sess()
    for attempt in range(RETRIES):
        try:
            r = sess.get(f"https://api.mojang.com/users/profiles/minecraft/{name}", timeout=6)
            if r.status_code == 404: return True
            elif r.status_code == 200: return False
            elif r.status_code == 429: time.sleep(5 * (attempt + 1))
            else: return None
        except: time.sleep(1)
    return None


def check_tiktok(name):
    sess = get_sess()
    for attempt in range(RETRIES):
        try:
            r = sess.get(f"https://www.tiktok.com/@{name}", timeout=8, allow_redirects=True)
            if r.status_code == 404: return True
            elif r.status_code == 200: return False
            elif r.status_code == 429: time.sleep(8 * (attempt + 1))
            else: return None
        except: time.sleep(2)
    return None


def check_youtube(name):
    sess = get_sess()
    for attempt in range(RETRIES):
        try:
            r = sess.get(f"https://www.youtube.com/@{name}", timeout=8, allow_redirects=True)
            if r.status_code == 404: return True
            elif r.status_code == 200: return False
            elif r.status_code == 429: time.sleep(8 * (attempt + 1))
            else: return None
        except: time.sleep(2)
    return None


def check_twitch(name):
    sess = get_sess()
    for attempt in range(RETRIES):
        try:
            r = sess.get(f"https://www.twitch.tv/{name}", timeout=6, allow_redirects=True)
            if r.status_code == 404: return True
            elif r.status_code == 200: return False
            elif r.status_code == 429: time.sleep(5 * (attempt + 1))
            else: return None
        except: time.sleep(1)
    return None


def check_github(name):
    sess = get_sess()
    for attempt in range(RETRIES):
        try:
            r = sess.get(f"https://api.github.com/users/{name}", timeout=6)
            if r.status_code == 404: return True
            elif r.status_code == 200: return False
            elif r.status_code in [429, 403]:
                time.sleep(10 * (attempt + 1))
            else: return None
        except: time.sleep(1)
    return None


def check_twitter(name):
    sess = get_sess()
    for attempt in range(RETRIES):
        try:
            r = sess.get(f"https://x.com/{name}", timeout=8, allow_redirects=True)
            if r.status_code == 404: return True
            elif r.status_code == 200: return False
            elif r.status_code == 429: time.sleep(10 * (attempt + 1))
            else: return None
        except: time.sleep(2)
    return None


def check_gunslol(name):
    sess = get_sess()
    for attempt in range(RETRIES):
        try:
            r = sess.get(f"https://guns.lol/{name}", timeout=6, allow_redirects=True)
            if r.status_code == 404: return True
            elif r.status_code == 200: return False
            elif r.status_code == 429: time.sleep(5 * (attempt + 1))
            else: return None
        except: time.sleep(1)
    return None


CHECKERS = {
    "roblox": check_roblox,
    "minecraft": check_minecraft,
    "tiktok": check_tiktok,
    "youtube": check_youtube,
    "twitch": check_twitch,
    "github": check_github,
    "twitter": check_twitter,
    "gunslol": check_gunslol,
}


def worker(name, hits, outfile, checker_fn):
    global checked, found, errors

    time.sleep(DELAY + random.uniform(0, 0.1))
    res = checker_fn(name)

    with lock:
        checked += 1
        if res is True:
            found += 1
            hits.append(name)
            with open(outfile, "a") as f:
                f.write(name + "\n")
            print()
            print(col(f"  [AVAILABLE]  {name}", "green") + col(f"  [{datetime.now().strftime('%H:%M:%S')}]", "gray"))
        elif res is False:
            draw_status(name, False)
        else:
            errors += 1
            draw_status(name, None)


# ── name generators ────────────────────────────────────────────

def make_letter_names(length, count=80000):
    names = set()
    pats = pat3 if length == 3 else pat4 if length == 4 else pat5 if length == 5 else pat6
    for pat in pats:
        for _ in range(3000):
            n = ""
            for ch in pat:
                n += random.choice(vowels if ch == "V" else cons)
            if len(n) == length:
                names.add(n)
    for start in cool_starts:
        if len(start) >= length:
            continue
        for _ in range(400):
            fill = ""
            was_v = start[-1] in vowels
            for i in range(length - len(start)):
                if was_v:
                    ch = random.choice(cons)
                else:
                    ch = random.choice(vowels) if random.random() > 0.3 else random.choice(cons)
                fill += ch
                was_v = ch in vowels
            n = start + fill
            if len(n) == length:
                names.add(n)
    while len(names) < count:
        n = ""
        sc = random.random() > 0.3
        for i in range(length):
            if (i % 2 == 0 and sc) or (i % 2 == 1 and not sc):
                n += random.choice(cons)
            else:
                n += random.choice(vowels)
        if n[0].isalpha():
            names.add(n)
    out = list(names)
    random.shuffle(out)
    return out[:count]


def make_num_names(length, count=80000):
    names = set()
    while len(names) < count:
        n = [random.choice(letters)]
        for i in range(length - 1):
            if random.random() < 0.65:
                n.append(random.choice(letters))
            else:
                n.append(random.choice(digits))
        names.add("".join(n))
    out = list(names)
    random.shuffle(out)
    return out[:count]


def make_underscore_names(length, count=80000):
    names = set()
    while len(names) < count:
        n = [random.choice(letters)]
        used_us = False
        for i in range(length - 1):
            r = random.random()
            if r < 0.75 or used_us:
                n.append(random.choice(letters))
            else:
                if n[-1] != "_" and i != length - 2:
                    n.append("_")
                    used_us = True
                else:
                    n.append(random.choice(letters))
        s = "".join(n)
        if not s.endswith("_"):
            names.add(s)
    out = list(names)
    random.shuffle(out)
    return out[:count]


def make_all(length, count=80000):
    names = set()
    while len(names) < count:
        n = [random.choice(letters)]
        used_us = False
        for i in range(length - 1):
            r = random.random()
            if r < 0.55:
                n.append(random.choice(letters))
            elif r < 0.85:
                n.append(random.choice(digits))
            else:
                if not used_us and n[-1] != "_" and i != length - 2:
                    n.append("_")
                    used_us = True
                else:
                    n.append(random.choice(letters))
        s = "".join(n)
        if not s.endswith("_"):
            names.add(s)
    out = list(names)
    random.shuffle(out)
    return out[:count]


def main():
    global checked, found, errors, total

    banner()

    # platform
    hdr("Platform")
    for k, v in PLATFORMS.items():
        option(k, v["name"], v["note"])
    pc = ask("Choose platform:")
    while pc not in PLATFORMS:
        print(col(f"  enter 1-{len(PLATFORMS)}", "red"))
        pc = ask("Choose platform:")
    platform = PLATFORMS[pc]

    # length
    hdr("Length")
    min_l = platform["min_len"]
    lengths = [l for l in [3, 4, 5, 6] if l >= min_l]
    for i, l in enumerate(lengths, 1):
        option(str(i), f"{l} letters")
    lc = ask("Choose length:")
    while not lc.isdigit() or int(lc) not in range(1, len(lengths) + 1):
        print(col(f"  enter 1-{len(lengths)}", "red"))
        lc = ask("Choose length:")
    length = lengths[int(lc) - 1]

    # charset
    hdr("Character Set")
    option("1", "Letters only          (a-z)")
    option("2", "Letters + numbers     (a-z, 0-9)")
    option("3", "Letters + underscore  (a-z, _)")
    option("4", "All                   (a-z, 0-9, _)")
    cc = ask("Choose charset:")
    while cc not in ["1", "2", "3", "4"]:
        print(col("  enter 1-4", "red"))
        cc = ask("Choose charset:")

    # speed — github and twitter need lower threads
    hdr("Speed")
    if platform["check"] in ["github", "twitter"]:
        option("1", "Normal   (5 threads)   -- recommended for this platform")
        option("2", "Fast     (10 threads)")
        option("3", "Turbo    (20 threads)")
        threads = {"1": 5, "2": 10, "3": 20}.get(ask("Choose speed:"), 5)
    else:
        option("1", "Normal   (15 threads)")
        option("2", "Fast     (25 threads)")
        option("3", "Turbo    (50 threads)")
        threads = {"1": 15, "2": 25, "3": 50}.get(ask("Choose speed:"), 25)

    # generate
    hdr("Generating")
    print(col("  generating, please wait...", "gray"))

    if cc == "1":
        names = make_letter_names(length)
    elif cc == "2":
        names = make_num_names(length)
    elif cc == "3":
        names = make_underscore_names(length)
    else:
        names = make_all(length)

    random.shuffle(names)
    total = len(names)
    print(col(f"  {total:,} usernames ready", "green"))

    clabels = {"1": "letters only", "2": "letters + numbers", "3": "letters + underscore", "4": "all"}
    outfile = os.path.join(outdir, platform["file"])

    hdr("Summary")
    print(col("  Platform   ", "gray") + col(platform["name"], "white"))
    print(col("  Length     ", "gray") + col(f"{length}-letter", "white"))
    print(col("  Charset    ", "gray") + col(clabels[cc], "white"))
    print(col("  Threads    ", "gray") + col(str(threads), "white"))
    print(col("  Usernames  ", "gray") + col(f"{total:,}", "white"))
    print(col("  Sample     ", "gray") + col(", ".join(names[:6]), "white"))
    print()

    input(col("  Press ENTER to start  |  Ctrl+C to stop\n", "yellow"))

    checked = 0
    found = 0
    errors = 0
    hits = []
    checker_fn = CHECKERS[platform["check"]]

    with open(outfile, "w") as f:
        f.write(f"# {platform['name']} available usernames\n")
        f.write(f"# by {AUTHOR}  |  {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

    hdr("Checking")
    t0 = time.time()

    try:
        with ThreadPoolExecutor(max_workers=threads) as ex:
            futs = {ex.submit(worker, u, hits, outfile, checker_fn): u for u in names}
            for ft in as_completed(futs):
                try:
                    ft.result()
                except Exception:
                    pass
    except KeyboardInterrupt:
        print(col("\n\n  stopped.", "red"))

    elapsed = time.time() - t0
    rate = checked / elapsed if elapsed > 0 else 0

    print()
    hdr("Results")
    print(col("  Platform  ", "gray") + col(platform["name"], "white"))
    print(col("  Checked   ", "gray") + col(f"{checked:,}", "white"))
    print(col("  Time      ", "gray") + col(f"{elapsed:.1f}s  ({rate:.1f}/sec)", "white"))
    print(col("  Found     ", "gray") + col(str(len(hits)), "green" if hits else "white"))

    if hits:
        print()
        print(col("  available:", "green"))
        for h in hits:
            print(col(f"    -> {h}", "green"))

    print()
    print(col("  " + "-" * 45, "gray"))
    print(col(f"  checker by {AUTHOR}", "cyan"))
    print()


if __name__ == "__main__":
    main()
