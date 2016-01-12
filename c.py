from configparser import RawConfigParser
from os.path import expanduser

#we are on master here

parser = RawConfigParser()
parser.read(expanduser('~') + '/.config/yarn/config')

#[lemonbar]
xpos = parser.getint('lemonbar', 'xpos')
ypos = parser.getint('lemonbar', 'ypos')
gap = parser.getint('lemonbar', 'gap')
direction = parser.get('lemonbar', 'direction')
background = parser.get('lemonbar', 'background')
foreground = parser.get('lemonbar', 'foreground')
width = parser.getint('lemonbar', 'width')
height = parser.getint('lemonbar', 'height')
offset = parser.getint('lemonbar', 'offset')
max_notify = parser.getint('lemonbar', 'max_notify')

#[scroll]
scroll = parser.getboolean('scroll', 'scroll')
half_scroll = parser.getboolean('scroll', 'half_scroll')
scroll_space_side = parser.get('scroll', 'scroll_space_side')
scroll_space = parser.getint('scroll', 'scroll_space')
scroll_len = parser.getint('scroll', 'scroll_len')
scroll_interval = parser.getfloat('scroll', 'scroll_interval')
scroll_reverse = parser.getboolean('scroll', 'scroll_reverse')
loopback_amount = parser.getint('scroll', 'loopback_amount')
loopback_distance = parser.getint('scroll', 'loopback_distance')
ellipse = parser.getboolean('scroll', 'ellipse')

#[style]
summary_font = parser.get('style', 'summary_font')
body_font = parser.get('style', 'body_font')
summary_chars = parser.getint('style', 'summary_chars')

#[other]
timeout = parser.getint('other', 'timeout')
sleep = parser.getint('other', 'sleep')
logging = parser.getboolean('other', 'logging')
log_file = parser.get('other', 'log_file')
trail = parser.get('other', 'trail')
no_summary = parser.get('other', 'no_summary')
no_body = parser.get('other', 'no_body')
no_duplicate = parser.getboolean('other', 'no_duplicate')
