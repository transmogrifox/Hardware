#include <cstdlib>
#include <cstdio>

//
// Exponential decay function discretized is the following
//   y[n] = alpha * y[n-1]  (1)
//
// Consider two values in the sequence:
//   y[n-1] = e^(-(n-1)T/tau) 
//   y[n]   = e^(-nT/tau)
//
// The ratio y[n]/y[n-1] = ( e^(-nT/tau) ) /  (e^(-(n-1)T/tau) )
//                       = e^(-nT/tau) e^((n-1)T/tau)
//                       = e^(-nT/tau + nT/tau -T/tau)
//                       = e^(-T/tau)
//
// Solving above for y[n], the following is obtained
//   y[n] = y[n-1]*e^(-T/tau)  (2)
//
// Now define the following and substitute into (2) to obtain (1):
//   alpha = e^(-T/tau)
//
// -----------------------------------------------
// ONE SIMPLE FIXED POINT IMPLEMENTATION 
//    (IF LIMITATION TO POWERS OF 2 IS ACCEPTABLE)
// -----------------------------------------------
//
// (1) can be implemented in the following form
//   y[n] = (A*y[n-1] - y[n-1])/A
//
// Which for a fixed point (integer) computation is the following operation
//   y[n] = ( (y[n-1] << log2(A)) - y[n-1] ) >> log2(A)
//
// Relating "alpha" to A is obtained by the following
//   alpha = (1/A)*(A-1)
//         = (1-1/A)
//   1/A   = 1-alpha
//   A     = 1/(1-alpha)
//
// Note the proposed algorithm limits the possible values for A to powers of 2, 
// which means possible values for "alpha" are limited
//
// The value of "A" should be quantized to the nearest power of 2. If higher resolution
// is required to obtain a more exact time constant then a more complex algorithm is needed.
//


// In this example, alpha = 1 - 2^-8 will be illustrated

int main(void)
{
    unsigned int y0 = 100000;

    unsigned int tmp = 0;
    unsigned int shift = 8;
    unsigned int offset = y0&0xFFFF;
    unsigned int lsbmask = offset;
    unsigned int msbmask = ~offset;
    unsigned int linrate = 10;

    int i;

    // Data output file
    FILE * outFile;
    outFile = fopen("data.txt","w");

    // Generate output data
    fprintf(outFile,"n\ty[n]\n");
    for(i=0; i<2200; i++)
    {
        tmp = y0 << shift;
        tmp -= y0;
        y0 = (tmp>>shift);
        if(offset > 0)
            offset -= linrate;

        fprintf(outFile,"%u\t%u\n", i, y0+offset);
    }

    fclose(outFile);


    return 0;
}