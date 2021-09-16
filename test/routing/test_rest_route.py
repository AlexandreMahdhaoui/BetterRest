import pytest

from test.routing.dummies import DummyRoute


class TestRestRoute:
    def test_as_route(self):
        print('\n', self.test.as_route())

    @pytest.fixture
    def fixture(self):
        self.setup()
        yield
        self.teardown()

    def setup(self):
        self.test = DummyRoute

    def teardown(self):
        pass

