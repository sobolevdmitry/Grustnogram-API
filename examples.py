from grustnogram import Grustnogram


# регистрация
api = Grustnogram()
response = api.register('johndoe', 'johndoe@mail.ru', '123456').json()
print(response)


# загрузка изображения и публикация поста
api = Grustnogram(access_token='your valid token')
image = open('sad-photo.jpg', 'rb')
response = api.upload_image(image).json()
media_url = response['data']
api.publish_post(media_url, 'очень грустное фото')


# получение всех публикаций из профиля пользователя
api = Grustnogram(access_token='your valid token')
response = api.get_user('lara').json()
id_user = response['data']['id']
posts = []
try:
    offset_post_id = None
    while True:
        response = api.posts(id_user=id_user, offset_post_id=offset_post_id).json()
        if response['err_msg'][0] is not None:
            raise Exception(response['err_msg'][0])
        if len(response['data']) == 0:
            break
        posts += response['data']
        offset_post_id = response['data'][-1]['id']
    print(posts)
except Exception as e:
    print(e)
