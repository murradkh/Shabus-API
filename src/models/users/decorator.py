from functools import wraps


def require_login(func: function):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        pass

    return decorated_function

# class abc(object):
#
#     def __init__(self,b,a,f=None,v=None):
#         self.a=a
#         self.b=b
#         print(a)
#         print(b)
#         # print(sd)
#
#     @classmethod
#     def test(cls,*args,**kwargs):
#         print(kwargs)
#         print(args)
#         print(*args)
#         return cls(*args, **kwargs)
# # print(**D)
# def ta(a,f,d):
#     pass
#
# # abc.test(a=3)
# ta(2,d=2,f=2)
# a = [21,1,4]
# print(*a)
