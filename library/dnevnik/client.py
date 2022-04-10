import requests
import logging
log = logging.getLogger(__name__)

from library.logging import colorize_json, cm, color

BASE_URL = 'https://dnevnik.mos.ru'

class ApiUrl:
    GROUPS = '/jersey/api/groups'
    SCHEDULE_ITEMS = '/jersey/api/schedule_items'
    ACADEMIC_YEARS = '/core/api/academic_years'
    TEACHER_PROFILES = '/core/api/teacher_profiles/{teacher_id}'
    STUDENT_PROFILES = '/core/api/student_profiles'
    ATTENDANCES = '/core/api/attendances?pid={teacher_id}'
    MARKS_GET = '/core/api/marks'
    MARKS_POST = '/core/api/marks?pid={teacher_id}'
    MARKS_PUT = '/core/api/marks/{mark_id}?pid={teacher_id}'
    CONTROL_FORMS = '/core/api/control_forms'

    LMS_LOGIN = '/lms/api/sessions'
    LMS_LOGOUT = '/lms/api/sessions?authentication_token={auth_token}'


class AuthorizedClient:
    def __init__(self, *, username: str=None, password: str=None):    
        self._base_url = BASE_URL
        self._login(username=username, password=password)

    def _login(self, username, password):
        log.info('Trying to log in...')
        response = requests.post(
            self.get_full_url(ApiUrl.LMS_LOGIN),
            headers=self.headers(add_personal=False),
            json={'login': username, 'password_plain': password}
        ).json()
        self._profile_id = response['profiles'][0]['id']
        self._auth_token = response['authentication_token']
        log.info(f'Got profile_id {self._profile_id} and auth_token of len {len(self._auth_token)} for {username} at login')

    def _logout(self):
        raise RuntimeError('Logout is disabled as it will require login on all devices')

        response = requests.delete(
            self.get_full_url(ApiUrl.LMS_LOGOUT.format(authentication_token=self._auth_token)),
            headers=self.headers(add_personal=False)
        ).json()
        if response == {'status': 'ok', 'http_status_code': 200}:
            log.info(f'Logged out')
        else:
            log.error(f'Got during log out: {response}')
            raise RuntimeError('Could not logout')

    def headers(self, add_personal=True):
        headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
            'Connection': 'keep-alive',
            'Content-Type': 'application/json;charset=utf-8',
            'Origin': self._base_url,
            'Referer': f'{self._base_url}/',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:83.0) Gecko/20100101 Firefox/83.0',
        }
        if add_personal:
            headers.update({
                'Auth-Token': self._auth_token,
                'Profile-Id': str(self._profile_id),
            })
        return headers

    def _check_response(self, response):
        try:
            data = response.json()
        except:
            log.error(f'Could not load json from {response.text}')
            raise

        if isinstance(data, dict):
            if data.get('code') == 400:
                raise RuntimeError(f'Got 400: {colorize_json(data)}')
            if data.get('message') == 'Предыдущая сессия работы в ЭЖД завершена. Войдите в ЭЖД заново':
                raise RuntimeError(f'Token is invalid')

        return data

    def get_full_url(self, path):
        assert path.startswith('/'), f'path must start with /, got: {path!r}'
        return f'{self._base_url}{path}'

    def post(self, url: str, json_data: dict):
        full_url = self.get_full_url(url)
        try:
            response = requests.post(full_url, json=json_data, headers=self.headers())
            return self._check_response(response)
        except:
            log.error(f'Error on POST to {full_url} with {colorize_json(json_data)}')
            raise

    def put(self, url: str, json_data: dict):
        full_url = self.get_full_url(url)
        try:
            response = requests.put(full_url, json=json_data, headers=self.headers())
            return self._check_response(response)
        except:
            log.error(f'Error on PUT to {full_url} with {colorize_json(json_data)}')
            raise

    def get(self, url: str, params: dict):
        full_url = self.get_full_url(url)

        str_params = {}
        for key, value in params.items():
            str_params[key] = str(value)

        try:
            response = requests.get(full_url, params=str_params, headers=self.headers())
            return self._check_response(response)
        except:
            log.error(f'Error on GET to {full_url} with str params {colorize_json(str_params)}')
            raise
