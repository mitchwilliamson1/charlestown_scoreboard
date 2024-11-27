import sys
import os
import importlib
import traceback
import argparse
from pathlib import Path

IGNORE = ["__init__.py", "config_methods.py"]
EXTEN = ".py"

# Definition of Arguments for the program
def run_arg_parser():
    parser = argparse.ArgumentParser(description="Parser to Specify Config")

    choices = get_config_modules()
    # Argument to specify which config module to import
    parser.add_argument(
        "-config",
        required=True,
        choices=choices,
        type=str,
        action="store",
        dest="config_module",
        help="Argument to specify which config to load from config dir",
    )
    # Argument if running as a windows service. Will force the location of python log files into separate directory
    # Enabling cmd to be called without having to delete existing log files
    parser.add_argument(
        "-is_win_service",
        required=False,
        action="store_true",
        dest="is_win_service",
        help="Argument to specify if codebase will be run as windows service",
    )
    # Argument to specify if running in development mode. Will output all >= DEBUG levels logs to console
    parser.add_argument(
        "-is_dev",
        required=False,
        action="store_true",
        dest="is_dev",
        help="Argument to specify if codebase will be run as development. If specified DEBUG level logs with be output to stdout console",
    )

    # Arguments to Ignore from Python Service
    parser.add_argument("-debug", action="store", help=argparse.SUPPRESS)
    parser.add_argument("-install", help=argparse.SUPPRESS)
    parser.add_argument("-start", help=argparse.SUPPRESS)
    parser.add_argument("-stop", help=argparse.SUPPRESS)

    return parser.parse_args()


# Loads the name of each config module in the config folder
def get_config_modules():
    config_modules = []
    for conf_file in os.listdir(os.path.dirname(os.path.realpath(__file__))):
        if conf_file.endswith(EXTEN) and conf_file not in IGNORE:
            config_module = conf_file[: -len(EXTEN)]
            config_modules.append(config_module)
    return config_modules


# Attempt to import the configuration module specified by module_name param
def import_module(module_name):
    try:
        global cfg
        cfg = importlib.import_module(".{}".format(module_name), __name__)
        validate_config(module_name, cfg)
        unpack_module(cfg)
    except ModuleNotFoundError as e:
        print("Unable to import configuration {}. Try:".format(module_name))
        print(traceback.format_exc())
        sys.exit(-1)


# Check config contains certain attributes
def validate_config(module_name, module):
    attrs = {
        "LOG_CONF": "LOG_CONF (Python Logger DictConfig) is required in the config to provide the program logger with a valid logging config for logger calls"
    }
    for attr, reason in attrs.items():
        if not hasattr(module, attr):
            raise Exception(
                f"{attr} attribute is missing from module configs/{module_name}.py. {reason}"
            )


# Loads attributes defined in param module into current module so it can be accessed as an attribute of the config module
def unpack_module(module):
    # Unpack config into current module
    for item in dir(module):
        # Skip private/sys items
        if item.startswith("__"):
            continue

        # Set all the contents of the config file to the current module
        # this will keep config imports super clean
        setattr(sys.modules[__name__], item, getattr(module, item))


# Creates a folder to store logs for the program
def prepare_log_folders(is_win_service):
    config_file_path = Path(__file__).parent.resolve()
    service_logs_file_path = os.path.join(config_file_path, "..", "logs", "service_log")
    console_logs_file_path = os.path.join(config_file_path, "..", "logs", "console_log")

    Path(service_logs_file_path).mkdir(parents=True, exist_ok=True)
    Path(console_logs_file_path).mkdir(parents=True, exist_ok=True)

    if is_win_service:
        return service_logs_file_path
    else:
        return console_logs_file_path


# Forces all filepaths for logging config handlers to the provided path param
def set_log_handlers_path(log_config, path):
    for handler_name, handler_config in log_config["handlers"].items():
        if "filename" in handler_config:
            handler_config["filename"] = os.path.join(path, handler_config["filename"])


# Adds a config logger called console which will stream all >= debug level logs to the console
# Adds the console logger to each handler
def enable_logging_to_console(log_config, is_dev):
    if not is_dev:
        return
    console_logger_config = {
        "level": "DEBUG",
        "formatter": "standard",
        "class": "logging.StreamHandler",
    }
    log_config["handlers"]["console"] = console_logger_config
    for logger_name, logger_config in log_config["loggers"].items():
        logger_config["handlers"].append("console")


args = run_arg_parser()
import_module(args.config_module)
log_config = getattr(sys.modules[__name__], "LOG_CONF")
log_path = prepare_log_folders(args.is_win_service)
set_log_handlers_path(LOG_CONF, log_path)
enable_logging_to_console(LOG_CONF, args.is_dev)
