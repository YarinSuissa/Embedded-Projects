#ifndef _bsp_H_
#define _bsp_H_

#include  <msp430G2553.h>     // MSP430x2xx
// #include  <msp430xG46x.h>    // MSP430x4xx

#define   debounceVal      280
#define   delay62_5ms      0xFFFF

// VECTOR abstraction
#define Timer_A_Interrupt  &TA0IV

// LEDs abstraction
#define LEDsArrPort        &P1OUT
#define LEDsArrPortDir     &P1DIR
#define LEDsArrPortSel     &P1SEL

//Timers abstraction
#define Timer_A_CTL        &TA0CTL
#define Timer_A_CC0_CTL    &TACCTL0
#define Timer_A_CC0_Reg    &TACCR0
#define Timer_A1_CTL       &TA1CTL
#define Timer_A1_CC2_CTL   &TA1CCTL2
#define Timer_A1_CC2_Reg   &TA1CCR2
#define Timer_A1_flag      &TA1IV
#define TBCLK_Port         0x10
#define TBCLK_Port_LAB     0x08

// LCD abstraction
#define LCDDataDIR         &P1DIR
#define LCDDataSEL         &P1SEL
#define LCDDataPort        &P1OUT
#define LCDCMDDIR          &P2DIR
#define LCDCMDSEL          &P2SEL
#define LCDCMDPort         &P2OUT
#define LCDRS              0x20
#define LCDRW              0x40
#define LCDE               0x80
#define LEDsArrPortSel     &P1SEL

// Switches abstraction
#define SWsArrPort         &P2IN
#define SWsArrPortDir      &P2DIR
#define SWsArrPortSel      &P2SEL
#define SWmask             0x0F

// PushButtons abstraction
#define PBsArrPort	   &P2IN 
#define PBsArrIntPend	   &P2IFG 
#define PBsArrIntEn	   &P2IE
#define PBsArrIntEdgeSel   &P2IES
#define PBsArrPortSel      &P2SEL 
#define PBsArrPortDir      &P2DIR 
#define PB0                0x01
#define PB1                0x02
//#define PB2                0x40
//#define PB3                0x80

#define gotoStates         0xC2AC

#endif



