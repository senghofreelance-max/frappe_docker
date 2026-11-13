# POS Admin Dashboard

Next.js App Router dashboard with TypeScript, Tailwind CSS 4, and PrimeReact 10.
The current dashboard uses sample data; Frappe API authentication and live data
are not connected yet.

## Run in the frappe_docker devcontainer

The project is a sibling of `development/`, inside the repository root already
mounted at `/workspace`. The shared devcontainer Compose file starts the
`pos-admin` Node service and publishes port 3000 on the host. Reopen the
devcontainer, then open <http://localhost:3000> on the host or
`http://<LAN-IP>:3000` from another LAN device. Set `NEXT_PUBLIC_FRAPPE_URL` to
`http://<LAN-IP>:8000` in `.devcontainer/.env` for dashboard users on other
devices. Within Compose, containers reach the dashboard at `http://pos-admin:3000`.

To run outside the devcontainer:

```sh
npm ci
npm run dev
```

## Build and run a standalone Docker image

```sh
docker build --build-arg NEXT_PUBLIC_FRAPPE_URL=http://localhost:8000 \
  -t cambo-pos-admin:local .
docker run --rm -p 3000:3000 cambo-pos-admin:local
```

Set the public Frappe URL at image build time with
`--build-arg NEXT_PUBLIC_FRAPPE_URL=https://<frappe-domain>` when building for a
specific environment. The multi-stage Dockerfile runs the production server as
an unprivileged user.
