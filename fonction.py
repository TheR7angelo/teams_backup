import base64
import time

from selenium.webdriver.common.by import By


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
