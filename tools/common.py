from textfmt import slug

REPO = "acarbayk/aurora-world-of-warcraft"
BASE = f"https://raw.githubusercontent.com/{REPO}/main"
import os
ED = os.environ.get("ED", "2024")
SOURCE = "World of Warcraft" if ED == "2024" else "World of Warcraft (2014)"
PREFIX = "ID_KAYA_WOW" if ED == "2024" else "ID_KAYA_WOW14"
FP = "wow-" if ED == "2024" else "wow14-"
ROOT = "/home/claude/aurora-world-of-warcraft"


def idp(kind, name):
    return f"{PREFIX}_{kind}_{slug(name)}"


def header(path, name, desc, version="1.2.1"):
    """path is relative to the world-of-warcraft/ folder."""
    fname = path.split("/")[-1]
    return f'''<?xml version="1.0" encoding="utf-8" ?>
<elements>
	<info>
		<name>{name}</name>
		<description>{desc}</description>
		<author url="https://github.com/{REPO}">Andrey Kuzinskiy (book), converted by Kaya Acarbay</author>
		<update version="{version}">
			<file name="{fname}" url="{BASE}/world-of-warcraft/{path}" />
		</update>
	</info>

'''


def footer():
    return "\n\n</elements>\n"
