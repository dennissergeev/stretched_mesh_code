<p align="center">
<img src="src/figures/regr__hab1_mod_c192_s10e_s10r_s10p_p__cell_width__c12_mesh__summary.png"
     alt="cover image"></a>
</p>

<h1 align="center">
The impact of the explicit representation of convection on the climate of a tidally locked planet in global stretched-mesh simulations.
</h1>
<p align="center">
<a href="https://arxiv.org/abs/2402">
<img src="https://img.shields.io/badge/arXiv-2402-red"
     alt="Preprint"></a>
</p>
<p align="center">
<a href="https://www.python.org/downloads/">
<img src="https://img.shields.io/badge/python-3.12-blue.svg"
     alt="Python 3.12"></a>
<a href="https://github.com/psf/black">
<img src="https://img.shields.io/badge/code%20style-black-000000.svg"
     alt="black"></a>
</p>


<h2 align="center">Repository contents</h2>

Notebooks and Python scripts are in the [`src/scripts/` directory](src/scripts/), while the figures themselves are in the `src/figures/` directory.

|  #  | Figure | Notebook |
|:---:|:-------|:---------|
|  1  | [Summary of the simulation setup](src/figures/regr__hab1_mod_c192_s10e_s10r_s10p_p__cell_width__c12_mesh__summary.pdf) | [Show-Mesh-And-Cell-Sizes.ipynb](https://nbviewer.jupyter.org/github/dennissergeev/stretched_mesh_code/blob/main/src/scripts/Show-Mesh-And-Cell-Sizes.ipynb) |
|  2  | [Clouds and precipitation in the simulations with stretched and quasi-uniform mesh](src/figures/combi_hab1_mod_c192_s10e_s10r_s10p_p__inst_diag__tot_col_m_c_tot_prec__grat__precip_sum_hist__cloud_types.pdf) | [Cloud-Precip-Snap-Hist.ipynb](https://nbviewer.jupyter.org/github/dennissergeev/stretched_mesh_code/blob/main/src/scripts/Cloud-Precip-Snap-Hist.ipynb) |
|  3  | [Meridional and time mean profiles of vertically integrated moisture diagnostics](src/figures/regr__hab1_mod_c192_s10e_s10r_s10p_p__tot_col_m_v_tot_col_m_c_tot_col_m_cl_tot_col_m_ci__tmm.pdf) | [Meridional-Mean-Cloud-Profiles.ipynb](https://nbviewer.jupyter.org/github/dennissergeev/stretched_mesh_code/blob/main/src/scripts/Meridional-Mean-Cloud-Profiles.ipynb) |
|  4  | [Vertical profiles of time mean diagnostics in the substellar region](src/figures/regr__hab1_mod_c192_s10e_s10r_s10p_p__tot_col_m_v_tot_col_m_c_tot_col_m_cl_tot_col_m_ci__tmm.pdf) | [Substellar-Vertical-Profiles.ipynb](https://nbviewer.jupyter.org/github/dennissergeev/stretched_mesh_code/blob/main/src/scripts/Substellar-Vertical-Profiles.ipynb) |
|  5  | [Thermodynamic and circulation regime](src/figures/regr__hab1_mod_c192_s10e_s10r_s10p_p__t_sfc_toa_olr_u_zm__w_zm_day__tm_map.pdf) | [Thermodynamic-And-Circulation-Regime.ipynb](https://nbviewer.jupyter.org/github/dennissergeev/stretched_mesh_code/blob/main/src/scripts/Thermodynamic-And-Circulation-Regime.ipynb) |
|  6  | [Maps of precipitation rate](src/figures/regr__hab1_mod_c192_s10e_s10r_s10p_p__tot_prec_ls_prec_conv_prec__tm_map.pdf) | [Precipitation-Maps.ipynb](https://nbviewer.jupyter.org/github/dennissergeev/stretched_mesh_code/blob/main/src/scripts/Precipitation-Maps.ipynb) |
|  7  | [Circulation regime bistability](src/figures/thai_hab1__c192_s10e_s10r_s10p_p__inst_diag__toa_osr__t_sfc__wind_08160m.pdf) | [Show-Bistability.ipynb](https://nbviewer.jupyter.org/github/dennissergeev/stretched_mesh_code/blob/main/src/scripts/Show-Bistability.ipynb) |


<h2 align="center">How to reproduce figures</h2>

<h3 align="center">Set up environment</h3>

To recreate the required environment for running Python code, follow these steps. (Skip the first two steps if you have Jupyter with `nb_conda_kernels` installed already.)

1. Install conda or mamba, e.g. using [miniforge](https://github.com/conda-forge/miniforge).
2. Install necessary packages to the `base` environment. Make sure you are installing them from the `conda-forge` channel.
```bash
mamba install -c conda-forge jupyterlab nb_conda_kernels
```
3. Git-clone or download this repository to your computer.
4. In the command line, navigate to the downloaded folder, e.g.
```bash
cd /path/to/downloaded/repository
```
5. Create a separate conda environment (it will be called `lfric_ana`).
```
mamba env create --file environment.yml
```

<h3 align="center">Open the code</h3>

1. Start the Jupyter Lab, for example from the command line (from the `base` environment).
```bash
jupyter lab
```
2. Open notebooks within the `lfric_ana` environment start running the code.


<h2 align="center">
System information and key python libraries
</h2>

TODO
