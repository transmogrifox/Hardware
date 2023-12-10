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
// If the decimal point is interpreted at the correct location, the entire operation can be
// simplified to the folowing:
//   y[n] = y0[n-1] - (1/A)y0[n-1]
// In this case "1/A" is evaluated by shifting the previous value and subtracting it from 
// the accumulator.
//   y[n] = y[n-1] - (y0[n-1] >> log2(A))
// Hence if "y0" represents the accumulator,
//   y0 -= y0>>log2(A)
//
// Relating "alpha" to A is obtained by the following
//   alpha = (1/A)*(A-1)
//         = (1-1/A)
//   1/A   = 1-alpha
//   A     = 1/(1-alpha)
//
// Then, recalling alpha = e^(-T/tau)
//   A = 1/(1 - e^(-T/tau))
// or if wanting to work backwards from a pre-determined value of "A"
//   tau = -T/ln( (A-1)/A )
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
    unsigned int shift = 8;
    unsigned int y0 = 10000 << shift;

    unsigned int tmp = 0;

    // Constant offset value
    unsigned int offst = 1000;
    unsigned int linrate = 100;
    unsigned int transition = 1800;

    // Integral of y[n], proportional to accumulated timing offset
    unsigned int runsum = 0;

    int i;

    // Data output file
    FILE * outFile;
    outFile = fopen("data_expo.txt","w");

    // Generate output data
    fprintf(outFile,"n\ty[n]\tINTEG(y[n])\n");
    for(i=0; i<1500; i++)
    {
        y0 -= y0 >> shift;
        runsum += (y0>>shift);
        fprintf(outFile,"%u\t%u\t%u\n", i, y0>>shift, runsum>>shift);
    }

    fclose(outFile);


    return 0;
}