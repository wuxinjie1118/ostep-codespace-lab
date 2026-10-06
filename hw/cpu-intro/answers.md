# OSTEP Ch.4 Homework Answers

## Q1
- Prediction / 预测: Both processes run 5 CPU-only instructions. PID 0 runs first (ticks 1-5) while PID 1 waits in READY; PID 1 runs at ticks 6-10.

```
Time        PID: 0        PID: 1           CPU           IOs
  1        RUN:cpu         READY             1          
  2        RUN:cpu         READY             1          
  3        RUN:cpu         READY             1          
  4        RUN:cpu         READY             1          
  5        RUN:cpu         READY             1          
  6           DONE       RUN:cpu             1          
  7           DONE       RUN:cpu             1          
  8           DONE       RUN:cpu             1          
  9           DONE       RUN:cpu             1          
 10           DONE       RUN:cpu             1          
```

Total time: 10; CPU utilization: 100%; I/O utilization: 0%.

- Reasoning / 理由: With `5:100`, every instruction is a CPU instruction and no I/O is ever issued. The CPU can never be idle because there is always a runnable process: PID 0 runs while PID 1 waits in READY, and as soon as PID 0 finishes, PID 1 takes over. The switch policy is irrelevant because no I/O ever happens.

## Q2
- Prediction / 预测: PID 0 runs its 4 CPU instructions first (ticks 1-4) while PID 1 waits in READY. PID 1 then issues its single I/O: 1 tick RUN:io, 5 ticks BLOCKED, 1 tick RUN:io_done. No other process is ready during the I/O, so the CPU idles for 5 ticks.

```
Time        PID: 0        PID: 1           CPU           IOs
  1        RUN:cpu         READY             1          
  2        RUN:cpu         READY             1          
  3        RUN:cpu         READY             1          
  4        RUN:cpu         READY             1          
  5           DONE        RUN:io             1          
  6           DONE       BLOCKED                           1
  7           DONE       BLOCKED                           1
  8           DONE       BLOCKED                           1
  9           DONE       BLOCKED                           1
 10           DONE       BLOCKED                           1
 11*          DONE   RUN:io_done             1          
```

Total time: 11; CPU utilization: 6/11 = 54.55%; I/O utilization: 5/11 = 45.45%.

- Reasoning / 理由: One I/O costs 1 (issue) + 5 (device work, default -L 5) + 1 (completion) = 7 ticks. Until PID 0 finishes, PID 1 sits in READY. During PID 1's BLOCKED ticks (6-10) no process is runnable, so the CPU idles.

## Q3
- Prediction / 预测: PID 0 issues its I/O first. Under the default SWITCH_ON_IO the OS switches to PID 1 while PID 0 is BLOCKED, so PID 1 uses the CPU during ticks 2-6. PID 0 handles io_done at tick 7.

```
Time        PID: 0        PID: 1           CPU           IOs
  1         RUN:io         READY             1          
  2        BLOCKED       RUN:cpu             1             1
  3        BLOCKED       RUN:cpu             1             1
  4        BLOCKED       RUN:cpu             1             1
  5        BLOCKED       RUN:cpu             1             1
  6        BLOCKED          DONE                           1
  7*   RUN:io_done          DONE             1          
```

Total time: 7; CPU utilization: 6/7 = 85.71%; I/O utilization: 5/7 = 71.43%.

- Reasoning / 理由: Swapping the order from Q2 changes everything: now the CPU-bound process (PID 1) runs while the I/O-bound process (PID 0) waits for its device. The I/O wait (ticks 2-6) is fully overlapped with PID 1's CPU work, so the CPU never idles.

## Q4
- Prediction / 预测: With SWITCH_ON_END the OS never switches while a process waits for I/O. PID 0 issues its I/O at tick 1 and is BLOCKED at ticks 2-6; PID 1 is runnable but the policy keeps it READY. After io_done (tick 7) PID 0 finishes, then PID 1 runs at ticks 8-11.

