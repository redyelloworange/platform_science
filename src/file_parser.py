def parse_newline_separated_file(filename: str):
    with open(filename, 'r') as f:
        return f.read().splitlines()
