from selenium import webdriver
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument('--use-fake-ui-for-media-stream')

def create_driver(browser='chrome'):
    if browser == 'chrome':
        return webdriver.Chrome(chrome_options=chrome_options)
    elif browser == 'firefox':
        #just testing...
        return webdriver.Chrome(chrome_options=chrome_options)
    else:
        print("Unsupported browser: " + browser)

