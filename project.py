import pandas as pd
import re
import numpy as np
import matplotlib.pyplot as plt
import matplotcheck.notebook as nb

from datetime import datetime

ildata = pd.read_csv('ildata.csv')

def main():
    mainFlag=True
    while(mainFlag):
        try:
            county, interval = get_input()
            x = final(county, interval)
            plt.pause(1)
            mainFlag = False
        except ValueError:
            pass
    return x

def get_input():
    county_array = ildata.region_name.unique()
    county_list = [x.split(' County')[0] for x in county_array]
    county_list = [x.lower() for x in county_list]

    input_county = input("Please enter the name of Illinois County: ")
    if input_county.lower().strip() in county_list:
        pass
    else:
        print(f'{input_county} is not a county in Illinois.')
        print('Names of counties in IL are as below.')
        print(county_list)
        raise ValueError

    input_interval = input("Please enter the interval frequency in weeks ('1, 4, or 12'): ")
    if input_interval in ['1', '4', '12']:
        pass
    else:
        print(f'{input_interval} weeks duration data is not available')
        raise ValueError

    return input_county, input_interval

def subsetter(county, interval):
    r = re.compile(f'{county} ', re.IGNORECASE)
    regmatch = np.vectorize(lambda x: bool(r.search(x)))
    countydata = ildata[regmatch(ildata.region_name.values)]
    county_with_interval_data = countydata[countydata['duration']== interval+' weeks']
    return county_with_interval_data

def final(county, interval):
    subset_data = subsetter(county, interval)
    interests = ["total_homes_sold", "inventory","age_of_inventory","median_sale_price"] +\
    ["months_of_supply", "percent_homes_sold_above_list"]
    print(f"Average quantities for {county.title()} County, IL on {interval} weeks basis")
    print(subset_data[interests].mean().round(2))

    if np.isnan(subset_data[interests[0]].mean()):
        raise ValueError

    print(f"\nAverage quantities for Illinois on {interval} weeks basis")
    print(ildata[interests].mean().round(2))

    print(f"\n\nCorrelations among select quantities for {county.title()} County, IL")
    print(subset_data[interests].corr().round(3))
    subset_data['period_time'] = pd.to_datetime(subset_data['period_end'], dayfirst=True)
    plt.pause(1)

    fig1, ax1 = plt.subplots(2,3, figsize = [12,8])

    subset_data.plot.scatter('period_time', 'total_homes_sold', ax = ax1[0,0], s = 6)
    subset_data.plot.scatter('period_time', 'total_new_listings', ax = ax1[0,0], s = 6, c = 'C1')
    subset_data.plot.scatter('period_time', 'inventory', ax = ax1[0,0], s = 6, c = 'C2')

    subset_data.plot.scatter('period_time', 'age_of_inventory', ax = ax1[0,1], s = 6)
    subset_data.plot.scatter('period_time', 'median_days_on_market', ax = ax1[0,1], s = 6, c = 'C1')

    subset_data.plot.scatter('period_time', 'months_of_supply', ax = ax1[0,2], s = 6, c = 'C0')

    subset_data.plot.scatter('period_time', 'median_sale_price', ax = ax1[1,0], s = 6)
    subset_data.plot.scatter('period_time', 'median_active_list_price', ax = ax1[1,0], s = 6, c = 'C1')

    subset_data.plot.scatter('period_time', 'percent_homes_sold_above_list', ax = ax1[1,1], s = 6)
    subset_data.plot.scatter('period_time', 'percent_off_market_in_one_week', ax = ax1[1,1], s = 6, c = 'C1')

    subset_data.plot.scatter('period_time', 'avg_offer_to_list', ax = ax1[1,2], s = 6)
    subset_data.plot.scatter('period_time', 'average_sale_to_list_ratio', ax = ax1[1,2], s = 6, c = 'C1')

    fig1.suptitle(f'{county.title()} County, IL')

    ax1[0,0].legend(['tot_homes_sold','tot_new_listings','inventory'], handletextpad = 0.1, borderpad = 0.1)
    ax1[0,1].legend(['age_of_inventory','median_days_on_market'], handletextpad = 0.1, borderpad = 0.1)
    ax1[1,0].legend(['med_sale_price','med_active_list_price'], handletextpad = 0.1, borderpad = 0.1)
    ax1[1,1].legend(['%homes_sold_above_list','%off_market_in_1week'], handletextpad = 0.1, borderpad = 0.1)
    ax1[1,2].legend(['avg_offer_to_list','avg_sale_to_list'], handletextpad = 0.1, borderpad = 0.1)

    ax1[0,2].set_ylabel('months_of_supply')
    ax1[0,0].set_ylabel('Number')
    ax1[0,1].set_ylabel('Days')
    ax1[1,0].set_ylabel('Price ($)')
    ax1[1,1].set_ylabel('Percent')
    ax1[1,2].set_ylabel('ratio')

    fig1.tight_layout()
    fig1.savefig(county+interval+ '_trends.png', dpi=120, bbox_inches = 'tight')
    axes=nb.convert_axes(plt,which_axes="current")
    return axes

if __name__=="__main__":
    main()
