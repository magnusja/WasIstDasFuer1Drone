
class Pipeline:
    def __init__(self, pipeline):
        self.pipeline = pipeline

    def run(self, input_image, output_image):
        exec_result = None
        for executor in self.pipeline:
            exec_result = executor.run(input_image, output_image, exec_result)
