# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from src.module.smoketestanalyzer import SmokeTestAnalyzer


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    module = SmokeTestAnalyzer(solution='vved',
                               env_file='/home/oalaa/maadi/VirtualEthernet_v11.4.0/b4233/vved1140.bash',
                               examples_list=["CGMII"], compilation_type='Simulation',
                               logging_dir='/home/hwalied/Project/tmp-logs',
                               output_dir='/home/hwalied/Project/tmp-logs',
                               hosts_file='/home/hwalied/tk/stamp_master/Utilities/ethernet-desgins-compiler/hosts',
                               distribute=true,
                               avb_list=[1], mode_of_operation="compile", compiled_path="",
                               check_method_name="run_validation")
    module.start()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
