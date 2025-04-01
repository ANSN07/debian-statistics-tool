# debian-statistics-tool
A Python CLI tool to analyze Debian package contents.
## Description
This CLI tool identifies the top 10 packages with the most files for a selected architecture by analyzing a contents file downloaded from a Debian mirror.

## Project Structure
- `package_statistics`
    - `config`
        - `constants.py`
    - `__init__.py`
    - `__main__.py`
    - `contents_analyzer.py`
- `pyproject.toml`
- `logs`
    - `app.log`

The starting point of the project is `main.py`, where I set up the CLI using the Argparse module in Python. The CLI tool accepts one argument, "architecture", allowing users to choose from a set of valid values. I used the logging module to structure logs properly. Logs are both displayed in the console and stored in a file under the `logs` folder. All constants are stored in a separate file inside the `config` folder. The main logic for downloading, processing the file and displaying results is encapsulated within a class and methods inside `contents_analyzer.py`. The entire project is organized within the `package_statistics` package. 

To handle the file, I download it from a mirror and copy it to a local destination. Instead of extracting the gzip file, I read it directly, as I do not need to store the state, making this approach faster. While extracting package names from each line in the file, I had to be cautious about malformed lines that do not conform to the expected structure (ie. columns containing filenames and package names). To address this, I split each line from the right, as package names do not contain spaces. I used a Counter to track occurrences of each package, which allowed me to count the number of files per package. To retrieve the top packages with the most files, I used the most_common method from collections.Counter.

Initially, I explored different options for building the command-line interface, including Argparse, Click, and Typer. I found Argparse to be relatively simple and sufficient for my needs. It automatically handles invalid or missing arguments without requiring additional configuration, saving development time.

I spent time structuring my project, using packages, modules, and classes appropriately to ensure reusability. Additionally, I considered alternative approaches to optimize time complexity, such as using a dictionary with sorted() and a defaultdict with a heapq. However, the Counter + most_common approach provided the best performance. Since I was working with a large file (almost 1 GB), it was important to choose the most efficient methods for downloading and processing.

It also took me some time to set up error handling, logging, linting (I used Black), testing, dependency management, and a virtual environment. Overall, the assessment took me approximately three days to complete. If I had additional time, I would focus on implementing unit tests to improve code reliability.

## Steps to run the project

1. Navigate to the project directory
2. Create a virtual environment named `venv` in your current directory:
```sh
python3 -m venv venv
```
3. Activate the virtual environment:
- On Linux/macOS:
```sh
source venv/bin/activate
```
- On Windows (Command Prompt):
```sh
venv\Scripts\activate
```
4.  Install Dependencies:
```sh
pip install -e .
```
5. Run the project:
```sh
package_statistics <architecture>
```
Example:
```sh
package_statistics i386
```
6. To show help:
```sh
package_statistics -h

