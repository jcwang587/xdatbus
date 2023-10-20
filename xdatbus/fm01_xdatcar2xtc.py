import MDAnalysis as MDa


def fm01_xdatcar2xtc(
        aimd_path
):
    """
    Initialize a trajectory writer instance for *filename*.

        Parameters
        ----------
        aimd_path : str
            Output filename of the trajectory; the extension determines the
            format.

    """

    xdatbusxyz_ase = read(aimd_path, format='vasp-xdatcar', index=':')
    write('XDATBUS.xyz', xdatbusxyz_ase, format='xyz')
    u = MDa.Universe('XDATBUS.xyz')

    if xtc:
        # Write out the XTC file
        with MDa.Writer("trajectory.xtc", u.atoms.n_atoms) as w:
            for ts in u.trajectory:
                print("Writing frame %d" % ts.frame)
                w.write(u.atoms)

    print("Done.")
