####################
"""
This file copies a part of the source code for the paper and includes the necessary data.
It is more of a pseudocode.
"""
####################


def set_boundary_conditions(node_list, n, n_p, n_t, PQ, m_pris):
    # set reference power and heat loads
    load_data = xlrd.open_workbook("load.xlsx").sheet_by_index(0)
    sample_load = [load_data.cell_value(i, 1) for i in range(96)]
    sample_load = [sample_load[i * 4] / 2 for i in range(24)]
    sample_load = ((np.array(sample_load) - 1.05) * 4 + 1.05)
    sample_load /= np.average(sample_load)
    sample_hload = [2.06, 2.07, 2.08, 2.09, 2.1, 2.08, 2.06, 2.04, 2.02, 2, 1.99, 1.96, 1.96, 1.99, 2, 2, 2, 2, 2, 2.01,
                    2.02, 2.03, 2.04, 2.05]
    sample_hload /= np.average(sample_hload)
    Pload = []
    Qload = []
    Hload = []
	
	# The actual power and heat loads of the nodes are obtained by multiplying sample loads with a coefficient(PQ[][] or m_pris[])
    for i in range(n):
        if i < n_p:
            Pload += [sample_load * PQ[i][0]]
            Qload += [sample_load * PQ[i][1]]
        else:
            Pload += [sample_load * 0]
            Qload += [sample_load * 0]
        if node_list[i].H_type == "HC":
            Hload += [sample_hload * (m_pris[i] * 20 * 4195 / 1000000)]  # Reference load * m c dT / 1000000 for MW
        else:
            Hload += [sample_hload * 0]
    for i in range(n_p):
        node_list[i].Pload = Pload[i][0:Constant.T] * 0.8
        node_list[i].Qload = Qload[i][0:Constant.T] * 0.8
        node_list[i].Hload = Hload[i][0:Constant.T] * 1.0

    # set DESs
    for i, node in enumerate(node_list):
        node.BuildGeneration(CV=general_DES(count=i, agent=node))
        node.m_pri = m_pris[i]
        CV = node.CV
        CV.HaveCost = False
		# Initialize
        CV.WP_ava.value = np.zeros(Constant.T)  # available WP power
        CV.PV_ava.value = np.zeros(Constant.T)  # available PV power
        CV.MTl.value = 0   # CHP/MT lower bound
        CV.MTu.value = 0   # CHP/MT lower bound
        CV.MT_HP_rat.value = 0  # Heat to power ratio
        CV.eh_COP.value = 0  # COP of electric pump (or electric heating device, EH)
        CV.eh_max.value = 0  # capacity of EH
        CV.R_HES_l.value = np.zeros(Constant.T)  # Heat resistance of HES
        CV.R_HES_u.value = np.zeros(Constant.T)  # Heat resistance of HES
        CV.R_CR.value = np.zeros(Constant.T)  # Heat resistance of HES
        CV.boilerl.value = 0  # boiler, we do not mention boilers in the paper, but we can still use the heat current model
        CV.boileru.value = 0  # boiler,  boilerl <= boiler output <= boileru, it can just be treated as a gas fired heat source
		# In below defines the DESs
        if i == 0:   # node 0, define the costs
            CV.MTu.value = 50
            CV.tanMT.value = 0
            CV.cost_fun = np.array([400, 400, 400, 400, 400, 400,
                                 550, 550, 550, 550, 550, 550,
                                 550, 550, 550, 550, 550, 550,
                                 550, 550, 550, 400, 400, 400])[0:Constant.T]
            CV.c_value = CV.cost_fun
            CV.cost += CV.cost_fun @ CV.MT
            CV.HaveCost = True
        else:   # other nodes
            b1 = node.is_DN_node and PQ[i][0] > 2.05  # condition 1: the node is a DN node and PQ > 2.05
            b2 = node.is_DHN_node and node.H_type == "HS"   # condition 2:, the node is a HS node in the DHN
            if b1 or b2:
                if b1 and not b2:
                    # DN nodes with a large power load,
					# implemented with gas fired CHP.
                    CV.MTl.value = 0.08 * PQ[i][0]
                    CV.MTu.value = PQ[i][0] * 0.4
                    CV.MT_HP_rat.value = 1
                    CV.cost_fun = lambda x:110 * x**2 + 440 * x
                    CV.c_value = 440 * np.ones(Constant.T)
                    CV.cost += cp.sum(CV.cost_fun(CV.MT))
                    CV.HaveCost = True
					
					# if it is also a DHN HC node, ...
                    if node.is_DHN_node:
                        CV.eh_max.value = (np.max(node.Hload)) / 4
                        CV.eh_COP.value = 2
                elif (not b1) and b2:
                    # i is a HS node in DHN, but may not be a DN node
                    # implemented with a boiler
                    CV.boileru.value = 20
                    CV.boilerl.value = 0
                    CV.cost_fun = lambda x:210 * x
                    CV.c_value = 210 * np.ones(Constant.T)
                    CV.cost += cp.sum(CV.cost_fun(CV.boiler))
                    CV.label = "boiler"
                    CV.HaveCost = True
                elif b1 and b2:
                    # i is a HS node in DHN, and a DN node with large power loads
                    # close to (b1 and not b2)， but it has a larger capacity and  heat to power ratio
                    CV.MTl.value = 0.2 * PQ[i][0]
                    CV.MTu.value = PQ[i][0]
                    CV.MT_HP_rat.value = 2
                    CV.cost_fun = lambda x:125 * x**2 + 450 * x
                    CV.c_value = 450 * np.ones(Constant.T)
                    CV.cost += cp.sum(CV.cost_fun(CV.MT))
                    CV.label = "MT"
                    CV.HaveCost = True

            if node.is_DHN_node:
                # DHN nodes are implemented heat pumps
				# besides, the total mass flow rate that enters the customer heat radiator is defined as m_sec_tot
				# the mass flow rate that enters the HES at the SHN are bounded by m_HES_l and m_HES_u
                    if node.H_type == "HC":
                        CV.m_sec_tot.value = 2.5 * m_pris[i]
                        CV.m_HES_l.value = 3
						CV.m_HES_u.value = CV.m_sec_tot - 3
                        CV.eh_max.value = (np.max(node.Hload)) / 4
                        CV.eh_COP.value = 2
                    if node.H_type == "HS":
                        CV.m_HES_l.value = np.array([1.5 * m_pris[i]]).repeat(Constant.T)
                        CV.m_HES_u.value = np.array([3.5 * m_pris[i]]).repeat(Constant.T)
						
					# kAs of the Heat exchange station(kA) and Customer Radiator(CR)
					CV.kA_HES = 4.e5
					CV.kA_CR = 2.e5
						
			# Available Wind power 
            if i != 0 and i <= n_p:
                with open("data/"+str(i)+".txt", "r") as file:
                    for dt in range(Constant.T):
                        CV.WP_ava.value[dt] = float(file.readline()) * 2
						
