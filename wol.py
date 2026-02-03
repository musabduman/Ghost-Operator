import sys
import socket
import struct
import config
hedef_mac=config.mac
def wake_on_lan(macaddres):
    if len(macaddres)==17:
        sep=macaddres[2]
        macaddres=macaddres.replace(sep,'')
    data=b'ff'*6+(macaddres*16).encode()
    send_data='b'
    for i in range(0,len(data),2):
        send_data += struct.pack('B',int(data[i:i +2],16))
    
    sock=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET,socket.SO_BROADCAST,1)
    sock.sendto(send_data,('255.255.255.255',9))
    print(f"Sihirli paket gönderildi! Bilgisyar açılıyor..")
if __name__=="__main__":
    try:
        wake_on_lan(hedef_mac)
    except Exception as e:
        print(f"hata {e}")
