#!/usr/bin/env python3
"""Build the uploadable plugin archives from plugin/.

  python3 scripts/build-plugin.py            # writes dist/

One source folder, three things to hand over, because each place reads its own
files and refuses or ignores the others:

  dist/mindvest-atlas-chatgpt.zip       ChatGPT and Codex: plugin.json, mcp.json,
                                        skills/, assets/. Upload on the OpenAI
                                        platform's Plugins page. This one is an
                                        EDITION: plugin/ with plugin-chatgpt/
                                        laid over it (see that folder's
                                        edition.json). It has no skill that
                                        places, changes or closes a trade.
  dist/mindvest-atlas-claude-code.zip   Claude Code: .claude-plugin/plugin.json,
                                        .mcp.json, skills/.
  dist/claude-skills/<skill>.zip        One per skill, for Claude's own
                                        "upload a skill" (it takes one at a time).

Nothing secret goes in: the archives carry the server's address and no key.
A person signs in to Atlas in their browser when the plugin first connects.
"""
import json
import os
import sys
import zipfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "plugin")
DIST = os.path.join(ROOT, "dist")

# What each archive takes from plugin/ (top-level names).
CHATGPT = {"plugin.json", "mcp.json", "skills", "assets"}
CLAUDE_CODE = {".claude-plugin", ".mcp.json", "skills"}
# OpenAI only takes an upload whose plugin.json `name` is the id of the plugin
# it replaces ("Plugin name must match the existing plugin", 2026-10-09). This
# is that plugin's id; the name people see is `displayName`. Claude Code reads
# its own file (.claude-plugin/plugin.json), which keeps the readable name.
OPENAI_PLUGIN_NAME = "app-699926e1ef3c8191b1da3adb6ba431b7"
# The categories OpenAI's own plugin list uses, spelled as it spells them. Its
# upload page answers "Select a valid category" to anything else ("finance" in
# lower case was refused, 2026-10-09).
OPENAI_CATEGORIES = {
    "Developer Tools", "Productivity", "Creativity", "Communication", "Education & Research",
    "Data & Analytics", "Finance", "Business & Operations", "Scientific Research", "Security",
}
# Never shipped, whoever asks.
NEVER = {".DS_Store", "__pycache__", ".git"}
SECRET_WORDS = ("Bearer ", "api_key", "apikey", "secret", "password", "token=")


def files_under(top: set[str]) -> list[str]:
    out = []
    for name in sorted(os.listdir(SRC)):
        if name not in top or name in NEVER:
            continue
        path = os.path.join(SRC, name)
        if os.path.isfile(path):
            out.append(name)
            continue
        for base, dirs, files in os.walk(path):
            dirs[:] = sorted(d for d in dirs if d not in NEVER)
            for f in sorted(files):
                if f not in NEVER:
                    out.append(os.path.relpath(os.path.join(base, f), SRC))
    return out


