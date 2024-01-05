"""Common objects stretched_mesh_proj."""
from aeolus.region import Region
from aeolus.model import lfric
from typing import NamedTuple


Simulation = NamedTuple(
    "Simulation",
    [
        ("title", str),
        ("work_name", str),
        ("planet", tuple),
        ("timestep", int),
        ("days_per_job", int),
        ("stretch_factor", float),
        ("vert_lev", str),
        ("kw_plt", dict),
    ],
)


SIMULATIONS = {
    "c192s10e": Simulation(
        title="C192s10e",
        work_name="thai_hab1_c192s10_l63_ec",
        planet="hab1",
        timestep=120,
        days_per_job=5,
        stretch_factor=10,
        vert_lev="L63_50t_13s_40km",
        kw_plt={"color": "#E24A33", "marker": "h"},
    ),
    "c192s10r": Simulation(
        title="C192s10r",
        work_name="thai_hab1_c192s10_l63_rc",
        planet="hab1",
        timestep=120,
        days_per_job=5,
        stretch_factor=10,
        vert_lev="L63_50t_13s_40km",
        kw_plt={"color": "#348ABD", "marker": "p"},
    ),
    "c192s10p": Simulation(
        title="C192s10p",
        work_name="thai_hab1_c192s10_l63_pc",
        planet="hab1",
        timestep=120,
        days_per_job=5,
        stretch_factor=10,
        vert_lev="L63_50t_13s_40km",
        kw_plt={"color": "#988ED5", "marker": "s"},
    ),
    "c192p": Simulation(
        title="C192p",
        work_name="thai_hab1_c192_l63",
        planet="hab1",
        timestep=300,
        days_per_job=10,
        stretch_factor=1,
        vert_lev="L63_50t_13s_40km",
        kw_plt={"color": "#777777", "marker": "o"},
    ),
}

SPINUP_DAYS = 500
DAYSIDE = Region(-90, 90, -90, 90, name="dayside", model=lfric)
NIGHTSIDE = Region(90, -90, -90, 90, name="nightside", model=lfric)