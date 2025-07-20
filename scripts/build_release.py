"""
Script to test, tag, build, and version OMNIMIND for release.
Modular and future-proof for CI/CD integration.
"""
import subprocess
import sys
from typing import Optional

def run_tests() -> bool:
    """Run the test suite (stub)."""
    try:
        subprocess.run([sys.executable, "-m", "pytest"], check=True)
        return True
    except Exception:
        return False

def tag_release(version: str):
    """Tag the current commit with the given version (stub)."""
    subprocess.run(["git", "tag", version])
    subprocess.run(["git", "push", "origin", version])

def build_package():
    """Build the project package (stub)."""
    subprocess.run([sys.executable, "setup.py", "sdist", "bdist_wheel"])

def main(version: Optional[str] = None):
    """Main entry for release build script."""
    if not run_tests():
        print("Tests failed. Aborting release.")
        sys.exit(1)
    if version:
        tag_release(version)
    build_package()
    print("Release build complete.")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Build and release OMNIMIND.")
    parser.add_argument("--version", type=str, help="Release version tag", required=False)
    args = parser.parse_args()
    main(args.version) 