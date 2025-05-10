class UserView:
    def __init__(self, model: User):
        self._model = model

    @property
    def id(self):
        """Access the id field."""
        return self._model.id

    @id.setter
    def id(self, value):
        # TODO: Add validation or transformation if needed
        self._model.id = value

    @id.deleter
    def id(self):
        del self._model.id

    @property
    def name(self):
        """Access the name field."""
        return self._model.name

    @name.setter
    def name(self, value):
        # TODO: Add validation or transformation if needed
        self._model.name = value

    @name.deleter
    def name(self):
        del self._model.name

    @property
    def modules(self):
        """Access the modules field."""
        return self._model.modules

    @modules.setter
    def modules(self, value):
        # TODO: Add validation or transformation if needed
        self._model.modules = value

    @modules.deleter
    def modules(self):
        del self._model.modules
