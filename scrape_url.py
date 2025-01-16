from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException, NoSuchElementException
import time
import json


# Function to set up Selenium WebDriver
def setup_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")  # Run in headless mode
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36")
    driver = webdriver.Chrome(options=chrome_options)
    driver.maximize_window()
    return driver


# Function to click all "Read More" or similar expandable elements
def click_expandable_elements(driver):
    # Potential selectors for expandable elements
    selectors = [
        "button",              # Generic buttons
        "a",                   # Links (e.g., 'Read More')
        "div",                 # Divs that are clickable
    ]
    for selector in selectors:
        try:
            elements = driver.find_elements(By.CSS_SELECTOR, selector)
            for element in elements:
                if element.is_displayed() and element.is_enabled():
                    try:
                        element.click()
                        time.sleep(0.5)  # Allow the content to load
                    except ElementClickInterceptedException:
                        driver.execute_script("arguments[0].scrollIntoView();", element)
                        time.sleep(0.5)
                        element.click()
        except Exception:
            continue


# Function to scroll the page to load dynamic content
def scroll_page(driver, pause_time=2):
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(pause_time)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height


# Main function to scrape the content of a page
def scrape_page(url):
    driver = setup_driver()
    try:
        # Load the page
        driver.get(url)
        time.sleep(3)  # Allow time for page to load

        # Interact with expandable elements
        click_expandable_elements(driver)

        # Scroll to the bottom to load all content
        scroll_page(driver)

        # Extract the full HTML content
        page_source = driver.page_source

        # Optional: Save the HTML to a file for review
        with open("page_content.html", "w", encoding="utf-8") as file:
            file.write(page_source)

        print("Page content scraped successfully!")
        return page_source

    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    finally:
        driver.quit()


# Example Usage
if __name__ == "__main__":
    url = "https://www.farmherbs.com/"  # Replace with your target URL
    full_content = scrape_page(url)

    # Save content as a JSON file
    with open("scraped_content.json", "w", encoding="utf-8") as json_file:
        json.dump({"URL": url, "Content": full_content}, json_file, indent=4)
