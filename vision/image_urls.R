library(data.table);library(rjson)

#Read file with species data
dvpi_gbif <- fread("data/dvpi_species_sc_gbif.csv")

#Read text files from the GBIF request
#One file has media data and the other species occurrence data
media <- fread("data/0364086-210914110416597/multimedia.txt")
occ <- fread("data/0364086-210914110416597/occurrence.txt")
occ_sub <- occ[, .(gbifID, taxonKey, datasetName)]

#Join files
media_taxon <- media[occ_sub, on="gbifID"]

#Define the licenses to filter 
valid_licenses <- c("http://creativecommons.org/licenses/by/4.0/",
                    "http://creativecommons.org/publicdomain/zero/1.0/")

#Filter media data
#In addition to licenses, we also filter only jpeg and observations from 
#the iNaturalist dataset which are generally of high quality (good labels)
media_valid <- media_taxon[license %in% valid_licenses & 
                             taxonKey %in% dvpi_gbif$usageKey & 
                             format == "image/jpeg" & 
                             datasetName == "iNaturalist research-grade observations", ]

#Data has been requested for 194 species 
#but we select the 100 most common for our classification model
#Get the top 100 species with most media data
taxon_occur <- table(media_valid$taxonKey)
taxon_occur_top_100 <- names(sort(taxon_occur, decreasing = TRUE)[1:100])

#For each of the 100 species we sample 250 URLs for each species
url_list <- lapply(taxon_occur_top_100, 
                   \(x) sample(media_valid[taxonKey == x, identifier], size = 250))
names(url_list) <- taxon_occur_top_100

#Convert to JSON and write to file
url_list_json <- toJSON(url_list)
writeLines(url_list_json, "data/url_list_100.json")
