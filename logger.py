import logging
from termcolor import colored

logging.basicConfig(filename='test.log', level = logging.INFO,
                    format='%(asctime)s:%(message)s')
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("rothemain.rothe_utils")
logging.getLogger('UFL').setLevel(logging.WARNING)
logging.getLogger('FFC').setLevel(logging.WARNING)

def log_n_output(message, color):
    logging.info(message)
    print_colored(message, color)
    
def log_n_output_colored_message(colored_message, color, white_message):
    logging.info(colored_message + white_message)
    print_colored_n_white(colored_text=colored_message, color=color, white_text=white_message)
    
def log_n_output_return_carriage(message, color):
    logging.info(message)
    print_colored(message + "\n", color)

def info(message):
    logging.info(message)
    
def print_colored(text, color):
    print(colored(text, color))
    
def print_colored_n_white(colored_text, color, white_text):
    print(colored(colored_text, color) + white_text)