
def get_loop(all_nums, last_num):
    l=len(all_nums)
    for i in range(l):
        if all_nums[i] == last_num:
            break
    return all_nums[i:]

def add_loop(loop):
    global loops
    global raw_l
    s = set(loop)
    if s not in loops:
        loops.append(s)
        raw_l.append(loop)

for inc in range(20):
    loops = list()
    raw_l = list()
    for start in range(100):
        loop_count = 0
        c = start
        l = []
        while c not in l and loop_count < 1000:
            loop_count += 1
            l.append(c)
            if c % 2 == 0:
                c = int(c / 2)
            else:
                c = c + inc + 1
        lup = get_loop(l, c)
        if len(lup) > 1:
            add_loop(lup)
    print('%s %s %s' % (inc, len(raw_l), raw_l))