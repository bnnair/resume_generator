import textwrap
# from src.utils import create_driver_selenium
from dotenv import load_dotenv
from concurrent.futures import ThreadPoolExecutor, as_completed
from logging_config import logger
from string import Template
from services.generator.config import global_config
from utils import template_base

load_dotenv()

class ResumeGenerator:
    def __init__(self):
        pass
    
    @staticmethod
    def _preprocess_template_string(template: str) -> str:
        # Preprocess a template string to remove unnecessary indentation.
        return textwrap.dedent(template)

    def set_resume(self, resume):
        self.resume = resume

    def create_resume(self, style_path, temp_html_path):
        print("---------------------inside the _create_resume method-------------")
        template = Template(global_config.html_template)
        message = template.substitute(
            markdown=self.generate_html_resume(), style_path=style_path)
        message = self._preprocess_template_string(message)
        logger.info(f"Creating resume at {temp_html_path}")
        # logger.info(f"Message: {message}")
        with open(temp_html_path, 'w', encoding='utf-8') as temp_file:
            temp_file.write(message)

    def generate_html_resume(self) -> str:
        def header_fn():
            template = Template(template_base.header_template)
            logger.debug(f"resume in generate html -- {self.resume}")
            message = template.substitute(
                name=self.resume.personalDetails.name,
                email=self.resume.personalDetails.email,
                mobile=self.resume.personalDetails.mobile,
                location=self.resume.personalDetails.location,
                country=self.resume.personalDetails.country,
                linkedin=self.resume.personalDetails.linkedin,
                github=self.resume.personalDetails.github)
            message = self._preprocess_template_string(message)
            # logger.info(f"Message: {message}")
            return message

        def summary_fn():
            template = Template(template_base.summary_template)
            message = template.substitute(
                summary = self.resume.summary.summary
            )
            message = self._preprocess_template_string(message)
            # logger.info(f"Message: {message}")
            return message

        def education_fn():
            education_entries = ""
            child_template = Template(template_base.education_child_template)
            for edu in self.resume.education:
                education_entries = education_entries + child_template.substitute(
                    institution=edu.institution,
                    degree=edu.degree,
                    field_of_study=edu.field_of_study,
                    duration=edu.duration
                )
            education_entries = self._preprocess_template_string(education_entries)
            # logger.info(f"Message: {message}")
            parent_template = Template(template_base.education_parent_template)
            message = parent_template.substitute(education_entries=education_entries)
            return message            


        def work_experience_fn():
            experience_entries = []
            child_template = Template(template_base.experience_child_template)
            parent_template = Template(template_base.experience_parent_template)
            for exp in self.resume.experiences:
                
                # Substitute all variables at once
                entry = child_template.substitute(
                    company=exp.company,
                    position=exp.position,
                    duration=exp.duration,
                    # Create responsibilities list items first
                    responsibilities="".join(f"<li>{r}</li>" for r in exp.responsibilities) 
                                        if exp.responsibilities else ""                
                )
                experience_entries.append(entry)

            # Join all entries at the end
            final_experience_section = parent_template.substitute(experience_entries="".join(experience_entries))
            logger.info(f"Final Experience Section: {final_experience_section}")
            return final_experience_section         

        def achievements_fn():
            achievements_template = Template(template_base.achievements_template)
            achievements = ""
            for achievement in self.resume.achievements:
                logger.debug(f"Achievement: {achievement}")
                achievements +="".join(f"<li><strong>{achievement.name} : </strong>{achievement.description}</li>")
            achievementsList = achievements_template.substitute(
                achievements=achievements
            )
            return achievementsList

        def certifications_fn():
            certifications_template = Template(template_base.certifications_template)
            certifications = ""
            for certification in self.resume.certifications:
                logger.debug(f"certification: {certification}")
                certifications +="".join(f"<li><strong>{certification.name} : </strong>{certification.description}</li>")
            certificationsList = certifications_template.substitute(
                certifications=certifications
            )
            return certificationsList

        def additional_skills_fn():
            skills_template = Template(template_base.skills_template)
            skills = ""
            for skill in self.resume.skills:
                logger.debug(f"skill: {skill}")
                skills +="".join(f"<li><strong>{skill.name} : </strong>({skill.description})</li>")
            skillsList = skills_template.substitute(
                skills=skills
            )
            return skillsList
        
        # Create a dictionary to map the function names to their respective callables
        functions = {
            "header": header_fn,
            "summary": summary_fn,
            "education": education_fn,
            "work_experience": work_experience_fn,
            "achievements": achievements_fn,
            "certifications": certifications_fn,
            "additional_skills": additional_skills_fn,
        }

        # Use ThreadPoolExecutor to run the functions in parallel
        with ThreadPoolExecutor() as executor:
            future_to_section = {executor.submit(
                fn): section for section, fn in functions.items()}
            results = {}
            for future in as_completed(future_to_section):
                section = future_to_section[future]
                try:
                    result = future.result()
                    if result:
                        results[section] = result
                except Exception as exc:
                    logger.debug(f'{section} generated 1 exc: {exc}')
        full_resume = "<body>\n"
        full_resume += f"  {results.get('header', '')}\n"
        full_resume += "  <main>\n"
        full_resume += f"    {results.get('summary', '')}\n"
        full_resume += f"    {results.get('work_experience', '')}\n"
        full_resume += f"    {results.get('achievements', '')}\n"
        full_resume += f"    {results.get('certifications', '')}\n"
        full_resume += f"    {results.get('additional_skills', '')}\n"
        full_resume += f"    {results.get('education', '')}\n"
        full_resume += "  </main>\n"
        full_resume += "</body>"
        return full_resume
