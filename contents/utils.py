holidays_dates  = [
    "0101",
    "1704",
    "1804",
    "0105",
    "0805",
    "2605",
    "0606",
    "1407",
    "1508",
    "0111",
    "1111",
    "2512"
]

covid_phases = [
    {
        "type": "span",
        'min': "2020-02-15",
        'max': "2020-03-17",
        'color': "blue",
        'label': "Premières restrictions",
    },
    {
        "type": "span",
        'min': "2020-03-17",
        'max': "2020-05-11",
        'color': "red",
        'label': "Confinement total 1",
    },
    {
        "type": "span",
        'min': "2020-10-30",
        'max': "2020-12-15",
        'color': "red",
        'label': "Confinement total 2",
    },
    {
        "type": "span",
        'min': "2021-01-16",
        'max': "2021-04-03",
        'color': "yellow",
        'label': "Couvre feu 1",
    },
    {
        "type": "span",
        'min': "2021-04-03",
        'max': "2021-05-19",
        'color': "red",
        'label': "Confinement total 3",
    },
    {
        "type": "line",
        'min': "2021-08-09",
        'max': "2021-08-09",
        'color': "yellow",
        'label': "Pass sanitaire",
    }
]

energies = ["Fioul","Charbon","Gaz","Nucléaire","Eolien","Solaire","Hydraulique","Bioénergies"]
energies_2 = ["Conso_gaz_totale_MW","Conso_elec_totale_MW","Conso_brute_totale_MW"]

fioul_feats = ['Fioul', 'Fioul - TAC', 'Fioul - Cogén.', 'Fioul - Autres']
gaz_feats = ['Gaz', 'Gaz - TAC', 'Gaz - Cogén.', 'Gaz - CCG', 'Gaz - Autres']
hydrauliques_feats = ['Hydraulique', 'Hydraulique - Fil de l?eau + éclusée', 'Hydraulique - Lacs', 'Hydraulique - STEP turbinage']
bioenergies_feats = ['Bioénergies - Déchets', 'Bioénergies - Biomasse','Bioénergies - Biogaz', 'Bioénergies']

compare_with_year = ["Année -1", "Année +1"]