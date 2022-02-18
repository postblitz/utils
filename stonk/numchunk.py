import os
import matplotlib.pyplot as plt

stock_nums = {}

for symbol in os.listdir('info'):
    for date in os.listdir(os.path.join('info', symbol)):
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

for sym in stock_nums:
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
    print('%s %s %s %s %s' % (sym, pe, current_pe, current_pe - pe, short_ratio), end='')
    if abs(current_pe - pe) > 2:
        print(' < ', end='')
    else:
        print(' ', end='')
    if short_ratio > 0.05 and short_ratio < 0.1:
        print('SHORTED')
    elif short_ratio > 0.1:
        print('HEAVILY SHORTED')
    else:
        print()

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
