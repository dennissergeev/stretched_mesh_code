"""Common objects stretched_mesh_proj."""
from dataclasses import dataclass, field
import os

from aeolus.const import init_const
from aeolus.meta import update_metadata
from aeolus.model import lfric
from aeolus.region import Region
from aeolus.subset import DimConstr
import matplotlib.pyplot as plt
import paths


@dataclass
class Simulation:
    """LFRic simulation details."""

    title: str
    work_name: str
    planet: tuple
    timestep: int
    days_per_job: int
    c_num: int
    stretch_factor: float
    convection_parameterization: str
    vert_lev: str
    kw_plt: dict = field(default_factory=dict)


SIMULATIONS = {
    "hab1_mod_c192s10e": Simulation(
        title="StretchExplicit",
        work_name="hab1_mod_c192s10e",
        planet="hab1",
        timestep=120,
        days_per_job=5,
        c_num=192,
        stretch_factor=10,
        convection_parameterization="None",
        vert_lev="L63_50t_13s_40km",
        kw_plt={"color": "#E24A33", "marker": "o"},
    ),
    "hab1_mod_c192s10r": Simulation(
        title="StretchReduced",
        work_name="hab1_mod_c192s10r",
        planet="hab1",
        timestep=120,
        days_per_job=5,
        c_num=192,
        stretch_factor=10,
        convection_parameterization="Reduced",
        vert_lev="L63_50t_13s_40km",
        kw_plt={"color": "#348ABD", "marker": "p"},
    ),
    "hab1_mod_c192s10p": Simulation(
        title="StretchParam",
        work_name="hab1_mod_c192s10p",
        planet="hab1",
        timestep=120,
        days_per_job=5,
        c_num=192,
        stretch_factor=10,
        convection_parameterization="Full",
        vert_lev="L63_50t_13s_40km",
        kw_plt={"color": "#988ED5", "marker": "s"},
    ),
    "hab1_mod_c192p": Simulation(
        title="UniformParam",
        work_name="hab1_mod_c192p",
        planet="hab1",
        timestep=300,
        days_per_job=10,
        c_num=192,
        stretch_factor=1,
        convection_parameterization="Full",
        vert_lev="L63_50t_13s_40km",
        kw_plt={"color": "#777777", "marker": "h"},
    ),
}


def all_sim_file_label(sims):
    """Make a shorter label for a list of labels with a common prefix."""
    pref = os.path.commonprefix(sims)
    return f"{pref}_{'_'.join([i.removeprefix(pref) for i in sims])}"


N_RES = 512  # lat/lon resolution for regridding
SPINUP_DAYS = 500
DAYSIDE = Region(-90, 90, -90, 90, name="dayside", model=lfric)
NIGHTSIDE = Region(90, -90, -90, 90, name="nightside", model=lfric)

CONST = init_const("hab1", directory=paths.const)
DC = DimConstr(model=lfric)

KW_ZERO_LINE = {
    "color": plt.rcParams["axes.edgecolor"],
    "linewidth": plt.rcParams["axes.linewidth"],
    "linestyle": "dashed",
    "dash_capstyle": "round",
}


# TODO: move to aeolus
@update_metadata(name="total_precipitation_rate", units="mm day-1")
def lfric_precip_sum(dset, const=CONST):
    """Calculate total precipitation."""
    ls_p = dset.extract_cube("ls_prec")
    ls_p = ls_p.copy(data=ls_p.data.filled(fill_value=0))
    cv_p = dset.extract_cube("conv_prec")
    cv_p = cv_p.copy(data=cv_p.data.filled(fill_value=0))
    p_sum = (ls_p + cv_p) / const.condensible_density
    return p_sum


SIMULATIONS_OLD = {
    "c192s10e": Simulation(
        title="StretchExplicit*",
        work_name="thai_hab1_c192s10_l63_ec",
        planet="hab1",
        timestep=120,
        days_per_job=5,
        c_num=192,
        stretch_factor=10,
        convection_parameterization="None",
        vert_lev="L63_50t_13s_40km",
        kw_plt={"color": "#E24A33", "marker": "h"},
    ),
    "c192s10r": Simulation(
        title="StretchReduced*",
        work_name="thai_hab1_c192s10_l63_rc",
        planet="hab1",
        timestep=120,
        days_per_job=5,
        c_num=192,
        stretch_factor=10,
        convection_parameterization="Reduced",
        vert_lev="L63_50t_13s_40km",
        kw_plt={"color": "#348ABD", "marker": "p"},
    ),
    "c192s10p": Simulation(
        title="StretchParam*",
        work_name="thai_hab1_c192s10_l63_pc",
        planet="hab1",
        timestep=120,
        days_per_job=5,
        c_num=192,
        stretch_factor=10,
        convection_parameterization="Full",
        vert_lev="L63_50t_13s_40km",
        kw_plt={"color": "#988ED5", "marker": "s"},
    ),
    "c192p": Simulation(
        title="UniformParam*",
        work_name="thai_hab1_c192_l63",
        planet="hab1",
        timestep=300,
        c_num=192,
        days_per_job=10,
        convection_parameterization="Full",
        stretch_factor=1,
        vert_lev="L63_50t_13s_40km",
        kw_plt={"color": "#777777", "marker": "o"},
    ),
}
