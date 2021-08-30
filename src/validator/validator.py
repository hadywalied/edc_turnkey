import re
import sys


class Monitoring:
    def __init__(self, module):
        self.state = ""
        self.examples = {}
        self.module = module

    def sendState(self, state):
        self.state = state
        self.validate()

    def validate(self):
        ex = self.state.split(" ")
        if ex[0] == "<<" and ex[-1] == "Successful":
            self.examples[ex[1]] = ex[-3]

        if ex[1] == "Failed":
            print("edc finished")
            self.module.examples_dict = self.examples
            # TODO: send the examples to the main module
