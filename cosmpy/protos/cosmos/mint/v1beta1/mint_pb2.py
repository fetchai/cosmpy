# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: cosmos/mint/v1beta1/mint.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from gogoproto import gogo_pb2 as gogoproto_dot_gogo__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='cosmos/mint/v1beta1/mint.proto',
  package='cosmos.mint.v1beta1',
  syntax='proto3',
  serialized_options=b'Z)github.com/cosmos/cosmos-sdk/x/mint/types',
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x1e\x63osmos/mint/v1beta1/mint.proto\x12\x13\x63osmos.mint.v1beta1\x1a\x14gogoproto/gogo.proto\"\xb2\x01\n\x06Minter\x12\x41\n\tinflation\x18\x01 \x01(\tB.\xda\xde\x1f&github.com/cosmos/cosmos-sdk/types.Dec\xc8\xde\x1f\x00\x12\x65\n\x11\x61nnual_provisions\x18\x02 \x01(\tBJ\xf2\xde\x1f\x18yaml:\"annual_provisions\"\xda\xde\x1f&github.com/cosmos/cosmos-sdk/types.Dec\xc8\xde\x1f\x00\"\xb8\x01\n\x06Params\x12\x12\n\nmint_denom\x18\x01 \x01(\t\x12_\n\x0einflation_rate\x18\x02 \x01(\tBG\xf2\xde\x1f\x15yaml:\"inflation_rate\"\xda\xde\x1f&github.com/cosmos/cosmos-sdk/types.Dec\xc8\xde\x1f\x00\x12\x33\n\x0f\x62locks_per_year\x18\x06 \x01(\x04\x42\x1a\xf2\xde\x1f\x16yaml:\"blocks_per_year\":\x04\x98\xa0\x1f\x00\x42+Z)github.com/cosmos/cosmos-sdk/x/mint/typesb\x06proto3'
  ,
  dependencies=[gogoproto_dot_gogo__pb2.DESCRIPTOR,])




_MINTER = _descriptor.Descriptor(
  name='Minter',
  full_name='cosmos.mint.v1beta1.Minter',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='inflation', full_name='cosmos.mint.v1beta1.Minter.inflation', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\332\336\037&github.com/cosmos/cosmos-sdk/types.Dec\310\336\037\000', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='annual_provisions', full_name='cosmos.mint.v1beta1.Minter.annual_provisions', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\362\336\037\030yaml:\"annual_provisions\"\332\336\037&github.com/cosmos/cosmos-sdk/types.Dec\310\336\037\000', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
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
  serialized_start=78,
  serialized_end=256,
)


_PARAMS = _descriptor.Descriptor(
  name='Params',
  full_name='cosmos.mint.v1beta1.Params',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='mint_denom', full_name='cosmos.mint.v1beta1.Params.mint_denom', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='inflation_rate', full_name='cosmos.mint.v1beta1.Params.inflation_rate', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\362\336\037\025yaml:\"inflation_rate\"\332\336\037&github.com/cosmos/cosmos-sdk/types.Dec\310\336\037\000', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='blocks_per_year', full_name='cosmos.mint.v1beta1.Params.blocks_per_year', index=2,
      number=6, type=4, cpp_type=4, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\362\336\037\026yaml:\"blocks_per_year\"', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=b'\230\240\037\000',
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=259,
  serialized_end=443,
)

DESCRIPTOR.message_types_by_name['Minter'] = _MINTER
DESCRIPTOR.message_types_by_name['Params'] = _PARAMS
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Minter = _reflection.GeneratedProtocolMessageType('Minter', (_message.Message,), {
  'DESCRIPTOR' : _MINTER,
  '__module__' : 'cosmos.mint.v1beta1.mint_pb2'
  # @@protoc_insertion_point(class_scope:cosmos.mint.v1beta1.Minter)
  })
_sym_db.RegisterMessage(Minter)

Params = _reflection.GeneratedProtocolMessageType('Params', (_message.Message,), {
  'DESCRIPTOR' : _PARAMS,
  '__module__' : 'cosmos.mint.v1beta1.mint_pb2'
  # @@protoc_insertion_point(class_scope:cosmos.mint.v1beta1.Params)
  })
_sym_db.RegisterMessage(Params)


DESCRIPTOR._options = None
_MINTER.fields_by_name['inflation']._options = None
_MINTER.fields_by_name['annual_provisions']._options = None
_PARAMS.fields_by_name['inflation_rate']._options = None
_PARAMS.fields_by_name['blocks_per_year']._options = None
_PARAMS._options = None
# @@protoc_insertion_point(module_scope)
