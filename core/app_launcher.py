import json
import subprocess


with open("apps.json", encoding="utf-8") as f:
    apps = json.load(f)


def open_app(app_name):

    app_name = app_name.lower()

    for name, appid in apps.items():

        if app_name in name:

            subprocess.run(
                f'powershell Start-Process shell:AppsFolder\\{appid}',
                shell=True
            )

            return True

    return False
