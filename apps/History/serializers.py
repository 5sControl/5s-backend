import datetime

from .models import History

from rest_framework import serializers

from ..Locations.models import Location
from ..Employees.models import CustomUser

from .recognition import face_rec


class HistorySerializer(serializers.ModelSerializer):
    """
    Create a History record if employee is authenticated, else
    write record with this unknown user and make history record
    """

    def create(self, validated_data):
        if validated_data['name_file'] != 'unknown':

            image = face_rec(validated_data=validated_data)
            action = validated_data['action']
            name_file = validated_data['name_file']
            camera = validated_data['camera']
            id_people = int(((f"{validated_data['name_file']}").split('_')[-1]).split('.')[0])
            location = []
            release_date = []

            if validated_data['action'] == 'entrance':
                release_date.append(None)
                location.append(Location.objects.get(gate_id__camera_input__id=validated_data['camera']))
            else:
                if validated_data['action'] == 'exit':
                    release_date.append(f"{datetime.datetime.now()}")
                    location.append(Location.objects.get(gate_id__camera_output__id=validated_data['camera']))

            history_data = History(
                camera=camera,
                action=action,
                name_file=name_file,
                release_date=release_date[0],
                location=location[0],
                people=CustomUser.objects.get(id=id_people),
                image=image
            )
            history_data.save()

            user = CustomUser.objects.filter(id=id_people)
            if validated_data['action'] == 'entrance':
                user.update(status=True, location=location[0])
            else:
                user.update(status=False, location=None)

            return history_data

        elif validated_data['name_file'] == 'unknown':
            image = face_rec(validated_data=validated_data)
            camera = validated_data['camera']
            action = validated_data['action']

            release_date = []
            location = []
            if validated_data['action'] == 'entrance':
                release_date.append(None)
                location.append(Location.objects.get(gate_id__camera_input__id=validated_data['camera']))
            else:
                if validated_data['action'] == 'exit':
                    release_date.append(f"{datetime.datetime.now()}")
                    location.append(Location.objects.get(gate_id__camera_output__id=validated_data['camera']))
            history_data = History(
                camera=camera,
                action=action,
                release_date=release_date[0],
                name_file=None,
                location=location[0],
                people=None,
                image=image
            )
            history_data.save()
            return history_data

        return

    class Meta:
        model = History
        fields = ['id', 'people', 'location', 'image', 'entry_date', 'release_date', 'camera', 'name_file', 'action']
        read_only_fields = ['entry_date']
