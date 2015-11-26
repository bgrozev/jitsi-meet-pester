import random
from selenium.webdriver import ActionChains
from pester import fixture
import utils


def check_display_name_locally(name):
    second_participant = fixture.get_second_participant()
    display_name_elem = second_participant.find_element_by_xpath(
        "//span[@id='localVideoContainer']/span[@id='localDisplayName']")
    local_video_container_elem = second_participant.find_element_by_xpath(
        "//span[@id='localVideoContainer']")
    ActionChains(second_participant).move_to_element(
        local_video_container_elem).perform()

    assert display_name_elem.is_displayed(),\
        'The display name must be displayed.'
    assert name in display_name_elem.text,\
        'The display name text must contain ' + name + '.'

def check_display_name_on_remote_side(name):
    owner = fixture.get_owner()

    second_participant_resource_jid = utils.get_local_resource_jid(
        fixture.get_second_participant())
    remote_video_span = owner.find_element_by_xpath(
        "//span[@id='participant_" + second_participant_resource_jid + "']")

    remote_video_span.click()
    ActionChains(owner).move_to_element(remote_video_span).perform()

    display_name_elem = owner.find_element_by_xpath(
        "//span[@id='participant_" + second_participant_resource_jid +
        "']/span[@id='participant_" + second_participant_resource_jid +
        "_name']")

    assert display_name_elem.is_displayed(),\
        'The remote display name must be displayed.'
    assert name in display_name_elem.text,\
        'The remote display name text must contain ' + name + '.'

def test_display_name():
    name = 'Name' + str(random.random())[2:]
    print('test_display_name: changing display name to ' + name)
    utils.change_display_name(fixture.get_second_participant(), name)
    check_display_name_locally(name)
    check_display_name_on_remote_side(name)
