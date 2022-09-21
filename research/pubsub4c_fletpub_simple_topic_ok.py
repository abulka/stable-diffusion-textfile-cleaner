import flet
from flet import Column, ElevatedButton, Page, Row, Text, TextField
from dataclasses import dataclass

@dataclass
class Message:
    user: str
    text: str

def main(page: Page):

    def on_broadcast_message(topic, message):  # your handler needs to take two arguments - topic and message
        page.add(Text(f"topic: {topic}, {message.user}: {message.text}"))

    page.pubsub.subscribe_topic('general', on_broadcast_message)

    def on_send_click(e):
        page.pubsub.send_all_on_topic('general', Message("John", "Hello, all!"))

    page.add(ElevatedButton(text="Send message", on_click=on_send_click))

flet.app(target=main)
