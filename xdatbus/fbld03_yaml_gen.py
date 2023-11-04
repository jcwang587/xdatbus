import yaml


# Function to generate the YAML template file
def yaml_gen(filepath):
    # Define your configuration template with comments
    config_template = {
        '# service_host': 'The host of the service in the format host:port',
        'service_host': 'localhost:8080',

        '# logging_level': 'Logging level. Options: DEBUG, INFO, WARNING, ERROR, CRITICAL',
        'logging_level': 'INFO',

        '# database': 'Database configuration section',
        'database': {
            '# host': 'Database host address',
            'host': 'localhost',

            '# port': 'Database port number',
            'port': 3306,

            '# username': 'Username for the database',
            'username': 'user',

            '# password': 'Password for the database',
            'password': 'pass',
        },

        '# server': 'Server configuration section',
        'server': {
            '# host': 'Server host address',
            'host': '0.0.0.0',

            '# port': 'Server port number',
            'port': 8080,
        }
    }

    with open(filepath, 'w') as file:
        yaml.dump(config_template, file, default_flow_style=False, sort_keys=False)
