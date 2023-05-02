# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: cosmos/base/tendermint/v1beta1/types.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from gogoproto import gogo_pb2 as gogoproto_dot_gogo__pb2
from tendermint.types import types_pb2 as tendermint_dot_types_dot_types__pb2
from tendermint.types import evidence_pb2 as tendermint_dot_types_dot_evidence__pb2
from tendermint.version import types_pb2 as tendermint_dot_version_dot_types__pb2
from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n*cosmos/base/tendermint/v1beta1/types.proto\x12\x1e\x63osmos.base.tendermint.v1beta1\x1a\x14gogoproto/gogo.proto\x1a\x1ctendermint/types/types.proto\x1a\x1ftendermint/types/evidence.proto\x1a\x1etendermint/version/types.proto\x1a\x1fgoogle/protobuf/timestamp.proto\"\xd8\x01\n\x05\x42lock\x12<\n\x06header\x18\x01 \x01(\x0b\x32&.cosmos.base.tendermint.v1beta1.HeaderB\x04\xc8\xde\x1f\x00\x12*\n\x04\x64\x61ta\x18\x02 \x01(\x0b\x32\x16.tendermint.types.DataB\x04\xc8\xde\x1f\x00\x12\x36\n\x08\x65vidence\x18\x03 \x01(\x0b\x32\x1e.tendermint.types.EvidenceListB\x04\xc8\xde\x1f\x00\x12-\n\x0blast_commit\x18\x04 \x01(\x0b\x32\x18.tendermint.types.Commit\"\xb3\x03\n\x06Header\x12\x34\n\x07version\x18\x01 \x01(\x0b\x32\x1d.tendermint.version.ConsensusB\x04\xc8\xde\x1f\x00\x12\x1d\n\x08\x63hain_id\x18\x02 \x01(\tB\x0b\xe2\xde\x1f\x07\x43hainID\x12\x0e\n\x06height\x18\x03 \x01(\x03\x12\x32\n\x04time\x18\x04 \x01(\x0b\x32\x1a.google.protobuf.TimestampB\x08\xc8\xde\x1f\x00\x90\xdf\x1f\x01\x12\x36\n\rlast_block_id\x18\x05 \x01(\x0b\x32\x19.tendermint.types.BlockIDB\x04\xc8\xde\x1f\x00\x12\x18\n\x10last_commit_hash\x18\x06 \x01(\x0c\x12\x11\n\tdata_hash\x18\x07 \x01(\x0c\x12\x17\n\x0fvalidators_hash\x18\x08 \x01(\x0c\x12\x1c\n\x14next_validators_hash\x18\t \x01(\x0c\x12\x16\n\x0e\x63onsensus_hash\x18\n \x01(\x0c\x12\x10\n\x08\x61pp_hash\x18\x0b \x01(\x0c\x12\x19\n\x11last_results_hash\x18\x0c \x01(\x0c\x12\x15\n\revidence_hash\x18\r \x01(\x0c\x12\x18\n\x10proposer_address\x18\x0e \x01(\tB4Z2github.com/cosmos/cosmos-sdk/client/grpc/tmserviceb\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'cosmos.base.tendermint.v1beta1.types_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'Z2github.com/cosmos/cosmos-sdk/client/grpc/tmservice'
  _BLOCK.fields_by_name['header']._options = None
  _BLOCK.fields_by_name['header']._serialized_options = b'\310\336\037\000'
  _BLOCK.fields_by_name['data']._options = None
  _BLOCK.fields_by_name['data']._serialized_options = b'\310\336\037\000'
  _BLOCK.fields_by_name['evidence']._options = None
  _BLOCK.fields_by_name['evidence']._serialized_options = b'\310\336\037\000'
  _HEADER.fields_by_name['version']._options = None
  _HEADER.fields_by_name['version']._serialized_options = b'\310\336\037\000'
  _HEADER.fields_by_name['chain_id']._options = None
  _HEADER.fields_by_name['chain_id']._serialized_options = b'\342\336\037\007ChainID'
  _HEADER.fields_by_name['time']._options = None
  _HEADER.fields_by_name['time']._serialized_options = b'\310\336\037\000\220\337\037\001'
  _HEADER.fields_by_name['last_block_id']._options = None
  _HEADER.fields_by_name['last_block_id']._serialized_options = b'\310\336\037\000'
  _BLOCK._serialized_start=229
  _BLOCK._serialized_end=445
  _HEADER._serialized_start=448
  _HEADER._serialized_end=883
# @@protoc_insertion_point(module_scope)
