# Local Frappe development

The devcontainer builds `frappe/bench` from `images/bench`, then its first
`postCreateCommand` runs `installer.py` to create `dev-bench`. Bench initializes
from `https://github.com/senghofreelance-max/frappe-16.git` on `develop` and reads
`apps-example.json`; that manifest fetches ERPNext and
`cambo_pos_api_retail_app`. The installer then creates the configured site and
installs the apps it fetched. It normalizes the Frappe checkout directory to
`apps/frappe`, which Bench requires even when the Git repository has a different
name. SSH Git URLs are normalized to HTTPS automatically so local setups do not
need a GitHub SSH key for the default examples.

## Persistent data on Linux and Windows

Docker Compose cannot reliably infer the host OS path for a bind mount. Set an
absolute path on each PC in `.devcontainer/.env` (copy
`devcontainer-example/.env.example` to that location as a template):

- Linux: `VOLUME_ROOT=/home/<user>/Desktop/docker/volume`
- Windows: `VOLUME_ROOT=C:/Users/<user>/Desktop/docker/volume`

Set `DB_ROOT_PASSWORD` to the same password for MariaDB and first site setup.
Create the bind mount directory before starting the devcontainer:

- Linux: `mkdir -p "$HOME/Desktop/docker/volume/mariadb"`
- Windows PowerShell: `New-Item -ItemType Directory -Force "$env:USERPROFILE\Desktop\docker\volume\mariadb"`

The bench itself lives under the mounted repository at `development/dev-bench`;
MariaDB's persistent data lives under `VOLUME_ROOT/mariadb`. Redis is ephemeral
and has no data volume in this development setup.

The custom app is cloned during `bench init` from the manifest. The default
examples use HTTPS URLs, which avoids the need for a GitHub SSH key in local
and devcontainer setups. Rebuild/reopen the devcontainer after changing its
image or compose configuration. Existing `dev-bench` folders are reused, so
rerunning the installer does not re-fetch app sources.

## Build an application image

The repository root `apps.json` is the manifest for an image that contains the
custom app. Build the runtime image with BuildKit/Buildx from the repository
root:

```sh
docker buildx build --load \
  --build-arg FRAPPE_PATH=https://github.com/senghofreelance-max/frappe-16.git \
  --build-arg FRAPPE_BRANCH=develop \
  --secret=id=apps_json,src=apps.json \
  --tag=cambo-pos:16 \
  --file=images/custom/Containerfile .
```

The root `apps.json` must list the apps to include; `development/apps-example.json`
is used only for the development bench. After the build, set these values in
the root `.env` before starting the production Compose stack:

```dotenv
CUSTOM_IMAGE=cambo-pos
CUSTOM_TAG=16
PULL_POLICY=missing
```

The custom image build fetches app sources and builds assets into the image. It
does not create a site; the development installer creates a site in `dev-bench`.
