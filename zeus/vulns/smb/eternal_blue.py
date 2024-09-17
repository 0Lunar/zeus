import socket
import logging


# CVE-2017-0144 - https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2017-0144

def check_eternalblue_vulnerability(target_ip: str, target_port: int = 445, timeout: int | float = 10) -> bool:
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        sock.connect((target_ip, target_port))
        
        smb_negotiation = (
            b"\x00\x00\x00\x90"
            b"\xff\x53\x4d\x42"
            b"\x72\x00\x00\x00\x00\x18\x53\xc8"
            b"\x00\x26\x00\x00\x00\x00\x00\x00"
            b"\x00\x00\x00\x00\x00\x00\xfe\xda"
            b"\x00\x00\x00\x00\x00\x00\x00\x00"
            b"\x00\x62\x00\x02\x50\x43\x20\x4e"
            b"\x45\x54\x57\x4f\x52\x4b\x20\x50"
            b"\x52\x4f\x47\x52\x41\x4d\x20\x31"
            b"\x2e\x30\x00\x02\x4c\x41\x4e\x4d"
            b"\x41\x4e\x31\x2e\x30\x00\x02\x57"
            b"\x69\x6e\x64\x6f\x77\x73\x20\x66"
            b"\x6f\x72\x20\x57\x6f\x72\x6b\x67"
            b"\x72\x6f\x75\x70\x73\x20\x33\x2e"
            b"\x31\x61\x00\x02\x4c\x4d\x31\x2e"
            b"\x32\x58\x30\x30\x32\x00\x02\x53"
            b"\x61\x6d\x62\x61\x00"
        )
        
        sock.send(smb_negotiation)

        response = sock.recv(1024)
        

        if response[68:70] == b"\x11\x03" or response[70:72] == b"\x02\x00":
            return True
        else:
            return False
            
    except Exception as e:
        logging.error(f"[!] Errore: {str(e)}")
    finally:
        sock.close()
