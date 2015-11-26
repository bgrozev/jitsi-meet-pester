import random
import utils
import driver_factory


class PesterFixture:
    def __init__(self,
                 url_base="https://beta.meet.jit.si/",
                 browsers=('chrome', 'chrome'),
                 url=''):
        if url:
            self.url = url
        else:
            self.url = url_base + "pester" + str(random.random())[2:]

        self.drivers = []
        self.browsers = []
        for browser in browsers:
            self.browsers.append(browser)
            self.drivers.append(driver_factory.create_driver(browser))
        print('Creating a fixture; url=' + self.url + '; browsers=' +
              str(browsers))

    def get_owner(self):
        return self.drivers[0]

    def get_second_participant(self):
        return self.drivers[1]

    def connect_all(self):
        # ICE will not succeed until we start more than one driver
        for driver in self.drivers:
            driver.get(self.url)
        for driver in self.drivers:
            utils.wait_for_ice(driver)

    def connect(self, driver, url_fragment=''):
        url = self.url + '#' + url_fragment if url_fragment else self.url
        driver.get(url)
        utils.wait_for_ice(driver)

    def close_all(self):
        for driver in self.drivers:
            driver.quit()

    def close(self, driver):
        for i in range(len(self.drivers)):
            if driver == self.drivers[i]:
                self.drivers[i] = False
        driver.quit()

    def create_driver(self, idx):
        idx = idx - 1
        if self.drivers[idx]:
            print("Replacing driver at index " + str(idx))
            self.drivers[idx].quit()

        browser = self.browsers[idx] if idx < len(self.browsers) else 'chrome'

        self.drivers[idx] = driver_factory.create_driver(browser)
        return self.drivers[idx]




