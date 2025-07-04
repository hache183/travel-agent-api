import os
from dotenv import load_dotenv
from langchain_core.tools import tool
from serpapi import GoogleSearch
from pydantic import BaseModel , Field
from typing import Optional
load_dotenv()

class FlightsInput(BaseModel):
	departure_airport: str = Field(description="The departure airport code (IATA).")
	arrival_airport: str = Field(description="The arrival airport code (IATA).")
	outbound_date: str = Field(description="The outbound date (YYYY-MM-DD) e.g. 2024-12-13.")
	return_date: str = Field(description="The return date (YYYY-MM-DD) e.g. 2024-12-19.")
	adults: Optional[int] = Field(1, description="The number of adults. Defaults to 1.")
	children: Optional[int] = Field(0, description="The number of children. Defaults to 0.")
class FlightsInputSchema(BaseModel):
	params: FlightsInput
@tool(args_schema=FlightsInputSchema)
def flights_finder(params: FlightsInput):
	"""
	This tool uses the SerpApi Google Flights API to retrieve flights info.
	Parameters:

	departure_airport (str): The departure airport code (IATA).
	arrival_airport (str): The arrival airport code (IATA).
	outbound_date (str): The outbound date (YYYY-MM-DD) e.g. 2024-12-13.
	return_date (str): The return date (YYYY-MM-DD) e.g. 2024-12-19.
	adults (int): The number of adults. Defaults to 1.
	children (int): The number of children. Defaults to 0.
	Returns: dict: A dictionary containing the flights info. If the API call fails, it returns the
	error message as a string.
	"""

	try:
		params = {
			"api_key": os.getenv("9b822597af73bd915ef0195f764158ee06ef2fd197e2e9444525fc19ddf832d6"),
			"engine": "google_flights",
			"hl": "it",
			"gl": "it",
			"currency": "EUR",
			"stops": "1",
			"departure_id": params.departure_airport,
			"arrival_id": params.arrival_airport,
			"outbound_date": params.outbound_date,
			"return_date": params.return_date,
			"adults" : params.adults,
			"children": params.children
		}
		search = GoogleSearch(params)
		# Tracing
		print("*" * 80)
		print("flights_finder")
		print("*" * 80)
		return search.get_dict()
	except Exception as e:
		return str(e)