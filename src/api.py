from fastapi import FastAPI
from pydantic import BaseModel
from typing import Union, List, Dict
from innoscripta import Innoscripta

class CompanyRequest(BaseModel):
    company_name: str
    company_country: str
    company_website: Union[str, None] = None

class SearchResponse(BaseModel):
    products_services: Union[List[str], None] = None
    keywords: Union[List[str], None] = None
    classification: Union[List[str], None] = None
    image_urls: Union[List, None] = None


app = FastAPI()

@app.get("/company/", response_model = SearchResponse)
async def get_company_info(company_request: CompanyRequest):
    name = company_request.company_name
    country = company_request.company_country
    website = company_request.company_website
    inno = Innoscripta(name=name, country=country, website=website)

    response = inno.main()

    return response