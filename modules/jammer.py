#!/usr/bin/env python3
# coding=UTF-8

from modules.utils import color


class Jam(object):
    name = "Denial of Service Module."
    desc = "Disabled in this build."
    version = "2.0"

    def __init__(self):
        pass

    def _disabled(self):
        print(color("[!] DOS module is disabled in this build.", "red"))

    def dnsdropstart(self, host):
        self._disabled()

    def dnsdropstop(self):
        self._disabled()

    def dnsamplificationstart(self, tgt):
        self._disabled()

    def synfloodstart(self, host, tgt, dport):
        self._disabled()

    def udpfloodstart(self, host, tgt, dport):
        self._disabled()

    def teardrop(self, target):
        self._disabled()

    def landstart(self, target, port):
        self._disabled()

    def icmpfloodstart(self, host, tgt):
        self._disabled()

    def pingofdeathstart(self, target):
        self._disabled()

    def icmpsmurfstart(self, tgt):
        self._disabled()

    def dhcpstarvationstart(self):
        self._disabled()
