import logging
import imp
import os
from subprocess import call
from virtstrap import *

vs_logger = logging.getLogger("virtstrap")

class InstallSectionSettings(SectionSettings):
    __section__ = "install"
    requirements = ListOption()
    scripts = ListOption()

class RequirementsFileNotFound(Exception):
    pass

class InstallSection(object):
    name = "install"
    settings = InstallSectionSettings

    def default(self, settings):
        """Create the virtual environment"""
        install_settings = settings.install

        requirements = install_settings.requirements
        old_path = os.environ['PATH']
        virtstrap_bin_path = settings.virtstrap.bin_path.abs_path
        os.environ['PATH'] = "{0}:{1}".format(virtstrap_bin_path,
                old_path)

        vs_logger.debug(str(install_settings._data))
        if requirements:
            self._requirements_installer(settings, requirements)
        
        scripts = install_settings.scripts
        if scripts:
            self._scripts_installer(settings, scripts)

        os.environ['PATH'] = old_path
        
    def _requirements_installer(self, settings, requirements_files):
        """Executes pip requirements"""
        virtstrap_bin_path = settings.virtstrap.bin_path
        pip_bin = virtstrap_bin_path.join("pip").abs_path
        pip_command = "install"
        root_dir = settings.project.root_dir
        vs_logger.debug("Requirements {0}".format(requirements_files))

        for requirements_file in requirements_files:
            reqs_file_path = root_dir.join(requirements_file).abs_path
            if not os.path.isfile(reqs_file_path):
                vs_logger.error('"{0}" requirements file not found.'
                        .format(requirements_file))
                ask_to_skip()
            call([pip_bin, pip_command, "-r", requirements_file])

    def _scripts_installer(self, settings, scripts):
        """Executes python scripts"""
        config_dir = settings.virtstrap.config_dir

        for script in scripts:
            script_path = config_dir.join(script)
            # Take the .py out of the name
            script_module_name = script.split(".")[0]
            # make an arbitrary name
            conf_module_path = "_".join(["conf", script_module_name])
            try:
                script_module = imp.load_source(conf_module_path, 
                        str(script_path))
            except ImportError:
                vs_logger.exception('Script at "{0}" not found'
                        .format(script_path))
                ask_to_skip()
            else:
                script_module.script_run(settings)

