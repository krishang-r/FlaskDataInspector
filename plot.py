import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO
import base64


def create_custom_displot(data, title):
    sns.set(style="whitegrid")
    sns.histplot(data, kde=True)
    plt.title(title)

    image_stream = BytesIO()
    plt.savefig(image_stream, format='png')
    image_stream.seek(0)

    encoded_image = base64.b64encode(image_stream.read()).decode('utf-8')
    return encoded_image

def create_custom_histplot(data, title, x_label, y_label):

    sns.set(style="whitegrid")
    sns.displot(data = data, bins=10)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)

    image_stream = BytesIO()
    plt.savefig(image_stream, format='png')
    image_stream.seek(0)

    encoded_image = base64.b64encode(image_stream.read()).decode('utf-8')
    return encoded_image

def create_custom_histplot_color(mf, title, x_label, y_label):
    sns.set(style="whitegrid")
    sns.histplot(x=mf, y=range(len(mf)), bins=10, cmap='Blues', edgecolor = 'Black', cbar=True)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)

    image_stream = BytesIO()
    plt.savefig(image_stream, format='png')
    image_stream.seek(0)

    encoded_image = base64.b64encode(image_stream.read()).decode('utf-8')
    return encoded_image

def create_box_plot(data, x_label, y_label, title):

    sns.set(style="whitegrid")
    sns.boxplot(data)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)

    image_stream = BytesIO()
    plt.savefig(image_stream, format='png')
    image_stream.seek(0)

    encoded_image = base64.b64encode(image_stream.read()).decode('utf-8')
    return encoded_image

def master_plot(file_name, mf_org, mf, emf, num, enum):
    
    Final_Plots = []
            
    title = file_name + "_distplot"
    Plot_1 = create_custom_displot(mf_org, title)
    Final_Plots.append(Plot_1)

    title = file_name + "_distplot"
    x_label = file_name
    y_label = 'No of customers'
    Plot_2 = create_custom_histplot(mf_org, title, x_label, y_label)
    Final_Plots.append(Plot_2)

    title = file_name + "_boxplot"
    x_label = file_name
    y_label = 'No of customers'
    Plot_3 = create_box_plot(mf_org, x_label, y_label, title)
    Final_Plots.append(Plot_3)

    title = file_name
    x_label = file_name
    y_label = 'No of customers'
    Plot_4 = create_custom_histplot_color(mf_org, title, x_label, y_label)
    Final_Plots.append(Plot_4)

    if (len(mf)!=0):
        title = f'{enum} <= {file_name} < {num}'
        x_label = file_name
        y_label = 'No of customers'
        Plot_5 = create_custom_histplot_color(mf, title, x_label, y_label)
        Final_Plots.append(Plot_5)

    title = f'{enum} <= {file_name} < {num}' + "_boxplot"
    x_label = file_name
    y_label = 'No of customers'
    Plot_6 = create_box_plot(mf, x_label, y_label, title)
    Final_Plots.append(Plot_6)

    title = f"{enum} <= {file_name} < {num}_distplot"
    x_label = file_name
    y_label = 'No of customers'
    Plot_7 = create_custom_histplot(mf, title, x_label, y_label)
    Final_Plots.append(Plot_7)

    if (len(emf) != 0):
        ax = sns.histplot(x=emf, y=range(len(emf)), bins=10, cmap='Blues', edgecolor = 'Black', cbar=True)
        title = f'{file_name} < {enum} and {file_name} >= {num}'
        x_label = file_name
        y_label = 'No of customers'
        Plot_8 = create_custom_histplot_color(emf, title, x_label, y_label)
        Final_Plots.append(Plot_8)
    
    return Final_Plots