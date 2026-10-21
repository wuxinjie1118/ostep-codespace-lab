#! /usr/bin/env python
# fairness.py -- reproduces the lottery-scheduler fairness study of OSTEP Ch.9 (Figure 9.2)
#
# Two jobs, equal tickets (100 each), equal length R; quantum = 1.
# Lottery selection replicates lottery.py exactly:
#   r = int(random()*1000001); winner = r % tickTotal
# Fairness F = (time first job completes) / (time second job completes).
# Average over 30 trials per job length R, for R from 1..1000.
# Outputs: table on stdout, fairness.csv, fairness_graph.svg (pure stdlib, no deps).

import random, math, os

TRIALS = 30
RS = [1,2,3,4,5,6,8,10,15,20,30,50,75,100,150,200,300,500,750,1000]

def one_run(R, seed):
    # exactly replicates lottery.py: walk the job list accumulating tickets
    # until the counter exceeds the winning ticket; finished jobs keep 0 tickets.
    random.seed(seed)
    tickets = [100, 100]
    run = [R, R]
    clock = 0
    fins = []
    while len(fins) < 2:
        r = int(random.random() * 1000001)
        total = tickets[0] + tickets[1]
        winner = r % total
        acc = 0
        wjob = 1
        for j in (0, 1):
            acc += tickets[j]
            if acc > winner:
                wjob = j
                break
        clock += 1
        run[wjob] -= 1
        if run[wjob] == 0:
            fins.append((clock, wjob))
            tickets[wjob] = 0
    t0 = fins[0][0]; t1 = fins[1][0]
    return min(t0, t1), max(t0, t1)

def avg_fairness(R):
    s = 0.0
    for t in range(TRIALS):
        a, b = one_run(R, 1000 + R * 100 + t)
        s += a / b
    return s / TRIALS

def svg(points):
    W, H = 940, 620
    L, Rm, T, B = 80, 40, 50, 70
    pw, ph = W - L - Rm, H - T - B
    xmin, xmax = 1, 1000
    ymin, ymax = 0.0, 1.0
    def X(x):
        return L + pw * (math.log10(x) - math.log10(xmin)) / (math.log10(xmax) - math.log10(xmin))
    def Y(y):
        return T + ph * (1 - (y - ymin) / (ymax - ymin))
    out = []
    out.append('<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d" font-family="Arial,Helvetica,sans-serif">' % (W, H, W, H))
    out.append('<rect width="%d" height="%d" fill="white"/>' % (W, H))
    out.append('<text x="%d" y="%d" font-size="20" font-weight="bold" text-anchor="middle">Lottery Scheduling Fairness (2 jobs, 100 tickets each, 30 trials)</text>' % (W/2, 32))
    # gridlines + y labels
    for yv in [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]:
        y = Y(yv)
        out.append('<line x1="%d" y1="%.1f" x2="%d" y2="%.1f" stroke="#ddd" stroke-width="1"/>' % (L, y, L+pw, y))
        out.append('<text x="%d" y="%.1f" font-size="13" text-anchor="end" fill="#333">%.1f</text>' % (L-10, y+4, yv))
    # x labels (log ticks 1,2,5,10,20,50,100,200,500,1000)
    for xv in [1,2,5,10,20,50,100,200,500,1000]:
        x = X(xv)
        out.append('<text x="%.1f" y="%d" font-size="13" text-anchor="middle" fill="#333">%d</text>' % (x, H-B+20, xv))
        out.append('<line x1="%.1f" y1="%d" x2="%.1f" y2="%d" stroke="#ddd" stroke-width="1"/>' % (x, T, x, T+ph))
    out.append('<text x="%d" y="%d" font-size="14" text-anchor="middle" fill="#333">Job Length (R, log scale)</text>' % (L+pw/2, H-28))
    out.append('<text x="%d" y="%d" font-size="14" text-anchor="middle" fill="#333" transform="rotate(-90 %d %d)">Average Fairness (F)</text>' % (22, T+ph/2, 22, T+ph/2))
    # axes
    out.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="#333" stroke-width="1.5"/>' % (L, T, L, T+ph))
    out.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="#333" stroke-width="1.5"/>' % (L, T+ph, L+pw, T+ph))
    # stride: perfectly fair F=1 (dashed)
    y1 = Y(1.0)
    out.append('<line x1="%d" y1="%.1f" x2="%d" y2="%.1f" stroke="#e64c3c" stroke-width="2" stroke-dasharray="8,5"/>' % (L, y1, L+pw, y1))
    out.append('<text x="%d" y="%.1f" font-size="13" fill="#e64c3c" text-anchor="end">Stride scheduler (deterministic): F = 1.0</text>' % (L+pw-8, y1-8))
    # lottery curve
    path = 'M%.1f %.1f ' % (X(points[0][0]), Y(points[0][1]))
    for R, F in points[1:]:
        path += 'L%.1f %.1f ' % (X(R), Y(F))
    out.append('<path d="%s" fill="none" stroke="#2f6fd6" stroke-width="2.5"/>' % path)
    # markers
    for R, F in points:
        out.append('<circle cx="%.1f" cy="%.1f" r="3.5" fill="#2f6fd6"/>' % (X(R), Y(F)))
    out.append('<text x="%d" y="%d" font-size="14" fill="#2f6fd6" font-weight="bold">Lottery scheduler (average of %d trials)</text>' % (L+10, 44, TRIALS))
    out.append('</svg>')
    return '\n'.join(out)

def main():
    here = os.path.dirname(os.path.abspath(__file__))
    rows = []
    print('R\tAvgFairnessF')
    for R in RS:
        F = avg_fairness(R)
        rows.append((R, F))
        print('%d\t%.4f' % (R, F))
    with open(os.path.join(here, 'fairness.csv'), 'w', encoding='utf-8') as f:
        f.write('R,avg_fairness_F\n')
        for R, F in rows:
            f.write('%d,%.4f\n' % (R, F))
    with open(os.path.join(here, 'fairness_graph.svg'), 'w', encoding='utf-8') as f:
        f.write(svg(rows))
    print('Wrote fairness.csv and fairness_graph.svg')

if __name__ == '__main__':
    main()
