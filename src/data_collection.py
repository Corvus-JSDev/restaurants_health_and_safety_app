import censusdis.data as ced
from censusdis.datasets import ACS5
import censusdis.states as states

# Download all counties with their corresponding state
counties_df = ced.download(
    dataset=ACS5,
    vintage=2022,
    download_variables=["NAME"],
    state=states.ALL_STATES,
    county="*"
)

counties_df[['county', 'state']] = counties_df['NAME'].str.split(', ', expand=True)

counties_df.drop(columns=['NAME', 'STATE', 'COUNTY'], inplace=True)

counties_df.to_csv('counties_with_states.csv', index=False)

print("data saved")
