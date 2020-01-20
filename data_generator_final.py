'''
Goals:
1. Generate  (1+i*pi/n)^n for n as big as possible
2. Create "claculator", that will be able to count [a_(n-1)-a_(n-2)]/ [a_n-a_(n-1)], for a_n=(1+ipi/n)^n
3. Create an algorithm that will find subsequence B of the sequence A, eg. b_1=a_4,b_2=a_21,b_3=a_85,... that  [b_(n-1)-b_(n-2)]/ [b_n-b_(n-1)] will be near Feigenbaum constant delta=4.6692016099 to the given decimal precision.
'''

import math
import multiprocessing as mp
CPU_NUM = 10

Feigenbaum_const = 4.6692016099
decimal_precision = 5
upper_limit = 1000000
i_upper_limit = 50
j_upper_limit = 5000
k_upper_limit = 1000000
l_upper_limit = 1000000
m_upper_limit = 1000000

i_start_value = 1

def findIndexes(i):
    l_answers_3 = {}
    l_answers_4 = {}
    l_answers_5 = {}

    j = i + 1
    k = j + 1
    while (j < j_upper_limit):
        k = j + 1
        while (k < k_upper_limit):
            result = (buffer[j] - buffer[i]) / (buffer[k] - buffer[j])
            if(round(result.real, decimal_precision) == round(Feigenbaum_const, decimal_precision)):
                l_answers_3[result] = (i, buffer[i], j, buffer[j], k, buffer[k])
                l = k + 1
                while (l < l_upper_limit):
                    result = (buffer[k] - buffer[j]) / (buffer[l] - buffer[k])
                    if(round(result.real, decimal_precision) == round(Feigenbaum_const, decimal_precision)):
                        l_answers_4[result] = (i, buffer[i], j, buffer[j], k, buffer[k], l, buffer[l])
                        m = l + 1
                        while (m < m_upper_limit):
                            result = (buffer[l] - buffer[k]) / (buffer[m] - buffer[l])
                            if(round(result.real, decimal_precision) == round(Feigenbaum_const, decimal_precision)):
                                l_answers_5[result] = (i, buffer[i], j, buffer[j], k, buffer[k], l, buffer[l], m, buffer[m])
                            m += 1
                    l += 1
            k += 1
        j += 1
    return (l_answers_3, l_answers_4, l_answers_5)


buffer = []
for n in range(1, upper_limit+1):
    complex_number = complex(1, math.pi/n)
    buffer.append(pow(complex_number, n))

answers_3 = {}      #triplets
answers_4 = {}      #quadruplets
answers_5 = {}      #quintuplets

if __name__ == '__main__': 
    print('Hello, I am Feigenbaum Constant ' + str(Feigenbaum_const) + '! How are you?')
    print('decimal_precision:' + str(decimal_precision))

    if(CPU_NUM > mp.cpu_count()):
        CPU_NUM = mp.cpu_count()
    
    pool = mp.Pool(CPU_NUM)
        
    i_indexes = list(range(i_start_value, i_upper_limit))
    pieces = pool.map(findIndexes, i_indexes)       #parallel processing per i
    
    for p in pieces:
        answers_3.update(p[0])
        answers_4.update(p[1])
        answers_5.update(p[2])
                
    pool.close()
    pool.join()
        
    with open("results_ijk_precision_" + str(decimal_precision) + "_i_range("
              + str(i_start_value) + "," + str(i_upper_limit) + ").txt", "w") as result_1:
        for line in answers_3:
            result_1.write(str(line) + " " + str(answers_3[line][0]) + " " + str(answers_3[line][2]) + " " + str(answers_3[line][4]) + "\n")
            
    with open("results_ijkl_precision_" + str(decimal_precision) + "_i_range("
              + str(i_start_value) + "," + str(i_upper_limit) + ").txt", "w") as result_2:
        for line in answers_4:
            result_2.write(str(line) + " " + str(answers_4[line][0]) + " " + str(answers_4[line][2])
            + " " + str(answers_4[line][4]) + " " + str(answers_4[line][6]) + "\n")
            
    with open("results_ijklm_precision_" + str(decimal_precision) + "_i_range("
              + str(i_start_value) + "," + str(i_upper_limit) + ").txt", "w") as result_3:
        for line in answers_5:
            result_3.write(str(line) + " " + str(answers_5[line][0]) + " " + str(answers_5[line][2])
            + " " + str(answers_5[line][4]) + " " + str(answers_5[line][6]) + " " + str(answers_5[line][8]) + "\n")

    print("Results saved, Finish")