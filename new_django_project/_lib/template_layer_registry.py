
class Registry(object):
    _info_ = {}

    def __init__(self, request):
        self._info_ = {}

    def get(self, key):
        return self._info_.get(key)

    def set(self, key, value):
        self._info_[key] = value

    def delete(self, key):
        del(self._info_[key])