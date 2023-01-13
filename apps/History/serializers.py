from .models import History

from rest_framework import serializers

from ..Locations.models import Location
from ..Employees.models import CustomUser

class HistorySerializer(serializers.ModelSerializer):
    """
    Create a History record if employee is authenticated, else
    write record with this unknown user and make history record
    """

    def create(self, validated_data):
        if validated_data['action'] == 'entrance':
            image = validated_data['image']
            camera = validated_data['camera']
            action = validated_data['action']
            name_file = validated_data['name_file']
            id_people = int(((f"[{validated_data['name_file']}").split('_')[-1]).split('.')[0])
            location = Location.objects.filter(gate_id__camera_input__id=validated_data['camera'])[0]
            history_data = History(
                camera=camera,
                action=action,
                name_file=name_file,
                location=location,
                people=CustomUser.objects.get(id=id_people),
                image=image
            )
            history_data.save()

            user = CustomUser.objects.filter(id=id_people)
            user.update(status=True, location=location)
            return history_data
        else:
            if validated_data['action'] == 'exit':
                image = validated_data['image']
                camera = validated_data['camera']
                action = validated_data['action']
                name_file = validated_data['name_file']
                id_people = int(((f"[{validated_data['name_file']}").split('_')[-1]).split('.')[0])
                location = Location.objects.filter(gate_id__camera_output__id=validated_data['camera'])[0]
                history_data = History(
                    camera=camera,
                    action=action,
                    name_file=name_file,
                    location=location,
                    people=CustomUser.objects.get(id=id_people),
                    image=image
                )
                history_data.save()

                user = CustomUser.objects.filter(id=id_people)
                user.update(status=False, location=None)
                return history_data
        return

    class Meta:
        model = History
        fields = ['id', 'people', 'location', 'image', 'entry_date', 'release_date', 'camera', 'name_file', 'action']
        read_only_fields = ['entry_date']
