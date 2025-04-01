import argparse
from .contents_analyzer import ContentsAnalyzer
import logging
from .config.constants import ARCHITECTURES, FILE_SAVE_PATH, URL

# Set up the basic configuration for logging
logging.basicConfig(
    level=logging.INFO,  # Capture all log messages except Debug logs
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.FileHandler("logs/app.log"),  # Store logs in a file
        logging.StreamHandler(),  # Log to console
    ],
)


def main():
    try:
        parser = argparse.ArgumentParser(
            description="A Python CLI tool to generate Debian package statistics"
        )
        # Define an argument "architecture" with a set of valid values
        parser.add_argument(
            "architecture",
            type=str,
            choices=ARCHITECTURES,
            help="Architecture (eg: amd64, arm64)",
        )
        # Parse the command-line arguments
        args = parser.parse_args()
        logging.debug(f"Selected architecture: {args.architecture}")

        # Debian mirror
        url = URL.format(args.architecture)
        # Destination to save the downloaded file
        destination = FILE_SAVE_PATH.format(args.architecture)

        analyzer = ContentsAnalyzer(url, destination)
        analyzer.download_contents_file()
        result = analyzer.process_contents_file()
        analyzer.display_top_packages(result)
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        raise SystemExit()


if __name__ == "__main__":
    main()
