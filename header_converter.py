import os
import re
import sys

def convert_header(input_file):
    pattern = r'#include\s+<(.+?)>'
    file = open(input_file, "r")
    lines = []
    for line in file.readlines():
        if re.search(pattern, line):
            line = re.sub(pattern, r'#include "\1"', line)
        lines.append(line)
    file = open(input_file, "w", newline='\r\n')
    file.writelines(lines)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: python {sys.argv[0]} file/folder")
        sys.exit(1)

    input = sys.argv[1]
    if os.path.isfile(input):
        convert_header(input)
    elif os.path.isdir(input):
        for root, _, files in os.walk(input):
            for file in files:
                convert_header(os.path.join(root, file))


