/******************************************************************************
 *
 * 文件名  ： inno_ax.h
 * 负责人  ： 彭鹏(pengp@innosilicon.com.cn)
 * 创建日期： 20171212
 * 版本号  ： v1.0
 * 文件描述： Innosilicon Ax系列芯片接口
 * 版权说明： Copyright (c) 2000-2020 Innosilicon
 * 其    他： 无
 * 修改日志： 无
 *
 *******************************************************************************/
/*---------------------------------- 预处理区 ---------------------------------*/
#ifndef _INNO_AX_H_
#define _INNO_AX_H_

/************************************ 头文件 ***********************************/
#include <stdint.h>
#include <stdbool.h>

/* TODO:将不同的平台驱动使用inno_drv屏蔽 */
#include "zynq_spi.h"

/************************************ 宏定义 ***********************************/
#define INNO_AX_REG_LEN                           (12)
#define INNO_AX_CMD_HL                            (2)
#define INNO_AX_CMD_BIST_START                    (0x01)
#define INNO_AX_CMD_BIST_FIX                      (0x03)
#define INNO_AX_CMD_RESET                         (0x04)
#define INNO_AX_CMD_RESET_DL                      (4)
#define INNO_AX_CMD_RESET_TL                      (INNO_AX_CMD_HL + INNO_AX_CMD_RESET_DL)
#define INNO_AX_CMD_READ_RESULT                   (0x08)
#define INNO_AX_CMD_WRITE_REG                     (0x09)
#define INNO_AX_CMD_WRITE_REG_DL                  (16)
#define INNO_AX_CMD_READ_REG                      (0x0A)
#define INNO_AX_CMD_BIST_COLLECT                  (0x0B)
#define INNO_AX_CMD_TVPLL                         (0x0D)
#define INNO_AX_CMD_TVPLL_DL                      (16)
/* 单job A6/A7 */
#define INNO_AX_CMD_WRITE_JOB_S                   (0x07)
/* 多job A5 */
#define INNO_AX_CMD_WRITE_JOB_M                   (0x0C)
/* 广播地址 */
#define INNO_AX_CMD_ADDR_BROADCAST                (0x00)
/*
 * T1: A5
 * T2: A6
 * T3: A7
 * T4: A8
 * */
#define INNO_AX_TYPE_T1                           (1)
#define INNO_AX_TYPE_T2                           (2)
#define INNO_AX_TYPE_T3                           (3)
#define INNO_AX_TYPE_T4                           (4)
#define INNO_AX_TYPE_ERR                          (-1)

/*********************************** 类型定义 **********************************/
typedef struct INNO_AX_TAG {
    ZYNQ_SPI_T     *spi;                            /* 表示芯片所在链的spi */
    int             chip_id;                        /* 表示该芯片在链中的位置 */
    bool            valid;                          /* 表示该芯片是否有效 */
    uint8_t         reg[INNO_AX_REG_LEN];           /* 寄存器原始值 */

#if 0
    IM_AX_PLL_T     pll;                            /* 芯片pll设置 */

    /* 以下内容与Ax芯片手册寄存器描述表对应 */
    uint8_t         pll_prediv;                     /* bits[4:0] 有效 */
    uint32_t        pll_fbdiv;                      /* bits[8:0] 有效 */
    uint8_t         reserved_79_77;                 /* bits[2:0] 必须恒为3'b010 */
    uint8_t         pll_pd;                         /* bits[0]   有效 */
    uint8_t         reserved_75_73;                 /* bits[2:0] 必须恒为3'b000 */
    uint8_t         pll_lock;                       /* bits[0]   有效 */
    uint8_t         pll_postdiv;                    /* bits[1:0] 有效 */
    uint32_t        reserved_69_56;                 /* bits[13:0]必须恒为14'b00_0010_0000 */

    uint8_t         sensor_digital_reset;           /* bits[0]   有效 */
    uint8_t         sensor_analog_power_down;       /* bits[0]   有效 */
    uint8_t         sensor_enable;                  /* bits[0]   有效 */
    uint32_t        sensor_val;                     /* bits[9:0] 有效 */

    uint8_t         output_io_strength_control;     /* bits[1:0] 有效 */
    uint8_t         reserved_21_20;                 /* bits[1:0] 必须恒为2'b10 */
    uint8_t         spi_divider;                    /* bits[1:0] 有效 */
    uint8_t         backup_full_flag;               /* bits[0]   有效 */
    uint8_t         busy_flag;                      /* bits[0]   有效 */
    uint8_t         backup_job_id;                  /* bits[3:0] 有效 */
    uint8_t         active_job_id;                  /* bits[3:0] 有效 */
    uint8_t         good_cores_count;               /* bits[7:0] 有效 */
#endif
}INNO_AX_T;

/*--------------------------------- 接口声明区 --------------------------------*/

/*********************************** 全局变量 **********************************/

/*********************************** 接口函数 **********************************/
/*******************************************************************************
 *
 * 函数名  : inno_ax_init
 * 描述    : 初始化ax芯片
 * 输入参数: ax      - 芯片指针
 *           spi     - 芯片所在链spi指针
 *           chip_id - 芯片编号(地址)
 * 输出参数: 无
 * 返回值:   无
 * 调用关系: 无
 * 其 它:    无
 *
 ******************************************************************************/
void inno_ax_init(INNO_AX_T *ax, ZYNQ_SPI_T *spi, int chip_id);

/*******************************************************************************
 *
 * 函数名  : inno_ax_cmd_reset_broadcast
 * 描述    : 给整条链的芯片发送复位命令
 * 输入参数: spi     - 链的spi指针
 *           buf     - 复位数据缓存
 *           len     - buf长度(Bytes)
 *           chip_num- 该链芯片总数
 * 输出参数: 无
 * 返回值:   true  - 复位成功
 *           false - 复位失败
 * 调用关系: 无
 * 其 它:    无
 *
 ******************************************************************************/
bool inno_ax_cmd_reset_broadcast(ZYNQ_SPI_T *spi, uint8_t *buf, int len, int chip_num);

/*******************************************************************************
 *
 * 函数名  : inno_ax_exit
 * 描述    : 反初始化芯片
 * 输入参数: ax - 芯片指针
 * 输出参数: 无
 * 返回值:   无
 * 调用关系: 无
 * 其 它:    无
 *
 ******************************************************************************/
void inno_ax_exit(INNO_AX_T *ax);

#endif // #ifndef _INNO_AX_H_

