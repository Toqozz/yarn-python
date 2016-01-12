import c
import dbus
import ctypes
import psutil
import gobject
import subprocess
import dbus.service
import multiprocessing
from generate import scroll
from time import sleep, time
from html.parser import HTMLParser
from xml.sax.saxutils import unescape
from dbus.mainloop.glib import DBusGMainLoop

#TODO, scroll from a different side?
#TODO, different colors / timeout(?) for different urgency?
#TODO, write bash script to show last message again.

# Push a notification onto the screen using lemonbar.
# Only ever executed as a seperate process.
def notify(summary, body, timeout, signature):
    # Do not reset the force value if this notification is coming from the queue.
    # If the tracker is full, the pending notification is sent to the queue.
    if signature == 'queue': pass
    elif tracker.count(1) == c.max_notify:
        notification_queue(summary, body, timeout)
        return
    else: force_value.value = 0                         # Force value is no longer needed and is reset.

    # Find place for new notification to go, and occupy it.
    position = tracker.index(0)
    tracker[position] = 1
    curtime = time()                                    # Kill notifications at the right time later on.
    # The actual BODY length to be held on the bar, since it changes dynamically with the summary.
    len_actual = c.summary_chars-(len(summary)-12)+c.scroll_len # 12 is the length of [ %{T2}%{T1} ].

    # Lemonbar options parsed from user config.
    if c.direction == 'up':
        command = 'lemonbar -p -b -B %s -F %s -g %sx%s+%s+%s -f %s -f %s -o %s' % \
        (c.background, c.foreground, c.width, c.height, c.xpos, c.ypos+((c.gap+c.height)*position), c.body_font, c.summary_font, c.offset)
    else:
        command = 'lemonbar -p -b -B %s -F %s -g %sx%s+%s+%s -f %s -f %s -o %s' % \
        (c.background, c.foreground, c.width, c.height, c.xpos, c.ypos-((c.gap+c.height)*position), c.body_font, c.summary_font, c.offset)

    if (c.ellipse == True and
            len(body) > len_actual):
        body = string_ellipse(body, len_actual)

    # Imported from generate.scroll, returns a list that can easily be 'scrolled'.  See generate.py.
    if c.scroll_reverse == True:
        array = scroll(summary, body, len_actual)
        array = list(reversed(array))
    else:
        array = scroll(summary, body, len_actual)

    process = subprocess.Popen(command.split(), stdin=subprocess.PIPE, bufsize=1, universal_newlines=True)
    pids[position] = process.pid                        # PID list equal in positions to tracker.
    if c.logging == True:
        file_write(pids[position], summary, body)



    # > ----- process loop start ------ < #
    #TODO, fix bug thing where a long message will hang on last character if the time is long.
    _ = 0
    if c.scroll_space_side == 'left': i = (len_actual-c.scroll_space)-1
    else: i = c.scroll_space
    executed = False
    # Be ready for pipes to be broken.
    try:
        while True:
            # Kill notification when time is up.
            if time() - curtime > timeout:
                break
            # Stop scrolling if the notification is shown all at once.
            elif (c.half_scroll == True and
                    array[i].strip() == (summary + body).strip() and
                    executed == False):
                executed = True
                _ = i
            # Out of text!  Ellipse the message so we have something meaningful to hold onto.
            elif (i+1 == len(array) and
                    executed == False):
                executed = True
                array.append(summary + (string_ellipse(body, len_actual) + '\n'))
                _ = i+1
            elif executed == False:
                _ = i
                i += 1

            process.stdin.write('%s' % (array[_]))      # Sometimes, python is strange about converting arrays, should not be an issue.
            sleep(c.scroll_interval)

    # We're ready for broken pipes.
    except BrokenPipeError:
        tracker[position] = 0
        print('The process that was being written to has been terminated, breaking.  This is not a bad thing.')
        return
    # > ----- process loop end ------ < #



    # The notification is ending, its place in the queue can be cleared.
    # Nothing under these lines will execute, at least not for the parent process.
    tracker[position] = 0
    process.terminate()

# Queue for pending notifications.
def notification_queue(summary, body, timeout):
    # If [force_value] has hit the top, start at the bottom again (or the top if notifications are coming downwards instead of up.)
    if force_value.value == c.max_notify:
        force_value.value = 0

    # Lock onto the process to be terminated.
    process = psutil.Process(pids[force_value.value])
    process.terminate()
    # Be sure that the process is terminated before continuing.
    while True:
        if process.is_running() == False:
            # A place in the queue has been cleared, the notification can be called again and will occupy the free space.
            # Next time, the to-be-terminated should be further up by one.
            tracker[force_value.value] = 0
            force_value.value += 1
            notify(summary, body, timeout, 'queue')
            return
        sleep(0.1)

    # os.kill(pids[force_value.value], signal.SIGTERM)
    # Less... accurate than psutil.  Could not find more information online, but when spamming notifications os.kill will cause [force_value] to get hung
    # on a previous number.  Though it does not seem to execute slower (0.0005305s vs 0.0005886s).  Perhaps psutil forks, and os.kill does not?
    # It is a very long time before force_value gets changed using os.kill, however.  I do not really understand the behaviour.
    # Using a while loop with psutil is the most consistent result.

