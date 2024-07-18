# Developer Guide

There are multiple ways to contribute to `osipi` and we welcome them all. `osipi` is a tool developed by the research community for the research community, and we are all responsible for ensuring it is as good as it can be. So, if you feel some part of it is not, fix it!

The way to do this is by making a pull request on GitHub. If you are not familiar with GitHub pull requests, it is not as scary as it sounds. The simplest way is to find the file that you want to edit on GitHub in your browser, edit it manually and follow the prompts to create a fork and pull request.

## Making a Pull Request (PR) to the OSIPI Package
### Step 1: Fork the Repository
First, fork the OSIPI repository to your GitHub account and make a new branch with the your new feature or bug fix.

### Step 2: Set Up Your Development Environment
After creating a fork, you have two options:
#### Option 1: Use Poetry

1. **Install Poetry**: If you don't have Poetry installed, follow the instructions [here](https://python-poetry.org/docs/#installation).
2. **Install Dependencies**: Run the following command in your terminal:
    ```sh
    poetry install
    ```
#### Option 2: Use Requirements File

1. **Install Dependencies**: Run the following command in your terminal:
    ```sh
    pip install -r requirements.txt
    ```

### Step 3: Make Your Contribution
Make your changes or add your contribution to the codebase.

### Step 4: Run Pre-commit Checks
Before pushing your changes, run pre-commit checks to ensure your code meets the project's standards.

1. Run the following command in your terminal:
    ```sh
    pre-commit run --all-files
    ```

### Step 5: Push Your Changes and Create a PR
1. Push your changes to your forked repository.
2. Create a pull request (PR) to the main OSIPI repository.


## How to Contribute Examples

One way to contribute is by providing examples of how you used `osipi` for a specific task. These are usually real-world examples with a relevant aim, perhaps to derive some results that you have published. To package these up as an example, follow these steps:

1. Code up your example in a single Python file in a narrative style, similar to a notebook. Have a look at the current examples to see how these need to be formatted, especially their docstrings, to make sure they show up properly on the website.
2. When you save your file, make sure the filename starts with *plot_*.
3. Then drop your file in the examples folder `osipi-docs-examples` in the appropriate subfolder.

When the documentation is generated, your example will automatically appear in the examples gallery and also in the documentation of any function you are using in the example.

## How to Contribute Documentation

`osipi` is a user interface and for that reason good, clear and well-structured documentation is equally important as the quality of the functionality itself. We especially welcome suggestions for improving the documentation from end-users who are not necessarily contributing new code. You know best what works, and what doesn't.

If you are a user of `osipi`, and some part of the documentation is not as clear as it can be, then submit your suggestions for improvement and make sure that the next person will not have to face the same issues.

If you want to edit the documentation of a specific function, then you need to find the function in the osipi source code `osipi-src`. Find the function and edit the documentation string immediately below its definition. If you want to edit any other part of the documentation, find the appropriate file in the documentation source code `osipi-docs-source` and edit it there.

## How to Contribute Tests

Beyond documentation and functionality, solid testing is equally critical for ensuring long-term stability of a package. `osipi` uses a continuous integration model where all tests are run before each push to the central repository. This is important because often changes at one part of the code, even if tested well locally, can have unintended consequences at other parts. The testing prevents that these errors propagate and destabilize parts of the package.

If you find a bug in any part of the code, this obviously points to a flaw in the code, but it also reveals a gap in the testing. It is critical when this happens that both the code AND the tests are reviewed to ensure that in future a scenario of this type is picked up during testing.

The tests are defined in the folder `osipi-tests`.

## How to Contribute Functionality

OSIPI is always happy to receive new functionality for inclusion in the `osipi` package. This can be code that addresses a gap in the current functionality, or it can be code that improves the performance of a current implementation. Improvements can consist of extending the functionality (e.g. with new optional arguments), user friendliness or consistency, improvement of the accuracy or precision in the results, computation time, or platform independence, or improved documentation or code structure.

