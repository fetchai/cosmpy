# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: ibc/applications/transfer/v1/transfer.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from gogoproto import gogo_pb2 as gogoproto_dot_gogo__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='ibc/applications/transfer/v1/transfer.proto',
  package='ibc.applications.transfer.v1',
  syntax='proto3',
  serialized_options=b'Z7github.com/cosmos/ibc-go/v2/modules/apps/transfer/types',
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n+ibc/applications/transfer/v1/transfer.proto\x12\x1cibc.applications.transfer.v1\x1a\x14gogoproto/gogo.proto\".\n\nDenomTrace\x12\x0c\n\x04path\x18\x01 \x01(\t\x12\x12\n\nbase_denom\x18\x02 \x01(\t\"l\n\x06Params\x12-\n\x0csend_enabled\x18\x01 \x01(\x08\x42\x17\xf2\xde\x1f\x13yaml:\"send_enabled\"\x12\x33\n\x0freceive_enabled\x18\x02 \x01(\x08\x42\x1a\xf2\xde\x1f\x16yaml:\"receive_enabled\"B9Z7github.com/cosmos/ibc-go/v2/modules/apps/transfer/typesb\x06proto3'
  ,
  dependencies=[gogoproto_dot_gogo__pb2.DESCRIPTOR,])




_DENOMTRACE = _descriptor.Descriptor(
  name='DenomTrace',
  full_name='ibc.applications.transfer.v1.DenomTrace',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='path', full_name='ibc.applications.transfer.v1.DenomTrace.path', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='base_denom', full_name='ibc.applications.transfer.v1.DenomTrace.base_denom', index=1,
      number=2, type=9, cpp_type=9, label=1,
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
  serialized_start=99,
  serialized_end=145,
)


_PARAMS = _descriptor.Descriptor(
  name='Params',
  full_name='ibc.applications.transfer.v1.Params',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='send_enabled', full_name='ibc.applications.transfer.v1.Params.send_enabled', index=0,
      number=1, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\362\336\037\023yaml:\"send_enabled\"', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='receive_enabled', full_name='ibc.applications.transfer.v1.Params.receive_enabled', index=1,
      number=2, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\362\336\037\026yaml:\"receive_enabled\"', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
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
  serialized_start=147,
  serialized_end=255,
)

DESCRIPTOR.message_types_by_name['DenomTrace'] = _DENOMTRACE
DESCRIPTOR.message_types_by_name['Params'] = _PARAMS
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

DenomTrace = _reflection.GeneratedProtocolMessageType('DenomTrace', (_message.Message,), {
  'DESCRIPTOR' : _DENOMTRACE,
  '__module__' : 'ibc.applications.transfer.v1.transfer_pb2'
  # @@protoc_insertion_point(class_scope:ibc.applications.transfer.v1.DenomTrace)
  })
_sym_db.RegisterMessage(DenomTrace)

Params = _reflection.GeneratedProtocolMessageType('Params', (_message.Message,), {
  'DESCRIPTOR' : _PARAMS,
  '__module__' : 'ibc.applications.transfer.v1.transfer_pb2'
  # @@protoc_insertion_point(class_scope:ibc.applications.transfer.v1.Params)
  })
_sym_db.RegisterMessage(Params)


DESCRIPTOR._options = None
_PARAMS.fields_by_name['send_enabled']._options = None
_PARAMS.fields_by_name['receive_enabled']._options = None
# @@protoc_insertion_point(module_scope)
