import semantic_version
import toml
import sys


def read_version(full=False):
    """Reads the project version from pyproject.toml."""
    try:
        with open("pyproject.toml", "r") as file:
            pyproject = toml.load(file)
        if full:
            return pyproject
        return semantic_version.Version.coerce(pyproject["tool"]["poetry"]["version"])
    except (FileNotFoundError, KeyError, toml.TomlDecodeError) as e:
        print(f"Error reading pyproject.toml: {e}")
        sys.exit(1)


def write_version(pyproject, version):
    """Writes the new version to pyproject.toml."""
    pyproject["tool"]["poetry"]["version"] = str(version)
    try:
        with open("pyproject.toml", "w") as file:
            toml.dump(pyproject, file)
    except Exception as e:
        print(f"Error writing pyproject.toml: {e}")
        sys.exit(1)


def bump_version(part):
    """Bumps the version (major, minor, or patch) and updates the file."""
    pyproject = read_version(full=True)
    version = semantic_version.Version.coerce(pyproject["tool"]["poetry"]["version"])

    if part == "major":
        new_version = version.next_major()
    elif part == "minor":
        new_version = version.next_minor()
    elif part == "patch":
        new_version = version.next_patch()
    else:
        print("Invalid part: choose 'major', 'minor', or 'patch'")
        sys.exit(1)

    write_version(pyproject, new_version)
    print(f"Updated version from {version} to {new_version}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python version_bump.py [read|major|minor|patch]")
        sys.exit(1)

    command = sys.argv[1].lower()
    if command == "read":
        print(read_version())
    elif command in {"major", "minor", "patch"}:
        bump_version(command)
    else:
        print("Invalid command: choose 'read', 'major', 'minor', or 'patch'")
        sys.exit(1)
