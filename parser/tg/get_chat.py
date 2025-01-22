from telegram import Bot

# Replace with your bot token
bot_token = '7938438245:AAGp9ukn4SQv_oVvhrWIXLCTMpWzGVCoG5Y'

# Replace with the channel username (e.g., @your_channel_username)
chat_id = '@your_channel_username'

# Create a Bot instance
bot = Bot(token=bot_token)

# Get chat information (this will give you the title and description of the channel)
chat_info = bot.get_chat(chat_id)

# Print the channel title and description
print("Channel Title:", chat_info.title)
print("Channel Description:", chat_info.description)
