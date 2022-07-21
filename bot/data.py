import configparser

config = configparser.ConfigParser()
config.read("./config/config.ini")

bt = config['bot']

api_id = bt['api_id']
api_hash = bt['api_hash']
bot_token = bt['bot_token']
bot_name = bt['name']