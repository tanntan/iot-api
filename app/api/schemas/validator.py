from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel


class LTMsgError(Exception):
    status_code: int
    detail: str
    message: str
    type: str
    value: str
    field: str

    def __init__(self, status_code=500, message='', type='', value='', field='', detail='', *args, **kwargs):
        self.status_code = status_code
        self.message = message
        self.type = type
        self.value = value
        self.field = field
        self.detail = detail
        super(LTMsgError, self).__init__(args, kwargs)


class NotFoundException(LTMsgError):
    def __init__(self, status_code=404, message='DATA NOT FOUND'):
        super(NotFoundException, self).__init__(status_code, message)


class BadRequestException(LTMsgError):
    def __init__(self, status_code=400, message='Bad Request'):
        super(BadRequestException, self).__init__(status_code, message)


class ForbiddenException(LTMsgError):
    def __init__(self, status_code=403, message='Forbidden'):
        super(ForbiddenException, self).__init__(status_code, message)


class UnauthorizedException(LTMsgError):
    def __init__(self, status_code=401, message='Unauthorized'):
        super(UnauthorizedException, self).__init__(status_code, message)


class CustomRequestValidationError(RequestValidationError):
    def __init__(self):
        self.status_code = 400
        self.detail = "Validation Error"

# #
# # HTTP_STATUS_CODE = {
# #     'noContent': 204,
# #     'fieldError': 400,
# #     'unauthorized': 403,
# #     'errorNotFound': 404,
# #     'noPermission': 401
# # }
#
#
# def return_error(errors):
#     try:
#         if isinstance(errors, list):
#             error = errors[0]
#         elif isinstance(errors.get('message'), dict) and 'errors' in errors.get('message'):
#             errors = errors.get('message').get('errors')
#             if isinstance(errors, list):
#                 error = errors[0]
#             else:
#                 error = errors
#         else:
#             error = errors
#             if isinstance(error.get('value'), list):
#                 error['value'] = ';'.join(error['value'])
#             errors = [error]
#         error = LTMsgError(**error)
#         if isinstance(error.value, list):
#             error.value = ';'.join(error.value)
#         return {
#                    'errors': errors,
#                    'type': error.type,
#                    'message': error.__dict__
#                }, HTTP_STATUS_CODE.get(error.type)
#     except Exception as e:
#         return {
#                    'errors': [LTMsgError(message=str(e), type=type(e).__name__, value='', field='').__dict__],
#                    'type': type(e).__name__,
#                    'message': e
#                }, 400
#
#
# ignore_keys = ['id', 'is_active']
#
#
# def validator(marshall_model, expect_model=''):
#     def validator_decorator(func):
#         def wrapper(*args, **kwargs):
#             if config.APP_MODE == 'development':
#                 func2 = marshal_with(marshall_model)(func)
#                 return func2(*args, **kwargs)
#             errors = []
#             try:
#                 if expect_model:
#                     payload = json.loads(request.get_data())
#                     for key in expect_model:
#                         if key not in ignore_keys:
#                             if getattr(expect_model[key], 'required'):
#                                 if key not in payload:
#                                     errors.append(
#                                         LTMsgError('missing field [{}]'.format(key), enum.ErrorType.fieldError, '',
#                                                    key).__dict__)
#                                 if key not in payload and not payload[key]:
#                                     errors.append(
#                                         LTMsgError('required field [{}]'.format(key), enum.ErrorType.fieldError, '',
#                                                    key).__dict__)
#
#                     # check payload
#                     for key in payload:
#                         if key not in ignore_keys:
#                             if getattr(expect_model, key, None):
#                                 field = getattr(expect_model, key)
#                                 if hasattr(field, 'pattern') and field.pattern:
#                                     if not re.match(field.pattern, payload[key]):
#                                         errors.append(
#                                             LTMsgError("invalid value '{}'".format(payload[key]),
#                                                        enum.ErrorType.fieldError,
#                                                        payload[key],
#                                                        key).__dict__)
#                             if key not in expect_model:
#                                 pass
#
#                     if errors:
#                         return return_error(errors)
#                 func2 = marshal_with(marshall_model)(func)
#                 return func2(*args, **kwargs)
#             except ValueError as e:
#                 return {
#                            'errors': [
#                                LTMsgError(message=str(e), type=type(e).__name__, value='', field='').__dict__],
#                            'type': type(e).__name__,
#                            'message': str(e)
#                        }, 400
#             except Unauthorized as e:
#                 return {
#                            'errors': [
#                                LTMsgError(message=str(e), type=type(e).__name__, value='', field='').__dict__],
#                            'type': type(e).__name__,
#                            'message': str(e)
#                        }, 401
#
#             except ObjNotFoundError as e:
#                 return {
#                            'errors': [
#                                LTMsgError(message=str(e), type=type(e).__name__, value='', field='').__dict__],
#                            'type': type(e).__name__,
#                            'message': str(e)
#                        }, 404
#
#             except Exception as e:
#                 if isinstance(e, LTMsgError):
#                     return return_error(e.__dict__)
#                 return {
#                            'errors': [
#                                LTMsgError(message=str(e), type=type(e).__name__, value='', field='').__dict__],
#                            'type': type(e).__name__,
#                            'message': str(e)
#                        }, 500
#
#         return wrapper
#
#     return validator_decorator
#
#
# def requires_access_level(access_level):
#     def decorator(f):
#         @wraps(f)
#         def decorated_function(*args, **kwargs):
#             if config.APP_MODE == 'development':
#                 return f(*args, **kwargs)
#             from camauto.api.current import current
#             user = current.user()
#             if not user:
#                 return {
#                            'errors': [
#                                LTMsgError(message="USER DON'T HAVE PERMISSION", type=enum.ErrorType.noPermission,
#                                           value='', field='').__dict__],
#                            'type': enum.ErrorType.noPermission,
#                            'message': 'NO PERMISSION'
#                        }, 401
#             elif user.role_name not in access_level and 'all' not in access_level:
#                 return {
#                            'errors': [
#                                LTMsgError(message="USER DON'T HAVE PERMISSION", type=enum.ErrorType.noPermission,
#                                           value='', field='').__dict__],
#                            'type': enum.ErrorType.noPermission,
#                            'message': 'NO PERMISSION'
#                        }, 401
#             return f(*args, **kwargs)
#
#         return decorated_function
#
#     return decorator
