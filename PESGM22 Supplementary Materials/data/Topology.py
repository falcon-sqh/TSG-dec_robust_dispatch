####################
"""
This file copies a part of the source code for the paper and includes the necessary data.
It is more of a pseudocode.
"""
####################





U_ref = 23  # kv
P_ref = 1  # MVA
I_ref = P_ref / U_ref  # kA
R_ref = U_ref / I_ref  # ohm
pi = 3.14159
rho = 1000
n = 17  # number of nodes
n_p = 14  # number of DN nodes
n_t = 14  # number of DHS nodes

# DN topology(FT_P), line impedence(RX) and reference load(PQ)
FT_P = np.array([[1, 2],
                 [1, 3],
                 [1, 4],
                 [2, 5],
                 [2, 6],
                 [5, 7],
                 [3, 8],
                 [8, 9],
                 [8, 10],
                 [3, 11],
                 [4, 12],
                 [4, 13],
                 [13, 14]]) - 1
RX = np.array([[0.075, 0.1],
               [0.11, 0.11],
               [0.11, 0.11],
               [0.09, 0.18],
               [0.08, 0.11],
               [0.04, 0.04],
               [0.08, 0.11],
               [0.08, 0.11],
               [0.11, 0.11],
               [0.11, 0.11],
               [0.09, 0.12],
               [0.08, 0.11],
               [0.04, 0.04]])/100  # p.u
PQ = np.array([[0, 0],  # 0
               [2, 1.6],  # 1
               [4, 2.7],  # 2
               [1, 0.9],  # 3
               [2, 0.8],  # 4
               [3, 1.5],  # 5
               [1.5, 1.2],  # 6
               [5, 3],  # 7
               [4.5, 2],  # 8
               [0.6, 0.1],  # 9
               [1, 0.9],  # 10
               [1, 0.7],  # 11
               [1, 0.9],  # 12
               [2.1, 1.0]])  # 13
			   
# DHS topology(FT_T)
FT_T = np.array([[1, 16],
                 [4, 16],
                 [6, 16],
                 [16, 5],
                 [3, 14],
                 [13, 14],
                 [14, 11],
                 [2, 7]
				 [9, 15],
				 [8, 15],
				 [15, 7],
				 [7, 5],
				 [7, 11]])

# Length(m) Diameter(m) and Velocity(m/s), flow balance has been guaranteed
LDV = np.array([[940, 0.25, 0.74],
                [1000, 0.3, 0.43],
                [1100, 0.3, 0.39],
                [2700, 0.35, 0.98],
                [810, 0.2, 0.45],
                [810, 0.3, 0.45],
                [2340, 0.3, 0.65],
                [1080, 0.35, 0.5],
                [1080, 0.2, 0.3],
                [1350, 0.35, 0.6],
                [2500, 0.35, 0.69796],
                [1890, 0.4, 0.65],
                [1890, 0.4, 0.65]])

# mass flow rate that enters the HES at node i in the primary heating network
m_pris = np.array([0,
                   36.3246650571320,
                   48.1056375080937,
                   14.1371669411541,
                   30.3949089234813,
                   175.968458509198, 
                   27.5674755352504,
                   48.1056375080937,
                   57.7267650097124,
                   9.42477796076938,
                   0,
                   127.627201552085, 
                   0,
                   31.8086256175967,
                   0,
                   0,
                   0])

# type of the nodes
node_list = [Node(is_DN_node=True, is_DHN_node=False, P_type="VT", H_type=None),  # 0
             Node(is_DN_node=True, is_DHN_node=True, P_type="PQ", H_type="HC"),  # 1 
             Node(is_DN_node=True, is_DHN_node=True, P_type="PQ", H_type="HC"),  # 2
             Node(is_DN_node=True, is_DHN_node=True, P_type="PQ", H_type="HC"),  # 3
             Node(is_DN_node=True, is_DHN_node=True, P_type="PQ", H_type="HC"),  # 4
             Node(is_DN_node=True, is_DHN_node=True, P_type="PQ", H_type="HS"),  # 5
             Node(is_DN_node=True, is_DHN_node=True, P_type="PQ", H_type="HC"),  # 6
             Node(is_DN_node=True, is_DHN_node=True, P_type="PQ", H_type="HC"),  # 7
             Node(is_DN_node=True, is_DHN_node=True, P_type="PQ", H_type="HC"),  # 8
             Node(is_DN_node=True, is_DHN_node=True, P_type="PQ", H_type="HC"),  # 9
             Node(is_DN_node=True, is_DHN_node=False, P_type="PQ", H_type=None),  # 10
             Node(is_DN_node=True, is_DHN_node=True, P_type="PQ", H_type="HS"),  # 11
             Node(is_DN_node=True, is_DHN_node=False, P_type="PQ", H_type=None),  # 12
             Node(is_DN_node=True, is_DHN_node=True, P_type="PQ", H_type="HC"),  # 13
             Node(is_DN_node=False, is_DHN_node=True, P_type=None, H_type="JN"),  # 14 JN = junction nodes, there is actually no HES at such nodes, but we can still treat it as a HC node with m_pri = 0
             Node(is_DN_node=False, is_DHN_node=True, P_type=None, H_type="JN"),  # 15
             Node(is_DN_node=False, is_DHN_node=True, P_type=None, H_type="JN"),  # 16
                 ]