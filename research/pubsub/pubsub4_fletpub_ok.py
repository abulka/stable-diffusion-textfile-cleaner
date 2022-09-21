# from pubsub import pub  # pip install PyPubSub
import flet
from flet import Column, ElevatedButton, Page, Row, Text, TextField

def main(page: Page):
    # I need the listener_chose_dir function defined HERE, in order to access 'page' variable etc. 
    # But if I define it here, the pub sub doesn't work.

    def listener_1(topic, arg):
        print('football', arg)

    # pub.subscribe(listener_1, 'football')
    page.pubsub.subscribe_topic("football", listener_1)

    # quick test of broadcasting
    # pub.sendMessage('football', arg={'headline': 'Ronaldo',
    #                              'news': 'Sold for $1M'})
    page.pubsub.send_all_on_topic('football', {'headline': 'Ronaldo',
                                 'news': 'Sold for $1M'})

    def send_click(e):
        print('click, so now broadcasting')
        # This broadcast doesn't work because the listener handler has fallen out of scope so PyPubSub ignores it
        # pub.sendMessage('football', arg={'headline': 'Ronaldo',
        #                          'news': 'Sold for $2M'})
        # Flet pub sub version - will it work?  YES - doesn't suffer the falling out of scope problem 🎉
        page.pubsub.send_all_on_topic('football', {'headline': 'Ronaldo',
                                 'news': 'Sold for $2M'})

    send = ElevatedButton("Send", on_click=send_click)
    page.add(send)    

flet.app(target=main)
