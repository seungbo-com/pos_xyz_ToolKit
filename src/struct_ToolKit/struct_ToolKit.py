#
import numpy as np

def pbc_vec(c_a, c_b, lattice_vec):

    '''
    Computing the vector from Triclinic Unitcell system.

    The order of the vector: a--->b = Vec (b - a)
    
    Args:
        c_a, c_b: array for cartesian coordinates
        lattice_vec: 3x3 array of lattice vector
    '''
    
    scale_diff = np.dot(c_b - c_a, np.linalg.inv(lattice_vec))
    scale_diff -= np.round(scale_diff)
    
    return np.dot(scale_diff, lattice_vec)

def three_body_corr(vec_ab, vec_bc):
    """
    Computing 3-body correlation (angle)
    
    Args:
        vec_ab, vec_bc: vectors of a <-- b , b --> c
        Schematic looks like: 
                a     c
                 \   /
                  \ /
                   b
        
    """
    ab_norm = np.linalg.norm(vec_ab); bc_norm = np.linalg.norm(vec_bc)
    vec_ab/=ab_norm;vec_bc/=bc_norm
        
    return np.arccos(np.einsum("i,i->",vec_ab , vec_bc)) * 180.0 / np.pi

def rotation_twoVec(a_v,b_v):
    """
    Computing Rotation Matrix (Rodrigues' Rotation Formula)
    """
    a_
    k_m = np.cross(a_v,b_v) # k_matrix
    
    skew_K_m = np.asarray([
        [0, -k_m[2],k_m[1]],
        [k_m[2], 0,-k_m[0]],
        [-k_m[1], k_m[0],0],
    ],dtype=float)
    
    angle_ab = three_body_corr(a_v,b_v) * np.pi / 180.0

    return np.identity(3) + np.sin(angle_ab) * skew_K_m + (1 - np.cos(angle_ab)) * np.dot(skew_K_m,skew_K_m)
