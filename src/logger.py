import datetime
import sys


def print_info(origin_module, message):
    print_log_entry(origin_module, message, "INFO")
    sys.stdout.flush()


def print_debug(origin_module, message):
    print_log_entry(origin_module, message, "DEBUG")
    sys.stdout.flush()


def print_error(origin_module, message):
    print_log_entry(origin_module, message, "ERROR")
    sys.stdout.flush()


def print_log_entry(origin_module, message, level):
    module_name = origin_module.split("/")[-1].split(".")[0]
    log_message = "[{}] [{}] '{}' : {}".format(datetime.datetime.now(), level, module_name, message)
    print(log_message)
    sys.stdout.flush()
