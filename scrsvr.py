#!/usr/bin/env python

import sys
import gtk
import appindicator

import os
import commands

class ScreensaverSwitch:
    def __init__(self):
        self.ind = appindicator.Indicator("screensaver-switch",
                                           "indicator-messages",
                                           appindicator.CATEGORY_APPLICATION_STATUS)
        self.ind.set_status(appindicator.STATUS_ACTIVE)
        self.ind.set_attention_icon("indicator-messages-new")

        self.menu_setup()
        self.ind.set_menu(self.menu)

    def menu_setup(self):
        self.menu = gtk.Menu()
        
        self.switcheroo = gtk.MenuItem("Toogle Screensaver")
        self.switcheroo.connect("activate", self.switch)
        self.switcheroo.show()
 
        self.quit_item = gtk.MenuItem("Quit")
        self.quit_item.connect("activate", self.quit)
        self.quit_item.show()

        self.menu.append(self.switcheroo)
        self.menu.append(self.quit_item)

    def switch(self, dude):
        self.scrsvr_on = self.check_if_on()
        
        if self.scrsvr_on:
            self.switch_off()
        else:
            self.switch_on()

    def switch_off(self):
        os.system("gsettings set org.gnome.desktop.screensaver lock-enabled false")
        os.system("gsettings set org.gnome.desktop.session idle-delay 0")

    def switch_on(self):
        os.system("gsettings set org.gnome.desktop.screensaver lock-enabled true")
        os.system("gsettings set org.gnome.desktop.session idle-delay 3600")

    def check_if_on(self):
        stat, out = commands.getstatusoutput("gsettings get org.gnome.desktop.screensaver lock-enabled")
        if "true" in out:
            return True
        else:
            return False

    def main(self):
        gtk.main()

    def quit(self, widget):
        sys.exit(0)

if __name__ == "__main__":
    indicator = ScreensaverSwitch()
    indicator.main()
