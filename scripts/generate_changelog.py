"""
Script to auto-create a clean changelog from git history for OMNIMIND.
Modular and future-proof for CI/CD integration.
"""
import subprocess
from typing import List

def get_git_log() -> List[str]:
    """Get git log messages (stub)."""
    result = subprocess.run(["git", "log", "--pretty=format:%s"], capture_output=True, text=True)
    return result.stdout.splitlines()

def generate_changelog(filename: str = "CHANGELOG.md"):
    """Generate a changelog file from git log (stub)."""
    log_lines = get_git_log()
    with open(filename, "w") as f:
        f.write("# Changelog\n\n")
        for line in log_lines:
            f.write(f"- {line}\n")
    print(f"Changelog written to {filename}")

if __name__ == "__main__":
    generate_changelog() 