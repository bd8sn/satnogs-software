#!/bin/sh
#
# SatNOGS rotator stress test script
#
# Copyright (C) 2015 Vasilis Tsiligiannis <acinonyx@openwrt.gr>
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

SETTLE_SLEEP=1

assert()
{
	cat <<EOF
Software Failure. Press left mouse button to continue
Guru Meditation #00000SAT.NOGS0000
EOF
}

usage()
{
	cat <<EOF
Usage: $0 hostname port

Parameters:
    hostname	host where rotctld runs
    port	port where roctld listens on
EOF
}

send_command()
{
	if [ $# -lt 3 ]; then
		assert
		exit 1
	fi
	hostname="$1"
	port="$2"
	shift 2
	command="$@"

	case $command in
		P*|p*|S*|R*)
			echo "$command" | nc "$hostname" "$port" 2>/dev/null
			;;
		*)
			;;
	esac
}


wait_for_settle()
{
	if [ $# -lt 3 ]; then
		assert
		exit 1
	fi
	hostname="$1"
	port="$2"
	sleep="$3"

	_curr="$(send_command $hostname $port p)"
	while [ "$_curr" != "$_prev" ]; do
		sleep $(($sleep))
		_prev="$_curr"
		_curr="$(send_command $hostname $port p)"
	done
}

stress()
{
	if [ $# -lt 2 ]; then
		usage
		exit 1
	fi

	while read _command; do
		if [ "${_command#+}" = "P" ]; then
			_command="$_command $(($(hexdump -n 2 -e '/2 "%u\n"' /dev/urandom) % 360)) $(($(hexdump -n 2 -e '/2 "%u\n"' /dev/urandom) % 90))"
		fi
		case $_command in 
			+*)
				;;
			s*)
				sleep $((${_command#s}))
				;;
			*)
				wait_for_settle "$1" "$2" "$SETTLE_SLEEP"
				;;
		esac
		_command="${_command#+}"
		send_command "$1" "$2" "$_command"
	done
}

stress "$1" "$2"
