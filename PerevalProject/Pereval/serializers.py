from rest_framework import serializers
from .models import PerevalAdded, Coords, PerevalUser, PerevalImages


class UserSerializer(serializers.ModelSerializer):

    class Meta:
       model = PerevalUser
       fields = ['user', 'fam', 'name', 'otc', 'phone', 'email']


class CoordsSerializer(serializers.ModelSerializer):

    class Meta:
       model = Coords
       fields = ['latitude', 'longitude', 'height']


class PerevalSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=PerevalUser.objects.all())
    coords = serializers.PrimaryKeyRelatedField(queryset=Coords.objects.all())

    class Meta:
        model = PerevalAdded
        depth = 1
        fields = ['beautyTitle', 'title', 'other_titles', 'connect', 'add_time', 'user', 'coords',
                  'level_winter', 'level_summer', 'level_autumn', 'level_spring']


class PerevalDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = PerevalAdded
        depth = 1
        fields = '__all__'


class ImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = PerevalImages
        fields = ['id', 'date_added', 'title', 'img']

    def create(self, validated_data):
        pereval = PerevalAdded.objects.create(**validated_data)
        coords_data = validated_data.pop('coords')
        images_data = validated_data.pop('img')
        Coords.objects.create(pereval=pereval, **coords_data)
        for image_data in images_data:
            image = PerevalImages.objects.create(**image_data)
            PerevalImages.objects.create(foto=image, pereval=pereval)
        return pereval