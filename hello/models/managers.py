class AbstractManager:
    def __init__(self, cls: type):
        self.cls = cls

    def all(self):
        for cls in self._get_subclasses():
            yield from cls.objects.all()

    def filter(self, **kwargs):
        for cls in self._get_subclasses():
            yield from cls.objects.filter(**kwargs)

    def _get_subclasses(self) -> list:
        return self.cls.__subclasses__()
