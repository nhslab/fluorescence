# %%
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os
#%%
# если поставить auto True, пределы представления графика будут считаться автоматически
# иначе необходимо выставить их вручную
auto = False
em_start = 280
em_finish = 600
ex_start = 250
ex_finish = 450

# %%
# функция преобразования данные в нужный формат. Тут немного костылей
def read_data(name):
    df = pd.read_csv(name)

    df.to_csv('temp', sep = ";", index = False)

    with open('temp', 'r') as file :
        filedata = file.read()
    filedata = filedata.replace(',', '.')
    with open('temp', 'w') as file:
        file.write(filedata)

    df = pd.read_csv('temp', sep=';')
    df = df.drop([0], axis=0)
    df = df.set_index('Wavelength')
    if auto == False:
        df = df.loc[f'{em_start}':f'{em_finish}', f'{ex_start}':f'{ex_finish}' ]
    for i in df.columns:
        df[i] = df[i].astype('float64')
    
    os.remove('temp')
    return df
#%%
# функции для корректного отображения осей графика
def format_y_axes(value, tick_number):
    return int(em[0]) + (int(em[1])-int(em[0]))*value
    
def format_x_axes(value, tick_number):
    return int(ex[0]) + (int(ex[1])-int(ex[0]))*value

# %%
#  собственно, функция построения графика
def plot_date(df, name):
    
    fig = plt.figure(figsize=(8,6), dpi = 100)
    ax = plt.axes()
    max_ampl = 3 #max_ampl = max(df['250'].tolist()[50:200])    normalize by 250 nm ex max.

    plt.imshow(df.T, aspect='auto', origin='lower', cmap=plt.cm.get_cmap('viridis',20),
            interpolation='gaussian', vmax = max_ampl, vmin=0)

    ax.grid(visible = False, color = 'black')
    plt.colorbar()

    ax.xaxis.set_major_formatter(plt.FuncFormatter(format_x_axes))
    ax.xaxis.set_major_locator(plt.MultipleLocator(50))
    ax.yaxis.set_major_formatter(plt.FuncFormatter(format_y_axes))
    ax.yaxis.set_major_locator(plt.MultipleLocator(10))

    ax.set_title(name[:-8])
    ax.set_xlabel('Emission, nm')
    ax.set_ylabel('Excitation, nm')
    plt.savefig(f'out/{name[:-4]}.png')
# %%
if 'out' not in os.listdir():
    os.mkdir('out')
for file in os.listdir():
    
    if file[-3:] == 'csv':
        df = read_data(file)
        ex = df.index.tolist()
        em = df.columns.tolist()
        plot_date(df, file)
# %%
