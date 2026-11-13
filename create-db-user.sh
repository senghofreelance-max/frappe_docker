#!/bin/bash
set -euo pipefail

if [[ ! "$DB_USER" =~ ^[A-Za-z0-9_]+$ ]] || [[ ! "$DB_PASSWORD" =~ ^[A-Za-z0-9@._-]+$ ]]; then
  echo "DB_USER or DB_PASSWORD contains unsupported characters" >&2
  exit 1
fi

mariadb-admin --protocol=tcp --host="${DB_HOST:-mariadb}" --user=root \
  --password="$MARIADB_ROOT_PASSWORD" ping --silent >/dev/null

mariadb --protocol=tcp --host="${DB_HOST:-mariadb}" --user=root \
  --password="$MARIADB_ROOT_PASSWORD" <<SQL
CREATE USER IF NOT EXISTS '${DB_USER}'@'%' IDENTIFIED BY '${DB_PASSWORD}';
ALTER USER '${DB_USER}'@'%' IDENTIFIED BY '${DB_PASSWORD}';
GRANT ALL PRIVILEGES ON *.* TO '${DB_USER}'@'%' WITH GRANT OPTION;
FLUSH PRIVILEGES;
SQL
