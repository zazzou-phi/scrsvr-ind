#!/usr/bin/env python

import pygtk
pygtk.require('2.0')
import gtk

have_appindicator = True
try:
    import appindicator
except:
    have_appindicator = False
