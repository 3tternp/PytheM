#!/usr/bin/env python3
# coding=UTF-8

# Copyright (c) 2016 Angelo Moura
#
# This file is part of the program PytheM
#
# PytheM is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307
# USA

import os
import re
import sys
import socket
import struct
import base64
from urllib.parse import unquote

try:
    import fcntl
except Exception:
    fcntl = None

try:
    import termcolor
except Exception:
    termcolor = None


def decode(base):
    text = input("[*] String to be decoded: ")
    decode = text.decode('{}'.format(base))
    result = "[+] Result: {}".format(decode)
    return result

def encode(base):
    text = input("[*] String to be encoded: ")
    encode = text.encode('{}'.format(base))
    result = "[+] Result: {}".format(encode)
    return result

def cookiedecode():
    cookie = input("[+] Enter the cookie value: ")
    res = base64.b64decode(unquote(cookie))
    print(res)

def get_myip(interface):
    if fcntl is None:
        raise OSError("fcntl is not available on this platform")
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    if isinstance(interface, str):
        interface = interface.encode()
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,
        struct.pack('256s', interface[:15])
    )[20:24])


def credentials(users,passwords):
    if users:
        for u in users:
            print("[$] Login found: {}".format(str(u[1])))
    if passwords:
        for p in passwords:
            print("[$] Password found: {}".format(str(p[1])))

    if not users and not passwords:
        print("[#] No accounts on the pot try again later.")


user_regex = '([Ee]mail|[Uu]ser|[Uu]sr|[Uu]sername|[Nn]ame|[Ll]ogin|[Ll]og|[Ll]ogin[Ii][Dd])=([^&|;]*)'
pw_regex = '([Pp]assword|[Pp]ass|[Pp]wd|[Pp]asswd|[Pp]wd|[Pp][Ss][Ww]|[Pp]asswrd|[Pp]assw)=([^&|;]*)'

def credentials_harvest(file):
    path = os.getcwd()
    if file is None:
        file = path + "/sslstrip.log"
    else:
        file = path + "/" + file
    print("[$] Credential Harvester:")
    #try:
    f = open(file,"r+")
    content = f.read().replace('\n','')
    #except:
        #print "[!] Problem reading the sslstrip log"
    users = re.findall(user_regex, content)
    passwords = re.findall(pw_regex, content)
    credentials(users,passwords)

def get_mymac(interface):
        if fcntl is None:
                raise OSError("fcntl is not available on this platform")
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        if isinstance(interface, str):
                interface = interface.encode()
        info = fcntl.ioctl(s.fileno(), 0x8927,  struct.pack('256s', interface[:15]))
        return ':'.join(f"{b:02x}" for b in info[18:24])


def set_ip_forwarding(value):
    with open('/proc/sys/net/ipv4/ip_forward', 'w') as file:
        file.write(str(value))
        file.close()
        print("[*] Setting the packet forwarding.")
def iptables():
    os.system('iptables -P INPUT ACCEPT && iptables -P FORWARD ACCEPT && iptables -F && iptables -X && iptables -t nat -F && iptables -t nat -X')
    print("[*] Iptables redefined")


def module_check(module):
    confirm = input("[-] Do you checked if your system has [%s] installed?, do you like to try installing? (apt-get install %s will be executed if yes [y/n]: " % (modules,module))
    if confirm == 'y':
        os.system('apt-get install %s' % module)
    else:
        print("[-] Terminated")
        sys.exit(1)

def color(message,color):
    if termcolor is None:
        return str(message)
    return termcolor.colored(str(message), str(color), attrs=["bold"])

def banner(version):
    banner = """\n

                      ---_ ...... _/_ -
                     /  .      ./ .'*  '
                     |''         /_|-'  '.
                    /                     )
                  _/                  >   '
                 /   .   .       _.-" /  .'
                 \           __/"   /  .'
                  \ '--  .-" /     / /'
                   \|  \ | /     / /
                        \:     / /
                     `\/     / /
                      \__`\/ /
                         \_ '



         [ PytheM - Penetration Testing Framework v{} ]\n
""".format(version)
    return color(banner,"blue")


