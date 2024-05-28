from google.protobuf import descriptor_pool, message_factory
from confluent_kafka.schema_registry.protobuf import ProtobufSerializer, ProtobufDeserializer
from abstract_classes import SchemaFactoryInterface
from schema_registry import SchemaRegistry


class ProtobufFactory(SchemaFactoryInterface):
    def __init__(self, schema_registry: SchemaRegistry):
        self.schema_registry = schema_registry
        self.pool = descriptor_pool.Default()
        self.factories = {}

    def create_serializer(self, subject: str):
        schema_response = self.schema_registry.get_latest_schema(subject)
        schema_str = schema_response.schema.schema_str
        return ProtobufSerializer(schema_str, self.schema_registry.client, {'use.deprecated.format': True})

    def create_deserializer(self, subject: str):
        schema_response = self.schema_registry.get_latest_schema(subject)
        schema_str = schema_response.schema.schema_str
        return ProtobufDeserializer(schema_str, self.schema_registry.client)

    def create_message_class(self, subject: str, message_name: str = None):
        if subject in self.factories:
            return self.factories[subject].GetPrototype(self.factories[subject].message_types_by_name[message_name])

        schema_response = self.schema_registry.get_latest_schema(subject)
        file_descriptor = self.pool.AddSerializedFile(schema_response.schema.schema_obj.SerializeToString())
        message_descriptor = file_descriptor.message_types_by_name[message_name]
        factory = message_factory.MessageFactory(self.pool)
        self.factories[subject] = factory
        return factory.GetPrototype(message_descriptor)

    def register_schema(self, subject: str, schema_path: str):
        with open(schema_path, 'r') as file:
            schema_str = file.read()
        return self.schema_registry.register_schema(subject, schema_str, 'PROTOBUF')
