from pydispatch import dispatcher  # http://pydispatcher.sourceforge.net/
SIGNAL = 'my-first-signal'
SIGNAL2 = 'my-first-signal2'


def handle_event(sender):
    """Simple event handler"""
    print('Signal was sent by', sender)



dispatcher.connect(handle_event, signal=SIGNAL, sender=dispatcher.Any)

first_sender = object()
second_sender = {}


def main():

    dispatcher.send(signal=SIGNAL, sender=first_sender)
    dispatcher.send(signal=SIGNAL, sender=second_sender)


    def handle_event2(sender, arg):
        """Simple event handler with arg"""
        print('Signal 2 was sent by', sender, 'arg', arg)
    dispatcher.connect(handle_event2, signal=SIGNAL2, sender=dispatcher.Any)

    myargs = {'headline': 'Ronaldo',
              'news': 'Sold for $1M'}
    dispatcher.send(signal=SIGNAL2, sender=None, arg=myargs)


main()

# just like with PyPubSub, this doesn't get sent to the handler since the handler has fallen out of scope
# and the pub sub system doesn't keep a reference to it, it seems.

myargs = {'headline': 'Felix',
            'news': 'Sold for $2M'}
dispatcher.send(signal=SIGNAL2, sender=None, arg=myargs)
