# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: cosmwasm/wasm/v1beta1/genesis.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database

# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from arcturus.protos.cosmwasm.wasm.v1beta1 import (
    tx_pb2 as cosmwasm_dot_wasm_dot_v1beta1_dot_tx__pb2,
)
from arcturus.protos.cosmwasm.wasm.v1beta1 import (
    types_pb2 as cosmwasm_dot_wasm_dot_v1beta1_dot_types__pb2,
)
from arcturus.protos.gogoproto import gogo_pb2 as gogoproto_dot_gogo__pb2

DESCRIPTOR = _descriptor.FileDescriptor(
    name="cosmwasm/wasm/v1beta1/genesis.proto",
    package="cosmwasm.wasm.v1beta1",
    syntax="proto3",
    serialized_options=b"Z&github.com/CosmWasm/wasmd/x/wasm/types",
    create_key=_descriptor._internal_create_key,
    serialized_pb=b'\n#cosmwasm/wasm/v1beta1/genesis.proto\x12\x15\x63osmwasm.wasm.v1beta1\x1a\x14gogoproto/gogo.proto\x1a!cosmwasm/wasm/v1beta1/types.proto\x1a\x1e\x63osmwasm/wasm/v1beta1/tx.proto"\xe9\x04\n\x0cGenesisState\x12\x33\n\x06params\x18\x01 \x01(\x0b\x32\x1d.cosmwasm.wasm.v1beta1.ParamsB\x04\xc8\xde\x1f\x00\x12\x43\n\x05\x63odes\x18\x02 \x03(\x0b\x32\x1b.cosmwasm.wasm.v1beta1.CodeB\x17\xc8\xde\x1f\x00\xea\xde\x1f\x0f\x63odes,omitempty\x12O\n\tcontracts\x18\x03 \x03(\x0b\x32\x1f.cosmwasm.wasm.v1beta1.ContractB\x1b\xc8\xde\x1f\x00\xea\xde\x1f\x13\x63ontracts,omitempty\x12O\n\tsequences\x18\x04 \x03(\x0b\x32\x1f.cosmwasm.wasm.v1beta1.SequenceB\x1b\xc8\xde\x1f\x00\xea\xde\x1f\x13sequences,omitempty\x12Y\n\x08gen_msgs\x18\x05 \x03(\x0b\x32+.cosmwasm.wasm.v1beta1.GenesisState.GenMsgsB\x1a\xc8\xde\x1f\x00\xea\xde\x1f\x12gen_msgs,omitempty\x1a\xe1\x01\n\x07GenMsgs\x12\x39\n\nstore_code\x18\x01 \x01(\x0b\x32#.cosmwasm.wasm.v1beta1.MsgStoreCodeH\x00\x12M\n\x14instantiate_contract\x18\x02 \x01(\x0b\x32-.cosmwasm.wasm.v1beta1.MsgInstantiateContractH\x00\x12\x45\n\x10\x65xecute_contract\x18\x03 \x01(\x0b\x32).cosmwasm.wasm.v1beta1.MsgExecuteContractH\x00\x42\x05\n\x03sum"\x81\x01\n\x04\x43ode\x12\x1b\n\x07\x63ode_id\x18\x01 \x01(\x04\x42\n\xe2\xde\x1f\x06\x43odeID\x12\x38\n\tcode_info\x18\x02 \x01(\x0b\x32\x1f.cosmwasm.wasm.v1beta1.CodeInfoB\x04\xc8\xde\x1f\x00\x12\x12\n\ncode_bytes\x18\x03 \x01(\x0c\x12\x0e\n\x06pinned\x18\x04 \x01(\x08"\xa2\x01\n\x08\x43ontract\x12\x18\n\x10\x63ontract_address\x18\x01 \x01(\t\x12@\n\rcontract_info\x18\x02 \x01(\x0b\x32#.cosmwasm.wasm.v1beta1.ContractInfoB\x04\xc8\xde\x1f\x00\x12:\n\x0e\x63ontract_state\x18\x03 \x03(\x0b\x32\x1c.cosmwasm.wasm.v1beta1.ModelB\x04\xc8\xde\x1f\x00"4\n\x08Sequence\x12\x19\n\x06id_key\x18\x01 \x01(\x0c\x42\t\xe2\xde\x1f\x05IDKey\x12\r\n\x05value\x18\x02 \x01(\x04\x42(Z&github.com/CosmWasm/wasmd/x/wasm/typesb\x06proto3',
    dependencies=[
        gogoproto_dot_gogo__pb2.DESCRIPTOR,
        cosmwasm_dot_wasm_dot_v1beta1_dot_types__pb2.DESCRIPTOR,
        cosmwasm_dot_wasm_dot_v1beta1_dot_tx__pb2.DESCRIPTOR,
    ],
)


