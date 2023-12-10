#include <cstdlib>
#include <cstdio>

//
// For theory of implementation, see comments in "expo_decay.c" 
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
    outFile = fopen("data_expo_lin.txt","w");

    // Generate output data
    fprintf(outFile,"n\ty[n]\tINTEG(y[n])\n");
    for(i=0; i<5000; i++)
    {
        //Switch between exponential decay vs linear rate based on count of
        //cycles since it began holdover
        //The value of "transition" is computed from the number of cycles at which 
        //y[n-1] - y[n] == linrate
        //In this example the value was simply guessed and adjusted graphically
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