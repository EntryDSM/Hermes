from abc import ABC, abstractmethod


class AbstractAdapter(ABC):
    @abstractmethod
    def _data_to_entity(self, schema, data):
        ...

    @abstractmethod
    def _entity_to_data(self, schema, entity):
        ...
