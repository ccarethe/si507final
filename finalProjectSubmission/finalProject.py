#####
##### SI 507 Final Project 🥲
##### Name: Christine Carethers
##### Uniqname: ccarethe
##### UMID: 4229 7153
#####

import requests
import json
import os
from textwrap import dedent
from treelib import Node, Tree
import pandas as pd
import plotly.express as px
import webbrowser as wb
from colorama import Fore, Back
import matplotlib.pyplot as plt

# Codes for bolding printed text
boldStart = '\033[1m'
boldEnd = '\033[0m'


class Park():
    '''A standard park item.

    INSTANCE ATTRIBUTES:
        name: str
            Name of national park
        url: str
            URL for national park website
        lat: str
            Latitude point of park location
        long: str
            Longitude point of park location
        activities: list
            List of activities at park
        topics: lit
            List of topics describing park
        state: str
            State park is located in (two-letter abbreviation)
        numVisitors: int
            Number of visitors to park in 2022
        '''

    def __init__(self, name, url, lat, long, activities, topics, state, numVisitors):
        self.name = name
        self.url = url
        self.lat = lat
        self.long = long
        self.activities = [item['name'] for item in activities]
        self.topics = [item['name'] for item in topics]
        self.state = state
        self.numVisitors = numVisitors


def writeJSONFile(filename, data):
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


def readJSONFile(filename):
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

        writeJSONFile('national_parks.json', parkData)
    else:
        parkData = readJSONFile('national_parks.json')
    
    return parkData


def createParks():
    '''Create park objects from info in json file.

    Creates park objects using park information stored in national parks json file.
    
    PARAMETERS:
        None

    RETURNS:
        list
            List of park objects
    
    '''

    # Check if cache with national park data exists
    parkData = checkParksCache()['data']
    visitData = cleanCSV('parkVisitation.csv')

    # Create emply list to store park objects
    parks = []

    # Create park objects from information in national parks json file
    for park in parkData:
        name = park['fullName']
        url = park['url']
        lat = park['latitude']
        long = park['longitude']
        activities = park['activities']
        topics = park['topics']
        state = park['states']
        numVisitors = int(sum(visitData['RecreationVisitors2022'][visitData['Park'] == name]))

        park = Park(name=name, url=url, lat=lat, long=long,
                    activities=activities, topics=topics, state=state, numVisitors=numVisitors)

        parks.append(park)

    # Return list of park objects
    return parks


