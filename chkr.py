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
                return 404, None

            asin_table = soup.find("table", id="productDetails_detailBullets_sections1")

            rows = asin_table.find_all("th")

            # Loop through the rows to find the ASIN
            asin = None
            for row in rows:
                if "ASIN" in row.text:
                    # If 'ASIN' is found, the corresponding <td> will contain the value
                    asin = row.find_next("td").text.strip()

            return 200, asin
        else:
            return response.status_code, None
    except requests.exceptions.RequestException as e:
        print(f"Error with URL {url}: {e}")
        return "Error", None


def check_urls_from_file(file_path):
    with open(file_path, "r") as file:
        urls = file.readlines()

    results = []
    for url in urls:
        url = url.strip()  # Remove any extra whitespace or newlines
        status, asin = check_url_status(url)
        results.append(
            {
                "url": url,
                "status": status,
                "ASIN": url.split("/")[-2],
                "Country": url.split("amazon")[1].split("/")[0].replace(".", ""),
            }
        )

    return results


# Function to write the results to a CSV file
def write_results_to_csv(results, output_file):
    with open(output_file, "w", newline="") as csvfile:
        fieldnames = ["url", "ASIN", "Country", "status"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for result in results:
            writer.writerow(result)


if __name__ == "__main__":
    input_file = "url.txt"
    output_file = "url_status_report.csv"

    results = check_urls_from_file(input_file)

    write_results_to_csv(results, output_file)

    print(f"[✅] written to {output_file}")
