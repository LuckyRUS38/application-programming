import time
import vk_api

vk_session = vk_api.VkApi(token='9aea6a728c90f96975a95f941bd4ca253417f3075564df88f3b71f9ed5984ee72ab61f515ab292d2837a1')
vk = vk_session.get_api()

people = set()
links = []
my_id = 711975659

friends = vk.friends.get(user_id=711975659, fields=['name'])

for friend in friends['items']:
    people.add((friend['id'], friend['first_name'], friend['last_name']))
    links.append((my_id, friend['id']))

list_people = list(people).copy()

for person in list_people:
    try:
        friends = vk.friends.get(user_id=person[0], fields=['first_name'])
    except vk_api.exceptions.ApiError:
        continue
    for friend in friends['items']:
        people.add((friend['id'], friend['first_name'], friend['last_name']))
        links.append((person[0], friend['id']))
    time.sleep(0.35)
    print(person)

f = open('people.txt', 'w')
for person in people:
    try:
        f.write(str(person[0]) + ' ' + person[1] + ' ' + person[2] + '\n')
    except Exception:
        continue

f.close()

f = open('links.txt', 'w')
for link in links:
    f.write(str(link[0]) + ' ' + str(link[1]) + '\n')
f.close()