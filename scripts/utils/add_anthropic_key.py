import os

key = input("Paste your Anthropic API key: ").strip()

env_path = ".env"
with open(env_path, "r") as f:
    content = f.read()

if "ANTHROPIC_API_KEY" in content:
    lines = content.splitlines()
    lines = [l for l in lines if not l.startswith("ANTHROPIC_API_KEY")]
    content = "\n".join(lines)

content = content.rstrip() + f"\nANTHROPIC_API_KEY={key}\n"

with open(env_path, "w") as f:
    f.write(content)

print("Done. ANTHROPIC_API_KEY added to .env")