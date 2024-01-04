from flask import Flask, render_template, request, url_for
from forms import Main_Form
from Main_data import columns_list
import os
from operations import master
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import seaborn as sns
from plot import master_plot


app = Flask(__name__)

app.config['SECRET_KEY'] = os.urandom(24)


list_of_tables = Result_list= []


@app.route("/", methods = ['GET', 'POST'])
@app.route("/home", methods = ['GET', 'POST'])
def home():
    global Result_list
    global list_of_tables

    main_form = Main_Form()
    if main_form.validate_on_submit():
        form_data = request.form.to_dict()
        list_of_tables = table_list(form_data)
        key = form_data["field_name"]
        for i in columns_list:
            if (i[0] == key):
             field_name = i[1]
        data_type = None
        op = mobile = False
        num = enum = thresh = None
        data = name = False
        if main_form.data_type.data == "0":
            data_type = float
            if main_form.op.data == "1":
                op = True
                if main_form.Enum.data == "Auto":
                    enum = None
                else:
                    try:
                        enum = float(form_data['Enum'])
                    except:
                        enum = form_data['Enum']

                if main_form.num.data == "Auto":
                    num = None
                else:
                    try:
                        num = float(form_data['num'])
                    except:
                        num = form_data['num']
                
                if main_form.thresh.data == "9 (default)":
                    thresh = 9
                else:
                    try:
                        thresh = float(form_data['thresh'])
                    except:
                        thresh = form_data['thresh']
            else:
                if main_form.mobile.data == "1":
                    mobile = True
                else:
                    mobile = False
        else:
            data_type = str
            if main_form.data.data == "2":
                name = True
            elif main_form.data.data == "1":
                data = True
        
        Result_list = master(file_name=field_name, mobile=mobile, op=op, name=name, data_type=data_type, num=num, enum=enum, thresh=thresh, data=data)
                


        return render_template('home.html', main_form = main_form, list_of_tables = list_of_tables)
    return render_template('home.html', main_form = main_form)

def table_list(form_data):
    key = form_data["field_name"]
    for i in columns_list:
        if (i[0] == key):
            field_name = i[1]
    list_of_tables = [
        ('home', "HOME"),
        ('final_stats' , 'Final Stats'),
        ('field_name' , f'{field_name}'),
        ('field_name_unique' , f'{field_name}_unique'),
        ("field_name_unique_non_nan" , f'{field_name}_unique_non-nan'),
        ('field_name_unique_nan' ,  f'{field_name}_unique_nan'),
        ('field_name_error' , f'{field_name}_error')
    ]

    if form_data['data_type'] == '0':
        if form_data['op'] == '0':
            pass
        elif form_data['op'] == '1':
            list_of_tables.extend([('field_name_unique_non_nan_filtered', f'{field_name}_unique_non-nan_filtered'), ('field_name_unique_non_nan_unfiltered', f'{field_name}_unique_non-nan_unfiltered'), ('plots', 'Plots')])
        else:
            return
    elif form_data['data_type'] == '1':
        if form_data['data'] == '2':
            pass
        elif form_data['data'] == '1':
            list_of_tables.extend([('field_name_upcomingdate', f'{field_name}_Upcoming-Date')])
        elif form_data['data'] == '0':
            pass
        else:
            return
    else:
        return
    return list_of_tables
    


@app.route("/final_stats")
def final_stats():
    Res_df = Result_list[2]
    Res_df['Values'] = Res_df['Values'].astype(int)
    Res_df = Res_df.to_html()
    return render_template('table.html', Res_df = Res_df, list_of_tables = list_of_tables)

@app.route("/field_name")
def field_name():
    Res_df = Result_list[-1].to_html()
    return render_template('table.html', Res_df = Res_df, list_of_tables = list_of_tables)

@app.route("/field_name_unique")
def field_name_unique():
    Res_df = Result_list[-2].to_html()
    return render_template('table.html', Res_df = Res_df, list_of_tables = list_of_tables)

@app.route("/field_name_unique_non-nan")
def field_name_unique_non_nan():
    Res_df = Result_list[1].to_html()
    return render_template('table.html', Res_df = Res_df, list_of_tables = list_of_tables)

@app.route("/field_name_unique_non-nan_filtered")
def field_name_unique_non_nan_filtered():
    Res_df = Result_list[3].to_html()
    return render_template('table.html', Res_df = Res_df, list_of_tables = list_of_tables)

@app.route("/field_name_unique_non-nan_unfiltered")
def field_name_unique_non_nan_unfiltered():
    Res_df = Result_list[4].to_html()
    return render_template('table.html', Res_df = Res_df, list_of_tables = list_of_tables)

@app.route("/field_name_upcomingdate")
def field_name_upcomingdate():
    Res_df = Result_list[3].to_html()
    return render_template('table.html', Res_df = Res_df, list_of_tables = list_of_tables)

@app.route("/plots")
def plots():

    mf_org = Result_list[5]
    mf = Result_list[6]
    emf = Result_list[7]
    num  = Result_list[8]
    enum = Result_list[9]
    file_name = Result_list[10]
    Plot_list = master_plot(file_name= file_name, mf_org= mf_org, mf= mf, emf= emf, num=num, enum = enum)
    return render_template('plot.html', list_of_tables = list_of_tables, Plot_list = Plot_list)

@app.route("/field_name_unique_nan")
def field_name_unique_nan():
    Res_df = Result_list[0].to_html()
    return render_template('table.html', Res_df = Res_df, list_of_tables = list_of_tables)

@app.route("/field_name_error")
def field_name_error():
    Res_df = Result_list[-3].to_html()
    return render_template('table.html', Res_df = Res_df, list_of_tables = list_of_tables)




if __name__ == "__main__":
    app.run(debug=True)