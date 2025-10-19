import requests
import re
from datetime import datetime
from collections import defaultdict
from typing import List, Dict, Optional


class MavenRepositoryClient:
    """Client to read versions and publication dates from Maven Central (repo1.maven.org)."""

    BASE_URL = "https://repo1.maven.org/maven2"

    # ----------------------------
    # Public methods
    # ----------------------------

    def get_versions(self, group_id: str, artifact_id: str) -> List[Dict[str, datetime]]:
        """Fetch and parse all available versions for a given artifact."""
        html = self._fetch_html(group_id, artifact_id)
        versions = self._parse_versions(html)
        return versions

    def get_latest(self, group_id: str, artifact_id: str) -> Optional[Dict[str, datetime]]:
        """Return the most recent version and its publication date."""
        versions = self.get_versions(group_id, artifact_id)
        return versions[0] if versions else None

    def get_latest_per_branch(self, group_id: str, artifact_id: str) -> Dict[str, Dict[str, datetime]]:
        """Return the latest version per major.minor branch."""
        versions = self.get_versions(group_id, artifact_id)
        branches = defaultdict(list)
        for r in versions:
            major_minor = ".".join(r["version"].split(".")[:2])
            branches[major_minor].append(r)

        return {
            branch: max(vers, key=lambda x: x["date"])
            for branch, vers in branches.items()
        }

    # ----------------------------
    # Internal helpers
    # ----------------------------

    def _fetch_html(self, group_id: str, artifact_id: str) -> str:
        """Download the raw HTML directory listing."""
        url = f"{self.BASE_URL}/{group_id.replace('.', '/')}/{artifact_id}/"
        response = requests.get(url)
        response.raise_for_status()
        return response.text

    def _parse_versions(self, html: str) -> List[Dict[str, datetime]]:
        """Extract versions and their publication dates from the <pre> block."""
        pre_block = re.search(r"<pre[^>]*>(.*?)</pre>", html, re.DOTALL)
        if not pre_block:
            return []

        content = pre_block.group(1)
        pattern = re.compile(
            r'<a href="([\w.\-]+)/".*?>\1/</a>\s+(\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2})'
        )

        results = []
        for version, date_str in pattern.findall(content):
            try:
                date = datetime.strptime(date_str, "%Y-%m-%d %H:%M")
                results.append({"version": version, "date": date})
            except ValueError:
                continue

        return sorted(results, key=lambda x: x["date"], reverse=True)

    # ----------------------------
    # Display helpers
    # ----------------------------

    @staticmethod
    def print_summary(versions: List[Dict[str, datetime]], limit: int = 10):
        """Print a summary of the latest versions."""
        if not versions:
            print("❌ No versions found.")
            return

        latest = versions[0]
        print(f"✅ Found {len(versions)} versions.")
        print(f"⭐ Latest version: {latest['version']} ({latest['date'].date()})\n")

        for v in versions[:limit]:
            print(f"- {v['version']} ({v['date'].date()})")

    @staticmethod
    def print_branches(branches: Dict[str, Dict[str, datetime]]):
        """Print the latest version per branch."""
        print("\n📦 Latest versions per branch:")
        for branch, info in sorted(branches.items(), reverse=True):
            print(f"{branch}.x → {info['version']} ({info['date'].date()})")


# ----------------------------
# Example usage
# ----------------------------
if __name__ == "__main__":
    client = MavenRepositoryClient()

    group = "org.springframework.boot"
    artifact = "spring-boot-starter"

    versions = client.get_versions(group, artifact)
    client.print_summary(versions)

    branches = client.get_latest_per_branch(group, artifact)
    client.print_branches(branches)
