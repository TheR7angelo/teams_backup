import base64
import os
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

from win32com.client import Dispatch


def driver_chrome():
    options = Options()
    options.add_experimental_option("prefs", {
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
    })

    user_data_dir = f"user-data-dir=C:\\Users\\{os.getlogin()}\\AppData\\Local\\Google\\Chrome\\User Data\\Default"

    options.add_argument(user_data_dir)
    # options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("start-maximized")
    options.add_argument("disable-infobars")
    options.add_argument("--disable-extensions")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    paths = [r"C:\Program Files\Google\Chrome\Application\chrome.exe",
             r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"]
    version = list(filter(None, [get_version_via_com(p) for p in paths]))[0][:2]

    path_chomedriver = f'chromedriver\\{version}\\chromedriver.exe'

    return webdriver.Chrome(executable_path=path_chomedriver, chrome_options=options)


def get_liste_conversation():
    driver = driver_chrome()

    lien = "https://teams.microsoft.com/"
    driver.get(lien)
    time.sleep(30)

    element = driver.find_element(By.XPATH, "//button[@id='app-bar-86fcd49b-61a2-4701-b771-54728cd291fb']")
    element.click()

    time.sleep(5)

    groupes = []
    while True:
        conversations = driver.find_elements(By.XPATH, "//div[@data-tab-area='recipient-group-list-item']")

        for conversation in conversations:
            personne = \
            conversation.get_attribute("innerText").replace(' ', '_').replace('-', '_').replace('(', '').replace(')',
                                                                                                                 '').replace(
                '+', 'plus_').split('\n')[0]
            groupes.append(personne)

        driver.execute_script('arguments[0].scrollIntoView(true);', conversations[-1])

    driver.quit()
    return groupes


def get_version_via_com(filename):
    parser = Dispatch("Scripting.FileSystemObject")
    try:
        version = parser.GetFileVersion(filename)
    except Exception:
        return None
    return version


def get_ext_from_byte(byte: bytes):
    byte = str(base64.b64encode(byte))

    if byte[2:12] == 'iVBORw0KGg':
        return 'png'
    elif byte[3:7] == '9j/4':
        return 'jpg'
    elif byte[2:6] == 'R0lG':
        return 'gif'
    elif byte[2:7] in ['SUkqA', 'TU0AK']:
        return 'tif'
    else:
        return 'txt'


def get_name_file(link: str):
    return link.split('/')[-1].split('.')[0]


def heur_mili(text: str):
    text = text.split('.')
    text[1] = text[1][:2]
    while len(text[1]) < 2:
        text[1] = f'{text[1]}0'
    text = '.'.join(text)

    return text


def getDownLoadedFileName(waitTime, driver):
    driver.execute_script("window.open()")
    # switch to new tab
    driver.switch_to.window(driver.window_handles[-1])
    # navigate to chrome downloads
    driver.get('chrome://downloads')
    # define the endTime
    endTime = time.time() + waitTime
    while True:
        try:
            # get downloaded percentage
            downloadPercentage = driver.execute_script(
                "return document.querySelector('downloads-manager').shadowRoot.querySelector('#downloadsList downloads-item').shadowRoot.querySelector('#progress').value")
            # check if downloadPercentage is 100 (otherwise the script will keep waiting)
            if downloadPercentage == 100:
                # return the file name once the download is completed
                return driver.execute_script(
                    "return document.querySelector('downloads-manager').shadowRoot.querySelector('#downloadsList downloads-item').shadowRoot.querySelector('div#content  #file-link').text")
        except:
            pass
        time.sleep(1)

        print()
        if time.time() > endTime:
            break


def get_link_share(driver):
    driver.switch_to.default_content()
    driver.switch_to.frame(
        driver.find_element(By.XPATH, "//iframe[@name='shareFrame']]"))

    element = driver.find_element(By.XPATH, '//input')
    src = element.get_attribute('src')

    return src
