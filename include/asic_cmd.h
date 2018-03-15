#ifndef _ASIC_CMD_
#define _ASIC_CMD_

typedef struct ASIC_CHAIN_TAG{
    int no;
    ZYNQ_SPI_T *spi;
}ASIC_CHAIN_T;


typedef struct ASIC_CMD_TAG{
    //
    bool (*asic_cmd_reset)(ASIC_CHAIN_T *, unsigned char, unsigned char *, int);    
    //
    bool (*asic_cmd_bist_start)(ASIC_CHAIN_T *, unsigned char, int *);    
    //
    bool (*asic_cmd_bist_collect)(ASIC_CHAIN_T *, unsigned char);    
    //
    bool (*asic_cmd_bist_fix)(ASIC_CHAIN_T *, unsigned char);
    //    
    bool (*asic_cmd_write_register)(ASIC_CHAIN_T *, unsigned char, unsigned char *, int);
    //    
    bool (*asic_cmd_read_register)(ASIC_CHAIN_T *, unsigned char, unsigned char *, int);
    //    
    bool (*asic_cmd_read_result)(ASIC_CHAIN_T *, unsigned char, unsigned char *, int);
    //    
    bool (*asic_cmd_write_job)(ASIC_CHAIN_T *, unsigned char *, int);
}ASIC_CMD_T;


unsigned short CRC16_2(unsigned char* pchMsg, unsigned short wDataLen);

void init_asic_cmd(void);

void register_asic_cmd(ASIC_CMD_T * cmd_ops_p);

bool asic_cmd_reset(ASIC_CHAIN_T *chain, unsigned char chip_id, unsigned char *buff, int len);

bool asic_cmd_bist_start(ASIC_CHAIN_T *chain, unsigned char chip_id, int *num);

bool asic_cmd_bist_collect(ASIC_CHAIN_T *chain, unsigned char chip_id);

bool asic_cmd_bist_fix(ASIC_CHAIN_T *chain, unsigned char chip_id);

bool asic_cmd_write_register(ASIC_CHAIN_T *chain, unsigned char chip_id, unsigned char *reg, int len);

bool asic_cmd_read_register(ASIC_CHAIN_T *chain, unsigned char chip_id, unsigned char *reg, int len);

bool asic_cmd_read_result(ASIC_CHAIN_T *chain, unsigned char chip_id, unsigned char *res, int len);

bool asic_cmd_write_job(ASIC_CHAIN_T *chain, unsigned char *job, int len);



#endif
