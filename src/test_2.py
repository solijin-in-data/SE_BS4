from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium_stealth import stealth
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time, random
from fake_useragent import UserAgent
import subprocess
#from python_anticaptcha import AnticaptchaClient

# Print versions for debugging
print("Selenium version:", webdriver.__version__)
chrome_driver_path = ChromeDriverManager().install()
result = subprocess.run([chrome_driver_path, "--version"], capture_output=True, text=True)
print("ChromeDriver version:", result.stdout.strip())

# Selenium optimization
options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("useAutomationExtension", False)
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36")
options.add_argument("--start-maximized")
options.add_argument("--disable-blink-features=AutomationControlled")

# Initialize driver
driver = webdriver.Chrome(service=Service(chrome_driver_path), options=options)

# Hide navigator.webdriver
driver.execute_cdp_cmd(
    'Page.addScriptToEvaluateOnNewDocument',
    {'source': 'Object.defineProperty(navigator, "webdriver", {get: () => undefined})'}
)

# Scrape data
url = "https://tradingeconomics.com/vietnam/gdp"
try:
    driver.get(url)

    # Simulate human-like behavior
    actions = ActionChains(driver)
    actions.move_by_offset(random.randint(50, 200), random.randint(50, 200)).click().perform()
    time.sleep(random.uniform(1, 3))
    driver.execute_script("window.scrollBy(0, 400);")
    time.sleep(random.uniform(2, 4))

    # Get HTML
    html = driver.page_source
    soup = BeautifulSoup(html, "lxml")

    # Check for bot detection
    if any(x in html.lower() for x in ["access denied", "403 forbidden", "captcha"]):
        print("BOT recognized")
    else:
        print("Access complete")

        # Locate the chart bars (adjust selector based on inspection)
        bars = driver.find_elements(By.CSS_SELECTOR, ".highcharts-series-group .highcharts-point")  # Example selector
        if not bars:
            print("No bars found, check the CSS selector")
        else:
            gdp_values = {}
            for bar in bars:
                # Move to the bar to trigger tooltip
                actions.move_to_element(bar).perform()
                time.sleep(1)  # Wait for tooltip to populate

                # Try to find the tooltip or updated element containing the value
                try:
                    tooltip = WebDriverWait(driver, 5).until(
                        EC.presence_of_element_located((By.CLASS_NAME, "highcharts-tooltip"))  # Adjust class if needed
                    )
                    value = tooltip.text.strip()  # Extract the text from the tooltip
                    year = bar.get_attribute("data-x") or bar.get_attribute("x")  # Try to get year from bar attributes
                    if year:
                        gdp_values[year] = value
                    print(f"Year: {year}, GDP: {value}")
                except Exception as e:
                    print(f"Error extracting value for bar: {e}")

            if gdp_values:
                print("Extracted GDP values:", gdp_values)
            else:
                print("No GDP values extracted, check tooltip locator")

        # Save HTML for debugging
        with open("page.html", "w", encoding="utf-8") as f:
            f.write(driver.page_source)
        print("HTML saved to page.html for inspection")

except Exception as e:
    print("Error in scraping process:", str(e))

finally:
    time.sleep(3)
    driver.quit()