def cleanCSV(filename):
    '''Read and normalize CSV data to naming scheme of national parks JSON data.
    
    PARAMETERS
        filename: str
            Filename of CSV
    RETURNS
        data: pandas dataframe
            Normalized visitation data
    '''

    # Load CSV file
    data = pd.read_csv(filename)

    # Convert visitor value from str to int
    data['RecreationVisitors2022'] = data['RecreationVisitors2022'].str.replace(',', '').astype(int)

    # Normalize park naming
    data['Park'] = data['Park'].str.replace(' NMP', ' National Military Park')
    data['Park'] = data['Park'].str.replace(' NPRES', ' National Preserve')
    data['Park'] = data['Park'].str.replace(' PKWY', ' Parkway')
    data['Park'] = data['Park'].str.replace(' MEM', ' Memorial')
    data['Park'] = data['Park'].str.replace(' NMEM', ' National Memorial')
    data['Park'] = data['Park'].str.replace(' NM', ' National Monument')
    data['Park'] = data['Park'].str.replace(' NHS', ' National Historic Site')
    data['Park'] = data['Park'].str.replace(' PRES', ' Preserve')
    data['Park'] = data['Park'].str.replace(' NHP', ' National Historical Park')
    data['Park'] = data['Park'].str.replace(' NP', ' National Park')
    data['Park'] = data['Park'].str.replace(' NRRA', ' National River & Recreation Area')
    data['Park'] = data['Park'].str.replace(' NRA', ' National Recreation Area')
    data['Park'] = data['Park'].str.replace(' NRES', ' National Reserve')
    data['Park'] = data['Park'].str.replace(' NR', ' National River')
    data['Park'] = data['Park'].str.replace(' EHP', ' Ecological & Historic Preserve')
    data['Park'] = data['Park'].str.replace(' NBP', ' NB Park')
    data['Park'] = data['Park'].str.replace(' NB', ' National Battlefield')
    data['Park'] = data['Park'].str.replace(' S&RR', ' Scenic & Recreational River')
    data['Park'] = data['Park'].str.replace(' NL', ' National Lakeshore')
    data['Park'] = data['Park'].str.replace(' The R.E.', ', The Robert E.')
    data['Park'] = data['Park'].str.replace(' NSR', ' National Scenic River')
    data['Park'] = data['Park'].str.replace(' NS', ' National Seashore')
    data['Park'] = data['Park'].str.replace('Booker T.', 'Booker T')
    data['Park'] = data['Park'].str.replace('Cesar E. Chavez', 'César E. Chávez')
    data['Park'] = data['Park'].str.replace("Ford's Theatre National Historic Site", "Ford's Theatre")
    data['Park'] = data['Park'].str.replace(" & HS", " and Historic Shrine")
    data['Park'] = data['Park'].str.replace("Haleakala", 'Haleakalā')
    data['Park'] = data['Park'].str.replace("Hawaii", 'Hawaiʻi')
    data['Park'] = data['Park'].str.replace('Franklin D.', 'Franklin D')
    data['Park'] = data['Park'].str.replace('James A.', 'James A')
    data['Park'] = data['Park'].str.replace('Jean Lafitte National Historical Park & Preserve', 'Jean Lafitte National Historical Park and Preserve')
    data['Park'] = data['Park'].str.replace('Kaloko Honokohau', 'Kaloko-Honokōhau')
    data['Park'] = data['Park'].str.replace('Klondike Gold Rush National Historical Park Alaska', 'Klondike Gold Rush National Historical Park')
    data['Park'] = data['Park'].str.replace('Klondike Gold Rush National Historical Park Seattle', 'Klondike Gold Rush - Seattle Unit National Historical Park')
    data['Park'] = data['Park'].str.replace('Lewis & Clark', 'Lewis and Clark')
    data['Park'] = data['Park'].str.replace(' HQ', ' Headquarters')
    data['Park'] = data['Park'].str.replace('Lyndon B.', 'Lyndon B')
    data['Park'] = data['Park'].str.replace('Maggie L.', 'Maggie L')
    data['Park'] = data['Park'].str.replace('Marsh-Billings-Rockefeller', 'Marsh - Billings - Rockefeller')
    data['Park'] = data['Park'].str.replace('Parks East', 'Parks-East')
    data['Park'] = data['Park'].str.replace(' W&SR', ' Wild & Scenic River')
    data['Park'] = data['Park'].str.replace('Ozark National Scenic River', 'Ozark National Scenic Riverways')
    data['Park'] = data['Park'].str.replace('Pennsylvania Avenue National Historic Site', 'Pennsylvania Avenue')
    data['Park'] = data['Park'].str.replace(' Intl.', ' International')
    data['Park'] = data['Park'].str.replace(' W.J.', ' William Jefferson')
    data['Park'] = data['Park'].str.replace("Pu'uhonua o Honaunau", "Puʻuhonua o Hōnaunau")
    data['Park'] = data['Park'].str.replace("Pu'ukohola Heiau", "Puʻukoholā Heiau")
    data['Park'] = data['Park'].str.replace("Redwood National Park", "Redwood National and State Parks")
    data['Park'] = data['Park'].str.replace(" IHS", " International Historic Site")
    data['Park'] = data['Park'].str.replace('Saint Croix National Scenic River', 'Saint Croix National Scenic Riverway')
    data['Park'] = data['Park'].str.replace("Sequoia National Park", 'Sequoia & Kings Canyon National Parks')
    data['Park'] = data['Park'].str.replace('Tumacacori', 'Tumacácori')
    data['Park'] = data['Park'].str.replace('Ulysses S.', 'Ulysses S')
    data['Park'] = data['Park'].str.replace('Wrangell-St. Elias', 'Wrangell - St Elias')
    data['Park'] = data['Park'].str.replace('Yukon-Charley Rivers', 'Yukon - Charley Rivers')
    data['Park'] = data['Park'].str.replace('Black Canyon of the Gunnison National Park', 'Black Canyon Of The Gunnison National Park')
    data['Park'] = data['Park'].str.replace('City of Rocks National Reserve', 'City Of Rocks National Reserve')
    data['Park'] = data['Park'].str.replace('Craters of the Moon National Monument & Preserve', 'Craters Of The Moon National Monument & Preserve')
    data['Park'] = data['Park'].str.replace('Gates of the Arctic National Park & Preserve', 'Gates Of The Arctic National Park & Preserve')
    data['Park'] = data['Park'].str.replace('Home of Franklin D Roosevelt National Historic Site', 'Home Of Franklin D Roosevelt National Historic Site')
    data['Park'] = data['Park'].str.replace('Rosie The Riveter WWII Home Front National Historical Park', 'Rosie the Riveter WWII Home Front National Historical Park')
    data['Park'] = data['Park'].str.replace('Statue of Liberty National Monument', 'Statue Of Liberty National Monument')
    data['Park'] = data['Park'].str.replace('War in the Pacific National Historical Park', 'War In The Pacific National Historical Park')

    return data



