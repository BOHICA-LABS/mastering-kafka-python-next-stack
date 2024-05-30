import faust
from protobuf.registry.schema_registry import SchemaRegistry
from protobuf.registry.protobuf_factory import ProtobufFactory
from protobuf.serializers.protobufcodec import ProtobufCodec

schema_registry_url = 'http://localhost:8081'
subject = 'users'
schema_version = 1  # Specify the version of the schema you want to use

schema_registry = SchemaRegistry(schema_registry_url)
protobuf_factory = ProtobufFactory(schema_registry)

User = protobuf_factory.create_message_class(subject, 'User', version=schema_version)
user_codec = ProtobufCodec(User)

app = faust.App('myapp_producer', broker='kafka://localhost:9092', web_port=6067)
topic = app.topic('users', value_type=bytes, value_serializer=user_codec)

@app.timer(interval=1.0)
async def produce():
    user = User(name='John Doe', age=30, email='john@example.com', interests=['hiking', 'reading'])
    await topic.send(value=user)
    print(f'Sent user: {user.name}, {user.age}, {user.email}, {user.interests}')

if __name__ == '__main__':
    app.main()
