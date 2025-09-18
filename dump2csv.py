import argparse
import os
import re
import csv


class InvalidPathError(Exception):
    pass


def parse_sql_dump(
    input_file: str, tables_whitelist: list[str]
) -> dict[str, list[list[str]]]:
    """
    parse .sql dump file and extracts data for specified tables.
    """
    table_values: dict[str, list[list[str]]] = {}
    current_table: str = ""
    is_whitelisted: bool = False

    with open(input_file, "r") as f:
        for line in f:
            line_stripped = line.strip().lower()

            if line_stripped.startswith("create table"):
                is_whitelisted = False
                match = re.search(r"create\s+table\s+`?(\w+)`?", line_stripped)
                if match:
                    table_name = match.group(1)
                    if not tables_whitelist or table_name in tables_whitelist:
                        current_table = table_name
                        table_values[current_table] = []
                        is_whitelisted = True
                    else:
                        current_table = ""
            elif line_stripped.startswith("insert into") and is_whitelisted:
                match = re.search(r"values\s*\((.*)\);", line_stripped)
                if match:
                    values_str = match.group(1)
                    values = [v.strip().strip("'\"") for v in values_str.split(",")]
                    table_values[current_table].append(values)

    return table_values


def save_data_to_csv(
    data: dict[str, list[list[str]]],
    output_dir: str,
    output_prefix: str,
    separator: str,
):
    """
    saves extracted data to csv files
    """
    if not output_dir.endswith(os.sep):
        output_dir += os.sep

    for table, rows in data.items():
        output_path = f"{output_dir}{output_prefix}{table}.csv"
        with open(output_path, "w", newline="") as csvfile:
            writer = csv.writer(csvfile, delimiter=separator)
            writer.writerows(rows)


def validate_args(args: argparse.Namespace):
    """
    validate command-line arguments.
    """
    if not os.path.isfile(args.input):
        raise FileNotFoundError(f"File '{args.input}' not found.")

    if not args.input.endswith(".sql"):
        raise ValueError(f"File '{args.input}' is not an .sql file.")

    if args.outputdir:
        if not os.path.isdir(args.outputdir):
            raise InvalidPathError(
                f"Output directory '{args.outputdir}' does not exist."
            )


def main():
    parser = argparse.ArgumentParser(
        prog="dump2data",
        description="Extract data from an .sql dump to .csv files.",
    )

    parser.add_argument("-i", "--input", help="Path to input .sql file", required=True)
    parser.add_argument("--seperator", default=",", help="CSV separator")
    parser.add_argument(
        "-t",
        "--tables",
        help="Whitelist tables for extraction (e.g., 'users,orders')",
    )
    parser.add_argument(
        "-od", "--outputdir", default="./", help="Path to the output directory"
    )
    parser.add_argument(
        "-op", "--outputprefix", default="", help="Prefix for output filenames"
    )

    args = parser.parse_args()

    try:
        validate_args(args)
        tables_whitelist = args.tables.split(",") if args.tables else []
        parsed_data = parse_sql_dump(args.input, tables_whitelist)
        save_data_to_csv(parsed_data, args.outputdir, args.outputprefix, args.seperator)

    except (FileNotFoundError, ValueError, InvalidPathError) as e:
        print(f"err: {e}")
        exit(1)


if __name__ == "__main__":
    main()
