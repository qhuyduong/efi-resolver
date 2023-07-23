import re
import sys


def convert_file(input_file, output_file):
    with open(input_file, "r") as infile, open(output_file, "w") as outfile:
        for line in infile.readlines():
            name = line.split("=")[0].replace(" ", "")
            guid = line.split("=")[1].replace(" ", "")
            outfile.write(f"///@protocol {guid}")
            outfile.write(f"///@binding {name} {guid}")
            protocol = re.sub(r"(?<!^)(?=[A-Z])", "_", name[1:]).upper()
            outfile.write(f"struct {protocol.replace('_GUID', '')}\n\n")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(f"Usage: python {sys.argv[0]} input_file output_file")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]
    convert_file(input_file, output_file)
