import face_recognition


class Recognition:

    def dataset_maker(self, validated_data):
        """
        This function takes an image and returns a list of face datasets in the image.
        """

        dataset = []
        for i in range(1, 6):
            face_img = face_recognition.load_image_file(f"images/{validated_data[f'image{i}']}")
            if i == 5:
                face_img1 = face_recognition.load_image_file(f"images/{validated_data[f'image1']}")
            else:
                face_img1 = face_recognition.load_image_file(f"images/{validated_data[f'image{i+1}']}")
            face_encoding = face_recognition.face_encodings(face_img)[0]
            face_encoding1 = face_recognition.face_encodings(face_img1)[0]
            rez = face_recognition.compare_faces([face_encoding1], face_encoding)
            if rez[0] == True:
                dataset.append(face_encoding)
        try:
            if len(dataset) != 0:
                print('[INFO] Dataset assembled successfully')
                return dataset
        except:
            print('[ERROR] No photos recognized')
            raise Exception


    def test_dataset_maker(self, image):
        """
        This function takes a saved test image and returns a list of face datasets in the image.
        """
        face_img = face_recognition.load_image_file(f"media/tests/{image}")
        dataset = face_recognition.face_encodings(face_img)[0]

        print('[INFO] Dataset assembled successfully')

        return dataset

