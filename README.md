##### Disclaimer:
This package is under development. All the details mentioned below are long-term intentions behind the production of this package.

## OSIPI: Open Science Initiative for Perfusion Imaging
OSIPI is a Python package developed by the Open Source Initiative for Perfusion Imaging [OSIPI](https://osipi.ismrm.org/), a project under the Perfusion Study Group of the International Society for Magnetic Resonance in Medicine [ISMRM](https://www.ismrm.org/). It serves as the authoritative tool for perfusion MRI analysis.

OSIPI's aim is to create open access resources for perfusion imaging research to eliminate duplicate development, to improve the reproducibility and to speed up the translation of perfusion imaging for clinical practice.

The `osipi` package structure and logic follows the [lexicon](https://osipi.github.io/OSIPI_CAPLEX/) defined by OSIPI, and wraps around selected implementations collected in the [code contributions](https://github.com/OSIPI/DCE-DSC-MRI_CodeCollection) of OSIPI.

## Features
- Comprehensive set of tools for analyzing perfusion MRI data
- Follows the lexicon defined by OSIPI
- Incorporates selected implementations contributed by the community


## Quick Start
### Installation
To install OSIPI, you can use pip:

      `pip install osipi`
### Usage
To use OSIPI in your Python scripts, import the package:

      `import osipi`

## Contributions
We welcome contributions to OSIPI! To contribute, follow these steps:

- Fork the OSIPI repository on GitHub.
- Create a new branch for your feature or bug fix.
- Make your changes and commit them with descriptive messages.
- Push your changes to your fork.
- Submit a pull request to the main OSIPI repository.

## Development Setup

We use poetry to manage the dependencies for this project.

### Using Poetry

1. If you don't have Poetry installed, you can install it using pip:

    ```bash
    pip install poetry
    ```

    Or, if you're using a Unix-based system, you can install it using the following command:

    ```bash
    curl -sSL https://install.python-poetry.org | python3 -
    ```

    For more information on installing Poetry, see the [official documentation](https://python-poetry.org/docs/)
2. Clone the repository to your local machine.
3. Navigate to the project directory.
4. Install the project dependencies with Poetry:

    ```bash
    poetry install
    ```

5. Activate the Poetry environment:

    ```bash
    poetry shell
    ```

## Setting up pre-commit

`pre-commit` is a tool that we use to maintain high-quality code in this project. It runs checks (hooks) on your code each time you commit changes. Here's how to set it up:

## Pre-Commit Hooks
Pre-commit hooks are scripts that run automatically before a commit is made in a Git repository. They help catch common issues like syntax errors, formatting problems, and other code quality issues.

### Example hooks
- `black` - a code formatter that automatically formats your code to a consistent style.
- `flake8` - a linter that checks your code for common errors and style issues.
- `trailing-whitespace` - a hook that removes trailing whitespace from your files.
- `ruff` - also a linter that checks your code for common errors and style issues.

We are using pre-commit configuration file to define our hooks. You can find the configuration file [here](https://github.com/OSIPI/osipi/blob/main/.pre-commit-config.yaml)

1. In the project directory, run the following command to install the `pre-commit` hooks:

    ```bash
    pre-commit install
    ```

2. You can run all pre-commit hooks on all files with:

    ```bash
    pre-commit run --all-files
    ```
**NOTE:**
- Next time you commit changes, `pre-commit` will run the hooks automatically.
- Some hooks automatically fix/format your files to specific standards. If you see that some of your files have been changed after a commit, don't worry! It's just `pre-commit` doing its job.
  Add the changes and commit them again.

For more details on how to contribute, visit the [Developer Guide](https://osipi.github.io/pypi/contribution/#making-a-pull-request-pr-to-the-osipi-package).
#### As mentioned before, this project is still in the early stages of development. If you'd like to contribute by adding functionality, we recommend opening an issue first to discuss your proposed functionality and the best ways to implement it.

## Details
For more detail please see the [documentation](https://osipi.github.io/pypi/).
