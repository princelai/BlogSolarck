---
title: 加密公共DNS
date: 2021-09-24T14:31:11+08:00
draft: false
isCJKLanguage: true
toc: true
categories:
- 电脑与网络
tags:
- dns
- DoH
- DoT
---

# 常用DoH和DoT公共DNS
DoH即[DNS over HTTPS](https://zh.wikipedia.org/wiki/DNS_over_HTTPS)，DoT即[DNS over TLS](https://zh.wikipedia.org/wiki/DNS_over_TLS)，均使用SSL/TLS技术加密DNS请求，防止中间人攻击、劫持，提高网络安全性。

下面仅列举一些常用的DoH、DoT地址：
|  名称   |                                DoH                                |       DoT       |
| :-----: | :---------------------------------------------------------------: | :-------------: |
|  阿里   | https://223.5.5.5/dns-query</br> https://dns.alidns.com/dns-query | dns.alidns.com  |
|  腾讯   |                     https://doh.pub/dns-query                     |     dot.pub     |
| google  |                   https://dns.google/dns-query                    |   dns.google    |
| AdGuard |                 https://dns.adguard.com/dns-query                 | dns.adguard.com |

更详细的列表内容可以在[国内公共DNS服务器 IP 地址](https://dns.iui.im/)查看

# DoH和DoT的测速

传统DNS测速上，通常使用`dig`命令，但`dig`不支持加密的DNS，DoH和DoT测速最简单的方法是使用`dog`[命令](https://github.com/ogham/dog)。

### 1. 对于DoH
```bash
dog -H @https://dns.google/dns-query google.com --time
```

### 2. 对于DoT
```bash
dog google.com --tls @dns.google --time
```

### 3. dog全部参数
```bash
dog --help
```
输出
```
dog ● command-line DNS client

Usage:
  dog [OPTIONS] [--] <arguments>

Examples:
  dog example.net                          Query a domain using default settings
  dog example.net MX                       ...looking up MX records instead
  dog example.net MX @1.1.1.1              ...using a specific nameserver instead
  dog example.net MX @1.1.1.1 -T           ...using TCP rather than UDP
  dog -q example.net -t MX -n 1.1.1.1 -T   As above, but using explicit arguments

Query options:
  <arguments>              Human-readable host names, nameservers, types, or classes
  -q, --query=HOST         Host name or IP address to query
  -t, --type=TYPE          Type of the DNS record being queried (A, MX, NS...)
  -n, --nameserver=ADDR    Address of the nameserver to send packets to
  --class=CLASS            Network class of the DNS record being queried (IN, CH, HS)

Sending options:
  --edns=SETTING           Whether to OPT in to EDNS (disable, hide, show)
  --txid=NUMBER            Set the transaction ID to a specific value
  -Z=TWEAKS                Set uncommon protocol-level tweaks

Protocol options:
  -U, --udp                Use the DNS protocol over UDP
  -T, --tcp                Use the DNS protocol over TCP
  -S, --tls                Use the DNS-over-TLS protocol
  -H, --https              Use the DNS-over-HTTPS protocol

Output options:
  -1, --short              Short mode: display nothing but the first result
  -J, --json               Display the output as JSON
  --color, --colour=WHEN   When to colourise the output (always, automatic, never)
  --seconds                Do not format durations, display them as seconds
  --time                   Print how long the response took to arrive

Meta options:
  -?, --help               Print list of command-line options
  -v, --version            Print version information

```

# 参考
[How to query for DNS over HTTPS/DNS over TLS using command line?](https://superuser.com/questions/1532975/how-to-query-for-dns-over-https-dns-over-tls-using-command-line)