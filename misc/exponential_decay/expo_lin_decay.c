#include <cstdlib>
#include <cstdio>

//
// For theory of decaying exponential implementation, see comments in "expo_decay.c" 
//

//
// To solve for "N" at transition where slope of decaying exponential equals slope of 
// straight line,
// N = (-tau/T)*ln(-m*tau/y)                                                       (1)
//   
//   T = sampling period
//   tau = -T/ln((A-1)/A)
//   m = slope of straight line after transition
//   y = initial condition for exponential component at time t = 0 (n=0)
//

// In this example, 
//    alpha = 1 - 2^-8  (A = 256)
//    T = 2
//    m = -100/A = 0.391
//    tau = 2*255.5  (factor of 2 because it's operated at 2T)
//    y = 10000 - 1000 = 9000 (initial value minus settled value)
//
//    N = -(511/2)*ln(-(-100/256)*511/9000) = 973
// Since the exponential is operated every other "tick", the total ticks to
// reach "transition" will be 2*N
//    transition = 2*973 = 1946
//
// Note a more direct computation of "transition" from (1) is to assume T=1, but tau is doubled
// since the filter is ticked every other sample,
//   transition = (-2*tau)*ln(-m*2*tau/y) = 2*255.5*ln(-100*2*255.5/9000) = 1946

int main(void)
{
    unsigned int shift = 8;
    unsigned int ya = 10000;
    unsigned int y0 = ya << shift;

    unsigned int tmp = 0;

    // Constant offset value
    unsigned int offst = 1000;
    unsigned int linrate = 100;
    unsigned int transition = 1946;

    // Integral of y[n], proportional to accumulated timing offset
    unsigned int runsum = 0;

    int i;

    // Data output file
    FILE * outFile;
    outFile = fopen("data_expo_lin.txt","w");

    // Generate output data
    fprintf(outFile,"n\ty[n]\tINTEG(y[n])\n");
    for(i=0; i<5000; i++)
    {
        //Switch between exponential decay vs linear rate based on count of
        //cycles since it began holdover
        //The value of "transition" is computed from the number of cycles at which 
        //y[n-1] - y[n] == linrate (derivative of exponential matches slope of line)
        if(i<transition)
        {
            //Multiplex either shifted value or a constant every other clock cycle
            //  The purpose is to realize a first order IIR that settles to a constant offset value,
            //   e.g. y[n] = beta*x[n] + alpha*y[n-1]
            //   where beta*x[n] <-- pre-computed constant in which 
            //     --"x" is the constant offset where you want the filter to settle
            //     --"beta" is (1-alpha)
            //     ** Note since the first and second term are accumulated every other clock cycle,
            //        the sampling period "T" used to compute "alpha" should be 2/CLOCK_FREQ 
            //  This interleaved approach avoids allows the accumulator to use a 2-input adder
            //  It is presumed a MUX and toggle flip flop needed to select between the two inputs, 
            //  constant "beta*x[n]" or (y[n-1] >> shift),
            //  is not going to be an unmanageable fabric and/or timing expense.

            //Even cycle
            if(i%2)
                y0 -= y0 >> shift;  //Decaying exponential function
            //Odd cycle
            else
                y0 += offst;  //Accumulate IIR filter input
        }
        else
        {
            y0 -= linrate;
        }

        runsum += (y0>>shift);
        fprintf(outFile,"%u\t%u\t%u\n", i, y0>>shift, runsum>>shift);
    }

    fclose(outFile);


    return 0;
}