# RySpy
RySpy is a demo project controlling a Pan-Tilt MIPI Camera module on a headless NanoPi M4.  

## Parts
* [NanoPi M4](https://www.friendlyarm.com/index.php?route=product/product&product_id=234): Small board computer
  * USB-C power cable
  * SD Card 
* [Pan-Tilt HAT](https://www.waveshare.com/pan-tilt-hat.htm): 2-DOF Servo Kit
* [13.2MP MIPI Camera](https://www.friendlyarm.com/index.php?route=product/product&product_id=228): 4224 x 3136 photographing and 13.2MP@30fps video recording.recording

## Setup

These instructions we made using my exact steps and will and may differ if you are using other equipment. 

### NanoPi M4 FriendlyDesktop
1. [Download Image](http://download.friendlyarm.com/NanoPiM4)
   * rk3399-sd-friendlydesktop-bionic-4.4-arm64-YYYYMMDD.img.zip
2. Unzip and follow the [Raspberry Pi Installation Intructions](https://www.raspberrypi.org/documentation/installation/installing-images/)
3. Plugin SD Card to NanoPi and power up
   * <code>ssh pi@NanoPi-M4</code>
     * Username: Pi
     * Password: Pi
     * You may need to look at your router to see what IP address it was assigned.
   * Alternatively you can us an HDMI monitory and it should auto login 
4. Update and install any normal Linux packages you like

```
sudo apt update && sudo apt upgrade
```

5. Disable LightDM if going Headless 

```
sudo systemctl stop lightdm
sudo systemctl mask lightdm
```

6. Disable the stupid green status LED. Add this to `/etc/rc.local`

```
echo none > /sys/class/leds/status_led/trigger"
```
   

See [NanoPi M4 Wiki](http://wiki.friendlyarm.com/wiki/index.php/NanoPi_M4) for more information
 
### VNC Headless Setup
1. Install TigerVNC

```sudo apt install tigervnc-common tigervnc-viewer tigervnc-standalone-server tigervnc-xorg-extension```

2. Setup Password

```
vncserver
```

3. Stop vncserver to setup the Desktop Environment 

```
vncserver -kill :*
```

4. Edit the VNC statup script to initialize LXDE

```
cat > ~/.vnc/xstartup << EOF 
#!/bin/sh 
/usr/bin/terminator &
/usr/bin/startlxde &

# Used display 0 for headless
vncserver :0 -localhost no
EOF

chmod +x ~/.vnc/xstarxtup
```


   * Still does not autstart at boot up for me. I need to ssh in and execute `vncserver` first. If you have a better way please let me know



5. Instal VNC Client Viewer
   * [Download RealVNC](https://www.realvnc.com/en/connect/download/vnc/)
  
## Pan-Tilt Setup
1. Install smbus to talk to the servo board over I2C
   
```
sudo apt -y install python-smbus
```

## Contribute
Please feel free to contribute pull requests or create issues for bugs and feature requests.

## Author
* Ryan (https://github.com/ryans-git)

## Credits
* [SunFounder PCA9685](https://github.com/sunfounder/SunFounder_PCA9685): PWM Servo Board Controlller 
