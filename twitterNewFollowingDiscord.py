import tweepy
import time
import csv
import sys
import os
import random
from dotenv import dotenv_values
from discord_webhook import DiscordWebhook, DiscordEmbed

config = dotenv_values(".env")

# For Twitter: Add the relevant keys, tokens and secrets from your Twitter app made here: https://apps.twitter.com/

client = tweepy.Client(bearer_token=config["bearer_token"])

# Variables - configure the bits below to get your script working. 

style = "1da1f2"   # Colour for the message - default is Twitter Bird blue
randomFooter = ["N'oubliez pas de DYOR !", "Plein de love.", "Bonne journée !", "Cordialement !", "(ɔ◔‿◔)ɔ ♥"]

# Discord incoming webhook URL

webhook = DiscordWebhook(url=config["discord_webhook"], username="Twitter Following")

# Database

pathDatabase = os.path.dirname(os.path.realpath(__file__)) + "/database.csv"

# Init
database = dict()
author = dict()
content = dict()
csvHeading = ["idTweeter","lastSuscribings"]
newFollowings = False

# Read CSV file to know get the following list and then update it.

try:
    fileDatabase = open(pathDatabase, 'r+')
    if (os.path.getsize(pathDatabase) == 0):
        print("Please fill the database before launching the program.")
        fileDatabase.close()
        sys.exit()
    else:
        reader = csv.DictReader(fileDatabase, delimiter=',')
        for data in reader:
            database[data['idTweeter']] = data['lastSuscribings'].split(';')
        fileDatabase.close()
        print("Database successfuly read")
except OSError:
    print ("Could not open/read file: " + pathDatabase)
    print ("Creating the file...")
    try:
        fileDatabase = open(pathDatabase, 'w')
        print("database.csv has been successfuly created !")
        print("Please fill the database before launching the program.")
        fileDatabase.close()
        sys.exit()
    except OSError:
        print("File couldn't be created. The program will be stopped.")
        sys.exit()

def followers():
    while True:
        # We are going to loop the database, and thus comparing the database with the data of the API.
        for key, value in database.items():
            popValuesFromDB = 0
            print("Check en cours pour", key)
            # We get the last followings of the user.
            lastFollowings = client.get_users_following(id=key, max_results=3, user_fields=['description','profile_image_url'])
            # We loop through the 3 last followings of the user.
            for i in range(0,3):
                if (str(lastFollowings[0][i].id) not in value):

                    personWhoFollows = client.get_user(id=key, user_fields=['profile_image_url'])
                    print(f"Nouvel abonnement pour @{personWhoFollows[0].username} !")

                    # We update the database values : we insert the new followings.
                    database[key].insert(0,str(lastFollowings[0][i].id))
                    # We need to delete the older values when we're done looping.
                    popValuesFromDB += 1

                    # Prepare values for Discord notification
                    author['name'] = "Nouvel abonnement pour @" + personWhoFollows[0].username + "!"
                    author['URL'] = "https://twitter.com/" + personWhoFollows[0].username
                    author['IconURL'] = personWhoFollows[0].profile_image_url

                    content['title'] = "Clique ici pour suivre @" + lastFollowings[0][i].username + "!"
                    content['description'] = lastFollowings[0][i].description
                    content['url'] = "https://twitter.com/" + lastFollowings[0][i].username

                    # # Send Discord notification
                    webhook.remove_embeds()

                    embed = DiscordEmbed(title=content['title'], description=content['description'], color=style, url=content['url'])
                    embed.set_author(name=author['name'], url=author['URL'], icon_url=author['IconURL'])
                    embed.set_image(url=lastFollowings[0][i].profile_image_url)
                    embed.set_footer(text=random.choice(randomFooter))
                    embed.set_timestamp()

                    webhook.add_embed(embed)
                    webhook.execute()
                    
                    time.sleep(1)

            if (popValuesFromDB != 0):
                for i in range (0, popValuesFromDB):
                    database[key].pop()
                # We write down on the CSV file the newest database
                print("Réécriture BDD en cours...")
                with open(pathDatabase, 'w') as fileDatabase:
                    writer = csv.writer(fileDatabase, delimiter=',')
                    writer.writerow(csvHeading)
                    for idTweeter, lastSuscribings in database.items():
                        writer.writerow([idTweeter, ';'.join(lastSuscribings)])
                print("Réécriture finie !") 
                
            print("Check fini ! Attente de 60 secondes !")

            time.sleep(60)

followers()