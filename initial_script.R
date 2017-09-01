# initial model playing
library(tidyverse)
library(skimr)

epl <- read_csv("epl_data_all_columns.csv")

weights <- tribble(~postion, ~var, ~weight,
                   "goalkeeper", "goal", 0,
                   "goalkeeper", "assist", 0
                   "goalkeeper", "ict", 0,
                   "goalkeeper", "form", .1,
                   "goalkeeper", "bps", .3,
                   "goalkeeper", "clean sheet", .3,
                   "goalkeepr", "saves", .3
                   "forward", "goal", .35,
                   "forward", "assist", .20,
                   "forward", "ict", .15,
                   "forward", "form", .10,
                   "forward", "bps", .05,
                   "forward", "clean sheet", 0,
                   "midfielder", "goal", .35,
                   "midfielder", "assist", .20,
                   "midfielder", "ict", .15,
                   "midfielder", "form", .10,
                   "midfielder", "bps", .05,
                   "midfielder", "clean sheet", 0,
                   "forward", "goal", .35,
                   "forward", "assist", .20,
                   "forward", "ict", .15,
                   "forward", "form", .10,
                   "forward", "bps", .05,
                   "forward", "clean sheet", 0


                   )

relevant_vars <- epl %>%
  select(name = web_name,
         goals_scored,
         assists,
         ict_index,
         form,
         bps,
         position = element_type) %>%
  mutate(postion = case_when(1 ~ "goalkeeper",
                             2 ~ "defender",
                             3 ~ "midfielder",
                             4 ~ "forward"))

# vars_zscores

# coeffs

# multiply
