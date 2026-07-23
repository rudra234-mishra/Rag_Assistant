import os
from dotenv import load_dotenv
load_dotenv()
from langchain_openai import AzureChatOpenAI,AzureOpenAIEmbeddings
from logging_config import logger

##LLM MODEL
try:
    logger.info("Model Connection Start :")
    llm_model=AzureChatOpenAI(
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        api_version=os.getenv("api_version"),
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        model=os.getenv("AZURE_OPENAI_MODEL")
    )
    logger.info("Model Connection Succesfull :")

except Exception as e:
    logger.info("Model Connection Failed %s",e)

##EMBEDDING MODEL
try:
    logger.info("Model Connection Start :")
    emd_model=AzureOpenAIEmbeddings(
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        api_version=os.getenv("api_version"),
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        azure_deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT")
    )
    logger.info("Model Connection Succesfull :")

except Exception as e:
    logger.info("Model Connection Failed %s",e)