from pysnmp.hlapi import *

router1 = {'host':'10.0.0.1', 'port':161}
router2 = {'host':'demo.snmplabs.com', 'port':161}
router = router2

errorIndication, errorStatus, errorIndex, varBinds = next(
  getCmd(
    SnmpEngine(),
    CommunityData('public', mpModel=0),
    UdpTransportTarget((router['host'], router['port'])),
    ContextData(),
    ObjectType(ObjectIdentity('1.3.6.1.2.1.1.1.0')),#desciption
    ObjectType(ObjectIdentity('1.3.6.1.2.1.1.3.0')),#Uptime
    ObjectType(ObjectIdentity('1.3.6.1.2.1.1.4.0')),#Contact
    ObjectType(ObjectIdentity('1.3.6.1.2.1.1.5.0')),#SysName
    ObjectType(ObjectIdentity('1.3.6.1.2.1.1.7.0')),#Service
  )
)

if errorIndication:
  print(errorIndication)
elif errorStatus:
  print('%s at %s' % (errorStatus.prettyPrint(),
    errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
else:
  print('All data:')
  for varBind in varBinds:
    # print(' = '.join([x.prettyPrint() for x in varBind]))
    print(varBind)
    print('--------')


errorIndication, errorStatus, errorIndex, varBinds = next(
  getCmd(
    SnmpEngine(),
    CommunityData('public', mpModel=0),
    UdpTransportTarget((router['host'], router['port'])),
    ContextData(),
    ObjectType(ObjectIdentity('1.3.6.1.2.1.2.1.0')),#IF Number
  )
)

if errorIndication:
  print(errorIndication)
elif errorStatus:
  print('%s at %s' % (errorStatus.prettyPrint(),
    errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
else:
  print('All data:')
  for varBind in varBinds:
    num = int(varBind.prettyPrint().split(' = ')[-1])
    for i in range(1,num+1):
        r_errorIndication, r_errorStatus, r_errorIndex, r_varBinds = next(
          getCmd(
            SnmpEngine(),
            CommunityData('public', mpModel=0),
            UdpTransportTarget((router['host'], router['port'])),
            ContextData(),
            ObjectType(ObjectIdentity('1.3.6.1.2.1.2.2.1.2.'+str(i))),#desciption
            ObjectType(ObjectIdentity('1.3.6.1.2.1.2.2.1.3.'+str(i))),#type
            ObjectType(ObjectIdentity('1.3.6.1.2.1.2.2.1.5.'+str(i))),#speed
            ObjectType(ObjectIdentity('1.3.6.1.2.1.2.2.1.6.'+str(i))),#MAC
            ObjectType(ObjectIdentity('1.3.6.1.2.1.2.2.1.8.'+str(i))),#status-up/down...
            ObjectType(ObjectIdentity('1.3.6.1.2.1.2.2.1.10.'+str(i))),#inoctets
            ObjectType(ObjectIdentity('1.3.6.1.2.1.2.2.1.3.'+str(i))),#outoctets ::  (outoctets1 - outoctets2)/(t1-t2)
          )
        )
        for varBind in r_varBinds:
            print(varBind.prettyPrint())
        print('--------??????')
    print('--------')
