# Uncomment the following imports before adding the Model code

from django.db import models
from django.utils.timezone import now
from django.core.validators import MaxValueValidator, MinValueValidator


# Create your models here.

# <HINT> Create a Car Make model `class CarMake(models.Model)`:
# - Name
# - Description
# - Any other fields you would like to include in car make model
# - __str__ method to print a car make object
class CarMake(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name

# <HINT> Create a Car Model model `class CarModel(models.Model):`:
# - Many-To-One relationship to Car Make model (One Car Make has many
# Car Models, using ForeignKey field)
# - Name
# - Type (CharField with a choices argument to provide limited choices
# such as Sedan, SUV, WAGON, etc.)
# - Year (IntegerField) with min value 2015 and max value 2023
# - Any other fields you would like to include in car model
# - __str__ method to print a car make object
class CarModel(models.Model):
    # Relación con CarMake
    make = models.ForeignKey(CarMake, on_delete=models.CASCADE, related_name='car_models')

    # Dealer ID del concesionario (relacionado a Cloudant)
    dealer_id = models.IntegerField()

    # Nombre del modelo del auto
    name = models.CharField(max_length=100)

    # Tipos de autos válidos
    CAR_TYPES = [
        ('SEDAN', 'Sedan'),
        ('SUV', 'SUV'),
        ('WAGON', 'Wagon'),
        ('HATCHBACK', 'Hatchback'),
        ('COUPE', 'Coupe'),
        ('MINIVAN', 'Minivan'),
        ('PICKUP', 'Pickup'),
        ('CONVERTIBLE', 'Convertible')
    ]
    car_type = models.CharField(max_length=11, choices=CAR_TYPES, default='SEDAN')

    # Año como fecha completa
    year = models.DateField()

    # Cualquier otro campo opcional, por ejemplo: color
    color = models.CharField(max_length=30, blank=True, null=True)

    def __str__(self):
        return f"{self.make.name} {self.name} ({self.car_type})"