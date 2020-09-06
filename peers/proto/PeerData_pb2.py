# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: PeerData.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='PeerData.proto',
  package='',
  syntax='proto3',
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x0ePeerData.proto\"K\n\x04Peer\x12\x12\n\naccountId1\x18\x01 \x01(\x05\x12\x12\n\naccountId2\x18\x02 \x01(\x05\x12\x0c\n\x04wins\x18\x03 \x01(\x05\x12\r\n\x05loses\x18\x04 \x01(\x05\"7\n\x07\x41vatars\x12\r\n\x05small\x18\x01 \x01(\t\x12\x0e\n\x06medium\x18\x02 \x01(\t\x12\r\n\x05large\x18\x03 \x01(\t\"\"\n\rPlayerRequest\x12\x11\n\taccountId\x18\x01 \x01(\x05\"\xf0\x01\n\x0ePlayerResponse\x12\x11\n\taccountId\x18\x01 \x01(\x05\x12\x10\n\x08username\x18\x02 \x01(\t\x12\x0c\n\x04rank\x18\x03 \x01(\x05\x12\x10\n\x08\x64otaPlus\x18\x04 \x01(\x08\x12\x0f\n\x07steamId\x18\x05 \x01(\t\x12\x19\n\x07\x61vatars\x18\x06 \x01(\x0b\x32\x08.Avatars\x12\x12\n\nprofileUrl\x18\x07 \x01(\t\x12\x13\n\x0b\x63ountryCode\x18\x08 \x01(\t\x12\x0c\n\x04wins\x18\t \x01(\x05\x12\r\n\x05loses\x18\n \x01(\x05\x12\x14\n\x05peers\x18\x0b \x03(\x0b\x32\x05.Peer\x12\x11\n\ttimestamp\x18\x0c \x01(\x03\"?\n\x0fPeerDataRequest\x12\x0b\n\x03key\x18\x01 \x01(\x03\x12\x1f\n\x07players\x18\x02 \x03(\x0b\x32\x0e.PlayerRequest\"A\n\x10PeerDataResponse\x12\x0b\n\x03key\x18\x01 \x01(\x03\x12 \n\x07players\x18\x02 \x03(\x0b\x32\x0f.PlayerResponseb\x06proto3'
)




_PEER = _descriptor.Descriptor(
  name='Peer',
  full_name='Peer',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='accountId1', full_name='Peer.accountId1', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='accountId2', full_name='Peer.accountId2', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='wins', full_name='Peer.wins', index=2,
      number=3, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='loses', full_name='Peer.loses', index=3,
      number=4, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=18,
  serialized_end=93,
)


_AVATARS = _descriptor.Descriptor(
  name='Avatars',
  full_name='Avatars',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='small', full_name='Avatars.small', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='medium', full_name='Avatars.medium', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='large', full_name='Avatars.large', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=95,
  serialized_end=150,
)


_PLAYERREQUEST = _descriptor.Descriptor(
  name='PlayerRequest',
  full_name='PlayerRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='accountId', full_name='PlayerRequest.accountId', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=152,
  serialized_end=186,
)


_PLAYERRESPONSE = _descriptor.Descriptor(
  name='PlayerResponse',
  full_name='PlayerResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='accountId', full_name='PlayerResponse.accountId', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='username', full_name='PlayerResponse.username', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='rank', full_name='PlayerResponse.rank', index=2,
      number=3, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='dotaPlus', full_name='PlayerResponse.dotaPlus', index=3,
      number=4, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='steamId', full_name='PlayerResponse.steamId', index=4,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='avatars', full_name='PlayerResponse.avatars', index=5,
      number=6, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='profileUrl', full_name='PlayerResponse.profileUrl', index=6,
      number=7, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='countryCode', full_name='PlayerResponse.countryCode', index=7,
      number=8, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='wins', full_name='PlayerResponse.wins', index=8,
      number=9, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='loses', full_name='PlayerResponse.loses', index=9,
      number=10, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='peers', full_name='PlayerResponse.peers', index=10,
      number=11, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='timestamp', full_name='PlayerResponse.timestamp', index=11,
      number=12, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=189,
  serialized_end=429,
)