_GENESISSTATE_GENMSGS = _descriptor.Descriptor(
    name="GenMsgs",
    full_name="cosmwasm.wasm.v1beta1.GenesisState.GenMsgs",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    create_key=_descriptor._internal_create_key,
    fields=[
        _descriptor.FieldDescriptor(
            name="store_code",
            full_name="cosmwasm.wasm.v1beta1.GenesisState.GenMsgs.store_code",
            index=0,
            number=1,
            type=11,
            cpp_type=10,
            label=1,
            has_default_value=False,
            default_value=None,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
            create_key=_descriptor._internal_create_key,
        ),
        _descriptor.FieldDescriptor(
            name="instantiate_contract",
            full_name="cosmwasm.wasm.v1beta1.GenesisState.GenMsgs.instantiate_contract",
            index=1,
            number=2,
            type=11,
            cpp_type=10,
            label=1,
            has_default_value=False,
            default_value=None,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
            create_key=_descriptor._internal_create_key,
        ),
        _descriptor.FieldDescriptor(
            name="execute_contract",
            full_name="cosmwasm.wasm.v1beta1.GenesisState.GenMsgs.execute_contract",
            index=2,
            number=3,
            type=11,
            cpp_type=10,
            label=1,
            has_default_value=False,
            default_value=None,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
            create_key=_descriptor._internal_create_key,
        ),
    ],
    extensions=[],
    nested_types=[],
    enum_types=[],
    serialized_options=None,
    is_extendable=False,
    syntax="proto3",
    extension_ranges=[],
    oneofs=[
        _descriptor.OneofDescriptor(
            name="sum",
            full_name="cosmwasm.wasm.v1beta1.GenesisState.GenMsgs.sum",
            index=0,
            containing_type=None,
            create_key=_descriptor._internal_create_key,
            fields=[],
        ),
    ],
    serialized_start=544,
    serialized_end=769,
)

_GENESISSTATE = _descriptor.Descriptor(
    name="GenesisState",
    full_name="cosmwasm.wasm.v1beta1.GenesisState",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    create_key=_descriptor._internal_create_key,
    fields=[
        _descriptor.FieldDescriptor(
            name="params",
            full_name="cosmwasm.wasm.v1beta1.GenesisState.params",
            index=0,
            number=1,
            type=11,
            cpp_type=10,
            label=1,
            has_default_value=False,
            default_value=None,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=b"\310\336\037\000",
            file=DESCRIPTOR,
            create_key=_descriptor._internal_create_key,
        ),
        _descriptor.FieldDescriptor(
            name="codes",
            full_name="cosmwasm.wasm.v1beta1.GenesisState.codes",
            index=1,
            number=2,
            type=11,
            cpp_type=10,
            label=3,
            has_default_value=False,
            default_value=[],
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=b"\310\336\037\000\352\336\037\017codes,omitempty",
            file=DESCRIPTOR,
            create_key=_descriptor._internal_create_key,
        ),
        _descriptor.FieldDescriptor(
            name="contracts",
            full_name="cosmwasm.wasm.v1beta1.GenesisState.contracts",
            index=2,
            number=3,
            type=11,
            cpp_type=10,
            label=3,
            has_default_value=False,
            default_value=[],
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=b"\310\336\037\000\352\336\037\023contracts,omitempty",
            file=DESCRIPTOR,
            create_key=_descriptor._internal_create_key,
        ),
        _descriptor.FieldDescriptor(
            name="sequences",
            full_name="cosmwasm.wasm.v1beta1.GenesisState.sequences",
            index=3,
            number=4,
            type=11,
            cpp_type=10,
            label=3,
            has_default_value=False,
            default_value=[],
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=b"\310\336\037\000\352\336\037\023sequences,omitempty",
            file=DESCRIPTOR,
            create_key=_descriptor._internal_create_key,
        ),
        _descriptor.FieldDescriptor(
            name="gen_msgs",
            full_name="cosmwasm.wasm.v1beta1.GenesisState.gen_msgs",
            index=4,
            number=5,
            type=11,
            cpp_type=10,
            label=3,
            has_default_value=False,
            default_value=[],
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=b"\310\336\037\000\352\336\037\022gen_msgs,omitempty",
            file=DESCRIPTOR,
            create_key=_descriptor._internal_create_key,
        ),
    ],
    extensions=[],
    nested_types=[
        _GENESISSTATE_GENMSGS,
    ],
    enum_types=[],
    serialized_options=None,
    is_extendable=False,
    syntax="proto3",
    extension_ranges=[],
    oneofs=[],
    serialized_start=152,
    serialized_end=769,
)


