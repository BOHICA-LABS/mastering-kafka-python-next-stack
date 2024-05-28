from confluent_kafka.schema_registry.json_schema import JSONSerializer, JSONDeserializer
from abstract_classes import SchemaFactoryInterface
from schema_registry import SchemaRegistry


class JSONSchemaFactory(SchemaFactoryInterface):
    def __init__(self, schema_registry: SchemaRegistry):
        self.schema_registry = schema_registry

    def create_serializer(self, subject: str):
        schema_response = self.schema_registry.get_latest_schema(subject)
        schema_str = schema_response.schema.schema_str
        return JSONSerializer(schema_str, self.schema_registry.client)

    def create_deserializer(self, subject: str):
        schema_response = self.schema_registry.get_latest_schema(subject)
        schema_str = schema_response.schema.schema_str
        return JSONDeserializer(schema_str, self.schema_registry.client)

    def create_message_class(self, subject: str, message_name: str = None):
        schema_response = self.schema_registry.get_latest_schema(subject)
        return schema_response.schema.schema_str

    def register_schema(self, subject: str, schema_path: str):
        with open(schema_path, 'r') as file:
            schema_str = file.read()
        return self.schema_registry.register_schema(subject, schema_str, 'JSON')
