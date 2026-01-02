
## Import Basic Modules
	## Engine
from KJH91_Projects.Project_ADC.Library_and_Engine import StickDiagram_KJH1
from KJH91_Projects.Project_ADC.Library_and_Engine import DesignParameters
from KJH91_Projects.Project_ADC.Library_and_Engine import DRC

	## Library
import copy
import math
import numpy as np
import time

	## KJH91 Basic Building Blocks
from KJH91_Projects.Project_ADC.Layoutgen_code.A_Basic_Building_Block import A02_ViaStack_KJH3
from KJH91_Projects.Project_ADC.Layoutgen_code.A_Basic_Building_Block import A14_Mosfet_KJH3
from KJH91_Projects.Project_ADC.Layoutgen_code.A_Basic_Building_Block import A08_PbodyContactPhyLen_KJH3
from KJH91_Projects.Project_ADC.Layoutgen_code.A_Basic_Building_Block import A07_NbodyContactPhyLen_KJH3

from KJH91_Projects.Project_ADC.Layoutgen_code.Q00_Decoder_Nand     import Q00_02_Nand_KJH0
from KJH91_Projects.Project_ADC.Layoutgen_code.Q01_Decoder_Nor      import Q01_02_Nor_KJH0
from KJH91_Projects.Project_ADC.Layoutgen_code.Q02_Decoder_Xgate    import Q02_00_Xgate_KJH0
from KJH91_Projects.Project_ADC.Layoutgen_code.Q03_Decoder_Inv      import Q03_00_Inv_KJH0

from KJH91_Projects.Project_ADC.Layoutgen_code.Q04_Decoder_Unit     import Q04_00_Placement_KJH0


