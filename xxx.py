import time
#3x+1 etc.
def get_loop(all_nums, last_num):
    l=len(all_nums)
    for i in range(l):
        if all_nums[i] == last_num:
            break
    return all_nums[i:]

def add_loop(loop):
    global loops
    s = set(loop)
    if s not in loops:
        loops.append(s)
        raw_l.append(loop)
        print(' added loop ', end='')

max_nr = 1000
good = []
for multiplier in range(10):
    multiplier = multiplier * 2 -9
    for adder in range(abs(multiplier)-2):
        adder = adder * 2 -7
        for slicer in [-2, 2]:
            print('%s %s %s' % (multiplier, adder, slicer))
            broken = 0
            loops = list()
            raw_l = list()
            for start in range(max_nr):
                l = []
                c = start
                loop_count = 0 
                while c not in l:
                    loop_count += 1
                    l.append(c)
                    if c % slicer == 0:
                        c = int(c / slicer)
                    else:
                        c = multiplier * c + adder
                    #print(c, end=' ')
                    if loop_count == 1000:
                        broken += 1
                        break
                lup = get_loop(l, c)    
                if len(lup) > 1:
                    #print(start, end=': ')
                    add_loop(lup)
                    #print('lc=%s loop:%s' % (loop_count, lup))
            print('%s %s' % (len(raw_l), raw_l))
            print('%6.4f%% exceeded loop limit' % (100*broken/max_nr))
            if broken == 0 :
                good.append((multiplier, adder, slicer, len(loops)))
print(good)