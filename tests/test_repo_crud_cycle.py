import requests
import time


class TestCRUD:
    #смотрим, что тестовая сущность (репозиторий) создалась (само создание вынесено в conftest.py)
    def test_get_repo(self, base_url, headers, repo_object_fixture):
        response = requests.get(f'{base_url}/repos/Mihail96tramontana/{repo_object_fixture}', headers=headers)
        assert response.status_code == 200, 'Код ответа сервера не 200'
        assert response.json()['name'] == repo_object_fixture, 'Ошибка в поле "name"'
        assert 'full_name' in response.json()
        assert 'Тестовый репозиторий' in response.json()['description']

    #обновляем описание тестовой сущности
    def test_patch_description_repo(self, base_url, headers, repo_object_fixture):
        response = requests.patch(f'{base_url}/repos/Mihail96tramontana/{repo_object_fixture}',
                                  headers=headers,
                                  json={'description':'Обновлённое описание'})
        assert response.status_code == 200, 'При обновлении описания сервер возвращает код ответа не 200'
        assert 'Обновлённое описание' in response.json()['description']

    #создаём тестовый issue в репозитории
    def test_create_issue(self, base_url, headers, repo_object_fixture):
        response = requests.post(f'{base_url}/repos/Mihail96tramontana/{repo_object_fixture}/issues', headers=headers,
                                 json={'title': 'Тестовый issue', 'body': 'Описание тестового issue'})
        assert response.status_code == 201, 'При создании issue код ответа не 200'
        assert response.json()['title'] == 'Тестовый issue', 'Ошибка в поле "title"'
        assert response.json()['state'] == 'open', 'Ошибка в поле "state"'

    #просматриваем созданный объект issue в списке
    def test_get_list_issue(self, base_url, headers, repo_object_fixture):
        time.sleep(5)
        response = requests.get(f'{base_url}/repos/Mihail96tramontana/{repo_object_fixture}/issues', headers=headers)
        assert response.status_code == 200, 'Код ответа при просмотре списка issue не 200'
        assert len(response.json())>0, 'В списке нет объектов'
        assert 'title' in response.json()[0]

    #закрываем активную задачу(issue)
    def test_close_issue(self, base_url, headers, repo_object_fixture):
        response = requests.patch(f'{base_url}/repos/Mihail96tramontana/{repo_object_fixture}/issues/1',
                                  headers=headers,
                                  json={'state': 'closed'})
        assert response.status_code == 200, 'Неправильный статус код при закрытии задачи(issue)'
        assert response.json()['state'] == 'closed', 'Ошибка в поле "state"'
    #после этого последнего теста выполняется teardown из фикстуры repo_object_fixture