def check() -> list[str]:
    """What would make an upload fail, found here instead of there."""
    wrong = []
    manifest = json.load(open(os.path.join(SRC, "plugin.json")))
    face = manifest["extensions"]["com.openai"]["interface"]
    if manifest.get("name") != OPENAI_PLUGIN_NAME:
        wrong.append(f"plugin.json name is {manifest.get('name')!r}; OpenAI only accepts {OPENAI_PLUGIN_NAME!r}")
    # "Value must be an absolute `https://` URL" (a mailto: link was refused, 2026-10-09).
    for key in ("websiteURL", "supportURL", "privacyPolicyURL", "termsOfServiceURL"):
        if key in face and not str(face[key]).startswith("https://"):
            wrong.append(f"plugin.json {key} is {face[key]!r}; OpenAI only accepts an https:// address")
    if face.get("category") not in OPENAI_CATEGORIES:
        wrong.append(f"plugin.json category is {face.get('category')!r}; OpenAI accepts one of {sorted(OPENAI_CATEGORIES)}")
    for key, most in (("displayName", 30), ("shortDescription", 30), ("longDescription", 4000)):
        if len(face.get(key) or "") > most:
            wrong.append(f"plugin.json {key} is {len(face[key])} characters; the most is {most}")
    for prompt in face.get("defaultPrompt") or []:
        if len(prompt) > 128:
            wrong.append(f"a starter prompt is {len(prompt)} characters; the most is 128")
    for key in ("composerIcon", "logo"):
        if not os.path.exists(os.path.join(SRC, face[key])):
            wrong.append(f"plugin.json {key} points at {face[key]}, which is not there")
    start = manifest["extensions"]["com.openai"].get("onboardingSkill")
    if start and not os.path.exists(os.path.join(SRC, start)):
        wrong.append(f"the first skill, {start}, is not there")
    servers = json.load(open(os.path.join(SRC, "mcp.json")))["mcpServers"]
    if len(servers) != 1:
        wrong.append("mcp.json must name exactly one server")
    skills = os.path.join(SRC, "skills")
    for name in sorted(os.listdir(skills)):
        page = os.path.join(skills, name, "SKILL.md")
        if not os.path.exists(page):
            wrong.append(f"skills/{name} has no SKILL.md")
            continue
        head = open(page).read().split("---")
        front = head[1] if len(head) > 2 else ""
        if f"name: {name}\n" not in front:
            wrong.append(f"skills/{name}/SKILL.md: its name must be {name}, the folder's")
        if "description: " not in front:
            wrong.append(f"skills/{name}/SKILL.md has no description")
        desc = front.split("description: ", 1)[-1].strip()
        if len(desc) > 1024:
            wrong.append(f"skills/{name}/SKILL.md: the description is {len(desc)} characters; the most is 1024")
    for rel in files_under(CHATGPT | CLAUDE_CODE):
        if rel.endswith((".png", ".jpg", ".jpeg", ".webp")):
            continue
        text = open(os.path.join(SRC, rel), errors="replace").read()
        for word in SECRET_WORDS:
            if word in text:
                wrong.append(f"{rel} contains {word!r}: nothing that looks like a credential goes in an archive")
    return wrong


# ── THE CHATGPT AND CODEX EDITION ───────────────────────────────────────────
# OpenAI's submission has the developer confirm that the plugin "does not
# initiate or execute ... investment trades on behalf of users" (2026-10-14).
# The server does not offer that edition the tools that would, and refuses a
# call to one. This is the package's half: its own listing, a plays skill that
# only reads, and none of the skills about placing a trade.
EDITION = os.path.join(ROOT, "plugin-chatgpt")
EDITION_NOT_SHIPPED = {"edition.json", "not-in-this-edition.json"}
TOOL_NAMED = __import__("re").compile(r"`([A-Z][A-Za-z0-9]*(?:-[A-Z][A-Za-z0-9]*)+)`")


def chatgpt_files() -> dict[str, str]:
    """{path inside the archive: file on disk} for the ChatGPT edition."""
    leave_out = set(json.load(open(os.path.join(EDITION, "edition.json")))["leave_out"])
    own_skills = set(os.listdir(os.path.join(EDITION, "skills"))) if os.path.isdir(os.path.join(EDITION, "skills")) else set()
    out: dict[str, str] = {}
    for rel in files_under(CHATGPT):
        parts = rel.split(os.sep)
        # A skill this edition does not have, or has its own version of, is
        # taken whole: never one file from each.
        if parts[0] == "skills" and len(parts) > 1 and (parts[1] in leave_out or parts[1] in own_skills):
            continue
        out[rel] = os.path.join(SRC, rel)
    for base, dirs, files in os.walk(EDITION):
        dirs[:] = sorted(d for d in dirs if d not in NEVER)
        for f in sorted(files):
            rel = os.path.relpath(os.path.join(base, f), EDITION)
            if rel in EDITION_NOT_SHIPPED or f in NEVER:
                continue
            out[rel] = os.path.join(base, f)
    return dict(sorted(out.items()))


