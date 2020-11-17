from django.conf import settings

from bs4 import BeautifulSoup
import pandas as pd
import pendulum
import requests


def get_dof_rate():
    r = requests.get('https://www.banxico.org.mx/tipcamb/tipCamMIAction.do')
    soup = BeautifulSoup(r.text, 'html.parser')
    df = pd.read_html(str(soup.select_one('.renglonTituloColumnas').parent), na_values='N/E')[0]
    df.columns = [row[0].strip() for row in df.iloc[1].str.rsplit(' ', 1)]
    df.drop([0, 1], inplace=True)

    dof_data = df[df['Publicación DOF'].notna()].iloc[0]
    # Assuming that the date is displayed in Mexico's timezone, otherwise just remove the tz parameter
    dof_date = pendulum.from_format(dof_data['Fecha'], 'DD/MM/YYYY', tz='America/Mexico_City')

    return {
        'last_updated': dof_date.in_timezone('UTC'),
        'value': float(dof_data['Publicación DOF']),
    }


def get_banxico_rate():
    date_now = pendulum.now(tz='America/Mexico_City')

    r = requests.get(
        f'https://www.banxico.org.mx/SieAPIRest/service/v1/series/SF43718/datos/{date_now.subtract(days=7).to_date_string()}/{date_now.to_date_string()}',
        headers={'Bmx-Token': settings.BANXICO_TOKEN},
    )

    banxico_data = r.json()['bmx']['series'][0]['datos'][-1]
    # Assuming that the date is displayed in Mexico's timezone, otherwise just remove the tz parameter
    banxico_date = pendulum.from_format(banxico_data['fecha'], 'DD/MM/YYYY', tz='America/Mexico_City')

    return {
        'last_updated': banxico_date.in_timezone('UTC'),
        'value': float(banxico_data['dato']),
    }


def get_fixer_rate():
    params = {'access_key': settings.FIXER_TOKEN, 'symbols': 'MXN'}

    if settings.FIXER_DEFAULT_CURRENCY:
        params['base'] = settings.FIXER_DEFAULT_CURRENCY

    fixer_r = requests.get(f'http://data.fixer.io/api/latest', params=params)
    fixer_data = fixer_r.json()
    fixer_date = pendulum.from_format(fixer_data['date'], 'YYYY-MM-DD')

    return {
        'last_updated': fixer_date,
        'value': float(fixer_data['rates']['MXN']),
    }
