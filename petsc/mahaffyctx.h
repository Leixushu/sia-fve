/* (C) 2015 Ed Bueler */

#ifndef MAHAFFYCTX_H_   /* Include guard */
#define MAHAFFYCTX_H_

#include <sys/time.h>
#include <petscdmda.h>
#include <petscvec.h>

typedef struct {
  DM        da, quadda;
  Vec       b,      // the bed elevation
            m,      // the (steady) surface mass balance
            Hexact; // the exact thickness (either in verification or data sense)
  PetscReal dx,     // fixed grid spacing; dx = dy
            Lx,     // domain is [-Lx,Lx] x [-Ly,Ly]
            Ly,
            n,      // Glen exponent for SIA flux term
            g,      // acceleration of gravity
            rho,    // ice density
            secpera,// number of seconds in a year
            A,      // ice softness
            Gamma,  // coefficient for SIA flux term
            eps,    // dimensionless regularization
            maxD,   // local value maximum of diffusivity, in m^2 s^-1; used for reporting
            D0;     // representative value of diffusivity (in regularization)
  PetscInt  Nx,     // grid has Nx x Ny nodes
            Ny,
            Neps;   // number of levels in regularization/continuation
  PetscBool mtrue,  // use true Mahaffy method instead of M*
            noupwind,// do not upwind "W H^{n+2}" term in flux formula  q = - D grad H + W H^{n+2}
            upwindfull,// when upwinding "W H^{n+2}" term, go all the way to element edge
            read,   // read grid and data from special-format PETSc binary file
            dome,   // use dome exact solution ("Bueler profile")
            bedstep,// use bedrock step exact solution from Jarosch, Schoof, Anslow (2013)
            swapxy, // swap x and y axes in building exact solution
            showdata,// show b and m with X viewer
            checkadmissible,// in FormFunctionLocal(), stop if H < 0.0
            forceadmissible,// in FormFunctionLocal(), set H = abs(H)
            divergetryagain,// on SNES diverge, try again with eps *= 1.5
            dump,   // dump fields into individual PETSc binary files
            history;// write ASCII history file
  char      figsprefix[512],
            readname[512];
  struct timeval starttime,
                 endtime;
} AppCtx;

#endif // MAHAFFYCTX_H_