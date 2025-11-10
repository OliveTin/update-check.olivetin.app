# update-check.olivetin.app

This is the source code for the OliveTin Update Check Service that runs at update-check.olivetin.app. This is public, so that it can be audited, and checked. However, it probably is of very limited use to anyone to re-deploy this code anywhere.

[Documentation for the update check / tracking service](https://docs.olivetin.app/update-tracking.html)

## Using this file in your scripts

People may want to grab the "latest-2k" or "latest-3k" release in their scripts, like this;

```bash
user@host: curl -sS https://raw.githubusercontent.com/OliveTin/update-check.olivetin.app/refs/heads/main/versions.json | jq -r '.["latest-2k"]'
2025.11.06
```

```bash
user@host: curl -sS https://raw.githubusercontent.com/OliveTin/update-check.olivetin.app/refs/heads/main/versions.json | jq -r '.["latest-3k"]'
3000.3.2
```

The GitHub action to update this file runs daily. 
