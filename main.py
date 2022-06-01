from typing import List
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import zeep
import pickle 
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

id_latin_dict = pickle.load(open("data/id_latin_dict.p", "rb"))

app = FastAPI()
 
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["POST"],
    allow_headers=["*"],
)

wsdl = 'http://service.dvpi.au.dk/1.0.0/DCE_DVPI.svc?singleWsdl'
client = zeep.Client(wsdl=wsdl)

def parse_response(resp):
  resp_split = resp.split(" ")
  resp_dict = {i.split("=")[0]: float(i.split("=")[1].strip('\"')) for i in resp_split[1:4]}
  return(resp_dict)

class Item(BaseModel):
    art: str
    dkg: str

@app.post("/dvpi")
async def get_dvpi(items: List[Item]):

    spec_list = [i.art for i in items]
    dkg_list = [i.dkg for i in items]
    id_list = [id_latin_dict.get(i) for i in spec_list]

    if None in id_list:
      id_none = [i for i, j in zip(spec_list, id_list) if j == None]
      raise HTTPException(status_code=404, detail= "Stancode not found for: " + ", ".join(id_none))

    body_items = ['<sc1064 ID="' + i + '" DKG="' + c + '" />' for i, c in zip(id_list, dkg_list)]

    request = "<DVPI_Input>" + "".join(body_items) + "</DVPI_Input>"

    response = client.service.DVPI(request)

    response_parsed = parse_response(response)

    return response_parsed

app.mount("/", StaticFiles(directory="static", html=True), name="static")
