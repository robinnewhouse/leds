//
// Created by Lilli Szafranski on 2/28/16.
//

#ifndef DODEC_C_PRODUCER_SERIAL_H
#define DODEC_C_PRODUCER_SERIAL_H

/* Returning -1 is bad I think */
int	write_data(int fileDescriptor, const void *data, size_t size);
int	read_data(int fileDescriptor, void *data, size_t size);

/* Returning -1 is bad I think */
int new_serial_device(const char *devName);

#endif //DODEC_C_PRODUCER_SERIAL_H
