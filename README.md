# update-check.olivetin.app

This is the source code for the OliveTin Update Check Service (which is now simply a file called [versions.json](https://raw.githubusercontent.com/OliveTin/update-check.olivetin.app/refs/heads/main/versions.json). This is also hosted at update-check.olivetin.app.

Older versions of this repository contained code to run a web service, but this has been deprecated in favor of a simple static file.

* [Update Checks](https://docs.olivetin.app/reference/updateChecks.html)
* [Update Tracking (legacy)](https://docs.olivetin.app/reference/updateTracking.html)

## Using this file in your scripts

People may want to grab the "latest-2k" or "latest-3k" release in their scripts, like this;

### latest-2k
```bash
#!/bin/bash

VERSION="latest-2k"

echo "Fetching download base URL for version: $VERSION "

SELECTOR=".[\"$VERSION-download-baseurl\"]"
DOWNLOAD_BASE_URL=$(curl -sS https://raw.githubusercontent.com/OliveTin/update-check.olivetin.app/refs/heads/main/versions.json | jq -r $SELECTOR )

echo "Using download base URL: $DOWNLOAD_BASE_URL"

# Change APK filename as needed
wget $DOWNLOAD_BASE_URL/OliveTin_linux_amd64.apk

```


## Command Line
```bash
user@host: curl -sS https://raw.githubusercontent.com/OliveTin/update-check.olivetin.app/refs/heads/main/versions.json | jq -r '.["latest-2k"]'
2025.11.06
```

### latest-3k
```bash
user@host: curl -sS https://raw.githubusercontent.com/OliveTin/update-check.olivetin.app/refs/heads/main/versions.json | jq -r '.["latest-3k"]'
3000.3.2
```

The GitHub action to update this file runs daily. 
