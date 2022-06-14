import time
import vk_api

vk_session = vk_api.VkApi(token='732431c2059a1e95c704562fd0b576ae218c11e0276da609c2d2afeb26f7baefc1457ef5a5f201218385c')
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