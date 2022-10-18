library(tidyverse);library(rgbif)

#Read file containing species of interest
dvpi <- read_csv("data/dvpi_species_sc.csv") |> 
  select(long_edit, sc)

#Lookup GBIF names/ids/keys for each species
gbif_keys <- name_backbone_checklist(dvpi$long_edit)

#Bind to dataframe and write to file
dvpi_keys <- bind_cols(dvpi, gbif_keys)

write_csv(dvpi_keys, "data/dvpi_species_sc_gbif.csv")

#Create GBIF request for all species with images (requires GBIF user)
#The resulting Darwin Core Archive can be downloaded from gbif.org
res <- occ_download(
  pred_in("taxonKey", dvpi_keys$usageKey),
  pred_in("basisOfRecord", 
          c('HUMAN_OBSERVATION','OBSERVATION', 
            'MACHINE_OBSERVATION', 'LIVING_SPECIMEN')),
  pred("mediatype", "StillImage"),
  user = "INSERT USERNAME",
  email = "INSERT EMAIL",
  pwd = "INSERT PASSWORD",
  format = "DWCA"
)
