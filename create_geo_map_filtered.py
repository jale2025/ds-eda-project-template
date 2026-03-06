
import pandas as pd
import plotly.express as px

def create_filtered_geo_map(file_path: str, output_file: str = 'house_geo_map_filtered.html'):
    '''
    Generates an interactive geographic scatter plot of houses from a CSV file,
    filtered for zipcodes greater than or equal to 98100.

    Args:
        file_path (str): The path to the input CSV file.
                         The file must contain 'lat', 'long', and 'zipcode' columns.
        output_file (str): The name of the output HTML file for the map.
    '''
    try:
        # Load the dataset
        df = pd.read_csv(file_path)

        # Drop rows with missing lat/long data if any
        df.dropna(subset=['lat', 'long'], inplace=True)

        # Filter for zipcodes >= 98100
        df_filtered = df[df['zipcode'] >= 98100].copy()

        # Convert zipcode to category for better coloring on the filtered dataframe
        df_filtered['zipcode'] = df_filtered['zipcode'].astype('category')

        print(f"Loaded {len(df)} records from {file_path}")
        print(f"Filtered down to {len(df_filtered)} records for zipcodes >= 98100")
        print("Generating filtered geographic map...")

        # Create an interactive scatter plot on a map using plotly with the filtered data
        fig = px.scatter_mapbox(df_filtered,
                                lat="lat",
                                lon="long",
                                color="zipcode",
                                hover_name="house_id",
                                hover_data={"sell_price": True, "bedrooms": True, "bathrooms": True, "zipcode": True},
                                zoom=8,
                                height=800,
                                title="Geographic Distribution of Houses for Zipcodes >= 98100")

        fig.update_layout(mapbox_style="open-street-map")
        fig.update_layout(margin={"r":0,"t":50,"l":0,"b":10})

        # Save the plot to an HTML file
        fig.write_html(output_file)
        print(f"Successfully generated filtered map and saved it to {output_file}")
        print("You can open this file in your web browser to view the interactive map.")

    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == '__main__':
    csv_file = 'house_data.csv'
    create_filtered_geo_map(csv_file)
