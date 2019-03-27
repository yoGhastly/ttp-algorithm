import random
import tools
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

data = pd.read_csv('mid_1tournament_g_10p100_cr_0.7_t_5_m_0.01', sep='\t')
data2 = pd.read_csv('mid_1tournament_g_500p100_cr_0.7_t_5_m_0.01', sep='\t')
data3 = pd.read_csv('mid_1tournament_g_50p10_cr_0.7_t_5_m_0.01', sep='\t')
data4 = pd.read_csv('mid_1tournament_g_50p200_cr_0.7_t_5_m_0.01', sep='\t')


items_sorted_strategy = \
    {
        'best_ratio':tools.get_list_of_ordered_items('best_ratio'),
        'most_expensive':tools.get_list_of_ordered_items('most_expensive'),
        'lightest':tools.get_list_of_ordered_items('lightest')
    }



Y = np.asarray(data3.index.values)
Y_500 = np.asarray(data2.index.values)
Y_10 = np.asarray(data.index.values)

avg_1= np.asarray(data['AVG'])
max_1 = np.asarray(data['MAX'])
min_1 = np.asarray(data['MIN'])

avg_2 = np.asarray(data2['AVG'])
max_2 = np.asarray(data2['MAX'])
min_2 = np.asarray(data2['MIN'])

avg_3 = np.asarray(data3['AVG'])
max_3 = np.asarray(data3['MAX'])
min_3 = np.asarray(data3['MIN'])

avg_4 = np.asarray(data4['AVG'])
max_4 = np.asarray(data4['MAX'])
min_4 = np.asarray(data4['MIN'])




plt.figure()
plt.subplot(2, 1, 1)
plt.plot(Y_10, max_1,label='max')
plt.plot(Y_10, avg_1,label='avg')
plt.plot(Y_10, min_1,label='min')
# plt.axis([1,5,0,100])
plt.legend()
plt.title('Population 10')

plt.subplot(2, 1, 2)
plt.plot(Y_500, max_2,label='max')
plt.plot(Y_500, avg_2,label='avg')
plt.plot(Y_500, min_2,label='min')
plt.title('Population 500')
plt.legend()



plt.show()

plt.subplot(2, 1, 1)
plt.plot(Y, max_3)
plt.plot(Y, avg_3)
plt.plot(Y, min_3)
# plt.axis([1,5,0,100])
plt.legend()
plt.title('Generations = 10')

plt.subplot(2, 1, 2)
plt.plot(Y, max_4)
plt.plot(Y, avg_4)
plt.plot(Y, min_4)
plt.title('Generations = 200')
plt.legend()

plt.show()
