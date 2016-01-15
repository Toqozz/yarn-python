# yarn

yarn hopes to fill a void between heavy notification daemons (notify-osd)
 and minimalistic notification daemons (dunst, statnot).

Currently, yarn uses lemonbar to actually print text to the screen.
While not the most efficient method that can be imagined,
it is still very lightweight and allows for some customization that would otherwise be difficult.  
Eventually, hopefully, yarn will have its own way of pushing notifications to the display.

## features

* Threaded notifications.
    * yarn displays notifications visually as seperate threads.
      The best way to explain this is through an image.  
      The summary kerning is my font, not yarn.  
      ![threaded notifications](http://i.imgur.com/I8lvv01.png)
* Customization.
    * Since yarn displays notifications using lemonbar, the extensive range of customizability is mirrored. 
    * Font, width, height, opacity, color, direction, etc -- see config file.
* Different ways of displaying text.
    * The main "feature" that yarn is built around is scrolling text,
      of course it can be disabled, but it is definitely a main feature, at least personally.
    * Scrolling can be manipulated:
      scroll direction, scroll speed, bounce, whether or not to loop the scroll, etc.
      Everything that I have thought of has been, is being, or is attempting to be implemented.
    * Different fonts for summary/body.
* Logging
    * Support for logging notifications (and their pid's) to file.
    * Use with scripts to handle things like hotkey url-opening, force-closing notificaions, or whatever really.


## dependencies

At the moment, yarn source code is not very portable.
There is an executable version, however the size is much larger because the dependencies are bundled with it.

If you are not using the "compiled" version, you will require the following known dependencies:
* pytho-psutil 
* python-dbus 
* python-gobject 
* lemonbar or lemonbar-xft

## install

### compiled

Download the executable from [here](https://www.dropbox.com/s/38abhbuhh1h02mu/yarn-0.9?dl=0)  
Make the file executable:

    chmod +x yarn

Run yarn directly (`./yarn`) or copy it to your bin folder:

    cp yarn /usr/local/bin
    yarn

### source

Clone the repository:

    cd ~/git/
    git clone https://github.com/Toqozz/yarn.git
    
Copy the config file to the correct directory:

    cd yarn/
    mkdir ~/.config/yarn/
    cp ./config/yarn/config ~/.config/yarn/config
    
## usage

Start the yarn daemon (or put it in your autostart):

    python ~/git/yarn/yarn.py 

That's really pretty much it.
