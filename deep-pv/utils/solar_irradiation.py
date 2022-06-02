import requests
"""
Get average monthly irradiation for a given location
Example input: {'lat': 45, 'long': 8}
More parameters are possible, check:
https://joint-research-centre.ec.europa.eu/pvgis-photovoltaic-geographical-information-system/getting-started-pvgis/api-non-interactive-service_en
TODO: Check what the returned value actually represents.
"""


BASE_URI = 'https://re.jrc.ec.europa.eu/'

def get_data(query, database = '/MRcalc'):
# response = requests.get(BASE_URI + '/api' + database + query)
    response = requests.get(BASE_URI + '/api' + database, params=query)
    return response.json()

def get_monthly_average_irr(query: dict):

    query['outputformat'] = 'json'
    query['horirrad'] = 1

    data = get_data(query)
    monthly = data['outputs']['monthly']
    avg_month_prod = sum([month['H(h)_m'] for month in monthly])/len(monthly)
    return avg_month_prod

if __name__ == '__main__':

    query = {
        'lat' : 45,
        'lon' : 8,
    }

    output = get_monthly_average_irr(query)
    print(output)
