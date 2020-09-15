import os

from django.dispatch import receiver
from django.db.models.signals import post_delete, post_save

from .models import DeviceFile, DeviceInfo, ConnectionInfo


@receiver(post_delete, sender=DeviceFile)
def auto_delete_file(sender, instance, **kwargs):
    if instance.file_content:
        if os.path.isfile(instance.file_content.path):
            os.remove(instance.file_content.path)


@receiver(post_save, sender=DeviceInfo)
def auto_compare_diff(sender, instance, **kwargs):
    record = instance.history.latest()
    prev_record = record.prev_record
    ope_type = {'~': 'update', '+': 'create', '-': 'delete'}
    compare_result = {
        'id': record.id,
        'changed_by': record.changed_by.name,
        'history_type': ope_type[record.history_type],
        'history_date': record.history_date
    }
    changes = {}
    if prev_record is not None:
        delta = record.diff_against(prev_record)
        for change in delta.changes:
            changes[change.field] = [change.old, change.new]
    compare_result['changes'] = changes

@receiver(post_delete, sender=DeviceInfo)
def auto_delete_connection(sender, instance, **kwargs):
    dev_connection = getattr(instance, 'dev_connection')
    if dev_connection:
        ConnectionInfo.objects.filter(id=dev_connection).delete()