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
import traceback

# Print versions for debugging
print("Selenium version:", webdriver.__version__)
chrome_driver_path = ChromeDriverManager().install()
result = subprocess.run([chrome_driver_path, "--version"], capture_output=True, text=True)
print("ChromeDriver version:", result.stdout.strip())

# Selenium optimization
options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("useAutomationExtension", False)
ua = UserAgent()
options.add_argument(f"user-agent={ua.random}")
options.add_argument("--proxy-server=http://193.151.141.17:8080")  # Proxy hiện tại
options.add_argument("user-data-dir=C:\\Users\\laptop\\AppData\\Local\\Google\\Chrome\\User Data\\Default")  # Cập nhật theo tên user của bạn
options.add_argument("--window-size=1920,1080")
options.add_argument("--start-maximized")

# Initialize driver
driver = webdriver.Chrome(service=Service(chrome_driver_path), options=options)

# Apply selenium-stealth
stealth(driver,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True)

# Hide navigator.webdriver
driver.execute_cdp_cmd(
    'Page.addScriptToEvaluateOnNewDocument',
    {'source': 'Object.defineProperty(navigator, "webdriver", {get: () => undefined})'}
)

# Scrape data
url = "https://tradingeconomics.com/vietnam/gdp"
try:
    driver.get(url)
    time.sleep(3)  # Giảm từ 5 xuống 3 giây chờ trang tải

    # Mô phỏng hành vi người dùng
    actions = ActionChains(driver)
    actions.move_by_offset(random.randint(50, 200), random.randint(50, 200)).click().perform()
    time.sleep(random.uniform(1, 2))  # Giảm từ 2-5 xuống 1-2 giây
    # Cuộn đến biểu đồ
    chart_container = driver.find_element(By.CLASS_NAME, "highcharts-container")
    driver.execute_script("arguments[0].scrollIntoView({ behavior: 'smooth', block: 'center' });", chart_container)
    time.sleep(1)  # Giảm từ 2-5 xuống 1 giây

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
                # Di chuột ra khỏi biểu đồ để tắt tooltip cũ
                actions.move_by_offset(0, -100).perform()
                time.sleep(0.5)  # Chờ tooltip cũ biến mất
                # Di chuyển chuột đến cột mới
                actions.move_to_element(bar).perform()
                time.sleep(1.5)  # Tăng từ 2 xuống 1.5 giây để xử lý 2014
                try:
                    # Tìm phần tử tooltip-box
                    tooltip_box = WebDriverWait(driver, 5).until(
                        EC.presence_of_element_located((By.CLASS_NAME, "tooltip-box"))
                    )
                    # Lấy năm từ <span class="tooltip-date">
                    date_element = WebDriverWait(tooltip_box, 5).until(
                        EC.presence_of_element_located((By.CLASS_NAME, "tooltip-date"))
                    )
                    year = date_element.text.strip()
                    # Sửa class cho hawk-tt.tooltip-value (loại bỏ khoảng trống)
                    gdp_element = WebDriverWait(tooltip_box, 5).until(
                        EC.presence_of_element_located((By.CLASS_NAME, "hawk-tt.tooltip-value"))
                    )
                    value = gdp_element.text.strip()
                    if year and value:
                        gdp_values[year] = value
                    print(f"Chỉ số: {index}, Năm: {year}, GDP: {value}")
                except Exception as e:
                    print(f"Lỗi khi lấy giá trị cho cột {index}: {type(e).__name__} - Chi tiết: {str(e)}")
                    print(f"Stack trace: {traceback.format_exc()}")

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

finally:
    time.sleep(2)  # Giảm từ 3 xuống 2 giây
    driver.quit()