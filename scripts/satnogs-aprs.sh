#!/bin/sh
#
# APRS decoding shell script
#
# Copyright (C) 2014 Vasilis Tsiligiannis <acinonyx@openwrt.gr>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

PPM=45
FREQ=144800k
SAMPRATE=22050
FIFO=/tmp/satnogs

if [ ! -e "$FIFO" ]; then
	echo "Warning: FIFO file does not exists. Creating it at $FIFO..."
	mkfifo "$FIFO"
fi

# Play audio from named pipe
aplay -t raw -r "$SAMPRATE" -f S16_LE -t raw -c 1 "$FIFO" &

# Convert to typical APRS message format
rtl_fm -p "$PPM" -f "$FREQ" -s "$SAMPRATE" | \
	tee "$FIFO" | \
	multimon -q -a AFSK1200 -t raw /dev/stdin | \
	sed ':a;N;/AFSK1200: /! ba;s/\n/msg/g;s/AFSK1200: fm \(\S\+\) to \(\S\+\) via \(\S\+\) .*msg/\1>\2,\3:/;s/AFSK1200: fm \(\S\+\) to \(\S\+\) .*msg/\1>\2:/'

