# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Congressman(models.Model):
    con_id = models.IntegerField(blank=True, null=True)
    dept_cd = models.IntegerField(primary_key=True)
    con_name_kr = models.TextField(blank=True, null=True)
    con_name_en = models.TextField(blank=True, null=True)
    con_name_cn = models.TextField(blank=True, null=True)
    photo_link = models.TextField(blank=True, null=True)
    district = models.TextField(blank=True, null=True)
    email = models.TextField(blank=True, null=True)
    hp = models.TextField(blank=True, null=True)
    tel_number = models.TextField(blank=True, null=True)
    birth = models.TextField(blank=True, null=True)
    election_record = models.TextField(blank=True, null=True)
    profile = models.TextField(blank=True, null=True)
    party = models.TextField(blank=True, null=True)
    election_detail = models.TextField(blank=True, null=True)
    secretary = models.TextField(blank=True, null=True)
    committee = models.TextField(blank=True, null=True)
    aide = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'congressman'


class Plenary(models.Model):
    speak_id = models.IntegerField(primary_key=True)
    date = models.TextField(blank=True, null=True)
    confer_num = models.IntegerField(blank=True, null=True)
    confer_name = models.TextField(blank=True, null=True)
    dept_cd = models.IntegerField(blank=True, null=True)
    con_name_kr = models.TextField(blank=True, null=True)
    speaking = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'plenary'
