#!/usr/bin/env python3
import argparse
import json
import os
import subprocess
import tempfile
from pathlib import Path


def cprint(*args, level: int = 1):
    """
    logs colorful messages
    level = 1 : RED
    level = 2 : GREEN
    level = 3 : YELLOW

    default level = 1
    """
    CRED = "\033[31m"
    CGRN = "\33[92m"
    CYLW = "\33[93m"
    reset = "\033[0m"
    message = " ".join(map(str, args))
    if level == 1:
        print(CRED, message, reset)  # noqa: T001, T201
    if level == 2:
        print(CGRN, message, reset)  # noqa: T001, T201
    if level == 3:
        print(CYLW, message, reset)  # noqa: T001, T201


def main():
    parser = get_args_parser()
    args = parser.parse_args()
    clone_standalone_apps(args)
    init_bench_if_not_exist(args)
    create_site_in_bench(args)


def get_args_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-j",
        "--apps-json",
        action="store",
        type=str,
        help="Path to apps.json, default: apps-example.json",
        default="apps-example.json",
    )  # noqa: E501
    parser.add_argument(
        "-b",
        "--bench-name",
        action="store",
        type=str,
        help="Bench directory name, default: frappe-bench",
        default="frappe-bench",
    )  # noqa: E501
    parser.add_argument(
        "-s",
        "--site-name",
        action="store",
        type=str,
        help="Site name, should end with .localhost, default: development.localhost",  # noqa: E501
        default="development.localhost",
    )
    parser.add_argument(
        "-r",
        "--frappe-repo",
        action="store",
        type=str,
        help="frappe repo to use, default: https://github.com/frappe/frappe",  # noqa: E501
        default="https://github.com/frappe/frappe",
    )
    parser.add_argument(
        "-t",
        "--frappe-branch",
        action="store",
        type=str,
        help="frappe repo to use, default: version-16",  # noqa: E501
        default="version-16",
    )
    parser.add_argument(
        "-p",
        "--py-version",
        action="store",
        type=str,
        help="python version, default: Not Set",  # noqa: E501
        default=None,
    )
    parser.add_argument(
        "-n",
        "--node-version",
        action="store",
        type=str,
        help="node version, default: Not Set",  # noqa: E501
        default=None,
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="verbose output",  # noqa: E501
    )
    parser.add_argument(
        "-a",
        "--admin-password",
        action="store",
        type=str,
        help="admin password for site, default: admin",  # noqa: E501
        default="admin",
    )
    parser.add_argument(
        "-d",
        "--db-type",
        action="store",
        type=str,
        help="Database type to use (e.g., mariadb or postgres)",
        default="mariadb",  # Set your default database type here
    )
    parser.add_argument(
        "--db-root-password",
        type=str,
        default=os.environ.get("DB_ROOT_PASSWORD", "123"),
        help="Database root password, default: DB_ROOT_PASSWORD or root.pwd@pos2026",
    )
    return parser


def app_is_frappe_app(app: dict) -> bool:
    """Treat apps as Frappe apps unless the manifest explicitly marks them standalone."""
    return bool(app.get("frappe_app", True))


def app_checkout_name(app: dict) -> str:
    """Return the requested checkout name or derive it from the repository URL."""
    if app.get("directory"):
        return app["directory"]
    repo_name = app["url"].rstrip("/").rsplit("/", 1)[-1]
    return repo_name.removesuffix(".git")


def clone_standalone_apps(args):
    apps_json = Path(args.apps_json)
    if not apps_json.is_absolute():
        apps_json = Path.cwd() / apps_json
    if not apps_json.exists():
        return

    with apps_json.open("r", encoding="utf-8") as file:
        apps = json.load(file)

    bench_path = Path(args.bench_name)
    if not bench_path.is_absolute():
        bench_path = Path.cwd() / bench_path
    development_path = bench_path.parent
    development_path.mkdir(parents=True, exist_ok=True)
    for app in apps:
        if app_is_frappe_app(app):
            continue

        checkout_path = development_path / app_checkout_name(app)
        if checkout_path.exists():
            if (checkout_path / ".git").exists():
                cprint(f"Repository already exists at {checkout_path}; skipping", level=3)
                continue
            raise FileExistsError(
                f"Repository destination exists but is not a Git repository: {checkout_path}"
            )

        repo_url = app["url"]
        branch = app.get("branch")
        cprint(f"Cloning standalone repository from {repo_url} ...", level=2)
        command = ["git", "clone"]
        if branch:
            command.extend(["--branch", branch])
        command.extend([repo_url, str(checkout_path)])
        subprocess.run(command, check=True)


