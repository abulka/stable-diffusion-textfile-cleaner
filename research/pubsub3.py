# Finally a version of pub sub which keeps handlers connected to the pub sub system
# even if they fall out of scope.  This is the one I'm going to use.

import smokesignal

# @smokesignal.on('foo')
# def my_callback():
#     print('foo was sent')

@smokesignal.on('foo', max_calls=2)
def my_callback(a, b, c, four=None):
    print('foo was sent HA', a, b, c, four)

# smokesignal.on('foo', my_callback, max_calls=5)

# Each callback responding to 'foo' is called with arguments
smokesignal.emit('foo', 1, 2, 3, four=4)

def main():
    @smokesignal.on('bar')
    def my_callback(a, b, c, four=None):
        print('bar was sent HA', a, b, c, four)
    smokesignal.emit('bar', 1, 2, 3, four=43)

main()
smokesignal.emit('bar', 1, 2, 3, four=434)

