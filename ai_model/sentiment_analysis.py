import requests
from dotenv import load_dotenv, find_dotenv
import os

print("Current Working Directory:", os.getcwd())

load_dotenv(dotenv_path="config.env")

API_TOKEN = os.getenv("API_TOKEN")

API_URL = "https://api-inference.huggingface.co/models/cardiffnlp/twitter-roberta-base-sentiment-latest"
headers = {"Authorization": f"Bearer {API_TOKEN}"}

def query(payload):
	response = requests.post(API_URL, headers=headers, json=payload)
	print(response.json())
	return response.json()
	
output = query({
	"inputs": "I am not sure if i like you"
})