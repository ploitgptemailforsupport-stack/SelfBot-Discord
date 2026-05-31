import requests
import random
import time
import threading
import re
from colorama import Fore, init

init(autoreset=True)

BASE_URL = 'https://discord.com/api/v9'
headers = {
    'Authorization': 'YOUR_TOKEN_HERE',
    'Content-Type': 'application/json'
}

terror_msgs = [
    'FUCK YOU', 'MONKEY', 'ASSHOLE', 'WHO GAVE YOU PERMISSION TO SPEAK?',
    'NIGGA ASSHOLE', 'KEEP CRYING YOUR PINGS OUT', 'WHAT A CRYBABY',
    'HAHAHA WTF YOU DOIN, YOU CRYING? LOLL', 'I THINK YOU WERE WARNED MOTHERFUCKER',
    'SUCK MY CUM', 'NO GIRL WANTS YOUR 1.5CM DICK', 'BITCH',
    'STUPID FUCKING DOG', 'KILL YOURSELF RETARD', 'YOURE A WORTHLESS CUNT',
    'SHUT THE FUCK UP WHORE', 'YOUR MOM SUCKS DICK FOR ROBUX',
    'PATHETIC LITTLE FAGGOT', 'HOPE YOU GET CANCER', 'GET RAPED IN THE ASS',
    'DUMBASS NIGGER', 'LICK MY ASSHOLE', 'YOURE SO FUCKING TRASH LMAO',
    'GO DIE IN REAL LIFE', 'YOUR FAMILY IS ASHAMED OF YOU',
    'YOU DESERVE TO BE BULLIED', 'MENTALLY ILL FREAK', 'TOXIC WASTE HUMAN',
    'I HOPE YOUR DOG DIES', 'YOURE THE REASON YOUR DAD LEFT',
    'UNLOVABLE PIECE OF SHIT', 'YOUR LIFE IS A JOKE', 'NO ONE LOVES YOU',
    'GO HANG YOURSELF', 'YOU SHOULDVE BEEN ABORTED', 'DISGUSTING HUMAN GARBAGE',
    'YOUR EXISTENCE IS A MISTAKE', 'KILL YOURSELF ALREADY', 'YOURE A WASTE OF OXYGEN',
    'NOBODY WOULD MISS YOU', 'PATHETIC VIRGIN LOSER', 'YOUR MOM REGRETS BIRTHING YOU',
    'GO CRY IN A CORNER FAGGOT', 'I HOPE YOU GET BEATEN IRL',
    'YOURE A DISAPPOINTMENT TO HUMANITY', 'STUPID FUCKING AUTIST',
    'YOUR BLOODLINE ENDS WITH YOU', 'DIE SLOWLY YOU WORTHLESS CUNT'
]

processed_messages = set()

def send_terror(channel_id, user_id, amount=10):
    amount = min(max(amount, 1), 48)
    print(f"{Fore.RED}[!] Terror → {user_id} | {amount} msgs")
    for i in range(amount):
        try:
            msg = random.choice(terror_msgs)
            formatted = f"# * <@{user_id}>\n``[{msg}]``"
            requests.post(f'{BASE_URL}/channels/{channel_id}/messages', headers=headers, json={'content': formatted})
            time.sleep(1.1)
        except: pass

def dmbomb():
    print(f"{Fore.RED}[!] Starting DM Bomb on all DMs...")
    dms = requests.get(f'{BASE_URL}/users/@me/channels', headers=headers).json()
    for dm in dms:
        if dm['type'] == 1:  # DM
            channel_id = dm['id']
            user_id = dm['recipients'][0]['id']
            threading.Thread(target=send_terror, args=(channel_id, user_id, 8), daemon=True).start()  # 8 msgs per person
            time.sleep(1.5)  # Avoid rate limits

def change_status(status):
    status_map = {"online":"online","dnd":"dnd","invisible":"invisible","idle":"idle","sleep":"invisible"}
    requests.patch(f"{BASE_URL}/users/@me/settings", headers=headers, json={"status": status_map.get(status.lower(), "online")})

def monitor_dms():
    print(f"{Fore.MAGENTA}[*] Bot Online | Commands: !help, !terror, !dmbomb, !status, !stopterror")

    while True:
        try:
            dms = requests.get(f'{BASE_URL}/users/@me/channels', headers=headers).json()

            for dm in dms:
                if dm['type'] != 1: continue
                channel_id = dm['id']

                msgs = requests.get(f'{BASE_URL}/channels/{channel_id}/messages?limit=8', headers=headers).json()

                for msg in msgs:
                    msg_id = msg['id']
                    if msg_id in processed_messages: continue
                    processed_messages.add(msg_id)

                    content = msg['content'].strip().lower()

                    if content == '!help':
                        help_text = "**Commands:**\n`!terror @user [amount]`\n`!dmbomb` (DMs everyone)\n`!status [online/dnd/invisible/idle/sleep]`\n`!stopterror`\n`!help`"
                        requests.post(f'{BASE_URL}/channels/{channel_id}/messages', headers=headers, json={'content': help_text})

                    elif content.startswith('!terror '):
                        mention = re.search(r'<@!?(\d+)>', msg['content'])
                        if mention:
                            user_id = mention.group(1)
                            amount_match = re.search(r'\d+$', msg['content'])
                            amount = int(amount_match.group()) if amount_match else 10
                            threading.Thread(target=send_terror, args=(channel_id, user_id, amount), daemon=True).start()

                    elif content == '!dmbomb':
                        threading.Thread(target=dmbomb, daemon=True).start()

                    elif content.startswith('!status '):
                        status = content.split(' ', 1)[1].strip()
                        change_status(status)

                    elif content == '!stopterror':
                        print(f"{Fore.YELLOW}[!] Stop command received")

        except: pass
        time.sleep(2.5)

if __name__ == "__main__":
    monitor_dms()