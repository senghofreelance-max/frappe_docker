# Development and production configuration

Use local `.env` files for credentials. Do not commit passwords or API tokens.
The values below are placeholders for each machine and deployment.

## Development machine

| Setting | Placeholder / value | Notes |
| --- | --- | --- |
| Dashboard URL | `http://<LAN-IP>:3000` | Next.js dev server, published on the host |
| Frappe URL | `http://<LAN-IP>:8000` | Browser-facing `NEXT_PUBLIC_FRAPPE_URL` for LAN clients; use localhost on the host itself |
| Frappe realtime | `<LAN-IP>:9000` | Socket.IO/WebSocket development port |
| Frappe asset watcher | `<LAN-IP>:6787` | Development only |
| MariaDB host / port | `mariadb:3306` in Compose; `<LAN-IP>:3312` from LAN | Published for LAN database clients in the development Compose file |
| Frappe site | `development.localhost` | Local site name; update if the installer site name changes |
| DB root user | `root` | Password key: `DB_ROOT_PASSWORD` |
| Host data directory (Linux) | `/home/<user>/Desktop/docker/volume` | Set as `VOLUME_ROOT` |
| Host data directory (Windows) | `C:/Users/<user>/Desktop/docker/volume` | Use forward slashes in Compose `.env` |
| Bench directory | `development/dev-bench` | Inside the repository workspace mount |

Copy `devcontainer-example/.env.example` to `.devcontainer/.env` on the first
PC and set `VOLUME_ROOT` and `DB_ROOT_PASSWORD`. Create `VOLUME_ROOT/mariadb`
before starting Compose. The same path setting on a Windows PC should point to
that PC's Desktop folder; do not copy the Linux path. The development stack uses
MariaDB's root account to create the local Frappe site, so `DB_ROOT_PASSWORD`
must match the password in the existing MariaDB volume. MariaDB is only exposed
on the host's LAN interface at port 3312 (container port 3306). The Frappe bench,
dashboard, realtime socket, and asset watcher are also published on all host
interfaces. LAN clients must use the host's LAN IP in their URLs, and the host
firewall must allow the ports they need. Set `NEXT_PUBLIC_FRAPPE_URL=http://<LAN-IP>:8000` in
`.devcontainer/.env` so browsers on other LAN devices call the correct host.
Inside Compose, containers use service DNS (`pos-admin:3000`, `mariadb:3306`);
`host.docker.internal` resolves to the Docker host for containers that need to
reach a host service.

The provided development values are for a local developer environment. Do not
reuse them in production.

## Production deployment placeholders

| Setting | Placeholder | Where it is used |
| --- | --- | --- |
| Public dashboard domain | `admin.example.com` | DNS and HTTPS reverse proxy |
| Public Frappe domain | `erp.example.com` | Frappe site and proxy routing |
| Dashboard URL | `https://admin.example.com` | Browser entry point |
| Frappe API URL | `https://erp.example.com` | Server-side integration preferred |
| Dashboard container port | `3000` | Internal container port; publish through HTTPS proxy |
| Frappe web / realtime | `8080` / `9000` | Proxy target / internal WebSocket service |
| Database host / port | `<private-db-host>` / `3306` | Private network only |
| Database name | `<frappe-site-db>` | Provisioned for the Frappe site |
| Database root password | `<secret-manager-reference>` | Supply through deployment secrets |
| Frappe service user | `<frappe-api-user>` | Use a least-privilege integration account |
| Frappe API token | `<secret-manager-reference>` | Server-only; never use a `NEXT_PUBLIC_` variable |
| Image | `cambo-pos:16` | Build from root `apps.json` manifest |
| Site name | `erp.example.com` | Must match the Frappe site's configured domain |

Set the production dashboard's environment in the deployment platform or a
secret manager. Only values that are safe for browsers belong in variables
prefixed with `NEXT_PUBLIC_`; credentials and Frappe API tokens must stay on
the server. Enable HTTPS at the reverse proxy and route WebSocket traffic for
Frappe realtime. Keep MariaDB and Redis off public interfaces.
