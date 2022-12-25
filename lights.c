#include <stdio.h>
#include <unistd.h>
void lights ();
int main (void){
    lights();
}

void lights ()
{
    int a = 0;
    int b = 0;
    while (b == 0){
        sleep(3);
        if (a == 0)
        {
            printf("RED\n");
            a++;
        }
        else if (a == 1)
        {
            printf("YELLOW\n");
            a++;
        }
        else
        {
            printf("GREEN\n");
            a = 0;
        }
    }
}