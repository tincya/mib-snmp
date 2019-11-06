from pysnmp.hlapi import *

router1 = {'host':'10.0.0.1', 'port':161}
router2 = {'host':'demo.snmplabs.com', 'port':161}
router = router1

# g = setCmd(
#     SnmpEngine(),
#     CommunityData('public', mpModel=0),
#     UdpTransportTarget((router1['host'], router1['port'])),
#     ContextData(),
#     ObjectType(ObjectIdentity('SNMPv2-MIB', 'sysDescr', 0), 'Linux i386')
#   )
# print(g)
# print('--------+----------')
# print(next(g))
# print('--------+----------')

"""
Retrieved Function: 
- Availability: hrDeviceStatus, localHwDeviceOper/AdminStatus 
- CPU info: cpmCPUTotal5sec/ busyPer
- Inteface Status : ifAdminStatus
- Interface Link Status: ifOperStatus
- Interface Bandwidth: ifInOctets, ifOutOctets, ifspeed, locIfIn/OutBitsSec
- IP accounting: cipMacTable, cipMacSwitchedPkts, cipMacSwitchedBytes, actCheckPoint 
- Topology ( optional)
"""
errorIndication, errorStatus, errorIndex, varBinds = next(
  getCmd(
    SnmpEngine(),
    CommunityData('public', mpModel=0),
    UdpTransportTarget((router['host'], router['port'])),
    ContextData(),
    # ObjectType(ObjectIdentity('SNMPv2-MIB', 'sysDescr', 0))
    ObjectType(ObjectIdentity('IF-MIB', 'ifNumber', 0)),
    # ObjectType(ObjectIdentity('IF-MIB', '1.3.6.1.2.1.2.1.0')),
    ObjectType(ObjectIdentity('1.3.6.1.2.1.1.1.0')),# sysDescr
    ObjectType(ObjectIdentity('1.3.6.1.2.1.1.5.0')),# sysName
    ObjectType(ObjectIdentity('1.3.6.1.2.1.2.1.0')),# mib-ifNumber
    ObjectType(ObjectIdentity('1.3.6.1.2.1.11.1.0')),
    # ObjectType(ObjectIdentity('1.3.6.1.2.1.2.2.1.7')),
    ObjectType(ObjectIdentity('1.3.6.1.4.1.9.9.109.1.1.1.1.3.1')),
    # ObjectType(ObjectIdentity('HOST-RESOURCES-MIB','hrDeviceStatus',1)),
    
    ObjectType(ObjectIdentity('IF-MIB','ifAdminStatus',1)),
    ObjectType(ObjectIdentity('IF-MIB','ifOperStatus',1)),
    ObjectType(ObjectIdentity('IF-MIB','ifInOctets',1)),
    ObjectType(ObjectIdentity('IF-MIB','ifOutOctets',1)),
    ObjectType(ObjectIdentity('IF-MIB','ifSpeed',1)),
    ObjectType(ObjectIdentity('1.3.6.1.4.1.9.2.2.1.1.6.1')),
    ObjectType(ObjectIdentity('1.3.6.1.4.1.9.2.2.1.1.8.1')),
    # ObjectType(ObjectIdentity('1.3.6.1.4.1.9.9.84.1.2.1.2')),

    # ObjectType(ObjectIdentity('IF-MIB','ifspeed',1)),

    ObjectType(ObjectIdentity('1.3.6.1.2.1.1.6.0'))
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

# ---

# errorIndication, errorStatus, errorIndex, varBinds = next(
#   sendNotification(
#     SnmpEngine(),
#     CommunityData('public', mpModel=0),
#     UdpTransportTarget(('demo.snmplabs.com', 162)),
#     ContextData(),
#     'trap',
#     NotificationType(
#       ObjectIdentity('1.3.6.1.6.3.1.1.5.2')
#     ).addVarBinds(
#       ('1.3.6.1.6.3.1.1.4.3.0', '1.3.6.1.4.1.20408.4.1.1.2'),
#       ('1.3.6.1.2.1.1.1.0', OctetString('my system'))
#     )
#   )
# )

# print(errorIndication, errorStatus, errorIndex, varBinds)

# if errorIndication:
#   print(errorIndication)
# else :
#   for varBind in varBinds:
#     print(varBind)
#     print('--------')

#   for (errorIndication, errorStatus, errorIndex, varBinds) in nextCmd(
# try:
#   for (errorIndication, errorStatus, errorIndex, varBinds) in bulkCmd(
#     SnmpEngine(),
#     UsmUserData('usr-md5-none', 'authkey1'),
#     UdpTransportTarget(('demo.snmplabs.com', 161)),
#     ContextData(),
#     ObjectType(ObjectIdentity('IF-MIB'))):

#     if errorIndication:
#       print(errorIndication)
#       break
#     elif errorStatus:
#       print('%s at %s' % (errorStatus.prettyPrint(), errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
#       break
#     else:
#       for varBind in varBinds:
#         print(' = '.join([x.prettyPrint() for x in varBind]))
# except KeyboardInterrupt:
#   print('done.')

