from pyrogram import Client, filters

api_id = int(os.environ["API_ID"])
api_hash = os.environ["API_HASH"]
bot_token = os.environ["BOT_TOKEN"]

app = Client(
    "my_bot",
    api_id=api_id,
    api_hash=api_hash,
    bot_token=bot_token
)


@app.on_message(filters.command("banall") & filters.group)
async def ban_all(client, message):
    chat_id = message.chat.id

    # Check if the user has admin privileges
    user = await client.get_chat_member(chat_id, message.from_user.id)

    if not user.privileges or not user.privileges.can_restrict_members:
        await message.reply_text("You don't have permission to use this command!")
        return

    banned_count = 0

    async for member in client.get_chat_members(chat_id):
        # Only ban members with no admin privileges
        if not member.privileges:
            try:
                await client.ban_chat_member(chat_id, member.user.id)
                banned_count += 1
            except:
                pass

    await message.reply_text(f"Banned {banned_count} non-admin members!")


app.run()
