from nose import with_setup
from pester import current_fixture
import utils

DISABLE_UDP_URL_FRAGMENT = "config.webrtcIceUdpDisable=true"
#TODO disable on firefox

#TODO: remove
def noop():
    pass

# Brings the conference to the default state before.
def tear_down_tcp():
    current_fixture.close(current_fixture.get_second_participant())
    second_participant = current_fixture.create_driver(2)
    current_fixture.connect(second_participant)
    utils.wait_for_send_receive_data(second_participant)

@with_setup(noop, tear_down_tcp)
def test_tcp():
    current_fixture.close(current_fixture.get_second_participant())
    second_participant = current_fixture.create_driver(2)
    current_fixture.connect(second_participant, DISABLE_UDP_URL_FRAGMENT)
    utils.wait_for_send_receive_data(second_participant, 20)

    assert "tcp" == get_protocol(second_participant),\
        "We must be connected through TCP"



# Returns the transport protocol used by the media connection in the Jitsi-Meet
# conference running in <tt>driver</tt>, or an error string (beginning with
# "error:") or null on failure.
def get_protocol(driver):
    protocol = driver.execute_script('''
    try {
        return APP.connectionquality.getStats().transport[0].type;
    } catch (err) {
        return 'error: '+err;
    }''')

    return str(protocol)
