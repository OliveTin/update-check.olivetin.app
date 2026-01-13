#!/usr/bin/env python3

# Get latest version of OliveTin/OliveTin from GitHub release API
# and update the local version if necessary.

import os
import sys
import json
import requests
import semver

def get_releases():
    url = "https://api.github.com/repos/OliveTin/OliveTin/releases"
    response = requests.get(url)

    if response.status_code != 200:
        print("Failed to get release information.")
        sys.exit(1)
    return json.loads(response.text)

# replace 0 padded numbers
def unpad_version(version_number):
    return '.'.join(str(int(part)) for part in version_number.split('.'))

def find_latest_versions():
    releases = get_releases()
    
    versions = {
        "latest-2k": None,
        "latest-2k-release": None,
        "latest-3k": None,
        "latest-3k-release": None
    }

    for release in releases:
        version_number = release["tag_name"]

        if "beta" in version_number.lower():
            print(f"Skipping beta version: {version_number}")
            continue

        release_semver = semver.VersionInfo.parse(unpad_version(version_number))

        if release_semver.major < 3000:
            if (versions["latest-2k"] is None) or (release_semver > semver.VersionInfo.parse(unpad_version(versions["latest-2k"]))):
                versions["latest-2k"] = version_number
                versions["latest-2k-release"] = release
        else:
            if (versions["latest-3k"] is None) or (release_semver > semver.VersionInfo.parse(unpad_version(versions["latest-3k"]))):
                versions["latest-3k"] = version_number
                versions["latest-3k-release"] = release
                versions["latest"] = version_number

        print("Checking version: ", release_semver)

    return versions

def get_latest_version():
    url = "https://api.github.com/repos/OliveTin/OliveTin/releases/latest"
    response = requests.get(url)
    if response.status_code != 200:
        print("Failed to get latest release information.")
        sys.exit(1)
    return json.loads(response.text)["tag_name"]

def get_checksums_from_release(release):
    """
    Download and parse checksums.txt from a release.
    Returns a dictionary mapping package filename to checksum.
    """
    if not release:
        return {}
    
    # Find the checksums.txt asset
    checksums_asset = None
    for asset in release.get('assets', []):
        if asset['name'] == 'checksums.txt':
            checksums_asset = asset
            break
    
    if not checksums_asset:
        return {}
    
    # Download the checksums file
    response = requests.get(checksums_asset['browser_download_url'])
    if response.status_code != 200:
        print(f"Warning: Failed to download checksums.txt for {release.get('tag_name', 'unknown')}")
        return {}
    
    # Parse the checksums file
    # Format is always: "<sha256checksum><2 spaces><filename>"
    checksums = {}
    for line in response.text.strip().split('\n'):
        line = line.strip()
        if not line:
            continue
        
        # Split on exactly two spaces
        if '  ' in line:
            parts = line.split('  ', 1)
            if len(parts) == 2:
                checksum = parts[0].strip()
                filename = parts[1].strip()
                if checksum and filename:
                    checksums[filename] = checksum
    
    return checksums

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

latest_versions = find_latest_versions()


print("Latest 2k version: " + latest_versions['latest-2k'])
print("Latest 3k version: " + latest_versions['latest-3k'])

versions_file = load_versions_file()
old_versions_file = versions_file.copy()

if 'latest-2k' not in versions_file:
    versions_file['latest-2k'] = None

if 'latest-3k' not in versions_file:
    versions_file['latest-3k'] = None

versions_file['latest-2k'] = latest_versions['latest-2k']
versions_file['latest-2k-download-baseurl'] = f"https://github.com/OliveTin/OliveTin/releases/download/{latest_versions['latest-2k']}/"
versions_file['latest-2k-release-url'] = f"https://github.com/OliveTin/OliveTin/releases/{latest_versions['latest-2k']}/"

if latest_versions['latest-2k-release']:
    checksums_2k = get_checksums_from_release(latest_versions['latest-2k-release'])
    packages_2k = {}
    for asset in latest_versions['latest-2k-release'].get('assets', []):
        package_info = {
            'download_url': asset['browser_download_url']
        }
        if asset['name'] in checksums_2k:
            package_info['checksum'] = checksums_2k[asset['name']]
        packages_2k[asset['name']] = package_info
    versions_file['latest-2k-packages'] = packages_2k

versions_file['latest-3k'] = latest_versions['latest-3k']
versions_file['latest-3k-download-baseurl'] = f"https://github.com/OliveTin/OliveTin/releases/download/{latest_versions['latest-3k']}/"
versions_file['latest-3k-release-url'] = f"https://github.com/OliveTin/OliveTin/releases/{latest_versions['latest-3k']}/"

if latest_versions['latest-3k-release']:
    checksums_3k = get_checksums_from_release(latest_versions['latest-3k-release'])
    packages_3k = {}
    for asset in latest_versions['latest-3k-release'].get('assets', []):
        package_info = {
            'download_url': asset['browser_download_url']
        }
        if asset['name'] in checksums_3k:
            package_info['checksum'] = checksums_3k[asset['name']]
        packages_3k[asset['name']] = package_info
    versions_file['latest-3k-packages'] = packages_3k

versions_file['latest'] = latest_versions['latest-3k']

if versions_file != old_versions_file:
    print("Updating versions.json file.")
    save_versions_file(versions_file)
    commit_changes_to_git(latest_versions['latest-2k'] + ' / ' + latest_versions['latest-3k'])
else:
    print("No updates to versions.json needed.")
