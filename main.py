import streamlit as st
from src import helpers

print("----- Prerequisite Checks -----")
helpers.ensure_county_data_is_installed()
helpers.ensure_sql_database_exists()