def print_help():
    print(color("[*] help:            Print the help message.","blue"))
    print()
    print(color("[*] exit/quit:         Leave the program.","blue"))
    print()
    print(color("[*] set                Set a variable's value.","blue"))
    print(color(" parameters:","red"))
    print(color("  - interface","yellow"))
    print(color("  - gateway","yellow"))
    print(color("  - target","yellow"))
    print(color("  - file","yellow"))
    print(color("  - arpmode","yellow"))
    print(color("  - domain","yellow"))
    print(color("  - redirect","yellow"))
    print(color("  - script","yellow"))
    print(color("  - filter","yellow"))
    print(color(" examples:","green"))
    print(color("  pythem> ","red") + "set interface         | open input to set")
    print("     or")
    print(color("  pythem> ","red") + "set interface wlan0   | don't open input to set value.")
    print()
    print(color("[*] print          Print a variable's value.","blue"))
    print(color(" examples:","green"))
    print(color("  pythem> ","red") + "print gateway")
    print()
    print(color("[SECTION - NETWORK, MAN-IN-THE-MIDDLE AND DENIAL OF SERVICE (DOS)]","grey"))
    print()
    print(color("[*] scan           Make a tcp/manual/arp scan.","blue"))
    print("Should be called after setting an interface and a target")
    print(color(" examples:","green"))
    print(color("  pythem> ","red") + "scan")
    print("  [*] Select one scan mode, options = tcp/arp/manual")
    print("  [+] Scan mode: arp")
    print("     or")
    print(color("  pythem> ","red") + "scan tcp")
    print(color("  pythem> ","red") + "scan manual")
    print("  [+] Enter the port, ports (separated by commas): 21,22,25,80")
    print()
    print(color("[*] arpspoof           Start or stop an arpspoofing attack.","blue"))
    print("Optional setting arpmode to select arpspoofing mode should be filled with rep or req")
    print("rep to spoof responses, req to spoof requests")
    print(color(" arguments:","red"))
    print(color("  - start","yellow"))
    print(color("  - stop","yellow"))
    print(color("  - status","yellow"))
    print(color("  - help","yellow"))
    print(color(" examples:","green"))
    print(color("  pythem> ","red") + "arpspoof start")
    print(color("  pythem> ","red") + "arspoof stop")
    print(color("  pythem> ","red") + "arpspoof status")
    print()
    print(color("[*] dnsspoof           Start a dnsspoofing attack.","blue"))
    print("Should be called after an ARP spoofing attack has been started")
    print(color(" arguments:","red"))
    print(color(" - start","yellow"))
    print(color(" - stop","yellow"))
    print(color(" - status","yellow"))
    print(color(" - help","yellow"))
    print(color(" examples:","green"))
    print(color("  pythem> ","red")+ "dnsspoof start")
    print(color("  pythem> ","red") + "dnsspoof stop")
    print(color("  pythem> ","red") + "dnsspoof status")
    print()
    print(color("[*] dhcpspoof          Start a DHCP ACK Injection spoofing attack.","blue"))
    print("If the real DHCP server ACK is faster than your host the spoofing will not work, check it with the sniffer")
    print(color(" arguments:","red"))
    print(color(" - start","yellow"))
    print(color(" - stop","yellow"))
    print(color(" - status","yellow"))
    print(color(" - help","yellow"))
    print(color(" examples:","green"))
    print(color("  pythem> ","red") + "dhcpspoof start")
    print(color("  pythem> ","red") + "dhcpspoof stop")
    print(color("  pythem> ","red") + "dhcpspoof status")
    print()
    print(color("[*] bdfproxy           Start BDFProxy and Metasploit combo.","blue"))
    print(color("           by:Joshua Pitts_|       |_by: rapid7","red"))
    print("Should be called after an ARP spoofing attack has been started.")
    print(color(" exmample:","green"))
    print(color("  pythem> ","red") + "bdfproxy")
    print()
    print(color("[*] hstsbypass         Start sslstrip+ and dns2proxy","blue"))
    print(color("   by:LeonardoNve && M.Marlinspike _|       |_by:LeonardNve","red"))
    print("Should be called after an ARP spoofing attack has been started.")
    print(color(" example:","green"))
    print(color("  pythem> ","red") + "hstsbypass")
    print()
    print(color("[*] harvest            Harvest credentials inside file, default file: sslstrip.log","blue"))
    print(color(" example:","green"))
    print(color("  pythem> ","red") + "harvest")
    print()
    print(color("[*] inject         Start to redirect clients to web server with a script tag to inject in html response","blue"))
    print("Should be used after a ARP spoof has been started")
    print(color(" arguments:", "red"))
    print(color("  - start","yellow"))
    print(color("  - stop","yellow"))
    print(color("  - help","yellow"))
    print(color(" examples:","green"))
    print(color("  pythem> ","red") + "inject start")
    print(color("  pythem> ","red") + "inject stop")
    print()
    print(color("[*] sniff          Start to sniff network traffic on desired network interface","blue"))
    print("Should be called after setting an interface")
    print(color(" sniff custom filters:","red"))
    print(color("  - http","yellow"))
    print(color("  - dns","yellow"))
    print(color("  - core","yellow"))
    print(color(" examples:","green"))
    print(color("  pythem> ","red")+ 'sniff http')
    print("     or")
    print(color("  pythem> ","red")+ 'sniff')
    print("  [+] Enter the filter: port 1337 and host 10.0.1.5  | tcpdump like format or http,dns,core specific filter.")
    print()
    print(color("[*] pforensic          Start a packet-analyzer","blue"))
    print("Should be called after setting file with a .pcap file")
    print(color(" examples:","green"))
    print(color("  pythem> ","red") + 'pforensic')
    print(color("  pforensic> ","yellow") + 'help')
    print()
    print(color("[*] dos                Start a Denial of Service attack (DOS).","blue"))
    print(color(" arguments:","red"))
    print(color("  - dnsdrop           | Start to drop DNS queries that pass through man-in-the-middle traffic.","yellow"))
    print(color("  - dnsamplification  | Start a DNS amplification attack on target address with given DNS servers to amplificate.","yellow"))
    print(color("  - synflood       | Start a SYN flood attack on target address, default port = 80, set port to change.","yellow"))
    print(color("  - udpflood       | Start a UDP flood attack on target address, default port = 80, set port to change.","yellow"))
    print(color("  - teardrop          | Start a UDP teardrop fragmentation attack.","yellow"))
    print(color("  - land       | Start a LAND attack on target address, default port = 80, set port to change.","yellow"))
    print(color("  - icmpflood          | Start a ICMP flood attack on target address.","yellow"))
    print(color("  - pingofdeath        | Start a ping of death (P.O.D) attack on target address.","yellow"))
    print(color("  - icmpsmurf          | Start a ICMP smurf attack on target host. Send echo-requests to hosts with spoofed target address.","yellow"))
    print(color("  - dhcpstarvation    | Start a DHCP starvation attack on network DHCP server. Multiple spoofed MAC dhcp discovers.","yellow"))
    print(color(" examples:","green"))
    print(color("  pythem> ","red") + "dos dnsdrop")
    print(color("  pythem> ","red") + "dos synflood help")
    print()
    print(color("[SECTION - EXPLOIT DEVELOPMENT AND REVERSE ENGINERING]","grey"))
    print()
    print(color("[*] xploit         Interactive stdin or tcp exploit development shell.","blue"))
    print("The stdin should be called after setting file")
    print("The tcp should be called after setting target")
    print(color(" arguments:","red"))
    print(color("  - stdin    | set file before","yellow"))
    print(color("  - tcp        | set target before","yellow"))
    print(color(" examples:","green"))
    print(color("  pythem> ","red") + "set file ./exec")
    print(color("  pythem> ","red") + "xploit stdin")
    print(color("  xploit> ","blue") + "help")
    print("     or")
    print(color("  pythem> ","red") + "xploit")
    print("  [*] Select one xploit mode, options = stdin/tcp")
    print("  [+] Exploit mode: stdin")
    print(color("  xploit> ","blue") + "help")
    print()
    print(color("[SECTION - BRUTE-FORCE]","grey"))
    print()
    print(color("[*] brute          Start a brute-force attack.","blue"))
    print("Should be called after setting a target and a wordlist file path")
    print(color(" arguments:","red"))
    print(color("  - ssh      | ip address as target","yellow"))
    print(color("  - url        | url (with http:// or https://) as target","yellow"))
    print(color("  - form   | url (with http:// or https://) as target","yellow"))
    print(color(" examples:","green"))
    print(color("  pythem> ","red") + "brute webform")
    print(color("  pythem> ","red") + "brute ssh help")
    print()
    print(color("[SECTION - UTILS]","grey"))
    print(color("[*] geoip            Approximately geolocate the location of a IP address.","blue"))
    print("Should be called after setting target(ip address)")
    print(color(" examples:","green"))
    print(color("  pythem> ","red") + "geoip")
    print("     or")
    print(color("  pythem> ","red") + "geoip 8.8.8.8")
    print()
    print(color("[*] decode and encode      Decode or encode a string with a chosen pattern.","blue"))
    print(color(" examples:","green"))
    print(color("  pythem> ","red") + "decode base64")
    print(color("  pythem> ","red") + "encode ascii")
    print()
    print(color("[*] cookiedecode       Decode a base64 url encoded cookie value.","blue"))
    print(color(" example:","green"))
    print(color("  pythem> ","red") + "cookiedecode")
    print()
    print(color("* Anything else will be executed in the terminal like ls, nano, cat, etc. *","yellow"))
    print(color("by: ","red") + color("m4n3dw0lf","blue"))
    print()
