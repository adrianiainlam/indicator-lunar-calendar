# indicator-lunar-calendar

An application indicator for Unity that displays the current date and time
in lunar calendar.

Copyright (c) 2016 Adrian I Lam <adrianiainlam@gmail.com>

*Not to be confused with [indicator-lunar][1], which shows attributes and
ephemerides for astronomical objects.*

[1]: https://launchpad.net/~thebernmeister/+archive/ubuntu/ppa

## Dependencies

 - [Node.js][2]
   
   Note: node-gtk, one of this program's dependencies, requires nodejs version
   5 or above.
   
   [2]: https://nodejs.org/en/

 - [node-gtk][3] (by @WebReflection)
 
   npm package: https://www.npmjs.com/package/node-gtk
   
   Dependencies: build-essential, git, nodejs (>= 5), gobject-introspection,
   libgirepository1.0-dev
   
   Note: This package failed to build for me. I had to remove `-Werror` from
   `cflags` in file "bindings.gyp" to get it to build.
   
   [3]: https://github.com/WebReflection/node-gtk
   
 - [lunar-calendar-zh][4] (by @roadmanfong)

   npm package: https://www.npmjs.com/package/lunar-calendar-zh
   
   Note: This package contains a bug which renders it useless if your computer
   is set to a time zone which observes Daylight Saving. I have forked it and
   fixed it in <https://github.com/adrianiainlam/LunarCalendar>.
   
   [4]: https://github.com/roadmanfong/LunarCalendar
   
 - [node-cron][5] (by @ncb000gt)
 
   npm package: https://www.npmjs.com/package/cron
   
   [5]: https://github.com/ncb000gt/node-cron

## Usage

 1. Install the dependencies listed above.
 2. Clone this repository.
 3. Add the script as a startup application.
 4. Run the script manually for the first time. (Alternatively, log out
    and log in again.)
 5. The indicator should be shown at the top right corner, having an icon
    that shows the year and a label that shows the month and date.
 6. Clicking on the indicator should result in a menu with more detailed
    information including the time.

## License

This program is released under the MIT License. For the full text of this
license, please refer to the file "indicator-lunar-calendar.js".
