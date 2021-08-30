from aenum import Enum


# SUPPORTED_SOLUTIONS = ['vved', 'v5f']

# COMPILATION_TYPES = ["Simulation", "Emulation", "Emu_Vsim", "Emu_Velclkgen"]

# MODES_OF_OPERATION = ['all', 'compile', 'run']

# METHOD_NAMES = ["run_validation", "validate_wire_delay", "validate_mpg_unlock_errors", "validate_cont_generic",
#                 "validate_performance", "validate_tcl_5g_reg", "validate_py_5g_reg"]


# TODO: turn the lists to enums

class SUPPORTED_SOLUTIONS(Enum):
    vved = "vved"
    v5f = "v5f"


class COMPILATION_TYPES(Enum):
    Simulation = "Simulation"
    Emulation = "Emulation"
    Emu_Vsim = "Emu_Vsim"
    Emu_Velclkgen = "Emu_Velclkgen"


class MODES_OF_OPERATION(Enum):
    all = "all"
    run = "run"
    compile = "compile"


class METHOD_NAMES(Enum):
    run_validation = "run_validation"
    validate_wire_delay = "validate_wire_delay"
    validate_mpg_unlock_errors = "validate_mpg_unlock_errors"
    validate_cont_generic = "validate_cont_generic"
    validate_performance = "validate_performance"
    validate_tcl_5g_reg = "validate_tcl_5g_reg"
    validate_py_5g_reg = "validate_py_5g_reg"


if __name__ == "__main__":
    st = "v5f"
    print(st in SUPPORTED_SOLUTIONS._value2member_map_)
