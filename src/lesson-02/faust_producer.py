import faust
from protobuf.protos.user_pb2 import User
from protobuf.serializers.protobufcodec import ProtobufCodec


user_codec = ProtobufCodec(User)

app = faust.App('myapp_producer', broker='kafka://localhost:9092', web_port=6067)
topic = app.topic('users', value_type=bytes, key_serializer=user_codec, value_serializer=user_codec)


@app.timer(interval=1.0)
async def produce():
    user = User(name='John Doe', age=30, email='john@example.com', interests=['hiking', 'reading'])
    await topic.send(value=user)
    print(f'Sent user: {user.name}, {user.age}, {user.email}, {user.interests}')


if __name__ == '__main__':
    app.main()
