import requests
import json
import os

def writeFile(filename, data):
    '''Write data to file.
    
    PARAMETERS:
    filename (str)
        Name of file to write data to
    data
        Data to be written to filename
    
    RETURNS:
    None
    
    '''

    with open(filename, 'w') as file:
        json.dump(data, file, indent=6)


def readFile(filename):
    '''Read file and save contents.
    
    PARAMETERS:
    filename (str)
        File to be read
    
    RETURNS:
    data (dict)
        Data read from file.
    
    '''

    with open(filename, 'r') as file:
        data = json.load(file)
    
    return data


def checkParksCache():
    '''Checks if cache exists for national parks data.
    
    If cache does not exist, creates new cache from data pulled from national parks API.
    
    PARAMETERS:
    None
    
    RETURNS:
    parkData (dict)
        National parks data
    
    '''

    if not os.path.isfile('national_parks.json'):
        # NATIONAL PARKS
        key = '2GqWtIMHBhEMlAcXnnp1zkbU2QadWavb9ARxdMpc'
        endpoint = 'https://developer.nps.gov/api/v1/parks'
        params = {'api_key': key, 'limit': 471}

        parkData = requests.get(endpoint, params=params).json()

        writeFile('national_parks.json', parkData)
    else:
        parkData = readFile('national_parks.json')
    
    return parkData


class Park():
    '''DESCRIPTION'''

    def __init__(self, name, url, description, lat, long, activities, topics, state, directions, addresses):
        self.name = name
        self.url = url
        self.description = description
        self.latlong = {'lat': lat, 'long': long}
        self.activities = [item['name'] for item in activities]
        self.topics = [item['name'] for item in topics]
        self.state = state
        self.directionsUrl = directions
        self.addresses = addresses



        



if __name__ == "__main__":

    parkData = checkParksCache()['data']
    