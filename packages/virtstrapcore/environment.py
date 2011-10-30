import logging
import tempita
VIRTUALENV_INSTALLED = True
try:
    import virtualenv
except ImportError:
    VIRTUALENV_INSTALLED = False
from virtstrap import *

QUICK_ACTIVATE_TEMPLATE = "quickactivate.sh.tmpl"
QUICK_ACTIVATE_FILE = "quickactivate.sh"

vs_logger = logging.getLogger("virtstrap")

class EnvironmentSectionSettings(SectionSettings):
    __section__ = "environment"
    use_site_packages = BooleanOption(default=False)
    quick_activate_name = StrOption(default="quickactivate.sh")
    custom = StrOption()

class EnvironmentSection(object):
    name = "environment"
    settings = EnvironmentSectionSettings

    def default(self, settings):
        """Create the virtual environment"""
        if not VIRTUALENV_INSTALLED:
            message = ("In order to bootstrap with virtstrap. "
                    "You need virtualenv installed and you "
                    "should not be in an active virtualenv")
            vs_logger.error(message)
            exit_with_error()
        if in_virtualenv():
            message = "Error: You are currently in an active virtualenv."
            vs_logger.error(message)
            exit_with_error()
        # Create a virtual environment into the virtstrap directory
        virtstrap_dir = settings.virtstrap.base_dir
        vs_logger.info("Creating Virtual Environment in {0}"
                .format(virtstrap_dir.abs_path))
        # Create prompt
        prompt = "({0}env) ".format(settings.project.name)
        virtualenv.create_environment(virtstrap_dir.abs_path,
                site_packages=settings.environment.use_site_packages, 
                prompt=prompt)
    
        # Build the file from the template
        vs_logger.info("Creating quickactivate.sh script for virtualenv")
        # Get path to template (it's in the current folder)
        template_path = os.path.join(os.path.dirname(__file__), 
                QUICK_ACTIVATE_TEMPLATE)
        # Load Template
        quick_activate_template = tempita.Template.from_filename(
                template_path)
        # Prepare template context
        context = dict(s=settings)
        # Render template to string
        output_string = quick_activate_template.substitute(context)
        # Open output file for writing
        output_filename = settings.environment.quick_activate_name
        quick_activate_file_path = settings.project.root_dir.join(
                output_filename)
        quick_activate_file = open(str(quick_activate_file_path), 'w')
        # Write to the file
        quick_activate_file.write(output_string)
        quick_activate_file.close()
