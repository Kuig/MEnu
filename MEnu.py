import pandas as pd
import datetime as dt
from numpy import random

# -----------------------------------------------------

# MEnu :: A weekly menu planner by Giorgio Presti

# -----------------------------------------------------

__version__ = "1.1.0"

### MAIN VARIABLES ###

settings = pd.DataFrame({'Name_0':['Name_0'],'Name_1':['Name_1'], 'Dedication':['Default']})

portate = pd.DataFrame({'Nome':[],'Contenuto':[]})

piatti = pd.DataFrame({'Nome':[],'Tipo':[], 'Stagione':[], 'Kids':[], 'Giorgio':[]})



### FUNCTIONS ###

# Load data and settings from excel file
# Portate: a list of dish types
# Piatti: a list of all available dishes
def loadData(dbFile = 'Menu.xlsx'):
    portate = pd.read_excel(dbFile, 'Portate')
    piatti = pd.read_excel(dbFile, 'Piatti')
    settings = pd.read_excel(dbFile, 'Settings').set_index('Variable').T
    return [portate, piatti, settings]

# Takes a list of Portate and a flag telling the sampler if it is the case to omit pizza.
# Returns a random Portata and a flag which is true if it is pizza time.
# The special case for pizza is due to my strong belief that at least one pizza a week is necessary, 
# but at the same time my companion strongly belief one pizza a week is enough.
# You can use the pizza type (z) to flag something you just want once a week.
def getPortata(portate = pd.DataFrame({'Nome':[],'Contenuto':[]}), 
             portataPrecedente = pd.DataFrame({'Nome':['no'],'Contenuto':['x']}),
             giaPizzato = False,
             seed = random.default_rng()):
    
    maschera = [(item != 'z' or not giaPizzato) for item in portate.Contenuto.to_list()]
    disponibili = portate[(portate.Nome != portataPrecedente.Nome.to_list()[0]) & maschera]
    r = disponibili.sample(random_state=seed)

    return [r, giaPizzato or r.Contenuto.to_list()[0] == 'z']

# Returns a dish given a list of dishes, the desired Portata, and some constrain
# (season, presence of person_1, presence of person_2, random seed, meal id / counter)
# Also returns the dish that needs to be dropped from the list
def getPiatto(piatti = pd.DataFrame({'Nome':[],'Tipo':[], 'Stagione':[], settings.Name_0[0]:[], settings.Name_1[0]:[]}), 
              portata = pd.DataFrame({'Nome':[],'Contenuto':[]}), 
              stagione = 1, 
              presName0 = 0, 
              presName1 = 0,
              seed = random.default_rng(),
              id = 0):

    portateDaPescare = [*portata.Contenuto.to_list()[0]]

    disponibili = piatti[(piatti.Stagione != -stagione) & 
                         (piatti[settings.Name_0[0]] >= presName0) & 
                         (piatti[settings.Name_1[0]] >= presName1) &
                         (piatti.Cena != -((id % 2)*2-1))]
    
    r = []
    toBeDropped = []

    for t in portateDaPescare:
        sampled = disponibili[disponibili.Tipo == t].sample(random_state=seed)

        if (t == 't' or t == 'p' or t == 'u' or t == 'z'): # TODO - Turn this into list-based, picked from settings sheet in the excel file
            toBeDropped.append(sampled.index[0])

        r.append(sampled.Nome.to_list()[0])
    
    return [r, toBeDropped]

# Returns a random meal from a list of Portate and dishes, considering usual constrain of getPiatto
# (this is basically like calling getPiatto over the result of getPortata)
def getPasto(portate = pd.DataFrame({'Nome':[],'Contenuto':[]}), 
                piatti = pd.DataFrame({'Nome':[],'Tipo':[], 'Stagione':[], settings.Name_0[0]:[], settings.Name_1[0]:[]}),
                portataPrecedente = pd.DataFrame({'Nome':['no'],'Contenuto':['x']}),
                giaPizzato = False,
                stagione = 1, 
                presName0 = 0, 
                presName1 = 0,
                seed = random.default_rng(),
                id = 0):
    
    [p, giaPizzato] = getPortata(portate, portataPrecedente, giaPizzato, seed)
    [r, toBeDropped] = getPiatto(piatti, p, stagione, presName0, presName1, seed, id)

    return [r, p, giaPizzato, toBeDropped]

# Returns a table with the weekly menu
def getWeek(portate = pd.DataFrame({'Nome':[],'Contenuto':[]}), 
            piatti = pd.DataFrame({'Nome':[],'Tipo':[], 'Stagione':[], settings.Name_0[0]:[], settings.Name_1[0]:[]}),
            inputTable = {},
            stagione = -1,
            weekId = 0):
    
    p = pd.DataFrame({'Nome':['no'],'Contenuto':['x']})
    giaPizzato = False

    outputTable = {
        'portata': ['No','No','No','No','No','No','No','No','No','No','No','No','No','No'],
        'piatto': ['','','','','','','','','','','','','','']
    }

    seed = random.default_rng(weekId)

    for port in range(14):
        [r, p, giaPizzato, toBeDropped] = getPasto(portate, piatti, p, giaPizzato, stagione, inputTable['Name_0'][port], inputTable['Name_1'][port], seed, port)
        outputTable['portata'][port] = p.Nome.to_list()[0]
        outputTable['piatto'][port] = ', '.join(r)
        piatti = piatti.drop(toBeDropped, axis='index')

    return outputTable



### STATE VARIABLES ###

labelTable = {
    'name': ['Pranzo','Cena','Pranzo','Cena','Pranzo','Cena','Pranzo','Cena','Pranzo','Cena','Pranzo','Cena','Pranzo','Cena'],
    'day':  ['Lunedì','Lunedì','Martedì','Martedì','Mercoledì','Mercoledì','Giovedì','Giovedì','Venerdì','Venerdì','Sabato','Sabato','Domenica','Domenica']
}

inputTable = {
    'Name_0': [0,1,0,1,0,1,0,1,0,1,1,1,1,1],
    'Name_1': [1,1,0,1,0,1,0,1,0,1,1,1,1,1]
}

# Init with current week number as seed
weekId = dt.date.today().isocalendar()[1]
stagione = 1 if (weekId > 14 and weekId < 43) else -1



### MAIN ###

if __name__ == '__main__':
    [portate, piatti, settings] = loadData(dbFile = 'Menu.xlsx')

    outputTable = getWeek(portate, piatti, inputTable, stagione, weekId)
    
    print('Week ' + str(weekId) + ':')
    
    for e in range(14):
        print(e.__str__().ljust(4) + 
            (labelTable['day'][e] + ' a ' + labelTable['name'][e] + ':').ljust(21) +
            outputTable['portata'][e].ljust(15) +
            outputTable['piatto'][e])