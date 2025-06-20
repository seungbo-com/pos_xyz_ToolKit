## POSCAR Editing
import numpy as np

class poscar_edit:

    def __init__(self, file_name, output_file):

        self.file_name = file_name      # Input file name
        self.output_file = output_file  # Output file name

    def read_poscar(self):
        '''
        Reading POSCAR file
        
        Return:
            dict{
                "coord": {atom type: xyz coords},
                "atom_type": [Atom Type],
                "atom_number": [Number of Atom],
                "lattice_parameter": array of lattice param
            }
        '''

        lta_lines = open(self.file_name).read().splitlines()

        lattice_param = [list(map(float, l_line.split())) for l_line in lta_lines[2:5]]

        name_atom = lta_lines[5].split() # Atom Species
        num_atom = [int(na) for na in lta_lines[6].split()] # Number of each atoms
        
        float_array, f_gather = {}, []; ii, num_cnt = 0, 0
        
        # Collecting the coordinates for each atoms
        for ea_line_c in lta_lines[8:] :
            
            if num_cnt <= num_atom[ii]:
                f_gather.append(np.asarray(list(map(float, ea_line_c.split()))))
                num_cnt += 1
                
                if num_cnt == num_atom[ii]:
                    float_array[name_atom[ii]] = f_gather
                    ii += 1; num_cnt = 0; f_gather = []
        
        return {"coord":float_array,
                "atom_type":name_atom,
                "atom_number":num_atom,
                "lattice_parameter":lattice_param}
    
    
    def construct_poscar(self, scale, text_line,order_atomS, order_atomN, lattice_param, coord_dict):
        
        '''
        Creating the POSCAR
        
        Input
            scale: Scale of the unitcell
            text_line: Comment Section for the POSCAR
            order_atomS: List of atom species
            order_atomN: List of number for each atom species
            lattice_param: Unit Cell Vector (3x3 array)
            coord_dict: Dictionary of coordinates for each atom; {atom: coordinates}
            
        '''
        combine_poscar = open(self.output_file, 'w'); combine_poscar.write("#"+ text_line +f"  \n {scale:.4f} \n")
        
        for lp_ in lattice_param: # Lattice Parameter
            combine_poscar.write(f" {lp_[0]:.5f}  {lp_[1]:.5f}  {lp_[2]:.5f}\n")
        
        # Atom Type
        combine_poscar.write('   '.join(order_atomS) + "\n")
        # Number of Atoms
        combine_poscar.write('   '.join([f"{atom_N}" for atom_N in order_atomN]) + "\n")
        combine_poscar.write("Cartesian\n")

        for order_atom in order_atomS:
            for rr_cc in coord_dict[order_atom]:
                combine_poscar.write("   " + '    '.join([f"{coord:.6f}" for coord in rr_cc]) + "\n")
                
        combine_poscar.close()

