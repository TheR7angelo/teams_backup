import datetime
import json

import os
import threading
import time
import base64
import sqlite3

import selenium.webdriver
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException

from win32com.client import Dispatch

# dead line 30 juin 2022

def get_version_via_com(filename):
    parser = Dispatch("Scripting.FileSystemObject")
    try:
        version = parser.GetFileVersion(filename)
    except Exception:
        return None
    return version


def get_file_content_chrome(driver, uri):
    result = driver.execute_async_script("""
    var uri = arguments[0];
    var callback = arguments[1];
    var toBase64 = function(buffer){for(var r,n=new Uint8Array(buffer),t=n.length,a=new Uint8Array(4*Math.ceil(t/3)),i=new Uint8Array(64),o=0,c=0;64>c;++c)i[c]="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/".charCodeAt(c);for(c=0;t-t%3>c;c+=3,o+=4)r=n[c]<<16|n[c+1]<<8|n[c+2],a[o]=i[r>>18],a[o+1]=i[r>>12&63],a[o+2]=i[r>>6&63],a[o+3]=i[63&r];return t%3===1?(r=n[t-1],a[o]=i[r>>2],a[o+1]=i[r<<4&63],a[o+2]=61,a[o+3]=61):t%3===2&&(r=(n[t-2]<<8)+n[t-1],a[o]=i[r>>10],a[o+1]=i[r>>4&63],a[o+2]=i[r<<2&63],a[o+3]=61),new TextDecoder("ascii").decode(a)};
    var xhr = new XMLHttpRequest();
    xhr.responseType = 'arraybuffer';
    xhr.onload = function(){ callback(toBase64(xhr.response)) };
    xhr.onerror = function(){ callback(xhr.status) };
    xhr.open('GET', uri);
    xhr.send();
    """, uri)
    if type(result) == int:
        raise Exception("Request failed with status %s" % result)
    return base64.b64decode(result)


# def save_message(driver, personne):
#
#     with sqlite3.connect('bdd.db') as conn:
#         cursor = conn.cursor()
#
#         cursor.execute(f'''
#                         CREATE TABLE IF NOT EXISTS "{personne}"
#                         (id INTERGER PRIMARY KEY, message TEXT, image_path TEXT ,image TEXT ,heur TEXT)
#                         ''')
#         driver.switch_to.frame(
#             driver.find_element(By.XPATH, "//iframe[@class='embedded-electron-webview embedded-page-content']"))
#         messages = driver.find_elements(By.XPATH, Xpath)
#         for message in messages:
#
#             date = message.find_element(By.XPATH,
#                                         "//div[@class='ui-chat__messageheader']//time[@dir='auto']")
#             message = message.find_element(By.XPATH, "//div[@dir='auto']//p")
#
#             date = date.get_attribute("datetime")
#             date = datetime.datetime.strptime(date, '%Y-%m-%dT%H:%M:%S.%f0Z')
#             date = date + datetime.timedelta(hours=1)
#
#             id = int(date.strftime('%Y%m%d%H%M%S%f'))
#             try:
#                 txt = message.get_attribute("innerText")
#             except:
#                 txt = ''
#             image = ''
#             heur = date.strftime('%Y-%m-%d_%H-%M-%S')
#             image_path = ''
#
#             command = f'''
#                     INSERT or REPLACE INTO '{personne}' (id, message, image_path, image, heur) values
#                     ({id}, "{txt}", "{image_path}", "{image}", "{heur}")
#                     '''
#             cursor.execute(command)
#             conn.commit()
#
#         print('hey')


