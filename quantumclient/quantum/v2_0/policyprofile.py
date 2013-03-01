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
from quantumclient.quantum.v2_0 import ListCommand, ShowCommand, UpdateCommand

RESOURCE = 'policy_profile'


#TODO Add command line help
class ListPolicyProfile(ListCommand):
    """List policy profiles that belong to a given tenant."""

    resource = RESOURCE
    log = logging.getLogger(__name__ + '.ListProfile')
    _formatters = {}
    list_columns = ['id', 'name']


#TODO Add command line help
class ShowPolicyProfile(ShowCommand):
    """Show information of a given policy profile."""

    resource = RESOURCE
    log = logging.getLogger(__name__ + '.ShowProfile')
    allow_names = False

class UpdatePolicyProfile(UpdateCommand):
    """Update policy profile's information."""

    resource = RESOURCE
    log = logging.getLogger(__name__ + '.UpdatePolicyProfile')
