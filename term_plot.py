# v1.08 / neurograph for terminal use
# needs `termplotlib`
# please install w/ `pip install termplotlib`

import shutil
import os
import glob
import re
import termplotlib as tpl
import numpy as np
import io


def print_line(length):
    return "=" * length


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

    output = io.StringIO()

    output.write(print_line(60) + "\n")
    output.write(f"{date_str}\n")
    output.write(print_line(60) + "\n")
    output.write("\n")

    first_x = x[0]
    first_y = y[0]
    last_x = x[-1]
    last_y = y[-1]

    last_x_str = f"{last_x:>9}"
    last_y_str = f"avg={last_y:5.2f}"

    output.write(f"{first_x:<9}{'':>{60 - 9 - len(last_x_str)}}{last_x_str}\n")
    output.write(f"{'='*10}{'':>{60 - 9 - len('=') * 9}}{'='*10}\n")
    output.write(f"avg={first_y:<5.2f}{'':>{60 - len(' avg=0.00') - len(last_y_str)}}{last_y_str}\n")

    fig = tpl.figure()
    fig.plot(x, y, width=60, height=20)

    # Center the x-axis and y-axis labels
    label = "x-axis: Iterations | y-axis: Avg"
    padding = (60 - len(label)) // 2
    output.write(f"{'':<{padding}}{label}\n")

    output.write(fig.get_string() + "\n")
    output.write("\n")

    # Print the whole output at once
    print(output.getvalue())

    # Close the StringIO object
    output.close()


if __name__ == "__main__":
    main()