from pubsub import pub  # pip install PyPubSub
import flet
from flet import Column, ElevatedButton, Page, Row, Text, TextField

# This doesn't get sent to the handler since the handler has fallen out of scope
# and the pub sub system doesn't keep a reference to it, it seems.
# See mac notes "pub sub in Python - Publisher Subscriber"


def main(page: Page):
    # I need the listener_chose_dir function defined HERE, in order to access 'page' variable etc. 
    # But if I define it here, the pub sub doesn't work.

    def listener_1(arg):
        print('football', arg)

    pub.subscribe(listener_1, 'football')

    # quick test of broadcasting
    pub.sendMessage('football', arg={'headline': 'Ronaldo',
                                 'news': 'Sold for $1M'})

    def send_click(e):
        print('click, so now broadcasting')
        # This broadcast doesn't work because the listener handler has fallen out of scope so PyPubSub ignores it
        pub.sendMessage('football', arg={'headline': 'Ronaldo',
                                 'news': 'Sold for $2M'})

    send = ElevatedButton("Send", on_click=send_click)
    page.add(send)    

flet.app(target=main)
