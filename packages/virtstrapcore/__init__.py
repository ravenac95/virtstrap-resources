from main import VirtStrapCore
from environment import EnvironmentSection
from install import InstallSection

virtstrap_core = VirtStrapCore()
virtstrap_core.register_core_sections(EnvironmentSection(), InstallSection())
