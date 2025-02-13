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

"""Tests for tensorflow_sight."""

import inspect
from typing import Any, Optional, Sequence

import numpy as np
import tensorflow as tf

# from google3.analysis.dremel.core.capacitor.public.python import pywrap_record_reader
from proto import sight_pb2
from py.sight import Sight
from py.widgets.tensorflow_sight import tensorflow_sight
from tensorflow.python.util.protobuf import compare
from absl.testing import absltest


def _read_text_file(file_path: str) -> str:
  read_text = ''
  with open(file_path, encoding='UTF-8') as fp:
    for line in fp:
      read_text += line
  return read_text


def _read_capacitor_file(file_path: str) -> Optional[Any]:
  protos = []
  record_reader = pywrap_record_reader.RecordReader.CreateFromPath(
      file_path, ['*'], 60.0)
  protos.extend(record_reader.IterRecords())
  return sorted(protos, key=lambda x: x.index)


def _create_attributes(sight: Sight) -> Sequence[sight_pb2.Attribute]:
  attribute = []
  if hasattr(sight, 'change_list_number'):
    attribute.append(
        sight_pb2.Attribute(
            key='change_list_number', value=str(sight.change_list_number)))
  if hasattr(sight, 'citc_snapshot'):
    attribute.append(
        sight_pb2.Attribute(
            key='citc_snapshot', value=str(sight.citc_snapshot)))
  return attribute


def _create_attributes_text(base_attributes: Sequence[sight_pb2.Attribute],
                            sight: Sight) -> str:
  attribute = []
  if hasattr(sight, 'change_list_number'):
    attribute.append(f'change_list_number={sight.change_list_number}')
  if hasattr(sight, 'citc_snapshot'):
    attribute.append(f'citc_snapshot={sight.citc_snapshot}')
  attribute.extend([f'{a.key}={a.value}' for a in base_attributes])
  return ','.join(attribute)


