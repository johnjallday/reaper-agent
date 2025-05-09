import platform
import subprocess
import requests
from configparser import ConfigParser
from pathlib import Path

WEB_INTERFACE_PORT = 2307
HOME = Path.home()
REAPER_PATH = HOME / "Library/Application Support/REAPER"

def _rel(p: Path) -> str:
    """Return path relative to $HOME, or absolute if outside."""
    try:
        return str(p.resolve().relative_to(HOME))
    except Exception:
        return str(p)

def web_interface_exists(resource_path: str, port: int) -> bool:
    """
    Return True if a web interface entry for this port is already in reaper.ini.
    """
    ini_path = Path(resource_path) / "reaper.ini"
    config = ConfigParser()
    config.read(ini_path)
    if not config.has_section("REAPER"):
        return False
    for _, val in config["REAPER"].items():
        if f"HTTP 0 {port}" in val:
            return True
    return False

def add_web_interface(resource_path, port=WEB_INTERFACE_PORT):
    """Add a REAPER Web Interface at a specified port (macOS only)."""
    if platform.system() != "Darwin":
        print("Web‐interface setup only on macOS, skipping.")
        return

    ini_path = Path(resource_path) / "reaper.ini"
    config = ConfigParser()
    config.read(ini_path)

    if not config.has_section("REAPER"):
        config.add_section("REAPER")
        config["REAPER"]["csurf_cnt"] = "0"

    count = int(config["REAPER"].get("csurf_cnt", "0"))
    if web_interface_exists(resource_path, port):
        print(f"Web interface already exists in {_rel(ini_path)}, skipping.")
        return

    count += 1
    config["REAPER"]["csurf_cnt"] = str(count)
    key = f"csurf_{count-1}"
    config["REAPER"][key] = f"HTTP 0 {port} '' 'index.html' 0 ''"

    with ini_path.open("w") as fp:
        config.write(fp)

    print(f"Updated {_rel(ini_path)} with port {port}.")

def is_connected(timeout=5, url=None):
    """
    Check HTTP connectivity to the Reaper web interface.
    Returns (success: bool, status_code: int|None).
    """
    if url is None:
        url = f"http://localhost:{WEB_INTERFACE_PORT}/"

    # On non-mac/windows, fall back to python requests
    system = platform.system()
    if system == "Windows":
        try:
            resp = requests.get(url, timeout=timeout)
            return (resp.status_code == 200), resp.status_code
        except requests.RequestException:
            return False, None

    # macOS / Linux: use curl if available
    cmd = ["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}", url]
    try:
        output = subprocess.check_output(cmd, stderr=subprocess.DEVNULL, timeout=timeout)
        code = int(output.decode().strip())
        return (code == 200), code
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired, ValueError):
        return False, None



