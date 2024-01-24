import subprocess
import sys

from pilot.helpers.Debugger import Debugger
from pilot.logger.logger import logger
import importlib.metadata


class CodeAider:
    def __init__(self):
        # super().__init__('code_aider', project)
        self.run_command = None
        self.save_dev_steps = True
        self.debugger = Debugger(self)
        self.shell = run_subprocess_with_conda_context(["aider"], "Running Aider shell")

        # Initialize new conda environment
        if not conda_env_exist('aiderenv'):
            create_conda_environment(["conda", "create", "--name", "aiderenv", "python=3.11", "-y"])

        # initialize aider-chat by pip install
        if not is_package_installed('aider-chat'):
            install_package('aider-chat')


def install_package(package):
    run_subprocess_with_conda_context(args=["pip", "install", package],
                                      description=f"installing {package}")


def conda_env_exist(env_name):
    try:
        # Getting the list of existing Conda environments
        result = run_subprocess(["conda", "env", "list"], "Chcking if conda environment exists")

        # Check if the environment name is in the output
        envs = result.stdout.splitlines()
        for env in envs:
            if env.split()[0] == env_name:
                return True
        return False
    except subprocess.SubprocessError as e:
        print(f"An error occurred: {e}")
        return False


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
        process = subprocess.Popen(args, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        output, error = process.communicate()
        if process.returncode != 0:
            logger.error(f"Error: The process exited with code {process.returncode} for {description}")
            logger.error(f"Error occurred : {error} during {description}")
        else:
            logger.info(f": {error.strip()} successfully for {description}")
        process.terminate()
        return output
    except Exception as e:
        logger.error(f"Error: The exception occurred {e} for {description}")


def run_subprocess_with_conda_context(args, description):
    try:
        logger.info(f"Running: {description}")
        conda_args = "conda run -n aiderenv".split()
        process_with_conda_context = subprocess.Popen(conda_args + args, shell=True, stdout=subprocess.PIPE,
                                                      stderr=subprocess.PIPE, text=True)
        output, error = process_with_conda_context.communicate()
        if process_with_conda_context.returncode != 0:
            logger.error(
                f"Error: The process exited with code {process_with_conda_context.returncode} for {description}")
            logger.error(f"Error occurred : {error} during {description}")
        else:
            logger.info(f": {error.strip()} successfully for {description}")

        process_with_conda_context.terminate()
        return output
    except Exception as e:
        logger.error(f"Error: The exception occurred {e} for {description}")


def run_command(command, shell):
    """Send a command to the shell and return the output."""
    shell.stdin.write(command + "\n")
    shell.stdin.flush()  # Ensure the command is sent to the shell

    # Read the output
    output = ""
    while True:
        line = shell.stdout.readline()
        if not line:
            break
        output += line
    return output


def initialize_aider_env():
    return


if __name__ == "__main__":
    coder = CodeAider()
    run_command("I want to create a pong game", coder.shell)
