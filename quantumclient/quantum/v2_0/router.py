# Copyright 2012 OpenStack LLC.
# All Rights Reserved
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
# vim: tabstop=4 shiftwidth=4 softtabstop=4

import argparse
import logging

from quantumclient.common import utils
from quantumclient.quantum import v2_0 as quantumv20


def _format_external_gateway_info(router):
    try:
        return utils.dumps(router['external_gateway_info'])
    except Exception:
        return ''


class ListRouter(quantumv20.ListCommand):
    """List routers that belong to a given tenant."""

    resource = 'router'
    log = logging.getLogger(__name__ + '.ListRouter')
    _formatters = {'external_gateway_info': _format_external_gateway_info, }
    list_columns = ['id', 'name', 'external_gateway_info']
    pagination_support = True
    sorting_support = True


class ShowRouter(quantumv20.ShowCommand):
    """Show information of a given router."""

    resource = 'router'
    log = logging.getLogger(__name__ + '.ShowRouter')


class CreateRouter(quantumv20.CreateCommand):
    """Create a router for a given tenant."""

    resource = 'router'
    log = logging.getLogger(__name__ + '.CreateRouter')
    _formatters = {'external_gateway_info': _format_external_gateway_info, }

    def add_known_arguments(self, parser):
        parser.add_argument(
            '--admin-state-down',
            dest='admin_state', action='store_false',
            help='Set Admin State Up to false')
        parser.add_argument(
            '--admin_state_down',
            dest='admin_state', action='store_false',
            help=argparse.SUPPRESS)
        parser.add_argument(
            'name', metavar='NAME',
            help='Name of router to create')

    def args2body(self, parsed_args):
        body = {'router': {
            'name': parsed_args.name,
            'admin_state_up': parsed_args.admin_state, }, }
        if parsed_args.tenant_id:
            body['router'].update({'tenant_id': parsed_args.tenant_id})
        return body


class DeleteRouter(quantumv20.DeleteCommand):
    """Delete a given router."""

    log = logging.getLogger(__name__ + '.DeleteRouter')
    resource = 'router'


class UpdateRouter(quantumv20.UpdateCommand):
    """Update router's information."""

    log = logging.getLogger(__name__ + '.UpdateRouter')
    resource = 'router'


class RouterInterfaceCommand(quantumv20.QuantumCommand):
    """Based class to Add/Remove router interface."""

    api = 'network'
    log = logging.getLogger(__name__ + '.AddInterfaceRouter')
    resource = 'router'

    def get_parser(self, prog_name):
        parser = super(RouterInterfaceCommand, self).get_parser(prog_name)
        parser.add_argument(
            'router_id', metavar='router-id',
            help='ID of the router')
        parser.add_argument(
            'subnet_id', metavar='subnet-id',
            help='ID of the internal subnet for the interface')
        return parser


class AddInterfaceRouter(RouterInterfaceCommand):
    """Add an internal network interface to a router."""

    def run(self, parsed_args):
        self.log.debug('run(%s)' % parsed_args)
        quantum_client = self.get_client()
        quantum_client.format = parsed_args.request_format
        #TODO(danwent): handle passing in port-id
        _router_id = quantumv20.find_resourceid_by_name_or_id(
            quantum_client, self.resource, parsed_args.router_id)
        _subnet_id = quantumv20.find_resourceid_by_name_or_id(
            quantum_client, 'subnet', parsed_args.subnet_id)
        quantum_client.add_interface_router(_router_id,
                                            {'subnet_id': _subnet_id})
        #TODO(danwent): print port ID that is added
        print >>self.app.stdout, (
            _('Added interface to router %s') % parsed_args.router_id)


class RemoveInterfaceRouter(RouterInterfaceCommand):
    """Remove an internal network interface from a router."""

    def run(self, parsed_args):
        self.log.debug('run(%s)' % parsed_args)
        quantum_client = self.get_client()
        quantum_client.format = parsed_args.request_format
        #TODO(danwent): handle passing in port-id
        _router_id = quantumv20.find_resourceid_by_name_or_id(
            quantum_client, self.resource, parsed_args.router_id)
        _subnet_id = quantumv20.find_resourceid_by_name_or_id(
            quantum_client, 'subnet', parsed_args.subnet_id)
        quantum_client.remove_interface_router(_router_id,
                                               {'subnet_id': _subnet_id})
        print >>self.app.stdout, (
            _('Removed interface from router %s') % parsed_args.router_id)


class SetGatewayRouter(quantumv20.QuantumCommand):
    """Set the external network gateway for a router."""

    log = logging.getLogger(__name__ + '.SetGatewayRouter')
    api = 'network'
    resource = 'router'

    def get_parser(self, prog_name):
        parser = super(SetGatewayRouter, self).get_parser(prog_name)
        parser.add_argument(
            'router_id', metavar='router-id',
            help='ID of the router')
        parser.add_argument(
            'external_network_id', metavar='external-network-id',
            help='ID of the external network for the gateway')
        parser.add_argument(
            '--disable-snat', action='store_false', dest='enable_snat',
            help='Disable Source NAT on the router gateway')
        return parser

    def run(self, parsed_args):
        self.log.debug('run(%s)' % parsed_args)
        quantum_client = self.get_client()
        quantum_client.format = parsed_args.request_format
        _router_id = quantumv20.find_resourceid_by_name_or_id(
            quantum_client, self.resource, parsed_args.router_id)
        _ext_net_id = quantumv20.find_resourceid_by_name_or_id(
            quantum_client, 'network', parsed_args.external_network_id)
        quantum_client.add_gateway_router(
            _router_id,
            {'network_id': _ext_net_id,
             'enable_snat': parsed_args.enable_snat})
        print >>self.app.stdout, (
            _('Set gateway for router %s') % parsed_args.router_id)


class RemoveGatewayRouter(quantumv20.QuantumCommand):
    """Remove an external network gateway from a router."""

    log = logging.getLogger(__name__ + '.RemoveGatewayRouter')
    api = 'network'
    resource = 'router'

    def get_parser(self, prog_name):
        parser = super(RemoveGatewayRouter, self).get_parser(prog_name)
        parser.add_argument(
            'router_id', metavar='router-id',
            help='ID of the router')
        return parser

    def run(self, parsed_args):
        self.log.debug('run(%s)' % parsed_args)
        quantum_client = self.get_client()
        quantum_client.format = parsed_args.request_format
        _router_id = quantumv20.find_resourceid_by_name_or_id(
            quantum_client, self.resource, parsed_args.router_id)
        quantum_client.remove_gateway_router(_router_id)
        print >>self.app.stdout, (
            _('Removed gateway from router %s') % parsed_args.router_id)
