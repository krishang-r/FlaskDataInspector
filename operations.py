# Imports

# In[ ]:


import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from datetime import date
import re
from Main_data import df as mdf


# Static Variable

# In[ ]:


id = "Name"
br_list = []

# Functions

# Break List for operation on nested lists

# In[2]:


def break_list(y, x=None):
    
    global br_list

    if x is None:
        br_list = []

    if isinstance(y, list):
        for i in y:
            try:
                j = eval(i)
                if (isinstance(j, tuple)):
                    j = i.replace(",","")
                elif isinstance(j, list):
                    break_list(j, br_list)
                else:
                    if isinstance(j, (int, float)):
                        if ("/" in i) or ("-" in i):
                            j = i
                        else:
                            j = float(j)
                        br_list.append(j)
            except:
                br_list.append(i)


# Function to check validitiy of date

# In[ ]:


def is_date_less_than_today(input_date):
    # Convert input_date to a date object
    input_date_object = date(*map(int, input_date.split('-')))
    
    # Get today's date
    today = date.today()

    # Compare the dates
    return input_date_object < today


# Function to check validity of name

# In[ ]:


def is_valid_name(name):
    if name != None:
        # Define a regular expression pattern for a valid name
        pattern = re.compile(r'^[A-Za-z\s.]+$')

        # Use the pattern to match the input name
        match = pattern.match(name)

        # Check if there is a match and the entire string is covered
        return bool(match and match.group(0) == name)


# function to create dataframe for mobile data

# In[ ]:


def mobile_df(x, y, c):
    z = pd.DataFrame(columns=c)
    a = y[id].values
    b = x[id].values
    for i in b:
        if i in a:
            row = {
                c[0] : ((y.loc[y[id]==i])[c[0]].values)[0],
                c[1] : ((y.loc[y[id]==i])[c[1]].values)[0]
            }
            z.loc[len(z)] = row
    return z




# Creating a final_df dataframe which has unique row values

# In[ ]:


def making_final_df(col, req_df, file_name):
    global br_list

    final_df = pd.DataFrame(columns = col)
    for x in req_df.iterrows():
        e = x[1][1]
        row = {
            id : x[1][0],
            file_name : e
        }
        if (isinstance(e, (int, float))):
                row[file_name] = float(e)
                final_df.loc[len(final_df)] = row
        elif (type(e) in (str, list, tuple)):
            e = str(e)
            try:
                f = eval(e)
                if (isinstance(f, (float, int))):
                    if ("/" in e) or ("-" in e):
                        row[file_name] = e
                    else:
                        row[file_name] = float(f)
                    final_df.loc[len(final_df)] = row
                elif(isinstance(f, tuple)):
                    if(isinstance(f[0], (int, float))):
                        f = eval(e.replace(",", ""))
                        row[file_name] = float(f)
                        final_df.loc[len(final_df)] = row
                elif (isinstance(f, list)):
                    break_list(f, br_list)
                    result_list = br_list
                    br_list = []
                    for m in result_list:
                        row[file_name] = m
                        final_df.loc[len(final_df)] = row
                else:
                    row[file_name] = f
                    final_df.loc[len(final_df)] = row 
            except:
                final_df.loc[len(final_df)] = row
                continue
    return final_df



# Creating a result_df dataframe having data with valid datatype

# In[ ]:


