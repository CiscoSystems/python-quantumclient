# vim: tabstop=4 shiftwidth=4 softtabstop=4
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.
#

import argparse
import logging

from quantumclient.quantum import v2_0 as quantumv20
from quantumclient.quantum.v2_0 import CreateCommand
from quantumclient.quantum.v2_0 import DeleteCommand
from quantumclient.quantum.v2_0 import ListCommand
from quantumclient.quantum.v2_0 import QuantumCommand
from quantumclient.quantum.v2_0 import ShowCommand


class ListProfile(ListCommand):
    """List profiles that belong to a given tenant."""

    resource = 'profile'
    log = logging.getLogger(__name__ + '.ListProfile')
    _formatters = {}
    list_columns = ['profile_id', 'name', 'profile_type',
                    'segment_type', 'segment_range', 'multicast_ip_range']


class ShowProfile(ShowCommand):
    """Show information of a given profile."""

    resource = 'profile'
    log = logging.getLogger(__name__ + '.ShowProfile')
    allow_names = False


class CreateProfile(CreateCommand):
    """Creates a profile."""

    resource = 'profile'
    log = logging.getLogger(__name__ + '.CreateProfile')

    def add_known_arguments(self, parser):
        parser.add_argument(
            'name',
            help='Name for N1KV Profile')
        parser.add_argument(
            'profile_type',
            choices=['network', 'policy'],
            help='Type of the Profile')
        #parser.add_argument(
        #    '--profile_id',
        #    help='ID for N1KV Profile')
        parser.add_argument(
            '--segment_type',
            help='Type of the segment - VLAN/VXLAN')
        parser.add_argument(
            '--segment_range',
            help='Range for the Segment')
        parser.add_argument(
            '--multicast_ip_range',
            help='Multicast IPv4 Range')

    def args2body(self, parsed_args):
        body = {'profile': {
            'name': parsed_args.name}}

        #if parsed_args.profile_id:
        #    body['profile'].update({'profile_id': parsed_args.profile_id})
        if parsed_args.profile_type:
            body['profile'].update({'profile_type':
                parsed_args.profile_type.lower()})
        if parsed_args.segment_type:
            body['profile'].update({'segment_type': parsed_args.segment_type})
        if parsed_args.segment_range:
            body['profile'].update({'segment_range':
                parsed_args.segment_range})
        if parsed_args.multicast_ip_range:
            body['profile'].update({'multicast_ip_range':
                parsed_args.multicast_ip_range})
        return body


class DeleteProfile(quantumv20.DeleteCommand):
    """Delete a  given profile"""

    log = logging.getLogger(__name__ + '.DeleteProfile')
    resource = 'profile'
    allow_names = False
