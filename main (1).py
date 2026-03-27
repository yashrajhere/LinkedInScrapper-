import sys
import time
import requests
from bs4 import BeautifulSoup
from rich.console import Console
from rich.table import Table

console = Console()

# Try Selenium (PC mode)
try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    SELENIUM_AVAILABLE = True
except:
    SELENIUM_AVAILABLE = False


# 🌐 LITE MODE (Termux)
def scrape_lite(url):
    headers = {"User-Agent": "Mozilla/5.0"}
    res = requests.get(url, headers=headers)

    soup = BeautifulSoup(res.text, "html.parser")

    data = {}
    data["Mode"] = "LITE (Public Only)"

    name = soup.find("h1")
    data["Name"] = name.text.strip() if name else "N/A"

    headline = soup.find("title")
    data["Headline"] = headline.text.strip() if headline else "N/A"

    return data


# 💻 FULL MODE (PC)
def scrape_full(url):
    options = webdriver.ChromeOptions()
    options.add_argument("user-data-dir=./session")

    driver = webdriver.Chrome(options=options)
    driver.get(url)
    time.sleep(5)

    data = {}
    data["Mode"] = "FULL (Logged In)"

    try:
        data["Name"] = driver.find_element(By.TAG_NAME, "h1").text
    except:
        data["Name"] = "N/A"

    try:
        data["Headline"] = driver.find_element(By.CLASS_NAME, "text-body-medium").text
    except:
        data["Headline"] = "N/A"

    try:
        data["Location"] = driver.find_element(By.CLASS_NAME, "text-body-small").text
    except:
        data["Location"] = "N/A"

    driver.quit()
    return data


# 🎨 Display
def display(data):
    table = Table(title="LinkedIn Scraper")

    table.add_column("Field", style="cyan")
    table.add_column("Value", style="green")

    for k, v in data.items():
        table.add_row(k, str(v))

    console.print(table)


# 🏁 Main CLI
def main():
    console.print("[bold green]Universal LinkedIn Scraper[/bold green]")

    if SELENIUM_AVAILABLE:
        console.print("[yellow]Running in FULL mode (PC)[/yellow]")
    else:
        console.print("[red]Running in LITE mode (Termux)[/red]")

    while True:
        url = input("\nEnter Profile URL (or exit): ")

        if url.lower() == "exit":
            break

        if SELENIUM_AVAILABLE:
            data = scrape_full(url)
        else:
            data = scrape_lite(url)

        display(data)


if __name__ == "__main__":
    main()