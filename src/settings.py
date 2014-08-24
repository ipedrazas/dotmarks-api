

DEBUG = True

# Enable reads (GET), inserts (POST) and DELETE for resources/collections
# (if you omit this line, the API will default to ['GET'] and provide
# read-only access to the endpoint).
RESOURCE_METHODS = ['GET', 'POST', 'DELETE']

# Enable reads (GET), edits (PATCH) and deletes of individual items
# (defaults to read-only item access).
ITEM_METHODS = ['GET', 'PATCH', 'PUT', 'DELETE']

PUBLIC_METHODS = ['GET']
PUBLIC_ITEM_METHODS = ['GET']

# We enable standard client cache directives for all resources exposed by the
# API. We can always override these global settings later.
CACHE_CONTROL = 'max-age=20'
CACHE_EXPIRES = 20

XML = False
# Enable CORS for all domains
X_DOMAINS = "*"
X_HEADERS = "Content-Type, Accept, Authorization, X-Requested-With, " \
    " Access-Control-Request-Headers, Access-Control-Allow-Origin, " \
    " Access-Control-Allow-Credentials, X-HTTP-Method-Override, mozSystem, " \
    " Access-Control-Allow-Methods "


AUTH_FIELD = 'username'

MONGO_QUERY_BLACKLIST = []

# MONGO_HOST = 'localhost'
# MONGO_PORT = 27017

import os
MONGO_HOST = os.environ.get('MONGODB_PORT_27017_TCP_ADDR')
MONGO_PORT = int(os.environ.get('MONGODB_PORT_27017_TCP_PORT'))

# MONGO_USERNAME = 'dmUser'
# MONGO_PASSWORD = 'ZOPa676KL5K5AALlfakjhdf7adfh47r3897gl'
# MONGO_USERNAME = 'ivan'
# MONGO_PASSWORD = 'ivan'


attachments = {
    'schema': {
        'file': {
            'type': 'media'
        },
        'name': {
            'type': 'string'
        },
        'user': {
            'type': 'string'
        }
    }
}

logs = {
    'schema': {
        'user': {
            'type': 'string'
        },
        'source_id': {
            'type': 'string'
        },
        'action': {
            'type': 'string'
        },
        'value': {
            'type': 'string'
        }
    }
}

# TODO: if URL + vtime are in DB, not store

history = {
    'schema': {
        'user': {
            'type': 'string'
        },
        'url': {
            'type': 'string',
            'minlength': 7,
            'required': True,
        },
        'title': {
            'type': 'string'
        },
        'vtime': {
            'type': 'number'
        }
    }
}

dotmarks = {
    'public_methods': ['GET'],
    'public_item_methods': ['GET'],

    'schema': {
        # 'public_methods': ['GET'],
        # 'public_item_methods': ['GET'],
        'url': {
            'type': 'string',
            'minlength': 7,
            'required': True,
            # 'unique': True,
        },
        'title': {
            'type': 'string'
        },
        'username': {
            'type': 'string',
            # 'required': True,
        },
        'tags': {
            'type': 'list'
        },
        'atags': {              # Automatic Tags
            'type': 'list'
        },
        'views': {
            'type': 'integer'
        },
        # To specify where the link comes from
        'source': {
            'type': 'string'
        },
        'star': {
            'type': 'boolean',
            'default': False
        }
    }
}

atags = {
    'schema': {
        'tag': {
            'type': 'string',
            'unique': True,
            'required': True,
        },
        'entries': {
            'type': 'list'
        },
        'keywords': {
            'type': 'list'
        }
    }
}

# The DOMAIN dict explains which resources will be available and how they will
# be accessible to the API consumer.
DOMAIN = {
    'dotmarks': dotmarks,
    'logs': logs,
    'atags': atags,
    'attachments': attachments,
    'history': history,
}
