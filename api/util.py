import requests

def _process_simple_request(req_url, error_msg=None, payload=None):
    """
    """
    r = requests.get(req_url, params=payload)
    if(r.status_code != 200 or not r.json()):
        raise Exception(error_msg)
    else:
        return r.json()

def _pythonic_property_name(s):
    """
    This function is used to translate a camel-case property name to an all lowercase
    python-style name separated by underscores instead.

    :param s: A camelCase string
    :returns: A lowercase underscore separated string
              (ie exampleAttrName -> example_attr_name)
    """
    new_name = ''
    for char in s:
        if not char.isdigit() and char.upper() == char:  # character is uppercase
            new_name += '_{0}'.format(char.lower())
        else:
            new_name += char
    return new_name
