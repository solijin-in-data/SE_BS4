from bs4 import BeautifulSoup
import requests

def get_https_proxy():
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"}
    
    html = "https://free-proxy-list.net/"
    response = requests.get(html, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')

    tbody = soup.find(class_ = "table table-striped table-bordered")
    rows = tbody.find_all('tr')

    for row in rows:
        cols = [col.text.strip() for col in row.find_all("td")]
        if len(cols) >= 7 and cols[6].lower() == "yes":  # cols[6] = HTTPS
            ip = cols[0]
            port = cols[1]
            return f"Found HTTPS proxy: {ip}:{port}"
    return None

