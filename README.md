# indicator-lunar-calendar

An application indicator for Unity that displays the current date and time
in lunar calendar.

Copyright (c) 2016-2019 Adrian I Lam <spam@adrianiainlam.tk> s/spam/me/

*Not to be confused with [indicator-lunar][1], which shows attributes and
ephemerides for astronomical objects.*

[1]: https://launchpad.net/~thebernmeister/+archive/ubuntu/ppa

## Screenshots

![indicator normal][sc1]  
Normal appearance of the indicator

![indicator menu][sc2]  
Menu of the indicator, shown on click

![indicator with solar term][sc3]  
Indicator showing solar term information

Note: The conversion is calculated using timezone UTC+8 (HKT), while the clock
shown above is using timezone UTC+1.

[sc1]: screenshots/sc1.png
[sc2]: screenshots/sc2.png
[sc3]: screenshots/sc3.png

## Dependencies

 - Python 3

 - [LunarCalendarPy][lcp] (included as submodule here)

   Translated from the JavaScript [LunarCalendar][lc] library by GitHub user
   @zzyss86.

   [lc]: https://github.com/zzyss86/LunarCalendar
   [lcp]: https://adrianiainlam.tk/git/?p=LunarCalendarPy.git;a=summary

 - [schedule][schedule]

   Used for periodic update of the indicator.

   [schedule]: https://pypi.org/project/schedule/

 - [dbus-python][dbus]

   Detects suspends/hibernates which would cause incorrect timings
   used by schedule.

   [dbus]: https://pypi.org/project/dbus-python/

This indicator used to be written in JavaScript (node.js) using the
node-gtk package, but it was eventually abandoned, got replaced,
the replacement was abandoned, etc. The situation was a bit too messy
for me so I decided to just rewrite the whole thing in Python, which
would also make installation easier for most standard Ubuntus, and
would use less RAM.


## Usage

 1. Install schedule and dbus-python (`pip install schedule dbus-python`).
 2. Clone this repository (`git clone --recurse-submodules git://adrianiainlam.tk/indicator-lunar-calendar.git`).
 3. Add the script as a startup application.
 4. Run the script manually for the first time. (Alternatively, log out
    and log in again.)
 5. The indicator should be shown at the top right corner, having an icon
    that shows the year and a label that shows the month and date.
 6. Clicking on the indicator should result in a menu with more detailed
    information including the time.

## License

This program is released under the MIT License. For the full text of this
license, please refer to the file "indicator-lunar-calendar.py".
