from django.test import TestCase

from apps.Employees.models import CustomUser
from apps.Employees.recognitions import Recognition

import face_recognition


class CustomUserModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        CustomUser.objects.create(first_name='Test_First_Name', last_name='Test_Last_Name',
                                                                image='media/tests/test_image_customuser.jpg')

    def test_first_name_label(self):
        user = CustomUser.objects.get(id=1)
        field_label = user.first_name

        self.assertEquals(field_label,'Test_First_Name')

    def test_last_name_label(self):
        user = CustomUser.objects.get(id=1)
        field_label = user.last_name

        self.assertEquals(field_label,'Test_Last_Name')

    def test_image_label(self):
        user = CustomUser.objects.get(id=1)
        field_label = user.image

        self.assertEquals(field_label, 'media/tests/test_image_customuser.jpg')
    
    def test_face_finder(self):
        face_img = face_recognition.load_image_file(f"media/tests/test_image_customuser.jpg")
        user_dataset = face_recognition.face_encodings(face_img)

        self.assertEquals(len(user_dataset), 1)
    
    # TODO: test_dataset_label -> overload create method to create dataset

    def test_dataset_label(self):
        user = CustomUser.objects.get(id=1)
        field_label = user.dataset
        user_dataset = Recognition().test_dataset_maker('test_image_customuser.jpg')

        self.assertEquals(user_dataset)




    