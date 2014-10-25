#!/bin/sh
#
# SatNOGS ground station script
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

# rigctld settings
USE_RIGCTLD=1
PORT=/dev/ttyUSB0
MODEL=202
BAUD=19200

# rtl_tcp settings
USE_RTLTCP=1
BUFFERS=5
LL_BUFFERS=20

# Do not edit bellow
#

# Bring up rotctl daemon
[ "$USE_RIGCTLD" = 1 ] && {
	killall -q rotctld
	rotctld -m $MODEL -s $BAUD -t $PORT &
}

# Bring up rtl_tcp
[ "$USE_RTLTCP" = 1 ] && {
	killall -q rtl_tcp
	sleep 5 # wait for possible threads to terminate
	rtl_tcp -n $LL_BUFFERS -b $BUFFERS &
}
