
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

import warnings
warnings.filterwarnings("ignore", category=np.VisibleDeprecationWarning)

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
from KJH91_Projects.Project_ADC.Layoutgen_code.P00_RDAC				import P00_01_Guardring
from KJH91_Projects.Project_ADC.Layoutgen_code.Q05_Decoder			import Q05_00_Decoder_KJH3



## Define Class
class _Combine(StickDiagram_KJH1._StickDiagram_KJH):

	## Input Parameters for Design Calculation: Used when import Sref
	_ParametersForDesignCalculation = dict(

	#RDAC and Decoder
		# Pside or Nside
		_RDAC_Pside=True,  # True/False

		# RDAC and Decoder delta X displacement
		_RDAC_displacement=50,

		#RDAC and Decoder Size
		_RDAC_Size = [2, 16],

		#RDAC
			# Guardring
			RDAC_Guard_NumCont 	= 3,

			# Poly Resister unit
			RDAC_ResWidth		= 1300,
			RDAC_ResLength		= 1500,
			RDAC_CONUMX			= None,
			RDAC_CONUMY			= 2,

		# Decoder
			# _Unit to Unit distance for DRC of routing
			_Decoder_Unit2UnitDist=400,  # number must be 100의 배수

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
				_Unit_Num_EachStag_input = [5], # ex) [2,3,4] 가장 마지막단(TG driving) nand input4, Nor input3, Nand input2, Nor input2 ...
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

	#RDAC and Decoder
		  # Pside or Nside
		  _RDAC_Pside=True,  # True/False

		  # RDAC and Decoder delta X displacement
		  _RDAC_displacement=50,

		#RDAC and Decoder Size
		_RDAC_Size = [2, 16],

		#RDAC
			# Guardring
			RDAC_Guard_NumCont 	= 3,

			# Poly Resister unit
			RDAC_ResWidth		= 1300,
			RDAC_ResLength		= 1500,
			RDAC_CONUMX			= None,
			RDAC_CONUMY			= 2,

		# Decoder
		  	# _Unit to Unit distance for DRC of routing
		  	_Decoder_Unit2UnitDist=400,  # number must be 100의 배수

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
				_Unit_Num_EachStag_input = [5], # ex) [2,3,4] 가장 마지막단(TG driving) nand input4, Nor input3, Nand input2, Nor input2 ...
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

								  ):

		## Class_HEADER: Pre Defined Parameter Before Calculation
			## Load DRC library
		_DRCobj = DRC.DRC()
			## Define _name
		_Name = self._DesignParameter['_Name']['_Name']

		## CALCULATION START
		RDACandDecoder_start_time = time.time()
		print('##############################')
		print('##     Calculation_Start    ##')
		print('##############################')

		## ########## ########## ########## ########## ########## ########## ########## ########## ########## ########## ########## ########## SRF_Decoder
		## Copy Calculation_Parameters from low-level-block ex)copy.deepcopy(B16_nmos_power_v2._NMOS_POWER._ParametersForDesignCalculation)
		_Caculation_Parameters = copy.deepcopy(Q05_00_Decoder_KJH3._Decoder._ParametersForDesignCalculation)
		## Define Calculation_Parameters ex) _Caculation_Parameters['_NMOSPOWER_PbodyContact_1_Length']  = _NMOSPOWER_PbodyContact_1_Length
		_Caculation_Parameters['_Decoder_Unit2UnitDist'] 				= _Decoder_Unit2UnitDist

		_Caculation_Parameters['_Decoder_Size'] 						= _RDAC_Size

		_Caculation_Parameters['_Decoder_RBit'] 						= _Decoder_RBit

		_Caculation_Parameters['_Unit_Routing_Dist'] 					= _Unit_Routing_Dist

		_Caculation_Parameters['_Unit_Xvt'] 							= _Unit_Xvt

		_Caculation_Parameters['_Unit_GatetoGateDist'] 					= _Unit_GatetoGateDist

		_Caculation_Parameters['_Unit_Num_EachStag_input']          	= _Unit_Num_EachStag_input

		_Caculation_Parameters['_Unit_Pbody_NumCont']               	= _Unit_Pbody_NumCont
		_Caculation_Parameters['_Unit_Pbody_XvtTop2Pbody']          	= _Unit_Pbody_XvtTop2Pbody
		_Caculation_Parameters['_Unit_Nbody_NumCont']               	= _Unit_Nbody_NumCont
		_Caculation_Parameters['_Unit_Nbody_Xvtdown2Nbody']         	= _Unit_Nbody_Xvtdown2Nbody
		_Caculation_Parameters['_Unit_PMOSXvt2NMOSXvt']             	= _Unit_PMOSXvt2NMOSXvt

		_Caculation_Parameters['_Unit_POGate_Comb_length']          	= _Unit_POGate_Comb_length

		_Caculation_Parameters['_Nand_NumberofGate']                	= _Nand_NumberofGate
		_Caculation_Parameters['_Nand_ChannelLength']               	= _Nand_ChannelLength
		_Caculation_Parameters['_Nand_POGate_ViaMxMx']              	= _Nand_POGate_ViaMxMx

		_Caculation_Parameters['_Nand_NMOS_ChannelWidth']           	= _Nand_NMOS_ChannelWidth
		_Caculation_Parameters['_Nand_NMOS_Source_Via_Close2POpin_TF']  = _Nand_NMOS_Source_Via_Close2POpin_TF
		_Caculation_Parameters['_Nand_PMOS_ChannelWidth']           	= _Nand_PMOS_ChannelWidth

		_Caculation_Parameters['_Nor_ChannelLength']                	= _Nor_ChannelLength
		_Caculation_Parameters['_Nor_POGate_ViaMxMx']               	= _Nor_POGate_ViaMxMx

		_Caculation_Parameters['_Nor_NMOS_ChannelWidth']            	= _Nor_NMOS_ChannelWidth
		_Caculation_Parameters['_Nor_NMOS_NumberofGate']            	= _Nor_NMOS_NumberofGate

		_Caculation_Parameters['_Nor_PMOS_ChannelWidth']            	= _Nor_PMOS_ChannelWidth
		_Caculation_Parameters['_Nor_PMOS_NumberofGate']            	= _Nor_PMOS_NumberofGate

		_Caculation_Parameters['_Nor_PMOS_Source_Via_Close2POpin_TF'] 	= _Nor_PMOS_Source_Via_Close2POpin_TF

		_Caculation_Parameters['_Inv_NumberofGate']                 	= _Inv_NumberofGate
		_Caculation_Parameters['_Inv_ChannelLength']                	= _Inv_ChannelLength

		_Caculation_Parameters['_Inv_NMOS_ChannelWidth']            	= _Inv_NMOS_ChannelWidth
		_Caculation_Parameters['_Inv_NMOS_POGate_ViaMxMx']          	= _Inv_NMOS_POGate_ViaMxMx

		_Caculation_Parameters['_Inv_PMOS_ChannelWidth']            	= _Inv_PMOS_ChannelWidth
		_Caculation_Parameters['_Inv_PMOS_POGate_ViaMxMx']          	= _Inv_PMOS_POGate_ViaMxMx

		_Caculation_Parameters['_Xgate_NumberofGate']               	= _Xgate_NumberofGate
		_Caculation_Parameters['_Xgate_ChannelLength']              	= _Xgate_ChannelLength

		_Caculation_Parameters['_Xgate_NMOS_ChannelWidth']          	= _Xgate_NMOS_ChannelWidth
		_Caculation_Parameters['_Xgate_NMOS_POGate_ViaMxMx']        	= _Xgate_NMOS_POGate_ViaMxMx

		_Caculation_Parameters['_Xgate_PMOS_ChannelWidth']          	= _Xgate_PMOS_ChannelWidth
		_Caculation_Parameters['_Xgate_PMOS_POGate_ViaMxMx']        	= _Xgate_PMOS_POGate_ViaMxMx
		
		## Generate Sref: ex)self._DesignParameter['_NMOS_POWER'] = self._SrefElementDeclaration(_DesignObj=B16_nmos_power_v2._NMOS_POWER( _DesignParameter=None, _Name='{}:NMOS_POWER'.format(_Name)))[0]
		self._DesignParameter['SRF_Decoder'] = self._SrefElementDeclaration(_DesignObj=Q05_00_Decoder_KJH3._Decoder(_DesignParameter=None, _Name='{}:SRF_Decoder'.format(_Name)))[0]

		## Define Sref Reflection: ex)self._DesignParameter['_NMOS_POWER']['_Reflect'] = [0, 0, 0]
		self._DesignParameter['SRF_Decoder']['_Reflect'] = [0, 0, 0]

		## Define Sref Angle: ex)'_NMOS_POWER'
		self._DesignParameter['SRF_Decoder']['_Angle'] = 0

		## Calculate Sref Layer by using Calculation_Parameter: ex)'_NMOS_POWER'
		self._DesignParameter['SRF_Decoder']['_DesignObj']._CalculateDesignParameter(**_Caculation_Parameters)

		## Define Sref _XYcoordinate: ex)'_NMOS_POWER'
		self._DesignParameter['SRF_Decoder']['_XYCoordinates'] = [[0, 0]]

		## ########## ########## ########## ########## ########## ########## ########## ########## ########## ########## ########## ########## SRF_RDAC
		## Copy Calculation_Parameters from low-level-block ex)copy.deepcopy(B16_nmos_power_v2._NMOS_POWER._ParametersForDesignCalculation)
		_Caculation_Parameters = copy.deepcopy(P00_01_Guardring._Guardring._ParametersForDesignCalculation)
		## Define Calculation_Parameters ex) _Caculation_Parameters['_NMOSPOWER_PbodyContact_1_Length']  = _NMOSPOWER_PbodyContact_1_Length
		_Caculation_Parameters['_Size'] 		= _RDAC_Size

		_Caculation_Parameters['_NumCont'] 		= RDAC_Guard_NumCont

		_Caculation_Parameters['_ResWidth'] 	= RDAC_ResWidth
		_Caculation_Parameters['_ResLength'] 	= RDAC_ResLength
		_Caculation_Parameters['_CONUMX'] 		= RDAC_CONUMX
		_Caculation_Parameters['_CONUMY'] 		= RDAC_CONUMY

		## Generate Sref: ex)self._DesignParameter['_NMOS_POWER'] = self._SrefElementDeclaration(_DesignObj=B16_nmos_power_v2._NMOS_POWER( _DesignParameter=None, _Name='{}:NMOS_POWER'.format(_Name)))[0]
		self._DesignParameter['SRF_RDAC'] = self._SrefElementDeclaration(_DesignObj=P00_01_Guardring._Guardring(_DesignParameter=None, _Name='{}:SRF_RDAC'.format(_Name)))[0]

		## Define Sref Reflection: ex)self._DesignParameter['_NMOS_POWER']['_Reflect'] = [0, 0, 0]
		self._DesignParameter['SRF_RDAC']['_Reflect'] = [0, 0, 0]

		## Define Sref Angle: ex)'_NMOS_POWER'
		self._DesignParameter['SRF_RDAC']['_Angle'] = 0

		## Calculate Sref Layer by using Calculation_Parameter: ex)'_NMOS_POWER'
		self._DesignParameter['SRF_RDAC']['_DesignObj']._CalculateDesignParameter(**_Caculation_Parameters)

		## Define Sref _XYcoordinate: ex)'_NMOS_POWER'
		self._DesignParameter['SRF_RDAC']['_XYCoordinates'] = [[0, 0]]

		## Get_Scoord_v4.
		## Calculate Sref XYcoord
		tmpXY = []
		## initialized Sref coordinate
		self._DesignParameter['SRF_RDAC']['_XYCoordinates'] = [[0, 0]]
		## Calculate
		## Target_coord: _XY_type1
		tmp1 = self.get_param_KJH4('SRF_Decoder','BND_Nbody_NwellExten0')
		target_coord = tmp1[0][0][0]['_XY_up_left']
		## Approaching_coord: _XY_type2
			#X
		tmp2_1 = self.get_param_KJH4('SRF_RDAC','SRF_Pbodyring','BND_ExtenMet1Layer_Bottom')
		approaching_coordx = tmp2_1[0][0][0][0]['_XY_left'][0]
			#Y
		tmp2_2 = self.get_param_KJH4('SRF_RDAC','BND_Vref{}_Vtc_M2'.format(_RDAC_Size[0]*_RDAC_Size[1]-1))
		approaching_coordy = tmp2_2[0][0][0]['_XY_down'][1]

		approaching_coord = [approaching_coordx,approaching_coordy]
		## Sref coord
		tmp3 = self.get_param_KJH4('SRF_RDAC')
		Scoord = tmp3[0][0]['_XY_origin']
		## Cal
		New_Scoord = self.get_Scoord_KJH4(target_coord, approaching_coord, Scoord)
		New_Scoord[1] = New_Scoord[1] + 500
		New_Scoord[0] = New_Scoord[0] + _RDAC_displacement
		tmpXY.append(New_Scoord)
		## Define Coordinates
		self._DesignParameter['SRF_RDAC']['_XYCoordinates'] = tmpXY
		
		## ########## ########## ########## ########## ########## ########## ########## ########## ########## ########## ########## Routing: Vref pin to Xgate
		#row
		for j in range(0,_RDAC_Size[0]):
			#column
			for i in range(0,_RDAC_Size[1]):

				###### Path_element Generation 2
				## Path Name:
				Path_name = 'VreftoXgate{}_{}'.format(j,i)

				## Path Width: ***** must be even number ***
				Path_width = 50

				## tmp
				tmpXY = []
				tmpMetal = []
				tmpViaTF = []
				tmpViaDir = []
				tmpViaWid = []

				## coord1  BND_Input_Vtc_M1/BND_Out_Vtc_M2/BND_Gate_Hrz_Mx
				## P1 calculation
				P1 = [0, 0]
				tmp = self.get_param_KJH4('SRF_RDAC', 'SRF_Vref{}_ViaM2M3'.format(j*_RDAC_Size[1]+i),'SRF_ViaM2M3','BND_Met3Layer')
				P1 = tmp[0][0][0][0][0]['_XY_right']
				## P2 calculation
				P2 = [0, 0]
				tmp = self.get_param_KJH4('SRF_Decoder','SRF_Routing_column{}'.format(j),'SRF_XgateInput_ViaM2M4','SRF_ViaM3M4','BND_Met4Layer')
				if j%2==0:
					P2[0] = tmp[0][i][0][0][0][0]['_XY_cent'][0]
				else:
					P2[0] = tmp[0][-1-i][0][0][0][0]['_XY_cent'][0]
				P2[1] = np.array(P1[1])
				## Metal Layer
				Metal = 3
				## Via: True=1/False=0
				ViaTF = 1
				## Via: Vtc=1/Hrz=0/Ovl=2
				ViaDir = 0
				## Via width: None/[1,3]
				ViaWid = [2, 1]

				tmpXY.append([P1, P2])
				tmpMetal.append(Metal)
				tmpViaTF.append(ViaTF)
				tmpViaDir.append(ViaDir)
				tmpViaWid.append(ViaWid)

				## coord2  BND_Input_Vtc_M1/BND_Out_Vtc_M2/BND_Gate_Hrz_Mx
				## P1 calculation
				P1 = np.array(P2)
				## P2 calculation
				P2 = [0, 0]
				tmp = self.get_param_KJH4('SRF_Decoder', 'SRF_Routing_column{}'.format(j), 'SRF_XgateInput_ViaM2M4', 'SRF_ViaM3M4', 'BND_Met4Layer')
				P2[0] = np.array(P1[0])
				if j%2 ==0:
					P2[1] = tmp[0][i][0][0][0][0]['_XY_down'][1]
				else:
					P2[1] = tmp[0][-1-i][0][0][0][0]['_XY_down'][1]
				## Metal Layer
				Metal = 4
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

				tmpXY = self.get_PTH_KJH2(Path_name, Path_width, tmpXY, tmpMetal, tmpViaTF, tmpViaDir, tmpViaWid,_Name)



		## ########## ########## ########## ########## ########## ########## ########## ########## ########## ########## ########## Routing: Xgate to Unitcap Combine
		## ########## ########## ########## ########## ########## ########## ########## ########## ########## ########## Routing: Xgate to Unitcap Combine: Hrz M5
		## PRe-defined
		CombineM5_Hrz_Ywidth = 450

		## Boundary_element Generation
		Element_name = 'BND_XgateOut_Hrz_M5'
		## Generate Boundary_element: ex)LayerName: METAL1 / DIFF (_ODLayer) / POLY / PIMP (_PPLayer) / NWELL / SLVT LVT RVT HVT / OP(OPpress) / CONT (CA) / PCCRIT
		self._DesignParameter[Element_name] = self._BoundaryElementDeclaration(
			_Layer=DesignParameters._LayerMapping['METAL5'][0],
			_Datatype=DesignParameters._LayerMapping['METAL5'][1],
			_XWidth=None,
			_YWidth=None,
			_XYCoordinates=[],
		)

		## Define Boundary_element _YWidth
		self._DesignParameter[Element_name]['_YWidth'] = CombineM5_Hrz_Ywidth

		## Define Boundary_element _XWidth
		tmp1 = self.get_param_KJH4('SRF_Decoder','SRF_Nbody0','SRF_NbodyContactPhyLen','BND_Met1Layer')
		tmp2 = self.get_param_KJH4('SRF_Decoder','SRF_Nbody{}'.format(_RDAC_Size[0]-1),'SRF_NbodyContactPhyLen','BND_Met1Layer')
		self._DesignParameter[Element_name]['_XWidth'] = abs(tmp2[0][0][0][0][0]['_XY_right'][0]-tmp1[0][0][0][0][0]['_XY_left'][0])

		## Define Boundary_element _XYCoordinates
		self._DesignParameter[Element_name]['_XYCoordinates'] = [[0, 0]]

		## Calculate Sref XYcoord
		tmpXY = []
		## Calculate
		## Target_coord: _XY_type1
			#Y
		if self._DesignParameter['SRF_Decoder']['_DesignObj']._DesignParameter['SRF_Routing_column{}'.format(_RDAC_Size[0]-1)]['_Reflect'] == [1,0,0]:
			tmp1_1 = self.get_param_KJH4('SRF_Decoder','SRF_Nbody{}'.format(_RDAC_Size[0]-1),'SRF_NbodyContactPhyLen','BND_Met1Layer')
			target_coordy = tmp1_1[0][0][0][0][0]['_XY_down'][1]
		else:
			tmp1_1 = self.get_param_KJH4('SRF_Decoder', 'SRF_Pbody{}'.format(_RDAC_Size[0] - 1), 'SRF_PbodyContactPhyLen', 'BND_Met1Layer')
			target_coordy = tmp1_1[0][0][0][0][0]['_XY_down'][1]
			#X
		tmp2_1 = self.get_param_KJH4('SRF_Decoder','SRF_Nbody0','SRF_NbodyContactPhyLen','BND_Met1Layer')
		target_coordx = tmp2_1[0][0][0][0][0]['_XY_left'][0]
		target_coord = [target_coordx,target_coordy]
		## Approaching_coord: _XY_type2
		tmp2 = self.get_param_KJH4(Element_name)
		approaching_coord = tmp2[0][0]['_XY_up_left']
		## Sref coord
		tmp3 = self.get_param_KJH4(Element_name)
		Scoord = tmp3[0][0]['_XY_origin']
		## Cal
		New_Scoord = self.get_Scoord_KJH4(target_coord, approaching_coord, Scoord)
		New_Scoord[1] = New_Scoord[1] - 200
		tmpXY.append(New_Scoord)
		## Define coordinates
		self._DesignParameter[Element_name]['_XYCoordinates'] = tmpXY


		## ########## ########## ########## ########## ########## ########## ########## ########## ########## ########## Routing: Xgate to Unitcap Combine: Vtc M6
		#row
		for j in range(0,_RDAC_Size[0]):
			#column
			for i in range(0,_RDAC_Size[1]):
				###### Path_element Generation 2
				## Path Name:
				Path_name = 'XgatetoUnitCap_{}_{}'.format(j,i)

				## Path Width: ***** must be even number ***
				Path_width = 50

				## tmp
				tmpXY = []
				tmpMetal = []
				tmpViaTF = []
				tmpViaDir = []
				tmpViaWid = []

				## coord1  BND_Input_Vtc_M1/BND_Out_Vtc_M2/BND_Gate_Hrz_Mx
				## P1 calculation
				P1 = [0, 0]
				tmp = self.get_param_KJH4('SRF_Decoder','SRF_Routing_column{}'.format(j),'SRF_XgateOut_ViaM2M6','SRF_ViaM5M6','BND_Met6Layer')
				P1 = tmp[0][i][0][0][0][0]['_XY_up']
				## P2 calculation
				P2 = [0, 0]
				tmp = self.get_param_KJH4('BND_XgateOut_Hrz_M5')
				P2[0] = np.array(P1[0])
				P2[1] = tmp[0][0]['_XY_down'][1]
				## Metal Layer
				Metal = 6
				## Via: True=1/False=0
				ViaTF = 1
				## Via: Vtc=1/Hrz=0/Ovl=2
				ViaDir = 1
				## Via width: None/[1,3]
				ViaWid = [1, 2]

				tmpXY.append([P1, P2])
				tmpMetal.append(Metal)
				tmpViaTF.append(ViaTF)
				tmpViaDir.append(ViaDir)
				tmpViaWid.append(ViaWid)

				tmpXY = self.get_PTH_KJH(Path_name, Path_width, tmpXY, tmpMetal, tmpViaTF, tmpViaDir, tmpViaWid)

		## ########## ########## ########## ########## ########## ########## ########## ########## ########## ########## Routing: Xgate to Unitcap Combine: ViaM5M6
		## Sref generation: ViaX
		ViaName = 'SRF_XgatetoUnitcap_ViaM5M6'
		## Define ViaX Parameter
		_Caculation_Parameters = copy.deepcopy(A02_ViaStack_KJH3._ViaStack._ParametersForDesignCalculation)
		_Caculation_Parameters['_Layer1'] = 5
		_Caculation_Parameters['_Layer2'] = 6
		_Caculation_Parameters['_COX'] = None
		_Caculation_Parameters['_COY'] = None

		## Sref ViaX declaration
		self._DesignParameter[ViaName] = self._SrefElementDeclaration(_DesignObj=A02_ViaStack_KJH3._ViaStack(_DesignParameter=None, _Name='{}:{}'.format(_Name, ViaName)))[0]

		## Define Sref Relection
		self._DesignParameter[ViaName]['_Reflect'] = [0, 0, 0]

		## Define Sref Angle
		self._DesignParameter[ViaName]['_Angle'] = 0

		## Calcuate Overlapped XYcoord
		tmp1 = self.get_param_KJH4('BND_XgateOut_Hrz_M5')
		tmp2 = self.get_param_KJH4('PTH_XgatetoUnitCap_0_0_0')
		Ovlpcoord = self.get_ovlp_KJH2(tmp1[0][0], tmp2[0][0])

		## Calcuate _COX and _COY:  None or 'MinEnclosureX' or 'MinEnclosureY' or 'SameEnclosure'
		_COX, _COY = self._CalculateNumViaByXYWidth(Ovlpcoord[0]['_Xwidth'], Ovlpcoord[0]['_Ywidth'],'MinEnclosureX')

		## Define _COX and _COY
		_Caculation_Parameters['_COX'] = _COX
		_Caculation_Parameters['_COY'] = _COY

		## Generate Metal(x), Metal(x+1) and C0(Viax) layer:  Option: _CalculateDesignParameter, _CalculateDesignParameterXmin, _CalculateDesignParameterYmin, _CalculateDesignParameterXYsame
		self._DesignParameter[ViaName]['_DesignObj']._CalculateDesignParameterXmin(**_Caculation_Parameters)

		## Calculate Sref XYcoord
		tmpXY = []
		## initialized Sref coordinate
		self._DesignParameter[ViaName]['_XYCoordinates'] = [[0, 0]]
		#row
		for j in range(0,_RDAC_Size[0]):
			#column
			for i in range(0,_RDAC_Size[1]):
				## Calculate
				## Target_coord
				tmp1 = self.get_param_KJH4('PTH_XgatetoUnitCap_{}_{}_0'.format(j,i))
				target_coord = tmp1[0][0]['_XY_down_left']
				## Approaching_coord
				tmp2 = self.get_param_KJH4(ViaName,'SRF_ViaM5M6','BND_Met6Layer')
				approaching_coord = tmp2[0][0][0][0]['_XY_down_left']
				## Sref coord
				tmp3 = self.get_param_KJH4(ViaName)
				Scoord = tmp3[0][0]['_XY_origin']
				## Calculate
				New_Scoord = self.get_Scoord_KJH4(target_coord, approaching_coord, Scoord)
				tmpXY.append(New_Scoord)
		## Define
		self._DesignParameter[ViaName]['_XYCoordinates'] = tmpXY





		## ########## ########## ########## ########## ########## ########## ########## ########## ########## ########## ########## Routing: Binary to decoder
		## ########## ########## ########## ########## ########## ########## ########## ########## ########## ########## Routing: Binary to decoder: Hrz M3
		#Pre-define
		HrzM3_Ywidth = 100
		distancefrom_BND_XgateOut_Hrz_M5 = 300
		dist_of_HrzM3 = 100

		for i in range(0,_Decoder_RBit):
		## ########## ########## ########## ########## ########## ########## ########## ########## ########## Routing: Binary to decoder: Hrz M3: D
			## Boundary_element Generation
			Element_name = 'BND_B_{}'.format(i)
			## Generate Boundary_element: ex)LayerName: METAL1 / DIFF (_ODLayer) / POLY / PIMP (_PPLayer) / NWELL / SLVT LVT RVT HVT / OP(OPpress) / CONT (CA) / PCCRIT
			self._DesignParameter[Element_name] = self._BoundaryElementDeclaration(
				_Layer=DesignParameters._LayerMapping['METAL3'][0],
				_Datatype=DesignParameters._LayerMapping['METAL3'][1],
				_XWidth=None,
				_YWidth=None,
				_XYCoordinates=[],
			)

			## Define Boundary_element _YWidth
			self._DesignParameter[Element_name]['_YWidth'] = HrzM3_Ywidth

			## Define Boundary_element _XWidth
			tmp = self.get_param_KJH4('BND_XgateOut_Hrz_M5')
			self._DesignParameter[Element_name]['_XWidth'] = tmp[0][0]['_Xwidth']

			## Define Boundary_element _XYCoordinates
			self._DesignParameter[Element_name]['_XYCoordinates'] = [[0, 0]]

			## Calculate Sref XYcoord
			tmpXY = []
			## Calculate
			## Target_coord: _XY_type1
			if i == 0:
				tmp1 = self.get_param_KJH4('BND_XgateOut_Hrz_M5')
				target_coord = tmp1[0][0]['_XY_down_left']
			else:
				tmp1 = self.get_param_KJH4('BND_Bb_{}'.format(i-1))
				target_coord = tmp1[0][0]['_XY_down_left']
			## Approaching_coord: _XY_type2
			tmp2 = self.get_param_KJH4(Element_name)
			approaching_coord = tmp2[0][0]['_XY_up_left']
			## Sref coord
			tmp3 = self.get_param_KJH4(Element_name)
			Scoord = tmp3[0][0]['_XY_origin']
			## Cal
			New_Scoord = self.get_Scoord_KJH4(target_coord, approaching_coord, Scoord)
			if i == 0:
				New_Scoord[1] = New_Scoord[1] - distancefrom_BND_XgateOut_Hrz_M5
			else:
				New_Scoord[1] = New_Scoord[1] - dist_of_HrzM3
			tmpXY.append(New_Scoord)
			## Define coordinates
			self._DesignParameter[Element_name]['_XYCoordinates'] = tmpXY

		## ########## ########## ########## ########## ########## ########## ########## ########## ########## Routing: Binary to decoder: Hrz M3: Dbar
			## Boundary_element Generation
			Element_name = 'BND_Bb_{}'.format(i)
			## Generate Boundary_element: ex)LayerName: METAL1 / DIFF (_ODLayer) / POLY / PIMP (_PPLayer) / NWELL / SLVT LVT RVT HVT / OP(OPpress) / CONT (CA) / PCCRIT
			self._DesignParameter[Element_name] = self._BoundaryElementDeclaration(
				_Layer=DesignParameters._LayerMapping['METAL3'][0],
				_Datatype=DesignParameters._LayerMapping['METAL3'][1],
				_XWidth=None,
				_YWidth=None,
				_XYCoordinates=[],
			)

			## Define Boundary_element _YWidth
			self._DesignParameter[Element_name]['_YWidth'] = HrzM3_Ywidth

			## Define Boundary_element _XWidth
			tmp = self.get_param_KJH4('BND_XgateOut_Hrz_M5')
			self._DesignParameter[Element_name]['_XWidth'] = tmp[0][0]['_Xwidth']

			## Define Boundary_element _XYCoordinates
			self._DesignParameter[Element_name]['_XYCoordinates'] = [[0, 0]]

			## Calculate Sref XYcoord
			tmpXY = []
			## Calculate
			## Target_coord: _XY_type1
			tmp1 = self.get_param_KJH4('BND_B_{}'.format(i))
			target_coord = tmp1[0][0]['_XY_down_left']
			## Approaching_coord: _XY_type2
			tmp2 = self.get_param_KJH4(Element_name)
			approaching_coord = tmp2[0][0]['_XY_up_left']
			## Sref coord
			tmp3 = self.get_param_KJH4(Element_name)
			Scoord = tmp3[0][0]['_XY_origin']
			## Cal
			New_Scoord = self.get_Scoord_KJH4(target_coord, approaching_coord, Scoord)
			New_Scoord[1] = New_Scoord[1] - dist_of_HrzM3
			tmpXY.append(New_Scoord)
			## Define coordinates
			self._DesignParameter[Element_name]['_XYCoordinates'] = tmpXY


		## ########## ########## ########## ########## ########## ########## ########## ########## ########## ########## Routing: Binary to decoder: Via

		# Define Gatename
		if len(_Unit_Num_EachStag_input) % 2 == 0:
			Gatename = 'SRF_Nor{}'.format(len(_Unit_Num_EachStag_input) - 1)
		else:
			Gatename = 'SRF_Nand{}'.format(len(_Unit_Num_EachStag_input) - 1)
		# Define GatePeriod
		GatePeriod = _Unit_Num_EachStag_input[-1]
		# Define NMOS{?}
		Mth_Input_of_Gate_Pointer = 0
		# initialized for cal
		Prev_Nth_Gate_Pointer = 0




		# Bit (start from LSB)
		for k in range(0,_Decoder_RBit):



			# Define nth of "Gatename"
			Nth_Gate_Pointer = (k // GatePeriod)
			# Control Mth_Input_of_Gate_Pointer --> NMOS{?}
			if Nth_Gate_Pointer == Prev_Nth_Gate_Pointer:
				Mth_Input_of_Gate_Pointer = Mth_Input_of_Gate_Pointer+1
			else:
				Prev_Nth_Gate_Pointer = Nth_Gate_Pointer
				Mth_Input_of_Gate_Pointer = 1



			# Check Period Flag for ping-pong...so hard to explain
			_Flag_Period = 2**k
			_Flag_Counter = 0
			_Flag_Bitbar = 1


			#row
			for j in range(0,_RDAC_Size[0]):

				# Define Metal layer of vtc
				if j % 2 == 0:
					MetalLayer = 6
					MetalLayername = 'METAL6'
				else:
					MetalLayer = 4
					MetalLayername = 'METAL4'

				#column
				for i in range(0,_RDAC_Size[1]):
					pass


					# Check Flag_Bitbar
					if _Flag_Counter < _Flag_Period:
						_Flag_Bitbar = _Flag_Bitbar
					else:
						_Flag_Bitbar = -_Flag_Bitbar
						_Flag_Counter= 0
					# Change _Flag_Bitbar depending on Gatetype
					if i ==0:
						if Gatename == 'SRF_Nor{}'.format(len(_Unit_Num_EachStag_input) - 1):
							_Flag_Bitbar = - _Flag_Bitbar
					# Increase Flag counter
					_Flag_Counter = _Flag_Counter + 1

					#
					if _Flag_Bitbar == 1:
						## ########## ########## ########## ########## ########## ########## ########## ########## ########## Routing: Binary to decoder: Vtc(metal4 or 6): Gen Via
						## Sref generation: ViaX
						ViaName = 'SRF_Bitbar{}_{}_{}_ViaM1M{}'.format(k,j,i,MetalLayer)
						## Define ViaX Parameter
						_Caculation_Parameters = copy.deepcopy(A02_ViaStack_KJH3._ViaStack._ParametersForDesignCalculation)
						_Caculation_Parameters['_Layer1'] = 1
						_Caculation_Parameters['_Layer2'] = MetalLayer
						_Caculation_Parameters['_COX'] = 2
						_Caculation_Parameters['_COY'] = 1

						## Sref ViaX declaration
						self._DesignParameter[ViaName] = self._SrefElementDeclaration(_DesignObj=A02_ViaStack_KJH3._ViaStack(_DesignParameter=None, _Name='{}:{}'.format(_Name, ViaName)))[0]

						## Define Sref Relection
						self._DesignParameter[ViaName]['_Reflect'] = [0, 0, 0]

						## Define Sref Angle
						self._DesignParameter[ViaName]['_Angle'] = 0

						## Generate Metal(x), Metal(x+1) and C0(Viax) layer:  Option: _CalculateDesignParameter, _CalculateDesignParameterXmin, _CalculateDesignParameterYmin, _CalculateDesignParameterXYsame
						self._DesignParameter[ViaName]['_DesignObj']._CalculateDesignParameterYmin(**_Caculation_Parameters)

						## Calculate Sref XYcoord
						tmpXY = []
						## initialized Sref coordinate
						self._DesignParameter[ViaName]['_XYCoordinates'] = [[0, 0]]
						## Calculate
						## Target_coord
						tmp1 = self.get_param_KJH4('SRF_Decoder','SRF_Routing_column{}'.format(j),'SRF_Placement',Gatename,'SRF_Pulldown','SRF_NMOS{}'.format( _Unit_Num_EachStag_input[-1] - Mth_Input_of_Gate_Pointer),'SRF_Gate_ViaM0Mx','SRF_ViaM0M1','BND_Met1Layer')
						if j%2==0:
							target_coord = tmp1[0][i][0][-1-Nth_Gate_Pointer][0][0][0][0][0][0]['_XY_cent']
						else:
							target_coord = tmp1[0][-1-i][0][-1-Nth_Gate_Pointer][0][0][0][0][0][0]['_XY_cent']
						## Approaching_coord
						tmp2 = self.get_param_KJH4(ViaName,'SRF_ViaM1M2','BND_Met1Layer')
						approaching_coord = tmp2[0][0][0][0]['_XY_cent']
						## Sref coord
						tmp3 = self.get_param_KJH4(ViaName)
						Scoord = tmp3[0][0]['_XY_origin']
						## Calculate
						New_Scoord = self.get_Scoord_KJH4(target_coord, approaching_coord, Scoord)
						tmpXY.append(New_Scoord)
						## Define
						self._DesignParameter[ViaName]['_XYCoordinates'] = tmpXY
					else:
						pass
						## ########## ########## ########## ########## ########## ########## ########## ########## ########## Routing: Binary to decoder: Vtc(metal4 or 6): Gen Via
						## Sref generation: ViaX
						ViaName = 'SRF_Bit{}_{}_{}_ViaM1M{}'.format(k, j, i, MetalLayer)
						## Define ViaX Parameter
						_Caculation_Parameters = copy.deepcopy(A02_ViaStack_KJH3._ViaStack._ParametersForDesignCalculation)
						_Caculation_Parameters['_Layer1'] = 1
						_Caculation_Parameters['_Layer2'] = MetalLayer
						_Caculation_Parameters['_COX'] = 2
						_Caculation_Parameters['_COY'] = 1

						## Sref ViaX declaration
						self._DesignParameter[ViaName] = self._SrefElementDeclaration(_DesignObj=A02_ViaStack_KJH3._ViaStack(_DesignParameter=None, _Name='{}:{}'.format(_Name, ViaName)))[0]

						## Define Sref Relection
						self._DesignParameter[ViaName]['_Reflect'] = [0, 0, 0]

						## Define Sref Angle
						self._DesignParameter[ViaName]['_Angle'] = 0

						## Generate Metal(x), Metal(x+1) and C0(Viax) layer:  Option: _CalculateDesignParameter, _CalculateDesignParameterXmin, _CalculateDesignParameterYmin, _CalculateDesignParameterXYsame
						self._DesignParameter[ViaName]['_DesignObj']._CalculateDesignParameterYmin(**_Caculation_Parameters)

						## Calculate Sref XYcoord
						tmpXY = []
						## initialized Sref coordinate
						self._DesignParameter[ViaName]['_XYCoordinates'] = [[0, 0]]
						## Calculate
						## Target_coord
						tmp1 = self.get_param_KJH4('SRF_Decoder', 'SRF_Routing_column{}'.format(j), 'SRF_Placement', Gatename, 'SRF_Pulldown', 'SRF_NMOS{}'.format(_Unit_Num_EachStag_input[-1] - Mth_Input_of_Gate_Pointer), 'SRF_Gate_ViaM0Mx', 'SRF_ViaM0M1', 'BND_Met1Layer')
						if j % 2 == 0:
							target_coord = tmp1[0][i][0][-1 - Nth_Gate_Pointer][0][0][0][0][0][0]['_XY_cent']
						else:
							target_coord = tmp1[0][-1 - i][0][-1 - Nth_Gate_Pointer][0][0][0][0][0][0]['_XY_cent']
						## Approaching_coord
						tmp2 = self.get_param_KJH4(ViaName, 'SRF_ViaM1M2', 'BND_Met1Layer')
						approaching_coord = tmp2[0][0][0][0]['_XY_cent']
						## Sref coord
						tmp3 = self.get_param_KJH4(ViaName)
						Scoord = tmp3[0][0]['_XY_origin']
						## Calculate
						New_Scoord = self.get_Scoord_KJH4(target_coord, approaching_coord, Scoord)
						tmpXY.append(New_Scoord)
						## Define
						self._DesignParameter[ViaName]['_XYCoordinates'] = tmpXY


		## ########## ########## ########## ########## ########## ########## ########## ########## ########## ########## Routing: Binary to decoder: Vtc

		# Bit (start from LSB)
		for k in range(0,_Decoder_RBit):

			#row
			for j in range(0,_RDAC_Size[0]):

				# Define Metal layer of vtc
				if j % 2 == 0:
					MetalLayer = 6
					MetalLayername = 'METAL6'
				else:
					MetalLayer = 4
					MetalLayername = 'METAL4'


				#column
				for i in range(0,_RDAC_Size[1]):
					pass
					ViaName = 'SRF_Bit{}_{}_{}_ViaM1M{}'.format(k, j, i, MetalLayer)

					try:
						tmp =self.get_param_KJH4(ViaName)
						var_value = ViaName
						if _RDAC_Pside == True:
							Bitbarflag = 0
						else:
							Bitbarflag = 1
					except:
						if _RDAC_Pside == True:
							Bitbarflag = 1
						else:
							Bitbarflag = 0
						var_value = 'SRF_Bitbar{}_{}_{}_ViaM1M{}'.format(k, j, i, MetalLayer)


					## Boundary_element Generation
					if Bitbarflag ==1:
						Element_name = 'BND_Bitbar{}_{}_{}_M{}'.format(k, j, i, MetalLayer)
					else:
						Element_name = 'BND_Bit{}_{}_{}_M{}'.format(k, j, i, MetalLayer)

					## Generate Boundary_element: ex)LayerName: METAL1 / DIFF (_ODLayer) / POLY / PIMP (_PPLayer) / NWELL / SLVT LVT RVT HVT / OP(OPpress) / CONT (CA) / PCCRIT
					self._DesignParameter[Element_name] = self._BoundaryElementDeclaration(
						_Layer=DesignParameters._LayerMapping[MetalLayername][0],
						_Datatype=DesignParameters._LayerMapping[MetalLayername][1],
						_XWidth=None,
						_YWidth=None,
						_XYCoordinates=[],
					)

					## Define Boundary_element _YWidth
					tmp1 = self.get_param_KJH4(var_value,'SRF_ViaM{}M{}'.format(MetalLayer-1,MetalLayer),'BND_Met{}Layer'.format(MetalLayer))
					if Bitbarflag ==1:
						tmp2 = self.get_param_KJH4('BND_Bb_{}'.format(k))
					else:
						tmp2 = self.get_param_KJH4('BND_B_{}'.format(k))
					self._DesignParameter[Element_name]['_YWidth'] = ( tmp1[0][0][0][0]['_XY_cent'][1] - tmp2[0][0]['_XY_down'][1] )

					## Define Boundary_element _XWidth
					self._DesignParameter[Element_name]['_XWidth'] = 50

					## Define Boundary_element _XYCoordinates
					self._DesignParameter[Element_name]['_XYCoordinates'] = [[0, 0]]

					## Calculate Sref XYcoord
					tmpXY = []
					## initialized Sref coordinate
					self._DesignParameter[Element_name]['_XYCoordinates'] = [[0, 0]]
					## Calculate
					## Target_coord: _XY_type1
					tmp1 = self.get_param_KJH4(var_value,'SRF_ViaM{}M{}'.format(MetalLayer-1,MetalLayer),'BND_Met{}Layer'.format(MetalLayer))
					target_coord = tmp1[0][0][0][0]['_XY_cent']
					## Approaching_coord: _XY_type2
					tmp2 = self.get_param_KJH4(Element_name)
					approaching_coord = tmp2[0][0]['_XY_up']
					## Sref coord
					tmp3 = self.get_param_KJH4(Element_name)
					Scoord = tmp3[0][0]['_XY_origin']
					## Cal
					New_Scoord = self.get_Scoord_KJH4(target_coord, approaching_coord, Scoord)
					tmpXY.append(New_Scoord)
					## Define coordinates
					self._DesignParameter[Element_name]['_XYCoordinates'] = tmpXY


		## ########## ########## ########## ########## ########## ########## ########## ########## ########## ########## Routing: Binary to decoder: Via
		# Bit (start from LSB)
		for k in range(0,_Decoder_RBit):

			#row
			for j in range(0,_RDAC_Size[0]):

				# Define Metal layer of vtc
				if j % 2 == 0:
					MetalLayer = 6
					MetalLayername = 'METAL6'
				else:
					MetalLayer = 4
					MetalLayername = 'METAL4'


				#column
				for i in range(0,_RDAC_Size[1]):
					pass
					BNDName = 'BND_Bit{}_{}_{}_M{}'.format(k, j, i, MetalLayer)

					try:
						tmp =self.get_param_KJH4(BNDName)
						var_value = BNDName
						Bitbarflag = 0
					except:
						Bitbarflag = 1
						var_value = 'BND_Bitbar{}_{}_{}_M{}'.format(k, j, i, MetalLayer)



					## Sref generation: ViaX
					if Bitbarflag ==1:
						ViaName = 'SRF_Bitbar{}_{}_{}_ViaM3M{}'.format(k, j, i, MetalLayer)
					else:
						ViaName = 'SRF_Bit{}_{}_{}_ViaM3M{}'.format(k, j, i, MetalLayer)

					## Define ViaX Parameter
					_Caculation_Parameters = copy.deepcopy(A02_ViaStack_KJH3._ViaStack._ParametersForDesignCalculation)
					_Caculation_Parameters['_Layer1'] = 3
					_Caculation_Parameters['_Layer2'] = MetalLayer
					_Caculation_Parameters['_COX'] = 2
					_Caculation_Parameters['_COY'] = 1

					## Sref ViaX declaration
					self._DesignParameter[ViaName] = self._SrefElementDeclaration(_DesignObj=A02_ViaStack_KJH3._ViaStack(_DesignParameter=None, _Name='{}:{}'.format(_Name, ViaName)))[0]

					## Define Sref Relection
					self._DesignParameter[ViaName]['_Reflect'] = [0, 0, 0]

					## Define Sref Angle
					self._DesignParameter[ViaName]['_Angle'] = 0

					## Generate Metal(x), Metal(x+1) and C0(Viax) layer:  Option: _CalculateDesignParameter, _CalculateDesignParameterXmin, _CalculateDesignParameterYmin, _CalculateDesignParameterXYsame
					self._DesignParameter[ViaName]['_DesignObj']._CalculateDesignParameterYmin(**_Caculation_Parameters)

					## Calculate Sref XYcoord
					tmpXY = []
					## initialized Sref coordinate
					self._DesignParameter[ViaName]['_XYCoordinates'] = [[0, 0]]
					## Calculate
					## Target_coord
					tmp1 = self.get_param_KJH4(var_value)
					target_coord = tmp1[0][0]['_XY_down']
					## Approaching_coord
					tmp2 = self.get_param_KJH4(ViaName,'SRF_ViaM3M4','BND_Met3Layer')
					approaching_coord = tmp2[0][0][0][0]['_XY_down']
					## Sref coord
					tmp3 = self.get_param_KJH4(ViaName)
					Scoord = tmp3[0][0]['_XY_origin']
					## Calculate
					New_Scoord = self.get_Scoord_KJH4(target_coord, approaching_coord, Scoord)
					tmpXY.append(New_Scoord)
					## Define
					self._DesignParameter[ViaName]['_XYCoordinates'] = tmpXY



		## ########## ########## ########## ########## ########## ########## ########## ########## ########## ########## ########## Routing: Not used pin to VDD or VSS

		## ########## ########## ########## ########## ########## ########## ########## ########## ########## ########## Routing: Not used pin to VDD or VSS: Cal total Input pin
		for p in range(0,len(_Unit_Num_EachStag_input)):
			pass
			if p ==0:
				Total_Input = _Unit_Num_EachStag_input[p]
			else:
				Total_Input = Total_Input * _Unit_Num_EachStag_input[p]

		
		## ########## ########## ########## ########## ########## ########## ########## ########## ########## ########## Routing: Not used pin to VDD or VSS: Define variable for Cal.
		# Define Gatename
		if len(_Unit_Num_EachStag_input) % 2 == 0:
			Gatename = 'SRF_Nor{}'.format(len(_Unit_Num_EachStag_input) - 1)
			GateType = 'Nor'
		else:
			Gatename = 'SRF_Nand{}'.format(len(_Unit_Num_EachStag_input) - 1)
			GateType = 'Nand'
			
		# Define GatePeriod
		GatePeriod = _Unit_Num_EachStag_input[-1]
		# Define NMOS{?}
		Mth_Input_of_Gate_Pointer = 0
		# initialized for cal
		Prev_Nth_Gate_Pointer = 0
		
	
		## ########## ########## ########## ########## ########## ########## ########## ########## ########## ########## Routing: Not used pin to VDD or VSS: Cal Start
		# Bit (start from LSB)
		for k in range(0,Total_Input-_Decoder_RBit):


			# Define nth of "Gatename"
			Nth_Gate_Pointer = (k // GatePeriod)
			# Control Mth_Input_of_Gate_Pointer --> NMOS{?}
			if Nth_Gate_Pointer == Prev_Nth_Gate_Pointer:
				Mth_Input_of_Gate_Pointer = Mth_Input_of_Gate_Pointer+1
			else:
				Prev_Nth_Gate_Pointer = Nth_Gate_Pointer
				Mth_Input_of_Gate_Pointer = 1


			#row
			for j in range(0,_RDAC_Size[0]):
				#column
				for i in range(0,_RDAC_Size[1]):
					pass

					# if nand
					if GateType == 'Nand':

						###### Path_element Generation 2
						## Path Name:
						Path_name = 'Nand_In2Vdd_{}{}{}'.format(k,j,i)

						## Path Width: ***** must be even number ***
						Path_width = 50

						## tmp
						tmpXY = []
						tmpMetal = []
						tmpViaTF = []
						tmpViaDir = []
						tmpViaWid = []

						## coord1
						## P1 calculation
						P1 = [0, 0]
						tmp = self.get_param_KJH4('SRF_Decoder', 'SRF_Routing_column{}'.format(j), 'SRF_Placement', Gatename, 'SRF_Pullup', 'SRF_PMOS{}'.format(Mth_Input_of_Gate_Pointer-1), 'SRF_Gate_ViaM0Mx', 'SRF_ViaM0M1', 'BND_Met1Layer')
						P1 = tmp[0][i][0][Nth_Gate_Pointer][0][0][0][0][0][0]['_XY_cent']
						## P2 calculation
						P2 = [0, 0]
						tmp = self.get_param_KJH4('SRF_Decoder', 'SRF_Routing_column{}'.format(j), 'SRF_Placement', Gatename, 'SRF_Pullup', 'SRF_PMOS{}'.format(Mth_Input_of_Gate_Pointer - 1), 'BND_Source_M1')
						P2[0] = tmp[0][i][0][Nth_Gate_Pointer][0][0][0][0]['_XY_cent'][0]
						P2[1] = np.array(P1[1])
						## Metal Layer
						Metal = 1
						## Via: True=1/False=0
						ViaTF = 0
						## Via: Vtc=1/Hrz=0/Ovl=2
						ViaDir = 2
						## Via width: None/[1,3]
						ViaWid = None

						tmpXY.append([P1, P2])
						tmpMetal.append(Metal)
						tmpViaTF.append(ViaTF)
						tmpViaDir.append(ViaDir)
						tmpViaWid.append(ViaWid)

						## coord2
						## P1 calculation
						P1 = np.array(P2)
						## P2 calculation
						P2 = [0, 0]
						tmp = self.get_param_KJH4('SRF_Decoder', 'SRF_Routing_column{}'.format(j), 'SRF_Placement', Gatename, 'SRF_Pullup', 'SRF_PMOS{}'.format(Mth_Input_of_Gate_Pointer - 1), 'BND_Source_M1')
						P2[0] = P1[0]
						P2[1] = tmp[0][i][0][Nth_Gate_Pointer][0][0][0][0]['_XY_up'][1]
						## Metal Layer
						Metal = 1
						## Via True=1/False=0
						ViaTF = 0
						## Via Vtc=1/Hrz=0/Ovl=2
						ViaDir = 2
						## Via width: None/[1,3]
						ViaWid = None

						tmpXY.append([P1, P2])
						tmpMetal.append(Metal)
						tmpViaTF.append(ViaTF)
						tmpViaDir.append(ViaDir)
						tmpViaWid.append(ViaWid)

						tmpXY = self.get_PTH_KJH(Path_name, Path_width, tmpXY, tmpMetal, tmpViaTF, tmpViaDir, tmpViaWid)

					# Gate type nor
					else:
						pass

						###### Path_element Generation 2
						## Path Name:
						Path_name = 'Nor_In2Vdd_{}{}{}'.format(k,j,i)

						## Path Width: ***** must be even number ***
						Path_width = 50

						## tmp
						tmpXY = []
						tmpMetal = []
						tmpViaTF = []
						tmpViaDir = []
						tmpViaWid = []

						## coord1
						## P1 calculation
						P1 = [0, 0]
						tmp = self.get_param_KJH4('SRF_Decoder', 'SRF_Routing_column{}'.format(j), 'SRF_Placement', Gatename, 'SRF_Pulldown', 'SRF_NMOS{}'.format(Mth_Input_of_Gate_Pointer-1), 'SRF_Gate_ViaM0Mx', 'SRF_ViaM0M1', 'BND_Met1Layer')
						P1 = tmp[0][i][0][Nth_Gate_Pointer][0][0][0][0][0][0]['_XY_cent']
						## P2 calculation
						P2 = [0, 0]
						tmp = self.get_param_KJH4('SRF_Decoder', 'SRF_Routing_column{}'.format(j), 'SRF_Placement', Gatename, 'SRF_Pulldown', 'SRF_NMOS{}'.format(Mth_Input_of_Gate_Pointer - 1), 'BND_Source_M1')
						P2[0] = tmp[0][i][0][Nth_Gate_Pointer][0][0][0][0]['_XY_cent'][0]
						P2[1] = np.array(P1[1])
						## Metal Layer
						Metal = 1
						## Via: True=1/False=0
						ViaTF = 0
						## Via: Vtc=1/Hrz=0/Ovl=2
						ViaDir = 2
						## Via width: None/[1,3]
						ViaWid = None

						tmpXY.append([P1, P2])
						tmpMetal.append(Metal)
						tmpViaTF.append(ViaTF)
						tmpViaDir.append(ViaDir)
						tmpViaWid.append(ViaWid)

						## coord2
						## P1 calculation
						P1 = np.array(P2)
						## P2 calculation
						P2 = [0, 0]
						tmp = self.get_param_KJH4('SRF_Decoder', 'SRF_Routing_column{}'.format(j), 'SRF_Placement', Gatename, 'SRF_Pulldown', 'SRF_NMOS{}'.format(Mth_Input_of_Gate_Pointer - 1), 'BND_Source_M1')
						P2[0] = P1[0]
						P2[1] = tmp[0][i][0][Nth_Gate_Pointer][0][0][0][0]['_XY_down'][1]
						## Metal Layer
						Metal = 1
						## Via True=1/False=0
						ViaTF = 0
						## Via Vtc=1/Hrz=0/Ovl=2
						ViaDir = 2
						## Via width: None/[1,3]
						ViaWid = None

						tmpXY.append([P1, P2])
						tmpMetal.append(Metal)
						tmpViaTF.append(ViaTF)
						tmpViaDir.append(ViaDir)
						tmpViaWid.append(ViaWid)

						tmpXY = self.get_PTH_KJH(Path_name, Path_width, tmpXY, tmpMetal, tmpViaTF, tmpViaDir, tmpViaWid)



		print('##############################')
		print('##     Calculation_End      ##')
		print('##############################')
		RDACandDecoder_end_time = time.time()
		self.RDACandDecoder_elapsed_time = RDACandDecoder_end_time - RDACandDecoder_start_time

############################################################################################################################################################ START MAIN
if __name__ == '__main__':

	''' Check Time'''
	start_time = time.time()

	from KJH91_Projects.Project_ADC.Library_and_Engine.Private import MyInfo
	from KJH91_Projects.Project_ADC.Library_and_Engine import DRCchecker_KJH0

	## LibraryName: ex)Proj_ADC_A_my_building_block
	libname = 'Proj_ZZ01_R00_00_Combine_KJH4'
	## CellName: ex)C01_cap_array_v2_84
	cellname = 'R00_00_Combine_v1'
	_fileName = cellname + '.gds'

	''' Input Parameters for Layout Object '''
	InputParams = dict(

	#RDAC and Decoder
		#Pside or Nside
		_RDAC_Pside = False, # True/False

		#RDAC and Decoder delta X displacement for DRC
		_RDAC_displacement = +11000,

		#RDAC and Decoder Size : Consider "_Decoder_RBit" and "_Unit_Num_EachStag_input" ex) [2, 8] --> 4 : 2*8 = 2**4
		_RDAC_Size = [1, 16],

		#RDAC
			# Guardringf
			RDAC_Guard_NumCont 	= 2,

			# Poly Resister unit
			RDAC_ResWidth		= 400,
			RDAC_ResLength		= 2514,
			RDAC_CONUMX			= None,
			RDAC_CONUMY			= 2,

		# Decoder
			# _Unit to Unit distance for DRC of routing
			_Decoder_Unit2UnitDist=400,  # number must be 100의 배수

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
				_Unit_Num_EachStag_input = [4], # ex) [2,3,4] 가장 마지막단(TG driving) nand input4, Nor input3, Nand input2, Nor input2 ...
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
						_Nand_NumberofGate      = [2],  # Number
						_Nand_ChannelLength     = [30],  # Number
						_Nand_POGate_ViaMxMx    = [[0, 1]],  # Ex) [1,5] -> ViaM1M5
						# Pulldown(NMOS)
							# Physical dimension
							_Nand_NMOS_ChannelWidth                 = [800,],  # Number
							# Source_node setting
							_Nand_NMOS_Source_Via_Close2POpin_TF    = [False],  # True/False --> First MOS
						# Pulldown(PMOS)
							# Physical dimension
							_Nand_PMOS_ChannelWidth                 = [400],  # Number
				# Nor( _Unit_Num_EachStag_input에서 2,4,6,7...번째 해당하는 nor 생성)
					# MOSFET
						# Common
						_Nor_ChannelLength      = [30,30],  		# Number
						_Nor_POGate_ViaMxMx     = [[0, 1],[0, 1]],  # Ex) [1,5] -> ViaM1M5
						# Pulldown(NMOS)
							# Physical dimension
							_Nor_NMOS_ChannelWidth	= [400,800],    # Number
							_Nor_NMOS_NumberofGate  = [1,3],        # Number
						# Pulldown(PMOS)
							# Physical dimension
							_Nor_PMOS_ChannelWidth	= [800,1600],   # Number
							_Nor_PMOS_NumberofGate  = [2,7],        # Number
							# Source_node setting
							_Nor_PMOS_Source_Via_Close2POpin_TF     = [False,False],  # True/False --> First MOS
				# Inv
					# Common
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
					_Xgate_NumberofGate     =1,
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
	LayoutObj = _Combine(_DesignParameter=None, _Name=cellname)
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
