import json
import os

from dotenv import load_dotenv
import pyairtable
from pyairtable.metadata import (
    get_api_bases,
    get_base_schema,
)


def main():
    api_token = os.getenv("API_TOKEN")
    api = pyairtable.Api(api_token)
    
    data = {
        # this says it's experimental but it seems to work.
        'bases': get_api_bases(api)['bases']
    }

    for base in data['bases']:
        print(f"handling {base['name']=}")
        base['tables'] = get_base_schema(api.get_base(base['id']))['tables']
        for table in base['tables']:
            print(f"\thandling {table['name']=}")
            table['records'] = []
            for record in api.get_table(base['id'], table['name']).all():
                table['records'].append(record)

    with open('data.json', 'w') as outfile:
        json.dump(data, outfile, indent=4)


    pass

if __name__ == "__main__":
    load_dotenv()
    main()