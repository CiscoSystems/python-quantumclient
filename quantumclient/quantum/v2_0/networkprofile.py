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
#@author Abhishek Raut, Cisco Systems
#@author Sergey Sudakovich, Cisco Systems

import logging
from quantumclient.quantum.v2_0 import ListCommand, ShowCommand, CreateCommand, DeleteCommand, UpdateCommand, \
                                       QuantumCommand, parse_args_to_dict
from quantumclient.common import exceptions

RESOURCE = 'network_profile'
SEGMENT_TYPE_CHOICES = ['vlan', 'vxlan']


#TODO Finish parameters
class ListNetworkProfile(ListCommand):
    """List network profiles that belong to a given tenant."""

    resource = RESOURCE
    log = logging.getLogger(__name__ + '.ListNetworkProfile')
    _formatters = {}
    list_columns = ['id', 'name', 'segment_type', 'segment_range', 'multicast_ip_index', 'multicast_ip_range']


class ShowNetworkProfile(ShowCommand):
    """Show information of a given network profile."""

    resource = RESOURCE
    log = logging.getLogger(__name__ + '.ShowNetworkProfile')
    allow_names = False


class CreateNetworkProfile(CreateCommand):
    """Creates a network profile."""

    resource = RESOURCE
    log = logging.getLogger(__name__ + '.CreateNetworkProfile')

    def add_known_arguments(self, parser):
        #TODO Change to mutually exclusive groups
        parser.add_argument('name', help='Name for Network Profile')
        parser.add_argument('segment_type', choices=SEGMENT_TYPE_CHOICES, help='Segment type')
        parser.add_argument('--segment_range', help='Range for the Segment')
        parser.add_argument('--multicast_ip_range', help='Multicast IPv4 Range')
        parser.add_argument("--add-tenant", help="Add tenant to the network profile")

    def args2body(self, parsed_args):
        body = {'network_profile': {'name': parsed_args.name}}
        if parsed_args.segment_type:
            body['network_profile'].update({'segment_type': parsed_args.segment_type})
        if parsed_args.segment_range:
            body['network_profile'].update({'segment_range': parsed_args.segment_range})
        if parsed_args.multicast_ip_range:
            body['network_profile'].update({'multicast_ip_range': parsed_args.multicast_ip_range})
        if parsed_args.add_tenant:
            body['network_profile'].update({'add_tenant': parsed_args.add_tenant})
        return body


class DeleteNetworkProfile(DeleteCommand):
    """Delete a given network profile."""

    log = logging.getLogger(__name__ + '.DeleteNetworkProfile')
    resource = RESOURCE
    allow_names = False


class UpdateNetworkProfile(UpdateCommand):
    """Update network profile's information."""

    resource = RESOURCE
    log = logging.getLogger(__name__ + '.UpdateNetworkProfile')

class UpdateNetworkProfileV2(QuantumCommand):

    api = 'network'
    log = logging.getLogger(__name__ + '.UpdateNetworkProfileV2')
    resource = RESOURCE

    def get_parser(self, prog_name):
        parser = super(UpdateNetworkProfileV2, self).get_parser(prog_name)
        parser.add_argument("--remove-tenant", help="Remove tenant from the network profile")
        return parser

    def run(self, parsed_args):
        self.log.debug('run(%s)' % parsed_args)
        quantum_client = self.get_client()
        quantum_client.format = parsed_args.request_format
        data = {self.resource: parse_args_to_dict(parsed_args)}
        if parsed_args.remove_tenant:
            data[self.resource]['remove_tenant'] = parsed_args.remove_tenant
        quantum_client.update_network_profile(parsed_args.id, {self.resource: data})
        print >>self.app.stdout, (
                _('Updated %(resource)s: %(id)s') %
                {'id': parsed_args.id, 'resource': self.resource})
        return
