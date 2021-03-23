import sys
import json
import os.path
import configparser

# Print colors
class col: # thanks joeld on stackoverflow lol
    OKGREEN = '\033[92m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

# Config settings
configur = configparser.ConfigParser()
configur.read('config.ini')

# Print fail and ok
def failed(msg):
    print(col.FAIL + "✗ " + str(msg) + col.ENDC)
    exit()
def success(msg):
    print(col.OKGREEN + "✓ " + str(msg) + col.ENDC)

# Get command line arguments
arguments = len(sys.argv) - 1
amount = 1;
if (arguments < amount):
    failed("Not enough arguments! >:(\nWrite the name of the file that is in 'data' folder like 'python convert.py sheet.json'")
elif (arguments > amount):
    failed("Too much arguments... :|\nWrite the name of the file that is in 'data' folder like 'python convert.py sheet.json'")

# Shared variables
metaName = configur.get('meta', 'name')
metaVersion = configur.get('meta', 'version')
metaAuthor = configur.get('meta', 'author')

folder = configur.get('options', 'folder') + '/'
file = sys.argv[1]
file = folder + file
xml = [
    '<?xml version="1.0" encoding="utf-8"?>\n',
    '<TextureAtlas imagePath="', '">\n','</TextureAtlas>',
    '<SubTexture name="','" x="','" y="','" width="','" height="','"/>',
    '\t<!-- Created with ' + metaName + ' ' + metaVersion + ' -->\n',
    '\t<!-- Made by ' + metaAuthor + ' -->\n'
]

# Try to find a given file
try:
    # Open JSON file with raw data
    with open(file) as data_raw:
        # Turn JSON to a python object
        data = json.load(data_raw)

        # Header open
        out = xml[0]
        out += xml[1] + data['meta']['image'] + xml[2]
        out += xml[10] + xml[11]

        # Individual frames
        if 'frames' in data:
            frames = data['frames']
            for frame in frames:
                details = frames[frame]['frame']
                # i'm sorry for this line
                out += '\t'+xml[4]+frame+xml[5]+str(details['x'])+xml[6]+str(details['y'])+xml[7]+str(details['w'])+xml[8]+str(details['h'])+xml[9]+'\n'
        else:
            failed("No frames are in the JSON data... :/")

        # Header close
        out += xml[3]
except:
    failed("Couldn't open or find a file :/")

# Getting the file name
fileName = 'sheet.xml'
if (file.endswith('.json')):
    fileName = file[:-5]+'.xml'

# Saving file as xml
if (os.path.exists(fileName)):
    outXml = open(fileName, 'w')
else:
    outXml = open(fileName, 'x')
outXml.write(out)
outXml.close()

# Print xml data
success("File saved as " + fileName)
print("\n" + out)