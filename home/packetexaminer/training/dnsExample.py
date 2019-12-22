#!/usr/bin/env python3
# File    : pcap_analytics.py
# Author  : Joe McManus josephmc@alumni.cmu.edu
# Version : 0.1  09/04/2018 Joe McManus
# Copyright (C) 2018 Joe McManus

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


from scapy.all import *
import json

packets = rdpcap("example.pcap")

queryClients = {}
for pkt in packets:
    if IP in pkt:
        if pkt.haslayer(DNS) and pkt.getlayer(DNS).qr == 0:
            lookup=(pkt.getlayer(DNS).qd.qname).decode("utf-8")
            # print(lookup)
            if lookup in queryClients:
                if pkt[IP].src not in queryClients[lookup]:
                    queryClients[lookup]['ip'].append(pkt[IP].src)
                    queryClients[lookup]['count']+=1
            else:
                queryClients[lookup] = {'ip':[],'count':1}

print(json.dumps(queryClients))
