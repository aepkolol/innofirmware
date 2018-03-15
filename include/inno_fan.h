/******************************************************************************
 *
 * 文件名  ：inno_fan.h
 * 负责人  ： yex(yex@innosilicon.com.cn)
 * 创建日期： 20171122
 * 版本号  ： V1.0
 * 文件描述： 风扇与温度控制接口
 * 版权说明： Copyright (c) 2000-2020   GNU
 * 其    他： 无
 * 修改日志： 无
 *
 *******************************************************************************/

/*---------------------------------- 预处理区 ---------------------------------*/
#ifndef _INNO_FAN_H_
#define _INNO_FAN_H_

/************************************ 头文件 ***********************************/
#include <stdio.h>
#include <pthread.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <stdbool.h>
#include <sys/ioctl.h>
#include <string.h>
#include <unistd.h>
#include "inno_log.h"

/************************************ 宏定义 ***********************************/
#define A7
//#define A6 0
#ifdef A7
#define ASIC_CHAIN_NUM 6
#define ASIC_CHIP_NUM 33
#endif

#define ASIC_INNO_FAN_PWM0_DEVICE_NAME  ("/dev/pwmgen0.0")

#define ASIC_INNO_FAN_PWM_STEP            (5)
#define ASIC_INNO_FAN_PWM_DUTY_MAX        (100)
#define ASIC_INNO_FAN_PWM_FREQ_TARGET     (20000)
#define ASIC_INNO_FAN_PWM_FREQ            (20000)
#define FAN_CNT                           ( 2 )
#define ASIC_INNO_FAN_TEMP_MAX_THRESHOLD  (100)
#define ASIC_INNO_FAN_TEMP_UP_THRESHOLD   (55)
#define ASIC_INNO_FAN_TEMP_DOWN_THRESHOLD (35)
#define ERR_HIGH_TEMP                     (400)
#define ERR_LOW_TEMP                      (655)
#define FAN_FIRST_STAGE                   (535)//40
#define FAN_SECOND_STAGE                  (520)//50
#define FAN_THIRD_STAGE                   (505)//60
#define FAN_FOUR_STAGE                    (498)//65
#define FAN_FIVE_STAGE                    (490)//70
#define FAN_SIX_STAGE                     (483)//75
#define FAN_SEVEN_STAGE                   (475)//80
#define FAN_EIGHT_STAGE                   (468)//85

#define FAN_DELTA1                        (10)//6
#define FAN_DELTA2                        (5) //3
#define TEMP_LABEL                        (594)
#define ACTIVE_STAT                       (6)
#define START_FAN_TH                      (550)//30
#define PREHEAT_SPEED                     (0)
#define DANGEROUS_TMP                     (460)//90
#define PRE_DGR_TEMP                      (456)//92.x
#define DEFAULT_HI_TEMP                   (652) //-40
#define MAGIC_NUM                         (100)

#define IOCTL_SET_FREQ(X) _IOR(MAGIC_NUM, (2*X), char *)
#define IOCTL_SET_DUTY(X) _IOR(MAGIC_NUM, (2*X+1), char *)

#define ASIC_CHIP_A_BUCKET              (ASIC_CHAIN_NUM * ASIC_CHIP_NUM)
#define ASIC_INNO_FAN_TEMP_MARGIN_RATE  (5.0f / 100.0f)
#define ASIC_INNO_FAN_CTLR_FREQ_DIV     (0)

/*********************************** 类型定义 **********************************/

/*--------------------------------- 接口声明区 --------------------------------*/

/*********************************** 全局变量 **********************************/
typedef struct {
    int temp[ASIC_CHAIN_NUM][ASIC_CHIP_NUM];    /* 用于存放所有链上的芯片温度*/
    int valid_chain[ASIC_CHAIN_NUM];           //用于判断该chain是否有效
    int index[ASIC_CHAIN_NUM];                  /*对应链上的chip_id */

    int speed;                              /* 0 - 100用于设置风扇转速(可能32档) */
    int last_fan_speed;
    int auto_ctrl;
    int pre_warn[4];

    int temp_arvarge[ASIC_CHAIN_NUM];          /*对应链上的平均温度*/
    int temp_highest[ASIC_CHAIN_NUM];            /*对应链上的最高温度*/
    int temp_lowest[ASIC_CHAIN_NUM];             /*对应链上的最低温度*/
    float temp2float[ASIC_CHAIN_NUM][3];         /*[][0]->highest,[][1]->avg, [][2]->lowest*/
    int last_fan_temp;
    pthread_mutex_t lock;                       /* lock */

}inno_fan_temp_s;

typedef enum{
    INNO_TYPE_NONE = 0x00,
    INNO_TYPE_A4,
    INNO_TYPE_A5,
    INNO_TYPE_A6,
    INNO_TYPE_A7,
    INNO_TYPE_A8,
    INNO_TYPE_A9,
}inno_type_e;

/*********************************** 接口函数 **********************************/
void inno_fan_temp_init(inno_fan_temp_s *fan_temp,int *fan_level);   /*主要用于Ax系列初始化风扇控制与温度显示*/
bool inno_fan_temp_add(inno_fan_temp_s *fan_temp,int chain_id, int chip_id, int temp); /*用于实时更新统计到的当前温度值，异常记录*/
void asic_temp_sort(inno_fan_temp_s *fan_temp, int chain_id);   /*对单条链统计到的所有温度做一次升序排列*/
int inno_fan_temp_highest(inno_fan_temp_s *fan_temp, int chain_id, inno_type_e inno_type); /*提供当前链统计到的实时最高温度(chip_type)*/
int inno_fan_temp_lowest(inno_fan_temp_s *fan_temp, int chain_id, inno_type_e inno_type); /*提供当前链统计到的实时最低温（chip_type）*/
int inno_fan_temp_avg(inno_fan_temp_s *fan_temp, int chain_id, inno_type_e inno_type); /*提供当前链所有芯片统计的实时平均温度*/
//void inno_fan_temp_update(inno_fan_temp_s *fan_temp,int chain_id, inno_type_e inno_type, int *fan_level);  /*用于更新风扇转速与温度显示数据*/
void inno_fan_speed_update(inno_fan_temp_s *fan_temp);
void chain_temp_update(inno_fan_temp_s *fan_temp,int chain_id,inno_type_e inno_type);
void inno_fan_speed_set(inno_fan_temp_s *fan_temp, int speed);  /*设置风扇转速 */

#endif // #ifndef _INNO_FAN_TEMP_H_
