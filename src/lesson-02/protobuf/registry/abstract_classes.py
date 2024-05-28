from abc import ABC, abstractmethod


class SchemaRegistryInterface(ABC):
    @abstractmethod
    def get_latest_schema(self, subject: str):
        pass

    @abstractmethod
    def register_schema(self, subject: str, schema_str: str, schema_type: str):
        pass

    @abstractmethod
    def get_schema(self, subject: str, version: int = None):
        pass

    @abstractmethod
    def get_versions(self, subject: str):
        pass


class SchemaFactoryInterface(ABC):
    @abstractmethod
    def create_serializer(self, subject: str, version: int = None):
        pass

    @abstractmethod
    def create_deserializer(self, subject: str, version: int = None):
        pass

    @abstractmethod
    def create_message_class(self, subject: str, message_name: str = None, version: int = None):
        pass

    @abstractmethod
    def register_schema(self, subject: str, schema_path: str):
        pass


class SchemaFactoryProducerInterface(ABC):
    @abstractmethod
    def get_factory(self, schema_type: str, schema_registry: SchemaRegistryInterface) -> SchemaFactoryInterface:
        pass
