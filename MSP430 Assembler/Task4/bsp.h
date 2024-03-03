#ifndef _bsp_H_
#define _bsp_H_

#include <msp430g2553.h>

#define DebounceValUp   280//NOT 1 RIGHT AMOUNT TO REACH 0.8MS
#define DebounceValDown 70//NOT 2 RIGHT AMOUNT TO REACH 0.2MS
#define delayXms

#define PBsSEL     &P2SEL
#define PBsDIR     &P2DIR
#define PBsINPUT   &P2IN
#define PBsPEND    &P2IFG
#define PBsENABLE  &P2IE
#define PBsEDGE    &P2IES
#define PBsOUT     &P2OUT

#define LedsSEL       &P1SEL
#define LedsDIR       &P1DIR
#define LedsOUT       &P1OUT

#endif