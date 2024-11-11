import requests
from bs4 import BeautifulSoup

url = "https://gamevui.vn/scores/super-mario-run-online/game#google_vignette"  # Thay bằng URL thực tế
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

# Tìm tất cả các hàng của bảng
rows = soup.find_all("tr")  # Cần điều chỉnh selector để chọn đúng phần tử

data = []
for row in rows[1:]:  
    cells = row.find_all("td")
    if len(cells) >= 4:  
        rank = cells[0].text.strip()
        level = cells[1].text.strip()
        username = cells[2].text.strip()
        score = cells[3].text.strip()

        data.append({
            "rank": rank,
            "level": level,
            "username": username,
            "score": score
        })

print(data)
