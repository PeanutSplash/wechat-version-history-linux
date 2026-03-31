from requests import Session
from json import load, dump
from subprocess import check_output
from os import environ
from os.path import getsize
from hashlib import md5
from argparse import ArgumentParser
from humanize import naturalsize

DOWNLOAD_URLS = {
    "x86_64": {
        "deb": "https://dldir1v6.qq.com/weixin/Universal/Linux/WeChatLinux_x86_64.deb",
        "rpm": "https://dldir1v6.qq.com/weixin/Universal/Linux/WeChatLinux_x86_64.rpm",
        "AppImage": "https://dldir1v6.qq.com/weixin/Universal/Linux/WeChatLinux_x86_64.AppImage",
    },
    "arm64": {
        "deb": "https://dldir1v6.qq.com/weixin/Universal/Linux/WeChatLinux_arm64.deb",
        "rpm": "https://dldir1v6.qq.com/weixin/Universal/Linux/WeChatLinux_arm64.rpm",
        "AppImage": "https://dldir1v6.qq.com/weixin/Universal/Linux/WeChatLinux_arm64.AppImage",
    },
    "LoongArch": {
        "deb": "https://dldir1v6.qq.com/weixin/Universal/Linux/WeChatLinux_LoongArch.deb",
    },
}

x = Session()
parser = ArgumentParser()
parser.add_argument("--released", type=str, help="The date and time of the release.")
parser.add_argument("--url", type=str, help="The URL of the primary package.")
args = parser.parse_args()
newData = {
    "released": args.released,
    "size": -1,
    "md5": "<unknown>",
    "version": "<unknown>",
}


def setOutput(key, value):
    """Set the output for GitHub Actions."""
    if "GITHUB_OUTPUT" in environ:
        with open(environ["GITHUB_OUTPUT"], "a") as f:
            f.write(f"{key}={value}\n")
    print(f"{key}={value}")


def getStat(url, file, directory="./downloads"):
    """Get and validate the stat of the file at the specified URL."""
    r = x.head(url)
    expectedHash = r.headers.get("X-COS-META-MD5")
    path = f"{directory}/{file}"
    with open(path, "rb") as f:
        hash = md5()
        while chunk := f.read(8192):
            hash.update(chunk)
    actualHash = hash.hexdigest()
    expectedSize = int(r.headers.get("Content-Length") or -1)
    actualSize = getsize(path)
    if expectedHash and actualHash != expectedHash:
        print(f"Hash mismatch! Expected: {expectedHash}, Got: {actualHash}")
    if expectedSize > 0 and actualSize != expectedSize:
        print(f"Size mismatch! Expected: {expectedSize}, Got: {actualSize}")
    return actualHash, actualSize


def getVersion():
    """Determines the version from the downloaded deb package."""
    fileName = args.url.split("/")[-1]
    output = check_output(f"dpkg-deb -f ./downloads/{fileName} Version", shell=True)
    version = output.decode("utf-8").strip()
    print(f"[getVersion] Version: {version}")
    return version


def updateJson():
    """Updates `versions.json` if update detected, appending the new version information."""
    with open("versions.json", "r") as f:
        data = load(f)
    print(f"Update detected.")
    data.append(newData)
    with open("versions.json", "w") as f:
        dump(data, f, indent=4)


def generateReleaseNotes():
    """Generate release notes based on the changes."""
    with open("release-notes.md", "w") as f:
        f.write("## Version Info\n")
        f.write(f"- Version: `{newData['version']}`\n")
        f.write(f"- Released: {newData['released']}\n")
        f.write("\n")
        f.write("## Downloads\n\n")
        for arch, formats in DOWNLOAD_URLS.items():
            f.write(f"### {arch}\n")
            for fmt, url in formats.items():
                f.write(f"- [{fmt}]({url})\n")
            f.write("\n")
        f.write("## Primary Package (x86_64 deb)\n")
        f.write(f"- Size: {naturalsize(newData['size'])}\n")
        f.write(f"- MD5: `{newData['md5']}`\n")
        f.write("\n")


def main():
    newData["version"] = getVersion()
    md5Hash, size = getStat(args.url, args.url.split("/")[-1])
    newData["md5"] = md5Hash
    newData["size"] = size
    updateJson()
    generateReleaseNotes()
    setOutput("version", newData["version"])


if __name__ == "__main__":
    main()
