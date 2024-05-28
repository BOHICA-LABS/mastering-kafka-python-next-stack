import os
import tempfile
import importlib.util
from google.protobuf import descriptor_pool, message_factory
from confluent_kafka.schema_registry.protobuf import ProtobufSerializer, ProtobufDeserializer
from .abstract_classes import SchemaFactoryInterface
from .schema_registry import SchemaRegistry


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

    def compile_proto_from_string(self, proto_string):
        with tempfile.TemporaryDirectory() as temp_dir:
            proto_filename = os.path.join(temp_dir, "temp.proto")

            # Write the .proto string to a file
            with open(proto_filename, 'w') as temp_proto_file:
                temp_proto_file.write(proto_string)

            # Determine the path to the protobuf includes
            proto_include = os.path.dirname(os.path.abspath(temp_proto_file.name))

            # Compile the .proto file using protoc
            protoc_command = f"protoc --proto_path={temp_dir} --proto_path={proto_include} --python_out={temp_dir} {proto_filename}"
            os.system(protoc_command)

            # Extract the generated Python module
            py_module_name = "temp_pb2"
            py_module_path = os.path.join(temp_dir, py_module_name + ".py")

            # Load the generated module dynamically
            spec = importlib.util.spec_from_file_location(py_module_name, py_module_path)
            generated_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(generated_module)

            return generated_module

    def create_message_class(self, subject: str, message_name: str = None):
        if subject in self.factories:
            return self.factories[subject].GetPrototype(self.factories[subject].message_types_by_name[message_name])

        schema_response = self.schema_registry.get_latest_schema(subject)
        schema_str = schema_response.schema.schema_str

        # Compile the .proto string and get the generated module
        generated_module = self.compile_proto_from_string(schema_str)

        # Get the message class from the generated module
        message_class = getattr(generated_module, message_name)

        # Create a MessageFactory and store it
        factory = message_factory.MessageFactory(self.pool)
        self.factories[subject] = factory

        return message_class

    def register_schema(self, subject: str, schema_path: str):
        with open(schema_path, 'r') as file:
            schema_str = file.read()
        return self.schema_registry.register_schema(subject, schema_str, 'PROTOBUF')
