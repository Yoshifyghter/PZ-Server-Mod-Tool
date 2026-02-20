import os, re, winreg

APPID = "108600"

def get_steam_path():
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Valve\Steam")
        value, _ = winreg.QueryValueEx(key, "SteamPath")
        return value.replace("/", "\\")
    except:
        return None


def get_libraries():
    steam = get_steam_path()
    if not steam:
        return []

    libs = [steam]
    vdf = os.path.join(steam, "steamapps", "libraryfolders.vdf")

    if os.path.exists(vdf):
        text = open(vdf, encoding="utf8", errors="ignore").read()
        matches = re.findall(r'"path"\s+"([^"]+)"', text)

        for m in matches:
            p = m.replace("\\\\","\\")
            if os.path.exists(p):
                libs.append(p)

    return list(set(libs))


def find_game():
    for lib in get_libraries():
        common = os.path.join(lib,"steamapps","common")
        if not os.path.exists(common):
            continue

        for folder in os.listdir(common):
            if "zomboid" in folder.lower():
                return os.path.join(common,folder)

    return None


def find_workshop():
    for lib in get_libraries():
        p = os.path.join(lib,"steamapps","workshop","content",APPID)
        if os.path.exists(p):
            return p
    return None