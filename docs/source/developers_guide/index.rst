.. _developer-guide:

###############
Developer guide
###############

There are multiple ways to contribute to ``osipi`` and we welcome them all. ``osipi`` is a tool developed by the research community for the research community, and we are all responsible for ensuring it is as good as it can be. So, if you feel some part of it is not, fix it! 

*******************************
How to contribute documentation
*******************************

``osipi`` is a user interface and for that reason good, clear and well-structured documentation is equally important as the quality of the functionality itself. We especially welcome suggestions for improving the documentation from end-users who are not necessarily contributing new code. You know best what works, and what doesn't.

If you are a user of ``osipi``, and some part of the documentation is not as clear as it can be, then submit your suggestions for improvement and make sure that the next person will not have to face the same issues. The way to do this is by making a pull request on github. If you are not familiar with github pull requests, it is not as scary as it sounds. The simplest way is to find the file that you want to edit in your browser, edit it manually and follow the prompts to create a fork and pull request. 

If you want to edit the documentation of a specific function, then you need to find the function in the osipi source code `osipi-src`. Find the function and edit the documentation string immediately below its definition. If you want to edit any other part of the documentation, find the appropriate file in the documentation source code `osipi-docs-source` and edit it there.


***********************
How to contribute tests
***********************

Beyond documentation and functionality, solid testing is equally critical for ensuring long-term stability of a package. ``osipi`` uses a continuous integration model where all tests are run before each push to the central respository. This is important because often changes at one part of the code, even if tested well locally, can have unintended consequences at other parts. The testing prevents that these errors propagate and destablize parts of the package. 

If you find a bug in any part of the code, this obviously points to a flaw in the code, but it also reveals a gap in the testing. It is critical when this happens that both the code AND the tests are reviewed to ensure that in future a scenario of this type is picked up during testing. 

The tests are defined in the folder `osipi-tests`.


*******************************
How to contribute functionality
*******************************

OSIPI is always happy to recieve new functionality for inclusion in the ``osipi`` package. This can be code that addresses a gap in the current functionality, or it can be code that improves the performance of a current implementation. Improvements can consist of extending the functionality (e.g. with new optional arguments), user friendliness or consistency, improvement of the accuracy or precision in the results, computation time, or platform independence, or improved documentation or code structure. 

Contribution of functionality generally proceeds in two steps. In the first step you submit your code to the primary *contributions* repository as explained in its `wiki <https://github.com/OSIPI/DCE-DSC-MRI_CodeCollection/wiki/How-to-contribute-code>`_. The task force will catalogue your code in the contributions repository and test it as explained in the `guidance <https://github.com/OSIPI/DCE-DSC-MRI_CodeCollection/wiki/The-testing-approach>`_. Afterwards, if it is found to address a gap in ``osipi`` and/or improve existing functionality, you will be invited to submit a pull request to ``osipi`` containing your contribution formatted as required by the package. 

While this is the general process, we accept there may be situations where a new submission to the contributions repository is overkill, for instance if your improvement concerns documentation only, or improvements in code structure or style. In that case a direct pull request to ``osipi`` may be acceptable - when in doubt please contact the OSIPI repository lead in the first instance to avoid unnecessary work. 


************************
How to contribute issues
************************

If you have a constructive suggestion for how ``osipi`` can be improved, but you are not able to address it yourself for some reason, it is still extremely helpful if you write this up as an issue so it can be picked up by others at a later stage. To write up an issue, go to the ``osipi`` repository on github, select `issues` and write a new one. Make sure to provide sufficient detail so that others can understand and address the issue.
 

*****************
Design principles
*****************

Style guide
^^^^^^^^^^^

``osipi`` follows the `google python style guide <https://google.github.io/styleguide/pyguide.html>`_. This means especially also that we expect proper attention to error handling. Consider for instance what happens if a user calls your snippet using arguments of incorrect type or length, for instance. Will they get an appropriate error message that will help them identify and fix the error? 


Package structure
^^^^^^^^^^^^^^^^^

