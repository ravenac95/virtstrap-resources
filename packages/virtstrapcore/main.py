"""
virtstrapcore.main
==================

The main controller for virtstrap after the 
bootstrapping process has completed. 

VirtStrap Core ensures that the core sections
of virtstrap are handled before any extension sections. 
For now this seems to be the best way to handle it
"""
import logging
vs_logger = logging.getLogger("virtstrap")

class CoreUninitialized(Exception):
    pass

class VirtStrapCore(object):
    def __init__(self, options=None, args=None, settings=None):
        self._settings = settings
        self._options = options
        self._args = args
        self._initialized = False
        self._core_sections = []

    def initialize(self, options, args, settings):
        vs_logger.debug("Initializing Core")
        # Parse the settings
        self._initialized = True
        self._settings = settings
        self._options = options
        self._args = args
        core_sections = self._core_sections
        for section in core_sections:
            section_settings = section.settings
            if not section_settings:
                continue
            settings.parse_section(section_settings)

    def execute_command(self):
        """Executes command from command line"""
        if not self._initialized:
            raise CoreUninitialized()
        args = self._args
        arg_length = len(args)
        command = "default"
        if arg_length > 0:
            command = args[0]
        core_sections = self._core_sections
        settings = self._settings
        for section in core_sections:
            section_command = getattr(section, command, None)
            if section_command:
                vs_logger.debug("Section {0} running command {1}".format(
                    section.name, command))
                section_command(settings)
    
    def register_core_sections(self, *core_sections):
        self._core_sections.extend(core_sections)


