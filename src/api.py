from fastapi import FastAPI
from pydantic import BaseModel
from typing import Union, List, Dict
from innoscripta import Innoscripta
import logging
import os

class CompanyRequest(BaseModel):
    company_name: str
    company_country: str
    company_website: Union[str, None] = None


class SearchResponse(BaseModel):
    products_services: Union[List[str], None] = None
    keywords: Union[List[str], None] = None
    company_classification: Union[List[str], None] = None
    images: Union[List, None] = None

logger = logging.getLogger(__name__)
logger.setLevel(os.getenv("LOGGER_LEVEL", logging.INFO))

app = FastAPI()


@app.get("/ping/")
def pong():
    return "pong"


@app.get("/company/", response_model=SearchResponse)
async def get_company_info(
    company_name: str, company_country: str, company_website: str = None
):
    name = company_name
    country = company_country
    website = company_website
    inno = Innoscripta(name=name, country=country, website=website)

    response = inno.main()
    print(response)
    logger.info("Response from Langchain: {response}")

    return response
