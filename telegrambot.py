import os
import json
import requests

from telegram import Bot


async def sendMessage(data):
    tg_bot = Bot(token=os.environ['TOKEN'])
    channel = os.environ['CHANNEL']
    discord_webhook_url = os.environ['DISCORD_WEBHOOK_URL']
  
    try:
        print('--->Sending message to telegram')
        if isinstance(data, bytes):
            data = data.decode('utf-8')  # Convert bytes to string
        if isinstance(data, str):
            json_data = json.loads(data)  # Parse JSON string
            embeds = json_data.get('embeds', [])
            for embed in embeds:
                title = embed.get('title', '')
                description = embed.get('description', '')
                color = embed.get('color', None)
                #color = embed.get('color', '16711680')
                
                message = f"**{title}**\n\n{description}"
                
                tg_bot.send_message(
                    chat_id=channel,
                    text=message,
                    parse_mode="MARKDOWN",
                    disable_web_page_preview=False
                )
                # Send message to Discord webhook
                discord_payload = {
                    'embeds': [
                        {
                            'title': title,
                            'description': description,
                            'color': color
                        }
                    ]
                }

                response = requests.post(discord_webhook_url,     
                json=discord_payload)
                response.raise_for_status()

        return True
      
    except KeyError:
        print('--->Key error - sending error to telegram')
        await tg_bot.send_message(
            chat_id=channel,
            text=data,
            parse_mode="MARKDOWN",
            disable_web_page_preview=True
        )
    except Exception as e:
        print("[X] Telegram Error:\n>", e)
    return False
