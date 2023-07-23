import re
import sys


def convert_to_g_guid(name):
    words = name.split("_")
    camel_case = "".join(word.capitalize() for word in words)
    g_guid = "g" + camel_case
    return g_guid


def convert_file(input_file, output_file):
    with open(input_file, "r") as infile, open(output_file, "w") as outfile:
        content = infile.read()

        # Regular expression to find protocol name and GUID
        pattern = re.compile(r"#define\s+(\w+)\s+.*?\{(.*?)\}", re.DOTALL)

        # Find all occurrences of the protocol name and GUID
        matches = pattern.findall(content)

        # Write the converted output to the outfile
        for protocol, guid in matches:
            guid = re.sub(r"\s+", "", guid)  # Remove whitespace from the GUID
            guid = re.sub(r"\\+", "", guid)  # Remove backslashes from the GUID
            protocol = protocol.rstrip("_GUID")
            if "PROTOCOL" not in protocol:
                protocol += "_PROTOCOL"
            outfile.write(f"///@protocol {{{guid}}}}}\n")
            outfile.write(f"///@binding {convert_to_g_guid(protocol)} {{{guid}}}}}\n")
            outfile.write(f"struct {protocol}\n\n")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(f"Usage: python {sys.argv[0]} input_file output_file")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]
    convert_file(input_file, output_file)
