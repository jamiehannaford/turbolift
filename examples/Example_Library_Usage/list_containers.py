# =============================================================================
# Copyright [2015] [Kevin Carter]
# License Information :
# This software has no warranty, it is provided 'as is'. It is your
# responsibility to validate the behavior of the routines and its accuracy
# using the code provided. Consult the GNU General Public license for further
# details (see GNU General Public License).
# http://www.gnu.org/licenses/gpl.html
# =============================================================================

import os
import json


HOME = os.getenv('HOME')


# Set some default args
import turbolift
args = turbolift.ARGS = {
    'os_user': 'YOURUSERNAME',    # Username
    'os_apikey': 'YOURAPIKEY',    # API-Key
    'os_rax_auth': 'YOURREGION',  # RAX Region, must be UPPERCASE
    'error_retry': 5,             # Number of failure retries
    'quiet': True                 # Make the application not print stdout
}


# Load our Logger
from turbolift.logger import logger
log_method = logger.load_in(
    log_level='info',
    log_file='turbolift_library',
    log_location=HOME
)


# Load our constants
turbolift.load_constants(log_method, args)


# Authenticate against the swift API
from turbolift.authentication import auth
authentication = auth.authenticate()


# Package up the Payload
import turbolift.utils.http_utils as http
payload = http.prep_payload(
    auth=auth,
    container=args.get('container'),
    source=args.get('source'),
    args=args
)


# Load all of our available cloud actions
from turbolift.clouderator import actions
cf_actions = actions.CloudActions(payload=payload)


# List Containers
# =============================================================================
kwargs = {
    'url': payload['url']
}
containers, list_count, last_container = cf_actions.container_lister(**kwargs)
print(json.dumps(containers, indent=2))
print('number of containers: [ %s ]' % list_count)
print('Last container in query: [ %s ]' % last_container)
