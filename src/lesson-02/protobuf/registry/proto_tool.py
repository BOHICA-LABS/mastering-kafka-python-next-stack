import argparse
import os
from schema_registry import SchemaRegistry
from protobuf_factory import ProtobufFactory


def initialize_schema_registry(url):
    return SchemaRegistry(url)


def register_protobuf_schema(factory, subject, schema_path):
    if not os.path.exists(schema_path):
        raise FileNotFoundError(f"Schema file not found: {schema_path}")
    factory.register_schema(subject, schema_path)


def create_serializer(factory, subject):
    return factory.create_serializer(subject)


def create_deserializer(factory, subject):
    return factory.create_deserializer(subject)


def create_message_class(factory, subject, message_name):
    return factory.create_message_class(subject, message_name)


def main():
    parser = argparse.ArgumentParser(description="Protobuf Factory Script")
    parser.add_argument("--url", type=str, required=True, help="Schema registry URL")
    parser.add_argument("--subject", type=str, required=True, help="Schema subject")
    parser.add_argument("--schema_path", type=str, help="Path to schema file for registration")
    parser.add_argument("--message_name", type=str, help="Message name for creating message class")
    parser.add_argument("--operation", type=str, required=True,
                        choices=["register", "serialize", "deserialize", "create_message"], help="Operation to perform")

    args = parser.parse_args()

    schema_registry = initialize_schema_registry(args.url)
    protobuf_factory = ProtobufFactory(schema_registry)

    if args.operation == "register":
        if not args.schema_path:
            raise ValueError("Schema path is required for registration")
        register_protobuf_schema(protobuf_factory, args.subject, args.schema_path)
        print(f"Schema registered for subject: {args.subject}")

    elif args.operation == "serialize":
        serializer = create_serializer(protobuf_factory, args.subject)
        print(f"Serializer created for subject: {args.subject}")

    elif args.operation == "deserialize":
        deserializer = create_deserializer(protobuf_factory, args.subject)
        print(f"Deserializer created for subject: {args.subject}")

    elif args.operation == "create_message":
        if not args.message_name:
            raise ValueError("Message name is required for creating message class")
        MessageClass = create_message_class(protobuf_factory, args.subject, args.message_name)
        print(f"Message class created for message: {args.message_name}")


if __name__ == "__main__":
    main()


# python proto_tool.py --url "http://localhost:8081" --subject "users" --schema_path "../../../protos/user.proto" --operation register

