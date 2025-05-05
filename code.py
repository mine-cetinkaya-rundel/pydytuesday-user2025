# load packages ---------------------------------------------------------------

import pydytuesday
import pandas
import great_tables

# load data -------------------------------------------------------------------

pydytuesday.get_date('2025-04-29')
user2025 = pandas.read_csv('https://raw.githubusercontent.com/rfordatascience/tidytuesday/main/data/2025/2025-04-29/user2025.csv')

# make table ------------------------------------------------------------------

from siuba import _
from siuba.dply.vector import if_else
from siuba.data import mutate, select, relocate
import pandas as pd

# Define paste0 and paste helpers
def paste0(*args):
    return "".join(str(a) for a in args)

def paste(*args):
    return ", ".join(str(a) for a in args)

# If using paste0 and paste inside if_else with siuba, wrap them as functions returning lambdas:
from siuba.siu import Call, make_sym
from functools import partial

def paste0_fn(*args):
    return Call("__call__", paste0, *args)

def paste_fn(*args):
    return Call("__call__", paste, *args)

# Run pipeline and assign to new DataFrame
program_cleaned = (
    program_raw
    >> mutate(
        content = _.content.str.replace(r"\*", "<br><br>*", regex=True),
        content = _.content.str.replace(": NA", ": None"),
        content = _.content.str.replace("Learning goals:", "<br>**Learning goals:**"),
        content = _.content.str.replace("Target audience:", "<br>**Target audience:**"),
        content = _.content.str.replace("Prerequisites:", "<br>**Prerequisites:**"),
        speakers = _.speakers.str.replace(";", ","),
        co_authors = _.co_authors.str.replace(";", ","),
        co_authors = _.co_authors.fillna(""),
        formatted_date = _.date.dt.strftime("%a, %b %-d, %Y"),

        info = if_else(
            _.session == "Poster",
            paste0_fn(
                "<a style='color:#2165b6;'>**", _.title, "**</a>",
                "<br><br><details><summary>More info</summary>",
                "<a style='font-size:90%;'>",
                _.content,
                "<br><br>**Date and time:** ", _.formatted_date, " - ", _.time,
                "<br><br>**Author(s):** ", _.speakers,
                if_else(_.co_authors == "", "", paste_fn(";", _.co_authors)),
                "<br><br>**Keyword(s):** ", _.keywords,
                "</a>",
                "</details>"
            ),
            paste0_fn(
                "<a style='color:#2165b6;'>**", _.title, "**</a>",
                "<br><br><details><summary>More info</summary>",
                "<a style='font-size:90%;'>",
                _.content,
                "<br><br>**Date and time:** ", _.formatted_date, " - ", _.time,
                "<br><br>**Author(s):** ", _.speakers,
                if_else(_.co_authors == "", "", paste_fn(";", _.co_authors)),
                "<br><br>**Keyword(s):** ", _.keywords,
                "<br><br>**Video recording available after conference:** ", _.video_recording,
                "</a>",
                "</details>"
            )
        ),

        speakers = _.speakers.str.replace(", ", "<br>")
    )
    >> relocate(_.info, _after = _.room)
    >> select(-_.id, -_.submitter_email, -_.title, -_.content, -_.video_recording, -_.co_authors, -_.formatted_date, -_.keywords)
)

