# Copyright 2023 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: service/decision/decision.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from sight.proto import sight_pb2 as sight_dot_proto_dot_sight__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1fservice/decision/decision.proto\x12\x18sight.x.service.decision\x1a\x17sight/proto/sight.proto\"\xcd\x01\n\x14\x44\x65\x63isionPointRequest\x12\x11\n\tclient_id\x18\x01 \x01(\t\x12\x11\n\tworker_id\x18\x02 \x01(\t\x12\x18\n\x10suggestion_count\x18\x03 \x01(\x03\x12\x34\n\x0e\x64\x65\x63ision_point\x18\x04 \x01(\x0b\x32\x1c.sight.x.proto.DecisionPoint\x12?\n\x0eoptimizer_type\x18\x05 \x01(\x0e\x32\'.sight.x.service.decision.OptimizerType\"\x96\x01\n\x15\x44\x65\x63isionPointResponse\x12M\n\x07\x61\x63tions\x18\x01 \x03(\x0b\x32<.sight.x.service.decision.DecisionPointResponse.ActionsEntry\x1a.\n\x0c\x41\x63tionsEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\x02:\x02\x38\x01\"\xe1\x01\n\x16\x44\x65\x63isionOutcomeRequest\x12\x38\n\x10\x64\x65\x63ision_outcome\x18\x01 \x01(\x0b\x32\x1e.sight.x.proto.DecisionOutcome\x12\x11\n\tclient_id\x18\x03 \x01(\t\x12\x11\n\tworker_id\x18\x04 \x01(\t\x12\x13\n\x0blast_reward\x18\x05 \x01(\x02\x12?\n\x0eoptimizer_type\x18\x06 \x01(\x0e\x32\'.sight.x.service.decision.OptimizerType\x12\x11\n\tlast_call\x18\x07 \x01(\x08\"/\n\x17\x44\x65\x63isionOutcomeResponse\x12\x14\n\x0cresponse_str\x18\x01 \x01(\t\"\xbd\x01\n\rLaunchRequest\x12I\n\x16\x64\x65\x63ision_config_params\x18\x01 \x01(\x0b\x32).sight.x.proto.DecisionConfigurationStart\x12?\n\x0eoptimizer_type\x18\x02 \x01(\x0e\x32\'.sight.x.service.decision.OptimizerType\x12\r\n\x05label\x18\x03 \x01(\t\x12\x11\n\tclient_id\x18\x04 \x01(\t\"(\n\x0eLaunchResponse\x12\x16\n\x0e\x64isplay_string\x18\x01 \x01(\t\"\r\n\x0bTestRequest\"\x1b\n\x0cTestResponse\x12\x0b\n\x03val\x18\x01 \x01(\t\"\xa9\x01\n\rCreateRequest\x12\x33\n\x06\x66ormat\x18\x01 \x01(\x0e\x32#.sight.x.service.decision.LogFormat\x12\x14\n\x0clog_dir_path\x18\x02 \x01(\t\x12\x11\n\tlog_owner\x18\x03 \x01(\t\x12\r\n\x05label\x18\x04 \x01(\t\x12+\n\tattribute\x18\x05 \x03(\x0b\x32\x18.sight.x.proto.Attribute\"1\n\x0e\x43reateResponse\x12\n\n\x02id\x18\x01 \x01(\x03\x12\x13\n\x0bpath_prefix\x18\x02 \x01(\t*;\n\rOptimizerType\x12\x0e\n\nOT_UNKNOWN\x10\x00\x12\r\n\tOT_VIZIER\x10\x01\x12\x0b\n\x07OT_ACME\x10\x02*[\n\tLogFormat\x12\x0e\n\nLF_UNKNOWN\x10\x00\x12\x0f\n\x0bLF_COLUMNIO\x10\x01\x12\x10\n\x0cLF_CAPACITOR\x10\x02\x12\x0e\n\nLF_SPANNER\x10\x03\x12\x0b\n\x07LF_AVRO\x10\x04\x32\x9f\x04\n\x0cSightService\x12W\n\x04Test\x12%.sight.x.service.decision.TestRequest\x1a&.sight.x.service.decision.TestResponse\"\x00\x12]\n\x06\x43reate\x12\'.sight.x.service.decision.CreateRequest\x1a(.sight.x.service.decision.CreateResponse\"\x00\x12]\n\x06Launch\x12\'.sight.x.service.decision.LaunchRequest\x1a(.sight.x.service.decision.LaunchResponse\"\x00\x12x\n\x13\x44\x65\x63isionPointMethod\x12..sight.x.service.decision.DecisionPointRequest\x1a/.sight.x.service.decision.DecisionPointResponse\"\x00\x12~\n\x15\x44\x65\x63isionOutcomeMethod\x12\x30.sight.x.service.decision.DecisionOutcomeRequest\x1a\x31.sight.x.service.decision.DecisionOutcomeResponse\"\x00\x62\x06proto3')

