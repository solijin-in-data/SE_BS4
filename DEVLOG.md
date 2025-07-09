# 📘 Dev Log: SE_BS4 

---

## 🧪 Version 0.1

**🔧 Thư viện sử dụng:**
- `selenium.webdriver`: Điều khiển trình duyệt Chrome
- `By`: Tìm phần tử trong DOM
- `Service`: Quản lý ChromeDriver
- `ActionChains`: Mô phỏng thao tác người dùng
- `webdriver_manager.chrome`: Tự động tải ChromeDriver
- `BeautifulSoup`: Phân tích HTML
- `time`, `random`: Quản lý thời gian chờ và tạo hành vi ngẫu nhiên

**⚙️ Thiết lập Driver:**
- Vô hiệu hóa Automation Extension
- Giả lập User-Agent và User Data
- Tắt proxy
- Chạy headless (headless=new)
- Tắt Blink features & navigator.webdriver

**📋 Quy trình:**
- Di chuyển chuột, cuộn trang và chờ
- Trích xuất HTML qua BeautifulSoup
- Tìm `span` với class `datatable-bold`

**❌ Kết quả:**  
- Bị ngắt đột ngột  
- Không tìm thấy dữ liệu GDP

**🧩 Vấn đề:**  
- Thiếu kiểm tra trạng thái truy cập → Có thể đã bị bot detection

---

## 🔁 Version 0.1.1 → 0.1.7

### Các cải tiến chính:
- Thêm xử lý **403 / Access Denied**
- Sử dụng `WebDriverWait`, `expected_conditions`, `NoSuchElementException`
- Fake User-Agent, Selenium Stealth
- Hover bar chart để trigger tooltip (GDP)
- Trích xuất tooltip `tooltip-box` → `tooltip-date`, `tooltip-value`

**⛔ Vấn đề:**  
- Website chặn bot → `DEPRECATED_ENDPOINT`
- Tooltip che khuất bar → Sai số dữ liệu

---

## 🛠 Version 0.1.8 → 0.1.13

### Tối ưu:
- Thêm `proxy` thay thế
- Hover offset để tắt tooltip cũ
- Tăng / giảm sleep hợp lý
- Sửa selector `.hawk-tt.tooltip-value`
- Thêm `traceback` và `readyState` check

**Kết quả:**  
- Lấy được **1 vài dữ liệu**, nhưng browser crash hoặc Timeout ở các bar khác  
- Vẫn lỗi `DEPRECATED_ENDPOINT`

---

## 🚀 Version 0.2 - Hoàn thiện

**Tối ưu cuối:**
- Cập nhật `user-data-dir` theo máy thật
- Giảm delay thời gian không cần thiết
- Tăng độ chính xác của hover + delay tooltip (1.5s)
- Sửa lỗi `.hawk-tt tooltip-value` → `.hawk-tt.tooltip-value`
- Hoàn thiện hệ thống báo lỗi (traceback)

**✅ Kết quả:**
- Truy cập thành công
- Lấy **toàn bộ dữ liệu GDP**
- **Lỗi DEPRECATED_ENDPOINT vẫn còn**, nhưng không ảnh hưởng tới kết quả chính

---

## 🛠 Version 0.2.1

## Tối ưu:
- Thêm chức năng `thay đổi proxy` cho mỗi lần chạy chương trình 
- Thêm `tùy chọn người dùng` trên cmd

**⛔ Vấn đề:**
- Load website bị ảnh hưởng bởi kết nối internet 

---
