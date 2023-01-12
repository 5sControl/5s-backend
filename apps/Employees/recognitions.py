import face_recognition


class Recognition:

    def dataset_maker(self, validated_data):
        """
        This function takes an image and returns a list of face datasets in the image.
        """

        face_img = face_recognition.load_image_file(f"images/{validated_data['image']}")
        dataset = face_recognition.face_encodings(face_img)[0]
        print('[INFO] Dataset assembled successfully')

        return dataset

    def test_dataset_maker(self, image):
        """
        This function takes a saved test image and returns a list of face datasets in the image.
        """
        face_img = face_recognition.load_image_file(f"media/tests/{image}")
        dataset = face_recognition.face_encodings(face_img)[0]

        print('[INFO] Dataset assembled successfully')

        return dataset

