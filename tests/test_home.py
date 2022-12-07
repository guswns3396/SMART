import pytest

from flaskr.home import app


# test configure
    # create study
    # invalid parameters
    # redirect to show
# test join
    # invalid id
    # valid id

@pytest.fixture
def client():
    """
    Configures the app for testing
    Sets app config variable ``TESTING`` to ``True``
    :return: App for testing
    """
    app.config['TESTING'] = True
    client = app.test_client()
    yield client
