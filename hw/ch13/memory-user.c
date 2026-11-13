#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
int main(int argc, char *argv[]) {
    if (argc < 2) { fprintf(stderr, "Usage: %s <MB>\n", argv[0]); return 1; }
    int mb = atoi(argv[1]);
    char *p = (char *)malloc(mb * 1024 * 1024);
    if (!p) { perror("malloc"); return 1; }
    for (size_t i = 0; i < (size_t)mb * 1024 * 1024; i += 4096) p[i] = 0;
    printf("Allocated %d MB at %p — PID %d\n", mb, (void *)p, getpid());
    pause();
    return 0;
}
