# --------------------------------------------------------------------------------------------------------------------
# The "data" repository includes all the raw RES and load data needed for the 33-bus test case.
# In the test case used in the manuscript, the modifications are presented in the function "obtainUBdata"
# The system is defined in "IEEE_33"
# --------------------------------------------------------------------------------------------------------------------
from Bus import Bus
from libs.contracts import *
from libs.controls import *

def IEEE_33(n=33):
    U_ref = 12.66  # kv
    P_ref = 1  # MVA
    I_ref = P_ref / U_ref  # kA
    R_ref = U_ref / I_ref  # ohm
    n = 33
    # Topology and loads
    FT = np.array([[33, 32],
                   [32, 31],
                   [31, 30],
                   [30, 29],
                   [29, 28],
                   [28, 27],
                   [27, 26],
                   [26, 6],
                   [25, 24],
                   [24, 23],
                   [23, 3],
                   [22, 21],
                   [21, 20],
                   [20, 19],
                   [19, 2],
                   [18, 17],
                   [17, 16],
                   [16, 15],
                   [15, 14],
                   [14, 13],
                   [13, 12],
                   [12, 11],
                   [11, 10],
                   [10, 9],
                   [9, 8],
                   [8, 7],
                   [7, 6],
                   [6, 5],
                   [5, 4],
                   [4, 3],
                   [3, 2],
                   [2, 1]]) - 1
    RX = np.array([[0.341, 0.5362],
                   [0.3105, 0.3619],
                   [0.9744, 0.9630],
                   [0.5075, 0.2585],
                   [0.8042, 0.7006],
                   [1.0590, 0.9337],
                   [0.2842, 0.1447],
                   [0.2030, 0.1034],
                   [0.8960, 0.7011],
                   [0.8980, 0.7091],
                   [0.4512, 0.3083],
                   [0.7089, 0.9373],
                   [0.4095, 0.4784],
                   [1.5042, 1.3554],
                   [0.1640, 0.1565],
                   [0.3720, 0.5740],
                   [1.2890, 1.7210],
                   [0.7463, 0.5450],
                   [0.5910, 0.5260],
                   [0.5416, 0.7129],
                   [1.4680, 1.1550],
                   [0.3744, 0.1238],
                   [0.1966, 0.0650],
                   [1.0440, 0.7400],
                   [1.0300, 0.7400],
                   [0.7114, 0.2351],
                   [0.1872, 0.6188],
                   [0.8190, 0.7070],
                   [0.3811, 0.1941],
                   [0.3660, 0.1864],
                   [0.4930, 0.2511],
                   [0.0922, 0.0470]])
    PQ = np.array([[0, 0],
                   [100, 60],
                   [90, 40],
                   [120, 80],
                   [60, 30],
                   [60, 20],
                   [200, 100],
                   [200, 100],
                   [60, 20],
                   [60, 20],
                   [45, 30],
                   [60, 35],
                   [60, 35],
                   [120, 80],
                   [60, 10],
                   [60, 20],
                   [60, 20],
                   [90, 40],
                   [90, 40],
                   [90, 40],
                   [90, 40],
                   [90, 40],
                   [90, 40],
                   [420, 200],
                   [420, 200],
                   [60, 25],
                   [60, 25],
                   [60, 20],
                   [120, 70],
                   [200, 600],
                   [150, 70],
                   [210, 100],
                   [60, 40]])
    # --------------------#
    PQ = PQ / 1000 * 2
    RX = RX[33 - n:32, :] * 1.5 / R_ref
    FT = FT[33 - n:32, :]
    # Define the list
    bus_list = [Bus() for i in range(n)]

    # Define the Load
    sample_load = np.array([0.5549771249999912,0.5272282687499916,0.35920822499999205,0.2813692499999923,0.2364911999999931,0.26976194999999215,0.3455698499999927,0.44411849999999287,0.4186723499999927,0.5072681249999924,0.5229780749999914,0.5065597349999907,0.26185967999999343,0.36511717499999247,0.3544352999999922,0.4187371499999928,0.5174093249999927,0.7954276499999903,0.7471192499999914,0.6940541249999913,0.7259093999999916,0.6549108749999911,0.8462915999999902,0.6257407499999921])
    Pload = np.array([sample_load * PQ[i][0] for i in range(n)])
    Qload = np.array([sample_load * PQ[i][1] for i in range(n)])

    for i in range(n):
        bus_list[i].Pload = Pload[i][0:Constant.T] * 1.05
        bus_list[i].Ploadl = 0.9 * bus_list[i].Pload
        bus_list[i].Ploadu = 1.1 * bus_list[i].Pload

        bus_list[i].Qload = Qload[i][0:Constant.T] * 1.05
        bus_list[i].Qloadl = 0.9 * bus_list[i].Qload
        bus_list[i].Qloadu = 1.1 * bus_list[i].Qload

    # Define the generation
    # -----
    # bus 0 generates between -2MW and 2MW(-2MVA and 2MVA)
    # cost_f = pri .* pgen
    # -----
    pri = np.array(
        [80, 80, 80, 80, 80, 80, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 80,
         80, 80])[0:Constant.T]
    bus_list[0].BuildGeneration(CV=AP(count=0, agent=bus_list[0], pri=pri, LB=-2, UB=2))

    for i in range(1, n):
        if i == 1 or i == 6 or i == 7 or i == 13 or i == 23 or i == 29 or i == 30 or i == 28 or i == 31:
            # These are implemented with MGTs
            k1 = 0.24
            k2 = 1.2
            bus_list[i].BuildGeneration(
                CV=MGT(count=i, LB=k1 * PQ[i][0], UB=k2 * PQ[i][0],
                                LBQ=0,            UBQ = 0.1*k1*PQ[i][0],
                       cost_fun=lambda x: 20 * (x ** 2 + 4 * x)))
        elif i % 5 != 0:
            # These are implemented with RESs
            bus_list[i].BuildGeneration(CV=RES(count=i))
        else:
            # These are loads
            bus_list[i].BuildGeneration(CV=User_only(count=i))
    return bus_list, n, FT, RX

def obtainUBdata(bus):
    # -------------------------------------------
    # Some operations to reshape the raw data
	# rat and rp are manually defined parameters for reshaping
    # -------------------------------------------
    T = 24
    if bus.name == '17' or bus.name == '24' or bus.name == '32':
        rat = 1.5
    else:
        rat = 0.35
    with open("data/" + bus.name + ".txt", "r") as file:
        for dt in range(T):
            rp = 1.6 if dt <= 5 else 1.2
            bus.UB[dt] = float(file.readline()) * rat * 1 * rp
        for dt in range(T):
            rp = 1.6 if dt <= 5 else 1.2
            bus.UBl[dt] = float(file.readline()) * rat * 0.9 * rp
        for dt in range(T):
            rp = 1.6 if dt <= 5 else 1.2
            bus.UBu[dt] = float(file.readline()) * rat * 1.1 * rp
        # ----------------------------------------
        # reactive power capacity: -UBQ~UBQ
        # ----------------------------------------
        bus.UBQ = (max(bus.UBu) * 1.3) ** 2 - (bus.UBu ** 2)
        if (bus.name == '17' or bus.name == '24' or bus.name == '32'):
            bus.UBQ = 0 * bus.UBQ
    bus.UB = bus.UB[0:Constant.T]
    bus.UBl = bus.UBl[0:Constant.T]
    bus.UBu = bus.UBu[0:Constant.T]