def init_bench_if_not_exist(args):
    if os.path.exists(args.bench_name):
        cprint("Bench already exists. Only site will be created", level=3)
        normalize_frappe_app(Path(args.bench_name))
        return
    env = os.environ.copy()
    if args.py_version:
        env["PYENV_VERSION"] = args.py_version
    apps_json = Path(args.apps_json)
    if not apps_json.is_absolute():
        apps_json = Path.cwd() / apps_json
    with apps_json.open("r", encoding="utf-8") as file:
        apps = json.load(file)
    frappe_apps = [
        {
            key: value
            for key, value in app.items()
            if key not in {"frappe_app", "directory"}
        }
        for app in apps
        if app_is_frappe_app(app)
    ]

    init_command = ""
    if args.node_version:
        init_command = f"nvm use {args.node_version};"
    if args.py_version:
        init_command += f"PYENV_VERSION={args.py_version} "
    init_command += "bench init "
    init_command += "--skip-redis-config-generation "
    init_command += "--verbose " if args.verbose else " "
    init_command += f"--frappe-path={args.frappe_repo} "
    init_command += f"--frappe-branch={args.frappe_branch} "
    with tempfile.TemporaryDirectory(prefix="frappe-apps-") as temp_dir:
        frappe_apps_path = Path(temp_dir) / "apps.json"
        frappe_apps_path.write_text(json.dumps(frappe_apps, indent=2) + "\n")
        init_command += f"--apps_path={frappe_apps_path} "
        init_command += args.bench_name
        command = ["/bin/bash", "-i", "-c", init_command]
        subprocess.run(command, env=env, cwd=os.getcwd(), check=True)
    normalize_frappe_app(Path(args.bench_name))
    cprint("Configuring Bench ...", level=2)
    cprint("Set db_host", level=3)
    if args.db_type:
        cprint(f"Setting db_type to {args.db_type}", level=3)
        subprocess.run(
            ["bench", "set-config", "-g", "db_type", args.db_type],
            cwd=os.path.join(os.getcwd(), args.bench_name),
            check=True,
        )

    cprint("Set redis_cache to redis://redis-cache:6379", level=3)
    subprocess.run(
        [
            "bench",
            "set-config",
            "-g",
            "redis_cache",
            "redis://redis-cache:6379",
        ],
        cwd=os.getcwd() + "/" + args.bench_name,
        check=True,
    )
    cprint("Set redis_queue to redis://redis-queue:6379", level=3)
    subprocess.run(
        [
            "bench",
            "set-config",
            "-g",
            "redis_queue",
            "redis://redis-queue:6379",
        ],
        cwd=os.getcwd() + "/" + args.bench_name,
        check=True,
    )
    cprint(
        "Set redis_socketio to redis://redis-queue:6379 for backward compatibility",  # noqa: E501
        level=3,
    )
    subprocess.run(
        [
            "bench",
            "set-config",
            "-g",
            "redis_socketio",
            "redis://redis-queue:6379",
        ],
        cwd=os.getcwd() + "/" + args.bench_name,
        check=True,
    )
    cprint("Set chromium_path to the system Chromium", level=3)
    subprocess.run(
        [
            "bench",
            "set-config",
            "-g",
            "chromium_path",
            "/usr/lib/chromium/chromium-headless-shell",
        ],
        cwd=os.getcwd() + "/" + args.bench_name,
        check=True,
    )
    cprint("Set developer_mode", level=3)
    subprocess.run(
        ["bench", "set-config", "-gp", "developer_mode", "1"],
        cwd=os.getcwd() + "/" + args.bench_name,
        check=True,
    )


def normalize_frappe_app(bench_path: Path):
    apps_path = bench_path / "apps"
    frappe_path = apps_path / "frappe"
    source_name = None
    if not frappe_path.is_dir():
        candidates = [
            app_path
            for app_path in apps_path.iterdir()
            if (app_path / "frappe" / "__init__.py").is_file()
        ]
        if len(candidates) != 1:
            raise RuntimeError(
                f"Expected one Frappe checkout in {apps_path}, found {len(candidates)}"
            )
        source_name = candidates[0].name
        candidates[0].rename(frappe_path)

    apps_file = bench_path / "sites" / "apps.txt"
    installed_apps = (
        apps_file.read_text().splitlines()
        if apps_file.exists()
        else [app_path.name for app_path in apps_path.iterdir() if app_path.is_dir()]
    )
    if source_name:
        installed_apps = [
            "frappe" if app == source_name else app for app in installed_apps
        ]
    if "frappe" not in installed_apps:
        installed_apps.insert(0, "frappe")
    apps_file.parent.mkdir(parents=True, exist_ok=True)
    apps_file.write_text("\n".join(installed_apps) + "\n")


def create_site_in_bench(args):
    site_path = os.path.join(os.getcwd(), args.bench_name, "sites", args.site_name)
    if os.path.isdir(site_path):
        cprint(f"Site {args.site_name} already exists; skipping creation", level=3)
        return

    if "mariadb" == args.db_type:
        cprint("Set db_host", level=3)
        subprocess.run(
            ["bench", "set-config", "-g", "db_host", "mariadb"],
            cwd=os.getcwd() + "/" + args.bench_name,
            check=True,
        )
        new_site_cmd = [
            "bench",
            "new-site",
            f"--db-root-username=root",
            f"--db-host=mariadb",  # Should match the compose service name
            f"--db-type={args.db_type}",  # Add the selected database type
            f"--mariadb-user-host-login-scope=%",
            f"--db-root-password={args.db_root_password}",
            f"--admin-password={args.admin_password}",
        ]
    else:
        cprint("Set db_host", level=3)
        subprocess.run(
            ["bench", "set-config", "-g", "db_host", "postgresql"],
            cwd=os.getcwd() + "/" + args.bench_name,
            check=True,
        )
        new_site_cmd = [
            "bench",
            "new-site",
            f"--db-root-username=root",
            f"--db-host=postgresql",  # Should match the compose service name
            f"--db-type={args.db_type}",  # Add the selected database type
            f"--db-root-password={args.db_root_password}",
            f"--admin-password={args.admin_password}",
        ]
    apps = os.listdir(f"{os.getcwd()}/{args.bench_name}/apps")
    apps.remove("frappe")
    for app in apps:
        new_site_cmd.append(f"--install-app={app}")
    new_site_cmd.append(args.site_name)
    cprint(f"Creating Site {args.site_name} ...", level=2)
    subprocess.run(
        new_site_cmd,
        cwd=os.getcwd() + "/" + args.bench_name,
        check=True,
    )


if __name__ == "__main__":
    main()
