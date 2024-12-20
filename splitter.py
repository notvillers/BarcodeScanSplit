'''Running the splitter by argument'''

import argparse
from src.main import run as run_by_arg_run

parser: argparse.ArgumentParser = argparse.ArgumentParser(
    prog = "PDF Splitter",
    description = "Split PDF files into individual pages, by reading the barcode on each page"
)

arg_list: list[list[any]] = [
    ["-s", "--source", str, "Directory containing PDF files"],
    ["-d", "--destination", str, "Directory to store output files"],
    ["-b", "--backup", str, "Directory to store backup files"],
    ["-l", "--log", str, "Directory to store log files"],
    ["-t", "--temp", str, "Temporary directory to store split PDF files"],
    ["-i", "--image", str, "Temporary directory to store the images"],
    ["-m", "--mode", str, "Mode of operation (single|multi), by default is single"],
    ["-p", "--processes", int, "Maximum number of processes to run, by default is the number of CPU threads"]
]

for arg in arg_list:
    parser.add_argument(arg[0], arg[1], type = arg[2], help = arg[3])

args: argparse.Namespace = parser.parse_args()

def main() -> None:
    '''Main function'''
    run_by_arg_run(
        pdf_dir = args.source,
        temp_dir = args.temp,
        image_dir = args.image,
        output_dir = args.destination,
        backup_dir = args.backup,
        log_dir = args.log,
        mode = args.mode,
        max_processes = args.processes
    )


if __name__ == '__main__':
    main()

# TODO: only create default directories if needed