def generateMap(parks):
    '''Create map of parks in passed list

    Uses park latitude and longitude points to generate map. Map of parks opens in new window.

    PARAMETERS:
        list
            List of park objects

    RETURNS:
        None

    '''

    # Transform data into pandas dataframe
    df = pd.DataFrame([(park.name, park.lat, park.long) for park in parks], columns=('name', 'latitude', 'longitude'))

    fig = px.scatter_geo(df,
                     lat='latitude',
                     lon='longitude',
                     title='Locations Map',
                     hover_name='name',
                     scope='usa')

    print('\nOpening new window...\n')

    fig.show()


def generateGraph(parks):
    '''Generates bar graph of number of visitors in 2022 by park.
    
    PARAMETERS
        parks: list of park objects
        
    RETURNS
        None
    '''

    # Create lists of park names and corresponding number of visitors
    parkNames = [park.name for park in parks]
    numVisitors = [park.numVisitors for park in parks]

    # Combine categories and values into a list of tuples and sort it
    combined = sorted(zip(parkNames, numVisitors), key=lambda x: x[1], reverse=True)

    # Unzip the sorted tuples
    sortedNames, sortedValues = zip(*combined)

    # Create bar graph
    plt.bar(sortedNames, sortedValues, color='blue')

    plt.xticks(rotation=45, ha='right')
    plt.xlabel('Park Name')
    plt.ylabel('Number of Visitors in 2022')
    plt.title('Number of Vistors in 2022 by Park')

    print('\nGenerating graph in separate window... To continue, exit window with graph.')

    plt.show()


def findParkInState(state, parks):
    '''
    Searches all parks in park list and identifies parks that are located in given state.

    PARAMETERS:
        state: str
            2-letter abbreviation of US state
        parks: list
            List of park objects

    RETURNS:
        parksInState: list
            List of park objects located in selected state'''

    # Create empty list to store valid state options.
    stateList = []

    for park in parks:
        if park.state not in stateList:
            stateList.append(park.state)

    # Prompt user to enter state. Will continue looping until user enters valid state.
    while True:
        if state.upper() not in stateList:
            state = input('\nPlease enter a valid state. Use 2 character state abbreviation. \nIf there are no parks in chosen state, input is considered invalid. ')
        else:
            break

    # Create empty list to store park objects for parks located in state.
    parksInState = []

    # Iterate through all parks - append parks located in given state to parksInState list.
    for park in parks:
        if state.upper() in park.state:
            parksInState.append(park)

    return parksInState


