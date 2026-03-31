from requests import Session
from os import environ
from json import load
from dateutil.parser import parse

# Primary URL used to detect updates (x86_64 deb)
PRIMARY_URL = "https://dldir1v6.qq.com/weixin/Universal/Linux/WeChatLinux_x86_64.deb"

x = Session()


def set_output(key: str, value: str):
    """Set the output for GitHub Actions if in a GitHub Actions environment. Also print to stdout for debugging."""
    if "GITHUB_OUTPUT" in environ:
        with open(environ["GITHUB_OUTPUT"], "a") as f:
            f.write(f"{key}={value}\n")
    print(f"{key}={value}")


def last_modified(url: str):
    """Get the last modified date of the file at the specified URL."""
    r = x.head(url)
    date = r.headers.get("Last-Modified")
    print(f"[last_modified] Last-Modified header: {date}")
    return parse(date)


def main():
    release_date = last_modified(PRIMARY_URL)
    with open("versions.json", "r") as f:
        data = load(f)
    released_before = data[-1]["released"] if data else "1970-01-01T00:00:00+00:00"
    released_before = parse(released_before)
    if release_date > released_before:
        print(f"[main] New version found, released on {release_date.isoformat()}")
        set_output("released", release_date.isoformat())
        set_output("url", PRIMARY_URL)
    else:
        print("[main] No new version found.")
        set_output("released", "none")


if __name__ == "__main__":
    main()
