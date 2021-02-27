import json
import requests
import re
import pathlib
import os

# started thinking I'd do functions, but nope, went BASIC style script
def HitTheAPI():
#       print("Hitting the steam API")
        steamResponse = requests.get("https://api.steampowered.com/ISteamNews/GetNewsForApp/v2/?appid=892970&count=5&maxlength=50")
        if steamResponse.status_code != 200:
                return 0
        return steamResponse.json()

if steam_obj == 0:
        print("Something went wrong with the call")
        quit()

# does the file exist? If so read else create and 0
file = pathlib.Path("steam.check.ver")
if file.exists ():
        versionFile = open('steam.check.ver', 'r')
#       print("oh look a file")
        versionValue = versionFile.readline()
        versionFile.close()
else:
#       print("Ain't no file here")
        versionFile = open('steam.check.ver', 'w')
        versionValue = "0"
        versionFile.write(versionValue)
        versionFile.close()
#Call the API, return the JSON or 0 if the HTTP call is anything but 200 (success)
steam_obj = HitTheAPI()

# uncomment out the below to debug the JSON news formatting
#for x in range(5): //use this to debug the titles
#       print(steam_obj["appnews"]["newsitems"][x]["title"])

newestUpdate = steam_obj["appnews"]["newsitems"][0]["title"]

# newestUpdate = "fuck" //testing the regex

print(newestUpdate) # //debug print
# regex to check if it's numeric, if not bomb out
if not re.search("^(\d+\.)?(\d+\.)?(\*|\d+)$", newestUpdate):
        print("Not a update notification")
        quit()
# passed the regex, check if its an update version then do the thing
if versionValue == newestUpdate:
        print("no update needed")
        quit()

# we are updating the file first so the system will no retry if a server bombs during update. Things will hang and this should just chill and retry the script
versionFile = open('steam.check.ver', 'w')
print("Updating file version")
versionFile.write(newestUpdate)
versionFile.close()
print("We're gonna update")

os.system("sudo systemctl restart valheim.service")
