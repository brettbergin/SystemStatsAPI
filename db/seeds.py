#!/usr/bin/env python3

from api.extensions import db

from api.models.memory import Memory
from api.models.disk import Disk
from api.models.cpu import CPU
from api.models.network import NetworkInfo
from api.models.network import NetworkIp
from api.models.system import SystemUser
from api.models.system import SystemUptime
from api.models.system import SystemOper
from api.models.users import User


mock_memory = {
    "target": "mock-hostname.local",
    "report_id": "ad536b7e-ce43-4118-b017-aae62fb346da",
    "timestamp": '22-07-10 15:31:11',
    "active": "12.69 GB",
    "available": "16.41 GB",
    "free": "3.7 GB",
    "inactive": "11.89 GB",
    "percent": 52.3,
    "total": "34.36 GB",
    "used": "16.72 GB",
    "wired": "4.03 GB"
}
mock_disk = {
      "target": "mock-hostname.local",
      "report_id": "ad536b7e-ce43-4118-b017-aae62fb346da",
      "timestamp": '22-07-10 15:31:11',
      "free": "1.27 TB",
      "mount_point": "/",
      "percent": 36.3,
      "total": "2 TB",
      "used": "726.71 GB"
}
mock_cpu = {
  "target": "mock-hostname.local",
  "report_id": "ad536b7e-ce43-4118-b017-aae62fb346da",
  "timestamp": '22-07-10 15:31:11',
  "percents": "CPU_1:20.8, CPU_2:0.0, CPU_3:20.8, CPU_4:0.0"
}
mock_network_info = {
  "target": "mock-hostname.local",
  "report_id": "ad536b7e-ce43-4118-b017-aae62fb346da",
  "timestamp": '22-07-10 15:31:11',
  "bytes_recvd": "2.71 GB",
  "bytes_sent": "2.27 GB",
  "dropped_pkt_in": "1.74 PB",
  "dropped_pkt_out": "0 bytes",
  "err_pkt_in": "0 bytes",
  "err_pkt_out": "12.6 KB",
  "packets_recvd": "262.43 MB",
  "packets_sent": "40.51 MB"
}
mock_network_ips = {
  "target": "mock-hostname.local",
  "report_id": "ad536b7e-ce43-4118-b017-aae62fb346da",
  "timestamp": '22-07-10 15:31:11',
  "addresses": "l0:127.0.0.1, en0:192.168.1.100"
}
mock_system_users = {
  "target": "mock-hostname.local",
  "report_id": "ad536b7e-ce43-4118-b017-aae62fb346da",
  "timestamp": '22-07-10 15:31:11',
  "started": "2022-06-01 18:50:56",
  "terminal": "console",
  "username": "test_user"
}
mock_system_uptime = {
  "target": "mock-hostname.local",
  "report_id": "ad536b7e-ce43-4118-b017-aae62fb346da",
  "timestamp": '22-07-10 15:31:11',
  "uptime": "38 days, 22:13:38.350826"
}
mock_operating_system = {
  "target": "mock-hostname.local",
  "report_id": "ad536b7e-ce43-4118-b017-aae62fb346da",
  "timestamp": '22-07-10 15:31:11',
  "opersys": "macOS-12.3.1-x86_64-i386-64bit"
}
mock_user = {
  "username": "test_user",
  "password": "test_password",
  "email": "test_email@example.com",
  "email_verified": False,
  "jwt_issue_count": 0
}

mem_mock = Memory(**mock_memory)
disk_mock = Disk(**mock_disk)
cpu_mock = CPU(**mock_cpu)
network_info_mock = NetworkInfo(**mock_network_info)
network_ips_mock = NetworkIp(**mock_network_ips)
system_user_mock = SystemUser(**mock_system_users)
system_uptime_mock = SystemUptime(**mock_system_uptime)
system_oper_mock = SystemOper(**mock_operating_system)
users_mock = User(**mock_user)

db.session.add(mem_mock)
db.session.add(disk_mock)
db.session.add(cpu_mock)
db.session.add(network_info_mock)
db.session.add(network_ips_mock)
db.session.add(system_user_mock)
db.session.add(system_uptime_mock)
db.session.add(system_oper_mock)
db.session.add(users_mock)

db.session.commit()
