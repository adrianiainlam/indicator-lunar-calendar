#!/usr/bin/env node
/*
 * indicator-lunar-calendar - shows lunar calendar information
 * Copyright (c) 2016 Adrian I Lam <adrianiainlam@gmail.com>
 * 
 * Permission is hereby granted, free of charge, to any person obtaining a
 * copy of this software and associated documentation files (the "Software"),
 * to deal in the Software without restriction, including without limitation
 * the rights to use, copy, modify, merge, publish, distribute, sublicense,
 * and/or sell copies of the Software, and to permit persons to whom the
 * Software is furnished to do so, subject to the following conditions:
 * 
 * The above copyright notice and this permission notice shall be included in
 * all copies or substantial portions of the Software.
 * 
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
 * THE AUTHOR OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
 * FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
 * IN THE SOFTWARE.
 */

/* import dependencies */
var GNode = require('node-gtk');
var Gtk = GNode.importNS('Gtk');
var AppIndicator3 = GNode.importNS('AppIndicator3');
var CronJob = require('cron').CronJob;
var LunarCalendar = require('lunar-calendar-zh');
var DBus = require('dbus-native');

/* setup indicator object */
GNode.startLoop();
Gtk.init(null);
var indicator = AppIndicator3.Indicator.new(
    "lunar-indicator",
    __dirname + '/icons/鼠.svg',
    AppIndicator3.IndicatorCategory.APPLICATION_STATUS
);
indicator.set_status(AppIndicator3.IndicatorStatus.ACTIVE);
var menu = new Gtk.Menu();
var item = new Gtk.MenuItem();
menu.append(item);
indicator.set_menu(menu);
menu.show_all();

function update_indicator() {
    /* get current time at UTC+8, add 1 to date if after 23:00 (子時) */
    var now = new Date(new Date().getTime() + 8 * 3600 * 1000);
    var hour = now.getUTCHours();
    if(hour >= 23) { // 子時 of the next day
        now = new Date(now.getTime() + 24 * 3600 * 1000);
    }
    var year  = now.getUTCFullYear();
    var month = now.getUTCMonth() + 1;
    var day   = now.getUTCDate();
    
    /* obtain date/time in lunar calendar */
    var lunar = LunarCalendar.solarToLunar(year, month, day);
    lunar.hour = '子丑寅卯辰巳午未申酉戌亥'[Math.floor((hour + 1) % 24 / 2)];
    
    /* output formatting */
    var compact_date = lunar.lunarMonthName + lunar.lunarDayName;
    var long_date = lunar.GanZhiYear + '年（' + lunar.zodiac + '年）\n' +
                    lunar.lunarMonthName + lunar.lunarDayName;
    if(lunar.term) { // add solar term (節氣) to output if at solar term
        compact_date += '　' + lunar.term;
        long_date += '　' + lunar.term;
    }
    long_date += '\n' + lunar.hour + '時';
    
    /* output to indicator */
    indicator.set_icon(__dirname + '/icons/' + lunar.zodiac + '.svg');
    indicator.set_label(compact_date, '');
    item.set_label(long_date);
}

var job = new CronJob({
    cronTime: '0 * * * *', // every hour
    onTick: update_indicator,
    start: true
});

update_indicator();

/* Detect resume from suspend and update date/time */
var bus = DBus.systemBus();
var service = bus.getService('org.freedesktop.login1');
service.getInterface(
    '/org/freedesktop/login1',
    'org.freedesktop.login1.Manager',
    function(err, nm) {
        nm.addListener('PrepareForSleep', function(arg) {
            // PrepareForSleep returns false when resuming from suspend
            if(!arg) {
                job.stop(); // force cronjob to recalculate time
                job.start();
                update_indicator();
            }
        });
    }
);

Gtk.main();
