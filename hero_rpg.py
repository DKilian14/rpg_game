import pickle

def save(map):
    with open('data.pickle','wb') as filehandler:
        pickle.dump(map.actualized_map, filehandler)

class Map:
    def __init__(self, name, size,data):
        self.name = name
        self.size = size
        self.actualized_map = data
        if self.actualized_map == []:
            self.actualized_map = self.createMap()
                  
    def createMap(self):
        map = []
        for i in range(self.size):
            cell = []
            map.append(cell)
            for j in range(self.size):
                cell.append([])
        return map
    
    def seeMap(self):
        for i in range(len(self.actualized_map)):
            print(self.actualized_map[i])
                

#-------------------------------THING CREATION ------------------------------------------------------------------------------------------------------
    def addThing(self):
        
        menu = ['item', 'character']
        
        new_type = input(f'what would you like to add? {menu} ')
        new_name = input(f'Enter name of the new {new_type} you would like to add:  >>')
        new_weight = input(f'Enter weight of the new {new_type}  you would like to add:  >>')
        #New location must be within the range of self.actualized_map. examples <2,2> or <5,1>
        new_location_row, new_location_column = [int(x) for x in input('enter the location of the thing you would like to add: >>').split(',')]
        if new_type == 'item':
            self.addItem(new_name, new_weight, new_location_row, new_location_column)
        elif new_type == 'character':
            self.addCharacter(new_name, new_weight, new_location_row, new_location_column)
            
            ################ ITEM CREATION ###############################################################################
    def addItem(self, new_name, new_weight, new_location_row, new_location_column):
        new_action = input('enter the action that the item has: >>')
        newObj = Item(new_name, new_weight, new_location_row, new_location_column, new_action)
        self.actualized_map[newObj.location_row][newObj.location_column].append([newObj.name, newObj])
        
           ################## CHARACTER CREATION #########################################################################
    def addCharacter(self, new_name, new_weight, new_location_row, new_location_column):
        new_character_type = input("enter the type of character ['NPC', 'PC'] >>")
        new_power = int(input('what is thier power? >>'))
        new_health = int(input('what is thier health? >>'))
        if new_character_type == 'NPC':
            self.addNPC(new_name, new_weight, new_location_row, new_location_column, new_power, new_health)
        elif new_character_type == 'PC':
            self.addPC(new_name, new_weight, new_location_row, new_location_column, new_power, new_health)
        
            #**********************************  NPC CREATION *******************************
    def addNPC(self,new_name, new_weight, new_location_row, new_location_column, new_power, new_health):
        new_alliance = input("what is their alliance ['evil', 'good','neutral'] >>")
        newObj = NPC(new_name, new_weight, new_location_row, new_location_column, new_power, new_health, new_alliance)
        self.actualized_map[newObj.location_row][newObj.location_column].append([newObj.name,newObj])
        
           #**********************************  PC CREATION *********************************
    def addPC(self, new_name, new_weight, new_location_row, new_location_column, new_power, new_health):
        new_items = []
        while True: 
            new_item = input("what items does the PC start with [type 'q' to stop]? >> ")
            if new_item != 'q':
                new_items.append(new_item)
            else: 
                break
        newObj = PC(new_name, new_weight, new_location_row, new_location_column, new_power, new_health, new_items)
        self.actualized_map[newObj.location_row][newObj.location_column].append([newObj.name,newObj])
   
    
#----------------------------GET LIST OF ALL THINGS------------------------------------------------------------------------------------------------------------------
    def getListOfAllThingsInCell(self, the_cell, all_things_in_map):
        for every_thing in the_cell:
            all_things_in_map.append(every_thing[1])
        
    def getListOfAllThings(self):
        all_things_in_map = []
        for every_row in range(len(self.actualized_map)):
            for every_cell in range(len(self.actualized_map[every_row])):
                self.getListOfAllThingsInCell(self.actualized_map[every_row][every_cell], all_things_in_map)      
        return all_things_in_map
    
    ########################## PRINT ALL THINGS ###########################################
    def printAllThings(self):
        all_things_in_map = self.getListOfAllThings()
        for every_item in all_things_in_map:
            print(every_item.__dict__.get('name'), "is at [",  every_item.__dict__.get('location_row'), ", ", every_item.__dict__.get('location_column'),']')
        
    ########################### FIND THING BY NAME #########################################
    def lookUpByName(self):
        all_things = self.getListOfAllThings()
        query= input("Enter the name of the thing >>")
        for i in all_things:
            if i.name == query:
                print(f"{i.name} is at {i.location_row}, {i.location_column}")
                return i        
        
    ########################## DELETE A THING ##############################################
    # *************ISSUE******* if there are any things with the same name, this will delete the first thing with a matching name on the map. This is due to not having unique identifiers. 
    def deleteThing(self, thing):
        
        revised_cell = []
        prev_cell = self.actualized_map[thing.location_row][thing.location_column]
        for i in prev_cell:
            if i[0] != thing.name:
                revised_cell.append(i)
        self.actualized_map[thing.location_row][thing.location_column] = revised_cell
        return thing
    
    
    ######################### MOVE A THING ###################################################
    
    def moveThing(self,thing,row,column):
        thing.location_row = row
        thing.location_column = column
        self.actualized_map[row][column].append([thing.name,thing])
    
    ######################### CHANGE ATTRIBUTE OF THING ######################################
    
    def changeThing(self):
        thing = self.lookUpByName()
        print(thing.__dict__.keys())
        #******************************** will break if someone enters the name or location. Map would need to be deleted. *******
        attribute_to_change = input('what would you like to change? (Do NOT change location or name of thing.)')
        if attribute_to_change in thing.__dict__.keys():
            
            print(thing.__dict__[attribute_to_change])
            if type(thing.__dict__[attribute_to_change]) == type(10):
                thing.__dict__[attribute_to_change] = int(input('change to? >>'))
            elif type(thing.__dict__[attribute_to_change]) == type([]):
                print('cannot change a list of items at this time.')
            else:
                thing.__dict__[attribute_to_change] = input('change to? >>')
        else:
            print('this is not an attribute')

