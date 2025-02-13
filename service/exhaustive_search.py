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

"""Exhaustive search for driving Sight applications."""

from concurrent import futures
import logging
from overrides import overrides
from typing import Any, Dict, List, Tuple

from service import service_pb2
from service.optimizer_instance import param_dict_to_proto
from service.optimizer_instance import OptimizerInstance

_file_name = "exhaustive_search.py"

class ExhaustiveSearch(OptimizerInstance):
  """Exhaustively searches over all the possible values of the action attributes.

  Attributes:
    possible_values: Maps each action attributes to the list of possible values
      of this attribute.
  """

  def __init__(self):
    super().__init__()
    self.next_sample_to_issue = []
    self.active_samples = {}
    self.complete_samples = {}
    self.last_sample = False
    self.sweep_issue_done = False
    self.possible_values = {}
    self.max_reward_sample = {}

  @overrides
  def launch(
      self, request: service_pb2.LaunchRequest
  ) -> service_pb2.LaunchResponse:
    method_name = "launch"
    logging.debug(">>>>  In %s of %s", method_name, _file_name)

    response = super(ExhaustiveSearch, self).launch(request)
    print("self.actions : ", self.actions)
    self.next_sample_to_issue = [0] * len(self.actions)
    print("self.next_sample_to_issue : ", self.next_sample_to_issue)

    self.possible_values = {}
    for i, key in enumerate(sorted(self.actions.keys())):
      logging.info('key=%s' % key)
      if self.actions[key].valid_float_values:
        self.possible_values[key] = list(self.actions[key].valid_float_values)
      else:
        self.possible_values[key] = []
        cur = self.actions[key].min_value
        while cur <= self.actions[key].max_value:
          self.possible_values[key].append(cur)
          cur += self.actions[key].step_size

    logging.info('possible_values=%s', self.possible_values)
    response.display_string = 'Exhaustive Search SUCCESS!'
    logging.debug("<<<<  Out %s of %s", method_name, _file_name)
    return response

  @overrides
  def decision_point(
      self, request: service_pb2.DecisionPointRequest
  ) -> service_pb2.DecisionPointResponse:
    method_name = "decision_point"
    logging.debug(">>>>  In %s of %s", method_name, _file_name)
    logging.info(
        (
            'Running for exhaustive search...., last_sample=%s,'
            ' sweep_issue_done=%s'
        ),
        self.last_sample,
        self.sweep_issue_done,
    )
    logging.info('self.next_sample_to_issue=%s', self.next_sample_to_issue)
    # logging.info('self.possible_values=%s', self.possible_values)

    if self.sweep_issue_done:
      return service_pb2.DecisionPointResponse(action={})

    next_action = {}
    for i, key in enumerate(self.actions):
      next_action[key] = self.possible_values[key][self.next_sample_to_issue[i]]
    self.active_samples[request.worker_id] = {
        'action': next_action,
        'sample': tuple(self.next_sample_to_issue),
    }
    if self.last_sample:
      self.sweep_issue_done = True
    else:
      # Advance next_sample_to_issue
      num_dims_advanced = 0
      keys = sorted(self.actions.keys())
      for i, key in reversed(list(enumerate(keys))):
        logging.info(
            'Advancing i=%s, key=%s, next_sample=%s, possible_values=%s',
            i,
            key,
            self.next_sample_to_issue[i],
            self.possible_values[keys[i]],
        )
        if self.next_sample_to_issue[i] < len(self.possible_values[key]) - 1:
          self.next_sample_to_issue[i] += 1
          break
        else:
          self.next_sample_to_issue[i] = 0
          num_dims_advanced += 1

      self.last_sample = num_dims_advanced == len(self.actions)

    logging.info('next_action=%s', next_action)
    response = service_pb2.DecisionPointResponse()
    response.action.extend(param_dict_to_proto(next_action))
    logging.debug("<<<<  Out %s of %s", method_name, _file_name)
    return response

  @overrides
  def finalize_episode(
      self, request: service_pb2.FinalizeEpisodeRequest
  ) -> service_pb2.FinalizeEpisodeResponse:
    method_name = "finalize_episode"
    logging.debug(">>>>  In %s of %s", method_name, _file_name)
    # logging.info('Running for exhaustive search....')

    # logging.info('FinalizeEpisode complete_samples=%s' % self.complete_samples)
    self.complete_samples[
        tuple(self.active_samples[request.worker_id]['sample'])
    ] = {
        'outcome': request.decision_outcome.outcome_value,
        'action': self.active_samples[request.worker_id]['action'],
    }
    logging.info('FinalizeEpisode complete_samples=%s' % self.complete_samples)

    if(self.max_reward_sample == {} or self.max_reward_sample['outcome'] < request.decision_outcome.outcome_value):
      self.max_reward_sample = {
        'outcome': request.decision_outcome.outcome_value,
        'action': self.active_samples[request.worker_id]['action'],
    }

    del self.active_samples[request.worker_id]
    # logging.info('FinalizeEpisode active_samples=%s' % self.active_samples)
    logging.debug("<<<<  Out %s of %s", method_name, _file_name)
    return service_pb2.FinalizeEpisodeResponse(response_str='Success!')

  @overrides
  def current_status(
      self, request: service_pb2.CurrentStatusRequest
  ) -> service_pb2.CurrentStatusResponse:
    method_name = "current_status"
    logging.debug(">>>>  In %s of %s", method_name, _file_name)
    response = (
        '[ExhaustiveSearch: {"Done" if self.sweep_issue_done else "In'
        ' Progress"}\n'
    )
    response += f'  #active_samples={len(self.active_samples)}\n'
    response += '  completed_samples=\n'
    response += ', '.join(list(self.actions)) + ', outcome\n'

    cur = [0] * len(self.actions)
    # action_keys = list(self.actions.keys())
    keys = sorted(self.actions.keys())
    logging.info('self.complete_samples=%s', self.complete_samples)

    reached_last = False
    while not reached_last:
      logging.info('cur(#%d)=%s', len(cur), cur)
      response += ', '.join(
          [str(self.possible_values[key][cur[i]]) for i, key in enumerate(keys)]
      )
      if tuple(cur) in self.complete_samples:
        response += ', ' + str(self.complete_samples[tuple(cur)]['outcome'])
      else:
        response += ', ?'
      response += '\n'

      # Advance cur, starting from the last dimension and going to the first.
      for i, key in reversed(list(enumerate(keys))):
        logging.info(
            'i=%d, key=%s, cur=%s, self.possible_values[key]=%s',
            i,
            key,
            cur[i],
            self.possible_values[key],
        )
        if cur[i] < len(self.possible_values[key]) - 1:
          cur[i] += 1
          break
        else:
          cur[i] = 0
          if i == 0:
            reached_last = True

    response += ']'
    logging.debug("<<<<  Out %s of %s", method_name, _file_name)
    return service_pb2.CurrentStatusResponse(response_str=response)

  @overrides
  def fetch_optimal_action(
    self, request: service_pb2.FetchOptimalActionRequest
  ) -> service_pb2.FetchOptimalActionResponse:
    method_name = "fetch_optimal_action"
    logging.debug(">>>>  In %s of %s", method_name, _file_name)
    best_action = self.max_reward_sample
    print(" : ", best_action)
    logging.debug("<<<<  Out %s of %s", method_name, _file_name)
    return service_pb2.CurrentStatusResponse(response_str=str(best_action))
