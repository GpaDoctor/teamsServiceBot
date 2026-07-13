from aiohttp import web
from botbuilder.core import ActivityHandler, TurnContext, CardFactory, BotFrameworkAdapter, BotFrameworkAdapterSettings
from botbuilder.schema import Activity, ActivityTypes

# --- 1. THE USER INTERFACE (ADAPTIVE CARDS) ---

def get_main_menu_card():
    return CardFactory.adaptive_card({
        "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
        "type": "AdaptiveCard",
        "version": "1.4",
        "body": [
            {"type": "TextBlock", "text": "Welcome! Please choose a service:", "weight": "Bolder", "size": "Medium"}
        ],
        "actions": [
            {"type": "Action.Submit", "title": "Setup File A Service", "data": {"actionType": "start_a"}},
            {"type": "Action.Submit", "title": "Setup File B Service", "data": {"actionType": "start_b"}}
        ]
    })

def get_question_card(file_type):
    question_text = "For File A: What is your primary industry?" if file_type == "A" else "For File B: Select your environment:"
    choices = (
        [{"title": "Finance", "value": "fin"}, {"title": "Healthcare", "value": "health"}] if file_type == "A"
        else [{"title": "Cloud", "value": "cloud"}, {"title": "On-Premise", "value": "onprem"}]
    )
    return CardFactory.adaptive_card({
        "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
        "type": "AdaptiveCard",
        "version": "1.4",
        "body": [
            {"type": "TextBlock", "text": question_text, "weight": "Bolder"},
            {"type": "Input.ChoiceSet", "id": "user_choice", "style": "expanded", "choices": choices}
        ],
        "actions": [
            {"type": "Action.Submit", "title": "Submit Answer & Download", "data": {"actionType": f"submit_{file_type.lower()}"}}
        ]
    })

def get_download_card(file_type, choice_made):
    if file_type == "A":
        title = f"File A Pack Ready ({choice_made.upper()})"
        pdf1, pdf2 = "https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf", "https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf"
    else:
        title = f"File B Pack Ready ({choice_made.upper()})"
        pdf1, pdf2 = "https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf", "https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf"

    return CardFactory.adaptive_card({
        "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
        "type": "AdaptiveCard",
        "version": "1.4",
        "body": [
            {"type": "TextBlock", "text": title, "weight": "Bolder", "size": "Medium"},
            {"type": "TextBlock", "text": "Click below to grab your two configuration files:"}
        ],
        "actions": [
            {"type": "Action.OpenUrl", "title": "Download PDF 1", "url": pdf1},
            {"type": "Action.OpenUrl", "title": "Download PDF 2", "url": pdf2}
        ]
    })

# --- 2. THE BOT ENGINE ---

class SimpleWizardBot(ActivityHandler):
    async def on_message_activity(self, turn_context: TurnContext):
        # Handle button clicks
        if turn_context.activity.value:
            data = turn_context.activity.value
            action = data.get("actionType")
            
            if action == "start_a":
                await turn_context.send_activity(Activity(type=ActivityTypes.message, attachments=[get_question_card("A")]))
            elif action == "start_b":
                await turn_context.send_activity(Activity(type=ActivityTypes.message, attachments=[get_question_card("B")]))
            elif action in ["submit_a", "submit_b"]:
                file_type = "A" if action == "submit_a" else "B"
                user_answer = data.get("user_choice", "default")
                await turn_context.send_activity(Activity(type=ActivityTypes.message, attachments=[get_download_card(file_type, user_answer)]))
            return

        # Handle text fallback
        await turn_context.send_activity(Activity(type=ActivityTypes.message, attachments=[get_main_menu_card()]))

# --- 3. THE LOCAL WEB SERVER ---

SETTINGS = BotFrameworkAdapterSettings(app_id="", app_password="")
ADAPTER = BotFrameworkAdapter(SETTINGS)
BOT = SimpleWizardBot()

async def messages_handler(request):
    body = await request.json()
    activity = Activity().deserialize(body)
    auth_header = request.headers.get("Authorization", "")
    await ADAPTER.process_activity(activity, auth_header, BOT.on_message_activity)
    return web.Response(status=201)

app = web.Application()
app.router.add_post("/api/messages", messages_handler)

if __name__ == "__main__":
    web.run_app(app, host="localhost", port=3978)