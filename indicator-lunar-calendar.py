#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# indicator-lunar-calendar - shows lunar calendar information
# Copyright (c) 2019 Adrian I Lam <spam@adrianiainlam.tk> s/spam/me/
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHOR OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
# IN THE SOFTWARE.
#
# I would like to thank Tobias Schlitt <toby@php.net>, who wrote
# indicator-chars <https://github.com/tobyS/indicator-chars> which I used
# as a reference when writing this software.

import signal
import datetime
import os
import gi
gi.require_version('Gdk', '3.0')
gi.require_version('Gtk', '3.0')
gi.require_version('AppIndicator3', '0.1')
from gi.repository import Gdk, Gtk, AppIndicator3
from LunarCalendarPy.LunarCalendar import LunarCalendar
import schedule
import threading
import time
import dbus
from dbus.mainloop.glib import DBusGMainLoop

APP_NAME = 'indicator-lunar-calendar-py'
APP_VERSION = '1.2+py'

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))


class IndicatorLunarCalendar:
    def __init__(self):
        self.indicator = AppIndicator3.Indicator.new(
            'lunar-indicator',
            os.path.join(SCRIPT_DIR, 'icons', '鼠.svg'),
            AppIndicator3.IndicatorCategory.APPLICATION_STATUS)
        self.indicator.set_status(AppIndicator3.IndicatorStatus.ACTIVE)

        self.menu = Gtk.Menu()
        self.item = Gtk.MenuItem()
        self.item.connect("activate", self.do_nothing)
        self.menu.append(self.item)
        self.indicator.set_menu(self.menu)
        self.menu.show_all()

        self.lc = LunarCalendar()
        self.update_indicator()

    def update_indicator(self):
        # get current time at UTC+8, add 1 to date if after 23:00 (子時)
        now = datetime.datetime.utcnow() + datetime.timedelta(hours=8)
        hour = now.hour
        if hour >= 23:
            now = now.date() + datetime.timedelta(days=1)

        lunar = self.lc.solarToLunar(now.year, now.month, now.day)
        lunar['hour'] = '子丑寅卯辰巳午未申酉戌亥'[(hour + 1) % 24 // 2]

        compact_date = lunar['lunarMonthName'] + lunar['lunarDayName']
        long_date = (
            lunar['GanZhiYear'] + '年（' + lunar['zodiac'] + '年）\n' +
            lunar['lunarMonthName'] + lunar['lunarDayName']
        )
        if lunar['term']:
            compact_date += ' ' + lunar['term']
            long_date += ' ' + lunar['term']
        long_date += '\n' + lunar['hour'] + '時'

        self.indicator.set_icon(
            os.path.join(SCRIPT_DIR, 'icons', lunar['zodiac'] + '.svg')
        )
        self.indicator.set_label(compact_date, '')
        self.item.set_label(long_date)

    def do_nothing(self, arg):
        pass


def run_schedule_one_iteration():
    prev_idle_sec = 60 * 60
    idle_sec = schedule.idle_seconds()
    while idle_sec < prev_idle_sec:
        prev_idle_sec = idle_sec

        if idle_sec > 2:
            time.sleep(idle_sec - 2)
        elif idle_sec > 0.199:
            time.sleep(idle_sec - 0.199)
        else:
            schedule.run_pending()

        idle_sec = schedule.idle_seconds()


def cronThreadBody():
    while True:
        run_schedule_one_iteration()


def updateJob(i):
    i.update_indicator()


if __name__ == '__main__':
    signal.signal(signal.SIGINT, lambda signum, frame: Gtk.main_quit())

    i = IndicatorLunarCalendar()

    schedule.every().hour.at(":00").do(updateJob, i=i)
    cronThread = threading.Thread(target=cronThreadBody)
    cronThread.start()

    dbusloop = DBusGMainLoop()
    bus = dbus.SystemBus(mainloop=dbusloop)
    obj = bus.get_object('org.freedesktop.login1', '/org/freedesktop/login1')
    iface = dbus.Interface(obj,
                           dbus_interface='org.freedesktop.login1.Manager')

    def sleepHandler(arg):
        if arg == 0:
            i.update_indicator()
            schedule.clear()
            schedule.every().minute.at(":00").do(updateJob, i=i)
            newThread = threading.Thread(target=run_schedule_one_iteration)
            newThread.start()

    iface.connect_to_signal('PrepareForSleep', sleepHandler)

    Gtk.main()
