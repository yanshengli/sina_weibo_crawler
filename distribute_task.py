__author__ = 'yanshengli@hitsz.edu.cn'

followee = set()
with open('followee.txt') as f:
    for line in f.readlines():
        if line.strip().isdigit():
            followee.add(line.strip())

followee = list(followee)
tot = len(followee)
per = tot / 53

idx = 0
for i in range(0, tot, per):
    idx += 1
    if idx == 54:
        for fo in followee[i:i + per]:
            import random
            r = random.choice(range(0, 54))
            print r
            with open('task/uid_%s.txt' % r, 'a') as f:
                print >> f, fo
    else:
        with open('task/uid_%s.txt' % idx, 'w') as f:
            for fo in followee[i:i + per]:
                print >> f, fo