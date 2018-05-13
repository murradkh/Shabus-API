from datetime import timedelta
from functools import wraps, update_wrapper
from flask import request, make_response, current_app
from requests.compat import basestring



def crossdomain(origin=None, methods=None, headers=None, max_age=21600,
                attach_to_all=True, automatic_options=True):
    """Decorator function that allows crossdomain requests.
      Courtesy of
      https://blog.skyred.fi/articles/better-crossdomain-snippet-for-flask.html
    """
    if methods is not None:
        methods = ', '.join(sorted(x.upper() for x in methods))
    if headers is not None and not isinstance(headers, basestring):
        headers = ', '.join(x.upper() for x in headers)
    if not isinstance(origin, basestring):
        origin = ', '.join(origin)
    if isinstance(max_age, timedelta):
        max_age = max_age.total_seconds()

    def get_methods():
        """ Determines which methods are allowed
        """
        if methods is not None:
            return methods

        options_resp = current_app.make_default_options_response()
        return options_resp.headers['allow']

    def decorator(f):
        """The decorator function
        """
        def wrapped_function(*args, **kwargs):
            """Caries out the actual cross domain code
            """
            if automatic_options and request.method == 'OPTIONS':
                resp = current_app.make_default_options_response()
            else:
                resp = make_response(f(*args, **kwargs))
            if not attach_to_all and request.method != 'OPTIONS':
                return resp

            h = resp.headers
            h['Access-Control-Allow-Origin'] = origin
            h['Access-Control-Allow-Methods'] = get_methods()
            h['Access-Control-Max-Age'] = str(max_age)
            h['Access-Control-Allow-Credentials'] = 'true'
            h['Access-Control-Expose-Headers'] = 'Set-Cookie, Content-Length, Set-Cookie, Cookie'
            h['Access-Control-Allow-Headers'] = \
                "Origin, X-Requested-With, Content-Type, Accept, Authorization"
            if headers is not None:
                h['Access-Control-Allow-Headers'] = headers
            return resp

        f.provide_automatic_options = False
        return update_wrapper(wrapped_function, f)
    return decorator



# def require_login(func: function):
#     @wraps(func)
#     def decorated_function(*args, **kwargs):
#         pass
#
#     return decorated_function





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
