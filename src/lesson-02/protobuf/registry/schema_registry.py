from confluent_kafka.schema_registry import SchemaRegistryClient, Schema
from abstract_classes import SchemaRegistryInterface


class SchemaRegistry(SchemaRegistryInterface):
    def __init__(self, url: str):
        self.client = SchemaRegistryClient({'url': url})

    def get_latest_schema(self, subject: str):
        return self.client.get_latest_version(subject)

    def register_schema(self, subject: str, schema_str: str, schema_type: str):
        schema = Schema(schema_str, schema_type)
        schema_id = self.client.register_schema(subject, schema)
        print(f"Schema registered with ID: {schema_id}")
        return schema_id
