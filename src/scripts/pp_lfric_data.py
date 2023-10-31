#!/usr/bin/env python
"""Process LFRic output by interpolating selected fields to a common grid."""
# Standard library
import argparse
from functools import partial
from pathlib import Path
from time import time
import warnings

# External libraries
from aeolus.const import add_planet_conf_to_cubes, init_const
from aeolus.coord import get_cube_rel_days
from aeolus.io import create_dummy_cube, save_cubelist
from aeolus.lfric import (
    add_equally_spaced_height_coord,
    add_um_height_coord,
    fix_time_coord,
    load_lfric_raw,
    simple_regrid_lfric,
)
from aeolus.log import create_logger
from aeolus.subset import unique_cubes

# Local modules
import paths

# Global definitions and styles
warnings.filterwarnings("ignore")
SCRIPT = Path(__file__).name


def parse_args(args=None):
    """Argument parser."""
    ap = argparse.ArgumentParser(
        SCRIPT,
        description=__doc__,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        epilog=f"""Usage:
./{SCRIPT} -p earth -l basic -i ~/path/to/inp/dir/ -o ~/path/to/out/dir
""",
    )

    ap.add_argument("-i", "--inpdir", type=str, help="Input directory")
    ap.add_argument("-o", "--outdir", type=str, help="Output directory")
    ap.add_argument(
        "-l", "--label", type=str, required=True, help="Simulation label"
    )
    ap.add_argument(
        "-p", "--planet", type=str, required=True, help="Planet configuration"
    )
    ap.add_argument(
        "-c",
        "--cnum",
        type=str,
        help="Cubed Sphere Mesh Number",
        default="C48",
    )
    ap.add_argument(
        "--ref_cube",
        type=str,
        default="air_potential_temperature",
        help="Reference cube, to which coordinates all data will be regridded",
    )
    ap.add_argument(
        "--level_height",
        type=str,
        default="uniform",
        help="Type of the vertical level height coordinate",
    )
    ap.add_argument(
        "--model_top",
        type=float,
        default=40e3,
        help="If level_height=uniform,set the model top height.",
    )
    ap.add_argument(
        "--time_prof",
        type=str,
        default="inst",
        help="Type of the time output",
        choices=["inst", "mean"],
    )
    return ap.parse_args(args)


def main(args=None):
    """Main entry point of the script."""
    t0 = time()
    L = create_logger(Path(__file__))
    # Parse command-line arguments
    args = parse_args(args)
    planet = args.planet
    L.info(f"{planet=}")

    label = args.label
    L.info(f"{label=}")

    # Cubed sphere mesh C number
    c_num = args.cnum

    # Height coordinate
    if args.level_height == "uniform":
        add_levs = partial(
            add_equally_spaced_height_coord, model_top_height=args.model_top
        )
    elif args.level_height == "um_L38_29t_9s_40km":
        add_levs = partial(
            add_um_height_coord,
            path_to_levels_file=paths.vert / "vertlevs_L38_29t_9s_40km",
        )
    else:
        raise ValueError(f"level_height={args.level_height} is not valid.")

    # Input directory
    # inpdir = mypaths.sadir / label
    inpdir = Path(args.inpdir)
    L.info(f"{inpdir=}")

    # File names
    time_prof = args.time_prof
    if time_prof == "inst":
        # file_stem = "lfric_diag"
        file_stem = "lfric_inst_diag"
        drop_coord = ["forecast_reference_time"]
    elif time_prof == "mean":
        file_stem = "lfric_averages"
        drop_coord = []
    else:
        raise ValueError(f"{time_prof=} is not valid.")

    # Create a subdirectory for processed data
    outdir = Path(args.outdir)
    # outdir = mypaths.sadir / label / "_processed"
    outdir.mkdir(parents=True, exist_ok=True)

    # Make a list of files matching the file mask and the start day threshold
    fnames = sorted(
        inpdir.glob(f"*/*{c_num}*/{file_stem}.nc"),
        key=lambda x: int(x.parent.parent.name),
    )
    if len(fnames) == 0:
        L.critical("No files found!")
        return
    L.info(f"fnames({len(fnames)}) = {fnames[0]} ... {fnames[-1]}")

    def combi_callback(cube, field, filename):
        [
            fix_time_coord(cube, field, filename),
            add_levs(cube, field, filename),
        ]

    cl_raw = load_lfric_raw(
        fnames, callback=combi_callback, drop_coord=drop_coord
    )
    if len(cl_raw) == 0:
        L.critical("Files are empty!")
        return
    # L.info(f"{cl_raw=}")
    cubes_to_regrid = unique_cubes(cl_raw)
    if len(w_cubes := cubes_to_regrid.extract("w_in_wth")) == 2:
        cubes_to_regrid.remove(w_cubes[-1])
    for cube in cubes_to_regrid:
        if cube.units == "ms-1":
            cube.units = "m s-1"
    # L.info(f"{cubes_to_regrid=}")
    # Create a dummy cube with a target grid
    tgt_cube = create_dummy_cube(nlat=90, nlon=144, pm180=True)
    # Regrid all cubes
    cl_proc = simple_regrid_lfric(
        cubes_to_regrid, tgt_cube=tgt_cube, ref_cube_constr=args.ref_cube
    )
    const = init_const(planet, directory=paths.const)
    add_planet_conf_to_cubes(cl_proc, const=const)

    # Write the data to a netCDF file
    gl_attrs = {
        "name": label,
        "planet": planet,
        "processed": "True",
    }
    days = 0 + get_cube_rel_days(cl_proc[0]).astype(int)
    day_str = f"days{days[0]}"
    if len(days) > 1:
        day_str += f"_{days[-1]}"
    fname_out = (
        outdir / f"{label}_{c_num}_{time_prof}_{day_str}_regr.nc".lower()
    )
    save_cubelist(cl_proc, fname_out, **gl_attrs)
    L.success(f"Saved to {fname_out}")
    L.info(f"Execution time: {time() - t0:.1f}s")


if __name__ == "__main__":
    main()
