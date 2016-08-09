
class Pipeline:
    def __init__(self, pipeline):
        self.pipeline = pipeline

    def run(self, input):
        for executor in self.pipeline:
            executor.run(input)
