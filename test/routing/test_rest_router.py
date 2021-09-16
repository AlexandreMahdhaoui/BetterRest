import pytest

from test.routing.dummies import DummyRouter


class TestRestRouter:
    def test_as_list(self):
        print('\n', self.test.as_list())

    def test_as_mount(self):
        print('\n', self.test.as_mount())

    @pytest.fixture
    def fixture(self):
        self.setup()
        yield
        self.teardown()

    def setup(self):
        self.test = DummyRouter

    def teardown(self):
        pass
