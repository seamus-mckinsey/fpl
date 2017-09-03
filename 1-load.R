#' Goal of this script is to download past history of players for
#' model training and testing.

# packages ----------------------------------------------------------------
library(tidyverse)
library(rvest)
library(purrr)

# load data ---------------------------------------------------------------

fpl_read <- function(player_number){
  
  fantasy_url <- 'https://fantasy.premierleague.com/drf/element-summary/'
  
  conn <- paste0(fantasy_url, player_number)
  
  read_html(conn) %>% 
    xml2::xml_text("history_past") %>% 
    jsonlite::fromJSON()
  
}

players_df <- tibble(player_number = 1:543) %>% 
  mutate(data = map(player_number, fpl_read))


# wrangle -----------------------------------------------------------------

fetch_stats <- function(index){
  players_df$data[[index]][[1]]
}

past_seasons <- players_df %>% 
  mutate(past_seasons = map(player_number, fetch_stats)) 


         