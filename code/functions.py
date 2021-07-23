# visualization
#from IPython.display import IFrame
#import plotly
import plotly.figure_factory as ff
#import plotly.express as px

# format damage_property, damge_crops, columns containing monetary amounts
def format_money(string):
    try: 
        if len(string) > 1:
            if string[-1] == 'K':
                return float(string[:-1]) * 1000
            elif string[-1] =='M':
                return float(string[:-1]) * 1000000
            elif string[-1] =='B':
                return float(string[:-1]) * 1000000000
            else:
                return string
        else:
            return 0
    except TypeError:
        return string

################################

# returns list of (zone, county) tuples for a state
def to_county_mapper(df, state):
    
    state_df = df[df['state'] == state]
    state_counties = state_df[state_df['cz_type'] == 'C']['cz_name'].unique().tolist()
    state_zones = state_df[state_df['cz_type'] == 'Z']['cz_name'].unique().tolist()
    
    to_county_map = []

    # make matches based on string overlap
    for zone in state_zones:
        for county in state_counties:
            if county in zone:
                to_county_map.append((zone, county))
                continue;
    return to_county_map

################################

def map_events(df, year, measure, state= 'usa'):
    
    state_grouped = df.groupby(['state', 'fips', 'year'])[measure].sum().reset_index()
    if state != 'usa':
        state_df = state_grouped[(state_grouped['state'] == state) & (state_grouped['year'] == year)]
    else: 
        state_df = state_grouped[(state_grouped['year'] == year)]
    values = state_df[measure].tolist()
    fips = state_df['fips'].tolist()

    colorscale = [
        'rgb(193, 193, 193)',
        'rgb(239,239,239)',
        'rgb(195, 196, 222)',
        'rgb(144,148,194)',
        'rgb(101,104,168)',
        'rgb(65, 53, 132)'
    ]

    fig = ff.create_choropleth(
        fips=fips, values=values, scope=[state],
        binning_endpoints=[1000, 10000, 100000, 1000000], colorscale=colorscale,
        county_outline={'color': 'rgb(255,255,255)', 'width': 0.5}, round_legend_values=True,
        legend_title=f'{measure.title()} by County', title=f'{state.upper()}, {year}'
    )
    fig.layout.template = None
    fig.show()

#https://stackoverflow.com/questions/39106223/list-of-all-the-geographic-scope-in-plotly

################################


events_dict = {'Drought': 'Drought', 
               'Northern Lights': 'Other',
               'OTHER': 'Other',
               'Astronomical Low Tide': 'Other',
               'Tsunami': 'Other',
               'Landslide': 'Landslide',
               'Heat': 'Excessive Heat',
               'Excessive Heat': 'Excessive Heat',
               'Tropical Storm': 'Tropical Storm', 
               'Tropical Depression': 'Hurricane',
               'Hurricane':'Hurricane',
               'Sneakerwave': 'High Surf/Rip Current',
               'Lightning': 'Lightning',
               'Tornado': 'Tornado',
               'High Surf': 'High Surf/Rip Current', 
               'Hurricane': 'Hurricane', 
               'Dense Fog': 'Dense Fog', 
               'Funnel Cloud': 'Other',
               'Wildfire': 'Wildfire',
               'Dense Smoke': 'Wildfire',
               'Waterspout': 'Other', 
               'Storm Surge/Tide': 'Storm Surge', 
               'Rip Current': 'High Surf/Rip Current',
               'Seiche': 'Other', 
               'Dust Storm': 'Dust Storm', 
               'Dust Devil': 'Tornado',
               'Volcanic Ash': 'Other', 
               'Debris Flow': 'Dust Storm',
               'Ice Storm': 'Winter Storm', 
               'Hail': 'Winter Storm',
               'Winter Weather': 'Extreme Cold',
               'Heavy Snow': 'Winter Storm', 
               'Winter Storm': 'Winter Storm', 
               'Cold/Wind Chill': 'Extreme Cold',
               'Lake-Effect Snow': 'Winter Storm',
               'Sleet': 'Winter Storm', 
               'Blizzard': 'Winter Storm', 
               'Avalanche': 'Winter Storm', 
               'Frost/Freeze': 'Extreme Cold',  
               'Freezing Fog': 'Extreme Cold',  
               'Extreme Cold/Wind Chill': 'Extreme Cold',  
               'High Snow': 'Winter Storm', 
               'Lakeshore Flood':'Flooding', 
               'Coastal Flood':'Flooding', 
               'Heavy Rain':'Flooding', 
               'Flash Flood':'Flooding',
               'Flood':'Flooding',
               'Thunderstorm Wind':'Extreme Wind', 
               'High Wind':'Extreme Wind',
               'Strong Wind':'Extreme Wind', 
               'Marine High Wind':'Extreme Wind'}