
import pandas as pd
import matplotlib.pyplot as plt


def data_convert():
    '''function to change object type of week commencing to date-time and for changing format'''
    
    # converting object type of week commencing to datetime
    data['Week commencing'] = pd.to_datetime(data['Week commencing'], dayfirst=True)

    # adding a new column to the data, which represet the given week commencing based on
    # YY-MM fomrat
    data['date_month'] = data['Week commencing'].dt.strftime('%Y-%m')

    return data

def data_typechange():
    ''' function to change the type and increase useablity of completion_rate '''
    
    # converting object type of completion rate to float type by utilizing .str.rstrip()
    # to remove of the percentage sign,
    # then dividing by 100.00 inoder to convert from percentage to actual value
    
    return data['Completion_rate'].str.rstrip('%').astype(float) /100.0

def completed_total(date_month):
    '''function to calculate completed total from completion rate'''
    
   # We are passing date month as an argument in this function and taking that
   # particular row using loc function to calculate completed total from 
   # completion rate and transaction total. 
   # The formula completed total = completion rate * transaction total is used.
    
    return date_month,(data.loc[data['date_month'] == date_month]['Completion_rate']) *\
           (data.loc[data['date_month'] == date_month]['Transactions_total'])                                                         


def add_sum():
   ''' function to find the sum of columns based on aggregate of months '''
    
   # Based on grouping date month column according to each month in given year,
   # we are attempting to find the sum of each specified column
   # ('Very satisfied,Satisfied,'Neither satisfied or dissatisfied,'Dissatisfied,
   # 'Very dissatisfied,'Transactions total,'Transactions online').
            
   return data.groupby(['date_month'], as_index=False)[['Very_satisfied',
                                                         'Satisfied',
                                                         'Neither_satisfied_or_dissatisfied',
                                                         'Dissatisfied',
                                                         'Very_dissatisfied',
                                                         'Transactions_total',
                                                         'Transactions_online']].sum()
# data is being saved as a csv file in this location
data = pd.read_csv('performance_data.csv')

# renaming certain columns in the data for user ease
data.rename(columns = {'Very satisfied':'Very_satisfied',
                       'Neither satisfied or dissatisfied':'Neither_satisfied_or_dissatisfied',
                       'Very dissatisfied':'Very_dissatisfied', 
                       'Transactions – total':'Transactions_total', 
                       'Transactions – online':'Transactions_online', 
                       'User satisfaction':'User_satisfaction', 
                       'Completion rate':'Completion_rate'}, 
            inplace =True)

# calling data_convert function which returns 
# new column to the data - date-month, which represet 
# the given week commencing based on YY-MM fomrat

data_convert()

# calling data_change method which returns completion_rate as a 
# float value and also by striping % sign 

data['Completion_rate'] = data_typechange()

# returns two value , one is date_month that we are passing and one is 
# completed total that we are calculating

date ,value = completed_total(data.date_month)

# plotting line graph based on 3 diffrent columns over a period of
 # nov 2021 to oct 2022

plt.figure(figsize = (10,5))
plt.style.use('ggplot')
plt.title("Satisfactory monthly count")
plt.plot (add_sum().date_month,add_sum().Very_dissatisfied,
          marker = 'o',
          label =' very dissatisfied',
          color="red")
plt.plot (add_sum().date_month,add_sum().Dissatisfied,
          marker = 'o',
          label = 'Dissatisfied',
          color = 'green')
plt.plot (add_sum().date_month,add_sum().Neither_satisfied_or_dissatisfied,
          marker = 'o',
          label = 'Neither satisfied or dissatisfied',
          color = 'blue')
plt.xlabel("Nov 2021 - Oct 2022", fontsize = 12 )
plt.ylabel('Count of customer rating', fontsize = 12 )
plt.legend(fontsize=12, loc='upper right')
plt.show()

# plotting stacked horizontal bar graph based on the
# transaction_total and transaction_online over a period of nov 2021 to oct 2022
 
plt.figure(figsize = (16,15))
plt.title("Monthly mode of transaction ",fontsize = 25)
plt.barh(add_sum().date_month, 
         add_sum().Transactions_total,
         label="Transactions_total" )
plt.barh(add_sum().date_month, 
         add_sum().Transactions_online,
         label="Transactions_online" )
plt.xticks(fontsize= 17)
plt.yticks(fontsize= 17)
plt.ylabel("Nov  2021 - Oct 2022", fontsize = 25 )
plt.xlabel('Transactions', fontsize = 25 )
plt.legend( fontsize=14, loc='upper right')
plt.show()

# plotting scatter plot based on total completed over a
 # time period of nov 2021 to oct 2022

plt.figure(figsize = (15,7))
plt.title("Completed count monthly",fontsize = 20)
plt.scatter(x=date,y=value)
plt.xlabel("Nov 2021 - Oct 2022", fontsize = 16 )
plt.ylabel('Total complete', fontsize = 16 )
plt.gcf().autofmt_xdate()
plt.show()