```
Time        PID: 0        PID: 1           CPU           IOs
  1         RUN:io         READY             1          
  2        BLOCKED         READY                           1
  3        BLOCKED         READY                           1
  4        BLOCKED         READY                           1
  5        BLOCKED         READY                           1
  6        BLOCKED         READY                           1
  7*   RUN:io_done         READY             1          
  8           DONE       RUN:cpu             1          
  9           DONE       RUN:cpu             1          
 10           DONE       RUN:cpu             1          
 11           DONE       RUN:cpu             1          
```

Total time: 11; CPU utilization: 6/11 = 54.55%; I/O utilization: 5/11 = 45.45%.

- Reasoning / 理由: The CPU idles for 5 ticks (2-6) even though PID 1 is READY — the switch policy forbids switching until the currently running process ends.

## Q5
- Prediction / 预测: Same workload as Q4 but with SWITCH_ON_IO, so this is exactly Q3: PID 1 runs during PID 0's I/O wait.

```
Time        PID: 0        PID: 1           CPU           IOs
  1         RUN:io         READY             1          
  2        BLOCKED       RUN:cpu             1             1
  3        BLOCKED       RUN:cpu             1             1
  4        BLOCKED       RUN:cpu             1             1
  5        BLOCKED       RUN:cpu             1             1
  6        BLOCKED          DONE                           1
  7*   RUN:io_done          DONE             1          
```

Total time: 7; CPU utilization: 6/7 = 85.71%; I/O utilization: 5/7 = 71.43%.

- Reasoning / 理由: SWITCH_ON_IO lets another process use the CPU while one is blocked, so the I/O wait is overlapped with useful work.

## Q6
- Prediction / 预测: PID 0 has 3 I/Os; PIDs 1-3 have 5 CPU instructions each. With IO_RUN_LATER, after PID 0's I/O completes at tick 7 it goes to the back of the READY queue instead of running immediately, so PID 2 and PID 3 get the CPU first (ticks 7-16). Only then does PID 0 handle io_done and issue its 2nd and 3rd I/Os — by then every other process is DONE, so the CPU idles during those I/O waits.

```
Time        PID: 0        PID: 1        PID: 2        PID: 3           CPU           IOs
  1         RUN:io         READY         READY         READY             1          
  2        BLOCKED       RUN:cpu         READY         READY             1             1
  3        BLOCKED       RUN:cpu         READY         READY             1             1
  4        BLOCKED       RUN:cpu         READY         READY             1             1
  5        BLOCKED       RUN:cpu         READY         READY             1             1
  6        BLOCKED       RUN:cpu         READY         READY             1             1
  7*         READY          DONE       RUN:cpu         READY             1          
  8          READY          DONE       RUN:cpu         READY             1          
  9          READY          DONE       RUN:cpu         READY             1          
 10          READY          DONE       RUN:cpu         READY             1          
 11          READY          DONE       RUN:cpu         READY             1          
 12          READY          DONE          DONE       RUN:cpu             1          
 13          READY          DONE          DONE       RUN:cpu             1          
 14          READY          DONE          DONE       RUN:cpu             1          
 15          READY          DONE          DONE       RUN:cpu             1          
 16          READY          DONE          DONE       RUN:cpu             1          
 17    RUN:io_done          DONE          DONE          DONE             1          
 18         RUN:io          DONE          DONE          DONE             1          
 19        BLOCKED          DONE          DONE          DONE                           1
 20        BLOCKED          DONE          DONE          DONE                           1
 21        BLOCKED          DONE          DONE          DONE                           1
 22        BLOCKED          DONE          DONE          DONE                           1
 23        BLOCKED          DONE          DONE          DONE                           1
 24*   RUN:io_done          DONE          DONE          DONE             1          
 25         RUN:io          DONE          DONE          DONE             1          
 26        BLOCKED          DONE          DONE          DONE                           1
 27        BLOCKED          DONE          DONE          DONE                           1
 28        BLOCKED          DONE          DONE          DONE                           1
 29        BLOCKED          DONE          DONE          DONE                           1
 30        BLOCKED          DONE          DONE          DONE                           1
 31*   RUN:io_done          DONE          DONE          DONE             1          
```

Total time: 31; CPU utilization: 21/31 = 67.74%; I/O utilization: 15/31 = 48.39%.

