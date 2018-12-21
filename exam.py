import re
import pprint
import plotly
import plotly.graph_objs as go
from plotly import tools




def plot():
    fig = tools.make_subplots(rows=2, cols=2)

    keys_1 = []
    values_1 = []
    for date in dataset[airport]['Domestic']['Arrival']:
        date_total = 0
        for i in dataset[airport]['Domestic']['Arrival'][date]:
            date_total += dataset[airport]['Domestic']['Arrival'][date][i]
        keys_1.append(date)
        values_1.append(date_total)
    chart_1 = go.Scatter(
        x=keys_1,
        y=values_1
    )
    fig.append_trace(chart_1, 1, 1)

    keys_2 = []
    values_2 = []
    for date in dataset[airport]['Domestic']['Departure']:
        date_total = 0
        for i in dataset[airport]['Domestic']['Departure'][date]:
            date_total += dataset[airport]['Domestic']['Departure'][date][i]
        keys_2.append(date)
        values_2.append(date_total)
    chart_2 = go.Scatter(
        x=keys_2,
        y=values_2
    )
    fig.append_trace(chart_2, 1, 2)


    new_dict = {}
    for date in dataset[airport]['Domestic']['Arrival']:
        for i in dataset[airport]['Domestic']['Arrival'][date]:
            if i not in new_dict:
                new_dict[i] = dataset[airport]['Domestic']['Arrival'][date][i]
            else:
                new_dict[i] += dataset[airport]['Domestic']['Arrival'][date][i]
    keys_3 = list(new_dict.keys())
    values_3 = list(new_dict.values())
    chart_3 = go.Bar(
        x=keys_3,
        y=values_3
    )
    fig.append_trace(chart_3, 2, 1)

    plotly.offline.plot(fig, filename='plotly.html')


def eliminate(line):
    result = re.split(r',', line, maxsplit=1)
    return result[1]


def get_date(line):
    mod_line = eliminate(line)
    result = re.split(r',', mod_line, maxsplit=1)
    date = re.findall(r'^\d{2,4}\-\d{1,2}\-\d{1,2}', result[0])
    return date[0], result[1]


def get_terminal(line):
    date, mod_line = get_date(line)
    result = re.split(r',', mod_line, maxsplit=1)
    if result[0] == 'Tom Bradley International Terminal' or 'Imperial Terminal' or 'Misc. Terminal':
        return result[0], result[1]
    terminal = re.findall(r'^Terminal \d$', result[0])
    return terminal[0], result[1]


def get_arr_dep(line):
    terminal, mod_line = get_terminal(line)
    result = re.split(r',', mod_line, maxsplit=1)
    arr_dep = re.findall(r'^Departure$', result[0])
    if len(arr_dep) == 0:
        arr_dep = re.findall(r'^Arrival$', result[0])
    return arr_dep[0], result[1]


def get_dom_int(line):
    arr_dep, mod_line = get_arr_dep(line)
    result = re.split(r',', mod_line, maxsplit=1)
    dom_int = re.findall(r'^Domestic$', result[0])
    if len(dom_int) == 0:
        dom_int = re.findall(r'^International$', result[0])
    return dom_int[0], result[1]


def get_num_pass(line):
    dom_int, mod_line = get_dom_int(line)
    result = re.split(r',', mod_line, maxsplit=1)
    pass_num = re.findall(r'\d{1,}', result[0])
    pass_num = float(pass_num[0])
    return pass_num

dataset = {
}
try:
    with open('airport.csv', 'r') as f:
        f.readline()
        line_number = 1
        airport = 'Los Angeles international airport'
        for line in f:
            #print(line_number)
            #print(line.strip())
            date = get_date(line)[0]
            terminal = get_terminal(line)[0]
            arr_dep = get_arr_dep(line)[0]
            dom_int = get_dom_int(line)[0]
            pass_num = get_num_pass(line)

            if airport not in dataset:
                dataset[airport] = {}
            if dom_int not in dataset[airport]:
                dataset[airport][dom_int] = dict()
            if arr_dep not in dataset[airport][dom_int]:
                dataset[airport][dom_int][arr_dep] = dict()
            if date not in dataset[airport][dom_int][arr_dep]:
                dataset[airport][dom_int][arr_dep][date] = dict()
            dataset[airport][dom_int][arr_dep][date][terminal] = pass_num
            line_number += 1
    pprint.pprint(dataset)
    plot()







except IOError as e:
    print("I/O error({0}): {1}".format(e.errno, e.strerror))

except ValueError as ve:
    print("Value error {0} in line {1}".format(ve, line_number))
