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

There are two ways to set up your development environment for this project. You can choose the one that suits you best.

### Option 1: Using venv and requirements.txt

1. Clone the repository to your local machine.
2. Navigate to the project directory.
3. Create a virtual environment using `venv` by running the following command:

    ```bash
    python -m venv venv
    ```

4. Activate the virtual environment:

    - On Windows, run:

        ```bash
        .\venv\Scripts\activate
        ```

    - On Unix or MacOS, run:

        ```bash
        source venv/bin/activate
        ```

5. Install the required packages from `requirements.txt`:

    ```bash
    pip install -r requirements.txt
    ```

### Option 2: Using Poetry

1. If you don't have Poetry installed, you can install it by following the instructions on the [official Poetry website](https://python-poetry.org/docs/#installation).
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


1. In the project directory, run the following command to install the `pre-commit` hooks:

    ```bash
    pre-commit install
    ```

2. You can run all pre-commit hooks on all files with:

    ```bash
    pre-commit run --all-files
    ```

After this, `pre-commit` will automatically run the hooks each time you commit changes to the project. If any of the hooks fail,
you'll need to fix the issues and then try committing your changes again.

Also some of hooks are auto fixed if you see file was modified after running `pre-commit run --all-files` then you can add the changes and commit again.

For more details on how to contribute, visit the [Developer Guide](https://osipi.github.io/pypi/contribution/#making-a-pull-request-pr-to-the-osipi-package).
#### As mentioned before, this project is still in the early stages of development. If you'd like to contribute by adding functionality, we recommend opening an issue first to discuss your proposed functionality and the best ways to implement it.

## Details
For more detail please see the [documentation](https://osipi.github.io/pypi/).