class Thing:
    def __init__(self, name, weight, location_row, location_column):
        self.name = name
        self.weight = weight
        self.location_row = location_row
        self.location_column = location_column
        
class Item(Thing):          #Child of Thing
    def __init__(self, name, weight,location_row, location_column, action):
        self.action = action
        super(Item, self).__init__(name, weight, location_row, location_column)
    
class Character(Thing):     #Child of Thing
    def __init__(self, name, weight, location_row, location_column, power, health):
        self.power = power
        self.health = health
        super(Character, self).__init__(name, weight, location_row, location_column)
    
class PC(Character):        #Child of Character
    def __init__(self, name, weight, location_row, location_column, power, health, items):
        self.items = items
        super(PC, self).__init__(name, weight, location_row, location_column, power, health)
    
class NPC(Character):       #Child of Character
    def __init__(self, name, weight, location_row, location_column, power, health, alliance):
        self.alliance = alliance
        super(NPC, self).__init__(name, weight, location_row, location_column, power, health)
        
#----------------  MENUS  ---------------------------------------------------

def displayCreationMenu():
    creation_menu = ['add thing', 'see map', 'quit','delete map', 'find thing','delete thing', 'list all things in map', 'Move a thing', 'change a thing']
    for i in range(len(creation_menu)):
        print(i+1, creation_menu[i])
    user_choice = int(input("what would you like to do? "))
    return user_choice

def displayInGameMenu(character, map):
    room = map.actualized_map[character.location_row][character.location_column]
    menu = determineInGameMenu(room)# decide if the menu should be changed based on the room the PC is in. 
    
    for i in range(len(menu)):
        print(i+1, menu[i])
    user_choice = int(input("what would you like to do? "))
    return user_choice

#----------------GAMEPLAY FUNCTIONS---------------------------------------------------------------------------
def determineInGameMenu(room):
    menu = ['move', 'check status', 'save and quit']
    for i in room: # iterate through every item in the room
        if type(i[1]).__name__ == 'Item': #if the 'thing' has a class type of 'Item':
            menu.append('Pick Up Item') #add 'pick up item' to the menu.
        if type(i[1]).__name__ == 'NPC':#if the 'thing' has a class type of 'NPC':
            print('Someone is in here with you!!')
            menu.append('Fight!') #add 'fight!' to the menu.
    return menu

def findMainCharacter(map):
    for i in map.getListOfAllThings():
        if type(i).__name__ == 'PC': 
            return i

def move(map):
    character = findMainCharacter(map)
    print(map.seeMap())
    
    direction = int(input("""
        Move which direction?
1. up
2. down
3. left
4. right
            
"""))
    
    if direction == 1:#UP
        
        if character.location_row-1 > 0:
            character = map.deleteThing(character)
            map.moveThing(character, character.location_row-1, character.location_column)
            print(map.seeMap())
        else:
            print("you hit the northern wall")
    if direction == 2:#DOWN
        if character.location_row+1 < map.size:
            character = map.deleteThing(character)
            map.moveThing(character, character.location_row+1, character.location_column)
            print(map.seeMap())  
        else:
            print("you hit the southern wall")
    if direction == 3:#LEFT
        if character.location_column-1 >= 0:
            character = map.deleteThing(character)
            map.moveThing(character, character.location_row, character.location_column-1)  
        else:
            print("you hit the western wall")
    if direction == 4:#RIGHT
        if character.location_column+1 < map.size:
            character = map.deleteThing(character)
            map.moveThing(character, character.location_row, character.location_column+1)  
        else:
            print("you hit the eastern wall")
    print()
    print()

    for i in map.actualized_map[character.location_row][character.location_column]:
        print(f"You have a {i} in the room. ")
        
    
    



def play(map):
    
    main_character = findMainCharacter(map)
    print(main_character)
    
    
    while True:
        user_choice = displayInGameMenu(main_character, map)
        if user_choice == 1:
            move(map)
        if user_choice == 2:
            pass
        if user_choice == 3:
            save(map)
            print('Game saved. thank you for playing!')
            break
    
    

################## STARTS THE CREATION MENU. 
def main():
    print("welcome to the game creator! Here, you can manipulate the game map before playing.")
    
    mordor = Map('mordor', 5, data)
    
    while True: 
        print("""
    ****** CREATION MENU *******
              """)
        user_choice = displayCreationMenu()
        
        if user_choice == 1: 
            mordor.addThing()
        elif user_choice == 2:
            mordor.seeMap()
        elif user_choice == 3:
            print('goodbye')
            save(mordor)
            break
        elif user_choice == 4:
            mordor.actualized_map = mordor.createMap()
        elif user_choice == 5:
            mordor.lookUpByName()
        elif user_choice == 6:
            print("*Delete Thing*")
            thing = mordor.lookUpByName()
            mordor.deleteThing(thing)
        elif user_choice == 7:
            mordor.printAllThings()
        elif user_choice == 8:
            mordor.printAllThings()
            thing = mordor.lookUpByName()
            mordor.deleteThing(thing)
            row, column = [int(x) for x in input('enter the location of the thing you would like to add: >>').split(',')]
            mordor.moveThing(thing,row,column)
        elif user_choice == 9:
            mordor.changeThing()
        

    print(f'Welcome to Mordor!!')

    play(mordor)

        
try:
    with open('data.pickle', 'rb') as filehandler:
        data = pickle.load(filehandler)
except:
    data = []
    
        
main()