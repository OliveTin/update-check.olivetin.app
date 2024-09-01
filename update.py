#!/usr/bin/env python3

# Get latest version of OliveTin/OliveTin from GitHub release API
# and update the local version if necessary.

import os
import sys
import json
import requests
import subprocess

def get_latest_version():
    url = "https://api.github.com/repos/OliveTin/OliveTin/releases/latest"
    response = requests.get(url)
    if response.status_code != 200:
        print("Failed to get latest release information.")
        sys.exit(1)
    return json.loads(response.text)["tag_name"]

def load_versions_file():
    with open("versions.json", "r") as f:
        return json.load(f)

def save_versions_file(versions):
    with open("versions.json", "w") as f:
        json.dump(versions, f, indent=4)


def commit_changes_to_git(latest_version):
    os.system("git add versions.json")
    os.system("git commit -m 'Update versions.json for " + latest_version + "'")
    os.system("git push")

latest_version = get_latest_version()

f = load_versions_file()

current_version = f['latest']

if current_version == latest_version:
    print("Already up-to-date: " + latest_version)
else:
    f['latest'] = latest_version

    save_versions_file(f)
    commit_changes_to_git(latest_version)
