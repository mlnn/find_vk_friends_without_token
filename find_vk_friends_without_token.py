from urllib.parse import urlencode
import requests
from pprint import pprint
import time

AUTHORIZE_URL = 'https://oauth.vk.com/authorize'
APP_ID = # добавить номер приложения
VERSION = '5.68'
TOKEN = # добавить токен


def get_token():
    params = {
        'client_id': APP_ID,
        'display': 'page',
        'redirect_uri': 'https://oauth.vk.com/blank.html',
        'scope': 'friends,status',
        'response_type': 'token',
        'v': VERSION
    }
    print('?'.join(
        (AUTHORIZE_URL, urlencode(params))
    ))


def get_my_id():
    params = {
        'v': VERSION,
        'access_token': TOKEN,
    }

    response = requests.get('https://api.vk.com/method/users.get', params)
    data = response.json()
    return data['response'][0]['id']


def get_friends(user):
    params = {
        'v': VERSION,
        'access_token': TOKEN,
        'user_id': user
    }
    response = requests.get('https://api.vk.com/method/friends.get', params)
    # print(response.status_code)
    data = response.json()
    try:
        # pprint(data['error'])
        if data['error']['error_code'] == 6:
            return 'wait'
        elif data['error']['error_code'] == 18:
            return 'nobody'
    except:
        return data['response']['items']


def main():
    my_id = get_my_id()
    my_friends = set(get_friends(my_id))
    cross_friends = my_friends.copy()
    count = 0
    for friend in my_friends:
        # time.sleep(0.3)
        count += 1
        friends_of_friend = set(get_friends(friend))
        if friends_of_friend == set('wait'):
            print('Много запросов. Подождем')
            time.sleep(1)
            friends_of_friend = set(get_friends(friend))
            if friends_of_friend != set('nobody'):
                cross_friends.intersection_update(friends_of_friend)
            else:
                print('Страница удалена или заблокирована. Пропускаем')
        elif friends_of_friend == set('nobody'):
            print('Страница удалена или заблокирована. Пропускаем')
            continue
        else:
            cross_friends.intersection_update(friends_of_friend)
        print('Обработано {:.4}%'.format(count/len(my_friends)*100))
    print(len(cross_friends))

main()