class TensorflowSightTest(absltest.TestCase):

  @classmethod
  def setUpClass(cls):
    super().setUpClass()
    cls.test_path = 'googlex/cortex/sight/py/widgets/tensorflow_sight/tensorflow_sight_test.py'

  def testLogFloatArrayToText(self):
    # SETUP
    params = sight_pb2.Params()
    params.label = 'testLogFloatArrayToText'
    params.log_owner = 'mdb/x-pitchfork'
    params.local = True
    params.text_output = True
    params.log_dir_path = self.create_tempdir().full_path

    # ACT
    with Sight(params) as sight:
      with tensorflow_sight.TfModelApplication('Model Application', sight):
        tensorflow_sight.log(
            'tensor',
            tf.convert_to_tensor(
                np.array([[1, 2.2, 3.333], [4.1, 5, 6.2]], dtype=np.float32)),
            sight)

      # ASSERT
      block_attrs = '| ' + _create_attributes_text([], sight)
    expected_log = """Model Application<<<%s
Model Application>>>%s
""" % (block_attrs, block_attrs)
    actual_log = _read_text_file(params.log_dir_path +
                                 '/testLogFloatArrayToText.txt')
    self.assertEqual(
        expected_log, actual_log,
        'Target code and generated logs are different. Expected log:\n%s\n'
        'Actual log:\n%s\n' % (expected_log, actual_log))

  def testLogFloatArrayToCapacitorFile(self):
    # SETUP
    params = sight_pb2.Params()
    params.label = 'testLogFloatArrayToCapacitorFile'
    params.log_owner = 'mdb/x-pitchfork'
    params.local = True
    params.capacitor_output = True
    params.log_dir_path = self.create_tempdir().full_path

    # ACT
    frameinfo = inspect.getframeinfo(inspect.currentframe())
    with Sight(params) as sight:
      with tensorflow_sight.TfModelApplication('Model Application', sight):
        tensorflow_sight.log(
            'tensor',
            tf.convert_to_tensor(
                np.array([[1, 2.5, 3], [4, 5.5, 6]], dtype=np.float32)), sight)

    # ASSERT
    expected_log = [
        sight_pb2.Object(
            location='0000000000',
            index=0,
            attribute=_create_attributes(sight),
            file=self.test_path,
            line=frameinfo.lineno + 2,
            func=frameinfo.function,
            ancestor_start_location=['0000000000'],
            sub_type=sight_pb2.Object.ST_BLOCK_START,
            block_start=sight_pb2.BlockStart(
                label='Model Application',
                sub_type=sight_pb2.BlockStart.ST_TENSORFLOW_MODEL_APPLICATION)),
        sight_pb2.Object(
            location='0000000000:0000000000',
            index=1,
            attribute=_create_attributes(sight),
            file=self.test_path,
            line=frameinfo.lineno + 6,
            func=frameinfo.function,
            ancestor_start_location=['0000000000', '0000000000:0000000000'],
            sub_type=sight_pb2.Object.ST_TENSOR,
            tensor=sight_pb2.Tensor(
                sub_type=sight_pb2.Tensor.ST_DOUBLE,
                label='tensor',
                shape=[2, 3],
                double_values=sight_pb2.Tensor.DoubleValues(
                    value=[1, 2.5, 3, 4, 5.5, 6]))),
        sight_pb2.Object(
            location='0000000001',
            index=2,
            attribute=_create_attributes(sight),
            file=self.test_path,
            line=frameinfo.lineno + 6,
            func=frameinfo.function,
            ancestor_start_location=['0000000001'],
            sub_type=sight_pb2.Object.ST_BLOCK_END,
            block_end=sight_pb2.BlockEnd(
                label='Model Application',
                sub_type=sight_pb2.BlockEnd.ST_TENSORFLOW_MODEL_APPLICATION,
                location_of_block_start='0000000000',
                num_direct_contents=1,
                num_transitive_contents=1))
    ]

    actual_log = _read_capacitor_file(
        params.log_dir_path + '/testLogFloatArrayToCapacitorFile.capacitor')

    self.assertEqual(len(expected_log), len(actual_log))
    for i in range(0, len(expected_log)):
      compare.assertProtoEqual(
          self, expected_log[i], actual_log[i],
          'Target code and generated logs are different. Expected log[%d]:\n%s\n'
          'Actual log[%d]:\n%s\n' % (i, expected_log[i], i, actual_log[i]),
          ignored_fields=['line'])

  def testLogIntArrayToCapacitorFile(self):
    # SETUP
    params = sight_pb2.Params()
    params.label = 'testLogIntArrayToCapacitorFile'
    params.log_owner = 'mdb/x-pitchfork'
    params.local = True
    params.capacitor_output = True
    params.log_dir_path = self.create_tempdir().full_path

    # ACT
    frameinfo = inspect.getframeinfo(inspect.currentframe())
    with Sight(params) as sight:
      with tensorflow_sight.TfModelApplication('Model Application', sight):
        tensorflow_sight.log(
            'tensor',
            tf.convert_to_tensor(
                np.array([[1, 2, 3], [4, 5, 6]], dtype=np.int64)), sight)

    # ASSERT
    expected_log = [
        sight_pb2.Object(
            location='0000000000',
            index=0,
            attribute=_create_attributes(sight),
            file=self.test_path,
            line=frameinfo.lineno + 2,
            func=frameinfo.function,
            ancestor_start_location=['0000000000'],
            sub_type=sight_pb2.Object.ST_BLOCK_START,
            block_start=sight_pb2.BlockStart(
                label='Model Application',
                sub_type=sight_pb2.BlockStart.ST_TENSORFLOW_MODEL_APPLICATION)),
        sight_pb2.Object(
            location='0000000000:0000000000',
            index=1,
            attribute=_create_attributes(sight),
            file=self.test_path,
            line=frameinfo.lineno + 6,
            func=frameinfo.function,
            ancestor_start_location=['0000000000', '0000000000:0000000000'],
            sub_type=sight_pb2.Object.ST_TENSOR,
            tensor=sight_pb2.Tensor(
                sub_type=sight_pb2.Tensor.ST_INT64,
                label='tensor',
                shape=[2, 3],
                int64_values=sight_pb2.Tensor.Int64Values(
                    value=[1, 2, 3, 4, 5, 6]))),
        sight_pb2.Object(
            location='0000000001',
            index=2,
            attribute=_create_attributes(sight),
            file=self.test_path,
            line=frameinfo.lineno + 6,
            func=frameinfo.function,
            ancestor_start_location=['0000000001'],
            sub_type=sight_pb2.Object.ST_BLOCK_END,
            block_end=sight_pb2.BlockEnd(
                label='Model Application',
                sub_type=sight_pb2.BlockEnd.ST_TENSORFLOW_MODEL_APPLICATION,
                location_of_block_start='0000000000',
                num_direct_contents=1,
                num_transitive_contents=1))
    ]

    actual_log = _read_capacitor_file(
        params.log_dir_path + '/testLogIntArrayToCapacitorFile.capacitor')

    self.assertEqual(len(expected_log), len(actual_log))
    for i in range(0, len(expected_log)):
      compare.assertProtoEqual(
          self, expected_log[i], actual_log[i],
          'Target code and generated logs are different. Expected log[%d]:\n%s\n'
          'Actual log[%d]:\n%s\n' % (i, expected_log[i], i, actual_log[i]),
          ignored_fields=['line'])


if __name__ == '__main__':
  absltest.main()
