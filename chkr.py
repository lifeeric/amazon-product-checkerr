import requests
from bs4 import BeautifulSoup
import csv


# Function to check if the product is available
def check_url_status(url):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        response = requests.get(url, timeout=10, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")

            unavailable_message = soup.find(id_="productTitle")

            if unavailable_message is not None:
                return 404
            return 200
        else:
            return response.status_code
    except requests.exceptions.RequestException as e:
        print(f"Error with URL {url}: {e}")
        return "Error"


def check_urls_from_file(file_path):
    with open(file_path, "r") as file:
        urls = file.readlines()

    for i, url in enumerate(urls):
        url = url.strip()  # Remove any extra whitespace or newlines
        status = check_url_status(url)
        result = {
            "url": url,
            "status": status,
            "ASIN": url.split("/")[-2],
            "Country": url.split("amazon")[1].split("/")[0].replace(".", ""),
        }

        write_result_to_csv(result)

        printProgressBar(
            i + 1,
            len(urls),
            prefix="Progress:",
            suffix="Complete",
            length=70,
        )

    return results


# Function to write the results to a CSV file
def write_result_to_csv(result):
    output_file = "url_status_report.csv"
    with open(output_file, "a", newline="") as csvfile:
        fieldnames = ["url", "ASIN", "Country", "status"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writerow(result)


# Print iterations progress
def printProgressBar(
    iteration, total, prefix="", suffix="", decimals=1, length=100, fill="█"
):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + "-" * (length - filledLength)
    print("\r%s |%s| %s%% %s" % (prefix, bar, percent, suffix), end="\r")
    # Print New Line on Complete
    if iteration == total:
        print()


if __name__ == "__main__":
    input_file = "url.txt"
    results = check_urls_from_file(input_file)
    print(f"[Done] ✅")
