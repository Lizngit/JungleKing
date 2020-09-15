import atexit
import math

from pyVmomi import vim, vmodl
from pyVim.connect import SmartConnectNoSSL, Disconnect





class VmManageUtil():

    def sandboxvmutil(self, host, user, password, port):
        esxi_host = {}
        # connect this thing
        si = SmartConnectNoSSL(
            host=host,
            user=user,
            pwd=password,
            port=port)

        atexit.register(Disconnect, si)
        content = si.RetrieveContent()

        container = content.viewManager.CreateContainerView(content.rootFolder, [vim.HostSystem], True)
        esxi_obj = [view for view in container.view]
        for esxi in esxi_obj:
            nic = esxi.config.network.vnic[0].spec
            esxi_config = esxi.summary.config

            result = {}
            result["sys_hostname"] = esxi_config.name
            result["hostname"] = nic.ip.ipAddress
            result["mac_address"] = nic.mac
            result["os_type"] = esxi_config.product.fullName
            result["status"] = esxi.summary.runtime.connectionState
            result["device_type"] = esxi.summary.hardware.vendor + " " + esxi.summary.hardware.model

            for i in esxi.summary.hardware.otherIdentifyingInfo:
                if isinstance(i, vim.host.SystemIdentificationInfo):
                    result["sn_number"] = i.identifierValue
            result["cpu_type"] = '%s Cores@%s Num@%s' % (esxi.summary.hardware.cpuModel,
                                                            esxi.summary.hardware.numCpuCores,
                                                            esxi.summary.hardware.numCpuPkgs)
            result["mem_total"] = math.ceil(esxi.summary.hardware.memorySize / 1024 / 1024 /1024)
        return result