'''Running the splitter by argument'''

from argparse import ArgumentParser, Namespace
from multiprocessing import freeze_support
from src.main import PathConfig, run as run_by_arg_run

parser: ArgumentParser = ArgumentParser(
    prog = "PDF Splitter",
    description = "Split PDF files into individual pages, by reading the barcode on each page"
)

arg_list: list[list[any]] = [["-s","--source", str, "Directory containing PDF files"],
                             ["-d", "--destination", str, "Directory to store output files"],
                             ["-b", "--backup", str, "Directory to store backup files"],
                             ["-l", "--log", str, "Directory to store log files"],
                             ["-t", "--temp", str, "Temporary directory to store split PDF files"],
                             ["-i", "--image", str, "Temporary directory to store the images"],
                             ["-m", "--mode", str, "Mode of operation (single|multi), by default is single"], # pylint: disable=line-too-long
                             ["-p", "--processes", int, "Maximum number of processes to run, by default is the number of CPU threads"], # pylint: disable=line-too-long
                             ["-f", "--prefixes", str, "Prefixes for OCR reading if barcode not found (ex.: 'KSZ,EKSZ')"], # pylint: disable=line-too-long
                             ["-r", "--ratio", float, "Image ratio to check for OCR, only neccessary if `--text-prefixes` is given (ex.: 0.4 means it scans from top to bottom 40%% of the image)"]] # pylint: disable=line-too-long

for arg in arg_list:
    parser.add_argument(arg[0],
                        arg[1],
                        type = arg[2],
                        help = arg[3])

args: Namespace = parser.parse_args()

def main() -> None:
    '''
        Main function
    '''
    path_config: PathConfig = PathConfig(source = args.source,
                                         destination = args.destination,
                                         temp = args.temp,
                                         image = args.image,
                                         backup = args.backup,
                                         log = args.log)
    run_by_arg_run(path_config = path_config,
                   mode = args.mode,
                   max_processes = args.processes,
                   ocr_prefixes = args.prefixes,
                   ratio = args.ratio)


if __name__ == '__main__':
    freeze_support()
    main()