def findParkInTopics(parksInState):
    '''
    Prompts user to choose topics they are interested in, then identifies parks that have
    selected topics.

    PARAMETERS
        parksInState: list
            List of park objects located in state user specified previously.

    RETURNS
        topicChoices: list
            List of topics selected by user
        parksInTopics: list
            List of park objects for parks that have selected topics
    '''

    print("\nWhat topics are you interested in? \nPlease indicate the number(s) for the corresponding topics. If entering more than one number, enter in format '1,2,3'.")

    # Generate list of available topics to choose from
    print(boldStart + '\nHere is a list of available topics.\n' + boldEnd)

    topicList = []
    for park in parksInState:
        for topic in park.topics:
            if topic not in topicList:
                topicList.append(topic)

    # Generate list of valid numbers user can enter
    topicList.sort()
    availableOptions = []

    for i in range(len(topicList)):
        print(f"{i+1}. {topicList[i]}")
        availableOptions.append(i+1)

    availableOptions = list(map(str, availableOptions))

    # Prompt user to select topic(s)
    while True:
        userChoice = input('\nEnter number(s) corresponding to topic(s). ')
        userChoice = userChoice.split(',')

        # Check if user input is valid
        if set(userChoice).issubset(set(availableOptions)):
            break
        else:
            print('\nInput invalid. If entered more than one value, use format "1,2,3".\n')

    # Transform user choices (numbers) into corresponding topics
    topicChoices = [topicList[int(i)-1] for i in userChoice]

    # Generate list of parks that have selected topic(s)
    parksInTopics = []
    for park in parksInState:
        for topic in topicChoices:
            if topic in park.topics and park not in parksInTopics:
                parksInTopics.append(park)

    return topicChoices, parksInTopics


def findParkInActivities(parksInTopics):
    '''
    Prompts user to choose activities they are interested in, then identifies parks that have
    selected activities.

    PARAMETERS
        parksInTopics: list
            List of park objects that have topics user specified previously.

    RETURNS
        activityChoices: list
            List of activities selected by user
        parksInActivities: list
            List of park objects for parks that have selected activities
    '''

    print("\nWhat activities are you interested in? \nPlease indicate the number(s) for the corresponding activities. If entering more than one number, enter in format '1,2,3'.")

    # Generate list of available activities to choose from
    print(boldStart + '\nHere is a list of available activities.\n' + boldEnd)

    activityList = []
    for park in parksInTopics:
        for activity in park.activities:
            if activity not in activityList:
                activityList.append(activity)

    activityList.sort()

    # Generate list of available options (numbers) for user
    availableOptions = []

    for i in range(len(activityList)):
        print(f"{i+1}. {activityList[i]}")
        availableOptions.append(i+1)

    availableOptions = list(map(str, availableOptions))

    # Prompt user for input and check their entered value(s)
    while True:
        userChoice = input('\nEnter number(s) corresponding to activity/activities. ')
        userChoice = userChoice.split(',')

        # If input is invalid, will continue looping
        if set(userChoice).issubset(set(availableOptions)):
            break
        else:
            print('\nInput invalid. If entered more than one value, use format "1,2,3".\n')

    # Generate list of activities that correspond to user activity choices (numbers)
    activityChoices = [activityList[int(i)-1] for i in userChoice]

    # Generate list of parks that have selected activities
    parksInActivities = []
    for park in parksInTopics:
        for activity in activityChoices:
            if activity in park.activities and park not in parksInActivities:
                parksInActivities.append(park)

    return activityChoices, parksInActivities


