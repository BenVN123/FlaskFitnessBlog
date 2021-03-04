import os

os.system('set FLASK_APP=fitnesssite')

"""
while True:
    e = input('Development mode [y/n]? ')
    if e == 'y':
        os.system('set FLASK_ENV=development')
        break
    elif e == 'n':
        break

while True:
    e = input('Initialize database [y/n]? ')
    if e == 'y':
        os.system('flask init-db')
        break
    elif e == 'n':
        break
"""

os.system('flask run')