# Shorten text and put an ellipse in the middle.
def string_ellipse(string, length):
    chop1 = length // 2
    if length % 2 == 0: chop2 = (length // 2) - 1           # We need to remove a character for the ellipse if string is even, // does it for us if odd.
    else: chop2 = length // 2

    # 17 + '…' + 17
    string = string[:chop1] + '…' + string[len(string)-chop2:]
    return string

#while len(string) >= length:
        # Find the middle of the string (does not need to be deadly accurate).
        # Chop chop.
        #middle = len(string) // 2
        #string = string[:middle] + string[middle+1:]
    # Finally insert ellipses.
    #string = string[:middle] + '…' + string[middle:]
    #return string

# Write to log (if enabled.)
def file_write(pid, summary, body):
    with open(c.log_file, 'a') as f:
        # Format: '[pid]: [summary]: [body]' (easy separation from sections using awk).
        f.write(str(pid) + ':' + summary + ':' + body + '\n')

# Function called by notify-send after initial cleanup of strings.
def print_notification(args):
    # Variable names for a dictionary later on, improved readability.
    keys = ['app_name', 'replaces_id', 'app_icon', 'summary',
            'body', 'actions', 'hints', 'expire_timeout']

    notification = dict([(keys[i], args[i]) for i in range(8)])
    if notification['expire_timeout'] <= 0:
        notification['expire_timeout'] = c.timeout

    # Using multi processing to display more than one notification at a time.
    thread = multiprocessing.Process(
        target=notify, args=(notification['summary'],
                             notification['body'],
                             notification['expire_timeout'],
                            'host')
    )

    thread.start()
    # Don't spam the daemon too much.  Causes notify-send to sleep also.
    sleep(c.sleep)

# Thanks to statnot for basic NotificationFetcher class: https://github.com/halhen/statnot
class NotificationFetcher(dbus.service.Object):
    _id = 0

    @dbus.service.method('org.freedesktop.Notifications', in_signature='susssasa{ss}i', out_signature='u')
    def Notify(self, app_name, replaces_id, app_icon, summary, body, actions, hints, expire_timeout):

        # Handle duplicate notifications
        # TODO, make it so that the variable is never created if whatever is false.
        if not c.no_duplicate == True:
            pass
        elif (c.no_duplicate == True and
                body == previous.value):
            print('A duplicate notification has been detected and ignored.')
            return 0
        else:
            previous.value = body

        # Make sure the sections we need are filled.
        # You actually cant send a notification without a summary with notify-send, but let's check anyway.
        if summary == '' or summary.isspace() == True:
            summary = c.no_summary
        if body == '' or body.isspace() == True:
            body = c.no_body

        # Change &amp; &lt; &gt; &quot; &apos; to & < > " '.
        # Strip new lines, extra whitespace.
        summary = unescape(summary, {'&apos;': "'", '&quot;': '"'})
        summary = summary.strip().replace('\n', '')
        body = unescape(body, {'&apos;': "'", '&quot;': '"'})
        body = body.strip().replace('\n', '')

        # If a limitation on summary characters exists, replace the remaining text with a trailing character.
        if (c.summary_chars > 0 and
                len(summary) > c.summary_chars):
            summary = (summary[:c.summary_chars] + c.trail)

        # Duplicate the body if loopback is being used and the body is too long for the bar.
        # Other methods would require cutting strings and making new ones on the fly, to make it shown at one time at least.
        # This really is the most efficient way to do it.
        if (c.loopback_amount > 0 and
                c.ellipse == False and
                len(body) > ((c.summary_chars-len(summary))+c.scroll_len)):     # Add whitespace to the body.
            body = body + ((' '*c.loopback_distance) + body) * c.loopback_amount

        # Change the font for the summary/body using lemonbar options.
        summary = ' %{T2}' + summary + '%{T1} '

        # Notifications need ids.
        if not replaces_id:
            self._id += 1
            replaces_id = self._id
        # Expire timeout defaults to -1, set it to a user default.
        # TODO, support 0.
        if expire_timeout <= 0:
            expire_timeout = c.timeout

        # Prepare agrs for print_notification()
        args = [app_name, replaces_id, app_icon, summary, body, actions, hints, expire_timeout]

        print_notification(args)
        return notifiction_id

    @dbus.service.method('org.freedesktop.Notifications', in_signature='', out_signature='as')
    def GetCapabilities(self):
        # Actions, hyperlinks, sounds, most things actually are supported through DIY in the log.
        return('body')

    @dbus.service.signal('org.freedesktop.Notifications', signature='uu')
    def NotificationClosed(self, id_in, reason_in):
        pass

    @dbus.service.method('org.freedesktop.Notifications', in_signature='u', out_signature='')
    def CloseNotification(self, id):
        # TODO support this.
        # yarn does not have a built in notify_close function right now.
        pass

    @dbus.service.method('org.freedesktop.Notifications', in_signature='', out_signature='ssss')
    def GetServerInformation(self):
        return ('yarn', 'github', '0.8.0', '1')

# If run directly (also omitted from loop).
if __name__ == '__main__':
    # Create a custom list equal to c.max_notify.
    l = []
    for i in range(0, c.max_notify):
        l.append(0)

    manager = multiprocessing.Manager()
    tracker = manager.list(l)                   # Places available for a  notification to be shown.
    pids = manager.list(l)                      # Pids that asociate to the 'places' in the tracker list.
    force_value = manager.Value('i', 0)         # Where to force-place the next notification.
    previous = manager.Value(ctypes.c_char_p, '')      # To hold the text of the last notification.

    #multiprocessing.set_start_method('spawn')  # Cannot be used with multiprocesing variables. (that i know of).

    # Start a loop to watch for messages in org.freedesktop.Notifications
    # Be the next owner if the name is in use.
    DBusGMainLoop(set_as_default=True)
    session_bus = dbus.SessionBus()
    session_bus.request_name('org.freedesktop.Notifications')
    name = dbus.service.BusName('org.freedesktop.Notifications', session_bus)
    nf = NotificationFetcher(session_bus, '/org/freedesktop/Notifications')

    # Watch for events and launch appropriate actions.
    gobject.MainLoop().run()
