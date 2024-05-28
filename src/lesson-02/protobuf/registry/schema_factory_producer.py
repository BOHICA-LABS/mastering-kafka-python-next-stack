from abstract_classes import SchemaFactoryProducerInterface, SchemaFactoryInterface, SchemaRegistryInterface
from avro_factory import AvroFactory
from json_schema_factory import JSONSchemaFactory
from protobuf_factory import ProtobufFactory


class SchemaFactoryProducer(SchemaFactoryProducerInterface):
    def get_factory(self, schema_type: str, schema_registry: SchemaRegistryInterface) -> SchemaFactoryInterface:
        if schema_type == 'avro':
            return AvroFactory(schema_registry)
        elif schema_type == 'json':
            return JSONSchemaFactory(schema_registry)
        elif schema_type == 'protobuf':
            return ProtobufFactory(schema_registry)
        else:
            raise ValueError(f"Unsupported schema type: {schema_type}")
