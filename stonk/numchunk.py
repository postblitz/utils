import datetime
import os
import matplotlib.pyplot as plt

stock_nums = {}
time_format = '%Y.%m.%d_%H.%M.%S'
date_to_get = datetime.datetime.strptime('2022.02.19_00.00.00', time_format)


for symbol in os.listdir('info'):
    for date in os.listdir(os.path.join('info', symbol)):
        fdate = datetime.datetime.strptime(date, time_format)
        if fdate.date() != date_to_get.date():
            print('%s not %s date' % (date, date_to_get))
            continue
        for filename in os.listdir(os.path.join('info', symbol, date)):
            if filename == 'nums':
                stock_nums[symbol] = {}
                path = os.path.join('info', symbol, date, filename)
                print(path)
                with open(path, 'r') as f:
                    whole_file = f.read()
                    for item in whole_file.split('\n'):
                        try:
                            key, value = item.split()
                            stock_nums[symbol][key] = value
                        except ValueError as ex:
                            if len(item.split()) == 0:
                                pass
print(len(stock_nums))

pe_syms = dict()
for sym in stock_nums:
    try:
        if 'trailingPE' not in stock_nums[sym]:
            continue
        price = float(stock_nums[sym]['currentPrice'])
        pe = float(stock_nums[sym]['trailingPE'])
        closing_price = float(stock_nums[sym]['previousClose'])
        if 'shortPercentOfFloat' in stock_nums[sym]:
            short_ratio = float(stock_nums[sym]['shortPercentOfFloat'])
        else:
            short_ratio = 0
        current_pe = (price * pe) / closing_price
        pe_syms[current_pe]=sym
        pe_diff_percentage = (abs(current_pe - pe)*100/pe)
        print('%s pe=%6.4f cpe=%6.4f pe_diff=%3.1f%% %6.4f' % (sym, pe, current_pe, pe_diff_percentage, short_ratio), end='')
        if pe_diff_percentage > 20:
            print(' < ', end='')
        else:
            print(' ', end='')
        if short_ratio > 0.05 and short_ratio < 0.1:
            print('SHORTED')
        elif short_ratio > 0.1:
            print('HEAVILY SHORTED %3.1f%%' % (short_ratio * 100))
        else:
            print()
    except Exception as ex:
        print('%s %s' % (sym, ex))

for pe in sorted(list(pe_syms.keys())):
    print('%s %4.2f' % (pe_syms[pe], pe))

#print(stock_nums)
# syms = []
# vals = []
# for sym in stock_nums:
#     if 'trailingPE' in stock_nums[sym]:
#         # print('%s %s' % (sym, stock_nums[sym]['trailingPE']))
#         syms.append(sym)
#         vals.append(float(stock_nums[sym]['trailingPE']))
# plt.ylabel('PE ratio')
# plt.plot(syms, vals)
# plt.show()
# for key in stock_nums['amat']:
    # print(key)
    # for symbol in stock_nums:
    #     try:
    #         print('%s %s' % (symbol, stock_nums[symbol][key]))
    #     except KeyError:
    #         if key not in stock_nums[symbol]:
    #             pass
