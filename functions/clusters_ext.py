
import numpy as np


def get_ext_cl(cl_name):
    '''
    '''
    # Name, max_EBV
    cl_exts = {
        'KMHK975': 0.312, 'KMHK1023': 0.312, 'SL551': 0.312,
        'BRHT38B': 0.312, 'KMHK1045': 0.312, 'H3': 0.312, 'SL588': 0.312,
        'H88-307': 0.275, 'HS390': 0.275, 'H88-316': 0.275, 'NGC2093': 0.246,
        'H88-320': 0.246, 'H88-331': 0.232, 'NGC2108': 0.196,
        'H88-333': 0.196, 'HS411': 0.196, 'HS412': 0.196, 'SL707': 0.196,
        'BSDL2995': 0.181, 'H88-334': 0.181, 'H88-269': 0.152,
        'NGC1917': 0.152, 'H88-279': 0.152, 'SL397': 0.152, 'HS247': 0.152,
        'KMHK229': 0.145, 'BSDL268': 0.145, 'KMHK378': 0.145,
        'NGC1793': 0.145, 'NGC1795': 0.145, 'KMHK1055': 0.145, 'SL579': 0.145,
        'SL33': 0.138, 'SL41': 0.138, 'KMHK123': 0.138, 'SL54': 0.138,
        'SL73': 0.138, 'H88-265': 0.138, 'BSDL1024': 0.13, 'H88-244': 0.13,
        'H88-245': 0.13, 'OGLE298': 0.13, 'SL351': 0.13, 'SL359': 0.13,
        'SL674': 0.123, 'HW55': 0.116, 'NGC419': 0.116, 'HW59': 0.116,
        'HW63': 0.116, 'L91': 0.116, 'NGC1697': 0.116, 'SL290': 0.116,
        'BSDL1035': 0.116, 'SL35': 0.116, 'SL5': 0.109, 'NGC1751': 0.109,
        'HS151': 0.109, 'NGC1865': 0.109, 'H88-235': 0.109, 'SL446A': 0.109,
        'L27': 0.101, 'H86-70': 0.101, 'B34': 0.101, 'B39': 0.101,
        'L30': 0.101, 'L34': 0.101, 'BS35': 0.101, 'L35': 0.101,
        'B47': 0.101, 'SL151': 0.101, 'SL444': 0.101, 'SL510': 0.101,
        'H88-26': 0.094, 'BRHT45A': 0.094, 'H88-52': 0.094, 'BSDL341': 0.094,
        'SL154': 0.094, 'NGC1863': 0.094, 'LW211': 0.094, 'SL548': 0.094,
        'SL555': 0.094, 'IC2146': 0.094, 'LW263': 0.094, 'SL678': 0.094,
        'C11': 0.094, 'BSDL3158': 0.094, 'OHSC28': 0.094, 'NGC2161': 0.094,
        'L28': 0.087, 'NGC1860': 0.087, 'KMHK907': 0.087, 'SL505': 0.087,
        'KMHK979': 0.087, 'HS329': 0.087, 'LW224': 0.087, 'SL663': 0.087,
        'L45': 0.08, 'NGC294': 0.08, 'L49': 0.08, 'L50': 0.08, 'BS88': 0.08,
        'L62': 0.08, 'L63': 0.08, 'L72': 0.08, 'SL13': 0.08, 'KMHK58': 0.08,
        'KMHK128': 0.08, 'LW69': 0.08, 'KMHK151': 0.08, 'SL72': 0.08,
        'SL96': 0.08, 'H88-33': 0.08, 'H88-40': 0.08, 'SL132': 0.08,
        'H88-55': 0.08, 'H88-67': 0.08, 'SL162': 0.08, 'KMHK506': 0.08,
        'KMHK505': 0.08, 'BSDL527': 0.08, 'SL218': 0.08, 'NGC1836': 0.08,
        'BRHT4B': 0.08, 'NGC1839': 0.08, 'NGC1838': 0.08, 'SL229': 0.08,
        'BSDL631': 0.08, 'SL230': 0.08, 'H88-131': 0.08, 'NGC1846': 0.08,
        'SL244': 0.08, 'HS121': 0.08, 'BSDL677': 0.08, 'BSDL675': 0.08,
        'KMHK586': 0.08, 'BSDL716': 0.08, 'HS131': 0.08, 'HS130': 0.08,
        'NGC1852': 0.08, 'SL269': 0.08, 'H88-188': 0.08, 'HS154': 0.08,
        'SL293': 0.08, 'HS156': 0.08, 'SL300': 0.08, 'HS264': 0.08,
        'B112': 0.072, 'BS121': 0.072, 'HW86': 0.072, 'KMHK95': 0.072,
        'KMHK112': 0.072, 'BSDL77': 0.072, 'HS38': 0.072, 'SL133': 0.072,
        'HS114': 0.072, 'HS116': 0.072, 'LW393': 0.072, 'LW397': 0.072,
        'KMHK1668': 0.072, 'KMHK1702': 0.072, 'SL870': 0.072, 'BS265': 0.065,
        'LW54': 0.065, 'BSDL594': 0.065, 'BSDL654': 0.065, 'BSDL665': 0.065,
        'BSDL761': 0.065, 'BSDL779': 0.065, 'HS178': 0.065, 'NGC1997': 0.065,
        'SL869': 0.065, 'SL874': 0.065, 'KMHK1719': 0.065, 'LW469': 0.065,
        'L19': 0.058, 'HW22': 0.058, 'K38': 0.051, 'L100': 0.051,
        'HW66': 0.043, 'HW79': 0.043, 'L106': 0.043, 'L110': 0.043,
        'L111': 0.043, 'L112': 0.043, 'L113': 0.043, 'L114': 0.043,
        'NGC1644': 0.043, 'SL549': 0.043, 'HW31': 0.036, 'NGC339': 0.036,
        'L58': 0.036, 'HW40': 0.036, 'HW41': 0.036, 'HW42': 0.036,
        'HS8': 0.036, 'L3': 0.029, 'L5': 0.029, 'L6': 0.029, 'L7': 0.029,
        'HW47': 0.029, 'H86-197': 0.029, 'L102': 0.029, 'L108': 0.029,
        'HW84': 0.029, 'HW85': 0.029, 'L4': 0.022, 'HW67': 0.022,
        'L109': 0.022, 'L115': 0.022, 'AM3': 0.014
    }

    # Get max ext value for this cluster.
    e_max = cl_exts[cl_name]

    # use_e_max = [
    #     'BRHT4B', 'HS130', 'BSDL654', 'C11', 'KMHK378', 'H88-33', 'KMHK907',
    #     'NGC1838', 'NGC1839', 'NGC1836', 'HS178', 'NGC1793', 'NGC1795',
    #     'BSDL716', 'H88-279 ', 'L30', 'HW47', 'BS88', 'BSDL779', 'H88-188',
    #     'LW224', 'H88-131', 'BSDL341', 'HS329', 'NGC1863  ', 'KMHK979',
    #     'SL218', 'HS154 ', 'NGC1860', 'BSDL677', 'KMHK1719'
    # ]

    # if cl_name in use_e_max:
    #     ext_extend = 0.
    # else:
    #     ext_extend = 0.1

    ext_extend = 0.
    if e_max > 0.1:
        step = 0.02
    elif 0.05 <= e_max <= 0.1:
        step = 0.01
    else:
        step = 0.005
    # Obtain new extinction range.
    e_rs = np.arange(0., (e_max + ext_extend), step)

    # If list is empty, pass null extinction value.
    if not e_rs.any():
        e_rs = [0.]

    print " Set max extinction value: {}, step: {}".format(max(e_rs), step)

    smc = ['L4', 'L5', 'L6', 'L7', 'L19', 'L27', 'HW47', 'BS121', 'L35',
           'L45', 'L49', 'L50', 'L62', 'L63', 'L110', 'L113', 'L3', 'L28',
           'HW66', 'L100', 'HW79', 'L102', 'L109', 'HW85', 'L114', 'L115',
           'L30', 'L34', 'NGC294', 'L72', 'H86-70', 'BS35', 'BS265', 'H86-197',
           'B34', 'B39', 'HW22', 'B47', 'L58', 'K38', 'BS88', 'B112', 'HW55',
           'NGC419', 'HW67', 'HW31', 'NGC339', 'HW40', 'HW41', 'HW42', 'HW59',
           'HW63', 'L91', 'AM3', 'L112', 'L106', 'L108', 'L111', 'HW84',
           'HW86']

    # Get galaxy.
    if cl_name in smc:
        print ' SMC cluster'
        # d_rs = np.arange(18.8, 19.201, 0.05)
        # de Grijs et al. (2015) +/- 0.1
        d_rs = np.arange(18.86, 19.061, 0.02)
    else:
        print ' LMC cluster'
        # d_rs = np.arange(18.3, 18.701, 0.05)
        # de Grijs et al. (2014) +/- 0.1
        d_rs = np.arange(18.4, 18.601, 0.02)

    return e_rs, d_rs
