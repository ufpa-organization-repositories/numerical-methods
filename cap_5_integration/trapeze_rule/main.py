from modules import *

table = get_table(file_name='table.csv')

integral = calc_integral_by_trapeze_method(table)
print(integral)