_OPTIMIZERTYPE = DESCRIPTOR.enum_types_by_name['OptimizerType']
OptimizerType = enum_type_wrapper.EnumTypeWrapper(_OPTIMIZERTYPE)
_LOGFORMAT = DESCRIPTOR.enum_types_by_name['LogFormat']
LogFormat = enum_type_wrapper.EnumTypeWrapper(_LOGFORMAT)
OT_UNKNOWN = 0
OT_VIZIER = 1
OT_ACME = 2
LF_UNKNOWN = 0
LF_COLUMNIO = 1
LF_CAPACITOR = 2
LF_SPANNER = 3
LF_AVRO = 4


_DECISIONPOINTREQUEST = DESCRIPTOR.message_types_by_name['DecisionPointRequest']
_DECISIONPOINTRESPONSE = DESCRIPTOR.message_types_by_name['DecisionPointResponse']
_DECISIONPOINTRESPONSE_ACTIONSENTRY = _DECISIONPOINTRESPONSE.nested_types_by_name['ActionsEntry']
_DECISIONOUTCOMEREQUEST = DESCRIPTOR.message_types_by_name['DecisionOutcomeRequest']
_DECISIONOUTCOMERESPONSE = DESCRIPTOR.message_types_by_name['DecisionOutcomeResponse']
_LAUNCHREQUEST = DESCRIPTOR.message_types_by_name['LaunchRequest']
_LAUNCHRESPONSE = DESCRIPTOR.message_types_by_name['LaunchResponse']
_TESTREQUEST = DESCRIPTOR.message_types_by_name['TestRequest']
_TESTRESPONSE = DESCRIPTOR.message_types_by_name['TestResponse']
_CREATEREQUEST = DESCRIPTOR.message_types_by_name['CreateRequest']
_CREATERESPONSE = DESCRIPTOR.message_types_by_name['CreateResponse']
DecisionPointRequest = _reflection.GeneratedProtocolMessageType('DecisionPointRequest', (_message.Message,), {
  'DESCRIPTOR' : _DECISIONPOINTREQUEST,
  '__module__' : 'service.decision.decision_pb2'
  # @@protoc_insertion_point(class_scope:sight.x.service.decision.DecisionPointRequest)
  })
_sym_db.RegisterMessage(DecisionPointRequest)

DecisionPointResponse = _reflection.GeneratedProtocolMessageType('DecisionPointResponse', (_message.Message,), {

  'ActionsEntry' : _reflection.GeneratedProtocolMessageType('ActionsEntry', (_message.Message,), {
    'DESCRIPTOR' : _DECISIONPOINTRESPONSE_ACTIONSENTRY,
    '__module__' : 'service.decision.decision_pb2'
    # @@protoc_insertion_point(class_scope:sight.x.service.decision.DecisionPointResponse.ActionsEntry)
    })
  ,
  'DESCRIPTOR' : _DECISIONPOINTRESPONSE,
  '__module__' : 'service.decision.decision_pb2'
  # @@protoc_insertion_point(class_scope:sight.x.service.decision.DecisionPointResponse)
  })
_sym_db.RegisterMessage(DecisionPointResponse)
_sym_db.RegisterMessage(DecisionPointResponse.ActionsEntry)

DecisionOutcomeRequest = _reflection.GeneratedProtocolMessageType('DecisionOutcomeRequest', (_message.Message,), {
  'DESCRIPTOR' : _DECISIONOUTCOMEREQUEST,
  '__module__' : 'service.decision.decision_pb2'
  # @@protoc_insertion_point(class_scope:sight.x.service.decision.DecisionOutcomeRequest)
  })
_sym_db.RegisterMessage(DecisionOutcomeRequest)

DecisionOutcomeResponse = _reflection.GeneratedProtocolMessageType('DecisionOutcomeResponse', (_message.Message,), {
  'DESCRIPTOR' : _DECISIONOUTCOMERESPONSE,
  '__module__' : 'service.decision.decision_pb2'
  # @@protoc_insertion_point(class_scope:sight.x.service.decision.DecisionOutcomeResponse)
  })
