"""Replace the README CI badge placeholder using the configured git remote."""

from __future__ import annotations

import re
import subprocess
from pathlib import Path

README_PATH = Path("README.md")
WORKFLOW = "ci.yml"


def get_repository_slug() -> str:
    """Return owner/repository from the origin remote."""
    result = subprocess.run(
        ["git", "remote", "get-url", "origin"],
        check=True,
        capture_output=True,
        text=True,
    )
    remote = result.stdout.strip()
    patterns = (
        r"github\.com[:/](?P<slug>[^/]+/[^/]+?)(?:\.git)?$",
        r"https://github\.com/(?P<slug>[^/]+/[^/]+?)(?:\.git)?$",
    )
    for pattern in patterns:
        match = re.search(pattern, remote)
        if match:
            return match.group("slug")
    raise ValueError(f"Unsupported GitHub remote: {remote}")


def main() -> None:
    slug = get_repository_slug()
    badge = (
        "<!-- CI_BADGE_START -->\n"
        f"[![CI](https://github.com/{slug}/actions/workflows/{WORKFLOW}/badge.svg)]"
        f"(https://github.com/{slug}/actions/workflows/{WORKFLOW})\n"
        "<!-- CI_BADGE_END -->"
    )
    content = README_PATH.read_text(encoding="utf-8")
    updated = re.sub(
        r"<!-- CI_BADGE_START -->.*?<!-- CI_BADGE_END -->",
        badge,
        content,
        flags=re.DOTALL,
    )
    README_PATH.write_text(updated, encoding="utf-8")
    print(f"Updated CI badge for {slug}")


if __name__ == "__main__":
    main()
