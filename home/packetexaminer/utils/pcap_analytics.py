from scapy.all import *
import json

def dnsCount(pkts):
    queryClients = {}
    for pkt in pkts:
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
    return json.dumps(queryClients)

def timeSeries(pkts):
    pktBytes=[]
    pktTimes=[]

    #Read each packet and append to the lists.
    for pkt in pkts:
        if IP in pkt:
            try:
                pktBytes.append(pkt[IP].len)
                pktTime=datetime.fromtimestamp(pkt.time)
                pktTimes.append(int(pktTime.timestamp()))
            except:
                pass
    data = {'pktBytes':pktBytes,'pktTimes':pktTimes}
    print(json.dumps(data))
    return json.dumps(data)

def portTraff(pkts, mode='d'):
    queryClients={}

    for pkt in pkts:
        if TCP in pkt:
            pport = pkt[TCP].dport if mode=='d' else pkt[TCP].sport
            if pport in queryClients:
                queryClients[pport] += 1
            else:
                queryClients[pport] = 1
    print(json.dumps(queryClients))
    return json.dumps(queryClients)

def ipCount(pkts, mode='d'):
    queryClients={}

    for pkt in pkts:
        if IP in pkt:
            p_ip = pkt[IP].dst if mode=='d' else pkt[IP].src
            if p_ip in queryClients:
                queryClients[p_ip] += 1
            else:
                queryClients[p_ip] = 1
    print(json.dumps(queryClients))
    return json.dumps(queryClients)

def toJSON(file_name="example.pcap", limit=100):
    packets = rdpcap(file_name, limit)
    return {
        'dnsCount':dnsCount(packets),
        'timeSeries':timeSeries(packets),
        'portTraffd':portTraff(packets,'d'),
        'portTraffs':portTraff(packets, 's'),
        'ipCountd':ipCount(packets,'d'),
        'ipCounts': ipCount(packets, 's')
    }