Contribution of functionality generally proceeds in two steps. In the first step you submit your code to the primary *contributions* repository as explained in its [wiki](https://github.com/OSIPI/DCE-DSC-MRI_CodeCollection/wiki/How-to-contribute-code). The task force will catalogue your code in the contributions repository and test it as explained in the [guidance](https://github.com/OSIPI/DCE-DSC-MRI_CodeCollection/wiki/The-testing-approach). Afterwards, if it is found to address a gap in `osipi` and/or improve existing functionality, you will be invited to submit a pull request to `osipi` containing your contribution formatted as required by the package.

While this is the general process, we accept there may be situations where a new submission to the contributions repository is overkill, for instance if your improvement concerns documentation only, or improvements in code structure or style. In that case a direct pull request to `osipi` may be acceptable - when in doubt please contact the OSIPI repository lead in the first instance to avoid unnecessary work.

See the section on design principles below for general requirements from `osipi` code snippets.

## How to Contribute Issues

If you have a constructive suggestion for how `osipi` can be improved, but you are not able to address it yourself for some reason, it is still extremely helpful if you write this up as an issue so it can be picked up by others at a later stage. To write up an issue, go to the `osipi` repository on GitHub, select `issues` and write a new one. Make sure to provide sufficient detail so that others can understand and address the issue.

## Design Principles

### Style Guide

`osipi` follows the [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html). This means especially also that we expect proper attention to error handling. Consider for instance what happens if a user calls your snippet using arguments of incorrect type or length. Will they get an appropriate error message that will help them identify and fix the error?

### Package Structure

The `osipi` documentation follows the structure of the OSIPI Lexicon exactly - see [here](https://osipi.github.io/OSIPI_CAPLEX/) for a detailed description of the Lexicon.

From a user perspective, the package structure is a flat list of functions that can all be accessed as `osipi.some_function`. They are listed in the __init__ file of the package, directly under the folder `src\osipi`. For clarity, the code itself is organized into modules, but these may evolve over time and should not be accessed directly. Module names all start with an underscore `_module.py` to emphasize their private and transient nature. Equally, subfolders may be added in the future as the package grows.



### Code Snippets

`osipi` is a collection of *simple* code snippets following a *simple* functional programming paradigm (did you see how we said *simple* twice there?). Each code snippet is a Python function that takes OSIPI variables as arguments and returns other OSIPI variables as results. At this stage, we are *not* planning to include an object-oriented interface or internal logic as this reduces the modularity of the code snippets, reduces compatibility with other packages, and increases the overhead of learning how to use `osipi`. Therefore, all code contributions will essentially consist of a new function or an improvement of an existing function.

Beyond the general requirements of the [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html), `osipi` requires that each new function is accompanied by an appropriate test in the tests folder, and that each function fully conforms to the Lexicon. In particular:

1. Each function must be defined in the lexicon, and the docstring must include a reference section containing the following four items:
    - Lexicon URL: webpage in the Lexicon where the function is defined.
    - Lexicon code: machine-readable code identifying the entry in the Lexicon.
    - OSIPI name: human-readable name for the function as defined in the Lexicon.
    - Adapted from contribution: module.py in the original snippet in the code contribution repository
2. Each argument to the function as well as each return value *must* be defined in the Lexicon. The docstring of the function must provide the following data on each argument and return value:
    - Python data type (include type hint in the function definition)
    - Lexicon code: machine-readable code identifying the corresponding quantity in the Lexicon.
    - OSIPI name: human-readable name for the quantity as defined in the Lexicon.
3. All arguments and return values must be provided in OSIPI units as defined in the Lexicon.
4. Arguments should be provided using OSIPI notation as defined in the Lexicon.
5. The docstring of the function must contain a self-contained code example that runs the function and illustrates the output.

!!!note
    If your function addresses entirely novel functionality or uses new variables that are not yet described in the Lexicon, then you should first contact the Lexicon maintainers and request that it is added as an entry to the Lexicon. Only afterwards can it be considered as a contribution to the `osipi` package.

!!!note
    The original [library for code contributions](https://github.com/OSIPI/DCE-DSC-MRI_CodeCollection/wiki/How-to-contribute-code) is less stringent as to code structure and documentation or testing requirements. However, it is nevertheless advisable to adhere to the same guidelines when submitting code to the original contributions repository as this will make it easier for testers to understand and run your code, and it will reduce the overhead on your part in rewriting the code
