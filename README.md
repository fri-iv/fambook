Fambook (c) 2017

- How to start:

1. sudo apt-get install python2.7 python-setuptools python-dev
2. sudo apt-get install python-pip
3. sudo apt-get install python-virtualenv
4. sudo apt-get install virtualenvwrapper
5. sudo apt-get install git
6. cd ~
7. git clone -b web_sockets https://github.com/symstu/fambook.git
8. mkvirtualenv fambook
9. workon fambook
10. cd fambook
11. add2virtualenv `pwd`
12. pip install -r conf/requirements.txt
13. sudo apt-get install postgresql postgresql-contrib
14. sudo -u postgres psql -c "alter role server with password '12345'"
15. sudo -u postgres createdb test2
16. cd db
17. alembic upgrade head
18. cd ../
19. python run_app.py