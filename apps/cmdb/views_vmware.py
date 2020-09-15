from django.views.generic import TemplateView
from system.mixin import LoginRequiredMixin
from custom import BreadcrumbMixin, SandboxListView, SandboxUpdateView, SandboxDeleteView
from cmdb.models import VMConnectionInfo

class VmwareConnectionInfoView(LoginRequiredMixin, BreadcrumbMixin, TemplateView):
    template_name = 'cmdb/vm_config_manage.html'

class VmwareConnectionInfoListView(SandboxListView):
    model = VMConnectionInfo
    fields = ['id', 'hostname', 'username', 'port']

class VmwareConnectionInfoUpdateView(SandboxUpdateView):
    model = VMConnectionInfo
    fields = '__all__'
    template_name = 'cmdb/vm_config_manage_update.html'
    context_object_name = "VMConnectionInfo"

    def get_context_data(self, **kwargs):
        kwargs['VMConnectionInfo_all'] = VMConnectionInfo.objects.all()
        return super().get_context_data(**kwargs)

class VmwareConnectionInfoDeleteView(SandboxDeleteView):
    model = VMConnectionInfo















