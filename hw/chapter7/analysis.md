# Chapter 7: CPU Scheduling — FIFO, SJF, RR Analysis

## Verified Results Summary

| Question | Workload | Policy | Avg Response | Avg Turnaround |
|---|---|---|---|---|
| Q1 | 200,200,200 | FIFO | 200.00 | 400.00 |
| Q1 | 200,200,200 | SJF | 200.00 | 400.00 |
| Q2 | 100,200,300 | FIFO | 133.33 | 333.33 |
| Q2 | 100,200,300 | SJF | 133.33 | 333.33 |
| Q3 | 200,200,200 | RR (q=1) | 1.00 | 599.00 |

## Q1. Three jobs of length 200 (FIFO & SJF)

Commands:
    python3 ./ext/ostep-homework/cpu-sched/scheduler.py -l 200,200,200 -p FIFO -c
    python3 ./ext/ostep-homework/cpu-sched/scheduler.py -l 200,200,200 -p SJF -c

Prediction: jobs complete at t=200, 400, 600, so avg turnaround = (200+400+600)/3 = 400,
avg response = (0+200+400)/3 = 200.

Verified: FIFO and SJF both give Response 200.00 / Turnaround 400.00. Identical because
all jobs have the same length, so SJF's order equals FIFO's order.

## Q2. Jobs of length 100, 200, 300 (FIFO & SJF)

Commands:
    python3 ./ext/ostep-homework/cpu-sched/scheduler.py -l 100,200,300 -p FIFO -c
    python3 ./ext/ostep-homework/cpu-sched/scheduler.py -l 100,200,300 -p SJF -c

Prediction: completions at t=100, 300, 600; avg turnaround = 333.33, avg response = 133.33.

Verified: both give Response 133.33 / Turnaround 333.33. The input is already sorted by
length, so SJF runs in the same order as FIFO.

## Q3. Three jobs of length 200 with RR, quantum = 1

Command:
    python3 ./ext/ostep-homework/cpu-sched/scheduler.py -l 200,200,200 -p RR -q 1 -c

Prediction: jobs get their first slice at t=0,1,2 -> avg response = 1. Jobs finish at
t=598,599,600 -> avg turnaround = 599.

Verified: Response 1.00 / Turnaround 599.00. RR is excellent for response time but
nearly pessimal for turnaround time — the fairness/performance trade-off.

## Q4. When does SJF deliver the same turnaround time as FIFO?

When job lengths are non-decreasing in arrival order (the FIFO order is already
shortest-first, e.g. 100,200,300), or when all jobs have the same length. Then SJF and
FIFO produce the same schedule.

## Q5. When does SJF deliver the same response time as RR?

When all jobs have the same length L and the quantum q >= L. RR never preempts a job
before completion, so each job's first run happens at 0, L, 2L, ... exactly as under SJF.
Example: -l 200,200,200 -p RR -q 200 -c gives avg response 200.00, same as SJF.

## Q6. SJF response time as job lengths increase

Response time grows linearly: the k-th job's response time equals the sum of the lengths
of all shorter jobs before it. Demo (SJF):

    -l 1,2,3        -> avg response 1.33
    -l 10,20,30     -> avg response 13.33
    -l 100,200,300  -> avg response 133.33

Multiplying job lengths by 10 multiplies response time by 10.

## Q7. RR response time as quantum increases; worst-case formula

Response time grows linearly with the quantum: the larger the quantum, the more RR
behaves like FIFO and the worse the response time. Demo (three jobs of length 200):

    q=1   -> avg response 1.00
    q=10  -> avg response 10.00
    q=100 -> avg response 100.00
    q=200 -> avg response 200.00

Worst-case response time with N jobs and quantum q: the last job waits for the N-1 jobs
ahead of it to run one full slice each, so:

    worst-case response time = (N-1) * q