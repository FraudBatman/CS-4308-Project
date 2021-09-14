// SCL v 1.0 File: welcome.c, Thu Apr 19 09:43:17 2018
 
/*
 Program     : welcome.scl
 Author      : J M Garrido, November 17, 2016.
 Description : Display welcome message on the screen
    and the value of variable x.
 */
#include "scl.h" 
 int main( ) {
double  x; 
  // a variable declaration  
double  t; 
  // time of the second event 
double  *  pt; 
  printf("Welcome to the world of SCL \n");
x = 45.95;
 // assigns a value to variable x  
 printf("Value of x:   %lf\n",x);
 printf("type value of t: ");
 scanf(" %lf", &t);
 printf("The value of t is:   %lf\n",t);
 if ( x >= t) { 
 printf(" %lf\n",t);
 }
 else {
 printf(" %lf\n",x);
 } // endif 
 if (  ! (x >= t)) { 
 printf(" %lf\n",x);
 } // endif 
return 0; 
 // execution terminates OK  
 }  // end function main 
