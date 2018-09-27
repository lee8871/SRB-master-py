import usb.core
import usb.util
import time


# find our device
dev = usb.core.find(idVendor=0x16c0, idProduct=0x05dc)

# was it found?
if dev is None:
    raise ValueError('Device not found')

# set the active configuration. With no arguments, the first
# configuration will be the active one
dev.set_configuration()

cfg = dev.get_active_configuration()
print('config number: ' + str(cfg.bConfigurationValue))
for intf in cfg:
    print('interface: ' + str(intf.bInterfaceNumber) + ',' + str(intf.bAlternateSetting))
    for ep in intf:
        print('endpoint: ' + str(ep.bEndpointAddress))
print('\n\n')

intf =  cfg[(0,0)]
ep_write =  intf[1]
ep_read =  intf[0]
print('endpoint read is '+ str(ep_read.bEndpointAddress))
print('endpoint write is '+ str(ep_write.bEndpointAddress))

speed_a = 90;
speed_b = -200;

while True:
    speed_a = speed_a+1;
    if speed_a>120:
        speed_a = 90
        time.sleep(3);
        pass
    write_d = [0,10,(0<<5)+4,(speed_a%256),int(speed_a/256),(speed_a%256),int((speed_a)/256)];

#    two_motor(addr = 10,speedA = 100, speedB = -300);


    print(str(write_d))
    ep_write.write(write_d)
    time.sleep(0.1);
    read_d =  ep_read.read(64,100)
    print(str(read_d))
    pass
