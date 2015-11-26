from numbers import Number
from nose.tools import *
from selenium.common.exceptions import TimeoutException
import pester
import time
import utils

# The fragment which will be added to the URL in order to disable UDP.
DISABLE_UDP_URL_FRAGMENT = "config.webrtcIceUdpDisable=true"

fixture = pester.fixture

# This is how we order the tests in a file, if we need to.
@nottest
def get_tests():
    return [test_udp, test_single_port, test_tcp]


# Checks if the two participants are connected via UDP.
def test_udp():
    time.sleep(5)

    assert_equals("udp", get_protocol(fixture.get_owner()),
                  "The owner must be connected through UDP.")
    assert_equals("udp", get_protocol(fixture.get_second_participant()),
                  "The second participant must be connected through UDP.")


# Checks if the two participants are connected via the same UDP port.
def test_single_port():
    owner = fixture.get_owner()
    second_participant = fixture.get_second_participant()

    owner_port = get_remote_port(owner)
    second_participant_port = get_remote_port(second_participant)

    assert_is_instance(owner_port, Number), "The owner's port must be a number."
    assert_is_instance(second_participant_port, Number,
                       "The second participant's port must be a number.")

    assert_equals(owner_port, second_participant_port,
                  "The two participants must use the same port.")


# Brings the conference to the default state after test_tcp has run.
def tear_down_tcp():
    fixture.close(fixture.get_second_participant())
    second_participant = fixture.create_driver(2)
    fixture.connect(second_participant)
    utils.wait_for_send_receive_data(second_participant)


# Checks if the connection will use TCP if we specifically disable UDP.
@with_setup(utils.noop, tear_down_tcp)
def test_tcp():
    # TODO disable TCP on firefox
    fixture.close(fixture.get_second_participant())
    second_participant = fixture.create_driver(2)

    try:
        fixture.connect(second_participant, DISABLE_UDP_URL_FRAGMENT)
        utils.wait_for_send_receive_data(second_participant, 20)
        timeout = False
    except TimeoutException:
        timeout = True

    if timeout:
        assert False, "The second participant must have connected."

    assert_equals("tcp", get_protocol(second_participant),
                  "The second participant must be connected through TCP.")


# Returns the transport protocol used by the media connection in the Jitsi-Meet
# conference running in 'driver', or an error string on failure.
def get_protocol(driver):
    return driver.execute_script('''
    try {
        return APP.connectionquality.getStats().transport[0].type.toLowerCase();
    } catch (err) {
        return 'error: ' + err;
    }''')


# Returns the remote port number used by the media connection in the Jitsi-Meet
# conference running in 'driver' as a number, or an error string on failure.
def get_remote_port(driver):
    return driver.execute_script('''
        try {
            var transport = APP.connectionquality.getStats().transport[0];
            var port = transport.ip.split(':')[1];
            return Number(port);
        } catch (err) {
            return 'error: ' + err;
        }''')
