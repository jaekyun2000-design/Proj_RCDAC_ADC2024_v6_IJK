
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

from KJH91_Projects.Project_ADC.Layoutgen_code.Q04_Decoder_Unit     import Q04_01_Routing_KJH0


## Define Class
class _Decoder(StickDiagram_KJH1._StickDiagram_KJH):

	## Input Parameters for Design Calculation: Used when import Sref
	_ParametersForDesignCalculation = dict(
	# Decoder
		# _Unit to Unit distance for DRC of routing
		_Decoder_Unit2UnitDist=400,  # number must be 100의 배수

		# _Decoder Size
		_Decoder_Size=[16, 2],
		
		# RDAC Bit
		_Decoder_RBit=5,
	# Unit
		# Routing
		_Unit_Routing_Dist=100,

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

	# Decoder
		#_Unit to Unit distance for DRC of routing
		_Decoder_Unit2UnitDist = 400, #number must be 100의 배수

		# _Decoder Size
		_Decoder_Size=[16, 2],


		# RDAC Bit
		_Decoder_RBit=5,
	# Unit
		# Routing
		_Unit_Routing_Dist=100,

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
		Decoder_start_time = time.time()
		print('##############################')
		print('##     Calculation_Start    ##')
		print('##############################')

		## ########## ########## ########## ########## ########## ########## ########## ########## ########## ########## ########## ########## SRF_Placement
		## Copy Calculation_Parameters from low-level-block ex)copy.deepcopy(B16_nmos_power_v2._NMOS_POWER._ParametersForDesignCalculation)
		_Caculation_Parameters = copy.deepcopy(Q04_01_Routing_KJH0._Routing._ParametersForDesignCalculation)
		## Define Calculation_Parameters ex) _Caculation_Parameters['_NMOSPOWER_PbodyContact_1_Length']  = _NMOSPOWER_PbodyContact_1_Length
		_Caculation_Parameters['_Routing_Dist'] 					= _Unit_Routing_Dist

		_Caculation_Parameters['_Unit_Xvt'] 						= _Unit_Xvt

		_Caculation_Parameters['_Unit_GatetoGateDist'] 				= _Unit_GatetoGateDist

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

		_Caculation_Parameters['_Nand_NMOS_ChannelWidth']           = _Nand_NMOS_ChannelWidth
		_Caculation_Parameters['_Nand_NMOS_Source_Via_Close2POpin_TF']  = _Nand_NMOS_Source_Via_Close2POpin_TF
		_Caculation_Parameters['_Nand_PMOS_ChannelWidth']           = _Nand_PMOS_ChannelWidth

		_Caculation_Parameters['_Nor_ChannelLength']                = _Nor_ChannelLength
		_Caculation_Parameters['_Nor_POGate_ViaMxMx']               = _Nor_POGate_ViaMxMx

		_Caculation_Parameters['_Nor_NMOS_ChannelWidth']            = _Nor_NMOS_ChannelWidth
		_Caculation_Parameters['_Nor_NMOS_NumberofGate']            = _Nor_NMOS_NumberofGate

		_Caculation_Parameters['_Nor_PMOS_ChannelWidth']            = _Nor_PMOS_ChannelWidth
		_Caculation_Parameters['_Nor_PMOS_NumberofGate']            = _Nor_PMOS_NumberofGate

		_Caculation_Parameters['_Nor_PMOS_Source_Via_Close2POpin_TF'] = _Nor_PMOS_Source_Via_Close2POpin_TF

		_Caculation_Parameters['_Inv_NumberofGate']                 = _Inv_NumberofGate
		_Caculation_Parameters['_Inv_ChannelLength']                = _Inv_ChannelLength

		_Caculation_Parameters['_Inv_NMOS_ChannelWidth']            = _Inv_NMOS_ChannelWidth
		_Caculation_Parameters['_Inv_NMOS_POGate_ViaMxMx']          = _Inv_NMOS_POGate_ViaMxMx

		_Caculation_Parameters['_Inv_PMOS_ChannelWidth']            = _Inv_PMOS_ChannelWidth
		_Caculation_Parameters['_Inv_PMOS_POGate_ViaMxMx']          = _Inv_PMOS_POGate_ViaMxMx

		_Caculation_Parameters['_Xgate_NumberofGate']               = _Xgate_NumberofGate
		_Caculation_Parameters['_Xgate_ChannelLength']              = _Xgate_ChannelLength

		_Caculation_Parameters['_Xgate_NMOS_ChannelWidth']          = _Xgate_NMOS_ChannelWidth
		_Caculation_Parameters['_Xgate_NMOS_POGate_ViaMxMx']        = _Xgate_NMOS_POGate_ViaMxMx

		_Caculation_Parameters['_Xgate_PMOS_ChannelWidth']          = _Xgate_PMOS_ChannelWidth
		_Caculation_Parameters['_Xgate_PMOS_POGate_ViaMxMx']        = _Xgate_PMOS_POGate_ViaMxMx
		
		for j in range(0, _Decoder_Size[0]):
			## Generate Sref: ex)self._DesignParameter['_NMOS_POWER'] = self._SrefElementDeclaration(_DesignObj=B16_nmos_power_v2._NMOS_POWER( _DesignParameter=None, _Name='{}:NMOS_POWER'.format(_Name)))[0]
			self._DesignParameter['SRF_Routing_column{}'.format(j)] = self._SrefElementDeclaration(_DesignObj=Q04_01_Routing_KJH0._Routing(_DesignParameter=None, _Name='{}:SRF_Routing_column{}'.format(_Name,j)))[0]
	
			## Define Sref Reflection: ex)self._DesignParameter['_NMOS_POWER']['_Reflect'] = [0, 0, 0]
			self._DesignParameter['SRF_Routing_column{}'.format(j)]['_Reflect'] = [0, 0, 0]
	
			## Define Sref Angle: ex)'_NMOS_POWER'
			self._DesignParameter['SRF_Routing_column{}'.format(j)]['_Angle'] = 0
	
			## Calculate Sref Layer by using Calculation_Parameter: ex)'_NMOS_POWER'
			self._DesignParameter['SRF_Routing_column{}'.format(j)]['_DesignObj']._CalculateDesignParameter(**_Caculation_Parameters)
	
			## Define Sref _XYcoordinate: ex)'_NMOS_POWER'
			self._DesignParameter['SRF_Routing_column{}'.format(j)]['_XYCoordinates'] = [[0, 0]]



		# self._DesignParameter['SRF_Routing_column1'] = copy.deepcopy(self._DesignParameter['SRF_Routing_column'])


		print('##############################')
		print('##     Calculation_End      ##')
		print('##############################')
		##Pre-defined
		# Unit2UnitDist = 400

		_Inverting_Flag = -1
		# Row
		for j in range(0,_Decoder_Size[0]):
			pass
			tmpXY = []
			#Gen New Row SRF
			# self._DesignParameter['SRF_Routing_column{}'.format(j)] = copy.deepcopy(self._DesignParameter['SRF_Routing'])
			# self._DesignParameter['SRF_Routing_column{}'.format(j)]['_DesignObj']._DesignParameter['_Name']['_Name'] = '{}:SRF_Routing_column{}'.format(_Name,j)
			# Column
			for i in range(0,_Decoder_Size[1]):
				pass

				# Inverting
				if _Inverting_Flag == 1:
					self._DesignParameter['SRF_Routing_column{}'.format(j)]['_Reflect'] = [1, 0, 0]

					# Row=1, column=1
					if j ==0 and i==0:
						tmpXY = [[0, 0]]
						## Define Coordinates
						self._DesignParameter['SRF_Routing_column{}'.format(j)]['_XYCoordinates'] = tmpXY

					# Row=2,3.. column=1
					elif j !=0 and i ==0:
						pass
						# Calculate
						## Target_coord: _XY_type1
						tmp1 = self.get_param_KJH4('SRF_Routing_column{}'.format(j - 1), 'SRF_Placement', 'BND_Pbody_M1Exten')
						target_coord = tmp1[0][0][0][0]['_XY_down_left']
						
						## Approaching_coord: _XY_type2
						tmp2 = self.get_param_KJH4('SRF_Routing_column{}'.format(j), 'SRF_Placement', 'BND_Pbody_M1Exten')
						approaching_coord = tmp2[0][0][0][0]['_XY_up_left']
						## Sref coord
						tmp3 = self.get_param_KJH4('SRF_Routing_column{}'.format(j))
						Scoord = tmp3[0][0]['_XY_origin']
						## Cal
						New_Scoord = self.get_Scoord_KJH4(target_coord, approaching_coord, Scoord)
						New_Scoord[0] = New_Scoord[0] + _Decoder_Unit2UnitDist
						tmpXY.append(New_Scoord)
						
						## Define Coordinates
						self._DesignParameter['SRF_Routing_column{}'.format(j)]['_XYCoordinates'] = tmpXY
						
					# Any column
					else:
						# Calculate
						## Target_coord: _XY_type1
						##X
						tmp1_1 = self.get_param_KJH4('SRF_Routing_column{}'.format(j), 'SRF_Placement', 'SRF_Xgate', 'SRF_NMOS', 'BND_PODummyLayer')
						tmp1_2 = self.get_param_KJH4('SRF_Routing_column{}'.format(j), 'SRF_Placement', 'SRF_Xgate', 'SRF_PMOS', 'BND_PODummyLayer')
						if tmp1_1[i - 1][0][0][0][-1][0]['_XY_right'][0] > tmp1_2[i - 1][0][0][0][-1][0]['_XY_right'][0]:
							target_coordx = tmp1_1[i - 1][0][0][0][-1][0]['_XY_right'][0]
						else:
							target_coordx = tmp1_2[i - 1][0][0][0][-1][0]['_XY_right'][0]
						##Y
						tmp1_3 = self.get_param_KJH4('SRF_Routing_column{}'.format(j), 'SRF_Placement', 'SRF_Xgate', 'SRF_PMOS', 'BND_{}Layer'.format(_Unit_Xvt))
						target_coordy = tmp1_3[i - 1][0][0][0][0][0]['_XY_down'][1]

						target_coord = [target_coordx, target_coordy]
						## Approaching_coord: _XY_type2
						##X
						if len(_Unit_Num_EachStag_input) % 2 == 0:
							_Most_left_logic = 'SRF_Nor{}'.format(len(_Unit_Num_EachStag_input) - 1)
						else:
							_Most_left_logic = 'SRF_Nand{}'.format(len(_Unit_Num_EachStag_input) - 1)

						tmp2_1 = self.get_param_KJH4('SRF_Routing_column{}'.format(j), 'SRF_Placement', _Most_left_logic, 'SRF_Pulldown', 'SRF_NMOS{}'.format(_Unit_Num_EachStag_input[-1] - 1), 'BND_PODummyLayer')
						tmp2_2 = self.get_param_KJH4('SRF_Routing_column{}'.format(j), 'SRF_Placement', _Most_left_logic, 'SRF_Pullup', 'SRF_PMOS{}'.format(_Unit_Num_EachStag_input[-1] - 1), 'BND_PODummyLayer')
						if tmp2_1[0][0][-1][0][0][0][0]['_XY_left'][0] > tmp2_2[0][0][-1][0][0][0][0]['_XY_left'][0]:
							approaching_coordx = tmp2_2[0][0][-1][0][0][0][0]['_XY_left'][0]
						else:
							approaching_coordx = tmp2_1[0][0][-1][0][0][0][0]['_XY_left'][0]
						##Y
						tmp2_3 = self.get_param_KJH4('SRF_Routing_column{}'.format(j), 'SRF_Placement', _Most_left_logic, 'SRF_Pullup', 'SRF_PMOS{}'.format(_Unit_Num_EachStag_input[-1] - 1), 'BND_{}Layer'.format(_Unit_Xvt))
						approaching_coordy = tmp2_3[0][0][-1][0][0][0][0]['_XY_down'][1]
						approaching_coord = [approaching_coordx, approaching_coordy]
						## Sref coord
						tmp3 = self.get_param_KJH4('SRF_Routing_column{}'.format(j))
						Scoord = tmp3[0][0]['_XY_origin']
						## Cal
						New_Scoord = self.get_Scoord_KJH4(target_coord, approaching_coord, Scoord)
						New_Scoord[0] = New_Scoord[0] + _Decoder_Unit2UnitDist
						tmpXY.append(New_Scoord)

						## Define Coordinates
						self._DesignParameter['SRF_Routing_column{}'.format(j)]['_XYCoordinates'] = tmpXY

				# No Inverting
				else:
					self._DesignParameter['SRF_Routing_column{}'.format(j)]['_Reflect'] = [0, 0, 0]

					# Row=1, column=1
					if j == 0 and i == 0:
						tmpXY = [[0, 0]]
						## Define Coordinates
						self._DesignParameter['SRF_Routing_column{}'.format(j)]['_XYCoordinates'] = tmpXY

					# Row=2,3.. column=1
					elif j !=0 and i ==0:
						pass
						# Calculate
						## Target_coord: _XY_type1
						tmp1 = self.get_param_KJH4('SRF_Routing_column{}'.format(j - 1), 'SRF_Placement', 'BND_Nbody_M1Exten')
						target_coord = tmp1[0][0][0][0]['_XY_down_left']
						
						## Approaching_coord: _XY_type2
						tmp2 = self.get_param_KJH4('SRF_Routing_column{}'.format(j), 'SRF_Placement', 'BND_Nbody_M1Exten')
						approaching_coord = tmp2[0][0][0][0]['_XY_up_left']
						## Sref coord
						tmp3 = self.get_param_KJH4('SRF_Routing_column{}'.format(j))
						Scoord = tmp3[0][0]['_XY_origin']
						## Cal
						New_Scoord = self.get_Scoord_KJH4(target_coord, approaching_coord, Scoord)
						New_Scoord[0] = New_Scoord[0] + _Decoder_Unit2UnitDist
						tmpXY.append(New_Scoord)
						
						## Define Coordinates
						self._DesignParameter['SRF_Routing_column{}'.format(j)]['_XYCoordinates'] = tmpXY
						
					# Any column
					else:
						# Calculate
						## Target_coord: _XY_type1
						##X
						tmp1_1 = self.get_param_KJH4('SRF_Routing_column{}'.format(j), 'SRF_Placement', 'SRF_Xgate', 'SRF_NMOS', 'BND_PODummyLayer')
						tmp1_2 = self.get_param_KJH4('SRF_Routing_column{}'.format(j), 'SRF_Placement', 'SRF_Xgate', 'SRF_PMOS', 'BND_PODummyLayer')
						if tmp1_1[i - 1][0][0][0][-1][0]['_XY_right'][0] > tmp1_2[i - 1][0][0][0][-1][0]['_XY_right'][0]:
							target_coordx = tmp1_1[i - 1][0][0][0][-1][0]['_XY_right'][0]
						else:
							target_coordx = tmp1_2[i - 1][0][0][0][-1][0]['_XY_right'][0]
						##Y
						tmp1_3 = self.get_param_KJH4('SRF_Routing_column{}'.format(j), 'SRF_Placement', 'SRF_Xgate', 'SRF_PMOS', 'BND_{}Layer'.format(_Unit_Xvt))
						target_coordy = tmp1_3[i - 1][0][0][0][0][0]['_XY_down'][1]

						target_coord = [target_coordx, target_coordy]
						## Approaching_coord: _XY_type2
						##X
						if len(_Unit_Num_EachStag_input) % 2 == 0:
							_Most_left_logic = 'SRF_Nor{}'.format(len(_Unit_Num_EachStag_input) - 1)
						else:
							_Most_left_logic = 'SRF_Nand{}'.format(len(_Unit_Num_EachStag_input) - 1)

						tmp2_1 = self.get_param_KJH4('SRF_Routing_column{}'.format(j), 'SRF_Placement', _Most_left_logic, 'SRF_Pulldown', 'SRF_NMOS{}'.format(_Unit_Num_EachStag_input[-1] - 1), 'BND_PODummyLayer')
						tmp2_2 = self.get_param_KJH4('SRF_Routing_column{}'.format(j), 'SRF_Placement', _Most_left_logic, 'SRF_Pullup', 'SRF_PMOS{}'.format(_Unit_Num_EachStag_input[-1] - 1), 'BND_PODummyLayer')
						if tmp2_1[0][0][-1][0][0][0][0]['_XY_left'][0] > tmp2_2[0][0][-1][0][0][0][0]['_XY_left'][0]:
							approaching_coordx = tmp2_2[0][0][-1][0][0][0][0]['_XY_left'][0]
						else:
							approaching_coordx = tmp2_1[0][0][-1][0][0][0][0]['_XY_left'][0]
						##Y
						tmp2_3 = self.get_param_KJH4('SRF_Routing_column{}'.format(j), 'SRF_Placement', _Most_left_logic, 'SRF_Pullup', 'SRF_PMOS{}'.format(_Unit_Num_EachStag_input[-1] - 1), 'BND_{}Layer'.format(_Unit_Xvt))
						approaching_coordy = tmp2_3[0][0][-1][0][0][0][0]['_XY_down'][1]
						approaching_coord = [approaching_coordx, approaching_coordy]
						## Sref coord
						tmp3 = self.get_param_KJH4('SRF_Routing_column{}'.format(j))
						Scoord = tmp3[0][0]['_XY_origin']
						## Cal
						New_Scoord = self.get_Scoord_KJH4(target_coord, approaching_coord, Scoord)
						New_Scoord[0] = New_Scoord[0] + _Decoder_Unit2UnitDist
						tmpXY.append(New_Scoord)

						## Define Coordinates
						self._DesignParameter['SRF_Routing_column{}'.format(j)]['_XYCoordinates'] = tmpXY
			

			# ## ########## ########## ########## ########## ########## ########## ########## ########## ########## ########## ########## ########## Body_Cover.
			# ## ########## ########## ########## ########## ########## ########## ########## ########## ########## ########## ########## Body_Cover.: Nbody
			## ########## ########## ########## ########## ########## ########## ########## ########## ########## ########## ##########  Nbody Gen.
			## Copy Calculation_Parameters from low-level-block ex)copy.deepcopy(B16_nmos_power_v2._NMOS_POWER._ParametersForDesignCalculation)
			_Caculation_Parameters = copy.deepcopy(A07_NbodyContactPhyLen_KJH3._NbodyContactPhyLen._ParametersForDesignCalculation)
			## Define Calculation_Parameters ex) _Caculation_Parameters['_NMOSPOWER_PbodyContact_1_Length']  = _NMOSPOWER_PbodyContact_1_Length
			_Caculation_Parameters['_Length'] = None
			_Caculation_Parameters['_NumCont'] = _Unit_Nbody_NumCont
			_Caculation_Parameters['_Vtc_flag'] = False
			
			## Calculate '_Length'
			# tmp = self.get_outter_KJH4('SRF_NMOS')
			tmp = self.get_param_KJH4('SRF_Routing_column{}'.format(j), 'SRF_Placement', 'BND_Nbody_M1Exten')
			_Caculation_Parameters['_Length'] = abs(tmp[-1][0][0][0]['_XY_right'][0] - tmp[0][0][0][0]['_XY_left'][0])
			
			## Generate Sref: ex)self._DesignParameter['_NMOS_POWER'] = self._SrefElementDeclaration(_DesignObj=B16_nmos_power_v2._NMOS_POWER( _DesignParameter=None, _Name='{}:NMOS_POWER'.format(_Name)))[0]
			self._DesignParameter['SRF_Nbody{}'.format(j)] = self._SrefElementDeclaration(_DesignObj=A07_NbodyContactPhyLen_KJH3._NbodyContactPhyLen(_DesignParameter=None, _Name='{}:SRF_Nbody{}'.format(_Name, j)))[0]
			
			## Define Sref Reflection: ex)self._DesignParameter['_NMOS_POWER']['_Reflect'] = [0, 0, 0]
			self._DesignParameter['SRF_Nbody{}'.format(j)]['_Reflect'] = [0, 0, 0]
			
			## Define Sref Angle: ex)'_NMOS_POWER'
			self._DesignParameter['SRF_Nbody{}'.format(j)]['_Angle'] = 0
			
			## Calculate Sref Layer by using Calculation_Parameter: ex)'_NMOS_POWER'
			self._DesignParameter['SRF_Nbody{}'.format(j)]['_DesignObj']._CalculateDesignParameter(**_Caculation_Parameters)
			
			## Define Sref _XYcoordinate: ex)'_NMOS_POWER'
			self._DesignParameter['SRF_Nbody{}'.format(j)]['_XYCoordinates'] = [[0, 0]]
			
			## Get_Scoord_v4.
			## Calculate Sref XYcoord
			tmpXY = []
			## initialized Sref coordinate
			self._DesignParameter['SRF_Nbody{}'.format(j)]['_XYCoordinates'] = [[0, 0]]
			
			## Calculate
			## Target_coord: _XY_type1
			tmp1 = self.get_param_KJH4('SRF_Routing_column{}'.format(j), 'SRF_Placement', 'BND_Nbody_M1Exten')
			if _Inverting_Flag == 1:
				target_coord = tmp1[0][0][0][0]['_XY_up_left']
			else:
				target_coord = tmp1[0][0][0][0]['_XY_down_left']
			
			## Approaching_coord: _XY_type2
			tmp2 = self.get_param_KJH4('SRF_Nbody{}'.format(j), 'SRF_NbodyContactPhyLen', 'BND_Met1Layer')
			approaching_coord = tmp2[0][0][0][0]['_XY_down_left']
			## Sref coord
			tmp3 = self.get_param_KJH4('SRF_Nbody{}'.format(j))
			Scoord = tmp3[0][0]['_XY_origin']
			## Cal
			New_Scoord = self.get_Scoord_KJH4(target_coord, approaching_coord, Scoord)
			tmpXY.append(New_Scoord)
			## Define coordinates
			self._DesignParameter['SRF_Nbody{}'.format(j)]['_XYCoordinates'] = tmpXY
			
			
			## ########## ########## ########## ########## ########## ########## ########## ########## ########## ########## Body_Cover.: Nbody: Nwell_Exten
			## Boundary_element Generation
			## Generate Boundary_element: ex)LayerName: METAL1 / DIFF (_ODLayer) / POLY / PIMP (_PPLayer) / NWELL / SLVT LVT RVT HVT / OP(OPpress) / CONT (CA) / PCCRIT
			self._DesignParameter['BND_Nbody_NwellExten{}'.format(j)] = self._BoundaryElementDeclaration(
				_Layer=DesignParameters._LayerMapping['NWELL'][0],
				_Datatype=DesignParameters._LayerMapping['NWELL'][1],
				_XWidth=None,
				_YWidth=None,
				_XYCoordinates=[],
			)

			## Define Boundary_element _YWidth
			tmp1 = self.get_param_KJH4('SRF_Routing_column{}'.format(j), 'SRF_Placement', 'BND_Nbody_NwellExten')
			self._DesignParameter['BND_Nbody_NwellExten{}'.format(j)]['_YWidth'] = tmp1[0][0][0][0]['_Ywidth']

			## Define Boundary_element _XWidth
			self._DesignParameter['BND_Nbody_NwellExten{}'.format(j)]['_XWidth'] = abs(tmp1[-1][0][0][0]['_XY_right'][0] - tmp1[0][0][0][0]['_XY_left'][0])

			## Define Boundary_element _XYCoordinates
			self._DesignParameter['BND_Nbody_NwellExten{}'.format(j)]['_XYCoordinates'] = [[0, 0]]

			## Calculate Sref XYcoord
			tmpXY = []
			## initialized Sref coordinate
			self._DesignParameter['BND_Nbody_NwellExten{}'.format(j)]['_XYCoordinates'] = [[0, 0]]
			## Calculate
			## Target_coord: _XY_type1
			tmp1 = self.get_param_KJH4('SRF_Routing_column{}'.format(j), 'SRF_Placement', 'BND_Nbody_NwellExten')
			if _Inverting_Flag==1:
				target_coord = tmp1[0][0][0][0]['_XY_up_left']
			else:
				target_coord = tmp1[0][0][0][0]['_XY_down_left']

			## Approaching_coord: _XY_type2
			tmp2 = self.get_param_KJH4('BND_Nbody_NwellExten{}'.format(j))
			approaching_coord = tmp2[0][0]['_XY_down_left']
			## Sref coord
			tmp3 = self.get_param_KJH4('BND_Nbody_NwellExten{}'.format(j))
			Scoord = tmp3[0][0]['_XY_origin']
			## Cal
			New_Scoord = self.get_Scoord_KJH4(target_coord, approaching_coord, Scoord)
			tmpXY.append(New_Scoord)
			## Define coordinates
			self._DesignParameter['BND_Nbody_NwellExten{}'.format(j)]['_XYCoordinates'] = tmpXY

			## ########## ########## ########## ########## ########## ########## ########## ########## ########## ########## Body_Cover.: Nbody: XVT_Exten
			_XVTLayer = 'BND_' + _Unit_Xvt + 'Layer'

			## Boundary_element Generation
			## Generate Boundary_element: ex)LayerName: METAL1 / DIFF (_ODLayer) / POLY / PIMP (_PPLayer) / NWELL / SLVT LVT RVT HVT / OP(OPpress) / CONT (CA) / PCCRIT
			self._DesignParameter['BND_Nbody_XvtExten{}'.format(j)] = self._BoundaryElementDeclaration(
				_Layer=DesignParameters._LayerMapping[_Unit_Xvt][0],
				_Datatype=DesignParameters._LayerMapping[_Unit_Xvt][1],
				_XWidth=None,
				_YWidth=None,
				_XYCoordinates=[],
			)

			## Define Boundary_element _YWidth
			tmp1 = self.get_param_KJH4('SRF_Routing_column{}'.format(j), 'SRF_Placement', 'BND_Nbody_XvtExten')
			self._DesignParameter['BND_Nbody_XvtExten{}'.format(j)]['_YWidth'] = tmp1[0][0][0][0]['_Ywidth']

			## Define Boundary_element _XWidth
			self._DesignParameter['BND_Nbody_XvtExten{}'.format(j)]['_XWidth'] = abs(tmp1[-1][0][0][0]['_XY_right'][0] - tmp1[0][0][0][0]['_XY_left'][0])

			## Define Boundary_element _XYCoordinates
			self._DesignParameter['BND_Nbody_XvtExten{}'.format(j)]['_XYCoordinates'] = [[0, 0]]

			## Calculate Sref XYcoord
			tmpXY = []
			## initialized Sref coordinate
			self._DesignParameter['BND_Nbody_XvtExten{}'.format(j)]['_XYCoordinates'] = [[0, 0]]
			## Calculate
			## Target_coord: _XY_type1
			tmp1 = self.get_param_KJH4('SRF_Routing_column{}'.format(j), 'SRF_Placement', 'BND_Nbody_XvtExten')
			if _Inverting_Flag==1:
				target_coord = tmp1[0][0][0][0]['_XY_up_left']
			else:
				target_coord = tmp1[0][0][0][0]['_XY_down_left']

			## Approaching_coord: _XY_type2
			tmp2 = self.get_param_KJH4('BND_Nbody_XvtExten{}'.format(j))
			approaching_coord = tmp2[0][0]['_XY_down_left']
			## Sref coord
			tmp3 = self.get_param_KJH4('BND_Nbody_XvtExten{}'.format(j))
			Scoord = tmp3[0][0]['_XY_origin']
			## Cal
			New_Scoord = self.get_Scoord_KJH4(target_coord, approaching_coord, Scoord)
			tmpXY.append(New_Scoord)
			## Define coordinates
			self._DesignParameter['BND_Nbody_XvtExten{}'.format(j)]['_XYCoordinates'] = tmpXY

			## ########## ########## ########## ########## ########## ########## ########## ########## ########## ########## Body_Cover.: Nbody: Bp_Exten

			## Boundary_element Generation
			## Generate Boundary_element: ex)LayerName: METAL1 / DIFF (_ODLayer) / POLY / PIMP (_PPLayer) / NWELL / SLVT LVT RVT HVT / OP(OPpress) / CONT (CA) / PCCRIT
			self._DesignParameter['BND_Nbody_BpExten{}'.format(j)] = self._BoundaryElementDeclaration(
				_Layer=DesignParameters._LayerMapping['PIMP'][0],
				_Datatype=DesignParameters._LayerMapping['PIMP'][1],
				_XWidth=None,
				_YWidth=None,
				_XYCoordinates=[],
			)

			## Define Boundary_element _YWidth
			tmp1 = self.get_param_KJH4('SRF_Routing_column{}'.format(j), 'SRF_Placement', 'BND_Nbody_BpExten')
			self._DesignParameter['BND_Nbody_BpExten{}'.format(j)]['_YWidth'] = tmp1[0][0][0][0]['_Ywidth']

			## Define Boundary_element _XWidth
			self._DesignParameter['BND_Nbody_BpExten{}'.format(j)]['_XWidth'] = abs(tmp1[-1][0][0][0]['_XY_right'][0] - tmp1[0][0][0][0]['_XY_left'][0])

			## Define Boundary_element _XYCoordinates
			self._DesignParameter['BND_Nbody_BpExten{}'.format(j)]['_XYCoordinates'] = [[0, 0]]

			## Calculate Sref XYcoord
			tmpXY = []
			## initialized Sref coordinate
			self._DesignParameter['BND_Nbody_BpExten{}'.format(j)]['_XYCoordinates'] = [[0, 0]]
			## Calculate
			## Target_coord: _XY_type1
			tmp1 = self.get_param_KJH4('SRF_Routing_column{}'.format(j), 'SRF_Placement', 'BND_Nbody_BpExten')
			if _Inverting_Flag==1:
				target_coord = tmp1[0][0][0][0]['_XY_up_left']
			else:
				target_coord = tmp1[0][0][0][0]['_XY_down_left']

			## Approaching_coord: _XY_type2
			tmp2 = self.get_param_KJH4('BND_Nbody_BpExten{}'.format(j))
			approaching_coord = tmp2[0][0]['_XY_down_left']
			## Sref coord
			tmp3 = self.get_param_KJH4('BND_Nbody_BpExten{}'.format(j))
			Scoord = tmp3[0][0]['_XY_origin']
			## Cal
			New_Scoord = self.get_Scoord_KJH4(target_coord, approaching_coord, Scoord)
			tmpXY.append(New_Scoord)
			## Define coordinates
			self._DesignParameter['BND_Nbody_BpExten{}'.format(j)]['_XYCoordinates'] = tmpXY





			## ########## ########## ########## ########## ########## ########## ########## ########## ########## ########## ########## Body_Cover.: Pbody
			## ########## ########## ########## ########## ########## ########## ########## ########## ########## ########## Pbody Gen.
			## Copy Calculation_Parameters from low-level-block ex)copy.deepcopy(B16_nmos_power_v2._NMOS_POWER._ParametersForDesignCalculation)
			_Caculation_Parameters = copy.deepcopy(A08_PbodyContactPhyLen_KJH3._PbodyContactPhyLen._ParametersForDesignCalculation)
			## Define Calculation_Parameters ex) _Caculation_Parameters['_NMOSPOWER_PbodyContact_1_Length']  = _NMOSPOWER_PbodyContact_1_Length
			_Caculation_Parameters['_Length'] = None
			_Caculation_Parameters['_NumCont'] = _Unit_Nbody_NumCont
			_Caculation_Parameters['_Vtc_flag'] = False
			
			## Calculate '_Length'
			tmp = self.get_param_KJH4('SRF_Routing_column{}'.format(j), 'SRF_Placement', 'BND_Pbody_M1Exten')
			_Caculation_Parameters['_Length'] = abs(tmp[-1][0][0][0]['_XY_right'][0] - tmp[0][0][0][0]['_XY_left'][0])
			
			## Generate Sref: ex)self._DesignParameter['_NMOS_POWER'] = self._SrefElementDeclaration(_DesignObj=B16_nmos_power_v2._NMOS_POWER( _DesignParameter=None, _Name='{}:NMOS_POWER'.format(_Name)))[0]
			self._DesignParameter['SRF_Pbody{}'.format(j)] = self._SrefElementDeclaration(_DesignObj=A08_PbodyContactPhyLen_KJH3._PbodyContactPhyLen(_DesignParameter=None, _Name='{}:SRF_Pbody{}'.format(_Name, j)))[0]
			
			## Define Sref Reflection: ex)self._DesignParameter['_NMOS_POWER']['_Reflect'] = [0, 0, 0]
			self._DesignParameter['SRF_Pbody{}'.format(j)]['_Reflect'] = [0, 0, 0]
			
			## Define Sref Angle: ex)'_NMOS_POWER'
			self._DesignParameter['SRF_Pbody{}'.format(j)]['_Angle'] = 0
			
			## Calculate Sref Layer by using Calculation_Parameter: ex)'_NMOS_POWER'
			self._DesignParameter['SRF_Pbody{}'.format(j)]['_DesignObj']._CalculateDesignParameter(**_Caculation_Parameters)
			
			## Define Sref _XYcoordinate: ex)'_NMOS_POWER'
			self._DesignParameter['SRF_Pbody{}'.format(j)]['_XYCoordinates'] = [[0, 0]]
			
			## Get_Scoord_v4.
			## Calculate Sref XYcoord
			tmpXY = []
			## initialized Sref coordinate
			self._DesignParameter['SRF_Pbody{}'.format(j)]['_XYCoordinates'] = [[0, 0]]
			
			## Calculate
			## Target_coord: _XY_type1
			tmp1 = self.get_param_KJH4('SRF_Routing_column{}'.format(j), 'SRF_Placement', 'BND_Pbody_M1Exten')
			if _Inverting_Flag == 1:
				target_coord = tmp1[0][0][0][0]['_XY_up_left']
			else:
				target_coord = tmp1[0][0][0][0]['_XY_down_left']
			
			## Approaching_coord: _XY_type2
			tmp2 = self.get_param_KJH4('SRF_Pbody{}'.format(j), 'SRF_PbodyContactPhyLen', 'BND_Met1Layer')
			approaching_coord = tmp2[0][0][0][0]['_XY_down_left']
			## Sref coord
			tmp3 = self.get_param_KJH4('SRF_Pbody{}'.format(j))
			Scoord = tmp3[0][0]['_XY_origin']
			## Cal
			New_Scoord = self.get_Scoord_KJH4(target_coord, approaching_coord, Scoord)
			tmpXY.append(New_Scoord)
			## Define coordinates
			self._DesignParameter['SRF_Pbody{}'.format(j)]['_XYCoordinates'] = tmpXY

			## ########## ########## ########## ########## ########## ########## ########## ########## ########## ########## Body_Cover.: Pbody: XVT_Exten
			_XVTLayer = 'BND_' + _Unit_Xvt + 'Layer'

			## Boundary_element Generation
			## Generate Boundary_element: ex)LayerName: METAL1 / DIFF (_ODLayer) / POLY / PIMP (_PPLayer) / NWELL / SLVT LVT RVT HVT / OP(OPpress) / CONT (CA) / PCCRIT
			self._DesignParameter['BND_Pbody_XvtExten{}'.format(j)] = self._BoundaryElementDeclaration(
				_Layer=DesignParameters._LayerMapping[_Unit_Xvt][0],
				_Datatype=DesignParameters._LayerMapping[_Unit_Xvt][1],
				_XWidth=None,
				_YWidth=None,
				_XYCoordinates=[],
			)

			## Define Boundary_element _YWidth
			tmp1 = self.get_param_KJH4('SRF_Routing_column{}'.format(j), 'SRF_Placement', 'BND_Pbody_XvtExten')
			self._DesignParameter['BND_Pbody_XvtExten{}'.format(j)]['_YWidth'] = tmp1[0][0][0][0]['_Ywidth']

			## Define Boundary_element _XWidth
			self._DesignParameter['BND_Pbody_XvtExten{}'.format(j)]['_XWidth'] = abs(tmp1[-1][0][0][0]['_XY_right'][0] - tmp1[0][0][0][0]['_XY_left'][0])

			## Define Boundary_element _XYCoordinates
			self._DesignParameter['BND_Pbody_XvtExten{}'.format(j)]['_XYCoordinates'] = [[0, 0]]

			## Calculate Sref XYcoord
			tmpXY = []
			## initialized Sref coordinate
			self._DesignParameter['BND_Pbody_XvtExten{}'.format(j)]['_XYCoordinates'] = [[0, 0]]
			## Calculate
			## Target_coord: _XY_type1
			tmp1 = self.get_param_KJH4('SRF_Routing_column{}'.format(j), 'SRF_Placement', 'BND_Pbody_XvtExten')
			if _Inverting_Flag==1:
				target_coord = tmp1[0][0][0][0]['_XY_up_left']
			else:
				target_coord = tmp1[0][0][0][0]['_XY_down_left']

			## Approaching_coord: _XY_type2
			tmp2 = self.get_param_KJH4('BND_Pbody_XvtExten{}'.format(j))
			approaching_coord = tmp2[0][0]['_XY_down_left']
			## Sref coord
			tmp3 = self.get_param_KJH4('BND_Pbody_XvtExten{}'.format(j))
			Scoord = tmp3[0][0]['_XY_origin']
			## Cal
			New_Scoord = self.get_Scoord_KJH4(target_coord, approaching_coord, Scoord)
			tmpXY.append(New_Scoord)
			## Define coordinates
			self._DesignParameter['BND_Pbody_XvtExten{}'.format(j)]['_XYCoordinates'] = tmpXY

			_Inverting_Flag = -_Inverting_Flag


		print('##############################')
		print('##     Calculation_End      ##')
		print('##############################')
		Decoder_end_time = time.time()
		self.Decoder_elapsed_time = Decoder_end_time - Decoder_start_time

############################################################################################################################################################ START MAIN
if __name__ == '__main__':

	''' Check Time'''
	start_time = time.time()

	from KJH91_Projects.Project_ADC.Library_and_Engine.Private import MyInfo
	from KJH91_Projects.Project_ADC.Library_and_Engine import DRCchecker_KJH0

	## LibraryName: ex)Proj_ADC_A_my_building_block
	libname = 'Proj_ZZ01_Q05_00_Decoder_KJH3'
	## CellName: ex)C01_cap_array_v2_84
	cellname = 'Q05_00_Decoder_v2'
	_fileName = cellname + '.gds'

	''' Input Parameters for Layout Object '''
	InputParams = dict(
	# Decoder
		#_Unit to Unit distance for DRC of routing
		_Decoder_Unit2UnitDist = 400, #number must be 100의 배수

		#_Decoder Size
		_Decoder_Size =[2,16],
		
		# RDAC Bit
		_Decoder_RBit = 4,

	# Unit
		# Routing
		_Unit_Routing_Dist = 50,

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
	LayoutObj = _Decoder(_DesignParameter=None, _Name=cellname)
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
	Checker.lib_deletion()
	Checker.cell_deletion()
	Checker.Upload2FTP()
	Checker.StreamIn(tech=DesignParameters._Technology)
	# Checker_KJH0.DRCchecker()



	print('#############################      Finished      ################################')
	print('{} Hours   {} minutes   {} seconds'.format(h,m,s))

# end of 'main():' ---------------------------------------------------------------------------------------------