_CODE = _descriptor.Descriptor(
    name="Code",
    full_name="cosmwasm.wasm.v1beta1.Code",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    create_key=_descriptor._internal_create_key,
    fields=[
        _descriptor.FieldDescriptor(
            name="code_id",
            full_name="cosmwasm.wasm.v1beta1.Code.code_id",
            index=0,
            number=1,
            type=4,
            cpp_type=4,
            label=1,
            has_default_value=False,
            default_value=0,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=b"\342\336\037\006CodeID",
            file=DESCRIPTOR,
            create_key=_descriptor._internal_create_key,
        ),
        _descriptor.FieldDescriptor(
            name="code_info",
            full_name="cosmwasm.wasm.v1beta1.Code.code_info",
            index=1,
            number=2,
            type=11,
            cpp_type=10,
            label=1,
            has_default_value=False,
            default_value=None,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=b"\310\336\037\000",
            file=DESCRIPTOR,
            create_key=_descriptor._internal_create_key,
        ),
        _descriptor.FieldDescriptor(
            name="code_bytes",
            full_name="cosmwasm.wasm.v1beta1.Code.code_bytes",
            index=2,
            number=3,
            type=12,
            cpp_type=9,
            label=1,
            has_default_value=False,
            default_value=b"",
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
            create_key=_descriptor._internal_create_key,
        ),
        _descriptor.FieldDescriptor(
            name="pinned",
            full_name="cosmwasm.wasm.v1beta1.Code.pinned",
            index=3,
            number=4,
            type=8,
            cpp_type=7,
            label=1,
            has_default_value=False,
            default_value=False,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
            create_key=_descriptor._internal_create_key,
        ),
    ],
    extensions=[],
    nested_types=[],
    enum_types=[],
    serialized_options=None,
    is_extendable=False,
    syntax="proto3",
    extension_ranges=[],
    oneofs=[],
    serialized_start=772,
    serialized_end=901,
)


_CONTRACT = _descriptor.Descriptor(
    name="Contract",
    full_name="cosmwasm.wasm.v1beta1.Contract",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    create_key=_descriptor._internal_create_key,
    fields=[
        _descriptor.FieldDescriptor(
            name="contract_address",
            full_name="cosmwasm.wasm.v1beta1.Contract.contract_address",
            index=0,
            number=1,
            type=9,
            cpp_type=9,
            label=1,
            has_default_value=False,
            default_value=b"".decode("utf-8"),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
            create_key=_descriptor._internal_create_key,
        ),
        _descriptor.FieldDescriptor(
            name="contract_info",
            full_name="cosmwasm.wasm.v1beta1.Contract.contract_info",
            index=1,
            number=2,
            type=11,
            cpp_type=10,
            label=1,
            has_default_value=False,
            default_value=None,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=b"\310\336\037\000",
            file=DESCRIPTOR,
            create_key=_descriptor._internal_create_key,
        ),
        _descriptor.FieldDescriptor(
            name="contract_state",
            full_name="cosmwasm.wasm.v1beta1.Contract.contract_state",
            index=2,
            number=3,
            type=11,
            cpp_type=10,
            label=3,
            has_default_value=False,
            default_value=[],
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=b"\310\336\037\000",
            file=DESCRIPTOR,
            create_key=_descriptor._internal_create_key,
        ),
    ],
    extensions=[],
    nested_types=[],
    enum_types=[],
    serialized_options=None,
    is_extendable=False,
    syntax="proto3",
    extension_ranges=[],
    oneofs=[],
    serialized_start=904,
    serialized_end=1066,
)


