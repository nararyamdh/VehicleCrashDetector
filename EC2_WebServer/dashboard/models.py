from django.db import models

class Cameras(models.Model):
    id_x = models.AutoField(primary_key=True,unique=True)
    camera_name = models.CharField(max_length=255, default='Unnamed')
    kinesis_datastream_name = models.CharField(max_length=255)
    visited_counter = models.IntegerField(default=0)
    vehicle_counter = models.IntegerField(default=0)
    accidents_today_counter = models.IntegerField(default=0)
    accidents_total_counter = models.IntegerField(default=0)
    emergency_counter = models.IntegerField(default=0)
    sqs_name = models.CharField(max_length=255, default='Unnamed')

    exlamacion_alarm = models.IntegerField(default=0)
    info_alarm = models.IntegerField(default=0)
    danger_alarm = models.IntegerField(default=0)

    date_added = models.DateTimeField(auto_now_add=True)

class DataStream(models.Model):
    id_x = models.AutoField(primary_key=True,unique=True)
    camera_name = models.CharField(max_length=255, default='Unnamed')
    date_added = models.DateTimeField(auto_now_add=True)

class History(models.Model):
    id_x = models.AutoField(primary_key=True,unique=True)
    call_from = models.CharField(max_length=255, default='Unnamed')
    call_to = models.CharField(max_length=255, default='Unnamed')
    date_added = models.DateTimeField(auto_now_add=True)