"""JWG architecture"""

from ... import ir
from ...binutils.assembler import BaseAssembler
from ..arch import Architecture
from ..arch_info import ArchInfo, TypeInfo
from ..data_instructions import Db, Dcd2, Dd, data_isa
from ..generic_instructions import Alignment, Label, RegisterUseDef
from ..runtime import get_runtime_files
from . import instructions, registers
from .registers import register_classes

