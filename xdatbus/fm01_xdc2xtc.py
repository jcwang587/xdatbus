import os
import MDAnalysis as MDa


def xdc2xtc(xyz_path):
    """
    Initialize a trajectory writer instance for *filename*.

        Parameters
        ----------
        xyz_path : str
            Path to the unwrapped xyz file

    """

    u = MDa.Universe(xyz_path)

    output_filename = os.path.basename(xyz_path).replace('.xyz', '.xtc')
    output_path = os.path.join(os.path.dirname(xyz_path), output_filename)

    # Write out the XTC file
    with MDa.Writer(output_path, u.atoms.n_atoms) as w:
        for ts in u.trajectory:
            print("Writing frame %d" % ts.frame)
            w.write(u.atoms)

    print("xdatbus-func: fm01_xdc2xtc: Done!")
