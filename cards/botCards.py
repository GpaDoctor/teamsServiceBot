from botbuilder.core import CardFactory

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

def get_download_card(file_type, choice_made, pdf1_url, pdf2_url):
    title = f"File {file_type.upper()} Pack Ready ({choice_made.upper()})"
    return CardFactory.adaptive_card({
        "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
        "type": "AdaptiveCard",
        "version": "1.4",
        "body": [
            {"type": "TextBlock", "text": title, "weight": "Bolder", "size": "Medium"},
            {"type": "TextBlock", "text": "Click below to grab your two configuration files:"}
        ],
        "actions": [
            {"type": "Action.OpenUrl", "title": "Download PDF 1", "url": pdf1_url},
            {"type": "Action.OpenUrl", "title": "Download PDF 2", "url": pdf2_url}
        ]
    })