

# BÀI 1: GIỚI THIỆU API VÀ WEB SERVICES
# File: api_demo.py
# Chạy bằng: python api_demo.py

import requests
import json

print("=== DEMO 3 API CƠ BẢN ===\n")

# 1. GITHUB API - Lấy thông tin user
print("1. GITHUB API:")
github_url = "https://api.github.com/users/torvalds"
response = requests.get(github_url)
data = response.json()
print(f"User: {data['login']}")
print(f"Repo công khai: {data['public_repos']}")
print(f"Followers: {data['followers']}\n")

# 2. OPENWEATHER API - Thời tiết TP.HCM (cần API key miễn phí)
print("2. OPENWEATHER API:")
# Đăng ký free key tại: https://openweathermap.org/api
# weather_url = "https://api.openweathermap.org/data/2.5/weather?q=HoChiMinhCity&appid=YOUR_API_KEY&units=metric"
# response = requests.get(weather_url)
# if response.status_code == 200:
#     data = response.json()
#     print(f"Nhiệt độ TP.HCM: {data['main']['temp']}°C")
#     print(f"Mô tả: {data['weather'][0]['description']}")
print("→ Uncomment và thay YOUR_API_KEY để test!\n")

# 3. COINGECKO API - Giá Bitcoin
print("3. COINGECKO API:")
coingecko_url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"
response = requests.get(coingecko_url)
data = response.json()
btc_price = data['bitcoin']['usd']
print(f"Giá Bitcoin: ${btc_price:,}\n")

# BONUS: Tìm repo Python phổ biến
print("BONUS - Tìm repo Python:")
search_url = "https://api.github.com/search/repositories?q=language:python&sort=stars&per_page=3"
response = requests.get(search_url)
repos = response.json()['items']
for repo in repos:
    print(f"- {repo['full_name']}: {repo['stargazers_count']} ⭐")

print("\n=== HOÀN THÀNH! ===")