def making_result_df(col, final_df, mobile, file_name, op, name, data_type):
    result_df = pd.DataFrame(columns = col)
    for x in final_df.iterrows():
        e = x[1][1]
        row = {
            id : x[1][0],
            file_name : e
        }
        if (mobile and (op == False)):
            if (isinstance(e,(int,float))):
                d = e
                if (isinstance(e, float)):
                    if (np.isnan(e)):
                        result_df.loc[len(result_df)] = row
                        continue
                    else:
                        d = str(int(e))
                        if (len(d)==10):
                            row[file_name] = d
                            result_df.loc[len(result_df)] = row
            elif (isinstance(e,str)):
                if (("-" in e) or (" " in e)):
                    d = e
                    d = d.replace("-","")
                    d = d.replace(" ", "")
                try:
                    d = str(int(d))
                    if (len(d)==10):
                        row[file_name] = d
                        result_df.loc[len(result_df)] = row
                except:
                    continue
        
        elif (name):
            if (isinstance(e, float)):
                if (isinstance(e, data_type) or np.isnan(e)):
                    result_df.loc[len(result_df)] = row
            else:
                if(is_valid_name(e)):
                    result_df.loc[len(result_df)] = row
                

        else:
            if (isinstance(e, float)):
                if (isinstance(e, data_type) or np.isnan(e)):
                    result_df.loc[len(result_df)] = row
            elif (isinstance(e, data_type)):
                result_df.loc[len(result_df)] = row

    return result_df


# Creating err_df dataframe having all the error values

# In[ ]:


def making_err_df(col, req_df, result_df, file_name):
    err_df = pd.DataFrame(columns=col)
    err = req_df[id].values
    ne = result_df[id].values
    for x in err:
        if x not in ne:
            y = (req_df.loc[req_df[id]==x]).values
            row = {
                id : y[0][0],
                file_name : y[0][1]
            }
            err_df.loc[len(err_df)] = row

    return err_df


# Function for creating plots

# In[ ]:


def create_custom_displot(data, title):
    sns.set(style="whitegrid")
    fig, ax = plt.subplots()
    sns.histplot(data, kde=True, ax=ax)
    ax.set_title(title)
    return fig, ax


# In[ ]:


def create_custom_histplot(data, title, x_label, y_label):
    sns.set(style="whitegrid")
    fig, ax = plt.subplots()
    sns.displot(data = data, bins=10, ax = ax)
    ax.set_title(title)
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    return fig, ax


# In[ ]:


def create_custom_histplot_color(mf, title, x_label, y_label):
    sns.set(style="whitegrid")
    fig, ax = plt.subplots()
    sns.histplot(x=mf, y=range(len(mf)), bins=10, cmap='Blues', edgecolor = 'Black', cbar=True, ax = ax)
    ax.set_title(title)
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    return fig, ax


# In[ ]:


def create_box_plot(data, x_label, y_label, title):
    sns.set(style="whitegrid")
    fig, ax = plt.subplots()
    sns.boxplot(x=x_label, y=y_label, data=data, ax=ax)
    ax.set_title(title)
    return fig, ax


# Final Operations

# In[ ]:


