import time
import sys
from rich.console import Console
from rich.progress import Progress
from rich.panel import Panel
from rich import print

# Selenium
from selenium import webdriver
from selenium.webdriver.common.by import By

console = Console()

# 🎨 Banner
def banner():
    console.print(Panel.fit(
        "[bold cyan]LINKEDIN SCRAPPER BY RAJ 🔥[/bold cyan]",
        border_style="green"
    ))

    console.print("\n[bold yellow]HOW TO USE:[/bold yellow]", style="yellow")
    console.print("[green]1. Enter your LinkedIn login credentials[/green]")
    console.print("[green]2. Wait for login success[/green]")
    console.print("[green]3. Enter profile URL to scrape[/green]\n")


# 🔐 Login Function
def login(driver, user, password):
    driver.get("https://www.linkedin.com/login")
    time.sleep(2)

    driver.find_element(By.ID, "username").send_keys(user)
    driver.find_element(By.ID, "password").send_keys(password)
    driver.find_element(By.ID, "password").submit()


# ⏳ Loading Bar
def loading():
    with Progress() as progress:
        task = progress.add_task("[cyan]Logging in...", total=100)

        for i in range(100):
            time.sleep(0.02)
            progress.update(task, advance=1)


# 🧠 Scraper
def scrape(driver, url):
    driver.get(url)
    time.sleep(5)

    data = {}

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

    return data


# 🎨 Display
def display(data):
    console.print("\n[bold green]SCRAPED DATA 🔥[/bold green]\n")

    for k, v in data.items():
        console.print(f"[cyan]{k}[/cyan] : [white]{v}[/white]")


# 🚀 MAIN
def main():
    banner()

    console.print("[bold red]LOGIN FIRST TO USE THIS TOOL 🔐[/bold red]\n")

    user = input("USER: ")
    password = input("PASS: ")

    # Browser
    options = webdriver.ChromeOptions()
    options.add_argument("user-data-dir=./session")

    driver = webdriver.Chrome(options=options)

    login(driver, user, password)

    # Loading animation
    loading()

    console.print("\n[bold green]LOGIN SUCCESSFULL ✅[/bold green]\n")

    while True:
        url = input("Enter username or URL you want to scrap data (or exit): ")

        if url.lower() == "exit":
            break

        data = scrape(driver, url)
        display(data)

    driver.quit()


if __name__ == "__main__":
    main()
