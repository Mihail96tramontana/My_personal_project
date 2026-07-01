import requests
import pytest
import allure


@allure.feature('Тестирование репозитория')
@allure.story('Негативные сценарии')
class TestNegativeCRUD:
    @allure.title('Создание дубликата репозитория')
    @allure.description('Создаём репозиторий с именем, которое уже используется в другом репозитории')
    @allure.severity(allure.severity_level.CRITICAL)
    def test_creat_repo_duplicate(self, base_url, headers, repo_object_fixture):
        with allure.step('Отправляем POST-запрос на создание дубликата репозитория'):
            response = requests.post(f'{base_url}/user/repos', headers=headers, json={'name': repo_object_fixture,
                                                                              'description': 'Тестовый репозиторий',
                                                                              'private': False})
        with allure.step('Проверяем, что код ответа 422'):
            assert response.status_code == 422, 'Код ответа сервера не 422'

    @allure.title('Просмотр несуществующего репозитория')
    @allure.description('Смотрим, что при запросе несуществующего репозитория отдаётся ошибка')
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize('repo_name_incorrect, expected_status_code', [('not-exist-repo', 404), ('fake-repo-123', 404)])
    def test_get_repo_non_existent(self, base_url, headers, repo_name_incorrect, expected_status_code):
        with allure.step('Отправляем GET-запрос на просмотр несуществующего репозитория'):
            response = requests.get(f'{base_url}/repos/Mihail96tramontana/{repo_name_incorrect}', headers=headers)
        with allure.step('Проверяем, что код ответа ожидаемый, скорее всего 404'):
            assert response.status_code == expected_status_code, 'Код ответа не ожидаемый'

    @allure.title('Удаление несуществующего репозитория')
    @allure.description('Смотрим, что при запросе на удаление несуществующего репозитория отдаётся ошибка')
    @allure.severity(allure.severity_level.NORMAL)
    def test_delete_repo_non_existent(self, base_url, headers):
        with allure.step('Отправляем DELETE-запрос на удаление несуществующего репозитория'):
            response = requests.delete(f'{base_url}/repos/Mihail96tramontana/non-existent-repo', headers=headers)
        with allure.step('Проверяем, что код ответа 404'):
            assert response.status_code == 404, 'Код ответа сервера не 404'

    @allure.title('Просмотр профиля юзера без авторизации')
    @allure.description('Смотрим, что неавторизованному юзеру нельзя просмотреть профиль любого юзера')
    @allure.severity(allure.severity_level.CRITICAL)
    def test_non_authorization(self, base_url):
        with allure.step('Отправляем GET-запрос на просмотр профиля неавторизованным юзером'):
            response = requests.get(f'{base_url}/user')
        with allure.step('Проверяем, что код ответа 401'):
            assert response.status_code == 401, 'Код ответа сервера не 401'

    @allure.title('Создание репозитория с некорректным телом')
    @allure.description('Смотрим, что нельзя создать репозиторий не заполнив обязательные поля')
    @allure.severity(allure.severity_level.NORMAL)
    def test_creat_repo_incorrect_body(self, base_url, headers):
        with allure.step('Отправляем запрос на создание репозитория с некорректным телом'):
            response = requests.post(f'{base_url}/user/repos', headers=headers, json={'name': '','description': '', 'private': False})
        with allure.step('Проверяем, что код ответа 422'):
            assert response.status_code == 422, 'Код ответа не 422'
        with allure.step('Проверяем поля, которые отдаёт сервер'):
            assert response.json()['message'] == 'New repository name must not be blank', 'Ошибка в поле "message"'
            assert 'errors' in response.json(), 'Поля "errors" нет в ответе от сервера'

    @allure.title('Создание репозитория без тела')
    @allure.description('Тестируем, что нельзя создать репозиторий без тела запроса вообще')
    @allure.severity(allure.severity_level.NORMAL)
    def test_creat_repo_non_body(self, base_url, headers):
        with allure.step('Отправляем POST-запрос на создание репозитория без тела'):
            response = requests.post(f'{base_url}/user/repos', headers=headers, json={})
        with allure.step('Проверяем, что код ответа 422'):
            assert response.status_code == 422, 'Код ответа не 422'
        with allure.step('Проверяем поля, которые отдаёт сервер'):
            assert response.json()['message'] == 'New repository name must not be blank'
            assert 'errors' in response.json(), 'Поля "errors" нет в ответе от сервера'

    @allure.title('Просмотр юзера профиля с невалидным токеном')
    @allure.description('Тестируем, что нельзя просмотреть профиль какого угодно юзера с невалидным токеном')
    @allure.severity(allure.severity_level.CRITICAL)
    def test_invalid_token(self, base_url):
        with allure.step('Отправляем GET-запрос на просмотр профиля юзера с невалидным токеном'):
            response = requests.get(f'{base_url}/user', headers={'Authorization':'Bearer invalid_token_12345'})
        with allure.step('Проверяем, что код ответа сервера 401'):
            assert response.status_code == 401, 'Код ответа не 401'