def remonte_max(driver, personne):

    def heur_mili(text: str):
        text = text.split('.')
        text[1] = text[1][:1]
        text = '.'.join(text)
        return text

    driver.switch_to.frame(
        driver.find_element(By.XPATH, "//iframe[@class='embedded-electron-webview embedded-page-content']"))

    time.sleep(5)

    print('go')

    Xpath = "//ul[@aria-label='Contenu de la conversation']//li[@data-tid='chat-pane-item']//p" #[@data-tid='chat-pane-item']"

    break_point = 0
    loop = 1
    elements = driver.find_elements(By.XPATH, Xpath)

    emojy = {'like': '👍',
             'heart': '❤',
             'laugh': '😀',
             'surprised': '😯',
             'sad': '😢',
             'angryface': '😠'
             }

    while True:

        for message in elements:
            date = message.find_element(By.XPATH,
                                        "./parent::div/parent::div/parent::div//div[@class='ui-chat__messageheader']//time[@dir='auto']")

            # date = date.get_attribute("datetime").split('.')
            # date[1] = date[1][:1]
            # date = '.'.join(date)
            # date = datetime.datetime.strptime(date, '%Y-%m-%dT%H:%M:%S.%f')
            # date = date + datetime.timedelta(hours=1)

            date = heur_mili(date.get_attribute("datetime"))
            date = datetime.datetime.strptime(date, '%Y-%m-%dT%H:%M:%S.%f') + datetime.timedelta(hours=1)

            id = int(date.strftime('%Y%m%d%H%M%S%f'))

            expediteur = message.find_element(By.XPATH,
                                        "./parent::div/parent::div/parent::div//div[@class='ui-chat__messageheader']//span[@dir='auto']")
            expediteur = expediteur.get_attribute("innerText")

            try:
                # txt = message.find_element(By.XPATH, "//div[@dir='auto']//p")
                txt = message.get_attribute("innerText")
            except:
                txt = ''

            # if txt == 'aie aie aie':
            #     print('h')

            reaction = []
            reactions = message.find_elements(By.XPATH,
                                    "./parent::div/parent::div/parent::div//div[@class='ui-chat__messageheader']//div[starts-with(@class, 'ui-reactions')]//span[starts-with(@class, 'ui-text')]")
            for react in reactions:

                # attrs = []
                # for attr in react.get_property('attributes'):
                #     attrs.append([attr['name'], attr['value']])

                tmp = [react.get_attribute('title'), react.get_attribute('data-tid').split('-')[0]]

                tmp[1] = emojy[tmp[1]]
                tmp = '*'.join(tmp)
                reaction.append(tmp[:])
                del tmp
            reaction = ';'.join(reaction)

            image = ''


            # heur = date.strftime('%d-%m-%Y_%H:%M:%S.%f').split('.')
            # heur[1] = heur[1][:1]
            # heur = '.'.join(heur)

            heur = heur_mili(date.strftime('%d-%m-%Y_%H:%M:%S.%f'))

            image_path = r'imgTeams'

            with sqlite3.connect('bdd.db') as conn:
                cursor = conn.cursor()

                cursor.execute(f'''
                                CREATE TABLE IF NOT EXISTS "{personne}"
                                (id REAL PRIMARY KEY, expediteur TEXT, message TEXT, reaction TEXT, image_path TEXT, image TEXT, heur TEXT)
                                ''')
                conn.commit()

                command = f'''
                        INSERT or REPLACE INTO '{personne}' (id, expediteur, message, reaction, image_path, image, heur) values
                        ({id}, "{expediteur}", "{txt}", "{reaction}", "{image_path}", "{image}", "{heur}")
                        '''
                cursor.execute(command)
                conn.commit()

        element = elements[0]

        try:
            driver.execute_script('arguments[0].scrollIntoView(true);', element)
        except StaleElementReferenceException:
            pass
        new_elements = driver.find_elements(By.XPATH, Xpath)
        new_element = new_elements[0]

        if element == new_element:
            break_point += 1
            # time.sleep(0.2)
        else:
            break_point = 0
            elements = new_elements

        print('break_point:', break_point)
        print('loop:', loop)
        loop += 1

        if break_point >= 75:
            break

    return None


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

driver = webdriver.Chrome(
    executable_path=path_chomedriver,
    chrome_options=options)

executor_url = driver.command_executor._url
session_id = driver.session_id

lien = "https://teams.microsoft.com/"
driver.get(lien)
time.sleep(30)

element = driver.find_element(By.XPATH, "//button[@id='app-bar-86fcd49b-61a2-4701-b771-54728cd291fb']")
element.click()

time.sleep(5)

# element = driver.find_elements_by_xpath("//div[@data-tab-area='recipient-group-list-item']")
conversations = driver.find_elements(By.XPATH, "//div[@data-tab-area='recipient-group-list-item']")

for conversation in conversations:
    conversation.click()
    time.sleep(2)
    personne = conversation.get_attribute("innerText").split(' (')[0].replace(' ', '_')
    print(personne)

    # messages = driver.find_elements(By.XPATH, "//ul[@aria-label='Contenu de la conversation']/li[@data-tid='chat-pane-item']//p")
    # Xpath = "//ul[@aria-label='Contenu de la conversation']/li[@data-tid='chat-pane-item']"
    messages = remonte_max(
        driver=driver, personne=personne)  # "//ul[@aria-label='Contenu de la conversation']/li[@data-tid='chat-pane-item//p']"
    # save_message(driver=driver, personne=personne)

    # for index, message in enumerate(messages):
    #
    #     try:
    #         txt = message.get_attribute("innerText")
    #     except:
    #         txt = ''
    #
    #     src = message.find_elements(By.XPATH, './/img')
    #     if len(src) > 0:
    #         src = src[0]
    #         src = src.get_attribute("src")
    #         bytes = get_file_content_chrome(driver, src)
    #         nom_fichier = src.split("/")[-1].replace('.png', '')
    #         os.makedirs('imgTeams', exist_ok=True)
    #         with open(f'imgTeams\\{nom_fichier}.png', 'wb') as outfile:
    #             outfile.write(bytes)
    #
    #     title = message.get_attribute("title")
    #
    #     print(txt)
    #     print(title)
    #     print(src)
    #
    #     date = message.find_element(By.XPATH,
    #                                 "./parent::div/parent::div/parent::div//div[@class='ui-chat__messageheader']//time[@dir='auto']")
    #     date = date.get_attribute("datetime")
    #     date = datetime.datetime.strptime(date, '%Y-%m-%dT%H:%M:%S.%f0Z')
    #
    #     date = date + datetime.timedelta(hours=1)
    #
    #     print(index)

"""
scroll vers le bas :
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

scroll vers le haut :
driver.execute_script("window.scrollTo(0, document.body.scrollBottom);")

boucle sur elements avec xpatj
elem = driver.find_elements_by_xpath("//div[@class='']/img")
for items in elem:
    src = items.get_attribute('src')
    lst.add(src)

click
element = driver.find_element(By.XPATH, "//button[@class='']")
    element.click()

touche
elem.send_keys(Keys.RETURN)
"""


def FUNC():
    pass


TH = threading.Thread(target=FUNC)
TH.start()
