import subprocess
import sys

from pilot.helpers.Debugger import Debugger
from pilot.logger.logger import logger
from pilot.helpers.Agent import Agent
import importlib.metadata


class CodeAider(Agent):
    def __init__(self):
        super().__init__('code_aider', "project test")
        self.run_command = None
        self.save_dev_steps = True
        self.debugger = Debugger(self)
        self.shell = None

        # Initialize new conda environment
        create_conda_environment(["conda", "create", "--name", "aiderenv", "python=3.11", "-y"])

        # initialize aider-chat by pip install
        if not is_package_installed('aider-chat'):
            install_package('aider-chat')


def install_package(package):
    run_subprocess_with_conda_context(args=["pip", "install", package],
                                      description=f"installing {package}")
    logger.info(f"subprocess for installation of {package} was successful.")


def is_package_installed(package_name):
    try:
        importlib.metadata.version(package_name)
        return True
    except importlib.metadata.PackageNotFoundError:
        return False


def create_conda_environment(args):
    run_subprocess(args, "Creating Conda environment 'aiderenv' ")


def run_subprocess(args, description):
    try:
        logger.info(f"Running: {description}")
        process = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        output, error = process.communicate()
        if process.returncode != 0:
            logger.error(f"Error: The process exited with code {process.returncode} for {description}")
            logger.error(f"Error occurred : {error} during {description}")
        else:
            logger.info(f"Output: {error.strip()} successfully for {description}")
        return output
    except Exception as e:
        logger.error(f"Error: The exception occurred {e} for {description}")


def run_subprocess_with_conda_context(args, description):
    try:
        logger.info(f"Running: {description}")
        conda_args = "conda run -n ${CONDA_ENV_NAME}".split();
        process = subprocess.Popen(conda_args + args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        output, error = process.communicate()
        if process.returncode != 0:
            logger.error(f"Error: The process exited with code {process.returncode} for {description}")
            logger.error(f"Error occurred : {error} during {description}")
        else:
            logger.info(f"Output: {error.strip()} successfully for {description}")
        return output
    except Exception as e:
        logger.error(f"Error: The exception occurred {e} for {description}")


if __name__ == "__main__":
    coder = CodeAider()
