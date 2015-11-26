from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

ICE_CONNECTED_CHECK_JS = '''
try {
    var jingle = APP.xmpp.getConnection().jingle.activecall;
    if (jingle.peerconnection.iceConnectionState === 'connected')
        return true;
} catch (err) {
    return false;
}'''


def wait_for_boolean(driver, script, timeout=10):
    WebDriverWait(driver, timeout).until(lambda d: d.execute_script(script))


def wait_for_ice(driver):
    wait_for_boolean(driver, ICE_CONNECTED_CHECK_JS)

def noop():
    pass

def change_display_name(driver, name):
    driver.find_element_by_xpath(
        "//span[@id='localVideoContainer']/a[@class='displayname']").click()
    input_elem = driver.find_element_by_xpath(
        "//span[@id='localVideoContainer']/input[@class='displayname']")
    ActionChains(driver).move_to_element(input_elem).perform()
    input_elem.send_keys(name)
    input_elem.send_keys(Keys.RETURN)

def wait_for_send_receive_data(driver, timeout=5):
    def got_data(ignore):
        stats = driver.execute_script(
            "return APP.connectionquality.getStats();")

        if not stats or not stats['bitrate']:
            return False
        download = stats['bitrate']['download'] if stats['bitrate']['download'] else -1
        upload = stats['bitrate']['upload'] if stats['bitrate']['upload'] else -1

        return download > 0 and upload > 0

    WebDriverWait(driver, timeout).until(got_data)

def get_local_resource_jid(driver):
    return driver.execute_script("return APP.xmpp.myResource();")


def click_on_element_by_id(driver, id):
    driver.find_element_by_xpath("//a[@id='" + id + "']").click()


def wait_for_element_by_xpath(driver, xpath, timeout=5):
    WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((By.XPATH, xpath)))

def wait_for_element_not_present_by_xpath(driver, xpath, timeout=5):
    WebDriverWait(driver, timeout).until(
        lambda d: len(d.find_elements_by_xpath(xpath)) == 0)
