import os
import shutil
import pandas as pd


def fm02_hillspot2hills(HILLSPOT_dir, hills_dir, cv, height_conversion=1, sigma_conversion=1, del_inter=False):
    """
    Convert HILLSPOT file to HILLS file
        Parameters
        ----------
        HILLSPOT_dir : str
            Path to HILLSPOT file
        hills_dir : str
            Path to the directory where the HILLS file will be created
        cv : str or list
            Name of the collective variable(s)
        height_conversion : float(optional)
            Conversion factor to convert the unit of the height from eV to kJ/mol
        sigma_conversion : float(optional)
            Conversion factor to convert the unit of the sigma based on the lattice in Angstrom
        del_inter : bool(optional)
            Delete the intermediate files created by this function.
    """
    hillspot = open(HILLSPOT_dir, 'r')
    column_names = (cv if isinstance(cv, list) else [cv]) + ['height', 'sigma']
    hs = pd.read_csv(hillspot, sep='\s+', header=None, names=column_names)

    hs['time'] = range(1, len(hs) + 1)
    hs['bias_factor'] = -1

    hs['sigma'] = hs['sigma'] * sigma_conversion
    hs['height'] = hs['height'] * height_conversion

    if isinstance(cv, list):
        for variable in cv:
            hs[variable] = hs[variable] * sigma_conversion
            # Create new sigma column for each CV
            hs['sigma_' + variable] = hs['sigma'] * sigma_conversion
        # Drop the old 'sigma' column as we have created new ones for each CV
        hs.drop(columns='sigma', inplace=True)
    else:
        hs[cv] = hs[cv] * sigma_conversion
        hs['sigma_' + cv] = hs['sigma'] * sigma_conversion

    # Generate the header
    header_str = '#! FIELDS time '
    for variable in (cv if isinstance(cv, list) else [cv]):
        header_str += variable + ' '
    for variable in (cv if isinstance(cv, list) else [cv]):
        header_str += 'sigma_' + variable + ' '
    header_str += 'height biasf\n'

    # Create the order for columns
    order = ['time'] + (cv if isinstance(cv, list) else [cv])
    for variable in (cv if isinstance(cv, list) else [cv]):
        order.append('sigma_' + variable)
    order += ['height', 'bias_factor']
    hs = hs[order]

    # write the dataframe to a hills file with tab-separated format
    hs.to_csv('HILLS', sep='\t', header=False, index=False, float_format='%.4f')

    file = open('HILLS', 'r+')
    lines = file.readlines()
    file.seek(0, 0)
    file.write(header_str)
    file.write('#! SET multivariate ' + str(isinstance(cv, list)).lower() + '\n')
    for line in lines:
        file.write(line)
    file.close()

    # copy the HILLS file to the hills_dir
    if hills_dir != 'HILLS':
        shutil.copy('HILLS', hills_dir)
        print('HILLS file is copied to', hills_dir)
    else:
        print('HILLS file is created in the current directory.')

    # delete the intermediate files
    if del_inter:
        os.remove('HILLS')
        print('Intermediate files are deleted.')
