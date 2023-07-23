import re
import sys

def convert_file(input_file, output_file):
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        content = infile.read()

        # Regular expression to find protocol name and GUID
        pattern = re.compile(r'#define\s+(\w+)\s+.*?\{(.*?)\}', re.DOTALL)

        # Find all occurrences of the protocol name and GUID
        matches = pattern.findall(content)

        # Write the converted output to the outfile
        for protocol, guid in matches:
            guid = re.sub(r'\s+', '', guid)  # Remove whitespace from the GUID
            guid = re.sub(r'\\+', '', guid)  # Remove backslashes from the GUID
            outfile.write(f"///@protocol {{{guid}}}}}\n")  # Include the closing curly brace
            outfile.write(f"///@binding {protocol} {{{guid}}}}}\n")  # Include the closing curly brace
            outfile.write(f"struct {protocol.rstrip('_GUID')}")
            outfile.write("\n")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(f"Usage: python {sys.argv[0]} input_file output_file")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]
    convert_file(input_file, output_file)
