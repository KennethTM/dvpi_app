from typing import List
from fastapi import FastAPI, HTTPException, File, UploadFile, Request
from pydantic import BaseModel
import zeep
import pickle 
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
from io import BytesIO
from fastai.vision.all import *
import numpy as np
from fastapi.templating import Jinja2Templates

#uvicorn main:app --reload

app = FastAPI()
 
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#DVPI calculator
id_latin_dict = pickle.load(open("data/id_latin_dict.p", "rb"))

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

#Image classifier
model_weights = "data/images_preproc/resnet_18_100.export"
model = load_learner(model_weights)
taxon_key_dict = pickle.load(open("data/taxon_key_dict.p", "rb"))

@app.post("/predict")
async def predict_image(file: UploadFile = File(...)):

  request_content = await file.read()

  try:
    image = np.array(Image.open(BytesIO(request_content)))
  except:
    raise HTTPException(status_code=422, detail="Unable to process file")

  pred, pred_idx, probs = model.predict(image)

  #get top preds
  val, idx = probs.topk(5)
  top_5_labels = model.dls.vocab[idx]

  label = ", ".join(["{} {}%".format(taxon_key_dict[l], int(probs[i]*100)) for l, i in zip(top_5_labels, idx)])
  
  #label = f'{pred} ({int(probs[pred_idx]*100)} %)'

  return {"response": label}

#Static files
#app.mount("/", StaticFiles(directory="static/", html=True), name="static")

app.mount("/static", StaticFiles(directory="static/"), name="static")

templates = Jinja2Templates(directory="templates")

@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse(
        "index.html", {"request": request}
    )
