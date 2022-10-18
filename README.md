# dvpi_app

## Application for determining DVPI and plant species identification

Web application build using FastAPI containing 3 endpoints:

* Landing page with simple interface for uploading '.csv' file for determining DVPI score (Danish stream plant index, [link to report in Danish](https://dce2.au.dk/pub/sr135.pdf)) or images for species identification
* Species identification using deep learning model trained to identify [100 plant species](https://github.com/KennethTM/dvpi_app/blob/main/static/taxon_list.html) included in DVPI 
* Determine DVPI score by calling an external SOAP API endpoint using a '.csv' file with plant species and cover ([example file](https://github.com/KennethTM/dvpi_app/blob/main/static/example.csv))

Repository contains all necessary file to run the application. To install packages for runtime environment:

`pip install -r requirements.txt`

To run the application locally run:

`uvicorn main:app --reload`

The repository also contains additionally files for serving the application on Heroku.

*Landing page interface*
![Landing page](https://github.com/KennethTM/dvpi_app/blob/main/dvpi_page.png)
