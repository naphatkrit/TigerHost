def pytest_addoption(parser):
    parser.addoption('--deis-url', action='store',
                     default=None, help="URL for the local deis instance.")
