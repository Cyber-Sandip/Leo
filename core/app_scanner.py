import subprocess
import json

apps = {}

# Get Windows start menu apps
command = 'powershell "Get-StartApps | Select-Object Name, AppID"'

result = subprocess.run(command, capture_output=True, text=True, shell=True)

lines = result.stdout.split("\n")

for line in lines[3:]:   # skip header
    parts = line.strip().split()

    if len(parts) > 1:
        name = " ".join(parts[:-1])
        appid = parts[-1]

        apps[name.lower()] = appid

# save database
with open("apps.json", "w", encoding="utf-8") as f:
    json.dump(apps, f, indent=4)

print("Apps detected:", len(apps))