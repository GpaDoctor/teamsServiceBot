from aiohttp import web
from botbuilder.core import BotFrameworkAdapter, BotFrameworkAdapterSettings
from botbuilder.schema import Activity

# Import the configured bot controller from bot.py
from bot import SimpleWizardBot

# Local test settings (leave empty for testing with Emulator)
SETTINGS = BotFrameworkAdapterSettings(app_id="", app_password="")
ADAPTER = BotFrameworkAdapter(SETTINGS)
BOT = SimpleWizardBot()

async def messages_handler(request):
    body = await request.json()
    activity = Activity().deserialize(body)
    auth_header = request.headers.get("Authorization", "")
    
    # Process request using our adapter and bot handler
    await ADAPTER.process_activity(activity, auth_header, BOT.on_message_activity)
    return web.Response(status=201)

app = web.Application()
app.router.add_post("/api/messages", messages_handler)

if __name__ == "__main__":
    print("Bot web server running on http://localhost:3978")
    web.run_app(app, host="localhost", port=3978)