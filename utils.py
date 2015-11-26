from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait

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

def change_display_name(driver, name):
    driver.find_element_by_xpath(
        "//span[@id='localVideoContainer']/a[@class='displayname']").click()
    input_elem = driver.find_element_by_xpath(
        "//span[@id='localVideoContainer']/input[@class='displayname']")
    ActionChains(driver).move_to_element(input_elem).perform()
    input_elem.send_keys(name)
    input_elem.send_keys(Keys.RETURN)

def get_local_resource_jid(driver):
    return driver.execute_script("return APP.xmpp.myResource();")