_sym_db.RegisterMessage(DecisionOutcomeResponse)

LaunchRequest = _reflection.GeneratedProtocolMessageType('LaunchRequest', (_message.Message,), {
  'DESCRIPTOR' : _LAUNCHREQUEST,
  '__module__' : 'service.decision.decision_pb2'
  # @@protoc_insertion_point(class_scope:sight.x.service.decision.LaunchRequest)
  })
_sym_db.RegisterMessage(LaunchRequest)

LaunchResponse = _reflection.GeneratedProtocolMessageType('LaunchResponse', (_message.Message,), {
  'DESCRIPTOR' : _LAUNCHRESPONSE,
  '__module__' : 'service.decision.decision_pb2'
  # @@protoc_insertion_point(class_scope:sight.x.service.decision.LaunchResponse)
  })
_sym_db.RegisterMessage(LaunchResponse)

TestRequest = _reflection.GeneratedProtocolMessageType('TestRequest', (_message.Message,), {
  'DESCRIPTOR' : _TESTREQUEST,
  '__module__' : 'service.decision.decision_pb2'
  # @@protoc_insertion_point(class_scope:sight.x.service.decision.TestRequest)
  })
_sym_db.RegisterMessage(TestRequest)

TestResponse = _reflection.GeneratedProtocolMessageType('TestResponse', (_message.Message,), {
  'DESCRIPTOR' : _TESTRESPONSE,
  '__module__' : 'service.decision.decision_pb2'
  # @@protoc_insertion_point(class_scope:sight.x.service.decision.TestResponse)
  })
_sym_db.RegisterMessage(TestResponse)

CreateRequest = _reflection.GeneratedProtocolMessageType('CreateRequest', (_message.Message,), {
  'DESCRIPTOR' : _CREATEREQUEST,
  '__module__' : 'service.decision.decision_pb2'
  # @@protoc_insertion_point(class_scope:sight.x.service.decision.CreateRequest)
  })
_sym_db.RegisterMessage(CreateRequest)

CreateResponse = _reflection.GeneratedProtocolMessageType('CreateResponse', (_message.Message,), {
  'DESCRIPTOR' : _CREATERESPONSE,
  '__module__' : 'service.decision.decision_pb2'
  # @@protoc_insertion_point(class_scope:sight.x.service.decision.CreateResponse)
  })
_sym_db.RegisterMessage(CreateResponse)

_SIGHTSERVICE = DESCRIPTOR.services_by_name['SightService']
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _DECISIONPOINTRESPONSE_ACTIONSENTRY._options = None
  _DECISIONPOINTRESPONSE_ACTIONSENTRY._serialized_options = b'8\001'
  _OPTIMIZERTYPE._serialized_start=1225
  _OPTIMIZERTYPE._serialized_end=1284
  _LOGFORMAT._serialized_start=1286
  _LOGFORMAT._serialized_end=1377
  _DECISIONPOINTREQUEST._serialized_start=87
  _DECISIONPOINTREQUEST._serialized_end=292
  _DECISIONPOINTRESPONSE._serialized_start=295
  _DECISIONPOINTRESPONSE._serialized_end=445
  _DECISIONPOINTRESPONSE_ACTIONSENTRY._serialized_start=399
  _DECISIONPOINTRESPONSE_ACTIONSENTRY._serialized_end=445
  _DECISIONOUTCOMEREQUEST._serialized_start=448
  _DECISIONOUTCOMEREQUEST._serialized_end=673
  _DECISIONOUTCOMERESPONSE._serialized_start=675
  _DECISIONOUTCOMERESPONSE._serialized_end=722
  _LAUNCHREQUEST._serialized_start=725
  _LAUNCHREQUEST._serialized_end=914
  _LAUNCHRESPONSE._serialized_start=916
  _LAUNCHRESPONSE._serialized_end=956
  _TESTREQUEST._serialized_start=958
  _TESTREQUEST._serialized_end=971
  _TESTRESPONSE._serialized_start=973
  _TESTRESPONSE._serialized_end=1000
  _CREATEREQUEST._serialized_start=1003
  _CREATEREQUEST._serialized_end=1172
  _CREATERESPONSE._serialized_start=1174
  _CREATERESPONSE._serialized_end=1223
  _SIGHTSERVICE._serialized_start=1380
  _SIGHTSERVICE._serialized_end=1923
# @@protoc_insertion_point(module_scope)
