from facebook_api import FacebookTestUser

f = FacebookTestUser()
users = f.test_user_list()
print 'users:', users
print 'type:', type(users)

for user in users:
    print user
# print f.app_auth()
# pointer = f.pointer()
# print pointer
# user = f.create_test_user()
# print user
# print f.delete_test_user('108790399692628')
# print f.delete_test_user('104086696832220')
# print f.delete_test_user('111030702800927')