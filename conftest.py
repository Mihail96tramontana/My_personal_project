import requests
import pytest
from config import GITHUB_TOKEN, BASE_URL


@pytest.fixture(scope='session')
def base_url():
    return BASE_URL

@pytest.fixture(scope='session')
def headers():
    return {'Authorization': f'Bearer {GITHUB_TOKEN}',
            'Accept':'application/vnd.github+json'}

@pytest.fixture(scope='session')
def repo_object_fixture(base_url, headers):
    response = requests.post(f'{base_url}/user/repos', headers=headers, json={'name': 'test-repo-autotest',
                                                                              'description': 'Тестовый репозиторий',
                                                                              'private': False})
    assert response.status_code == 201, 'Код ответа сервера не 201'
    repo_object = response.json()['name']

    yield repo_object

    response = requests.delete(f'{base_url}/repos/Mihail96tramontana/{repo_object}', headers=headers)

