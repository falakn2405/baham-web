# Create your tests here.
from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import date
from baham.constants import TOWNS
from baham.enum_types import UserType, VehicleStatus, VehicleType
from baham.models import Contract, Vehicle, VehicleModel, UserProfile

class VehicleTest(TestCase):

    def setUp(self):
        self.superuser = User.objects.create(username='admin', email='admin@gmail.com', password='abc123@@')
        return super().setUp()


    def test_one_vehicle_per_owner(self):
        falak = User.objects.create(username='falak', email='falak@gmail.com', password='752411')
        toyotacorolla = VehicleModel.objects.create(vendor='Toyota', model='Corolla', type=VehicleType.SEDAN, capacity=4)
        toyotasedan = VehicleModel.objects.create(vendor='Toyota', model='Sedan', type=VehicleType.SEDAN, capacity=4)
        altis18 = Vehicle.objects.create(registration_number='Altis-1.8', colour='#ff00ff', model=toyotacorolla, 
                                        owner=falak, status=VehicleStatus.FULL)        
        with self.assertRaises(Exception):
            altis16 = Vehicle.objects.create(registration_number='Altis-1.6', colour='#ff00ff', model=toyotasedan, 
                                        owner=falak, status=VehicleStatus.AVAILABLE)


class ContractTest(TestCase):

    def setUp(self):
        self.superuser = User.objects.create(username='admin', email='admin@gmail.com', password='abc123@@')
        return super().setUp()

    def test_no_more_passengers_than_vehicle_sitting_capacity(self):
        falak = User.objects.create(username='falak', email='falak@gmail.com', password='752411')
        toyotacorola = VehicleModel.objects.create(vendor='Toyota', model='Corola', type=VehicleType.SEDAN, capacity=4)
        altis18 = Vehicle.objects.create(registration_number='Altis-1.8', colour='#ff00ff', model=toyotacorola, 
                                        owner=falak, status=VehicleStatus.AVAILABLE)
        qunooj = User.objects.create(username='Qunooj', email='qunooj@gmail.com', password='752411')
        zain = User.objects.create(username='Zain', email='zain@gmail.com', password='752411')
        meesum = User.objects.create(username='Meesum', email='meesum@gmail.com', password='752411')
        daniyal = User.objects.create(username='Daniyal', email='daniyal@gmail.com', password='752411')
        asad = User.objects.create(username='Asad', email='asad@gmail.com', password='752411')
        test_date = date(2023, 5, 31)
        test_date_str = test_date.isoformat()
        user1 = UserProfile.objects.create(user=qunooj, birthdate=test_date_str, gender='M', type=UserType.COMPANION, primary_contact="03479319624",
                                           address="Defence", landmark="Islamabad", town='Kot Hathial')
        user2 = UserProfile.objects.create(user=zain, birthdate=test_date_str, gender='M', type=UserType.COMPANION, primary_contact="03479319624",
                                           address="Defence", landmark="Islamabad", town='Kot Hathial')
        user3 = UserProfile.objects.create(user=meesum, birthdate=test_date_str, gender='M', type=UserType.COMPANION, primary_contact="03479319624",
                                           address="Defence", landmark="Islamabad", town='Kot Hathial')
        user4 = UserProfile.objects.create(user=daniyal, birthdate=test_date_str, gender='M', type=UserType.COMPANION, primary_contact="03479319624",
                                           address="Defence", landmark="Islamabad", town='Kot Hathial')
        user5 = UserProfile.objects.create(user=asad, birthdate=test_date_str, gender='M', type=UserType.COMPANION, primary_contact="03479319624",
                                           address="Defence", landmark="Islamabad", town='Kot Hathial')
        contract1 = Contract.objects.create(vehicle=altis18, companion=user1, effective_start_date=test_date_str, expiry_date=test_date_str, fuel_share=50, 
                                            maintenance_share=40, schedule='Tuesday Evening')
        contract2 = Contract.objects.create(vehicle=altis18, companion=user2, effective_start_date=test_date_str, expiry_date=test_date_str, fuel_share=50, 
                                            maintenance_share=40, schedule='Tuesday Evening')
        contract3 = Contract.objects.create(vehicle=altis18, companion=user3, effective_start_date=test_date_str, expiry_date=test_date_str, fuel_share=50, 
                                            maintenance_share=40, schedule='Tuesday Evening')
        contract4 = Contract.objects.create(vehicle=altis18, companion=user4, effective_start_date=test_date_str, expiry_date=test_date_str, fuel_share=50, 
                                            maintenance_share=40, schedule='Tuesday Evening')
        with self.assertRaises(Exception):
            contract5 = Contract.objects.create(vehicle=altis18, companion=user5, effective_start_date=test_date_str, expiry_date=test_date_str, fuel_share=50, 
                                            maintenance_share=40, schedule='Tuesday Evening')



    def test_total_share_cannot_exceed_hundred_on_record_creation(self):
        falak = User.objects.create(username='falak', email='falak@gmail.com', password='752411')
        toyotacorola = VehicleModel.objects.create(vendor='Toyota', model='Corola', type=VehicleType.SEDAN, capacity=4)
        altis18 = Vehicle.objects.create(registration_number='Altis-1.8', colour='#ff00ff', model=toyotacorola, 
                                        owner=falak, status=VehicleStatus.AVAILABLE)
        test_date = date(2023, 5, 31)
        test_date_str = test_date.isoformat()
        qunooj = User.objects.create(username='Qunooj', email='qunooj@gmail.com', password='752411')
        user1 = UserProfile.objects.create(user=qunooj, birthdate=test_date_str, gender='M', type=UserType.COMPANION, primary_contact="03479319624",
                                           address="Defence", landmark="Islamabad", town='Kot Hathial')
        with self.assertRaises(Exception):
            contract1 = Contract.objects.create(vehicle=altis18, companion=user1, effective_start_date=test_date_str, expiry_date=test_date_str, fuel_share=110, 
                                            maintenance_share=90, schedule='Tuesday Evening')


    def test_total_share_cannot_exceed_hundred_on_record_updation(self):
        falak = User.objects.create(username='falak', email='falak@gmail.com', password='752411')
        toyotacorolla = VehicleModel.objects.create(vendor='Toyota', model='Corolla', type=VehicleType.SEDAN, capacity=4)
        altis18 = Vehicle.objects.create(registration_number='Altis-1.8', colour='#ff00ff', model=toyotacorolla, 
                                        owner=falak, status=VehicleStatus.AVAILABLE)
        test_date = date(2023, 5, 31)
        test_date_str = test_date.isoformat()
        qunooj = User.objects.create(username='Qunooj', email='qunooj@gmail.com', password='752411')
        user1 = UserProfile.objects.create(user=qunooj, birthdate=test_date_str, gender='M', type=UserType.COMPANION, primary_contact="03479319624",
                                           address="Defence", landmark="Islamabad", town='Kot Hathial')
        contract1 = Contract.objects.create(vehicle=altis18, companion=user1, effective_start_date=test_date_str, expiry_date=test_date_str, fuel_share=50, 
                                            maintenance_share=20, schedule='Tuesday Evening')
        with self.assertRaises(Exception):
            contract1.fuel_share=100
            contract1.maintenance_share = 50
            contract1.update()

    def test_companions_cannot_have_multiple_active_contracts_simultaneously(self):
        falak = User.objects.create(username='falak', email='falak@gmail.com', password='752411')
        toyotacorolla = VehicleModel.objects.create(vendor='Toyota', model='Corolla', type=VehicleType.SEDAN, capacity=4)
        altis18 = Vehicle.objects.create(registration_number='Altis-1.8', colour='#ff00ff', model=toyotacorolla, 
                                        owner=falak, status=VehicleStatus.AVAILABLE)
        qunooj = User.objects.create(username='Qunooj', email='qunooj@gmail.com', password='752411')
        toyotasedan = VehicleModel.objects.create(vendor='Toyota', model='Sedan', type=VehicleType.SEDAN, capacity=4)
        kuy875 = Vehicle.objects.create(registration_number='KUY-875', colour='#ff00ff', model=toyotasedan, 
                                        owner=qunooj, status=VehicleStatus.AVAILABLE)
        test_date = date(2023, 5, 31)
        test_date_str = test_date.isoformat()
        asad = User.objects.create(username='Asad', email='asad@gmail.com', password='752411')
        user1 = UserProfile.objects.create(user=asad, birthdate=test_date_str, gender='M', type=UserType.COMPANION, primary_contact="03479319624",
                                           address="Defence", landmark="Islamabad", town='Kot Hathial')
        contract1 = Contract.objects.create(vehicle=altis18, companion=user1, effective_start_date=test_date_str, expiry_date=test_date_str, fuel_share=50, 
                                            maintenance_share=40, schedule='Tuesday Evening')
        with self.assertRaises(Exception):
            contract2 = Contract.objects.create(vehicle=kuy875, companion=user1, effective_start_date=test_date_str, expiry_date=test_date_str, fuel_share=50, 
                                            maintenance_share=40, schedule='Tuesday Evening')
