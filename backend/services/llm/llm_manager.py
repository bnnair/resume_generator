from abc import ABC, abstractmethod
from langchain_core.messages import BaseMessage
from logging_config import logger
from openai import OpenAI

from langchain_openai import ChatOpenAI
from services.llm.config_manager import ConfigManager
from tenacity import retry, retry_if_exception, retry_if_result, stop_after_attempt, wait_fixed
from openai import AuthenticationError, APIError, APITimeoutError


def is_empty_response(response):
    """Check if the response is empty or invalid."""
    # logger.info(f"response : {response}")
    empty = response is None or response.strip() == ""
    if empty:
        logger.warning("Empty response detected. Retrying...")
    return empty


### StrategyPattern
class AIModel(ABC):
    @abstractmethod
    def invoke(self, prompt: str) -> str:
        pass
    
class OpenAIModel(AIModel):
    def __init__(self, api_key: str, llm_model: str):
        self.model = ChatOpenAI(model_name=llm_model, openai_api_key=api_key,
                                temperature=0.4)
    @retry(
        stop=stop_after_attempt(3),  # Max 3 tries
        wait=wait_fixed(2),          # 2-second delay
        retry=(
            retry_if_exception((AuthenticationError, APIError, APITimeoutError)) |   # Auto-retry on exceptions
            retry_if_result(is_empty_response)  # Retry on empty responses
        )
    )
    def invoke(self, prompt: str) -> BaseMessage:
        logger.debug("Invoking OpenAI API")
        try:
            response = self.model.invoke(prompt)
            logger.debug(f"response : {response}")
            return response
        except Exception as e:
            logger.error(f"Error occurred while invoking openai llm: {e}")
            raise  # Re-raise the exception for retry

class DeepSeekModel(AIModel):
    def __init__(self, api_key: str,  llm_model: str):       
        self.api_key = api_key
        self.llm_model = llm_model
        logger.debug(f"self.api_key : {self.api_key}")
        logger.debug(f"self.llm_model : {self.llm_model}")  

    @retry(
    stop=stop_after_attempt(3),  # Max 3 tries
    wait=wait_fixed(2),          # 2-second delay
    retry=(
        retry_if_exception((AuthenticationError, APIError, APITimeoutError)) |   # Auto-retry on exceptions
        retry_if_result(is_empty_response)  # Retry on empty responses
        )
    )
    def invoke(self, prompt: str) -> BaseMessage:
        logger.debug("Invoking DeepSeek API")
        try:
            # Call the Deepseek API
            client = OpenAI(api_key=self.api_key, base_url="https://openrouter.ai/api/v1") 
            logger.debug(f"client : {client}")
            logger.info(f"prompt-------: {prompt}")
            logger.info(f"llm model -----> {self.llm_model}")
            response = client.chat.completions.create(
                model=self.llm_model, 
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,  # Controls creativity (0 = deterministic, 1 = creative)
                # max_tokens=500,   # Limit the length of the response
            )
            logger.debug(f"response-------------------------------- : {response}")
            return response.choices[0].message.content.strip()

        except Exception as e:
            # Handle errors gracefully
            logger.error(f"Error calling Deepseek LLM: {e}")
            raise    
    
class AIAdapter:
    def __init__(self, model_type: str):
        logger.debug(f"model type in AIAdapter : {model_type}")
        configs = ConfigManager.update_config()
        self.model = self._create_model(configs, model_type)

    def _create_model(self, configs: dict, model_type : str) -> AIModel:
        logger.debug(f"model type in create model of AIAdapter : {model_type}")
        logger.debug(f"configs in create model of AIAdapter : {configs}")
        for config in configs:
            logger.debug(f"config in create model of AIAdapter : {config}")
            if model_type in config.get("name"):
                llm_model = config['model_name'][0]
                logger.debug(f"llm_model : {llm_model}")
                llm_api_key = config['api_key']
                logger.debug(f"Using {model_type} with {llm_model}")
                break
            
        if model_type == "openai":
            return OpenAIModel(api_key=llm_api_key, llm_model=llm_model)
        elif model_type == "deepseek":
            return DeepSeekModel(api_key=llm_api_key, llm_model=llm_model)
        else:    
            raise ValueError(f"Unsupported model type: {model_type}")
        
        
    def invoke(self, prompt: str) -> str:
        return self.model.invoke(prompt)

