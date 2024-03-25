import os
import sys
import venv
import logging

#logging root configuration
logging.basicConfig(level=logging.INFO, # This will log all levels of messages
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def distribute():
    """Create new version on PyPI
    
    IMPORTANT! First increment your version number in pyproject.toml:
    - Increment the MAJOR version when you make incompatible API changes.
    - Increment the MINOR version when you add functionality in a backwards compatible manner.
    - Increment the PATCH version when you make backwards compatible bug fixes.

    You need: PyPI username and password.
    You need to type in the PyPI password rather than copy-pasting.
    """
    create_venv()
    install()

    os.system(activate() + ' && ' + 'pip install --upgrade build')
    os.system(activate() + ' && ' + 'python -m build')
    os.system(activate() + ' && ' + 'pip install --upgrade twine')
    os.system(activate() + ' && ' + 'twine upload dist/*')

def create_venv():
    venv_dir = os.path.join(os.getcwd(), ".venv")
    if not os.path.exists(venv_dir):
        logging.info("Creating virtual environment...")
        os.system('py -3 -m venv .venv')
    else:
        logging.info("Virtual environment already exists.")

def activate():
    """Active virtual environment"""

    venv_dir = os.path.join(os.getcwd(), ".venv")
    os.makedirs(venv_dir, exist_ok=True)
    venv.create(venv_dir, with_pip=True)
    windows = (sys.platform == "win32") or (sys.platform == "win64") or (os.name == 'nt')
    if windows:
        return os.path.join(venv_dir, "Scripts", "activate")
    else: # MacOS and Linux
        return '. "' + os.path.join(venv_dir, "bin", "activate")

def install():
    """Install requirements to a virtual environment"""

    logging.info("Installing requirements...")
    os.system(activate() + ' && ' + 'py -m pip install -r requirements.txt')



if __name__ == '__main__':

    #install()
    distribute()