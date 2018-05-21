#include<stdio.h>
int main(){
  /*error  */
  int score[5] = {0, 10, 20, 30, 40};
  int sum,mean;
  sum=0;
  mean=0;

  for( i = 0; i < 5; i++)
  {
  sum = sum + score[i];
  }

  mean = sum /5;
  printf(" %d \n", mean);
  return 0;
}
