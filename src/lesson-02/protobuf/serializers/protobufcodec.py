import faust
from google.protobuf.message import Message
from typing import Any


class ProtobufCodec(faust.Codec):
    def __init__(self, message_type: type, **kwargs: Any):
        super().__init__(**kwargs)
        self.message_type = message_type

    def _dumps(self, obj: Message) -> bytes:
        return obj.SerializeToString()

    def _loads(self, s: bytes) -> Message:
        message = self.message_type()
        message.ParseFromString(s)
        return message
