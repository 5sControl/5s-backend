import os
import pickle
import sys
import face_recognition


def train_model_by_img(name):

    face_img = face_recognition.load_image_file(f"/{image}")
    face_enc = face_recognition.face_encodings(face_img)[0]

    # print(face_enc)

    if len(known_encodings) == 0:
        known_encodings.append(face_enc)
    else:
        for item in range(0, len(known_encodings)):
            result = face_recognition.compare_faces([face_enc], known_encodings[item])
            # print(result)

            if result[0]:
                known_encodings.append(face_enc)
                # print("Same person!")
                break
            else:
                # print("Another person!")
                break

    data = {
        "name": name,
        "encodings": known_encodings
    }

    with open(f"{name}_encodings.pickle", "wb") as file:
        file.write(pickle.dumps(data))

    return f"[INFO] File {name}_encodings.pickle successfully created"