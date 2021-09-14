// SCL v 1.0 File: bitops1.c, Sun Apr 22 11:49:01 2018
 
/* Program: bitops1.scl
   Test the Sysplm with several bitwise operations
   J Garrido March 2017.
*/    
#include "sysplm.h" 
#define MM 0x066 
 // 0110 0110 
#define MN 0x0B3 
 // 1011 0011 
// global declarations 
unsigned int  a; 
 unsigned short  b; 
 unsigned long  c; 
 /** 
  description
      This is the main function of the application.
      */
 int main( ) {
byte  vara; 
 byte  varb; 
 byte  varc1; 
 byte  varc2; 
 byte  varc3; 
 byte  varc4; 
 byte  d1; 
 byte  d2; 
 vara = MM;
 // 0110 0110 
varb = MN;
 // 1011 0011 
varc1 = (vara) & (varb);
varc2 = (vara) | (varb);
varc3 = (vara) ^ (varb);
varc4 =  ~ (vara);
 // 
 printf(" %04X    %04X    %04X    %04X\n",varc1, varc2, varc3, varc4);
 // Using a mask to select or alter bits 
varc1 = (vara) & (0x0FE);
 // clear bit 0 (lowest bit) 
varc2 = (vara) & (0x01);
 // clear all except bit 0 
varc3 = (vara) | (0x01);
 // set bit 0 
varc4 = (vara) ^ (0x01);
 // complement bit 0 
 printf(" %04X    %04X    %04X    %04X\n",varc1, varc2, varc3, varc4);
d1 = ( (vara) << (3)) ;
d2 = ( (varb) >> (2)) ;
 printf("d1:   %04X  d2:   %04X\n",d1, d2);
 // 
a = d1;
 // move d1 to (low byte) of a 
 printf("a:   %d\n",a);
a = (a) << (8);
 // shift to high byte of a 
 printf("a:   %d\n",a);
a = (a) | (d2);
 // copy d2 to low byte of a 
 printf("a:   %d\n",a);
 return 0; 
 }  // end function main 
