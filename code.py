# load packages ---------------------------------------------------------------

import pydytuesday
import pandas
import great_tables

# load data -------------------------------------------------------------------

pydytuesday.get_date('2025-04-29')
user2025 = pandas.read_csv('https://raw.githubusercontent.com/rfordatascience/tidytuesday/main/data/2025/2025-04-29/user2025.csv')

# make table ------------------------------------------------------------------

program <- program_raw |>
  mutate(
    content = str_replace_all(content, "\\*", "<br><br>*"),
    content = str_replace_all(content, ": NA", ": None"),
    content = str_replace(content, "Learning goals:", "<br>**Learning goals:**"),
    content = str_replace(content, "Target audience:", "<br>**Target audience:**"),
    content = str_replace(content, "Prerequisites:", "<br>**Prerequisites:**"),
    speakers = str_replace_all(speakers, "\\;", ","),
    co_authors = str_replace_all(co_authors, "\\;", ","),
    co_authors = if_else(is.na(co_authors), "", co_authors),
    formatted_date = format(date, format = "%a, %b %e, %Y"),
    info = if_else(
      session == "Poster",
      paste0(
      "<a style='color:#2165b6;'>**",title,"**</a>", 
      "<br><br><details><summary>More info</summary>", 
      "<a style='font-size:90%;'>", 
      content, 
      "<br><br>**Date and time:** ", formatted_date, " - ", time,
      "<br><br>**Author(s):** ", speakers, 
      if_else(co_authors == "", "", paste(";", co_authors)), 
      "<br><br>**Keyword(s):** ", keywords, 
      "</a>",
      "</details>"
      ),
      paste0(
      "<a style='color:#2165b6;'>**",title,"**</a>", 
      "<br><br><details><summary>More info</summary>", 
      "<a style='font-size:90%;'>", 
      content, 
      "<br><br>**Date and time:** ", formatted_date, " - ", time,
      "<br><br>**Author(s):** ", speakers, 
      if_else(co_authors == "", "", paste(";", co_authors)), 
      "<br><br>**Keyword(s):** ", keywords, 
      "<br><br>**Video recording available after conference:** ", video_recording, 
      "</a>",
      "</details>"
      )
    )
    ,
    speakers = str_replace_all(speakers, "\\, ", "<br>")
  ) |>
  relocate(info, .after = room) |>
  select(!c(id, submitter_email, title, content, video_recording, co_authors, formatted_date, keywords))
