# discord-playing-cards-bot

Generates custom playing card set and creates a bot draws them using a discord command. Needs python 3.10.
Usage:
1. To generate the playing cards do
`python card_generator/generate_card.py all`. Uses base images from the base_images directory, which use selected pieces from the EVMavericks collection.
2. To launch the bot, do
`python discord_bot/main.py`. Needs the authorization token to be passed in either as an environment variable or in a .env file.
3. The bot looks for a command `/draw` followed by a number from 1 to 5. For invalid input it defaults to 1. The bot then generates an image with that number of randomly selected cards (with replacement, ie., one card can appear multiple times in each selection) from the collection and posts it in a response.
4. The code is pretty light and was tested to work on a google cloud ec2-micro instance.