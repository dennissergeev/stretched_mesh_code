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
        ("stretch_factor", float),
        ("vert_lev", str),
        ("kw_plt", dict),
    ],
)


SIMULATIONS = {
    "c192s10e": Simulation(
        title="C192s10e",
        work_name="thai_hab1_c192s10",
        planet="hab1",
        timestep=120,
        stretch_factor=10,
        vert_lev="L38_29t_9s_40km",
        kw_plt={"color": "C0", "marker": "h"},
    ),
    "c192s10r": Simulation(
        title="C192s10r",
        work_name="thai_hab1_c192s10_l63_rc",
        planet="hab1",
        timestep=120,
        stretch_factor=10,
        vert_lev="L63_50t_13s_40km",
        kw_plt={"color": "C1", "marker": "p"},
    ),
    "c192s10p": Simulation(
        title="C192s10p",
        work_name="thai_hab1_c192s10_l63_pc",
        planet="hab1",
        timestep=120,
        stretch_factor=10,
        vert_lev="L63_50t_13s_40km",
        kw_plt={"color": "C2", "marker": "s"},
    ),
    "c192p": Simulation(
        title="C192p",
        work_name="thai_hab1_c192_l63",
        planet="hab1",
        timestep=300,
        stretch_factor=1,
        vert_lev="L63_50t_13s_40km",
        kw_plt={"color": "C3", "marker": "o"},
    ),
}


DAYSIDE = Region(-90, 90, -90, 90, name="dayside", model=lfric)
NIGHTSIDE = Region(90, -90, -90, 90, name="nightside", model=lfric)