def fin_ops(data_type, mobile, col, result_df, file_name, op, num, enum, thresh, data, err_df):
    nan_df = pd.DataFrame(columns = col)
    non_nan_df = pd.DataFrame(columns = col)
    fin_list = ['Features', 'Values']
    fin_stat_df = pd.DataFrame(columns = fin_list)
    if (data_type == float):
        if (op == False):
            if(mobile):
                nan_df_1 = pd.DataFrame(columns = col)
                non_nan_df_1 = pd.DataFrame(columns = col)
                result_df_1 = pd.DataFrame(columns = col)
                for x in result_df.iterrows():
                    e = x[1][1]
                    row = {
                        id : x[1][0],
                        file_name : e
                    }
                    try:
                        if(isinstance(e,str)):
                            row[file_name] = float(e)
                    except:
                        continue
                    result_df_1.loc[len(result_df_1)] = row
                
                nan_df_1 = result_df_1.loc[np.isnan(result_df_1[file_name])]
                non_nan_df_1 = result_df_1.loc[~np.isnan(result_df_1[file_name])]

                nan_df = mobile_df(nan_df_1, result_df, col)
                non_nan_df = mobile_df(non_nan_df_1, result_df, col)



            else:
                if (len(result_df) != 0):
                    nan_df = result_df.loc[np.isnan(result_df[file_name])]
                    non_nan_df = result_df.loc[~np.isnan(result_df[file_name])]
                else:
                    nan_df = result_df
                    non_nan_df = result_df


            fin_stat_df.loc[len(fin_stat_df)] = {
                    fin_list[0] : 'NaN Count',
                    fin_list[1] : len(nan_df)
                }
            
            fin_stat_df.loc[len(fin_stat_df)] = {
                    fin_list[0] : 'Non-NaN Count',
                    fin_list[1] : len(non_nan_df)
                }
            
            return_list = [nan_df, non_nan_df, fin_stat_df]
            return return_list
            
        else:

            if (len(result_df) != 0):
                nan_df = result_df.loc[np.isnan(result_df[file_name])]
                non_nan_df = result_df.loc[~np.isnan(result_df[file_name])]
            else:
                nan_df = result_df
                non_nan_df = result_df
            
            mf = non_nan_df[file_name].values
            mf_org = sorted(mf)

            
            q1 = non_nan_df[file_name].quantile(0.25)
            q3 = non_nan_df[file_name].quantile(0.75)
            iqr = q3 - q1

            if (num == None):
                # num = non_nan_df[file_name].mean() + thresh *non_nan_df[file_name].std()
                num = q3 + (thresh * iqr)
                if (num > max(mf_org)):
                    num = max(mf_org)
            if (enum == None):
                # enum = non_nan_df[file_name].mean() - 1.5*non_nan_df[file_name].std()
                enum = q1 - (1.5 *iqr)
                if ((0.01*num )< enum):
                    enum = 0
                elif (enum<0):
                    enum = -1*enum
                else: enum = enum

                if (enum < min(mf_org)):
                    enum = min(mf_org)
            if (enum == -1):
                enum = mf_org[0]
            if (num == -1):
                num = mf_org[-1]
            
            nf_1 = non_nan_df.loc[non_nan_df[file_name] < num]



            mf = nf_1[file_name].values

            nf_1 = nf_1.loc[nf_1[file_name] >= enum]

            mf = nf_1[file_name].values


            nf_2 = non_nan_df.loc[non_nan_df[file_name] >= num]


            #count of values above upper bound
            ct = len(nf_2)

            emf = nf_2[file_name].values

            efilt = non_nan_df.loc[non_nan_df[file_name] < enum]


            #count of values below lower bound
            cte = len(efilt)

            nf_2 = pd.concat([efilt, nf_2], ignore_index= True)

            emf = nf_2[file_name].values

            fin_stat_df.loc[len(fin_stat_df)] = {
                    fin_list[0] : 'NaN Count',
                    fin_list[1] : len(nan_df)
                }
            
            fin_stat_df.loc[len(fin_stat_df)] = {
                    fin_list[0] : 'Non-NaN Count',
                    fin_list[1] : len(non_nan_df)
                }
            
            fin_stat_df.loc[len(fin_stat_df)] = {
                    fin_list[0] : 'Threshold',
                    fin_list[1] : thresh
                }
            
            fin_stat_df.loc[len(fin_stat_df)] = {
                    fin_list[0] : "Lower Bound Filtered Value",
                    fin_list[1] : enum
                }
            
            fin_stat_df.loc[len(fin_stat_df)] = {
                    fin_list[0] : "Upper Bound Filtered Value",
                    fin_list[1] : num
                }
            
            fin_stat_df.loc[len(fin_stat_df)] = {
                    fin_list[0] : "Mean of Filtered Value",
                    fin_list[1] : nf_1[file_name].mean()
                }
            
            fin_stat_df.loc[len(fin_stat_df)] = {
                    fin_list[0] : "Max of Filtered Value",
                    fin_list[1] : nf_1[file_name].max()
                }
            
            fin_stat_df.loc[len(fin_stat_df)] = {
                    fin_list[0] : "Min of Filtered Value",
                    fin_list[1] : nf_1[file_name].min()
                }
            
            fin_stat_df.loc[len(fin_stat_df)] = {
                    fin_list[0] : "Mean of Unfiltered Value",
                    fin_list[1] : nf_2[file_name].mean()
                }
            
            fin_stat_df.loc[len(fin_stat_df)] = {
                    fin_list[0] : "Max of Unfiltered Value",
                    fin_list[1] : nf_2[file_name].max()
                }
            
            fin_stat_df.loc[len(fin_stat_df)] = {
                    fin_list[0] : "Min of Unfiltered Value",
                    fin_list[1] : nf_2[file_name].min()
                }
            
            fin_stat_df.loc[len(fin_stat_df)] = {
                    fin_list[0] : "Unfiltered Value Count above Upper bound",
                    fin_list[1] : ct
                }
            
            fin_stat_df.loc[len(fin_stat_df)] = {
                    fin_list[0] : "Unfiltered Value Count below Lower bound",
                    fin_list[1] : cte
                }
            

            
            return_list = [nan_df, non_nan_df, fin_stat_df, nf_1, nf_2, mf_org, mf, emf, num ,enum, file_name]
            return return_list

            

    elif (data):
        non_valid_date_df = pd.DataFrame(columns = col)
        for x in result_df.iterrows():
            e = x[1][1]
            row = {
                id : x[1][0],
                file_name : e
                }
            if (isinstance(e, float)):
                nan_df.loc[len(nan_df)] = row
                continue
            try:
                if (("/"in e) or ("-" in e)):
                    da = e
                    if ("/" in e):
                        da = e.replace("/", "-")
                    if (len(da)>10):
                        err_df.loc[len(err_df)] = row
                    if ("-" in da[-4:]):
                        pass
                    elif ("-" in da[0:4]):
                        x = da.split('-')
                        da = x[2]+'-'+x[1]+'-'+x[0]
                    else:
                        err_df.loc[len(err_df)] = row
                        continue
                    if is_date_less_than_today(da):
                        non_nan_df.loc[len(non_nan_df)] = row
                    else:
                        non_valid_date_df.loc[len(non_valid_date_df)] = row


                else:
                    err_df.loc[len(err_df)] = row
            except:
                err_df.loc[len(err_df)] = row
        
        
        row = {}
        row[fin_list[0]] = "Null Count"
        row[fin_list[1]] = len(nan_df)
        fin_stat_df.loc[len(fin_stat_df)] = row
        row[fin_list[0]] = "Non-Null Count"
        row[fin_list[1]] = len(non_nan_df)
        fin_stat_df.loc[len(fin_stat_df)] = row
        row[fin_list[0]] = "Upcoming Count"
        row[fin_list[1]] = len(non_valid_date_df)
        fin_stat_df.loc[len(fin_stat_df)] = row

        return_list = [nan_df, non_nan_df, fin_stat_df, non_valid_date_df, err_df]
        return return_list

                
    else:
        for x in result_df.iterrows():
            e = x[1][1]
            row = {
                id : x[1][0],
                file_name : e
                }
            if (isinstance(e, float)):
                nan_df.loc[len(nan_df)] = row
            else:
                non_nan_df.loc[len(non_nan_df)] = row

        fin_stat_df.loc[len(fin_stat_df)] = {
                    fin_list[0] : 'NaN Count',
                    fin_list[1] : len(nan_df)
                }
            
        fin_stat_df.loc[len(fin_stat_df)] = {
                    fin_list[0] : 'Non-NaN Count',
                    fin_list[1] : len(non_nan_df)
                }
            
        return_list = [nan_df, non_nan_df, fin_stat_df]
        return return_list
    



# In[ ]:


def master(file_name, mobile, op, name, data_type, num, enum, thresh, data):

    df = pd.concat([mdf[id], mdf[file_name]], axis = 1)
    col = df.columns
    req_df = df

    final_df = making_final_df(col, req_df, file_name)
    result_df = making_result_df(col, final_df, mobile, file_name, op, name, data_type)
    err_df = making_err_df(col, req_df, result_df, file_name)
    result_op = fin_ops(data_type, mobile, col, result_df, file_name, op, num, enum, thresh, data, err_df)

    if data == True:
        err_df = result_op[-1]
        result_op.pop()

    result_op.extend([err_df, final_df, req_df])

    return result_op
    
    

