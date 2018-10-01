import pytest

from salicml.api import main as salicml
from salicml.middleware.middleware import Middleware
from salicml.data_source.data_source_db import DataSourceMock

OK_CODE = 200
BAD_CODE = 400


def get_data_source():
    planilha_orcamentaria = [['012345', '2A', 123],
                             ['012345', '2A', 124],
                             ['012345', '2A', 125],
                             ['012348', '3A', 126],
                             ['012348', '3A', 127], ]
    data_source = DataSourceMock(planilha_orcamentaria=planilha_orcamentaria)

    columns = ['0', '1', '2']

    print(
        'data_source.planilha = {}'.format(
            data_source.get_planilha_orcamentaria(
                columns=columns)))
    return data_source


@pytest.fixture
def client():
    app = salicml.app
    app.config['TESTING'] = True

    data_source = get_data_source()
    app.middleware = Middleware(data_source=data_source)
    app.middleware.load_all()
    client = salicml.app.test_client()

    yield client  # TearDown code is below, SetUp code is above

    pass


def test_number_of_item_endpoint_keys(client):
    ''''''
    pronac = '012345'
    endpoint = 'metric/number_of_items/{}'.format(pronac)
    response = client.get(endpoint)
    result = response.json

    assert response.status_code == OK_CODE

    expected_keys = ['is_outlier', 'maximum_expected', 'minimum_expected',
                     'number_of_items']

    for key in expected_keys:
        assert key in result

    assert len(result) == len(expected_keys)


def test_number_of_items_endpoint_invalid_pronac(client):
    pronac = '123a45'
    endpoint = 'metric/number_of_items/{}'.format(pronac)
    response = client.get(endpoint)
    assert response.status_code == BAD_CODE
