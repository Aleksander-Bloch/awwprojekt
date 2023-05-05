#include <stdio.h>
#pragma GCC diagnostic ignored "-Wunused-variable"

inline bool acquireLock(int *lock){
    char str[80*25];
  bool returnvalue = false;
  int *lockval;
  asm  (       /*------a fence here------*/

               :     "+r"   (lockval),
                     "+r"   (returnvalue)
               :     "r"    (lock)       // "lock" is the address of the lock in
                                         // memory.

               :     "cr0"               // cr0 is clobbered by cmpwi and stwcx.
               );

  return returnvalue;
}
int main()
{
  int myLock;
  if(acquireLock(&myLock)){
       printf("got it!\n");
  }else{
       printf("someone else got it\n");
  }
  return 0;
}