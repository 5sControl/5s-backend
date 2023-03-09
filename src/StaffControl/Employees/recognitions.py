# import face_recognition
# from PIL import Image, ImageDraw


# class Recognition:
#     def dataset_maker(self, validated_data):
#         """
#         This function takes an image and returns a list of face datasets in the image.
#         """
#         list_images = [
#             "",
#             "image_below",
#             "image_above",
#             "image_center",
#             "image_left",
#             "image_right",
#         ]
#         dataset = []
#         for i in range(1, 6):
#             face_img = face_recognition.load_image_file(
#                 f"images/{validated_data[f'{list_images[i]}']}"
#             )
#             if i == 5:
#                 face_img1 = face_recognition.load_image_file(
#                     f"images/{validated_data[f'{list_images[1]}']}"
#                 )
#             else:
#                 face_img1 = face_recognition.load_image_file(
#                     f"images/{validated_data[f'{list_images[i + 1]}']}"
#                 )

#             face_encoding = face_recognition.face_encodings(face_img)[0]
#             face_encoding1 = face_recognition.face_encodings(face_img1)[0]
#             rez = face_recognition.compare_faces([face_encoding1], face_encoding)
#             if rez[0] == True:
#                 dataset.append(face_encoding)
#         try:
#             if len(dataset) != 0:
#                 print("[INFO] Dataset assembled successfully")
#                 return dataset
#         except:
#             print("[ERROR] No photos recognized")
#             raise Exception

#     def test_dataset_maker(self, image):
#         """
#         This function takes a saved test image and returns a list of face datasets in the image.
#         """
#         face_img = face_recognition.load_image_file(f"media/tests/{image}")
#         dataset = face_recognition.face_encodings(face_img)[0]

#         print("[INFO] Dataset assembled successfully")

#         return dataset


# def face_rec(validated_data):
#     """The function draws a frame around the face"""
#     list_images = [
#         "",
#         "image_below",
#         "image_above",
#         "image_center",
#         "image_left",
#         "image_right",
#     ]
#     for i in range(1, 6):
#         face_img = face_recognition.load_image_file(
#             f"images/{validated_data[f'{list_images[i]}']}"
#         )
#         face_location = face_recognition.face_locations(face_img)

#         pil_img = Image.fromarray(face_img)
#         draw1 = ImageDraw.Draw(pil_img)

#         for top, right, bottom, left in face_location:
#             draw1.rectangle(
#                 ((left, top), (right, bottom)), outline=(255, 255, 0), width=4
#             )

#         del draw1
#         pil_img.save(f"images/{validated_data[f'{list_images[i]}']}")
#         # return name_image
