# Twitter Following Bot - Sending notifications on Discord
With this project, you can add thanks to a CSV database Twitter IDs you want to watch : you'll get a Discord notification whenever they follow someone.

## Setup

### Bearer token and webhook

For this code running smoothly, you need 2 things:
- Twitter Bearer Token, available for free on [Twitter Developer Dashboard](https://developer.twitter.com/en/portal/dashboard).
- Discord Webhook, you can create it from your Discord Server. More info on [Discord Webhook](https://support.discord.com/hc/en-us/articles/228383668-Intro-to-Webhooks).

### Setting up the environment and the packages

First, create an environment for this python project:
```
$ python3 -m venv env
$ source env/bin/activate
```

Then, thanks to the [requirements](requirements.txt) file, you can instally directly the needed packages with:
```
$ pip3 install -r requirements.txt
```

Once it's done, all you have to do is to set up your bearer token and webhook in the .env file:

```
$ echo "bearer_token=yourbearertoken" >> .env
$ echo "discord_webhook=yourdiscordwebhook" >> .env
```

### Updating the database.csv file with your Twitter IDs
Lastly, you have to update the CSV file with the Twitter IDs you want to look up.
For this, go on [Twitter ID](https://tweeterid.com) and then type the @handle of the person you want to follow. Then, copy/paste the ID in the CSV file in the first column.

The IDs behind the first columns are the 6 last people that the ID followed: so you can change it but it'll be updated as soon as you run the code.

## Run the code

Now that you set up everything, you should be able to run the python file smoothly:
```
python3 twitterNewFollowingDiscord.py
```

Have fun 😎
