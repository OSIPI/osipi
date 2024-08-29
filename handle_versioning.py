import semantic_version
import toml


def read_version():
    with open("pyproject.toml", "r") as file:
        pyproject = toml.load(file)
    return semantic_version.Version(pyproject["tool"]["poetry"]["version"])


def write_version(version):
    with open("pyproject.toml", "r") as file:
        pyproject = toml.load(file)
    pyproject["tool"]["poetry"]["version"] = str(version)
    with open("pyproject.toml", "w") as file:
        toml.dump(pyproject, file)


def bump_version(part):
    version = read_version()
    if part == "major":
        new_version = version.next_major()
    elif part == "minor":
        new_version = version.next_minor()
    elif part == "patch":
        new_version = version.next_patch()
    else:
        raise ValueError("Invalid part: choose 'major', 'minor', or 'patch'")
    write_version(new_version)
    print(f"Updated version to {new_version}")


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2 or sys.argv[1] not in ["read", "major", "minor", "patch"]:
        raise ValueError("Missing command: choose 'read', 'major', 'minor', or 'patch")

    command = sys.argv[1]
    if command == "read":
        current_version = read_version()
        print(f"Current version is {current_version}")

    else:
        bump_version(command)
