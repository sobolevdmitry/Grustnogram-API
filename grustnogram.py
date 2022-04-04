import requests
from urllib.parse import urlencode


class Grustnogram:
    API_URL = 'https://api.grustnogram.ru'
    UPLOAD_URL = 'https://media.grustnogram.ru/cors.php'
    TIMEOUT = 5
    DEFAULT_USERAGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36'

    def __init__(self, access_token=None, useragent=None, proxies=None):
        self.access_token = access_token
        self.proxies = proxies
        if useragent is not None:
            self.useragent = useragent
        else:
            self.useragent = self.DEFAULT_USERAGENT

    def register(self, nickname, email, password):
        return self.request('/users', {
            'nickname': nickname,
            'email': email,
            'password': password,
            'password_confirm': password
        })

    def login(self, nickname, password):
        return self.request('/sessions', {
            'email': nickname,
            'password': password
        })

    def activate(self, code):
        return self.request('/activate', {
            'code': code
        })

    def logout(self):
        return self.request('/sessions/current', method='DELETE')

    def reset_password(self, email):
        return self.request('/respsswd', {
            'email': email
        })

    def update_password(self, code, password):
        return self.request('/updpsswd', {
            'code': code,
            'password': password,
            'password_confirm': password
        })

    def self(self):
        return self.request('/users/self')

    def status(self):
        return self.request('/status')

    def notifications(self):
        return self.request('/notifications')

    def posts(self, q=None, id_user=None, offset_post_id=None, my=None):
        body = {}
        if q:
            body['q'] = q
        if id_user:
            body['id_user'] = id_user
        if offset_post_id:
            body['offset_post_id'] = offset_post_id
        if my:
            body['my'] = my
        return self.request('/posts?' + urlencode(body))

    def users(self, q):
        body = {
            'q': q
        }
        return self.request('/users?' + urlencode(body))

    def get_user(self, nickname):
        return self.request('/users/' + nickname)

    def get_followers(self, user_id, offset_id=None):
        body = {
            'id': user_id
        }
        if offset_id:
            body['offset_id'] = offset_id
        return self.request('/followers/' + str(user_id) + '?' + urlencode(body))

    def get_followings(self, user_id, offset_id=None):
        body = {
            'id': user_id
        }
        if offset_id:
            body['offset_id'] = offset_id
        return self.request('/follow/' + str(user_id) + '?' + urlencode(body))

    def get_post(self, code):
        return self.request('/p/' + str(code))

    def get_post_likes(self, post_id, offset_id=None):
        body = {
            'id': post_id
        }
        if offset_id:
            body['offset_id'] = offset_id
        return self.request('/posts/' + str(post_id) + '/likes?' + urlencode(body))

    def get_post_comments(self, post_id, offset=None):
        body = {
            'id': post_id
        }
        if offset:
            body['offset'] = offset
        return self.request('/posts/' + str(post_id) + '/comments?' + urlencode(body))

    def like(self, post_id):
        return self.request('/posts/' + str(post_id) + '/like', method='POST')

    def unlike(self, post_id):
        return self.request('/posts/' + str(post_id) + '/like', method='DELETE')

    def follow(self, user_id):
        return self.request('/users/' + str(user_id) + '/follow', method='POST')

    def unfollow(self, user_id):
        return self.request('/users/' + str(user_id) + '/follow', method='DELETE')

    def comment(self, post_id, text):
        body = {
            'comment': text
        }
        return self.request('/posts/' + str(post_id) + '/comments?' + urlencode(body), method='POST')

    def delete_comment(self, comment_id):
        return self.request('/posts/comments/' + str(comment_id), method='DELETE')

    def complaint(self, post_id, reason):
        return self.request('/posts/' + str(post_id) + '/complaint?type=' + str(reason), method='POST')

    def edit_profile(self, nickname=None, name=None, about=None, avatar=None):
        body = {}
        if nickname is not None:
            body['nickname'] = nickname
        if name is not None:
            body['name'] = name
        if about is not None:
            body['about'] = about
        if avatar is not None:
            body['avatar'] = avatar
        return self.request('/users/self', data=body, method='PUT')

    def delete_avatar(self):
        return self.edit_profile(avatar="")

    def publish_post(self, media_url, text):
        return self.request('/posts', data={
            'filter': 1,
            'text': text,
            'media': [
                media_url
            ]
        })

    def edit_post(self, post_id, text):
        return self.request('/posts/' + str(post_id), data={
            'text': text
        }, method='PUT')

    def delete_post(self, post_id):
        return self.request('/posts/' + str(post_id), method='DELETE')

    def upload_image(self, file):
        return requests.post(self.UPLOAD_URL, headers=self.get_headers(), files={'file': file}, proxies=self.proxies, timeout=self.TIMEOUT)

    def request(self, endpoint, data=None, method=None):
        try:
            if method is None:
                if data is None:
                    method = 'GET'
                else:
                    method = 'POST'
            headers = self.get_headers()
            if method == 'GET':
                return requests.get(f'{self.API_URL}{endpoint}', headers=headers, proxies=self.proxies, timeout=self.TIMEOUT)
            else:
                return requests.request(method, f'{self.API_URL}{endpoint}', json=data, headers=headers, proxies=self.proxies, timeout=self.TIMEOUT)
        except (requests.exceptions.ProxyError,
                requests.exceptions.ReadTimeout,
                requests.exceptions.ConnectTimeout):
            return self.request(endpoint=endpoint, data=data, method=method)

    def get_headers(self):
        headers = {
            'User-Agent': self.useragent,
            'Origin': 'https://grustnogram.ru',
            'Referer': 'https://grustnogram.ru',
        }
        if self.access_token is not None:
            headers['Access-Token'] = self.access_token
        return headers
