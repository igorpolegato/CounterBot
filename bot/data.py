import configparser

config = configparser.ConfigParser()
config.read("./config/config.ini")

ignorar = []
usuarios = []

bt = config['bot']
lk = config['links']
msgens = config['mensagens']

api_id = bt['api_id']
api_hash = bt['api_hash']
bot_token = bt['bot_token']
bot_name = bt['name']

for l in lk['ignorar'].split(","):
    ignorar.append(l.strip())

for u in msgens['users'].split(","):
    usuarios.append(u.strip())

lk_ignore = ignorar

perm_users = list(map(int, usuarios))
gp_id = int(msgens['grupo'])
min_range = int(msgens['min'])
max_range = int(msgens['max'])