## Define Class
class _Routing(StickDiagram_KJH1._StickDiagram_KJH):

	## Input Parameters for Design Calculation: Used when import Sref
	_ParametersForDesignCalculation = dict(
	# Unit
		# Routing
		_Routing_Dist=100,

		# Xvt
		_Unit_Xvt = 'SLVT',

		# Gate to gate dist.
		_Unit_GatetoGateDist = 100,

		# Inputs of Nand,Nor
		_Unit_Num_EachStag_input = [2,2,2], # ex) [2,3,4] 가장 마지막단(TG driving) nand input4, Nor input3, Nand input2, Nor input2 ...

		# Power rail
			# Pbody_Pulldown(NMOS)
			_Unit_Pbody_NumCont         =2,  # Number
			_Unit_Pbody_XvtTop2Pbody    = None,  # Number/None(Minimum)
			# Nbody_Pullup(PMOS)
			_Unit_Nbody_NumCont         = 2,  # Number
			_Unit_Nbody_Xvtdown2Nbody   = None,  # Number/None(Minimum)
			# PMOS and NMOS Height
			_Unit_PMOSXvt2NMOSXvt                   = 1000,  # number

		# Poly Gate setting
			# Poly Gate setting : vertical length
		_Unit_POGate_Comb_length    = None,  # None/Number


	# Nand( _Unit_Num_EachStag_input에서 1,3,5,7...번째 해당하는 nand 생성)
		# MOSFET
			# Common
			_Nand_NumberofGate      = [1,2],  # Number
			_Nand_ChannelLength     = [30,30],  # Number
			_Nand_POGate_ViaMxMx    = [[0, 1],[0, 3]],  # Ex) [1,5] -> ViaM1M5
			# Pulldown(NMOS)
				# Physical dimension
				_Nand_NMOS_ChannelWidth                 = [350,500],  # Number
				# Source_node setting
				_Nand_NMOS_Source_Via_Close2POpin_TF    = [False,False],  # True/False --> First MOS
			# Pulldown(PMOS)
				# Physical dimension
				_Nand_PMOS_ChannelWidth                 = [350,480],  # Number


	# Nor( _Unit_Num_EachStag_input에서 2,4,6,7...번째 해당하는 nor 생성)
		# MOSFET
			# Common
			_Nor_ChannelLength      = [30,30],  # Number
			_Nor_POGate_ViaMxMx     = [[0, 3],[0, 1]],  # Ex) [1,5] -> ViaM1M5
			# Pulldown(NMOS)
				# Physical dimension
				_Nor_NMOS_ChannelWidth	= [400,800],      # Number
				_Nor_NMOS_NumberofGate  = [1,3],        # Number
			# Pulldown(PMOS)
				# Physical dimension
				_Nor_PMOS_ChannelWidth	= [800,1600],      # Number
				_Nor_PMOS_NumberofGate  = [2,7],        # Number
				# Source_node setting
				_Nor_PMOS_Source_Via_Close2POpin_TF     = [False,False],  # True/False --> First MOS


	# Inv
		#Common
		_Inv_NumberofGate   = 5,
		_Inv_ChannelLength  = 30,

		# NMosfet
			# Physical dimension
			_Inv_NMOS_ChannelWidth	= 400,      # Number
			# Poly Gate setting
				# Poly Gate Via setting :
				_Inv_NMOS_POGate_ViaMxMx    = [0 ,1],     # Ex) [1,5] -> ViaM1M5

		# PMosfet
			# Physical dimension
			_Inv_PMOS_ChannelWidth  = 800,      # Number
			# Poly Gate setting
				# Poly Gate Via setting :
				_Inv_PMOS_POGate_ViaMxMx    = [0 ,1],     # Ex) [1,5] -> ViaM1M5

	# Xgate
		# Common
		_Xgate_NumberofGate     = 3,
		_Xgate_ChannelLength    = 30,

		# NMosfet
			# Physical dimension
			_Xgate_NMOS_ChannelWidth    = 400,      # Number
			# Poly Gate setting
				# Poly Gate Via setting :
				_Xgate_NMOS_POGate_ViaMxMx  = [0 ,1],     # Ex) [1,5] -> ViaM1M5

		# PMosfet
			# Physical dimension
			_Xgate_PMOS_ChannelWidth    = 800,      # Number
			# Poly Gate setting
				# Poly Gate Via setting :
				_Xgate_PMOS_POGate_ViaMxMx  = [0 ,1],     # Ex) [1,5] -> ViaM1M5

	)

	## Initially Generated _DesignParameter
	def __init__(self, _DesignParameter=None, _Name=None):
		if _DesignParameter != None:
			self._DesignParameter = _DesignParameter
		else:
			self._DesignParameter = dict(
			_Name=self._NameDeclaration(_Name=_Name),
			_GDSFile=self._GDSObjDeclaration(_GDSFile=None),
			_XYcoordAsCent=dict(_XYcoordAsCent=0),
			)

	## DesignParameter Calculation
	def _CalculateDesignParameter(self,

	# Unit
		  # Routing
		  _Routing_Dist=100,

		# Xvt
		_Unit_Xvt = 'SLVT',

		# Gate to gate dist.
		_Unit_GatetoGateDist = 100,

		# Inputs of Nand,Nor
		_Unit_Num_EachStag_input = [2,2,2], # ex) [2,3,4] 가장 마지막단(TG driving) nand input4, Nor input3, Nand input2, Nor input2 ...

		# Power rail
			# Pbody_Pulldown(NMOS)
			_Unit_Pbody_NumCont         =2,  # Number
			_Unit_Pbody_XvtTop2Pbody    = None,  # Number/None(Minimum)
			# Nbody_Pullup(PMOS)
			_Unit_Nbody_NumCont         = 2,  # Number
			_Unit_Nbody_Xvtdown2Nbody   = None,  # Number/None(Minimum)
			# PMOS and NMOS Height
			_Unit_PMOSXvt2NMOSXvt                   = 1000,  # number

		# Poly Gate setting
			# Poly Gate setting : vertical length
		_Unit_POGate_Comb_length    = None,  # None/Number


	# Nand( _Unit_Num_EachStag_input에서 1,3,5,7...번째 해당하는 nand 생성)
		# MOSFET
			# Common
			_Nand_NumberofGate      = [1,2],  # Number
			_Nand_ChannelLength     = [30,30],  # Number
			_Nand_POGate_ViaMxMx    = [[0, 1],[0, 3]],  # Ex) [1,5] -> ViaM1M5
			# Pulldown(NMOS)
				# Physical dimension
				_Nand_NMOS_ChannelWidth                 = [350,500],  # Number
				# Source_node setting
				_Nand_NMOS_Source_Via_Close2POpin_TF    = [False,False],  # True/False --> First MOS
			# Pulldown(PMOS)
				# Physical dimension
				_Nand_PMOS_ChannelWidth                 = [350,480],  # Number


	# Nor( _Unit_Num_EachStag_input에서 2,4,6,7...번째 해당하는 nor 생성)
		# MOSFET
			# Common
			_Nor_ChannelLength      = [30,30],  # Number
			_Nor_POGate_ViaMxMx     = [[0, 3],[0, 1]],  # Ex) [1,5] -> ViaM1M5
			# Pulldown(NMOS)
				# Physical dimension
				_Nor_NMOS_ChannelWidth	= [400,800],      # Number
				_Nor_NMOS_NumberofGate  = [1,3],        # Number
			# Pulldown(PMOS)
				# Physical dimension
				_Nor_PMOS_ChannelWidth	= [800,1600],      # Number
				_Nor_PMOS_NumberofGate  = [2,7],        # Number
				# Source_node setting
				_Nor_PMOS_Source_Via_Close2POpin_TF     = [False,False],  # True/False --> First MOS


	# Inv
		#Common
		_Inv_NumberofGate   = 5,
		_Inv_ChannelLength  = 30,

		# NMosfet
			# Physical dimension
			_Inv_NMOS_ChannelWidth	= 400,      # Number
			# Poly Gate setting
				# Poly Gate Via setting :
				_Inv_NMOS_POGate_ViaMxMx    = [0 ,1],     # Ex) [1,5] -> ViaM1M5

		# PMosfet
			# Physical dimension
			_Inv_PMOS_ChannelWidth  = 800,      # Number
			# Poly Gate setting
				# Poly Gate Via setting :
				_Inv_PMOS_POGate_ViaMxMx    = [0 ,1],     # Ex) [1,5] -> ViaM1M5

	# Xgate
		# Common
		_Xgate_NumberofGate     = 3,
		_Xgate_ChannelLength    = 30,

		# NMosfet
			# Physical dimension
			_Xgate_NMOS_ChannelWidth    = 400,      # Number
			# Poly Gate setting
				# Poly Gate Via setting :
				_Xgate_NMOS_POGate_ViaMxMx  = [0 ,1],     # Ex) [1,5] -> ViaM1M5

		# PMosfet
			# Physical dimension
			_Xgate_PMOS_ChannelWidth    = 800,      # Number
			# Poly Gate setting
				# Poly Gate Via setting :
				_Xgate_PMOS_POGate_ViaMxMx  = [0 ,1],     # Ex) [1,5] -> ViaM1M5


								  ):

		## Class_HEADER: Pre Defined Parameter Before Calculation
			## Load DRC library
		_DRCobj = DRC.DRC()
			## Define _name
		_Name = self._DesignParameter['_Name']['_Name']

		## CALCULATION START
		start_time = time.time()
		print('##############################')
		print('##     Calculation_Start    ##')
		print('##############################')

		## ########## ########## ########## ########## ########## ########## ########## ########## ########## ########## ########## ########## SRF_Placement
		## Gen XVT list
		_Nand_XVT = []
		for i in range(0,len(_Nand_NumberofGate)):
			_Nand_XVT.append(_Unit_Xvt)

		_Nor_XVT = []
		for i in range(0,len(_Nor_ChannelLength)):
			_Nor_XVT.append(_Unit_Xvt)

		## Copy Calculation_Parameters from low-level-block ex)copy.deepcopy(B16_nmos_power_v2._NMOS_POWER._ParametersForDesignCalculation)
		_Caculation_Parameters = copy.deepcopy(Q04_00_Placement_KJH0._Placement._ParametersForDesignCalculation)
		## Define Calculation_Parameters ex) _Caculation_Parameters['_NMOSPOWER_PbodyContact_1_Length']  = _NMOSPOWER_PbodyContact_1_Length
		_Caculation_Parameters['_GatetoGateDist'] = _Unit_GatetoGateDist

		_Caculation_Parameters['_Unit_Num_EachStag_input']          = _Unit_Num_EachStag_input

		_Caculation_Parameters['_Unit_Pbody_NumCont']               = _Unit_Pbody_NumCont
		_Caculation_Parameters['_Unit_Pbody_XvtTop2Pbody']          = _Unit_Pbody_XvtTop2Pbody
		_Caculation_Parameters['_Unit_Nbody_NumCont']               = _Unit_Nbody_NumCont
		_Caculation_Parameters['_Unit_Nbody_Xvtdown2Nbody']         = _Unit_Nbody_Xvtdown2Nbody
		_Caculation_Parameters['_Unit_PMOSXvt2NMOSXvt']             = _Unit_PMOSXvt2NMOSXvt

		_Caculation_Parameters['_Unit_POGate_Comb_length']          = _Unit_POGate_Comb_length

		_Caculation_Parameters['_Nand_NumberofGate']                = _Nand_NumberofGate
		_Caculation_Parameters['_Nand_ChannelLength']               = _Nand_ChannelLength
		_Caculation_Parameters['_Nand_POGate_ViaMxMx']              = _Nand_POGate_ViaMxMx
		_Caculation_Parameters['_Nand_XVT']                         = _Nand_XVT

		_Caculation_Parameters['_Nand_NMOS_ChannelWidth']           = _Nand_NMOS_ChannelWidth
		_Caculation_Parameters['_Nand_NMOS_Source_Via_Close2POpin_TF']  = _Nand_NMOS_Source_Via_Close2POpin_TF
		_Caculation_Parameters['_Nand_PMOS_ChannelWidth']           = _Nand_PMOS_ChannelWidth

		_Caculation_Parameters['_Nor_ChannelLength']                = _Nor_ChannelLength
		_Caculation_Parameters['_Nor_POGate_ViaMxMx']               = _Nor_POGate_ViaMxMx
		_Caculation_Parameters['_Nor_XVT']                          = _Nor_XVT

		_Caculation_Parameters['_Nor_NMOS_ChannelWidth']            = _Nor_NMOS_ChannelWidth
		_Caculation_Parameters['_Nor_NMOS_NumberofGate']            = _Nor_NMOS_NumberofGate

		_Caculation_Parameters['_Nor_PMOS_ChannelWidth']            = _Nor_PMOS_ChannelWidth
		_Caculation_Parameters['_Nor_PMOS_NumberofGate']            = _Nor_PMOS_NumberofGate

		_Caculation_Parameters['_Nor_PMOS_Source_Via_Close2POpin_TF'] = _Nor_PMOS_Source_Via_Close2POpin_TF

		_Caculation_Parameters['_Inv_NumberofGate']                 = _Inv_NumberofGate
		_Caculation_Parameters['_Inv_ChannelLength']                = _Inv_ChannelLength
		_Caculation_Parameters['_Inv_XVT']                          = _Unit_Xvt

		_Caculation_Parameters['_Inv_NMOS_ChannelWidth']            = _Inv_NMOS_ChannelWidth
		_Caculation_Parameters['_Inv_NMOS_POGate_ViaMxMx']          = _Inv_NMOS_POGate_ViaMxMx

		_Caculation_Parameters['_Inv_PMOS_ChannelWidth']            = _Inv_PMOS_ChannelWidth
		_Caculation_Parameters['_Inv_PMOS_POGate_ViaMxMx']          = _Inv_PMOS_POGate_ViaMxMx

		_Caculation_Parameters['_Xgate_NumberofGate']               = _Xgate_NumberofGate
		_Caculation_Parameters['_Xgate_ChannelLength']              = _Xgate_ChannelLength
		_Caculation_Parameters['_Xgate_XVT']                        = _Unit_Xvt

		_Caculation_Parameters['_Xgate_NMOS_ChannelWidth']          = _Xgate_NMOS_ChannelWidth
		_Caculation_Parameters['_Xgate_NMOS_POGate_ViaMxMx']        = _Xgate_NMOS_POGate_ViaMxMx

		_Caculation_Parameters['_Xgate_PMOS_ChannelWidth']          = _Xgate_PMOS_ChannelWidth
		_Caculation_Parameters['_Xgate_PMOS_POGate_ViaMxMx']        = _Xgate_PMOS_POGate_ViaMxMx

		## Generate Sref: ex)self._DesignParameter['_NMOS_POWER'] = self._SrefElementDeclaration(_DesignObj=B16_nmos_power_v2._NMOS_POWER( _DesignParameter=None, _Name='{}:NMOS_POWER'.format(_Name)))[0]
		self._DesignParameter['SRF_Placement'] = self._SrefElementDeclaration(_DesignObj=Q04_00_Placement_KJH0._Placement(_DesignParameter=None, _Name='{}:SRF_Placement'.format(_Name)))[0]

		## Define Sref Reflection: ex)self._DesignParameter['_NMOS_POWER']['_Reflect'] = [0, 0, 0]
		self._DesignParameter['SRF_Placement']['_Reflect'] = [0, 0, 0]

		## Define Sref Angle: ex)'_NMOS_POWER'
		self._DesignParameter['SRF_Placement']['_Angle'] = 0

		## Calculate Sref Layer by using Calculation_Parameter: ex)'_NMOS_POWER'
		self._DesignParameter['SRF_Placement']['_DesignObj']._CalculateDesignParameter(**_Caculation_Parameters)

		## Define Sref _XYcoordinate: ex)'_NMOS_POWER'
		self._DesignParameter['SRF_Placement']['_XYCoordinates'] = [[0, 0]]

		print('####################################')
		print('## Calculation_Start_Routing      ##')
		print('####################################')

		## ########## ########## ########## ########## ########## ########## ########## ########## ########## ########## ########## ########## Routing
		## ########## ########## ########## ########## ########## ########## ########## ########## ########## ########## ########## Routing: Define_Routing_Grid
		## Pre-defined
		_Routing_width = 50

		tmp  = self.get_param_KJH4('SRF_Placement','SRF_Xgate','SRF_PMOS','BND_Gate_Hrz_Mx')
		for i in range(0,100):
			if i ==0:
				locals()['Y_grid{}_up'.format(i)] = tmp[0][0][0][0][0]['_XY_up'][1]
				locals()['Y_grid{}_down'.format(i)] = tmp[0][0][0][0][0]['_XY_down'][1]
			else:
				locals()['Y_grid{}_up'.format(i)]   = locals()['Y_grid{}_down'.format(i-1)] - _Routing_Dist
				locals()['Y_grid{}_down'.format(i)] = locals()['Y_grid{}_up'.format(i)] - _Routing_width

			locals()['Y_grid{}'.format(i)] = 0.5*( locals()['Y_grid{}_up'.format(i)] + locals()['Y_grid{}_down'.format(i)] )

		## ########## ########## ########## ########## ########## ########## ########## ########## ########## ########## ########## Routing: Inv to Xgate
		## ########## ########## ########## ########## ########## ########## ########## ########## ########## ########## Routing: Inv to Xgate: Net1
		###### Path_element Generation 2
		## Path Name:
		Path_name = 'Net1'

		## Path Width: ***** must be even number ***
		Path_width = _Routing_width

		## tmp
		tmpXY = []
		tmpMetal = []
		tmpViaTF = []
		tmpViaDir = []
		tmpViaWid = []

		## coord1  BND_Input_Vtc_M1/BND_Out_Vtc_M2/BND_Gate_Hrz_Mx
		## P1 calculation
		P1 = [0, 0]

		tmp = self.get_param_KJH4('SRF_Placement','SRF_Inv','SRF_PMOS','BND_Gate_Hrz_Mx')
		P1[0] = tmp[0][0][0][0][0]['_XY_left'][0]
		P1[1] = locals()['Y_grid0']
		## P2 calculation
		P2 = [0, 0]
		tmp = self.get_param_KJH4('SRF_Placement','SRF_Xgate','SRF_PMOS','BND_Gate_Hrz_Mx')
		P2[0] = tmp[0][0][0][0][0]['_XY_cent'][0]
		P2[1] = np.array(P1[1])
		## Metal Layer
		Metal = 1
		## Via: True=1/False=0
		ViaTF = 0
		## Via: Vtc=1/Hrz=0/Ovl=2
		ViaDir = 1
		## Via width: None/[1,3]
		ViaWid = [2,1]

		tmpXY.append([P1, P2])
		tmpMetal.append(Metal)
		tmpViaTF.append(ViaTF)
		tmpViaDir.append(ViaDir)
		tmpViaWid.append(ViaWid)

		tmpXY = self.get_PTH_KJH(Path_name, Path_width, tmpXY, tmpMetal, tmpViaTF, tmpViaDir, tmpViaWid)

		## ########## ########## ########## ########## ########## ########## ########## ########## ########## ########## Routing: Inv to Xgate: Net2
		###### Path_element Generation 2
		## Path Name:
		Path_name = 'Net2'

		## Path Width: ***** must be even number ***
		Path_width = _Routing_width

		## tmp
		tmpXY = []
		tmpMetal = []
		tmpViaTF = []
		tmpViaDir = []
		tmpViaWid = []

		## coord1  BND_Input_Vtc_M1/BND_Out_Vtc_M2/BND_Gate_Hrz_Mx
		## P1 calculation
		P1 = [0, 0]
		tmp = self.get_param_KJH4('SRF_Placement','SRF_Inv','BND_Out_Vtc_M2')
		P1[0] = tmp[0][0][0][0]['_XY_left'][0]
		P1[1] = locals()['Y_grid1']
		## P2 calculation
		P2 = [0, 0]
		tmp = self.get_param_KJH4('SRF_Placement','SRF_Xgate','SRF_NMOS','BND_Gate_Hrz_Mx')
		P2[0] = tmp[0][0][0][0][0]['_XY_cent'][0]
		P2[1] = np.array(P1[1])
		## Metal Layer
		Metal = 1
		## Via: True=1/False=0
		ViaTF = 0
		## Via: Vtc=1/Hrz=0/Ovl=2
		ViaDir = 1
		## Via width: None/[1,3]
		ViaWid = [2,1]

		tmpXY.append([P1, P2])
		tmpMetal.append(Metal)
		tmpViaTF.append(ViaTF)
		tmpViaDir.append(ViaDir)
		tmpViaWid.append(ViaWid)

		## coord1  BND_Input_Vtc_M1/BND_Out_Vtc_M2/BND_Gate_Hrz_Mx
		## P1 calculation
		P1 = np.array(P2)
		## P2 calculation
		P2 = [0, 0]
		tmp = self.get_param_KJH4('SRF_Placement','SRF_Xgate','SRF_NMOS','BND_Gate_Hrz_Mx')
		P2 = tmp[0][0][0][0][0]['_XY_cent']
		## Metal Layer
		Metal = 1
		## Via: True=1/False=0
		ViaTF = 0
		## Via: Vtc=1/Hrz=0/Ovl=2
		ViaDir = 1
		## Via width: None/[1,3]
		ViaWid = [2,1]

		tmpXY.append([P1, P2])
		tmpMetal.append(Metal)
		tmpViaTF.append(ViaTF)
		tmpViaDir.append(ViaDir)
		tmpViaWid.append(ViaWid)

		tmpXY = self.get_PTH_KJH(Path_name, Path_width, tmpXY, tmpMetal, tmpViaTF, tmpViaDir, tmpViaWid)

		## Sref generation: ViaX
		## Define ViaX Parameter
		_Caculation_Parameters = copy.deepcopy(A02_ViaStack_KJH3._ViaStack._ParametersForDesignCalculation)
		_Caculation_Parameters['_Layer1'] = 1
		_Caculation_Parameters['_Layer2'] = 2
		_Caculation_Parameters['_COX'] = 1
		_Caculation_Parameters['_COY'] = 2

		## Sref ViaX declaration
		self._DesignParameter['SRF_Net2_ViaM1M2'] = self._SrefElementDeclaration(_DesignObj=A02_ViaStack_KJH3._ViaStack(_DesignParameter=None, _Name='{}:SRF_Net2_ViaM1M2'.format(_Name)))[0]

		## Define Sref Relection
		self._DesignParameter['SRF_Net2_ViaM1M2']['_Reflect'] = [0, 0, 0]

		## Define Sref Angle
		self._DesignParameter['SRF_Net2_ViaM1M2']['_Angle'] = 0

		## Generate Metal(x), Metal(x+1) and C0(Viax) layer:  Option: _CalculateDesignParameter, _CalculateDesignParameterXmin, _CalculateDesignParameterYmin, _CalculateDesignParameterXYsame
		self._DesignParameter['SRF_Net2_ViaM1M2']['_DesignObj']._CalculateDesignParameterXmin(**_Caculation_Parameters)

		## Calculate Sref XYcoord
		tmpXY = []
		## initialized Sref coordinate
		self._DesignParameter['SRF_Net2_ViaM1M2']['_XYCoordinates'] = [[0, 0]]
		## Calculate
		## Target_coord
		tmp1 = self.get_param_KJH4('PTH_Net2_0')
		target_coord = tmp1[0][0]['_XY_up_left']
		## Approaching_coord
		tmp2 = self.get_param_KJH4('SRF_Net2_ViaM1M2','SRF_ViaM1M2','BND_Met1Layer')
		approaching_coord = tmp2[0][0][0][0]['_XY_up_left']
		## Sref coord
		tmp3 = self.get_param_KJH4('SRF_Net2_ViaM1M2')
		Scoord = tmp3[0][0]['_XY_origin']
		## Calculate
		New_Scoord = self.get_Scoord_KJH4(target_coord, approaching_coord, Scoord)
		tmpXY.append(New_Scoord)
		## Define
		self._DesignParameter['SRF_Net2_ViaM1M2']['_XYCoordinates'] = tmpXY

		## ########## ########## ########## ########## ########## ########## ########## ########## ########## ########## ########## Routing: Nand0 to Inv: Net3
		###### Path_element Generation 2
		## Path Name:
		Path_name = 'Net3'

		## Path Width: ***** must be even number ***
		Path_width = _Routing_width

		## tmp
		tmpXY = []
		tmpMetal = []
		tmpViaTF = []
		tmpViaDir = []
		tmpViaWid = []

		## coord1  BND_Input_Vtc_M1/BND_Out_Vtc_M2/BND_Gate_Hrz_Mx
		## P1 calculation
		P1 = [0, 0]
		tmp = self.get_param_KJH4('SRF_Placement','SRF_Nand0','BND_Out_Vtc_M2')
		P1[0] = tmp[0][0][0][0]['_XY_left'][0]
		P1[1] = locals()['Y_grid1']
		## P2 calculation
		P2 = [0, 0]
		tmp = self.get_param_KJH4('SRF_Placement','SRF_Inv','BND_Input_Vtc_M1')
		P2[0] = tmp[0][0][0][0]['_XY_right'][0]
		P2[1] = np.array(P1[1])
		## Metal Layer
		Metal = 2
		## Via: True=1/False=0
		ViaTF = 0
		## Via: Vtc=1/Hrz=0/Ovl=2
		ViaDir = 1
		## Via width: None/[1,3]
		ViaWid = [2,1]

		tmpXY.append([P1, P2])
		tmpMetal.append(Metal)
		tmpViaTF.append(ViaTF)
		tmpViaDir.append(ViaDir)
		tmpViaWid.append(ViaWid)

		tmpXY = self.get_PTH_KJH(Path_name, Path_width, tmpXY, tmpMetal, tmpViaTF, tmpViaDir, tmpViaWid)

		## Sref generation: ViaX
		## Define ViaX Parameter
		_Caculation_Parameters = copy.deepcopy(A02_ViaStack_KJH3._ViaStack._ParametersForDesignCalculation)
		_Caculation_Parameters['_Layer1'] = 1
		_Caculation_Parameters['_Layer2'] = 2
		_Caculation_Parameters['_COX'] = 1
		_Caculation_Parameters['_COY'] = 2

		## Sref ViaX declaration
		self._DesignParameter['SRF_Net3_ViaM1M2'] = self._SrefElementDeclaration(_DesignObj=A02_ViaStack_KJH3._ViaStack(_DesignParameter=None, _Name='{}:SRF_Net3_ViaM1M2'.format(_Name)))[0]

		## Define Sref Relection
		self._DesignParameter['SRF_Net3_ViaM1M2']['_Reflect'] = [0, 0, 0]

		## Define Sref Angle
		self._DesignParameter['SRF_Net3_ViaM1M2']['_Angle'] = 0

		## Generate Metal(x), Metal(x+1) and C0(Viax) layer:  Option: _CalculateDesignParameter, _CalculateDesignParameterXmin, _CalculateDesignParameterYmin, _CalculateDesignParameterXYsame
		self._DesignParameter['SRF_Net3_ViaM1M2']['_DesignObj']._CalculateDesignParameterXmin(**_Caculation_Parameters)

		## Calculate Sref XYcoord
		tmpXY = []
		## initialized Sref coordinate
		self._DesignParameter['SRF_Net3_ViaM1M2']['_XYCoordinates'] = [[0, 0]]
		## Calculate
		## Target_coord
		tmp1 = self.get_param_KJH4('PTH_Net3_0')
		target_coord = tmp1[0][0]['_XY_up_right']
		## Approaching_coord
		tmp2 = self.get_param_KJH4('SRF_Net3_ViaM1M2','SRF_ViaM1M2','BND_Met2Layer')
		approaching_coord = tmp2[0][0][0][0]['_XY_up_right']
		## Sref coord
		tmp3 = self.get_param_KJH4('SRF_Net3_ViaM1M2')
		Scoord = tmp3[0][0]['_XY_origin']
		## Calculate
		New_Scoord = self.get_Scoord_KJH4(target_coord, approaching_coord, Scoord)
		tmpXY.append(New_Scoord)
		## Define
		self._DesignParameter['SRF_Net3_ViaM1M2']['_XYCoordinates'] = tmpXY

		## Y_Grid number
		Y_Grid_number = 1
		## ########## ########## ########## ########## ########## ########## ########## ########## ########## ########## ########## Routing: Nor{} to Nand{} and Nand{} to Nor{}
		for j in range(0,len(_Unit_Num_EachStag_input)-1): # J = Nand Nor Nand Nor Nand Nor...
			pass

			# BSking is iteration of for loop
			if j ==0:
				NumLogic = 1
			else:
				NumLogic = NumLogic*_Unit_Num_EachStag_input[j-1]

		## ########## ########## ########## ########## ########## ########## ########## ########## ########## ########## Routing: Nor{} to Nand{}
			if j%2==0:
				pass
				for k in range(0,NumLogic):
					for i in range(0,_Unit_Num_EachStag_input[j]):
						pass

						###### Path_element Generation 2
						## Path Name:
						Path_name = 'Net_Nor2Nand{}{}{}'.format(j,k,i)

						## Path Width: ***** must be even number ***
						Path_width = _Routing_width

						## tmp
						tmpXY = []
						tmpMetal = []
						tmpViaTF = []
						tmpViaDir = []
						tmpViaWid = []

						## coord1  BND_Input_Vtc_M1/BND_Out_Vtc_M2/BND_Gate_Hrz_Mx
						## P1 calculation
						P1 = [0, 0]
						tmp = self.get_param_KJH4('SRF_Placement', 'SRF_Nor{}'.format(j+1), 'BND_Out_Vtc_M2')
						P1[0] = tmp[0][k*_Unit_Num_EachStag_input[j]+i][0][0]['_XY_left'][0]
						P1[1] = locals()['Y_grid{}'.format(Y_Grid_number)]
						Y_Grid_number = Y_Grid_number+1
						## P2 calculation
						P2 = [0, 0]
						tmp = self.get_param_KJH4('SRF_Placement', 'SRF_Nand{}'.format(j), 'BND_Input{}_Vtc_M1'.format(i))
						P2[0] = tmp[0][k][0][0]['_XY_right'][0]
						P2[1] = np.array(P1[1])
						## Metal Layer
						Metal = 3
						## Via: True=1/False=0
						ViaTF = 0
						## Via: Vtc=1/Hrz=0/Ovl=2
						ViaDir = 1
						## Via width: None/[1,3]
						ViaWid = [2, 1]

						tmpXY.append([P1, P2])
						tmpMetal.append(Metal)
						tmpViaTF.append(ViaTF)
						tmpViaDir.append(ViaDir)
						tmpViaWid.append(ViaWid)

						tmpXY = self.get_PTH_KJH(Path_name, Path_width, tmpXY, tmpMetal, tmpViaTF, tmpViaDir, tmpViaWid)

						########################## Sref generation: ViaX
						## Define ViaX Parameter
						_Caculation_Parameters = copy.deepcopy(A02_ViaStack_KJH3._ViaStack._ParametersForDesignCalculation)
						_Caculation_Parameters['_Layer1'] = 2
						_Caculation_Parameters['_Layer2'] = 3
						_Caculation_Parameters['_COX'] = 1
						_Caculation_Parameters['_COY'] = 2

						_ViaName = 'SRF_'+ Path_name + '_ViaM2M3'
						_FullPath_name = 'PTH_' + Path_name + '_0'
						## Sref ViaX declaration
						self._DesignParameter[_ViaName] = self._SrefElementDeclaration(_DesignObj=A02_ViaStack_KJH3._ViaStack(_DesignParameter=None, _Name='{}:{}'.format(_Name,_ViaName)))[0]

						## Define Sref Relection
						self._DesignParameter[_ViaName]['_Reflect'] = [0, 0, 0]

						## Define Sref Angle
						self._DesignParameter[_ViaName]['_Angle'] = 0

						## Generate Metal(x), Metal(x+1) and C0(Viax) layer:  Option: _CalculateDesignParameter, _CalculateDesignParameterXmin, _CalculateDesignParameterYmin, _CalculateDesignParameterXYsame
						self._DesignParameter[_ViaName]['_DesignObj']._CalculateDesignParameterXmin(**_Caculation_Parameters)

						## Calculate Sref XYcoord
						tmpXY = []
						## initialized Sref coordinate
						self._DesignParameter[_ViaName]['_XYCoordinates'] = [[0, 0]]
						## Calculate
						## Target_coord
						tmp1 = self.get_param_KJH4(_FullPath_name)
						target_coord = tmp1[0][0]['_XY_down_left']
						## Approaching_coord
						tmp2 = self.get_param_KJH4(_ViaName, 'SRF_ViaM2M3', 'BND_Met2Layer')
						approaching_coord = tmp2[0][0][0][0]['_XY_down_left']
						## Sref coord
						tmp3 = self.get_param_KJH4(_ViaName)
						Scoord = tmp3[0][0]['_XY_origin']
						## Calculate
						New_Scoord = self.get_Scoord_KJH4(target_coord, approaching_coord, Scoord)
						tmpXY.append(New_Scoord)
						## Define
						self._DesignParameter[_ViaName]['_XYCoordinates'] = tmpXY

						########################## Sref generation: ViaX
						## Define ViaX Parameter
						_Caculation_Parameters = copy.deepcopy(A02_ViaStack_KJH3._ViaStack._ParametersForDesignCalculation)
						_Caculation_Parameters['_Layer1'] = 1
						_Caculation_Parameters['_Layer2'] = 3
						_Caculation_Parameters['_COX'] = 1
						_Caculation_Parameters['_COY'] = 2

						_ViaName = 'SRF_'+ Path_name + '_ViaM1M3'
						_FullPath_name = 'PTH_' + Path_name + '_0'
						## Sref ViaX declaration
						self._DesignParameter[_ViaName] = self._SrefElementDeclaration(_DesignObj=A02_ViaStack_KJH3._ViaStack(_DesignParameter=None, _Name='{}:{}'.format(_Name,_ViaName)))[0]

						## Define Sref Relection
						self._DesignParameter[_ViaName]['_Reflect'] = [0, 0, 0]

						## Define Sref Angle
						self._DesignParameter[_ViaName]['_Angle'] = 0

						## Generate Metal(x), Metal(x+1) and C0(Viax) layer:  Option: _CalculateDesignParameter, _CalculateDesignParameterXmin, _CalculateDesignParameterYmin, _CalculateDesignParameterXYsame
						self._DesignParameter[_ViaName]['_DesignObj']._CalculateDesignParameterXmin(**_Caculation_Parameters)

						## Calculate Sref XYcoord
						tmpXY = []
						## initialized Sref coordinate
						self._DesignParameter[_ViaName]['_XYCoordinates'] = [[0, 0]]
						## Calculate
						## Target_coord
						tmp1 = self.get_param_KJH4(_FullPath_name)
						target_coord = tmp1[0][0]['_XY_up_right']
						## Approaching_coord
						tmp2 = self.get_param_KJH4(_ViaName, 'SRF_ViaM1M2', 'BND_Met2Layer')
						approaching_coord = tmp2[0][0][0][0]['_XY_up_right']
						## Sref coord
						tmp3 = self.get_param_KJH4(_ViaName)
						Scoord = tmp3[0][0]['_XY_origin']
						## Calculate
						New_Scoord = self.get_Scoord_KJH4(target_coord, approaching_coord, Scoord)
						# New_Scoord[1] = New_Scoord[1] - 0.5*Path_width
						tmpXY.append(New_Scoord)
						## Define
						self._DesignParameter[_ViaName]['_XYCoordinates'] = tmpXY

		## ########## ########## ########## ########## ########## ########## ########## ########## ########## ########## Routing: Nand{} to Nor{}
			else:
				pass
				for k in range(0, NumLogic):
					for i in range(0,_Unit_Num_EachStag_input[j]):
						pass

						###### Path_element Generation 2
						## Path Name:
						Path_name = 'Net_Nand2Nor{}{}{}'.format(j,k,i)

						## Path Width: ***** must be even number ***
						Path_width = _Routing_width

						## tmp
						tmpXY = []
						tmpMetal = []
						tmpViaTF = []
						tmpViaDir = []
						tmpViaWid = []

						## coord1  BND_Input_Vtc_M1/BND_Out_Vtc_M2/BND_Gate_Hrz_Mx
						## P1 calculation
						P1 = [0, 0]
						tmp = self.get_param_KJH4('SRF_Placement', 'SRF_Nand{}'.format(j+1), 'BND_Out_Vtc_M2')
						P1[0] = tmp[0][k*_Unit_Num_EachStag_input[j]+i][0][0]['_XY_left'][0]
						P1[1] = locals()['Y_grid{}'.format(Y_Grid_number)]
						Y_Grid_number = Y_Grid_number+1
						## P2 calculation
						P2 = [0, 0]
						tmp = self.get_param_KJH4('SRF_Placement', 'SRF_Nor{}'.format(j), 'PTH_INPUT{}_2'.format(i))
						P2[0] = tmp[0][k][0][0]['_XY_right'][0]
						P2[1] = np.array(P1[1])
						## Metal Layer
						Metal = 3
						## Via: True=1/False=0
						ViaTF = 0
						## Via: Vtc=1/Hrz=0/Ovl=2
						ViaDir = 1
						## Via width: None/[1,3]
						ViaWid = [2, 1]

						tmpXY.append([P1, P2])
						tmpMetal.append(Metal)
						tmpViaTF.append(ViaTF)
						tmpViaDir.append(ViaDir)
						tmpViaWid.append(ViaWid)

						tmpXY = self.get_PTH_KJH(Path_name, Path_width, tmpXY, tmpMetal, tmpViaTF, tmpViaDir, tmpViaWid)

						########################## Sref generation: ViaX
						## Define ViaX Parameter
						_Caculation_Parameters = copy.deepcopy(A02_ViaStack_KJH3._ViaStack._ParametersForDesignCalculation)
						_Caculation_Parameters['_Layer1'] = 2
						_Caculation_Parameters['_Layer2'] = 3
						_Caculation_Parameters['_COX'] = 1
						_Caculation_Parameters['_COY'] = 2

						_ViaName = 'SRF_'+ Path_name + '_ViaM2M3'
						_FullPath_name = 'PTH_' + Path_name + '_0'
						## Sref ViaX declaration
						self._DesignParameter[_ViaName] = self._SrefElementDeclaration(_DesignObj=A02_ViaStack_KJH3._ViaStack(_DesignParameter=None, _Name='{}:{}'.format(_Name,_ViaName)))[0]

						## Define Sref Relection
						self._DesignParameter[_ViaName]['_Reflect'] = [0, 0, 0]

						## Define Sref Angle
						self._DesignParameter[_ViaName]['_Angle'] = 0

						## Generate Metal(x), Metal(x+1) and C0(Viax) layer:  Option: _CalculateDesignParameter, _CalculateDesignParameterXmin, _CalculateDesignParameterYmin, _CalculateDesignParameterXYsame
						self._DesignParameter[_ViaName]['_DesignObj']._CalculateDesignParameterXmin(**_Caculation_Parameters)

						## Calculate Sref XYcoord
						tmpXY = []
						## initialized Sref coordinate
						self._DesignParameter[_ViaName]['_XYCoordinates'] = [[0, 0]]
						## Calculate
						## Target_coord
						tmp1 = self.get_param_KJH4(_FullPath_name)
						target_coord = tmp1[0][0]['_XY_down_left']
						## Approaching_coord
						tmp2 = self.get_param_KJH4(_ViaName, 'SRF_ViaM2M3', 'BND_Met2Layer')
						approaching_coord = tmp2[0][0][0][0]['_XY_down_left']
						## Sref coord
						tmp3 = self.get_param_KJH4(_ViaName)
						Scoord = tmp3[0][0]['_XY_origin']
						## Calculate
						New_Scoord = self.get_Scoord_KJH4(target_coord, approaching_coord, Scoord)
						tmpXY.append(New_Scoord)
						## Define
						self._DesignParameter[_ViaName]['_XYCoordinates'] = tmpXY

						########################## Sref generation: ViaX
						## Define ViaX Parameter
						_Caculation_Parameters = copy.deepcopy(A02_ViaStack_KJH3._ViaStack._ParametersForDesignCalculation)
						_Caculation_Parameters['_Layer1'] = 1
						_Caculation_Parameters['_Layer2'] = 3
						_Caculation_Parameters['_COX'] = 1
						_Caculation_Parameters['_COY'] = 2

						_ViaName = 'SRF_'+ Path_name + '_ViaM1M3'
						_FullPath_name = 'PTH_' + Path_name + '_0'
						## Sref ViaX declaration
						self._DesignParameter[_ViaName] = self._SrefElementDeclaration(_DesignObj=A02_ViaStack_KJH3._ViaStack(_DesignParameter=None, _Name='{}:{}'.format(_Name,_ViaName)))[0]

						## Define Sref Relection
						self._DesignParameter[_ViaName]['_Reflect'] = [0, 0, 0]

						## Define Sref Angle
						self._DesignParameter[_ViaName]['_Angle'] = 0

						## Generate Metal(x), Metal(x+1) and C0(Viax) layer:  Option: _CalculateDesignParameter, _CalculateDesignParameterXmin, _CalculateDesignParameterYmin, _CalculateDesignParameterXYsame
						self._DesignParameter[_ViaName]['_DesignObj']._CalculateDesignParameterXmin(**_Caculation_Parameters)

						## Calculate Sref XYcoord
						tmpXY = []
						## initialized Sref coordinate
						self._DesignParameter[_ViaName]['_XYCoordinates'] = [[0, 0]]
						## Calculate
						## Target_coord
						tmp1 = self.get_param_KJH4(_FullPath_name)
						target_coord = tmp1[0][0]['_XY_up_right']
						## Approaching_coord
						tmp2 = self.get_param_KJH4(_ViaName, 'SRF_ViaM1M2', 'BND_Met2Layer')
						approaching_coord = tmp2[0][0][0][0]['_XY_up_right']
						## Sref coord
						tmp3 = self.get_param_KJH4(_ViaName)
						Scoord = tmp3[0][0]['_XY_origin']
						## Calculate
						New_Scoord = self.get_Scoord_KJH4(target_coord, approaching_coord, Scoord)
						# New_Scoord[1] = New_Scoord[1] - 0.5*Path_width
						tmpXY.append(New_Scoord)
						## Define
						self._DesignParameter[_ViaName]['_XYCoordinates'] = tmpXY
		
		## ########## ########## ########## ########## ########## ########## ########## ########## ########## ########## Xgate ViaM2M4 for Vref
		## ########## ########## ########## ########## ########## ########## ########## ########## ########## Xgate ViaM2M4 for Vref: Source ViaM2M4
		## Define ViaX Parameter
		_Caculation_Parameters = copy.deepcopy(A02_ViaStack_KJH3._ViaStack._ParametersForDesignCalculation)
		_Caculation_Parameters['_Layer1'] = 2
		_Caculation_Parameters['_Layer2'] = 4
		_Caculation_Parameters['_COX'] = 1
		_Caculation_Parameters['_COY'] = 2

		_ViaName = 'SRF_XgateInput_ViaM2M4'
		_FullPath_name = 'PTH_' + Path_name + '_0'
		## Sref ViaX declaration
		self._DesignParameter[_ViaName] = self._SrefElementDeclaration(_DesignObj=A02_ViaStack_KJH3._ViaStack(_DesignParameter=None, _Name='{}:{}'.format(_Name, _ViaName)))[0]

		## Define Sref Relection
		self._DesignParameter[_ViaName]['_Reflect'] = [0, 0, 0]

		## Define Sref Angle
		self._DesignParameter[_ViaName]['_Angle'] = 0

		## Generate Metal(x), Metal(x+1) and C0(Viax) layer:  Option: _CalculateDesignParameter, _CalculateDesignParameterXmin, _CalculateDesignParameterYmin, _CalculateDesignParameterXYsame
		self._DesignParameter[_ViaName]['_DesignObj']._CalculateDesignParameterXmin(**_Caculation_Parameters)

		## Calculate Sref XYcoord
		tmpXY = []
		## initialized Sref coordinate
		self._DesignParameter[_ViaName]['_XYCoordinates'] = [[0, 0]]
		## Calculate
		## Target_coord
		tmp1 = self.get_param_KJH4('SRF_Placement','SRF_Xgate','BND_Input_Vtc_M2')
		target_coord = tmp1[0][0][0][0]['_XY_left']
		## Approaching_coord
		tmp2 = self.get_param_KJH4(_ViaName, 'SRF_ViaM2M3', 'BND_Met2Layer')
		approaching_coord = tmp2[0][0][0][0]['_XY_up_left']
		## Sref coord
		tmp3 = self.get_param_KJH4(_ViaName)
		Scoord = tmp3[0][0]['_XY_origin']
		## Calculate
		New_Scoord = self.get_Scoord_KJH4(target_coord, approaching_coord, Scoord)
		# New_Scoord[1] = New_Scoord[1] - 0.5*Path_width
		tmpXY.append(New_Scoord)
		## Define
		self._DesignParameter[_ViaName]['_XYCoordinates'] = tmpXY
		## ########## ########## ########## ########## ########## ########## ########## ########## ########## Xgate ViaM2M4 for Vref: Source ViaM2M4
		## Define ViaX Parameter
		_Caculation_Parameters = copy.deepcopy(A02_ViaStack_KJH3._ViaStack._ParametersForDesignCalculation)
		_Caculation_Parameters['_Layer1'] = 2
		_Caculation_Parameters['_Layer2'] = 6
		_Caculation_Parameters['_COX'] = 1
		_Caculation_Parameters['_COY'] = 2

		_ViaName = 'SRF_XgateOut_ViaM2M6'
		_FullPath_name = 'PTH_' + Path_name + '_0'
		## Sref ViaX declaration
		self._DesignParameter[_ViaName] = self._SrefElementDeclaration(_DesignObj=A02_ViaStack_KJH3._ViaStack(_DesignParameter=None, _Name='{}:{}'.format(_Name, _ViaName)))[0]

		## Define Sref Relection
		self._DesignParameter[_ViaName]['_Reflect'] = [0, 0, 0]

		## Define Sref Angle
		self._DesignParameter[_ViaName]['_Angle'] = 0

		## Generate Metal(x), Metal(x+1) and C0(Viax) layer:  Option: _CalculateDesignParameter, _CalculateDesignParameterXmin, _CalculateDesignParameterYmin, _CalculateDesignParameterXYsame
		self._DesignParameter[_ViaName]['_DesignObj']._CalculateDesignParameterXmin(**_Caculation_Parameters)

		## Calculate Sref XYcoord
		tmpXY = []
		## initialized Sref coordinate
		self._DesignParameter[_ViaName]['_XYCoordinates'] = [[0, 0]]
		## Calculate
		## Target_coord
		tmp1 = self.get_param_KJH4('SRF_Placement','SRF_Xgate','BND_Output_Vtc_M2')
		target_coord = tmp1[0][0][0][0]['_XY_left']
		## Approaching_coord
		tmp2 = self.get_param_KJH4(_ViaName, 'SRF_ViaM2M3', 'BND_Met2Layer')
		approaching_coord = tmp2[0][0][0][0]['_XY_down_left']
		## Sref coord
		tmp3 = self.get_param_KJH4(_ViaName)
		Scoord = tmp3[0][0]['_XY_origin']
		## Calculate
		New_Scoord = self.get_Scoord_KJH4(target_coord, approaching_coord, Scoord)
		# New_Scoord[1] = New_Scoord[1] - 0.5*Path_width
		tmpXY.append(New_Scoord)
		## Define
		self._DesignParameter[_ViaName]['_XYCoordinates'] = tmpXY
		
		
		print('##############################')
		print('##     Calculation_End      ##')
		print('##############################')
		end_time = time.time()
		self.elapsed_time = end_time - start_time

