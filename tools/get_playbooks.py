import os
from pprint import pprint
from airtable import Airtable
import sys
import yaml
from slugify import slugify

base_key = 'appMSqBJzpQCqGq22'
table_name = 'Playbooks'
datafile = "../data/playbooks.yaml"


airtable = Airtable(base_key, table_name, api_key=os.environ['AIRTABLE_API_KEY'])

def _slugify_for_dict_keys(lower_dict):
    upper_dict = {}
    for k, v in lower_dict.items():
        if isinstance(v, dict):
            v = _slugify_for_dict_keys(v)
        k = slugify(k,replacements=[['-', '_']])
        upper_dict[k] = v
    return upper_dict

pages = airtable.get_all(view='Published',)


playbooks = []
for page in pages:

    playbook = page['fields']
    playbook['Organization'] = airtable.get(playbook['Organization'][0] )['fields']

    newPlaybook = _slugify_for_dict_keys(playbook)

    playbooks.append(newPlaybook)


with open(datafile, 'w') as outfile:
    yaml.dump(playbooks, outfile, default_flow_style=False)
    
