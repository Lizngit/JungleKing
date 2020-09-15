import time
import logging

from celery import shared_task
from celery_once import QueueOnce

from utils.sandbox_utils import SandboxScan, LoginExecution
from utils.vmware import VmManageUtil
from .models import DeviceScanInfo,VMConnectionInfo

info_logger = logging.getLogger('sandbox_info')

@shared_task(base=QueueOnce)
def vmscan_execution():
    print("开始扫描:")
    vmmanage=VmManageUtil()
    start_time = time.time()

    hosts = VMConnectionInfo.objects.all()
    print("正在扫描："+str(hosts))

    for host in hosts:
        print(host.hostname)
        print(host.username)
        print(host.password)
        print(host.port)
        defaults=vmmanage.sandboxvmutil(host.hostname,host.username,host.password,host.port)
        print(defaults)
        DeviceScanInfo.objects.update_or_create(
         defaults=defaults
        )
    end_time = time.time()
    msg = 'Scan task has been completed, execution time: %(time)s, %(num)s hosts are up.' % {
        'time': end_time - start_time,
        'num': len(hosts)
    }
    info_logger.info(msg)
    return msg


@shared_task(base=QueueOnce)
def scan_execution():
    scan = SandboxScan()
    execution = LoginExecution()
    scan_type = execution.get_scan_type()
    auth_type = execution.get_auth_type()
    start_time = time.time()
    if scan_type == 'basic_scan':
        hosts = scan.basic_scan()
        print("正在扫描："+str(hosts))
        for host in hosts:
            DeviceScanInfo.objects.update_or_create(
                hostname=host,
            )
    else:
        hosts = scan.os_scan()
        print("正在扫描："+str(hosts))
        login_hosts = [host for host in hosts if host['os'] in ['Linux', 'embedded']]
        nologin_hosts = [host for host in hosts if host not in login_hosts]
        for host in nologin_hosts:
            DeviceScanInfo.objects.update_or_create(
                hostname=host['host'],
                defaults={
                    'os_type': host['os']
                }
            )
        for host in login_hosts:
            kwargs = {
                'hostname': host['host'],
                'username': execution.get_ssh_username(),
                'port': execution.get_ssh_port(),
                'password': execution.get_ssh_password(),
                'private_key': execution.get_ssh_private_key()
            }
            defaults = execution.login_execution(auth_type=auth_type, **kwargs)
            print(defaults)
            DeviceScanInfo.objects.update_or_create(
                hostname=host['host'],
                defaults=defaults
            )
            #print(DeviceScanInfo.objects.values_list())
    end_time = time.time()
    msg = 'Scan task has been completed, execution time: %(time)s, %(num)s hosts are up.' % {
        'time': end_time - start_time,
        'num': len(hosts)
    }
    info_logger.info(msg)
    return msg