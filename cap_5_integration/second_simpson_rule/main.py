from modules import *

table = get_table(file_name='table.csv')

integral = calc_integral_by_second_simpson_rule(table)
print(integral)