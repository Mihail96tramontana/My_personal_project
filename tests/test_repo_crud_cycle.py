import requests
import time
import allure

@allure.feature('Тестирование репозитория')
@allure.story('Позитивные сценарии')
class TestCRUD:
    @allure.title('Проверка создания репозитория')
    @allure.description('Смотрим, что тестовая сущность (репозиторий) действительно создалась методом get (само создание вынесено в conftest.py)')
    @allure.severity(allure.severity_level.CRITICAL)
    def test_get_repo(self, base_url, headers, repo_object_fixture):
        with allure.step('Отправляем POST-запрос на создание тестовой сущности - нового репозитория'):
            response = requests.get(f'{base_url}/repos/Mihail96tramontana/{repo_object_fixture}', headers=headers)
        with allure.step('Проверяем, что отдаваемый сервером код ответа - 200'):
            assert response.status_code == 200, 'Код ответа сервера не 200'
        with allure.step('Проверяем поля, которые отдаёт сервер'):
            assert response.json()['name'] == repo_object_fixture, 'Ошибка в поле "name"'
            assert 'full_name' in response.json()
            assert 'Тестовый репозиторий' in response.json()['description']

    @allure.title('Проверяем обновление тестовой сущности')
    @allure.description('Обновляем описание репозитория методом patch')
    @allure.severity(allure.severity_level.NORMAL)
    def test_patch_description_repo(self, base_url, headers, repo_object_fixture):
        with allure.step(' PATCH-запрос на обновление поля "description"'):
            response = requests.patch(f'{base_url}/repos/Mihail96tramontana/{repo_object_fixture}',
                                  headers=headers,
                                  json={'description':'Обновлённое описание'})
            with allure.step('Проверяем, что отдаваемый сервером код ответа - 200'):
                assert response.status_code == 200, 'При обновлении описания сервер возвращает код ответа не 200'
            with allure.step('Проверяем, что значение в поле "description" сменилось'):
                assert 'Обновлённое описание' in response.json()['description']

    @allure.title('Проверяем создание тестовой issue(задачи)')
    @allure.description('Создаём тестовую задачу(issue) методом post')
    @allure.severity(allure.severity_level.NORMAL)
    def test_create_issue(self, base_url, headers, repo_object_fixture):
        with allure.step('Отправляем POST-запрос на создание задачи'):
            response = requests.post(f'{base_url}/repos/Mihail96tramontana/{repo_object_fixture}/issues', headers=headers,
                                 json={'title': 'Тестовый issue', 'body': 'Описание тестового issue'})
        with allure.step('Проверяем, что отдаваемый сервером код ответа - 201'):
            assert response.status_code == 201, 'При создании issue код ответа не 200'
        with allure.step('Проверяем поля, которые отдаёт сервер'):
            assert response.json()['title'] == 'Тестовый issue', 'Ошибка в поле "title"'
            assert response.json()['state'] == 'open', 'Ошибка в поле "state"'

    @allure.title('Просмотр созданного issue в списке')
    @allure.description('Просматриваем созданный объект issue в списке методом get')
    @allure.severity(allure.severity_level.NORMAL)
    def test_get_list_issue(self, base_url, headers, repo_object_fixture):
        time.sleep(5)
        with allure.step('Отправляем GET-запрос на просмотр списка задач'):
            response = requests.get(f'{base_url}/repos/Mihail96tramontana/{repo_object_fixture}/issues', headers=headers)
        with allure.step('Проверяем, что отдаваемый сервером код ответа - 200'):
            assert response.status_code == 200, 'Код ответа при просмотре списка issue не 200'
        with allure.step('Проверяем, что в списке есть объекты и он не пустой'):
            assert len(response.json())>0, 'В списке нет объектов'
        with allure.step('Проверяем, что сервер отдаёт поле "title" в первом объекте'):
            assert 'title' in response.json()[0]

    @allure.title('Закрываем задачу(issue)')
    @allure.description('Закрываем активную задачу(issue) методом patch')
    @allure.severity(allure.severity_level.NORMAL)
    def test_close_issue(self, base_url, headers, repo_object_fixture):
        with allure.step('Отправляем PATCH-запрос на закрытие активной задачи(issue)'):
            response = requests.patch(f'{base_url}/repos/Mihail96tramontana/{repo_object_fixture}/issues/1',
                                      headers=headers,
                                      json={'state': 'closed'})
        with allure.step('Проверяем, что отдаваемый сервером код ответа - 200'):
            assert response.status_code == 200, 'Неправильный статус код при закрытии задачи(issue)'
        with allure.step('Проверяем, что значение в поле "state" = "closed"'):
            assert response.json()['state'] == 'closed', 'Ошибка в поле "state"'

    #после этого последнего теста выполняется teardown из фикстуры repo_object_fixture



