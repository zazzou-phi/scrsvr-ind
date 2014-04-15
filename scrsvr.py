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
        self.ind.set_attention_icon("new-messages-red")
        #self.ind.set_icon_theme_path("/home/source/scrsvr-ind")

        self.check_scrsvr = self.check_if_on()
        if self.check_scrsvr:
            self.ind.set_icon(get_path("scrsvr-on-dark.svg"))
        else:
            self.ind.set_icon(get_path("scrsvr-off-dark.svg"))

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
        #self.ind.set_attention()
        self.ind.set_icon(get_path("scrsvr-off-dark.svg"))
        os.system("gsettings set org.gnome.desktop.screensaver lock-enabled false")
        os.system("gsettings set org.gnome.desktop.session idle-delay 0")
        os.system("gsettings set org.gnome.settings-daemon.plugins.power sleep-inactive-ac-timeout 0")
        os.system("gsettings set org.gnome.settings-daemon.plugins.power sleep-inactive-battery-timeout 0")


    def switch_on(self):
        #self.ind.set_active()
        self.ind.set_icon(get_path("scrsvr-on-dark.svg"))
        os.system("gsettings set org.gnome.desktop.screensaver lock-enabled true")
        os.system("gsettings set org.gnome.desktop.session idle-delay 3600")
        os.system("gsettings set org.gnome.settings-daemon.plugins.power sleep-inactive-ac-timeout 3600")
        os.system("gsettings set org.gnome.settings-daemon.plugins.power sleep-inactive-battery-timeout 1800")

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

def get_path(file_name):
    python_file = os.path.dirname(__file__)
    rel_path = os.path.join(python_file, file_name)
    abs_path = os.path.abspath(rel_path)
    return abs_path

if __name__ == "__main__":
    indicator = ScreensaverSwitch()
    indicator.main()
