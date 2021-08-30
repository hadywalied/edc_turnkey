import re
import sys


class Monitoring:
    def __init__(self, smoke_module):
        self.state = ""
        self.examples = {"test":"created"}
        self.smoke = smoke_module

    def sendState(self, state):
        self.state = state
        self.validate()

    def validate(self):
        ex = self.state.split(" ")
        if len(ex) > 3:
            if ex[0] == "<<" and ex[-1] == "Successful":
                self.examples[ex[1]] = ex[-3]
                self.examples["test"] = "successful"

            if ex[1] == "Failed": # Failed : 0
                print("edc finished")
                if self.examples["test"] == "created":
                    self.examples["test"] = "failed"
                self.smoke.examples_dict = self.examples
                # TODO: send the examples to the main module
