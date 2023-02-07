username = [1, 2 ,3 ,4 ,5, 6, 7]
password_list = [1, 2, 3, 4, 5, 6, 7]
x = 0
y = 3
j = 0
y = len(username)
for u in username:
    for p in password_list[x:y]:
        j = +1
        creds = {
            'username': u,
            'password': p
            }
        print(u, p)
        print(j)
        if j == len(username):
            x += 3
            y += 3