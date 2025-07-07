from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from selenium_stealth import stealth
import time
import random
import subprocess

# In phiên bản để kiểm tra
print("Phiên bản Selenium:", webdriver.__version__)
chrome_driver_path = ChromeDriverManager().install()
result = subprocess.run([chrome_driver_path, "--version"], capture_output=True, text=True)
print("Phiên bản ChromeDriver:", result.stdout.strip())

# Cấu hình Selenium
options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("useAutomationExtension", False)
ua = UserAgent()
options.add_argument(f"user-agent={ua.random}")
options.add_argument("--start-maximized")
# options.add_argument("--headless=new")  # Bỏ tạm để kiểm tra
options.add_argument("--disable-blink-features=AutomationControlled")

# Khởi tạo driver
driver = webdriver.Chrome(service=Service(chrome_driver_path), options=options)

# Ẩn dấu hiệu Selenium
driver.execute_cdp_cmd(
    'Page.addScriptToEvaluateOnNewDocument',
    {'source': 'Object.defineProperty(navigator, "webdriver", {get: () => undefined})'}
)
stealth(driver,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True)

# Lấy dữ liệu
url = "https://tradingeconomics.com/vietnam/gdp"
try:
    driver.get(url)
    time.sleep(5)  # Chờ trang tải hoàn toàn

    # Mô phỏng hành vi người dùng
    actions = ActionChains(driver)
    actions.move_by_offset(random.randint(50, 200), random.randint(50, 200)).click().perform()
    time.sleep(random.uniform(1, 3))
    driver.execute_script("window.scrollBy(0, 400);")
    time.sleep(random.uniform(2, 4))

    # Lấy HTML
    html = driver.page_source
    soup = BeautifulSoup(html, "lxml")

    # Kiểm tra phát hiện bot
    if any(x in html.lower() for x in ["access denied", "403 forbidden", "captcha"]):
        print("BOT bị nhận diện")
    else:
        print("Truy cập thành công")

        # Tìm các cột trong biểu đồ
        bars = driver.find_elements(By.CSS_SELECTOR, ".highcharts-series-group .highcharts-point")
        if not bars:
            print("Không tìm thấy cột, kiểm tra lại selector CSS")
        else:
            gdp_values = {}
            for index, bar in enumerate(bars):
                actions.move_to_element(bar).perform()
                time.sleep(2)  # Chờ tooltip
                try:
                    # Tìm phần tử tooltip-box
                    tooltip_box = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.CLASS_NAME, "tooltip-box"))
                    )
                    # Lấy năm từ <span class="tooltip-date">
                    date_element = WebDriverWait(tooltip_box, 5).until(
                        EC.presence_of_element_located((By.CLASS_NAME, "tooltip-date"))
                    )
                    year = date_element.text.strip()
                    # Lấy giá trị GDP từ <span class="hawk-tt tooltip-value">
                    gdp_element = WebDriverWait(tooltip_box, 5).until(
                        EC.presence_of_element_located((By.CLASS_NAME, "hawk-tt.tooltip-value"))
                    )
                    value = gdp_element.text.strip()
                    if year and value:
                        gdp_values[year] = value
                    print(f"Chỉ số: {index}, Năm: {year}, GDP: {value}")
                except Exception as e:
                    print(f"Lỗi khi lấy giá trị cho cột {index}: {e}")

            if gdp_values:
                print("Giá trị GDP:", gdp_values)
            else:
                print("Không lấy được giá trị GDP")

        # Lưu HTML để kiểm tra
        with open("page.html", "w", encoding="utf-8") as f:
            f.write(driver.page_source)
        print("HTML đã lưu vào page.html")

except Exception as e:
    print("Lỗi trong quá trình cào dữ liệu:", str(e))
    # Thử khởi động lại nếu cần (tùy chọn)
    try:
        driver.quit()
        driver = webdriver.Chrome(service=Service(chrome_driver_path), options=options)
        driver.get(url)
        print("Đã khởi động lại driver, thử lại sau 5 giây...")
        time.sleep(5)
    except Exception as e2:
        print("Không thể khởi động lại: ", str(e2))

finally:
    time.sleep(3)
    driver.quit()