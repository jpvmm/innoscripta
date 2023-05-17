import os

from dotenv import load_dotenv
from langchain import PromptTemplate
from langchain.chains import LLMChain
from langchain.llms import OpenAI
from serpapi import GoogleSearch

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
SERPAPI_KEY = os.getenv("SERPAPI_KEY")


class Innoscripta:
    """Class of innoscript solution"""

    def __init__(self, name: str, country: str, website: str = None):
        """
        Initialize the Innoscripta search engine.

        Args:
            name (str): name of the company
            country (str): name of the country of the company
            website (str): website of the company
        """
        self.name = name
        self.country = country
        if not website:
            self.website = ""
        else:
            self.website = website

    def main(self):
        """
        Will do the innoscripta querying
        """
        parsed_gpt_ouput = self.gpt_call()
        google_query = self.google_query_formation(parsed_gpt_ouput["products_services"])
        imgs = self.google_search(google_query)
        parsed_gpt_ouput["images"] = imgs

        return parsed_gpt_ouput

    def gpt_call(self) -> dict:
        """
        Will call gpt-3.5-turbo for querying informations about a company.

        Args:
            name(str): Name of the company
            country(str): Country of the company
            website(str): Website of the company

        Results:
            output(dict) = Parsed output of OpenAIAPI
        """
        llm = OpenAI(model_name="gpt-3.5-turbo", temperature=0)

        prompt = self.prompt_template()

        chain = LLMChain(llm=llm, prompt=prompt)
        output = chain.run(
            {
                "name_of_company": self.name,
                "country_of_company": self.country,
                "website_of_company": self.website,
            }
        )
        parsed = self.parse_output(output)

        return parsed

    def google_query_formation(self, products: list) -> str:
        """
        Will manipulate strings to create Google search query

        Return:
            google_query(str): Google query
        """
        products_services_str = " + ".join(products)

        return " + ".join([self.name, products_services_str])

    def google_search(self, query: str) -> list:
        """
        Will query google for images based in the output of OpenAIAPI

        Args:
            query(str): Formated query using the output openaiAPI

        Results:
            imgs(list): List with URLs for images
        """
        search = GoogleSearch(
            {
                "q": query,
                "engine": "google_images",
                "location": "Austin, Texas",
                "api_key": SERPAPI_KEY,
            }
        )
        response = search.get_dict()
        imgs = [r["original"] for r in response["images_results"][:5]]

        return imgs

    def prompt_template(self):
        template = """
        I'll give you three inputs. These inputs will be the name of the company, 
        the country of the company, and the website company. The website of the company
        is not mandatory, so it can be just an empty string.
        If the website was not provided, gather all info you can with just name and country.
        You have to give me the products and services that the company offers as output.
        you dont need to give me nothing more than the ouput.



        input:
        IKEA Deutschland GmbH & Co. KG
        Germany
        ikea.com

        the output must be in this format, please use it:
        "products_services": Furniture, Home decor, Kitchen and Dining;
        "keywords":furniture, storage, lighting;
        "company_classification":5712 (Furniture Stores) – SIC, 442110 (Furniture Stores) – NAICS
        do it yourself now.
        input:
        {name_of_company}
        {country_of_company}
        {website_of_company}

        what is the output?
        """

        prompt = PromptTemplate(
            input_variables=[
                "name_of_company",
                "country_of_company",
                "website_of_company",
            ],
            template=template,
        )

        return prompt

    def parse_output(self, output_langchain: str) -> dict:
        """
        Will parse the output_langchain of the Langchain query

        Args:
            output(str): The output_langchain of Langchain query.

        Returns:
            result_dict(dict): the parsed output_langchain to dict
        """

        result_dict = {}

        sections = [section.strip() for section in output_langchain.split(";")]

        for section in sections:
            if section:
                header, values_str = section.split(":")
                header = header.strip('"')
                values = [value.strip() for value in values_str.strip("[]").split(",")]

                result_dict[header] = values

        return result_dict
