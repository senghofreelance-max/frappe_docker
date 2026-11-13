import json
from pathlib import Path

import pytest

from development.installer import (
    normalize_apps_json,
    normalize_frappe_app,
    normalize_git_url,
)


def test_normalize_frappe_app_renames_checkout_and_updates_apps_file(
    tmp_path: Path,
):
    bench_path = tmp_path / "dev-bench"
    source_path = bench_path / "apps" / "frappe-16"
    (source_path / "frappe").mkdir(parents=True)
    (source_path / "frappe" / "__init__.py").touch()
    sites_path = bench_path / "sites"
    sites_path.mkdir()
    (sites_path / "apps.txt").write_text("frappe-16\nerpnext\n")

    normalize_frappe_app(bench_path)

    assert (bench_path / "apps" / "frappe" / "frappe" / "__init__.py").is_file()
    assert not source_path.exists()
    assert (sites_path / "apps.txt").read_text() == "frappe\nerpnext\n"


def test_normalize_frappe_app_creates_apps_file_for_existing_checkout(
    tmp_path: Path,
):
    bench_path = tmp_path / "dev-bench"
    frappe_path = bench_path / "apps" / "frappe"
    (frappe_path / "frappe").mkdir(parents=True)
    (frappe_path / "frappe" / "__init__.py").touch()
    (bench_path / "apps" / "erpnext").mkdir()
    (bench_path / "sites").mkdir()

    normalize_frappe_app(bench_path)

    assert (bench_path / "sites" / "apps.txt").read_text() == "frappe\nerpnext\n"


def test_normalize_frappe_app_rejects_missing_framework_checkout(
    tmp_path: Path,
):
    bench_path = tmp_path / "dev-bench"
    (bench_path / "apps").mkdir(parents=True)

    with pytest.raises(RuntimeError, match="Expected one Frappe checkout"):
        normalize_frappe_app(bench_path)


def test_normalize_git_url_rewrites_ssh_github_url():
    assert normalize_git_url("git@github.com:senghofreelance-max/frappe-16.git") == (
        "https://github.com/senghofreelance-max/frappe-16.git"
    )
    assert normalize_git_url("https://github.com/frappe/frappe") == "https://github.com/frappe/frappe"


def test_normalize_apps_json_rewrites_ssh_urls(tmp_path: Path):
    apps_path = tmp_path / "apps.json"
    apps_path.write_text(
        json.dumps(
            [
                {"url": "git@github.com:senghofreelance-max/cambo_pos_api_retail_app.git"},
                {"url": "https://github.com/frappe/erpnext.git"},
            ]
        )
    )

    normalize_apps_json(apps_path)

    assert json.loads(apps_path.read_text()) == [
        {"url": "https://github.com/senghofreelance-max/cambo_pos_api_retail_app.git"},
        {"url": "https://github.com/frappe/erpnext.git"},
    ]
