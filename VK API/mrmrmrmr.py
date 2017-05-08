import requests
import re
from datetime import date
import matplotlib.pyplot as plt
from matplotlib import style
style.use('ggplot') 

from collections import Counter

def vk_api(method, **kwargs):
    api_request = 'https://api.vk.com/method/'+method
    return requests.get(api_request, params=kwargs).json()

def word_count (text):
    return len([i for i in text.replace('\n', ' ').split(' ') if i != ''])


def get_comments(post, comment_max_count):
    comments = []
    if comment_max_count < 0:
        item_count = post['comments']['count']
    else:
        item_count = min(post['comments']['count'], comment_max_count)

    if item_count == 0:
        return []

    result = vk_api('wall.getComments', owner_id=post['owner_id'], post_id=post['id'], v='5.63', count=100)
    comments += result['response']['items']
    while len(comments) < item_count:
        result = vk_api('wall.getComments', owner_id=post['owner_id'], post_id=post['id'], v='5.63',
                        offset=len(comments), count=100)
        comments += result['response']['items']

    return comments

def load_posts (group_name, max_count=200):
    group_info = vk_api('groups.getById', group_id=group_name, v='5.63')
    group_id = group_info['response'][0]['id']

    posts = []

    result = vk_api('wall.get', owner_id=-group_id, v='5.63', count=100)
    posts += result['response']['items']

    if max_count < 0:
        item_count = result['response']['count']
    else:
        item_count = min(result['response']['count'], max_count)

    while len(posts) < item_count:
        result = vk_api('wall.get', owner_id=-group_id, v='5.63', count=100, offset=len(posts))
        posts += result['response']['items']

    return posts

def load_comments (posts, max_count=500):

    all_comments = []

    for post in posts:
        comments = get_comments(post, max_count)
        all_comments.append([{'len': word_count(i['text']), 'from_id': i['from_id']} for i in comments])

    return all_comments

def plot_word_counts (posts, comments):

    lens = [word_count(i['text']) for i in posts]

    comm_avg_lens = []

    for c in comments:
        if len(c) == 0:
            comm_avg_lens.append(0)
        else:
            comm_avg_lens.append(sum([i['len'] for i in c])/len(c))

    plt.figure()
    plt.scatter(lens, comm_avg_lens)
    plt.xlabel('post length')
    plt.ylabel('comment length')
    plt.show()

def find_user_age(bdate):
    d = [int(i) for i in bdate.split('.')]
    if len(d) < 3:
        return -1
    else:
        return (date.today() - date(d[2], d[1], d[0])).days // 365

def load_user_data (id):

    if id < 0:
        return {'age': -1, 'city': ''}

    result = vk_api('users.get', user_ids=id, fields='bdate,city')
    result = result['response'][0]

    if 'bdate' not in result:
        age = -1
    else:
        age = find_user_age(result['bdate'])

    if 'city' not in result or result['city'] == 0:
        city_name = ''
    else:
        city_id = result['city']
        city_name = vk_api('database.getCitiesById', city_ids=city_id)['response'][0]['name']

    return {'age': age, 'city': city_name}


def plot_users_from_posts (posts):

    ages = {}
    cities = {}

    for post in posts:
        user_data = load_user_data(post['from_id'])
        words = word_count(post['text'])

        if user_data['age'] in ages:
            ages[user_data['age']].append(words)
        else:
            ages[user_data['age']] = [words]

        if user_data['city'] in cities:
            cities[user_data['city']].append(words)
        else:
            cities[user_data['city']] = [words]

    age_keys = [i for i in ages if i != -1]
    age_avg_lens = [sum(ages[i])/len(ages[i]) for i in age_keys]

    plt.figure()
    plt.bar(age_keys, age_avg_lens)
    plt.title('Age/post length')
    plt.show()

    topcities = sorted([i for i in cities if i != ''], key = lambda x: len(cities[x]))[-25:]
    city_avg_lens = [sum(cities[i]) / len(cities[i]) for i in topcities]

    plt.figure()
    plt.bar(range(len(topcities)), city_avg_lens)
    plt.xticks(range(len(topcities)), topcities, rotation='vertical')
    plt.title('City/post length')
    plt.show()

def plot_users_from_comments (comments):

    ages = {}
    cities = {}

    for c_list in comments:
        for comment in c_list:
            user_data = load_user_data(comment['from_id'])

            if user_data['age'] in ages:
                ages[user_data['age']].append(comment['len'])
            else:
                ages[user_data['age']] = [comment['len']]

            if user_data['city'] in cities:
                cities[user_data['city']].append(comment['len'])
            else:
                cities[user_data['city']] = [comment['len']]

    age_keys = [i for i in ages if i != -1]
    age_avg_lens = [sum(ages[i])/len(ages[i]) for i in age_keys]

    plt.figure()
    plt.bar(age_keys, age_avg_lens)
    plt.title('Age/comment length')
    plt.show()

    topcities = sorted([i for i in cities if i != ''], key = lambda x: len(cities[x]))[-25:]
    city_avg_lens = [sum(cities[i]) / len(cities[i]) for i in topcities]

    plt.figure()
    plt.bar(range(len(topcities)), city_avg_lens)
    plt.xticks(range(len(topcities)), topcities, rotation='vertical')
    plt.title('City/comment length')
    plt.show()

posts = load_posts('wbtbwb_official')
comments = load_comments(posts)
plot_word_counts(posts, comments)
plot_users_from_posts(posts)
plot_users_from_comments(comments)
