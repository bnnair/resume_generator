import os
from pathlib import Path
import tempfile
# import inquirer
from services.generator.config import global_config
from utils.utils import HTML_to_PDF
from logging_config import logger


class FacadeManager:
    def __init__(self, style_manager, resume_generator, resume_object):
        logger.debug(
            "-------------------inside the init of manager_facade.py--------------")
        lib_directory = Path(__file__).resolve().parents[2]
        global_config.STYLES_DIRECTORY = os.path.join(lib_directory,"utils", "resume_styles")
        logger.debug(f"global_config.STYLES_DIRECTORY===={global_config.STYLES_DIRECTORY}")
        self.style_manager = style_manager
        self.style_manager.set_styles_directory(global_config.STYLES_DIRECTORY)
        self.resume_generator = resume_generator
        self.resume_generator.set_resume(resume_object)
        self.selected_style = None

    def prompt_user(self, choices: list[str], message: str) -> str:
        return choices[0]

    def choose_style(self):
        styles = self.style_manager.get_styles()
        print(styles)
        if not styles:
            print("No styles available")
            return None
        formatted_choices = self.style_manager.format_choices(styles)
        logger.debug(f"formatted_choices----:{formatted_choices}")
        selected_choice = self.prompt_user(
            formatted_choices, "Which style would you like to adopt?")
        self.selected_style = selected_choice.split(' (')[0]

    def pdf_base64(self):

        if self.selected_style is None:
            raise ValueError(
                "a Style should be selected to generate a PDF.")

        style_path = self.style_manager.get_style_path(self.selected_style)

        with tempfile.NamedTemporaryFile(delete=False, mode='w', suffix='.html', encoding='utf-8') as temp_html_file:
            temp_html_path = temp_html_file.name
            logger.debug(
                f"create resume job description text using the resume generator..")
            self.resume_generator.create_resume(
                style_path, temp_html_path)

        logger.debug(f"the html resume is converted to pdf .....")
        pdf_base64 = HTML_to_PDF(temp_html_path)
        os.remove(temp_html_path)
        # logger.info(f"Resume PDF Base64: {pdf_base64}")
        return pdf_base64
