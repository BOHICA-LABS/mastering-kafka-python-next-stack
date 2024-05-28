import faust
from protobuf.protos.user_pb2 import User
from protobuf.serializers.protobufcodec import ProtobufCodec
from google.protobuf.message import Message
from typing import Any

user_codec = ProtobufCodec(User)

app = faust.App('myapp_consumer', broker='kafka://localhost:9092', web_port=6068)
topic = app.topic('users', value_type=bytes, key_serializer=user_codec, value_serializer=user_codec)


@app.agent(topic)
async def process(users):
    async for user in users:
        print(f'Received user: {user.name}, {user.age}, {user.email}, {user.interests}')


if __name__ == '__main__':
    app.main()
