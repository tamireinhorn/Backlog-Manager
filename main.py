from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
import bs4
import time
import hashlib
from selenium import webdriver


def process_game(game: bs4.element.Tag):

    game_status = game.img['src'].split('/')[1].split('.')[0] # Parse the image name and get a status
    if game_status == 'compilation':
        return 
    game_name = game.b.text
    game_console = game.div.b.text.lstrip().split()[0] # Parse the console abbreviation and get the console for the game.
    videogame = {'title': game_name, 'console': game_console, 'status': game_status}
    return videogame


URL = "https://backloggery.com/games.php?user=belugabaleia&search=&rating=&status=&own=0&region=&wish=0&alpha="
driver = webdriver.Chrome()
driver.get(URL)
timeout = 5
try:
    element_present = EC.presence_of_element_located((By.CSS_SELECTOR, '.gamebox'))
    WebDriverWait(driver, timeout).until(element_present)
except TimeoutException:
    raise TimeoutException('The page took too long to display the games.')
buttons = driver.find_elements(By.CSS_SELECTOR, '.lessmore') # Find the buttons to expand everything that is needed.
for button in buttons:
    time.sleep(2)
    button.click()
soup = BeautifulSoup(driver.page_source, 'html.parser')
# Find all elements with the "gamebox" class that do not have any other subclasses 
games = soup.select('.gamebox:not([class*=" "])')
games_list = []
for game in games:
    videogame = process_game(game)
    if videogame:
        games_list.append(videogame)
print('Yeah I did the parsing')