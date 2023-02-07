import argparse, socket, struct

def usage():
    print("Before execute, you should change your wlan to monitor mode")
    print("Usage: sudo python signal-strength.py <interface> <mac address>")
    print("Please press Ctrl+C to stop")

class AP:
    def __init__(self, interface, ap_mac):
        self.interface = interface
        self.mac = ap_mac
        self.pwr = None

    def packetDump(self):
        packet = None
        try:
            s = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.htons(0x0003))
            s.bind((self.interface, 0x0003))
            packet = s.recvfrom(2048)[0]
        except:
            print("Fail")
        return packet

    def checkStrength(self):
        pkt = ap.packetDump()
        rt_hlen = struct.unpack('>bb', pkt[2:4])
        if rt_hlen == 0:
            return None
        f_80211 = pkt[rt_hlen[0]:]

        if f_80211[0:1] == b'\x80':
            ta = f_80211[16:22].hex().upper()
            #print('ta: ', ta, 'type(ta)', type(ta))
            ta = ':'.join(ta[i:i+2] for i in range(0, 12, 2))
            #print('ta: ', ta, 'type(ta)', type(ta))
            if ta == self.mac:
                self.pwr = int.from_bytes(pkt[18:19], "big", signed=True)
                print(f"ta = {ta}, signal-strength: {self.pwr}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('interface', help=' : Interface')
    parser.add_argument('mac', metavar='MAC', help=' : AP MAC')
    args = parser.parse_args()
    usage()

    if (args.interface is None) or (args.mac is None):
        print("Insufficient Args")
        usage()
        exit()
    else:
        ap = AP(args.interface, args.mac)
        try:
            while True:
                ap.checkStrength()
        except KeyboardInterrupt:
            print("Stopped")

