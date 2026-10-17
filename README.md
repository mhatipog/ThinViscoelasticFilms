# Code for Thin Viscoelastic Film simulations on flat substrates

This repository contains a Fortran 90 code for the numerical simulations of thin viscoelastic films and drops on solid, flat substrates. The nomenclature used in the code, reflects the reference paper 
[Barra et al., *Interfacial dynamics of thin viscoelastic films and drops*, JNNFM (2016)](http://dx.doi.org/10.1016/j.jnnfm.2016.10.001). 
All terms and nomenclature in the code refer to that publication. Please ask the author if you cannot access the reference paper.

This code is based on the finite difference discretization, on a staggered grid. 
It uses a fixed spatial grid size Delta x and an adaptive time step Delta t.

This code solves the thin film (or long wave) approximation of thin viscoelastic films 
on a solid, flat substrate subject to the van der Waals interaction force, in two spatial dimensions. 
The governing equations are obtained within a long-wave (lubrication) approximation of the Navier–Stokes equations 
with Jeffreys model for viscoelastic stresses. This version of the code does not include any gravitational effects. 

The implementation provided is suitable for CPUs in serial mode. 

## Build

To build the prject, move into the [build](./build/) folder by running 

`cd build`

and then either run the provided compile script, by running

`bash CompileScript`

or simply build with 

`make all`

Run the executable from the repository root (so relative output paths resolve correctly):

```sh
cd ..
mkdir -p output
./build/ThinVEFilm
```

The `output/` directory is relative to the current working directory. You can change `folder` in `paras.f90` before compiling if you want a different location.

## Output

Output files are written to the `output/` directory when the program is launched from the repository root, as shown above. The path is set by `folder` in [`paras.f90`](./paras.f90). Create the directory before running. The `status.dat` file summarizes the parameters used for the simulation and monitors the adaptive time stepping and Newton's convergence in time. The state variable of the thin film equation is the thickness of the film relative to the solid substrate, printed in the file `thickness.dat`, for all contiguous grid points, for all consecutive time steps. The file `thickness.dat` gets printed at each selected output in append mode (i.e., never overwritten). On the other hand, there exist another output file for the solution, called `resLastOut.dat` that at every step gets overwritten to store the solution at the last output, with more significant digits of precision. This has been implemented so that we can checkpoint the solution and continue the simulation later with an existing solution. In the case of the consitnuation of an existing simulation, use `init_switch=1` in the [`paras.f90`](./paras.f90) file and make sure that `output/resLastOut.dat` exists (when launching from the repository root).

## Numerical smoke test

On a system with `gfortran`, `make`, and Python 3, run `python3 tests/check_linear_growth.py`. This builds a temporary copy of the original Newtonian configuration with a shorter run time and checks the linear instability growth rate against theory. No third-party Python packages are needed; production parameters are unchanged.

## Contributors
Different contributors during the years have worked on different parts of this code. We acknowledge:

* Te-Sheng Lin

* Nebo Murisic

* Ensela Mema

* Kyle Mahady [@kmahady on GitHub](https://github.com/kmahady)

* Ivana Seric [@ivanaseric on GitHub](https://github.com/ivanaseric)

* Michael Lam [@mayhl on GitHub](https://github.com/mayhl/)

* Valeria Barra [@valeriabarra on GitHub](https://github.com/valeriabarra)

* Ryan Allaire

all supervised or co-supervised by Prof. Lou Kondic, 
from the Department of Mathematical Sciences, at the New Jersey Institute of Technology.

Users and contributors are always welcome.

## Citing this project

If you use any component of this code, please cite the following

- Codebase: 
  ```
  @software{TFVCode,
    author       = {Valeria Barra},
    title        = {valeriabarra/ThinViscoelasticFilms: v0.1},
    month        = dec,
    year         = 2019,
    publisher    = {Zenodo},
    version      = {v0.1},
    doi          = {10.5281/zenodo.3561225},
    url          = {https://doi.org/10.5281/zenodo.3561225}
  }
  ```

- Publications:
  * [J.A. Diez, L. Kondic, *Computing three-dimensional thin film flows including contact lines*, J. Comput. Phys. 183 (2002) 274–306](http://www.sciencedirect.com/science/article/pii/S0021999102971974)

  * [L. Kondic, *Instabilities in gravity driven flow of thin fluid films*, SIAM Rev. 45 (2003) 95–115](https://doi.org/10.1137/S003614450240135) 

  * [J.A. Diez, L. Kondic, *On the breakup of fluid films of finite and infinite extent*, Phys. Fluids 19 (2007) 072107](https://doi.org/10.1063/1.2749515)

  * [T.-S. Lin, L. Kondic, *Thin films flowing down inverted substrates: Two dimensional flow*, Phys. Fluids 22 (2010)](https://aip.scitation.org/doi/10.1063/1.3428753)

  * [Barra et al., *Interfacial dynamics of thin viscoelastic films and drops*, JNNFM (2016)](http://dx.doi.org/10.1016/j.jnnfm.2016.10.001)
