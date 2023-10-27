import os
import subprocess
from datetime import datetime

def get_unique_filename():
    tsfmt = datetime.now().strftime("%Y%m%d-%H%M%S")
    counter = 0
    while True:
        filename = f"tmp{tsfmt}-{counter}.log"
        if not os.path.exists(filename):
            return filename
        counter += 1

def write_datetime_to_file(filename):
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(filename, 'w') as file:
        file.write(f"Current Date and Time is: {current_time}\n")
        unamea = subprocess.check_output("uname -a", shell=True, universal_newlines=True)
        file.write(f"Result of `uname -a` is: {unamea}\n")

if __name__ == "__main__":
    unique_filename = get_unique_filename()
    write_datetime_to_file(unique_filename)
    print(f"File '{unique_filename}' has been created.")