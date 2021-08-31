import pdb
import sys

from src.logging import Loggers
from src.observers.observers import ConcreteObserver
from src.observers.subjects import ConcreteSubject
from src.app_resources import *
import os
from os import path

from src.validator.validator import Monitoring


class SmokeTestAnalyzer:
    """
    edc to turnkey controller module
        - input:
                - solution	(5g or ethernet)
                - env_file  < taking all the examples from it >
                - examples_list: if empty take all examples
                - examples_file : a csv file to pass examples with it's hosts
                - compilation type (Simulation, Emulation, Emu_Velcklgen, etc...)
                - logging dir (export for edc)
                - output dir  (path to compiled designs)
                - hosts file (for edc)
                - distibute  (for edc)
                - avb_list
                - mode_of_operation
                - compiled_ path : compiled design path

        - output:
                -- edc_output:
                                - compiled solution in output_dir ...
                -- turnkey output:

    """

    def __init__(self, solution=SUPPORTED_SOLUTIONS.vved.value,
                 env_file="",
                 examples_list=None,
                 examples_file="",
                 compilation_type=COMPILATION_TYPES.Simulation.value,
                 logging_dir="",
                 output_dir="",
                 hosts_file="",
                 distribute=False,
                 avb_list=None,
                 mode_of_operation=MODES_OF_OPERATION.all.value,
                 compiled_path="",
                 check_method_name=""):
        if avb_list is None:
            avb_list = []
        if examples_list is None:
            examples_list = []
        self.solution = solution
        self.env_file = env_file
        self.examples_list = examples_list
        self.example_file = examples_file
        self.compilation_type = compilation_type
        self.logging_dir = logging_dir
        self.output_dir = output_dir
        self.hosts_file = hosts_file
        self.distribute = distribute
        self.avb_list = avb_list
        self.mode_of_operation = mode_of_operation
        self.compiled_path = compiled_path
        self.check_method_name = check_method_name

        self.examples_dict = {}

        self.validate_inputs()

        self.edc_path = "/project/med/Ethernet/Development/oalaa/stamp/Utilities/ethernet-desgins-compiler/bin/edc"
        self.turnkey_path = os.environ.get("STAMP_REG_PATH") + "/turnKey/main_arguments.py"

        self.initialize_observers()

    def initialize_observers(self):
        self.logger = Loggers(self.logging_dir, "loggings")
        self.monitor = Monitoring(self)
        self.subject = ConcreteSubject()
        self.observer = ConcreteObserver(logger=self.logger, monitor=self.monitor)
        self.subject.attach(self.observer)

    def validate_inputs(self):
        if not self.solution in SUPPORTED_SOLUTIONS._value2member_map_:
            print("unsupported solution")
            sys.exit()
        elif not path.exists(self.env_file):
            print("env file doesn't exist")
            sys.exit()
        elif not path.exists(self.logging_dir):
            os.makedirs(self.logging_dir)
            print("logging directory doesn't exist")
            # sys.exit()
        elif not path.exists(self.output_dir):
            print("output directory doesn't exist")
            sys.exit()
        elif not path.exists(self.hosts_file):
            print("hosts file doesn't exist")
            sys.exit()
        elif not type(self.distribute) == bool:
            print("distribute variable is not boolean")
            sys.exit()
        elif not self.mode_of_operation in MODES_OF_OPERATION._value2member_map_:
            print("unsupported mode of opertaion")
            sys.exit()
        elif not self.check_method_name in METHOD_NAMES._value2member_map_:
            print("method not supported")
            sys.exit()
        elif self.mode_of_operation == "run" and not path.exists(self.compiled_path):
            print("compiled design path doesn't exist")
            sys.exit()
        if (self.mode_of_operation == "all" or self.mode_of_operation == "run") and len(self.avb_list) == 0:
            print("avb list error")
            sys.exit()

    def start(self):
        pdb.set_trace()
        if self.mode_of_operation is MODES_OF_OPERATION.all.value:
            commands = [self.write_command_edc(), self.write_command_turnkey()]
        elif self.mode_of_operation is MODES_OF_OPERATION.run.value:
            commands = [self.write_command_turnkey()]
        elif self.mode_of_operation is MODES_OF_OPERATION.compile.value:
            commands = [self.write_command_edc()]
        else:
            print("wrong mode")
            sys.exit()

        print(commands)
        self.subject.start_process(commands=commands)

    def write_command_edc(self):

        if self.example_file == "":
            command = "{edc} -c --solution {solution} --compile_type {compile_type} --env_file {env_file}" \
                      " --output_dir {output_dir}  --hosts_file {hosts} --export {exports} ".format(
                edc=self.edc_path,
                solution=self.solution,
                compile_type=self.compilation_type,
                env_file=self.env_file,
                output_dir=self.output_dir,
                hosts=self.hosts_file,
                exports=self.logging_dir)
            if self.distribute:
                command += " --distribute "
            for example in self.examples_list:
                command += " --example_name {example} ".format(example=example)
        else:
            command = "{edc} -c --solution {solution} --compile_type {compile_type} --env_file {env_file}" \
                      " --output_dir {output_dir}  --export {exports} --examples_file {file}".format(
                edc=self.edc_path,
                solution=self.solution,
                compile_type=self.compilation_type,
                env_file=self.env_file,
                output_dir=self.output_dir,
                exports=self.logging_dir,
                file=self.example_file)
            if self.distribute:
                command += " --distribute "
        return command

    def write_command_turnkey(self):
        if not self.examples_dict:
            converted_list = [str(element) for element in self.examples_list]
            examples = ",".join(converted_list)
        elif self.examples_dict["test"] == "created":
            converted_list = [str(element) for element in self.examples_list]
            examples = ",".join(converted_list)
        elif self.examples_dict["test"] == "failed":
            print("No examples Passed")
            sys.exit()
        else:
            del self.examples_dict["test"]
            converted_list = [str(element) for element in self.examples_dict.keys()]
            examples = ",".join(converted_list)

        solution = 'eth' if (self.solution is SUPPORTED_SOLUTIONS.vved.value) else '5g' if (
                self.solution is SUPPORTED_SOLUTIONS.v5f.value) else 'eth'

        converted_list = [str(element) for element in self.avb_list]
        avb = ",".join(converted_list)
        command = "python {turnkey} --examples {ex} --solution {sol} --env {env} --log {log} " \
                  "--mode_of_operation {op} --avb_list {avb} --compiled_design {comp} " \
                  " --function_name {fun}".format(
            turnkey=self.turnkey_path,
            ex=examples,
            sol=solution,
            env=self.env_file,
            log=self.logging_dir,
            op="run",
            avb=avb,
            comp=self.compiled_path,
            fun=self.check_method_name
        )
        return command

    def __del__(self):
        del (self.subject)
