library(data.table);library(rjson)

dvpi_gbif <- fread("data/dvpi_species_sc_gbif.csv")

#gbif data
media <- fread("data/0364086-210914110416597/multimedia.txt")
occ <- fread("data/0364086-210914110416597/occurrence.txt")

occ_sub <- occ[, .(gbifID, taxonKey, datasetName)]

media_taxon <- media[occ_sub, on="gbifID"]

valid_licenses <- c("http://creativecommons.org/licenses/by/4.0/",
                    "http://creativecommons.org/publicdomain/zero/1.0/")

media_valid <- media_taxon[license %in% valid_licenses & taxonKey %in% dvpi_gbif$usageKey & format == "image/jpeg" & datasetName == "iNaturalist research-grade observations", ]

taxon_occur <- table(media_valid$taxonKey)
taxon_occur_top_100 <- names(sort(taxon_occur, decreasing = TRUE)[1:100])

#sample 250 urls for each taxon
url_list <- lapply(taxon_occur_top_100, \(x) sample(media_valid[taxonKey == x, identifier], size = 250))
names(url_list) <- taxon_occur_top_100

url_list_json <- toJSON(url_list)
writeLines(url_list_json, "data/url_list_100.json")
