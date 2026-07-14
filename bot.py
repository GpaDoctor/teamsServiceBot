from botbuilder.core import ActivityHandler, TurnContext
from botbuilder.schema import Activity, ActivityTypes

# Import your custom modules
from cards.botCards import get_main_menu_card, get_question_card, get_download_card
from services.pdfService import get_pdf_links

class SimpleWizardBot(ActivityHandler):
    async def on_message_activity(self, turn_context: TurnContext):
        
        # 1. Handle button clicks (Adaptive Card interactions)
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
                
                # Fetch PDF links from our isolated service layer
                pdf1, pdf2 = get_pdf_links(file_type, user_answer)
                
                # Deliver the final download card
                await turn_context.send_activity(Activity(
                    type=ActivityTypes.message, 
                    attachments=[get_download_card(file_type, user_answer, pdf1, pdf2)]
                ))
            return

        # 2. Default text fallback (if they just type 'hello')
        await turn_context.send_activity(Activity(type=ActivityTypes.message, attachments=[get_main_menu_card()]))