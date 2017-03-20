//
// Created by Lilli Szafranski on 2/28/16.
//

#include <sys/types.h>
#include <stdio.h>
#include <sys/fcntl.h>
#include <sys/termios.h>
#include <unistd.h>
#include "Serial.h"
#include "Globals.h"

/* Returning -1 is bad I think */
int	write_data(int fileDescriptor, const void *data, size_t size)
{
#ifdef REALLY_WRITING
//    static long printCounter = 0;
//    printf(".");
//    if (printCounter++ % 150 == 0)
//        printf("\n");

    int n;
    n = (int) write(fileDescriptor, data, size);

    if (n != size) printf("\nWEIRD!!\n");

    return n;
#else
    return (int)size;
#endif
}


/* Returning -1 is bad I think */
int	read_data(int fileDescriptor, void *data, size_t size)
{
#ifdef REALLY_WRITING

    int n;
    n = (int) read(fileDescriptor, data, size);

    if (n != size) printf("\nWEIRD!!\n");

    return n;
#else
    return (int)size;
#endif
}

/* Returning -1 is bad I think */
int new_serial_device(const char *devName)
{
#ifdef REALLY_WRITING
    int fd=-1;
    struct termios term;

    printf("new_serial_device: %s\n", devName);
    fd = open(devName, O_RDWR);
    if (fd < 0) return fd;
    if (tcgetattr(fd, &term) < 0) {
        printf("unable to get terminal settings");
        goto fail;
    }
    cfmakeraw(&term);
    if (tcsetattr(fd, TCSANOW, &term) < 0) {
        printf("unable to set terminal settings");
        goto fail;
    }

    return fd;

    fail:
    printf("not recognized\n");
    if (fd > 0) close(fd);
    return -1;
#else
    return 1;
#endif
}
