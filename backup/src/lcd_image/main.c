/* Copyright 2018 Canaan Inc.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

#include "unistd.h"
#include "board_config.h"
#include "bsp.h"
#include "dvp.h"
#include "fpioa.h"
#include "gpiohs.h"
#include "image_process.h"
#include "kpu.h"
#include "lcd.h"
#include "nt35310.h"
#include "ov2640.h"
#include "ov5640.h"
#include "plic.h"
#include "region_layer.h"
#include "sysctl.h"
#include "uarths.h"
#include "utils.h"
#include "w25qxx.h"
#include <aiimg.h>
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include "image.h"

#define INCBIN_STYLE INCBIN_STYLE_SNAKE
#define INCBIN_PREFIX
#include "incbin.h"

#define PLL0_OUTPUT_FREQ 800000000UL
#define PLL1_OUTPUT_FREQ 400000000UL

#define CLASS_NUMBER 20

volatile uint32_t g_ai_done_flag;
volatile uint8_t g_dvp_finish_flag;

// static image_t kpu_image, display_image;
static uint16_t lcd_gram[320 * 224] __attribute__((aligned(32)));

kpu_model_context_t face_detect_task;
static region_layer_t detect_rl0, detect_rl1;
static obj_info_t face_detect_info;
#define ANCHOR_NUM 3
// NOTE x,y

static float layer0_anchor[ANCHOR_NUM * 2]= {
    0.76120044, 0.57155991, 0.6923348, 0.88535553, 0.47163042, 0.34163313,
};

static float layer1_anchor[ANCHOR_NUM * 2]= {
    0.33340788, 0.70065861, 0.18124964, 0.38986752, 0.08497349, 0.1527057,
};

static void io_set_power(void)
{
#if BOARD_LICHEEDAN
    sysctl_set_power_mode(SYSCTL_POWER_BANK6, SYSCTL_POWER_V18);
    sysctl_set_power_mode(SYSCTL_POWER_BANK7, SYSCTL_POWER_V18);
#else
    sysctl_set_power_mode(SYSCTL_POWER_BANK1, SYSCTL_POWER_V18);
#endif
}

static void io_mux_init(void)
{
#if BOARD_LICHEEDAN
    fpioa_set_function(38, FUNC_GPIOHS0 + DCX_GPIONUM);
    fpioa_set_function(36, FUNC_SPI0_SS3);
    fpioa_set_function(39, FUNC_SPI0_SCLK);
    fpioa_set_function(37, FUNC_GPIOHS0 + RST_GPIONUM);
    sysctl_set_spi0_dvp_data(1);
#else
    fpioa_set_function(8, FUNC_GPIOHS0 + DCX_GPIONUM);
    fpioa_set_function(6, FUNC_SPI0_SS3);
    fpioa_set_function(7, FUNC_SPI0_SCLK);
    sysctl_set_spi0_dvp_data(1);
#endif
}

int main(void)
{
    printf("lcd test\n");
    io_mux_init();
    io_set_power();
    lcd_init();
#if BOARD_LICHEEDAN
    lcd_set_direction(DIR_YX_RLDU);     /* left up 0,0 */
#else
    lcd_set_direction(DIR_YX_RLUD);     /* left up 0,0 */
#endif
    while(1)
    {
        lcd_draw_picture(0, 0, 320, 240, rgb_image);
        usleep(1000000);
        printf("show pic\n");
    }
    while (1);
}
