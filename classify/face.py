class FaceClassifier(object):

    def run(self, input_image, output_image, faces):
        return faces[0] if len(faces) > 0 else None
