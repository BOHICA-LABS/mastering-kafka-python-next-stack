"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""

import builtins
import collections.abc
import google.protobuf.descriptor
import google.protobuf.internal.containers
import google.protobuf.message
import typing

DESCRIPTOR: google.protobuf.descriptor.FileDescriptor

@typing.final
class User(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    NAME_FIELD_NUMBER: builtins.int
    AGE_FIELD_NUMBER: builtins.int
    EMAIL_FIELD_NUMBER: builtins.int
    INTERESTS_FIELD_NUMBER: builtins.int
    name: builtins.str
    age: builtins.int
    email: builtins.str
    @property
    def interests(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.str]: ...
    def __init__(
        self,
        *,
        name: builtins.str = ...,
        age: builtins.int = ...,
        email: builtins.str = ...,
        interests: collections.abc.Iterable[builtins.str] | None = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["age", b"age", "email", b"email", "interests", b"interests", "name", b"name"]) -> None: ...

global___User = User