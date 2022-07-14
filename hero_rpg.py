import pickle

# In this simple RPG game, the hero fights the goblin. He has the options to:

# 1. fight goblin
# 2. do nothing - in which case the goblin will attack him anyway
# 3. flee



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
                cell.append([i,j])
        return map
                
                
    def addItem(self, new_name, new_weight, new_location_row, new_location_column):
        new_action = input('enter the action that the item has: >>')
        newObj = Item(new_name, new_weight, new_location_row, new_location_column, new_action)
        self.actualized_map[newObj.location_row][newObj.location_column].append([newObj.name, newObj])
        pass
        
        
        
        
        
        
        
        
        
        
    def addThing(self):
        
        menu = ['item', 'character']
        
        new_type = input(f'what would you like to add? {menu} ')
        new_name = input('Enter name of thing you would like to add:  >>')
        new_weight = input('Enter weight of thing you would like to add:  >>')
        #New location must be within the range of self.actualized_map. examples <2,2> or <5,1>
        new_location_row, new_location_column = [int(x) for x in input('enter the location of the thing you would like to add: >>').split(',')]
        if new_type == 'item':
            self.addItem(new_name, new_weight, new_location_row, new_location_column)
            
        elif new_type == 'character':
            new_character_type = input("enter the type of character ['NPC', 'PC'] >>")
            new_power = int(input('what is thier power? >>'))
            new_health = int(input('what is thier health? >>'))
            
            if new_character_type == 'NPC':
                new_alliance = input("what is their alliance ['evil', 'good','neutral'] >>")
                newObj = NPC(new_name, new_weight, new_location_row, new_location_column, new_power, new_health, new_alliance)
                self.actualized_map[newObj.location_row][newObj.location_column].append([newObj.name,newObj])
                
                
                
            elif new_character_type == 'PC':
                new_items = []
                while True: 
                    new_item = input("what items does the PC start with [type 'q' to stop]? >> ")
                    if new_item != 'q':
                        new_items.append(new_item)
                    else: 
                        break
                newObj = PC(new_name, new_weight, new_location_row, new_location_column, new_power, new_health, new_items)
                self.actualized_map[newObj.location_row][newObj.location_column].append([newObj.name,newObj])
   
    
        
   
   
   
   
    def seeMap(self):
        for i in range(len(self.actualized_map)):
            print(self.actualized_map[i])
    
    
    
    
    
    
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
        
    




def displayCreationMenu():
    creation_menu = ['add thing', 'see map', 'quit']
    for i in range(len(creation_menu)):
        print(i+1, creation_menu[i])
    user_choice = int(input("what would you like to do? "))
    return user_choice



################## RUNS THE GAME
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
            with open('data.pickle','wb') as filehandler:
                pickle.dump(mordor.actualized_map, filehandler)
            break
        
        
        
        
        
        
try:
    with open('data.pickle', 'rb') as filehandler:
        data = pickle.load(filehandler)
except:
    data = []
    
        # mordor.seeMap()
        # mordor.addThing()
        
main()