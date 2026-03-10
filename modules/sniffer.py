#!/usr/bin/env python3
# coding=UTF-8

import os
import time

from scapy.all import sniff, wrpcap

from modules.utils import color


class Sniffer(object):
    name = "Sniffer"
    desc = "Scapy sniffer"
    version = "2.0"

    def __init__(self, interface, filter, path):
        self.path = path
        self.interface = interface
        self.filter = filter
        self.packetcounter = 0
        self._packets = []
        self._write_pcap = False

        try:
            answer = input(
                "[*] Wish to write a .pcap file with the sniffed packets in the actual directory?[y/n]: "
            ).strip().lower()
            self._write_pcap = answer == "y"
        except KeyboardInterrupt:
            self._write_pcap = False

    def _on_packet(self, p):
        self.packetcounter += 1
        self._packets.append(p)
        print(
            "\n------------------------------[PACKET N:{}]------------------------------".format(
                self.packetcounter
            )
        )
        try:
            p.show()
        except Exception:
            print(color("[!] Failed to render packet.", "red"))
        print("-------------------------------------------------------------------------\n")

    def start(self):
        try:
            if self.filter:
                sniff(iface=self.interface, filter=str(self.filter), prn=self._on_packet, store=False)
            else:
                sniff(iface=self.interface, prn=self._on_packet, store=False)
        except KeyboardInterrupt:
            pass
        finally:
            if self._write_pcap and self._packets:
                try:
                    out_dir = os.path.join(self.path, "log")
                    os.makedirs(out_dir, exist_ok=True)
                    ts = time.strftime("%Y%m%d-%H%M%S")
                    out_path = os.path.join(out_dir, f"sniff-{ts}.pcap")
                    wrpcap(out_path, self._packets)
                    print(color(f"[+] Saved pcap: {out_path}", "yellow"))
                except Exception as e:
                    print(color(f"[!] Failed to save pcap: {e}", "red"))