- Reasoning / 理由: Each I/O takes 7 ticks (1 issue + 5 wait + 1 done); PID 0 has 3 I/Os. IO_RUN_LATER deliberately delays the just-unblocked process, so the CPU-bound processes run first. Once they are DONE, PID 0's remaining I/Os leave the CPU idle (ticks 19-23 and 26-30). The I/O device is also idle from tick 7 to tick 17 while PIDs 2 and 3 run.

## Q7
- Prediction / 预测: Same workload, but IO_RUN_IMMEDIATE — PID 0 runs as soon as its I/O finishes (ticks 7, 14, 21) and immediately issues the next I/O, so the device is never idle between PID 0's I/Os; the CPU-bound processes fill the 5-tick wait gaps.

```
Time        PID: 0        PID: 1        PID: 2        PID: 3           CPU           IOs
  1         RUN:io         READY         READY         READY             1          
  2        BLOCKED       RUN:cpu         READY         READY             1             1
  3        BLOCKED       RUN:cpu         READY         READY             1             1
  4        BLOCKED       RUN:cpu         READY         READY             1             1
  5        BLOCKED       RUN:cpu         READY         READY             1             1
  6        BLOCKED       RUN:cpu         READY         READY             1             1
  7*   RUN:io_done          DONE         READY         READY             1          
  8         RUN:io          DONE         READY         READY             1          
  9        BLOCKED          DONE       RUN:cpu         READY             1             1
 10        BLOCKED          DONE       RUN:cpu         READY             1             1
 11        BLOCKED          DONE       RUN:cpu         READY             1             1
 12        BLOCKED          DONE       RUN:cpu         READY             1             1
 13        BLOCKED          DONE       RUN:cpu         READY             1             1
 14*   RUN:io_done          DONE          DONE         READY             1          
 15         RUN:io          DONE          DONE         READY             1          
 16        BLOCKED          DONE          DONE       RUN:cpu             1             1
 17        BLOCKED          DONE          DONE       RUN:cpu             1             1
 18        BLOCKED          DONE          DONE       RUN:cpu             1             1
 19        BLOCKED          DONE          DONE       RUN:cpu             1             1
 20        BLOCKED          DONE          DONE       RUN:cpu             1             1
 21*   RUN:io_done          DONE          DONE          DONE             1          
```

Total time: 21; CPU utilization: 21/21 = 100%; I/O utilization: 15/21 = 71.43%.

- Reasoning / 理由: IMMEDIATE keeps the I/O pipeline full: PID 0's io_done and next RUN:io happen back-to-back (ticks 7-8 and 14-15), and each 5-tick I/O wait is filled by a CPU-bound process (PID 1, then PID 2, then PID 3).

## Q8
Commands: `python3 process-run.py -s <seed> -l 3:50,3:50` with three settings each: default (SWITCH_ON_IO + IO_RUN_LATER), `-I IO_RUN_IMMEDIATE`, `-S SWITCH_ON_END`. Full traces are in q8-s1.txt / q8-s2.txt / q8-s3.txt.

### Seed 1
- Prediction / 预测: The seed fixes the instruction lists: PID 0 = CPU, IO, IO; PID 1 = CPU, CPU, CPU. Total time should be 15 for both I/O policies, because PID 1 is already DONE when PID 0's I/O finishes (nothing to reorder). With SWITCH_ON_END, PID 1 cannot run during PID 0's waits, so total time should rise to 18.

### Seed 2
- Prediction / 预测: PID 0 = IO, IO, CPU; PID 1 = CPU, IO, IO. Both processes are I/O-heavy, so whenever one process's I/O completes the other is usually BLOCKED too — the two I/O policies should give the same trace (total about 16). SWITCH_ON_END serializes every I/O, so it should be much longer (about 30).

### Seed 3
- Prediction / 预测: PID 0 = CPU, IO, CPU; PID 1 = IO, IO, CPU. Here the two I/O policies should differ: at tick 9 PID 1's I/O completes while PID 0 is READY, so IO_RUN_LATER lets PID 0 run first (total ~18), while IO_RUN_IMMEDIATE runs PID 1 right away (total ~17). SWITCH_ON_END serializes everything (total ~24).
