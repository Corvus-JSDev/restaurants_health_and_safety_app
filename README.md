![preview image](https://github.com/Corvus-JSDev/restaurants_health_and_safety_app/blob/main/data/imgs/project-showcase.png)

![demo video](https://github.com/Corvus-JSDev/restaurants_health_and_safety_app/blob/main/data/imgs/dinesafe_demo_video.gif)

# Project Overview

This web application is designed to provide users with easy access to comprehensive, country-wide restaurant health inspection data, all in one centralized platform. By utilizing APIs to aggregate public health inspection records from various government databases, this app enables consumers to quickly assess the cleanliness and safety standards of restaurants they’re considering.

The project leverages a combination of Python, relevant libraries, and API integration to pull, process, and display up-to-date health inspection data from government databases. It demonstrates my expertise in data collection, API integration, data processing, and web development. By transforming raw data into actionable insights and presenting it through an intuitive user interface, this app showcases my ability to solve real-world problems with data-driven solutions.


*As a proof of concept, this project is still in development and only supports the following US states: New York, Pennsylvania, and Delaware. This project can benefit greatly from the help of the open-source community and other collaborators to reach its full potential.*



# Technologies Utilized

- Python
- Pandas
- SQLite3
- Streamlit
- CensusData
- Sodapy
- Censusdis
- Geocoder



# Data Gathering, Sourcing, Cleaning, and Visualization

The initial step in this process involved obtaining a comprehensive list of all U.S. states and their respective counties, enabling users to easily select the desired data slice for analysis. To accomplish this, I utilized the *censusdis* python package to download a CSV file containing the counties and their corresponding states. I then utilized *SQLite3* to convert that CSV into a structured SQL database, enhancing data organization and accessibility. As an added feature, I integrated the *Geocoder* package to automatically detect the user's state, further enhancing the UI and streamlining the data selection process.

Once the user selects a specific state and county, the next step is to gather and format the relevant data. To achieve this, I leveraged the *Sodapy* package, which facilitates easy access to public government databases. By entering the selected state’s URL (e.g., health.data.ny.gov) and the corresponding database ID (e.g., cnih-y5dw), I am able to retrieve the necessary data efficiently.

After the data is collected, I load it into a *Pandas* DataFrame for further processing. If a restaurant has undergone multiple inspections within a year, I aggregate these records to calculate the total number of critical, minor, and repeat violations for each restaurant over time. This step ensures that the data reflects the cumulative inspection history, providing a clearer picture of the restaurant's safety record.

For states that provide detailed data, such as New York which gives specific counts for critical, minor, and repeat violations, I implement a custom, weighted evaluation algorithm. This algorithm calculates a risk score for each restaurant, offering a concise and easily interpretable measure of its cleanliness and safety. The risk score provides users with a clear indication of how well the restaurant meets health standards.

Once all data has been compiled and processed, I focus on styling the DataFrame to enhance user experience. I use Pandas built-in `style.map()` method, applying a custom function that visually highlights risk areas by coloring them red for high risk, yellow for moderate risk, and green for low risk. Additionally, I employ another styling function to alternate row colors, making the table more readable and user-friendly by breaking up the solid blocks of data.
