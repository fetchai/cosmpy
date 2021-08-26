import os

for x in os.walk('../cosmpy'):
    sys.path.insert(0, x[0])