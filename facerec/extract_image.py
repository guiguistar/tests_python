import argparse
import face_recognition
import os
import pickle

def convert(dirname):
    list_photos = os.listdir(dirname)
    known_face_encodings = []
    known_face_names = []

    for file_name in list_photos:
        forename, *_ = file_name.split('_')

        path = os.path.join(dirname,file_name)
        
        image = face_recognition.load_image_file(path)

        face_encodings = face_recognition.face_encodings(image)

        if face_encodings:
            face_encoding = face_encodings[0]

            known_face_encodings.append(face_encoding)
            known_face_names.append(forename)    

        print(forename)

    return known_face_encodings, known_face_names

def save(filename, *objs):
    with open(filename, 'wb') as f:
        for obj in objs:
            pickle.dump(obj, f)

def load(filename):
    with open(filename, 'rb') as f:
        known_face_encodings = pickle.load(f)
        known_face_names = pickle.load(f)

    return known_face_encodings, known_face_names

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--dirname", type=str,
                        help="photos directory", default=".")
    parser.add_argument("-o", "--output", type=str,
                        help="the name of the ouput file")
    parser.add_argument("-i", "--input", type=str,
                        help="the name of the input file")
    args = parser.parse_args()    

    if args.output:
        know_face_encodings, known_face_names = convert(args.dirname)
        save(args.output, know_face_encodings, known_face_names)

        print(*known_face_names, sep='\n')

    if args.input:
        known_face_encodings, known_face_names = load(args.input)

        print(*known_face_names, sep='\n')
        
