
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
from KJH91_Projects.Project_ADC.Layoutgen_code.A_Basic_Building_Block import A14_Mosfet_KJH3
from KJH91_Projects.Project_ADC.Layoutgen_code.R00_Combine_P00_Q05 import R00_00_Combine_KJH3


## Define Class
class _Test11(StickDiagram_KJH1._StickDiagram_KJH):

	## Input Parameters for Design Calculation: Used when import Sref
	_ParametersForDesignCalculation = dict(

		_NumbofRbit=5,

	#RDAC and Decoder
		#RDAC and Decoder delta X displacement for DRC
		_RDAC_displacement = -100,

		#RDAC and Decoder Size : Consider "_Decoder_RBit" and "_Unit_Num_EachStag_input" ex) [2, 8] --> 4 : 2*8 = 2**4
		_RDAC_Size = [1, 4],

		#RDAC
			# Guardring
			RDAC_Guard_NumCont 	= 2,

			# Poly Resister unit
			RDAC_ResWidth		= 2000,
			RDAC_ResLength		= 1500,
			RDAC_CONUMX			= None,
			RDAC_CONUMY			= 2,

		# Decoder
			# _Unit to Unit distance for DRC of routing
			_Decoder_Unit2UnitDist=400,  # number must be 100의 배수

			# RDAC Bit
			#_Decoder_RBit = 2, --> 위에서 겹침

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
					_Unit_PMOSXvt2NMOSXvt                   = 1500,  # number
					# Poly Gate setting
						# Poly Gate setting : vertical length
					_Unit_POGate_Comb_length    = None,  # None/Number
				# Nand( _Unit_Num_EachStag_input에서 1,3,5,7...번째 해당하는 nand 생성)
					# MOSFET
						# Common
						_Nand_NumberofGate      = [2,2],  # Number
						_Nand_ChannelLength     = [30,30],  # Number
						_Nand_POGate_ViaMxMx    = [[0, 1],[0, 1]],  # Ex) [1,5] -> ViaM1M5
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
						_Nor_POGate_ViaMxMx     = [[0, 1],[0, 1]],  # Ex) [1,5] -> ViaM1M5
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

	## Initially Generated _DesignParameter
	def __init__(self, _DesignParameter=None, _Name=None):
		if _DesignParameter != None:
			self._DesignParameter = _DesignParameter
		else:
			self._DesignParameter = dict(
			_Name=self._NameDeclaration(_Name=_Name),
			_GDSFile=self._GDSObjDeclaration(_GDSFile=None),
			_XYcoordAsCent=dict(_XYcoordAsCent=0),  # downleft_coordination == 0
			)

	## DesignParameter Calculation
	def _CalculateDesignParameter(self,

	  	_NumbofRbit=5,

	#RDAC and Decoder
		#RDAC and Decoder delta X displacement for DRC
		_RDAC_displacement = -100,

		#RDAC and Decoder Size : Consider "_Decoder_RBit" and "_Unit_Num_EachStag_input" ex) [2, 8] --> 4 : 2*8 = 2**4
		_RDAC_Size = [1, 4],

		#RDAC
			# Guardring
			RDAC_Guard_NumCont 	= 2,

			# Poly Resister unit
			RDAC_ResWidth		= 2000,
			RDAC_ResLength		= 1500,
			RDAC_CONUMX			= None,
			RDAC_CONUMY			= 2,

		# Decoder
			# _Unit to Unit distance for DRC of routing
			_Decoder_Unit2UnitDist=400,  # number must be 100의 배수

			# RDAC Bit
			#_Decoder_RBit = 2, --> 위에서 겹침

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
					_Unit_PMOSXvt2NMOSXvt                   = 1500,  # number
					# Poly Gate setting
						# Poly Gate setting : vertical length
					_Unit_POGate_Comb_length    = None,  # None/Number
				# Nand( _Unit_Num_EachStag_input에서 1,3,5,7...번째 해당하는 nand 생성)
					# MOSFET
						# Common
						_Nand_NumberofGate      = [2,2],  # Number
						_Nand_ChannelLength     = [30,30],  # Number
						_Nand_POGate_ViaMxMx    = [[0, 1],[0, 1]],  # Ex) [1,5] -> ViaM1M5
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
						_Nor_POGate_ViaMxMx     = [[0, 1],[0, 1]],  # Ex) [1,5] -> ViaM1M5
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


								  ):

		## Class_HEADER: Pre Defined Parameter Before Calculation
			## Load DRC library
		_DRCobj = DRC.DRC()
			## Define _name
		_Name = self._DesignParameter['_Name']['_Name']

		## CALCULATION START
		print('##############################')
		print('##     Calculation_Start    ##')
		print('##############################')

		## ########## ########## ########## ########## ########## ########## ########## ########## ########## ########## ########## ########## SRF_RDACandDecoder_Neg
		## ########## ########## ########## ########## ########## ########## ########## ########## ########## ########## ########## SRF_RDACandDecoder_Pos: Gen and placement
		## Copy Calculation_Parameters from low-level-block ex)copy.deepcopy(B16_nmos_power_v2._NMOS_POWER._ParametersForDesignCalculation)
		_Caculation_Parameters = copy.deepcopy(R00_00_Combine_KJH3._Combine._ParametersForDesignCalculation)
		## Define Calculation_Parameters ex) _Caculation_Parameters['_NMOSPOWER_PbodyContact_1_Length']  = _NMOSPOWER_PbodyContact_1_Length
		_Caculation_Parameters['_RDAC_displacement'] = _RDAC_displacement

		_Caculation_Parameters['_RDAC_Size'] = _RDAC_Size

		_Caculation_Parameters['RDAC_Guard_NumCont'] = RDAC_Guard_NumCont
		_Caculation_Parameters['RDAC_ResWidth'] = RDAC_ResWidth
		_Caculation_Parameters['RDAC_ResLength'] = RDAC_ResLength

		_Caculation_Parameters['RDAC_CONUMX'] = RDAC_CONUMX
		_Caculation_Parameters['RDAC_CONUMY'] = RDAC_CONUMY

		_Caculation_Parameters['_Decoder_Unit2UnitDist'] = _Decoder_Unit2UnitDist

		_Caculation_Parameters['_Decoder_RBit'] = _NumbofRbit

		_Caculation_Parameters['_Unit_Routing_Dist'] = _Unit_Routing_Dist
		_Caculation_Parameters['_Unit_Xvt'] = _Unit_Xvt
		_Caculation_Parameters['_Unit_GatetoGateDist'] = _Unit_GatetoGateDist
		_Caculation_Parameters['_Unit_Num_EachStag_input'] = _Unit_Num_EachStag_input

		_Caculation_Parameters['_Unit_Pbody_NumCont'] = _Unit_Pbody_NumCont
		_Caculation_Parameters['_Unit_Pbody_XvtTop2Pbody'] = _Unit_Pbody_XvtTop2Pbody
		_Caculation_Parameters['_Unit_Nbody_NumCont'] = _Unit_Nbody_NumCont
		_Caculation_Parameters['_Unit_Nbody_Xvtdown2Nbody'] = _Unit_Nbody_Xvtdown2Nbody
		_Caculation_Parameters['_Unit_PMOSXvt2NMOSXvt'] = _Unit_PMOSXvt2NMOSXvt
		_Caculation_Parameters['_Unit_POGate_Comb_length'] = _Unit_POGate_Comb_length

		_Caculation_Parameters['_Nand_NumberofGate'] = _Nand_NumberofGate
		_Caculation_Parameters['_Nand_ChannelLength'] = _Nand_ChannelLength
		_Caculation_Parameters['_Nand_POGate_ViaMxMx'] = _Nand_POGate_ViaMxMx

		_Caculation_Parameters['_Nand_NMOS_ChannelWidth'] = _Nand_NMOS_ChannelWidth
		_Caculation_Parameters['_Nand_NMOS_Source_Via_Close2POpin_TF'] = _Nand_NMOS_Source_Via_Close2POpin_TF
		_Caculation_Parameters['_Nand_PMOS_ChannelWidth'] = _Nand_PMOS_ChannelWidth

		_Caculation_Parameters['_Nor_ChannelLength'] = _Nor_ChannelLength
		_Caculation_Parameters['_Nor_POGate_ViaMxMx'] = _Nor_POGate_ViaMxMx

		_Caculation_Parameters['_Nor_NMOS_ChannelWidth'] = _Nor_NMOS_ChannelWidth
		_Caculation_Parameters['_Nor_NMOS_NumberofGate'] = _Nor_NMOS_NumberofGate

		_Caculation_Parameters['_Nor_PMOS_ChannelWidth'] = _Nor_PMOS_ChannelWidth
		_Caculation_Parameters['_Nor_PMOS_NumberofGate'] = _Nor_PMOS_NumberofGate
		_Caculation_Parameters['_Nor_PMOS_Source_Via_Close2POpin_TF'] = _Nor_PMOS_Source_Via_Close2POpin_TF

		_Caculation_Parameters['_Inv_NumberofGate'] = _Inv_NumberofGate
		_Caculation_Parameters['_Inv_ChannelLength'] = _Inv_ChannelLength

		_Caculation_Parameters['_Inv_NMOS_ChannelWidth'] = _Inv_NMOS_ChannelWidth
		_Caculation_Parameters['_Inv_NMOS_POGate_ViaMxMx'] = _Inv_NMOS_POGate_ViaMxMx

		_Caculation_Parameters['_Inv_PMOS_ChannelWidth'] = _Inv_PMOS_ChannelWidth
		_Caculation_Parameters['_Inv_PMOS_POGate_ViaMxMx'] = _Inv_PMOS_POGate_ViaMxMx

		_Caculation_Parameters['_Xgate_NumberofGate'] = _Xgate_NumberofGate
		_Caculation_Parameters['_Xgate_ChannelLength'] = _Xgate_ChannelLength

		_Caculation_Parameters['_Xgate_NMOS_ChannelWidth'] = _Xgate_NMOS_ChannelWidth
		_Caculation_Parameters['_Xgate_NMOS_POGate_ViaMxMx'] = _Xgate_NMOS_POGate_ViaMxMx

		_Caculation_Parameters['_Xgate_PMOS_ChannelWidth'] = _Xgate_PMOS_ChannelWidth
		_Caculation_Parameters['_Xgate_PMOS_POGate_ViaMxMx'] = _Xgate_PMOS_POGate_ViaMxMx

		## Generate Sref: ex)self._DesignParameter['_NMOS_POWER'] = self._SrefElementDeclaration(_DesignObj=B16_nmos_power_v2._NMOS_POWER( _DesignParameter=None, _Name='{}:NMOS_POWER'.format(_Name)))[0]
		self._DesignParameter['SRF_RDACandDecoder_Neg'] = self._SrefElementDeclaration(_DesignObj=R00_00_Combine_KJH3._Combine(_DesignParameter=None, _Name='{}:SRF_RDACandDecoder_Neg'.format(_Name)))[0]

		## Define Sref Reflection: ex)self._DesignParameter['_NMOS_POWER']['_Reflect'] = [0, 0, 0]
		self._DesignParameter['SRF_RDACandDecoder_Neg']['_Reflect'] = [0, 0, 0]

		## Define Sref Angle: ex)'_NMOS_POWER'
		self._DesignParameter['SRF_RDACandDecoder_Neg']['_Angle'] = 0

		## Calculate Sref Layer by using Calculation_Parameter: ex)'_NMOS_POWER'
		self._DesignParameter['SRF_RDACandDecoder_Neg']['_DesignObj']._CalculateDesignParameter(**_Caculation_Parameters)

		## Define Sref _XYcoordinate: ex)'_NMOS_POWER'
		self._DesignParameter['SRF_RDACandDecoder_Neg']['_XYCoordinates'] = [[0, 0]]










		print('###############################')
		print('##     Calculation_End      ##')
		print('##############################')

############################################################################################################################################################ START MAIN
if __name__ == '__main__':

	''' Check Time'''
	Start_time = time.time()

	from KJH91_Projects.Project_ADC.Library_and_Engine.Private import MyInfo
	from KJH91_Projects.Project_ADC.Library_and_Engine import DRCchecker_KJH0

	## LibraryName: ex)Proj_ADC_A_my_building_block
	libname = 'Proj_RcdacSar_Y00_NewMethod'
	## CellName: ex)C01_cap_array_v2_84
	cellname = 'Y00_A03_TEST11_version1'
	_fileName = cellname + '.gds'

	''' Input Parameters for Layout Object '''
	InputParams = dict(


		_NumbofRbit = 5,

	#RDAC and Decoder
		#RDAC and Decoder delta X displacement for DRC
		_RDAC_displacement = -100,

		#RDAC and Decoder Size : Consider "_Decoder_RBit" and "_Unit_Num_EachStag_input" ex) [2, 8] --> 4 : 2*8 = 2**4
		_RDAC_Size = [1, 4],

		#RDAC
			# Guardring
			RDAC_Guard_NumCont 	= 2,

			# Poly Resister unit
			RDAC_ResWidth		= 2000,
			RDAC_ResLength		= 1500,
			RDAC_CONUMX			= None,
			RDAC_CONUMY			= 2,

		# Decoder
			# _Unit to Unit distance for DRC of routing
			_Decoder_Unit2UnitDist=400,  # number must be 100의 배수

			# RDAC Bit
			#_Decoder_RBit = 2, --> 위에서 겹침

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
					_Unit_PMOSXvt2NMOSXvt                   = 1500,  # number
					# Poly Gate setting
						# Poly Gate setting : vertical length
					_Unit_POGate_Comb_length    = None,  # None/Number
				# Nand( _Unit_Num_EachStag_input에서 1,3,5,7...번째 해당하는 nand 생성)
					# MOSFET
						# Common
						_Nand_NumberofGate      = [2,2],  # Number
						_Nand_ChannelLength     = [30,30],  # Number
						_Nand_POGate_ViaMxMx    = [[0, 1],[0, 1]],  # Ex) [1,5] -> ViaM1M5
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
						_Nor_POGate_ViaMxMx     = [[0, 1],[0, 1]],  # Ex) [1,5] -> ViaM1M5
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
	LayoutObj = _Test11(_DesignParameter=None, _Name=cellname)
	LayoutObj._CalculateDesignParameter(**InputParams)
	LayoutObj._UpdateDesignParameter2GDSStructure(_DesignParameterInDictionary=LayoutObj._DesignParameter)
	testStreamFile = open('./{}'.format(_fileName), 'wb')
	tmp = LayoutObj._CreateGDSStream(LayoutObj._DesignParameter['_GDSFile']['_GDSFile'])
	tmp.write_binary_gds_stream(testStreamFile)
	testStreamFile.close()

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
	# Checker.cell_deletion()
	Checker.Upload2FTP()
	Checker.StreamIn(tech=DesignParameters._Technology)
	# Checker_KJH0.DRCchecker()

	''' Check Time'''
	elapsed_time = time.time() - Start_time
	m, s = divmod(elapsed_time, 60)
	h, m = divmod(m, 60)

	print('#############################      Finished      ################################')
# end of 'main():' ---------------------------------------------------------------------------------------------