def checkParkListLength(parkList, precedingParkList, state, choices, tree, lastQuestion=False):
    '''Checks list of resulting parks.

    If the current park list length is equal to zero, will let user know no parks fulfilled their specified criteria.
    Will redirect to user to view result park list (pulled from preceding park list).

    If the park list length is equal to 1, the program will redirect the user to view resulting current park list.

    Else, prompts the user as usual to see if they want to continue the question game (by calling userContinue).

    PARAMETERS
        parkList: list
            List of current parks
        precedingParkList: list
            List of parks generated prior to current list
        state: str
            User selected state
        choices: list
            List of choices user made (topics or activities)
        tree: Tree
            Tree containing questions answered and list of parks generated
        lastQuestion: bool
            Indicates if user is one the last question (activities) or has more questions to go

    RETURNS
        Bool
            Value determined by return value of userContinue
            If user wishes to continue game, will return True
            If user does not wish to continue game or is on the last question, will return False'''

    # If no parks in current list, end game and redirect user to resulting park list (use preceding list)
    if len(parkList) == 0:
        print(f"We're sorry. There are no parks in {state} with choices: {choices}")
        return userContinue(parkList=precedingParkList, parkTree=tree, end=True)
    else: 
        print(boldStart + f'\nHere are parks in state {state} with choices {choices}.\n' + boldEnd)
        printFoundParks(parkList)
        # If only one park in current list, end game and redirect user to resulting park list (use current list)
        if len(parkList) == 1:
            return userContinue(parkList=parkList, parkTree=tree, end=True)
        # Prompt user to continue or quit game
        else:
            return userContinue(parkList=parkList, parkTree=tree, end=lastQuestion)


def printFoundParks(parkList):
    '''Prints parks in parkList in nice format.

    PARAMETERS
        parkList: list
            List of park objects

    RETURNS
        None
    '''

    for i in range(len(parkList)):
        print(f"{i+1}. {parkList[i].name}")


def parkSelection(parks):
    '''Walks user through park selection game.

    First, prompts user to choose state they want to visit.
    Then, user has option to finish game or continue with questions.

    If continuing, user is prompted to select topics they are interested in.
    A list of parks with selected topics is generated.
    User is again asked if they want to continue the game.

    If continuing, user is prompted to select activities they are interested in.
    A list of parks with selected activities is generated.

    User then interacts with resulting park list.

    PARAMETERS
        parks: list
            List of park objects

    RETURNS
        None
    '''

    # parks = createParks()

    print(boldStart + Fore.GREEN + '\nNOW STARTING THE PARK SELECTION GAME! \u2605 \u2605 \u2605' + boldEnd)

    # Prompts user to select state
    state = input('\nWhat state do you want to visit? Use 2 character state abbreviation. ')
    parksInState = findParkInState(state, parks)
    
    # Creates tree to keep track of questions and resulting park lists
    stateNode = Node(tag=f'Select State: {state}')
    stateParksNode = Node(tag=''.join([f"{i+1}. {parksInState[i].name}\n" for i in range(len(parksInState))]))
    tree = Tree()

    tree.add_node(stateNode)
    tree.add_node(stateParksNode, parent=stateNode)

    # List parks in selected state
    print(boldStart + f"\nHere are parks in the state {state}.\n" + boldEnd)
    printFoundParks(parksInState)

    # Check if user wants to continue searching for parks
    if not userContinue(parkList=parksInState, parkTree=tree):
        return

    # Prompt user to select topics and returns list of parks with selected topics
    topicChoices, parksInTopics = findParkInTopics(parksInState)

    # Update tree to keep track of question asked, user response, and resulting park list
    topicNode = Node(f"Selected Topics: {topicChoices}")
    # topicParksNode = Node(tag=[park.name for park in parksInTopics])
    topicParksNode = Node(tag=''.join([f"{i+1}. {parksInTopics[i].name}\n" for i in range(len(parksInTopics))]))
    tree.add_node(topicNode, parent=stateParksNode)
    tree.add_node(topicParksNode, parent=topicNode)

    # Check length of park list and whether user wishes to continue game
    if not checkParkListLength(parkList=parksInTopics, precedingParkList=parksInState,
                        state=state, choices=topicChoices, tree=tree):
        return
    
    # Prompt user to select activities and returns list of parks with selected activities
    activityChoices, parksInActivities = findParkInActivities(parksInTopics)

    # Update tree to keep track of question asked, user response, and resulting park list
    activityNode = Node(f"Selected Activities: {activityChoices}")
    activityParksNode = Node(tag=''.join([f"{i+1}. {parksInActivities[i].name}\n" for i in range(len(parksInActivities))]))
    tree.add_node(activityNode, parent=topicParksNode)
    tree.add_node(activityParksNode, parent=activityNode)

    # Check park list and provide user with interactive options
    checkParkListLength(parkList=parksInActivities, precedingParkList=parksInTopics,
                        state=state, choices=activityChoices, tree=tree, lastQuestion=True)


