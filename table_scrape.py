import pandas as pd
from bs4 import BeautifulSoup
import requests


def qb_projections(url, amount, remove, teams_rm):

    source = requests.get(url).text

    soup = BeautifulSoup(source,'lxml')

    table = soup.find('table')
    rows = table.find_all('tr')
    rows = rows[2:]

    df = pd.DataFrame(columns = ['Name', 'Team', 'FPTS'])
    next = 0
    for i in range(amount):
        info = rows[i].find_all('td')
        team = info[0].text
        team = team[len(team)-4:len(team)].strip()
        name = info[0].a.text
        fpts = round(float(info[10].text),1)
        if remove and not team in teams_rm:
            df.loc[next] = [name, team, fpts]
            next+=1
        elif not remove:
            df.loc[next] = [name, team, fpts]
            next+=1

    return df

def rb_projections(url,amount, remove, teams_rm):

    source = requests.get(url).text

    soup = BeautifulSoup(source,'lxml')

    table = soup.find('table')
    rows = table.find_all('tr')
    rows = rows[2:]

    df = pd.DataFrame(columns = ['Name', 'Team', 'FPTS'])
    next = 0
    for i in range(amount):
        info = rows[i].find_all('td')
        team = info[0].text
        team = team[len(team)-4:len(team)].strip()
        name = info[0].a.text
        rec = float(info[4].text)
        fpts = round(float(info[8].text)+rec,1)
        if remove and not team in teams_rm:
            df.loc[next] = [name, team, fpts]
            next+=1
        elif not remove:
            df.loc[next] = [name, team, fpts]
            next+=1

    return df

def wr_projections(url,amount, remove, teams_rm):

    source = requests.get(url).text

    soup = BeautifulSoup(source,'lxml')

    table = soup.find('table')
    rows = table.find_all('tr')
    rows = rows[2:]

    df = pd.DataFrame(columns = ['Name', 'Team', 'FPTS'])
    next = 0
    for i in range(amount):
        info = rows[i].find_all('td')
        team = info[0].text
        team = team[len(team)-4:len(team)].strip()
        name = info[0].a.text
        rec = float(info[1].text)
        fpts = round(float(info[8].text)+rec,1)
        if remove and not team in teams_rm:
            df.loc[next] = [name, team, fpts]
            next+=1
        elif not remove:
            df.loc[next] = [name, team, fpts]
            next+=1

    return df

def te_projections(url, amount, remove, teams_rm):
    source = requests.get(url).text

    soup = BeautifulSoup(source,'lxml')

    table = soup.find('table')
    rows = table.find_all('tr')
    rows = rows[2:]

    df = pd.DataFrame(columns = ['Name', 'Team', 'FPTS'])
    next = 0
    for i in range(amount):
        info = rows[i].find_all('td')
        team = info[0].text
        team = team[len(team)-4:len(team)].strip()
        name = info[0].a.text
        rec = float(info[1].text)
        fpts = round(float(info[5].text)+rec,1)
        if remove and not team in teams_rm:
            df.loc[next] = [name, team, fpts]
            next+=1
        elif not remove:
            df.loc[next] = [name, team, fpts]
            next+=1

    return df

def d_projections(url, amount, remove, teams_rm):
    source = requests.get(url).text

    soup = BeautifulSoup(source,'lxml')

    table = soup.find('table')
    rows = table.find_all('tr')
    rows = rows[1:]

    df = pd.DataFrame(columns = ['Name', 'Team', 'FPTS'])
    next = 0
    for i in range(amount):
        info = rows[i].find_all('td')
        team = info[0].text
        team = team[len(team)-4:len(team)].strip()
        name = info[0].a.text
        fpts = round(float(info[9].text),1)
        if remove and not team in teams_rm:
            df.loc[next] = [name, team, fpts]
            next+=1
        elif not remove:
            df.loc[next] = [name, team, fpts]
            next+=1

    return df
