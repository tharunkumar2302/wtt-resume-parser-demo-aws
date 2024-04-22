# import logging
# import os
# from datetime import datetime

# # Set the log file name with current date and time
# LOG_FILE_NAME = f"{datetime.now().strftime('%m%d%Y__%H%M%S')}.log"

# # Set the log file directory
# LOG_FILE_DIR = os.path.abspath(os.path.join(os.getcwd(), "logs"))

# # Create log file directory if not exists
# os.makedirs(LOG_FILE_DIR, exist_ok=True)

# # Set the full log file path
# LOG_FILE_PATH = os.path.join(LOG_FILE_DIR, LOG_FILE_NAME)

# # Print the log file path
# print(f"Log file path: {LOG_FILE_PATH}\n")

# # Configure the logging object
# logging.basicConfig(
#     filename=LOG_FILE_PATH,
#     format="[ %(asctime)s ] %(lineno)d %(name)s - %(levelname)s - %(message)s",
#     level=logging.INFO,
# )

# logger = logging.getLogger(__name__)
# # logger.setLevel(logging.INFO)

# # Write messages to the log file
# logging.info("This is a informational message.")
# logging.warning("This is a warning message.")
# logging.error("This is an error message.")
# logging.critical("This is a critical message.")


import logging
import os
from datetime import datetime

# Set the log file name with current date and time
LOG_FILE_NAME = f"{datetime.now().strftime('%m%d%Y__%H%M%S')}.log"

# Set the log file directory
LOG_FILE_DIR = os.path.abspath(os.path.join(os.getcwd(), "logs"))

# Print the log file path
# print(f"Log file path: {LOG_FILE_PATH}\n")

# Check if the log file directory exists, and create it if it doesn't
if not os.path.isdir(LOG_FILE_DIR):
    os.mkdir(LOG_FILE_DIR)

# Construct the log file path
LOG_FILE_PATH = os.path.join(LOG_FILE_DIR, LOG_FILE_NAME)

# Initialize the custom handler for logging
handler = logging.FileHandler(LOG_FILE_PATH, mode='w')

# Format the log entries
formatter = logging.Formatter("[ %(asctime)s ] %(lineno)d %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)

# Get the root logger
root_logger = logging.getLogger()

# Add the custom handler to the root logger
root_logger.addHandler(handler)

# Configure the logging level
root_logger.setLevel(logging.INFO)

# Write messages to the log file
# logging.debug("This is a debug message.")
# logging.info("This is a informational message.")
# logging.warning("This is a warning message.")
# logging.error("This is an error message.")
# logging.critical("This is a critical message.")

# Remove the added custom handler to prevent redundant logs in future runs
# for hdlr in root_logger.handlers[:]:
#     if isinstance(hdlr, logging.FileHandler):
#         root_logger.removeHandler(hdlr)