
'''
pythonでは、
プロジェクト内で上位の階層にあるモジュールを直接読み込めない。
それをやるには、__init.py__にそれぞれimportを行っておくことが必用なようだ。
'''

'''
import os
from os.path import join, dirname
from dotenv import load_dotenv
ここに処理を記述した場合、クローラーを起動した際に最初に動く。
print('===',__path__)

#dotenv_path = join(dirname(__file__), '../../.env')
dotenv_path = join(dirname(__file__),'.env')
print('===',dotenv_path)
load_dotenv(dotenv_path)
#load_dotenv('/home/mikuras/sc/ranko/ranko/.env')

print('=== dot env test',os.environ.get("MONGOCLIENT"))
'''