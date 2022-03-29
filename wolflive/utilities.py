# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
import datetime
# %%
# pop account details from input files
def get_account_from_input(filename='db/input.txt'):
    """
    function takes in the input text file directory
    that containes account details
    with format address:password
    remove the top details from the file and returns it
    in:
        filename:str
    out:
        [address,password]:list
    """
    with open(filename,encoding='utf-8') as file:
        main = file.readlines()
        if main:
            one = main.pop(0)
            with open(filename,'w',encoding="utf-8") as f:
                f.writelines(main)
            return one.replace('\n','').split(':')
        else:
            return False
# get_account_from_input()







# %%
# get and record new account detail

import csv
import os



def generate_output_account_details(details):
    if os.path.exists('db/output.txt'):
        with open('db/output.txt','a') as file:
            file.write(details+'\n')
    else:
        with open('db/output.txt','w') as file:
            file.write(details+'\n')





def get_and_record_new_account_detail(filename='accounts.csv',account_details = [],primary_account = '',new_password=123456):
    
    """
    function keep record of old account details and new account details
    in:
        filename:str
    out:
        [new_address,new_password]:list
    """
    
    if not os.path.isdir('db'):
        
        os.mkdir('db')
    if os.path.exists('db/'+ filename):
        
        with open('db/' + filename, newline='') as csvfile:
            
            reader = csv.DictReader(csvfile)
            length = len(list(reader)) + 1
            with open('db/' + filename, 'a', newline='') as csvfile:
                
                fieldnames = ['old_address', 'old_password','new_address','new_password']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writerow({'old_address': account_details[0], 'old_password': account_details[1],'new_address':f'+{length+1}@'.join(primary_account.split('@')),'new_password':new_password})
                generate_output_account_details(f'+{length}@'.join(primary_account.split('@'))+':'+str(new_password))

                return {'old_email': account_details[0], 'old_password': account_details[1],'new_email':f'+{length}@'.join(primary_account.split('@')),'new_password':new_password}
                
        

    else:
        
        length = 1
        with open('db/'+filename, 'w', newline='') as csvfile:
            print(6)
            fieldnames = ['old_address', 'old_password','new_address','new_password']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerow({'old_address': account_details[0], 'old_password': account_details[1],'new_address':f'+{length}@'.join(primary_account.split('@')),'new_password':new_password})
            return {'old_email': account_details[0], 'old_password': account_details[1],'new_email':f'+{length}@'.join(primary_account.split('@')),'new_password':new_password}









# %%
# funtion to get workspace
"""
workspace in this context is dictionary 
that contains the bot progress
for the current account in the list

"""
import pickle
import os

def _get_workspace():
    """
        return existing wokspace from 
        pickle file and return False of none exsits

        workspace in this context is dictionary 
        that contains the bot progress
        for the current account in the list
    out:
        workspace:dict
    """

    
    if os.path.exists('db/workspace.pickle'):
        with open('db/workspace.pickle','rb') as file:
            return pickle.load(file)
            
    else:
        return False

# get_workspace()


# %%
# set workspace
import pickle
from datetime import datetime


def _set_workspace(**kwargs):
    """
    take in keyword argument and 
    add it to the default workpace
    parameters and return the created workspace
    in:
        data:kwargs
    out:
        stored data:dict
    """
    pre_data = {
        "change_email":False,
        "send_validation_email":False,
        "time_send":None,
        "confirm_validation":False,
        "change_password":False
        }
    if not os.path.isdir('db'):
        os.mkdir('db')
    with open('db/workspace.pickle','wb') as file:
        pickle.dump({**pre_data,**kwargs},file)
        return {**pre_data,**kwargs}
# set_workspace(what='yes o',change_password=True)


# drop workspace
# %%
def _drop_workspace():
    """
        function delete the current workspace
    """
    if os.path.exists('db/workspace.pickle'):
        os.remove('db/workspace.pickle')



# %%
import requests
import random
from bs4 import BeautifulSoup
from random import choice



def get_proxy():
    """
        function returns a python obect containing
        return dict:
            ip:str
            port:str
            code:str
            country:str
            google:str
            https:bool
            last_checked:str

    """
    try:
        # response = requests.get('https://sslproxies.org/')
        # soup = BeautifulSoup(response.content, 'html5lib') 
        # rows = soup.select('#proxylisttable  tbody tr')
        # proxies = list()
        proxies =None
        with open('active_proxies.txt',encoding='utf-8') as f:
            # proxies = [x for x in f.readlines() if x.split(':')[1] in ['8080\n','80\n']]
            proxies = f.readlines()
            
        # for row in rows:
        #     # raw_data = row.select('td')
        #     data = {'ip':raw_data[0].text,'port':raw_data[1].text,'code':raw_data[2].text,'country':raw_data[3].text,'anonymity':raw_data[4].text, 'google':raw_data[5].text,'https':bool(raw_data[6].text=='yes'),'last_checked':raw_data[7].text}
        #     proxies.append(data)
        return choice(proxies)
    except Exception as e:
        print("No internet connection")
        return 






# %%
# generate_output_account_details("helloo.@gmail.com:112344")
# %%

if __name__ == '__main__':
    data = {'change_email': True, 'send_validation_email': True, 'time_send': None, 'confirm_validation': True, 'change_password': False, 'old_email': 'aniekutmfonekere@gmail.com', 'old_password': '123456', 'new_email': 'aniekutmfonekere@gmail.com', 'new_password': 123456}
    _set_workspace(**data)