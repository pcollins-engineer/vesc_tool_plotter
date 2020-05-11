from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Foil(models.Model):
    title = models.CharField('foil title', max_length=50)
    description = models.CharField('foil description', max_length=200)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'foils'

class Board(models.Model):
    title = models.CharField('board title', max_length=50)
    description = models.CharField('board description', max_length=200)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'boards'

class Motor(models.Model):
    title = models.CharField('motor title', max_length=50)
    description = models.CharField('motor description', max_length=200)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'motors'

class Propellor(models.Model):
    title = models.CharField('propellor title', max_length=50)
    description = models.CharField('propellor description', max_length=200)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'propellors'

class Controller(models.Model):
    title = models.CharField('controller title', max_length=50)
    description = models.CharField('controller description', max_length=200)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'controllers'

class Build(models.Model):
    title = models.CharField('foil title', max_length=50)
    description = models.CharField('foil description', max_length=200)
    author_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='build')
    foil_id = models.ForeignKey(Foil, on_delete=models.CASCADE, related_name='build')
    board_id = models.ForeignKey(Board, on_delete=models.CASCADE, related_name='build')
    motor_id = models.ForeignKey(Motor, on_delete=models.CASCADE, related_name='build')
    propellor_id = models.ForeignKey(Propellor, on_delete=models.CASCADE, related_name='build')
    controller_id = models.ForeignKey(Controller, on_delete=models.CASCADE, related_name='build')

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'builds'

# Ride data for V 0.1
class Ride(models.Model):
    rider_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ride')
    title = models.CharField('ride title', max_length=50)
    description = models.CharField('ride description', max_length=200)
    ride_date = models.DateField('date of ride')
    build = models.ForeignKey(Build, models.SET_NULL, null=True, related_name='ride')
    pub_date = models.DateField('date uploaded', False, True) # Automatically sets

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'rides'
