# PiPresenter Installation

## Get Raspbian
Download [https://www.raspberrypi.org/downloads/raspbian/](Raspbian Jessie Lite), unzip it and dd it to your sdcard, e.g.:
```
unzip YYYY-MM-DD-raspbian-jessie-lite.zip
sudo dd if=YYYY-MM-DD-raspbian-jessie-lite.img of=/dev/sdc
# Do you know the sudo killall -USR1 dd trick?
```

## Assemble the Pi
1. Plug the touchscreen on your Pi.
2. Connect the Pi to a monitor.
3. Connect the Pi to a keyboard.
4. A mouse might be helpful, but is not required.
5. Insert the sdcard.
6. Connect your Pi to the power supply.

## Raspbian Installation
1. Log in (defaults are pi/raspberry)
2. `sudo raspi-config`
3. Expand Filesystem
4. Change password of pi to something secure
5. i18n options: Whatever you need
6. Advanced
7. Enable SPI
8. *Optional:* SSH
9. Finish and reboot

## Internet Access
Setup your internet access.
There are a lot of tutorials (e.g. [https://www.raspberrypi.org/documentation/configuration/wireless/wireless-cli.md](the official one)) out there, so I won't do another one.

## Touchscreen
In case of the Kuman touchscreen, it's just a matter of following the instructions on the CD.
PiPresenter is optimized for a resolution of 480x320px.

## Actual Installation
1. Install git: `sudo apt-get install git`
2. Clone the source to `/opt/pipresenter`.
3. Own that folder as user pi.
4. Create folder `work` and do `chmod 777 work`.
5. `sudo apt-get update`, install packages from `material/packages`
6. You have to downgrade libsdl because the jessie version is bugged. Use `material/usewheezysdl.sh` for that.
7. Install the udev rules. They symlink the touchscreen to `/dev/input/touchscreen` and block all but mass storages on usb port 1.4 (if you look onto the LAN and USB ports, it is the top right one): `sudo cp /opt/pipresenter/material/01-pipresenter.rules /etc/udev/rules.d/`
8. Reboot
9. Calibrate the touchscreen: `sudo TSLIB_FBDEVICE=/dev/fb1 TSLIB_TSDEVICE=/dev/input/touchscreen ts_calibrate`
(You do not need to calibrate X)
10. Copy onstick.sh and onstickremove.sh to /root, make them executable and add them to usbmount.
  This goes to `/etc/usbmount/mount.d/00_create_model_symlink` before `exit 0`:
  ```
  # OnStick event
  /root/onstick.sh
  ```
  And this to `/etc/usbmount/mount.d/00_remove_model_symlink` before `exit 0`:
  ```
  # OnStickRemove Event
  /root/onstickremove.sh
  ```
  There are examples in `material/`.

11. Create user present without a password: 
  ```
  sudo adduser present
  sudo passwd -d present
  ```
12. Add present to necessary groups: 
  ```
  sudo adduser present video
  sudo adduser present users
  sudo adduser present input
  ```
13. Copy `material/.bashrc` and `material/.xinitrc` to `/home/present` and chown them for pi and make them read-only using chmod.
14. Setup auto-login: `sudo cp -r material/getty@tty1.service.d /etc/systemd/system/`