_SEQUENCE = _descriptor.Descriptor(
    name="Sequence",
    full_name="cosmwasm.wasm.v1beta1.Sequence",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    create_key=_descriptor._internal_create_key,
    fields=[
        _descriptor.FieldDescriptor(
            name="id_key",
            full_name="cosmwasm.wasm.v1beta1.Sequence.id_key",
            index=0,
            number=1,
            type=12,
            cpp_type=9,
            label=1,
            has_default_value=False,
            default_value=b"",
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=b"\342\336\037\005IDKey",
            file=DESCRIPTOR,
            create_key=_descriptor._internal_create_key,
        ),
        _descriptor.FieldDescriptor(
            name="value",
            full_name="cosmwasm.wasm.v1beta1.Sequence.value",
            index=1,
            number=2,
            type=4,
            cpp_type=4,
            label=1,
            has_default_value=False,
            default_value=0,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
            create_key=_descriptor._internal_create_key,
        ),
    ],
    extensions=[],
    nested_types=[],
    enum_types=[],
    serialized_options=None,
    is_extendable=False,
    syntax="proto3",
    extension_ranges=[],
    oneofs=[],
    serialized_start=1068,
    serialized_end=1120,
)

_GENESISSTATE_GENMSGS.fields_by_name[
    "store_code"
].message_type = cosmwasm_dot_wasm_dot_v1beta1_dot_tx__pb2._MSGSTORECODE
_GENESISSTATE_GENMSGS.fields_by_name[
    "instantiate_contract"
].message_type = cosmwasm_dot_wasm_dot_v1beta1_dot_tx__pb2._MSGINSTANTIATECONTRACT
_GENESISSTATE_GENMSGS.fields_by_name[
    "execute_contract"
].message_type = cosmwasm_dot_wasm_dot_v1beta1_dot_tx__pb2._MSGEXECUTECONTRACT
_GENESISSTATE_GENMSGS.containing_type = _GENESISSTATE
_GENESISSTATE_GENMSGS.oneofs_by_name["sum"].fields.append(
    _GENESISSTATE_GENMSGS.fields_by_name["store_code"]
)
_GENESISSTATE_GENMSGS.fields_by_name[
    "store_code"
].containing_oneof = _GENESISSTATE_GENMSGS.oneofs_by_name["sum"]
_GENESISSTATE_GENMSGS.oneofs_by_name["sum"].fields.append(
    _GENESISSTATE_GENMSGS.fields_by_name["instantiate_contract"]
)
_GENESISSTATE_GENMSGS.fields_by_name[
    "instantiate_contract"
].containing_oneof = _GENESISSTATE_GENMSGS.oneofs_by_name["sum"]
_GENESISSTATE_GENMSGS.oneofs_by_name["sum"].fields.append(
    _GENESISSTATE_GENMSGS.fields_by_name["execute_contract"]
)
_GENESISSTATE_GENMSGS.fields_by_name[
    "execute_contract"
].containing_oneof = _GENESISSTATE_GENMSGS.oneofs_by_name["sum"]
_GENESISSTATE.fields_by_name[
    "params"
].message_type = cosmwasm_dot_wasm_dot_v1beta1_dot_types__pb2._PARAMS
_GENESISSTATE.fields_by_name["codes"].message_type = _CODE
_GENESISSTATE.fields_by_name["contracts"].message_type = _CONTRACT
_GENESISSTATE.fields_by_name["sequences"].message_type = _SEQUENCE
_GENESISSTATE.fields_by_name["gen_msgs"].message_type = _GENESISSTATE_GENMSGS
_CODE.fields_by_name[
    "code_info"
].message_type = cosmwasm_dot_wasm_dot_v1beta1_dot_types__pb2._CODEINFO
_CONTRACT.fields_by_name[
    "contract_info"
].message_type = cosmwasm_dot_wasm_dot_v1beta1_dot_types__pb2._CONTRACTINFO
_CONTRACT.fields_by_name[
    "contract_state"
].message_type = cosmwasm_dot_wasm_dot_v1beta1_dot_types__pb2._MODEL
DESCRIPTOR.message_types_by_name["GenesisState"] = _GENESISSTATE
DESCRIPTOR.message_types_by_name["Code"] = _CODE
DESCRIPTOR.message_types_by_name["Contract"] = _CONTRACT
DESCRIPTOR.message_types_by_name["Sequence"] = _SEQUENCE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

