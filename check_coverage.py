import subprocess
import sys


def run_coverage():
    try:
        # Run tests with coverage
        subprocess.run(["poetry", "run", "coverage", "run", "-m", "pytest"], check=True)
        # Generate coverage report and check threshold
        subprocess.run(["poetry", "run", "coverage", "report", "--fail-under=95"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Coverage check failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    print("Running coverage check...")
    run_coverage()
    print("Coverage check passed.")
