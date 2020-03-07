from django.test import TestCase

from ..models.devices import Device, Blind, Bed
from ..models.managers import AbstractManager


class AbstractManagerTests(TestCase):
    def setUp(self):
        self.maxDiff = None
        self.objects = AbstractManager(Device)

        self.blind1 = Blind.objects.create(id='123', name='blind1')
        self.bed1 = Bed.objects.create(id='456', name='bed1')
        self.bed2 = Bed.objects.create(id='789', name='bed2')

    def test_all_base_member(self):
        names = {d.name for d in self.objects.all()}

        self.assertSetEqual({'blind1', 'bed1', 'bed2'}, names)

    def test_all_call_abstract_method(self):
        types = {d.get_type() for d in self.objects.all()}

        self.assertSetEqual({Device.Type.BLINDS, Device.Type.BED}, types)

    def test_filter_base_member(self):
        names = {d.name for d in self.objects.filter(id__in=[self.blind1.id, self.bed1.id])}

        self.assertSetEqual({'blind1', 'bed1'}, names)

    def test_filter_call_abstract_method(self):
        types = {d.get_type() for d in self.objects.filter(id__in=[self.blind1.id, self.bed1.id])}

        self.assertSetEqual({Device.Type.BLINDS, Device.Type.BED}, types)
