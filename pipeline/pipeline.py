
class Pipeline:
    def __init__(self, pipeline):
        self.pipeline = pipeline

    def run(self, input_image, output_image):
        for executor in self.pipeline:
            executor.run(input_image, output_image)
