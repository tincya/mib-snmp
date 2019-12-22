from scapy.all import *
import json

def dnsCount(pkts):
    queryClients = {}
    for pkt in pkts:
        if IP in pkt:
            if pkt.haslayer(DNS) and pkt.getlayer(DNS).qr == 0:
                lookup=(pkt.getlayer(DNS).qd.qname).decode("utf-8")
                if lookup in queryClients:
                    if pkt[IP].src not in queryClients[lookup]:
                        queryClients[lookup]['ip'].append(pkt[IP].src)
                    queryClients[lookup]['count']+=1
                else:
                    queryClients[lookup] = {'ip':[],'count':1}

    return queryClients

def timeSeries(pkts):
    queryClients = {}

    for pkt in pkts:
        if IP in pkt:
            try:
                pktBytes = pkt[IP].len
                pktTime=datetime.fromtimestamp(pkt.time)
                pktTime=str(int(pktTime.timestamp()))
                if pktTime in queryClients:
                    queryClients[pktTime] += pktBytes
                else:
                    queryClients[pktTime] = pktBytes
            except:
                pass
    return queryClients

def portTraff(pkts, mode='d'):
    queryClients={}

    for pkt in pkts:
        if TCP in pkt:
            pport = pkt[TCP].dport if mode=='d' else pkt[TCP].sport
            if pport in queryClients:
                queryClients[pport] += 1
            else:
                queryClients[pport] = 1
    return queryClients

def ipCount(pkts, mode='d'):
    queryClients={}

    for pkt in pkts:
        if IP in pkt:
            p_ip = pkt[IP].dst if mode=='d' else pkt[IP].src
            if p_ip in queryClients:
                queryClients[p_ip] += 1
            else:
                queryClients[p_ip] = 1
    return queryClients

def toJSON(file_name="example.pcap", limit=100):
    try:
        packets = rdpcap(file_name, limit)
    except:
        return None
    return json.dumps({
        'dnsCount':dnsCount(packets),
        'timeSeries':timeSeries(packets),
        'portTraffd':portTraff(packets,'d'),
        'portTraffs':portTraff(packets, 's'),
        'ipCountd':ipCount(packets,'d'),
        'ipCounts': ipCount(packets, 's')
    })