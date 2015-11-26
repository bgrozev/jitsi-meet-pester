import random
import utils
import driver_factory


class PesterFixture:
    def __init__(self,
                 url_base="https://beta.meet.jit.si/",
                 browsers=('chrome', 'chrome'),
                 url=''):
        self.drivers = []
        for browser in browsers:
            self.drivers.append(driver_factory.create_driver(browser))

        if url:
            self.url = url
        else:
            self.url = url_base + str(random.random())[2:]
        print('Creating a fixture; url=' + self.url + '; browsers=' +
              str(browsers))

    def get_owner(self):
        return self.drivers[0]

    def get_second_participant(self):
        return self.drivers[1]

    def connect_all(self):
        for driver in self.drivers:
            driver.get(self.url)
        for driver in self.drivers:
            utils.wait_for_ice(driver)

    def quit_all(self):
        for driver in self.drivers:
            driver.quit()

