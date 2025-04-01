import requests
import shutil
import gzip
import os
import logging
from collections import Counter
from .config.constants import NUM_PKG


class ContentsAnalyzer:

    def __init__(self, url, destination):
        self.url = url
        self.destination = destination

    # Method to download and save contents file
    def download_contents_file(self):
        try:
            # Skip download if file already exists
            if os.path.isfile(self.destination):
                logging.info(
                    f"File already exists: {self.destination}, skipping download"
                )
                return
            logging.info("Downloading Contents file...")
            try:
                response = requests.get(self.url, stream=True)
                response.raise_for_status()  # Check if request was successful
            except requests.exceptions.RequestException as e:
                logging.error(f"Error downloading the file: {e}")
                raise SystemExit()
            # Copy file to destination
            with open(self.destination, "wb") as out_file:
                shutil.copyfileobj(response.raw, out_file)
            logging.info(f"File downloaded successfully: {self.destination}")

        except Exception as e:
            logging.error(f"Unexpected error: {e}")
            raise SystemExit()

    # Method to find top packages with most files
    def process_contents_file(self):
        # Initialize counter
        counter = Counter()
        try:
            if os.path.getsize(self.destination) == 0:
                raise ValueError(f"File is empty!")
            # Read the gzip file
            with gzip.open(self.destination, "rt") as file:
                for line in file:
                    # Split from right as file names may contain spaces
                    content = line.rsplit()
                    # Ignore malformed lines
                    if len(content) != 2:
                        continue
                    # Get the list of packages
                    packages = content[-1].split(",")
                    # Count occurence of each package to get file count
                    for package in packages:
                        counter[package] += 1
            # Return top packages
            top_packages = counter.most_common(NUM_PKG)
            logging.info("File processing completed successully")
            return top_packages
        except Exception as e:
            logging.error(f"Error processing {self.destination}: {e}")
            raise SystemExit()

    # Method to display results to the user
    def display_top_packages(self, result):
        if not result:
            logging.warning("No results to display! Exiting...")
            raise SystemExit()
        print(f"\n{'NO.':<5} {'PACKAGE_NAME':<40} {'FILE_COUNT':<10}\n")
        for index, (package, count) in enumerate(result, start=1):
            print(f"{index:<5} {package:<40} {count:<10}")
