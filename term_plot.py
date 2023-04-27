
# v1.07 / neurograph for terminal use
# needs `termplotlib`
# please install w/ `pip install termplotlib`

import shutil
import os
import glob
import re
import termplotlib as tpl
import numpy as np


def print_line(length):
    print("=" * length)

""" def print_line():
    terminal_width = shutil.get_terminal_size().columns
    print("=" * terminal_width) """

def main():
    log_dir = "logs/"
    log_files = glob.glob(log_dir + "*.txt")
    latest_log = max(log_files, key=os.path.getctime)

    with open(latest_log, "r") as file:
        lines = file.readlines()

    x = []
    y = []
    date_str = ""

    for line in lines:
        if line.startswith(":::"):
            date_match = re.search(r'::: (.+ \d+ \d+:\d+:\d+ [A-Za-z]+ \d+)', line)
            if date_match:
                date_str = date_match.group(1)
        elif line.startswith("["):
            match = re.search(r'\[(\d+)\s\|\s[\d.]+\]\sloss=[\d.]+\savg=([\d.]+)', line)
            if match:
                x.append(int(match.group(1)))
                y.append(float(match.group(2)))

    print_line(60)
    print(f"{date_str}")
    print_line(60)
    print()

    first_x = x[0]
    first_y = y[0]
    last_x = x[-1]
    last_y = y[-1]

    print(f"{first_x:<7}{'':>42}{last_x:>7}")
    print(f"{'='*7}{'':>42}{'='*7}")
    print(f"avg={first_y:<6.2f}{'':>39}avg={last_y:.2f}")

    fig = tpl.figure()
    fig.plot(x, y, width=60, height=20)

    # Center the x-axis and y-axis labels
    label = "x-axis: Iterations | y-axis: Avg"
    padding = (60 - len(label)) // 2
    print(f"{'':<{padding}}{label}")

    fig.show()
    print()

if __name__ == "__main__":
    main()
