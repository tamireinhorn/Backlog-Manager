from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
from selenium import webdriver




URL = "https://backloggery.com/games.php?user=belugabaleia&search=&rating=&status=&own=0&region=&wish=0&alpha="
driver = webdriver.Chrome()
driver.get(URL)
timeout = 5
try:
    element_present = EC.presence_of_element_located((By.CSS_SELECTOR, '.gamebox'))
    WebDriverWait(driver, timeout).until(element_present)
except TimeoutException:
    raise TimeoutException('The page took too long to display the games.')
soup = BeautifulSoup(driver.page_source, 'html.parser')
# Find all elements with the "gamebox" class that do not have any other subclasses 
games = soup.select('.gamebox:not([class*=" "])')
games_list = []
for game in games:
    game_status = game.img['src'].split('/')[1].split('.')[0] # Parse the image name and get a status
    game_name = game.b.text
    game_console = game.div.b.text.lstrip().split()[0] # Parse the console abbreviation and get the console for the game.
    videogame = {'title': game_name, 'console': game_console, 'status': game_status}
    games_list.append(videogame)
print('Yeah I did the parsing')