GenesisState = _reflection.GeneratedProtocolMessageType(
    "GenesisState",
    (_message.Message,),
    {
        "GenMsgs": _reflection.GeneratedProtocolMessageType(
            "GenMsgs",
            (_message.Message,),
            {
                "DESCRIPTOR": _GENESISSTATE_GENMSGS,
                "__module__": "cosmwasm.wasm.v1beta1.genesis_pb2"
                # @@protoc_insertion_point(class_scope:cosmwasm.wasm.v1beta1.GenesisState.GenMsgs)
            },
        ),
        "DESCRIPTOR": _GENESISSTATE,
        "__module__": "cosmwasm.wasm.v1beta1.genesis_pb2"
        # @@protoc_insertion_point(class_scope:cosmwasm.wasm.v1beta1.GenesisState)
    },
)
_sym_db.RegisterMessage(GenesisState)
_sym_db.RegisterMessage(GenesisState.GenMsgs)

Code = _reflection.GeneratedProtocolMessageType(
    "Code",
    (_message.Message,),
    {
        "DESCRIPTOR": _CODE,
        "__module__": "cosmwasm.wasm.v1beta1.genesis_pb2"
        # @@protoc_insertion_point(class_scope:cosmwasm.wasm.v1beta1.Code)
    },
)
_sym_db.RegisterMessage(Code)

Contract = _reflection.GeneratedProtocolMessageType(
    "Contract",
    (_message.Message,),
    {
        "DESCRIPTOR": _CONTRACT,
        "__module__": "cosmwasm.wasm.v1beta1.genesis_pb2"
        # @@protoc_insertion_point(class_scope:cosmwasm.wasm.v1beta1.Contract)
    },
)
_sym_db.RegisterMessage(Contract)

Sequence = _reflection.GeneratedProtocolMessageType(
    "Sequence",
    (_message.Message,),
    {
        "DESCRIPTOR": _SEQUENCE,
        "__module__": "cosmwasm.wasm.v1beta1.genesis_pb2"
        # @@protoc_insertion_point(class_scope:cosmwasm.wasm.v1beta1.Sequence)
    },
)
_sym_db.RegisterMessage(Sequence)


DESCRIPTOR._options = None
_GENESISSTATE.fields_by_name["params"]._options = None
_GENESISSTATE.fields_by_name["codes"]._options = None
_GENESISSTATE.fields_by_name["contracts"]._options = None
_GENESISSTATE.fields_by_name["sequences"]._options = None
_GENESISSTATE.fields_by_name["gen_msgs"]._options = None
_CODE.fields_by_name["code_id"]._options = None
_CODE.fields_by_name["code_info"]._options = None
_CONTRACT.fields_by_name["contract_info"]._options = None
_CONTRACT.fields_by_name["contract_state"]._options = None
_SEQUENCE.fields_by_name["id_key"]._options = None
# @@protoc_insertion_point(module_scope)