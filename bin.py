# import json

# a = {'value':b'Hello'}

# b = json.dumps(a)

import pickle

a = b'Hello'
b = pickle.dumps(a)

c = pickle.loads(b)
print(type(c))