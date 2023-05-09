
def excel_sheet(numberplate):
    import pandas as pd
    sheet_id = '1MkVBQYNqql8Ui7YScYl3IXQeRlHzaX1f9Z5CERndSME'

    df = pd.read_csv(f'https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv')

    if numberplate in df['Number Plate'].values:
        row = df[df['Number Plate'] == numberplate]
        bus_name = row.iloc[0, 1]
        place = row.iloc[0, 2]
        print(bus_name)
        print(place)
        return bus_name,place
    else:
        print(numberplate)
        print("The Number Plate is not registered ")
        return 0
x=excel_sheet('KLO6')
print(x[0])
