from pathlib import Path
from loguru import logger
import json
import sys
import time
import platform
import os
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService

# def save_to_jsonfile(resume: dict):
#     logger.info("inside the save resume json file")
#     json_resume_folder = Path(__file__).resolve().parent.parent
#     logger.debug(f"json resume folder----> {json_resume_folder}")
#     json_resume_file = json_resume_folder.joinpath("data", "resume.json")    
#     logger.debug(f"json resume file --------> {json_resume_file}")
    
#     # Save to a JSON file
#     with open(json_resume_file, "w", encoding="utf8") as json_file:
#         json.dump(resume, json_file, indent=4, ensure_ascii=False)  # `indent` for pretty formatting


def save_jobDesc(jobDesc : dict, file_path:str):
    logger.info("inside the save job desc method..")
    jd_file = Path(file_path)
    logger.debug(f"jd folder----> {jd_file}")
    logger.debug(f"job Desc file --------> {jobDesc.dict()}")
   
    with open(jd_file, "w", encoding="utf8") as jd_file:
           json.dump(jobDesc.dict(), jd_file, indent=4, ensure_ascii=False) 


def save_to_jsonfile(resume: dict, file_path: str):
    """Save the resume to a JSON file."""
    json_resume_file = Path(file_path) 
    resume_data = resume
    logger.info(f"Saving resume to {json_resume_file}")
    # Save to a JSON file
    with open(json_resume_file, "w", encoding="utf8") as json_file:
        json.dump(resume_data, json_file, indent=4, ensure_ascii=False) 
        
        
def create_driver_selenium():
    options = get_chrome_browser_options()  # Use the method to get Chrome options

    chrome_install = ChromeDriverManager().install()
    folder = os.path.dirname(chrome_install)
    if platform.system() == "Windows":
        chromedriver_path = os.path.join(folder, "chromedriver.exe")
    else:
        chromedriver_path = os.path.join(folder, "chromedriver")
    service = ChromeService(executable_path=chromedriver_path)
    return webdriver.Chrome(service=service, options=options)


def HTML_to_PDF(FilePath):
    if not os.path.isfile(FilePath):
        raise FileNotFoundError(
            f"The specified file does not exist: {FilePath}")
    FilePath = f"file:///{os.path.abspath(FilePath).replace(os.sep, '/')}"
    driver = create_driver_selenium()

    try:
        driver.get(FilePath)
        time.sleep(5)
        pdf_base64 = driver.execute_cdp_cmd("Page.printToPDF", {
            "printBackground": True,
            "landscape": False,
            "paperWidth": 8.0,
            "paperHeight": 11.0,
            "marginTop": 0.5,
            "marginBottom": 0.5,
            "marginLeft": 0.75,
            "marginRight": 0.75,
            "displayHeaderFooter": False,
            "preferCSSPageSize": True,
            "generateDocumentOutline": False,
            "generateTaggedPDF": False,
            "transferMode": "ReturnAsBase64"
        })
        return pdf_base64['data']
    except WebDriverException as e:
        raise RuntimeError(f"WebDriver exception occurred: {e}")
    finally:
        driver.quit()
        
        
def get_chrome_browser_options():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-gpu")
    options.add_argument("window-size=1200x800")
    options.add_argument("--disable-background-timer-throttling")
    options.add_argument("--disable-backgrounding-occluded-windows")
    options.add_argument("--disable-translate")
    options.add_argument("--disable-popup-blocking")
    options.add_argument("--no-first-run")
    options.add_argument("--no-default-browser-check")
    options.add_argument("--single-process")
    options.add_argument("--disable-logging")
    options.add_argument("--disable-autofill")
    options.add_argument("--disable-plugins")
    options.add_argument("--disable-animations")
    options.add_argument("--disable-cache")
    options.add_experimental_option(
        "excludeSwitches", ["enable-automation", "enable-logging"])

    options.add_argument("--single-process")
    return options