def check_chatgpt_edition() -> list[str]:
    wrong = []
    files = chatgpt_files()
    manifest = json.load(open(files["plugin.json"]))
    face = manifest["extensions"]["com.openai"]["interface"]
    if manifest.get("name") != OPENAI_PLUGIN_NAME:
        wrong.append(f"plugin-chatgpt/plugin.json name is {manifest.get('name')!r}; OpenAI only accepts {OPENAI_PLUGIN_NAME!r}")
    for key in ("websiteURL", "supportURL", "privacyPolicyURL", "termsOfServiceURL"):
        if key in face and not str(face[key]).startswith("https://"):
            wrong.append(f"plugin-chatgpt/plugin.json {key} is {face[key]!r}; OpenAI only accepts an https:// address")
    if face.get("category") not in OPENAI_CATEGORIES:
        wrong.append(f"plugin-chatgpt/plugin.json category is {face.get('category')!r}")
    for key, most in (("displayName", 30), ("shortDescription", 30), ("longDescription", 4000)):
        if len(face.get(key) or "") > most:
            wrong.append(f"plugin-chatgpt/plugin.json {key} is {len(face[key])} characters; the most is {most}")
    for key in ("composerIcon", "logo"):
        if face[key].lstrip("./") not in files:
            wrong.append(f"plugin-chatgpt/plugin.json {key} points at {face[key]}, which is not in the archive")
    start = (manifest["extensions"]["com.openai"].get("onboardingSkill") or "").lstrip("./")
    if start and start not in files:
        wrong.append(f"the edition's first skill, {start}, is not in the archive")
    # The words a listing must not use for a plugin that places no trade.
    said = " ".join([manifest.get("description") or "", face.get("longDescription") or "",
                     " ".join(face.get("capabilities") or [])]).lower()
    for phrase in ("place and manage", "handles the execution", "post and take", "place it", "carries out in your own broker"):
        if phrase in said:
            wrong.append(f"plugin-chatgpt/plugin.json still says {phrase!r}: this edition places no trade")
    lacking_path = os.path.join(EDITION, "not-in-this-edition.json")
    if not os.path.exists(lacking_path):
        wrong.append("plugin-chatgpt/not-in-this-edition.json is missing: run mcp-server/scripts/sync_tool_docs.py")
        lacking = set()
    else:
        lacking = set(json.load(open(lacking_path))["tools"])
    for rel, path in files.items():
        if rel.endswith((".png", ".jpg", ".jpeg", ".webp")):
            continue
        text = open(path, errors="replace").read()
        for word in SECRET_WORDS:
            if word in text:
                wrong.append(f"{rel} (ChatGPT edition) contains {word!r}")
        # A page a person wrote must not tell a model to call a tool this
        # edition is not offered. (The generated field lists quote the tools'
        # own descriptions, which may mention another tool in passing.)
        if rel.endswith("SKILL.md"):
            named = sorted(set(TOOL_NAMED.findall(text)) & lacking)
            if named:
                wrong.append(f"{rel} (ChatGPT edition) names tools it is not offered: {', '.join(named)}")
            skill = rel.split(os.sep)[1]
            if f"name: {skill}\n" not in text.split("---")[1]:
                wrong.append(f"{rel} (ChatGPT edition): its name must be {skill}")
    skills = sorted({rel.split(os.sep)[1] for rel in files if rel.startswith("skills" + os.sep)})
    for name in skills:
        if os.path.join("skills", name, "SKILL.md") not in files:
            wrong.append(f"skills/{name} (ChatGPT edition) has no SKILL.md")
    return wrong


def write_zip_from(path: str, files: dict[str, str]) -> None:
    """`files` is {name inside the archive: file on disk}."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        for rel, src in files.items():
            info = zipfile.ZipInfo(rel, date_time=(2026, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            with open(src, "rb") as fh:
                z.writestr(info, fh.read())


def write_zip(path: str, files: list[str], strip: str = "") -> None:
    """`files` are paths under plugin/; `strip` is taken off the front of each name."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        for rel in files:
            # A fixed date, so the same source always makes the same archive.
            info = zipfile.ZipInfo(rel[len(strip):], date_time=(2026, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            with open(os.path.join(SRC, rel), "rb") as fh:
                z.writestr(info, fh.read())


def main() -> int:
    wrong = check() + check_chatgpt_edition()
    if wrong:
        print("Not built:")
        for w in wrong:
            print("  " + w)
        return 1
    made = []
    write_zip_from(os.path.join(DIST, "mindvest-atlas-chatgpt.zip"), chatgpt_files())
    made.append("mindvest-atlas-chatgpt.zip")
    write_zip(os.path.join(DIST, "mindvest-atlas-claude-code.zip"), files_under(CLAUDE_CODE))
    made.append("mindvest-atlas-claude-code.zip")
    for name in sorted(os.listdir(os.path.join(SRC, "skills"))):
        files = [f for f in files_under({"skills"}) if f.startswith(f"skills/{name}/")]
        # The skill's own folder at the top of its archive.
        write_zip(os.path.join(DIST, "claude-skills", f"{name}.zip"), files, strip="skills/")
        made.append(f"claude-skills/{name}.zip")
    for m in made:
        print(f"  dist/{m}  {os.path.getsize(os.path.join(DIST, m)):,} bytes")
    return 0


if __name__ == "__main__":
    sys.exit(main())
