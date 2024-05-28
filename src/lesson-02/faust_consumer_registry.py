import faust
from protobuf.registry.schema_registry import SchemaRegistry
from protobuf.registry.protobuf_factory import ProtobufFactory
from protobuf.serializers.protobufcodec import ProtobufCodec

schema_registry_url = 'http://localhost:8081'
subject = 'users'
schema_version = 1  # Specify the version of the schema you want to use, or set to None if not using version

schema_registry = SchemaRegistry(schema_registry_url)
protobuf_factory = ProtobufFactory(schema_registry)

# Fetch the User message class from the registry
User = protobuf_factory.create_message_class(subject, 'User', version=schema_version)
user_codec = ProtobufCodec(User, version=schema_version)

app = faust.App('myapp_consumer', broker='kafka://localhost:9092', web_port=6068)
topic = app.topic('users', key_serializer=None, value_serializer=user_codec)

@app.agent(topic)
async def process(users):
    async for user in users:
        print(f'Received user: {user.name}, {user.age}, {user.email}, {user.interests}')

if __name__ == '__main__':
    app.main()
