
from rest_framework import serializers
from .models import *

class MyUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = myuser
        fields = ('id', 'email', 'first_name', 'last_name',)


class DeceasedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deceased
        fields = ['first_name', 'last_name', 'city', 'relationship_type', 'audience', 'date_of_birth', 'date_of_death', 'cover_photo']

    def create(self, validated_data):
        return Deceased.objects.create(**validated_data)


class MemorialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deceased
        fields = "__all__"
        #fields = ['id','first_name', 'last_name', 'cover_photo','date_of_birth','date_of_death']
    

class TributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tribute
        fields = ['text']

class TributeListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tribute
        fields = '__all__'