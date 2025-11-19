import re

with open("issue_body.txt") as f:
    issue_body = f.read()

def find_section(title):
    m = re.search(rf"{title}\\n\\n([\\s\\S]*?)(\\n(?=###)|$)", issue_body)
    return m.group(1).strip() if m else ""

depth = find_section("### Investigation Depth")
target = find_section("### Target Repository URL")
methodologies_raw = find_section("### Methodology (The Wisdom Ladder)")
tools = []
for line in methodologies_raw.splitlines():
    m = re.match(r"- \[x\] (.+)", line.strip())
    if m:
        tools.append(m.group(1).strip())
tools_str = ", ".join(tools)

intent = find_section("### Intent / Strategic Context (Optional)")
if intent.lower() == "_no response_":
    intent = ""

clues = find_section("### Special Observations (Optional)")
if clues.lower() == "_no response_":
    clues = ""

with open("issue_vars.sh", "w") as out:
    out.write(f'AGENT_TARGET="{target}"\n')
    out.write(f'AGENT_DEPTH="{depth}"\n')
    out.write(f'AGENT_TOOLS="{tools_str}"\n')
    out.write(f'AGENT_INTENT="{intent}"\n')
    out.write(f'AGENT_CLUES="{clues}"\n')
