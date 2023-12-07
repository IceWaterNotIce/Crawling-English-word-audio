# Description: This program is used to download the audio of words from the Cambridge Dictionary website.
#            The words are read from the words.txt file.
# 


import requests
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Read words form words.txt
file_path = 'words.txt'
with open(file_path, 'r') as file:
    string_list = file.readlines()
# Remove newline characters from each line
searchwords = [line.strip() for line in string_list]

# Create a new instance of the Chrome driver
options = webdriver.ChromeOptions()
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)
wait = WebDriverWait(driver, 10)

for searchword in searchwords:

    # Navigate to the website
    driver.get("https://dictionary.cambridge.org/zht/%E8%A9%9E%E5%85%B8/%E8%8B%B1%E8%AA%9E-%E6%BC%A2%E8%AA%9E-%E7%B9%81%E9%AB%94/")

    # Wait 30s for the audio element to be loaded
    wait = WebDriverWait(driver, 30)

    # Enter the word
    Input_searchword = wait.until(EC.presence_of_element_located((By.ID, "searchword")))
    Input_searchword.send_keys(searchword)
    Input_searchword.submit()

    # Get url to dowland the audio of word
    audio_searchword = wait.until(EC.presence_of_element_located((By.ID, "audio1")))
    source_searchword = audio_searchword.find_elements(By.TAG_NAME, "source")[0]
    # Get the value of the "src" attribute of the source element
    audio_source_url = source_searchword.get_attribute("src")

    # Download audio
    DownlandFile_path = os.path.join(os.getcwd(), 'Audio')
    file_name = driver.find_element(By.XPATH, '//*[@id="page-content"]/div[2]/div[4]/div/div/div/div[2]/div[1]/span/span').text + ".mp3"
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                            'Chrome/51.0.2704.63 Safari/537.36', 'Accept-Language':'zh-CN,zh;q=0.9'}
    response = requests.get(url=audio_source_url, headers=headers)

    # write the contents of the response to a file
    with open(f"{DownlandFile_path}\{file_name}", "wb") as f:
        f.write(response.content)
    # print a message indicating that the file has been downloaded
    print(f"File downloaded to {DownlandFile_path}\{DownlandFile_path}")


# Close the browser window
driver.quit()