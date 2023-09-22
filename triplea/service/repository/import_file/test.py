


import os

# for name, value in os.environ.items():
#     print("{0}: {1}".format(name, value))



name = "PATH"
print(os.environ.get(name))

print(os.environ.get('PYTHONPATH'))