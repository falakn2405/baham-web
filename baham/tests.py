# Create your tests here.
import base64
from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from baham import views
from baham.enum_types import VehicleStatus, VehicleType

from baham.models import Vehicle, VehicleModel


USERNAME = 'testuser'
PASSWORD = 'WeakestPass'

class VehicleModelTest(TestCase):
    
    def setUp(self):
        '''
        Provide all pre-requisites userd in the tests
        '''
        self.superuser = User.objects.create_superuser(username=USERNAME, email='admin@dareecha.com', password=PASSWORD)
        return super().setUp()
    
    def test_auto_date_created_on_save(self):
        obj = VehicleModel.objects.create(vendor='Kia', model='Sportage', type=VehicleType.SUV, capacity=7)
        # See if the date_created is automatically set
        # Pass this test if obj.date_created is not None
        self.assertIsNotNone(obj.created_by)
        self.assertIsNotNone(obj.date_created)
    
    def test_create_with_same_vendor_and_model(self):
        # Create a new object
        kia = VehicleModel.objects.create(vendor='Kia', model='Sportage', type=VehicleType.SUV, capacity=7)
        # An error must be thrown
        with self.assertRaises(Exception):
            # Create a new object with same vendor and model
            VehicleModel.objects.create(vendor='Kia', model='Sportage', type=VehicleType.SEDAN, capacity=5)

    def test_update_with_same_vendor_and_model(self):
        VehicleModel.objects.create(vendor='Honda', model='CD125', type=VehicleType.MOTORCYCLE, capacity=2)
        cd70 = VehicleModel.objects.create(vendor='Honda', model='CD70', type=VehicleType.MOTORCYCLE, capacity=2)
        cd70.model = 'CD125'
        # An error must be thrown
        with self.assertRaises(Exception):
            # Create a new object with same vendor and model
            cd70.update()

    def test_one_vehicle_per_owner(self):
        owais = User.objects.create(username='owais', email='owais@dareecha.com', password='WeakestPass')
        cd70 = VehicleModel.objects.create(vendor='Honda', model='CD70', type=VehicleType.MOTORCYCLE, capacity=2)
        cd125 = VehicleModel.objects.create(vendor='Honda', model='CD125', type=VehicleType.MOTORCYCLE, capacity=2)
        Vehicle.objects.create(registration_number='KHI-885', colour='#ff00ff', model=cd70, owner=owais, status=VehicleStatus.FULL)
        # An error must be thrown
        with self.assertRaises(Exception):
            # Create a new object with same vendor and model
            Vehicle.objects.create(registration_number='KHI-996', colour='#ffff00', model=cd125, owner=owais, status=VehicleStatus.AVAILABLE)


class RESTAPITest(TestCase):
    
    def setUp(self):
        self.superuser = User.objects.create_superuser(username=USERNAME, email='admin@dareecha.com', password=PASSWORD)
        return super().setUp()
    
    def test_get_csrf_token(self):
        credentials = f"{USERNAME}:{PASSWORD}"
        encoded_credentials = base64.b64encode(credentials.encode('utf-8')).decode('utf-8')
        response = self.client.get(reverse('get_csrf_token'), HTTP_AUTHORIZATION='Basic ' + encoded_credentials)
        self.assertEquals(response.status_code, 200)
        self.assertTrue(response.json())
        self.assertIsNotNone(response.json()['csrf_token'])
    
    def test_get_vehicle_model_by_uuid(self):
        model = VehicleModel.objects.create(vendor='Honda', model='CD125', type=VehicleType.MOTORCYCLE, capacity=2)
        credentials = f"{USERNAME}:{PASSWORD}"
        encoded_credentials = base64.b64encode(credentials.encode('utf-8')).decode('utf-8')
        response = self.client.get(reverse('get_vehicle_model', args=[model.uuid,]), HTTP_AUTHORIZATION='Basic ' + encoded_credentials)
        vehicle_obj = response.json()['results']
        self.assertEquals(str(model.uuid), vehicle_obj['uuid'])
    