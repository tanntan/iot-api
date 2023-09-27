import json
import random
from sqlalchemy import String, Column, Integer, Text, Boolean, DateTime, UnicodeText, func
from sqlalchemy.orm import declared_attr

MAX = 4000


def random_string(digit=8, chars='OObQYf56d5664UY0MknYZ2tnwhUmceceDTZLJjptw11ed-afa1-uXPiJVexrfSCH80242ac120002='):
    return ''.join(random.choice(chars) for x in range(digit))


def random_int(digit=8, chars='0123456789'):
    return int(''.join(random.choice(chars) for x in range(digit)))


Key = lambda: String(50)
gid = lambda: random_int()


def pk_column(**kwargs):
    return Column(Integer, autoincrement=True, primary_key=True, index=True, unique=True, **kwargs)


def fk_column(**kwargs):
    if 'index' not in kwargs:
        kwargs['index'] = True
    if 'default' not in kwargs:
        kwargs['default'] = 0
    if 'nullable' not in kwargs:
        kwargs['nullable'] = False
    return Column(Integer, **kwargs)


def code_column(**kwargs):
    if 'default' not in kwargs:
        kwargs['default'] = ''
    return Column(String(50), **kwargs)


def title_column(**kwargs):
    if 'default' not in kwargs:
        kwargs['default'] = ''
    return Column(String(250), **kwargs)


def note_column(**kwargs):
    if 'default' not in kwargs:
        kwargs['default'] = ''
    return Column(String(500), **kwargs)


def max_column(**kwargs):
    if 'default' not in kwargs:
        kwargs['default'] = ''
    return Column(String(MAX), **kwargs)


def text_column(**kwargs):
    if 'default' not in kwargs:
        kwargs['default'] = ''
    return Column(Text(), **kwargs)


def boolean_column(**kwargs):
    if 'default' not in kwargs:
        kwargs['default'] = False
    return Column(Boolean(), **kwargs)


def datetime_column(**kwargs):
    if 'default' not in kwargs:
        kwargs['default'] = func.now()
    return Column(DateTime, **kwargs)


def integer_column(**kwargs):
    if 'default' not in kwargs:
        kwargs['default'] = 0
    return Column(Integer(), **kwargs)


def enum_column(**kwargs):
    return Column(String(20), **kwargs)


def unicode_column(**kwargs):
    return Column(UnicodeText, **kwargs)


class Mixin(object):
    @declared_attr
    def id(self):
        return pk_column()

    @declared_attr
    def created_date(self):
        return datetime_column()

    @declared_attr
    def created_by(self):
        return title_column(default=lambda: 'system')

    @declared_attr
    def updated_date(self):
        return datetime_column(onupdate=func.now())

    @declared_attr
    def update_by(self):
        return title_column(onupdate=lambda: 'system')

    @declared_attr
    def is_active(self):
        return boolean_column(default=True)

    def __str__(self):
        if hasattr(self, 'code') and hasattr(self, 'name'):
            return u'%s - %s' % (self.code, self.name)
        if hasattr(self, 'code'):
            return getattr(self, 'code')
        if hasattr(self, 'name'):
            return getattr(self, 'name')
        return str(self.id)


class TrackMixin():
    pass


class ExtMixin(object):
    @declared_attr
    def ext_data(self):
        return text_column(default=lambda: '{}')

    @property
    def ext(self):
        if not hasattr(self, '_ext'):
            try:
                self._ext = json.loads(self.ext_data)
            except:
                self._ext = {}
            return self._ext

    @ext.setter
    def ext(self, value):
        self.ext_data = json.dumps(value)
        self._ext = value

    def __getattr__(self, name):
        if name.startswith('ext__'):
            keys = [k for k in name.split('__') if k and k != 'ext']
            if len(keys) == 1:
                return self.ext.get(keys[0])
            if len(keys) == 2:
                return self.ext.get(keys[0], dict()).get(keys[1])
        return super(ExtMixin, self).__getattribute__(name)

    def __setattr__(self, name, value):
        if name.startswith('ext__') and name != 'ext':
            keys = [k for k in name.split('__') if k and k != 'ext']
            if len(keys) == 1:
                self.ext[keys[0]] = value
            if len(keys) == 2:
                if keys[0] not in self.ext:
                    self.ext[keys[0]] = dict()
                self.ext[keys[0]][keys[1]] = value
            self.ext = self.ext
        super(ExtMixin, self).__setattr__(name, value)
