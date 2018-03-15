#ifndef _INNO_SPI_
#define _INNO_SPI_


void spi_send_data(ZYNQ_SPI_T *spi, unsigned char *buf, int len);

void spi_recv_data(ZYNQ_SPI_T *spi, unsigned char *buf, int len);

void spi_send_data_in_word(ZYNQ_SPI_T *spi, unsigned char *buf, int len);

void spi_recv_data_in_word(ZYNQ_SPI_T *spi, unsigned char *buf, int len);

bool spi_send_command(ZYNQ_SPI_T *spi, unsigned char cmd, unsigned char chip_id, unsigned char *buff, int len);

bool spi_poll_result(ZYNQ_SPI_T *spi, unsigned char cmd, unsigned char chip_id, unsigned char *buff, int len);



#endif
