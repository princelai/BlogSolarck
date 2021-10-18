---
title: "Gnome_wayland_on_nvidia"
date: 2021-10-18T22:40:29+08:00
draft: true
isCJKLanguage: true
toc: true
categories:
- 电脑与网络
tags:
- 
---

```
yay -Syu --needed xorg-xwayland libxcb egl-wayland nvidia-dkms
```

```
vim  /usr/lib/udev/rules.d/61-gdm.rules 
```
```
# disable Wayland on Hi1710 chipsets
ATTR{vendor}=="0x19e5", ATTR{device}=="0x1711", RUN+="/usr/lib/gdm-runtime-config set daemon WaylandEnable false"
# disable Wayland when using the proprietary nvidia driver
# DRIVER=="nvidia", RUN+="/usr/lib/gdm-runtime-config set daemon WaylandEnable false"
# disable Wayland if modesetting is disabled
IMPORT{cmdline}="nomodeset", RUN+="/usr/lib/gdm-runtime-config set daemon WaylandEnable false"
```


```bash
gsettings set org.gnome.mutter experimental-features '["scale-monitor-framebuffer"]'
```

## 参考
[Use wayland with propietary nvidia drivers](https://forum.manjaro.org/t/howto-use-wayland-with-propietary-nvidia-drivers/36130)