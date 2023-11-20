import requests
import json

if __name__ == "__main__":
    # NATIONAL PARKS
    key = '2GqWtIMHBhEMlAcXnnp1zkbU2QadWavb9ARxdMpc'
    endpoint = 'https://developer.nps.gov/api/v1/parks'
    params = {'api_key': key, 'limit': 5}

    data = requests.get(endpoint, params=params).json()

    with open('sample_nationalpark.json', 'w') as file:
        json.dump(data, file, indent=6)