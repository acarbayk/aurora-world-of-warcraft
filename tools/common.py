from textfmt import slug

REPO = "acarbayk/aurora-world-of-warcraft"
BASE = f"https://raw.githubusercontent.com/{REPO}/main"
SOURCE = "World of Warcraft"
PREFIX = "ID_KAYA_WOW"
ROOT = "/home/claude/aurora-world-of-warcraft"


def idp(kind, name):
    return f"{PREFIX}_{kind}_{slug(name)}"


def header(path, name, desc, version="0.1.0"):
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