############################################################################################################################################################ START MAIN
if __name__ == '__main__':

	''' Check Time'''
	start_time = time.time()

	from KJH91_Projects.Project_ADC.Library_and_Engine.Private import MyInfo
	from KJH91_Projects.Project_ADC.Library_and_Engine import DRCchecker_KJH0

	## LibraryName: ex)Proj_ADC_A_my_building_block
	libname = 'Proj_ZZ01_Q04_01_Routing'
	## CellName: ex)C01_cap_array_v2_84
	cellname = 'Q04_01_Routing_v2'
	_fileName = cellname + '.gds'

	''' Input Parameters for Layout Object '''
	InputParams = dict(

	# Unit
		# Routing
		_Routing_Dist = 50,

		# Xvt
		_Unit_Xvt = 'SLVT',

		# Gate to gate dist.
		_Unit_GatetoGateDist = 150,

		# Inputs of Nand,Nor
		_Unit_Num_EachStag_input = [2,2,2], # ex) [2,3,4] 가장 마지막단(TG driving) nand input4, Nor input3, Nand input2, Nor input2 ...

		# Power rail
			# Pbody_Pulldown(NMOS)
			_Unit_Pbody_NumCont         =2,  # Number
			_Unit_Pbody_XvtTop2Pbody    = None,  # Number/None(Minimum)
			# Nbody_Pullup(PMOS)
			_Unit_Nbody_NumCont         = 2,  # Number
			_Unit_Nbody_Xvtdown2Nbody   = None,  # Number/None(Minimum)
			# PMOS and NMOS Height
			_Unit_PMOSXvt2NMOSXvt                   = 1200,  # number

		# Poly Gate setting
			# Poly Gate setting : vertical length
		_Unit_POGate_Comb_length    = None,  # None/Number


	# Nand( _Unit_Num_EachStag_input에서 1,3,5,7...번째 해당하는 nand 생성)
		# MOSFET
			# Common
			_Nand_NumberofGate      = [2,2],  # Number
			_Nand_ChannelLength     = [30,30],  # Number
			_Nand_POGate_ViaMxMx    = [[0, 1],[0, 4]],  # Ex) [1,5] -> ViaM1M5
			# Pulldown(NMOS)
				# Physical dimension
				_Nand_NMOS_ChannelWidth                 = [400,500],  # Number
				# Source_node setting
				_Nand_NMOS_Source_Via_Close2POpin_TF    = [False,False],  # True/False --> First MOS
			# Pulldown(PMOS)
				# Physical dimension
				_Nand_PMOS_ChannelWidth                 = [800,480],  # Number


	# Nor( _Unit_Num_EachStag_input에서 2,4,6,7...번째 해당하는 nor 생성)
		# MOSFET
			# Common
			_Nor_ChannelLength      = [30,30],  # Number
			_Nor_POGate_ViaMxMx     = [[0, 1],[0, 4]],  # Ex) [1,5] -> ViaM1M5
			# Pulldown(NMOS)
				# Physical dimension
				_Nor_NMOS_ChannelWidth	= [400,800],      # Number
				_Nor_NMOS_NumberofGate  = [4,3],        # Number
			# Pulldown(PMOS)
				# Physical dimension
				_Nor_PMOS_ChannelWidth	= [800,1600],      # Number
				_Nor_PMOS_NumberofGate  = [8,7],        # Number
				# Source_node setting
				_Nor_PMOS_Source_Via_Close2POpin_TF     = [False,False],  # True/False --> First MOS


	# Inv
		#Common
		_Inv_NumberofGate   = 1,
		_Inv_ChannelLength  = 30,

		# NMosfet
			# Physical dimension
			_Inv_NMOS_ChannelWidth	= 400,      # Number
			# Poly Gate setting
				# Poly Gate Via setting :
				_Inv_NMOS_POGate_ViaMxMx    = [0 ,1],     # Ex) [1,5] -> ViaM1M5 -----> Fixed

		# PMosfet
			# Physical dimension
			_Inv_PMOS_ChannelWidth  = 800,      # Number
			# Poly Gate setting
				# Poly Gate Via setting :
				_Inv_PMOS_POGate_ViaMxMx    = [0 ,1],     # Ex) [1,5] -> ViaM1M5 -----> Fixed

	# Xgate
		# Common
		_Xgate_NumberofGate     = 1,
		_Xgate_ChannelLength    = 30,

		# NMosfet
			# Physical dimension
			_Xgate_NMOS_ChannelWidth    = 400,      # Number
			# Poly Gate setting
				# Poly Gate Via setting :
				_Xgate_NMOS_POGate_ViaMxMx  = [0 ,1],     # Ex) [1,5] -> ViaM1M5 -----> Fixed

		# PMosfet
			# Physical dimension
			_Xgate_PMOS_ChannelWidth    = 800,      # Number
			# Poly Gate setting
				# Poly Gate Via setting :
				_Xgate_PMOS_POGate_ViaMxMx  = [0 ,1],     # Ex) [1,5] -> ViaM1M5 -----> Fixed

	)

	'''Mode_DRCCHECK '''
	Mode_DRCCheck = False
	Num_DRCCheck = 1

	for ii in range(0, Num_DRCCheck if Mode_DRCCheck else 1):
		if Mode_DRCCheck:
			''' Input Parameters for Layout Object '''
		else:
			pass

	''' Generate Layout Object '''
	## Gen Object:
	LayoutObj = _Routing(_DesignParameter=None, _Name=cellname)
	LayoutObj._CalculateDesignParameter(**InputParams)
	LayoutObj._UpdateDesignParameter2GDSStructure(_DesignParameterInDictionary=LayoutObj._DesignParameter)
	testStreamFile = open('./{}'.format(_fileName), 'wb')
	tmp = LayoutObj._CreateGDSStream(LayoutObj._DesignParameter['_GDSFile']['_GDSFile'])
	tmp.write_binary_gds_stream(testStreamFile)
	testStreamFile.close()

	''' Check Time'''
	elapsed_time = time.time() - start_time
	m, s = divmod(elapsed_time, 60)
	h, m = divmod(m, 60)

	print('###############      Sending to FTP Server...      ##################')
	My = MyInfo.USER(DesignParameters._Technology)
	Checker = DRCchecker_KJH0.DRCchecker_KJH0(
	username=My.ID,
	password=My.PW,
	WorkDir=My.Dir_Work,
	DRCrunDir=My.Dir_DRCrun,
	libname=libname,
	cellname=cellname,
	GDSDir=My.Dir_GDS
	)
	# Checker.lib_deletion()
	Checker.cell_deletion()
	Checker.Upload2FTP()
	Checker.StreamIn(tech=DesignParameters._Technology)
	# Checker_KJH0.DRCchecker()

	print('#############################      Finished      ################################')
	print('{} Hours   {} minutes   {} seconds'.format(h, m, s))
# end of 'main():' ---------------------------------------------------------------------------------------------