The ``osipi`` package currently only includes methods for the dynamic contrast (DC) approach to perfusion MRI (DC-MRI, a unifying term for the separate fields DCE-MRI and DSC-MRI). In particular arterial spin labelling (ASL) solutions are not currently included. However the package structure foresees future inclusion if ASL and therefore has two separate subpackages ``osipi.asl`` and ``osipi.dc``, where the former is just an empty placeholder at this stage. If the ASL part is included in future versions, it may have its own internal logic and design principles.

The ``osipi`` package follows the structure of the OSIPI Lexicon exactly - see `here <https://osipi.github.io/OSIPI_CAPLEX/>`_ for a detailed description of the Lexicon. In line with the main headings in the lexicon, the ``osipi.dc`` package is structured as follows:

::

    osipi.dc
    ├── quantities
    ├── models
    │   ├── concentration
    │   │   ├── aif
    │   │   └── tissue
    │   ├── descriptive
    │   ├── empproperties
    │   ├── identity
    │   ├── leakage
    │   └── signal
    ├── processes 
    │   ├── aif
    │   ├── baseline
    │   ├── bat
    │   ├── calibration
    │   ├── concentration
    │   ├── leakage
    │   ├── parameters
    │   └── R1           
    └── general  
        ├── averaging
        ├── deconvolution
        ├── descriptive
        ├── forward
        ├── optimization
        ├── segmentation
        └── uncertainty

.. note::

    Please note at this stage most modules are just placeholders to ensure a proper structure of the package. Content will be filled in if and when contributions are recieved.

Code snippets
^^^^^^^^^^^^^

``osipi`` is a collection of *simple* code snippets following a *simple* functional programming paradigm (did you see how we said *simple* twice there?). Each code snippet is a python function that takes OSIPI variables as argument and returns other OSIPI variables as result. At this stage we are *not* planning to include an object oriented interface or internal logic as this reduces the modularity of the code snippets, reduces compatibility with other packages and increases the overhead of learning how to use ``osipi``. Therefore all code contributions will essentially exist of a new function, or an improvement of an existing function. 

Beyond the general requirements of the `google python style guide <https://google.github.io/styleguide/pyguide.html>`_, ``osipi`` requires that each new function is accompanied by an appropriate test in the tests folder, and that each function fully conforms to the Lexicon. In particular:

1. Each function must be defined in the lexicon, and the doc string must include a reference section containing the following four items:
    - Lexicon url: webpage in the Lexicon where the function is defined.
    - Lexicon code: machine-readable code identifying the entry in the Lexicon.
    - OSIPI name: human-readable name for the function as defined in the Lexicon.
    - Adapted from contribution: module.py in the original snippet in the code contribution repository
2. Each argument to the function as as well as each return value *must* be defined in the Lexicon. The doc string of the function must provide the following data on each argument and return value:
    - python data type
    - Lexicon code: machine-readable code identifying the corresponding quantitity in the Lexicon.
    - OSIPI name: human-readable name for the quantity as defined in the Lexicon.
3. All arguments and return values must be provided in OSIPI units as defined in the Lexicon.
4. Arguments should be provided using OSIPI notation as defined in the Lexicon.
5. The docstring of the function must contain a self contained code example that runs the function and illustrates the output.
  

.. note::

    If your function addresses entirely novel functionality or uses new variables that are not yet described in the Lexicon, then you should first contact the Lexicon maintainers and request that it is added as an entry to the Lexicon. Only afterwards can it be considered as a contribution to the ``osipi`` package.

.. note::

    The original `library for code contributions <https://github.com/OSIPI/DCE-DSC-MRI_CodeCollection/wiki/How-to-contribute-code>`_ is less stringent as to code structure and documentation or testing requirements. However, it is nevertheless advisable to adhere to the same guidelines when submitting code to the original contributions repository as this will make it easier for testers to understand and run your code, and it will reduce the overhead on your part in rewriting the code if it is subsequently invited as a contribution to ``osipi``. 

