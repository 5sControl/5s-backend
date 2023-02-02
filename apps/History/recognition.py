import face_recognition
from PIL import Image, ImageDraw


def face_rec(validated_data, person_name=False):
    face_img = face_recognition.load_image_file(validated_data['image'])
    gal_face_location = face_recognition.face_locations(face_img)

    pil_img = Image.fromarray(face_img)
    draw1 = ImageDraw.Draw(pil_img)

    for (top, right, bottom, left) in gal_face_location:
        draw1.rectangle(((left, top), (right, bottom)), outline=(255, 255, 0), width=4)
        if person_name:
            draw1.text((left, top - 10), person_name, align="left")

    del draw1
    pil_img.save(f"{validated_data['image']}")
    return validated_data['image']
