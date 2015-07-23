import random
import json
from Records import *
from FormID import FormIDHandler

form_ids = FormIDHandler()

f = open('..\enchants.json')
params = json.load(f, 'ascii')