_PEERDATAREQUEST = _descriptor.Descriptor(
  name='PeerDataRequest',
  full_name='PeerDataRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='key', full_name='PeerDataRequest.key', index=0,
      number=1, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='players', full_name='PeerDataRequest.players', index=1,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=431,
  serialized_end=494,
)


_PEERDATARESPONSE = _descriptor.Descriptor(
  name='PeerDataResponse',
  full_name='PeerDataResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='key', full_name='PeerDataResponse.key', index=0,
      number=1, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='players', full_name='PeerDataResponse.players', index=1,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=496,
  serialized_end=561,
)

_PLAYERRESPONSE.fields_by_name['avatars'].message_type = _AVATARS
_PLAYERRESPONSE.fields_by_name['peers'].message_type = _PEER
_PEERDATAREQUEST.fields_by_name['players'].message_type = _PLAYERREQUEST
_PEERDATARESPONSE.fields_by_name['players'].message_type = _PLAYERRESPONSE
DESCRIPTOR.message_types_by_name['Peer'] = _PEER
DESCRIPTOR.message_types_by_name['Avatars'] = _AVATARS
DESCRIPTOR.message_types_by_name['PlayerRequest'] = _PLAYERREQUEST
DESCRIPTOR.message_types_by_name['PlayerResponse'] = _PLAYERRESPONSE
DESCRIPTOR.message_types_by_name['PeerDataRequest'] = _PEERDATAREQUEST
DESCRIPTOR.message_types_by_name['PeerDataResponse'] = _PEERDATARESPONSE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Peer = _reflection.GeneratedProtocolMessageType('Peer', (_message.Message,), {
  'DESCRIPTOR' : _PEER,
  '__module__' : 'PeerData_pb2'
  # @@protoc_insertion_point(class_scope:Peer)
  })
_sym_db.RegisterMessage(Peer)

Avatars = _reflection.GeneratedProtocolMessageType('Avatars', (_message.Message,), {
  'DESCRIPTOR' : _AVATARS,
  '__module__' : 'PeerData_pb2'
  # @@protoc_insertion_point(class_scope:Avatars)
  })
_sym_db.RegisterMessage(Avatars)

PlayerRequest = _reflection.GeneratedProtocolMessageType('PlayerRequest', (_message.Message,), {
  'DESCRIPTOR' : _PLAYERREQUEST,
  '__module__' : 'PeerData_pb2'
  # @@protoc_insertion_point(class_scope:PlayerRequest)
  })
_sym_db.RegisterMessage(PlayerRequest)

PlayerResponse = _reflection.GeneratedProtocolMessageType('PlayerResponse', (_message.Message,), {
  'DESCRIPTOR' : _PLAYERRESPONSE,
  '__module__' : 'PeerData_pb2'
  # @@protoc_insertion_point(class_scope:PlayerResponse)
  })
_sym_db.RegisterMessage(PlayerResponse)

PeerDataRequest = _reflection.GeneratedProtocolMessageType('PeerDataRequest', (_message.Message,), {
  'DESCRIPTOR' : _PEERDATAREQUEST,
  '__module__' : 'PeerData_pb2'
  # @@protoc_insertion_point(class_scope:PeerDataRequest)
  })
_sym_db.RegisterMessage(PeerDataRequest)

PeerDataResponse = _reflection.GeneratedProtocolMessageType('PeerDataResponse', (_message.Message,), {
  'DESCRIPTOR' : _PEERDATARESPONSE,
  '__module__' : 'PeerData_pb2'
  # @@protoc_insertion_point(class_scope:PeerDataResponse)
  })
_sym_db.RegisterMessage(PeerDataResponse)


# @@protoc_insertion_point(module_scope)