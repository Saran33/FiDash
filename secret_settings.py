import os


# class RandReprod(object):
#     def seed(self, a=3):
#         self.seedint = a
#     def random(self):
#         self.seedint = (self.seedint * 3) % 19
#         return self.seedint

# _inst = RandReprod()
# seed = _inst.seed
# random = _inst.random

# SECRET_KEY = os.urandom(12).hex()
SECRET_KEY = os.urandom(12).hex()
# SECRET_KEY = "TEST_SECRET_KEY"