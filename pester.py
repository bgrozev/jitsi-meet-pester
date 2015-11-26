from inspect import getmembers, isfunction
from testconfig import config
from fixture import PesterFixture

tests_to_run = ["test_tcp", "test_display_name"]
current_fixture = False


def setup_module():
    print("setup_module")
    browsers = ['chrome', 'chrome']
    print(config)
    if 'browser1' in config:
        browsers[0] = config['browser1']
    if 'browser2' in config:
        browsers[1] = config['browser2']

    global current_fixture
    current_fixture = PesterFixture(browsers=browsers)
    current_fixture.connect_all()


def teardown_module():
    current_fixture.quit_all()


def test_generate_tests():
    import importlib

    for module_name in tests_to_run:
        module = importlib.import_module(module_name)
        if hasattr(module, 'get_tests'):
            functions = module.get_tests()
            test_generate_tests.compat_func_name = module_name
            for test in functions:
                yield test
        else:
            functions = [o for o in getmembers(module) if
                         isfunction(o[1]) and o[0].startswith('test')]
            for test in functions:
                test_generate_tests.compat_func_name = module_name + ': ' + test[0]
                yield test[1]
