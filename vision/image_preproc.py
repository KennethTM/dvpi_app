from PIL import Image 
from pathlib import Path
import os
import pandas as pd
import pickle

#Save taxonkey-name dict
df = pd.read_csv("data/dvpi_species_sc_gbif.csv")
taxon_key_dict = {str(k): v for k, v in zip(df["usageKey"], df["long_edit"])}

with open("data/taxon_key_dict.p", "wb") as output_file:
    pickle.dump(taxon_key_dict, output_file)

#Preprocess images to smaller size
data_dir = Path("data")
image_dir = data_dir/"images"
preproc_dir = data_dir/"images_preproc"
size = (640, 640) 

for dir in image_dir.glob('*'):

    for img in dir.glob('*.jpeg'):
        
        _, _, taxon, file = img.parts

        dir_out = preproc_dir/taxon
        image_out = dir_out/file

        if not os.path.exists(dir_out):
            os.mkdir(dir_out)

        try:
            image=Image.open(img)
        except IOError as er:
            print(er)
            continue

        if os.path.exists(image_out):
            continue

        image.thumbnail(size) 
        image.save(dir_out/file) 
