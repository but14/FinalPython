from selenium import webdriver
from selenium.webdriver.common.by import By
from pymongo import MongoClient
import re
import time

# MongoDB setup
client = MongoClient("mongodb://localhost:27017/")
db = client['mario']
collection = db['leaderboard']

# Selenium setup
driver = webdriver.Chrome()  # Ensure ChromeDriver is installed
driver.get("https://gamevui.vn/scores/super-mario-run-online/game")
time.sleep(5)  # Wait for JavaScript to load content

players = []
items = driver.find_elements(By.CLASS_NAME, "clearfix")

for item in items:
    try:
        # Try to locate the username and score elements
        name_element = item.find_element(By.CLASS_NAME, "username")
        score_element = item.find_element(By.CLASS_NAME, "score")
        
        # Extract name
        name = name_element.get_attribute("title")
        
        # Extract score, remove non-numeric characters, and convert to integer
        score_text = score_element.text
        score = int(re.sub(r'\D', '', score_text))  # Remove any non-digit characters

        # Add player data to list
        players.append({"name": name, "score": score})
        
        # Debug print to confirm extraction
        print(f"Name: {name}, Score: {score}")
        
    except Exception as e:
        # Print error message if element is not found or parsing fails
        print("Error extracting data:", e)

# Insert data into MongoDB if players were found
if players:
    collection.insert_many(players)
    print("Data inserted into MongoDB!")
else:
    print("No data found to insert.")

driver.quit()