def userContinue(parkList, parkTree, end=False):
    '''
    Presents interactive options for users who do not wish to continue game or are at the end of the game.

    For resulting park list, user can:
    1. Open link for select park from list
    2. Generate map of parks from list
    3. Create bar graph showing number of visitors in 2022 by park
    4. Exit game

    PARAMETERS
        parkList:
            list of park objects
        parkTree: Tree
            Tree containing questions asked and resulting park lists
        end: Bool
            Indicates whether game is over
    '''

    # If there are still questions left, ask user if they wish to continue the game
    if not end:
        userContinue = input('\nWould you like to continue with questions (YES/NO)? ')
        # Loops until user provides valid input
        while userContinue.upper() not in ['YES', 'NO']:
            userContinue = input('Response invalid. Please respond either YES or NO. ')
    # If there are no more questions, user will proceed to interactive options
    else:
        userContinue = 'NO'

    if userContinue.upper() == 'NO':

        # Show user question and park list tree
        print(boldStart + Fore.MAGENTA + '\n\nHere is your park question tree:\n' + boldEnd)
        parkTree.show()

        # Show user final list of parks meeting their criteria
        print(boldStart + Fore.MAGENTA + 'Here are your selected parks:\n' + boldEnd)
        for i in range(len(parkList)):
            print(f"{i+1}. {parkList[i].name}")

        # Show users options to interact with list of parks
        while True:
            print('\n\u2022 If you would like to learn more about a park, enter its number. \n\u2022 If you would like to generate a map of the parks, enter "MAP". \n\u2022 If you would like to create a bar graph showing number of visitors in 2022 by park, enter "BAR". \n\u2022 Else, enter QUIT.\n')
            userInput = input('Enter a value: ')

            # If user entered a number, check if number is valid
            try:
                userInput = int(userInput)
                options = [i+1 for i in range(len(parkList))]
                if userInput not in options:
                    print('\nPlease enter a valid response.')
                    continue
                # If number is valid, open webpage associated with selected park
                else:
                    parkURL = parkList[userInput-1].url
                    print(f'\nLoading {parkURL} in a new window...\n')
                    wb.open(parkURL)
            except:
                if userInput.upper() != 'QUIT' and userInput.upper() != 'BAR' and userInput.upper() != 'MAP':
                    print('\nPlease enter a valid response.\n')
                    continue
                # Generate map of resulting list of parks
                elif userInput.upper() == 'MAP':
                    generateMap(parkList)
                elif userInput.upper() == 'BAR':
                    generateGraph(parkList)
                else:
                    print('\nGoodbye!\n')
                    return False
    return True


def playGame():
    '''Prompts user to play selection game.

    User can choose to:
    1. Generate map of all US parks.
    2. Play park selection game.

    PARAMETERS
        None

    RETURNS
        None
    '''

    # Create list of park objects from national park data
    parks = createParks()

    print(boldStart + Fore.BLACK + Back.WHITE + '\nWELCOME TO THE PARK SELECTION GAME!' + boldEnd)

    while True:
        print(boldStart + Fore.CYAN + "\nYou are on the program's MAIN PAGE." + boldEnd)
        # Prompt user to select "play mode"
        print('\nChoose from the following options:')
        print(dedent('''
                    1. Generate map of all US National Parks.
                    2. Play park selection game.
                    '''))
        userChoice = input('Please enter your selection. Enter "QUIT" to leave the program. ')

        if userChoice.upper() not in ['1', '2', 'QUIT']:
            print('\nPlease enter a valid selection.')
        elif userChoice == '1':
            generateMap(parks)
            print('\nYour map has been generated in a new window.\n')
        elif userChoice == '2':
            parkSelection(parks)

        # Will continue looping until user quits program
        else:
            print("\nGoodbye!\n")
            break


if __name__ == "__main__":

    playGame()

