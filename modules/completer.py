try:
    import readline
except Exception:
    readline = None


class Completer(object):
    name = "TAB completer"
    desc = "Auto complete PytheM commands with tab"
    version = "0.3"

    def __init__(self, console):
        if readline is None:
            return
        readline.parse_and_bind("tab: complete")
        if console == "pythem":
            readline.set_completer(self.pythem)

    def suboption(self, text, state):
        results = [x for x in self.suboptions if x.startswith(text)] + [None]
        return results[state]

    def pythem(self, text, state):
        if "set" in text and state == 1:
            self.suboptions = [
    'interface',
    'arpmode',
    'target',
    'gateway',
    'file',
    'domain',
    'port',
    'script',
    'redirect',
     'help']
            readline.set_completer(self.suboption)

        elif "print" in text and state == 1:
            self.suboptions = [
    'interface',
    'arpmode',
    'target',
    'gateway',
    'file',
    'domain',
    'port',
    'script',
    'redirect',
     'help']
            readline.set_completer(self.suboption)

        elif "scan" in text and state == 1:
            self.suboptions = ['tcp', 'arp', 'manual', 'help']
            readline.set_completer(self.suboption)

        elif "arpspoof" in text and state == 1:
            self.suboptions = ['start', 'stop', 'status', 'help']
            readline.set_completer(self.suboption)

        elif "dnsspoof" in text and state == 1:
            self.suboptions = ['start', 'stop', 'status', 'help']
            readline.set_completer(self.suboption)

        elif "dhcpspoof" in text and state == 1:
            self.suboptions = ['start', 'stop', 'status', 'help']
            readline.set_completer(self.suboption)

        elif "inject" in text and state == 1:
            self.suboptions = ['start', 'stop', 'status', 'help']
            readline.set_completer(self.suboption)

        elif "xploit" in text and state == 1:
            self.suboptions = ['stdin', 'tcp', 'help']
            readline.set_completer(self.suboption)

        elif "brute" in text and state == 1:
            self.suboptions = ['ssh', 'url', 'form', 'help']
            readline.set_completer(self.suboption)

        elif "dos" in text and state == 1:
            self.suboptions = [
    'dnsdrop',
    'dnsamplification',
    'synflood',
    'udpflood',
    'icmpsmurf',
    'icmpflood',
    'dhcpstarvation',
    'teardrop',
    'pingofdeath',
    'land',
     'help']
            readline.set_completer(self.suboption)

        elif "sniff" in text and state == 1:
            self.suboptions = ['help']
            readline.set_completer(self.suboption)

        elif "pforensic" in text and state == 1:
            self.suboptions = ['help']
            readline.set_completer(self.suboption)

        else:
            self.words = [
    'clear',
    'help',
    'exit',
    'quit',
    'set',
    'print',
    'scan',
    'arpspoof',
    'dnsspoof',
    'inject',
    'sniff',
    'pforensic',
    'dos',
    'xploit',
    'brute',
    'geoip',
    'decode',
    'encode',
    'cookiedecode',
    'hstsbypass',
    'harvest',
    'bdfproxy',
     'dhcpspoof']
            results = [x for x in self.words if x.startswith(text)] + [None]
            return results[state]



