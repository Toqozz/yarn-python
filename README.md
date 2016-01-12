# yarn

yarn hopes to fill a void between heavy notification daemons (notify-osd) and minimalistic notification daemons (dunst, statnot).

Currently, yarn uses lemonbar to actually print text to the screen.  While not the most efficient method that can be imagined,
it is still very lightweight and allows for some customization that would otherwise be difficult.  
Eventually, hopefully, yarn will have its own way of pushing notifications to the display.

## features

* Threaded notifications.
    * yarn displays notifications visually as seperate threads.  The best way to explain this is through an image. 
    ![threaded notifications](http://i.imgur.com/ci9pmle.png)
* Customization.
    * Since yarn displays notifications using lemonbar, the extensive range of customizability is mirrored. 
    * Font, width, height, opacity, color, direction, etc -- see config file.
* Feature rich ways of displaying your text.
    * The main "feature" that yarn is built around is scrolling text, of course it can be disabled, but it is definitely a main feature, at least personally.
    * Scrolling can be manipulated in various ways: scroll direction, scroll speed, the amount of 