library(tidyverse);library(rgbif)

dvpi <- read_csv("data/dvpi_species_sc.csv") |> 
  select(long_edit, sc)

gbif_keys <- name_backbone_checklist(dvpi$long_edit)

dvpi_keys <- bind_cols(dvpi, gbif_keys)

write_csv(dvpi_keys, "data/dvpi_species_sc_gbif.csv")

res <- occ_download(
  pred_in("taxonKey", dvpi_keys$usageKey),
  pred_in("basisOfRecord", c('HUMAN_OBSERVATION','OBSERVATION','MACHINE_OBSERVATION', 'LIVING_SPECIMEN')),
  pred("mediatype", "StillImage"),
  user = "",
  email="",
  pwd="",
  format="DWCA"
)
