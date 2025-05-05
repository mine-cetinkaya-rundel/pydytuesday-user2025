# load packages ---------------------------------------------------------------

import pydytuesday
import pandas
import great_tables

# load data -------------------------------------------------------------------

pydytuesday.get_date('2025-04-29')
user2025 = pandas.read_csv('https://raw.githubusercontent.com/rfordatascience/tidytuesday/main/data/2025/2025-04-29/user2025.csv')

# make table ------------------------------------------------------------------

