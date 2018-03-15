#ifndef _SPI_CMD_
#define _SPI_CMD_

bool spi_cmd_reset(ASIC_CHAIN_T *chain, unsigned char chip_id, unsigned char *buff, int len);

bool spi_cmd_bist_start(ASIC_CHAIN_T *chain, unsigned char chip_id, int *num);

bool spi_cmd_bist_collect(ASIC_CHAIN_T *chain, unsigned char chip_id);

bool spi_cmd_bist_fix(ASIC_CHAIN_T *chain, unsigned char chip_id);

bool spi_cmd_write_register(ASIC_CHAIN_T *chain, unsigned char chip_id, unsigned char *reg, int len);

bool spi_cmd_read_register(ASIC_CHAIN_T *chain, unsigned char chip_id, unsigned char *reg, int len);

bool spi_cmd_read_result(ASIC_CHAIN_T *chain, unsigned char chip_id, unsigned char *res, int len);

bool spi_cmd_write_job(ASIC_CHAIN_T *chain, unsigned char *job, int len);


#endif
