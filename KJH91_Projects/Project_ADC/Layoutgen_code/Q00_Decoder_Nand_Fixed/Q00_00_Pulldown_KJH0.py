from KJH91_Projects.Project_ADC.Library_and_Engine import StickDiagram_KJH1
from KJH91_Projects.Project_ADC.Library_and_Engine import DesignParameters
from KJH91_Projects.Project_ADC.Library_and_Engine import DRC

import numpy as np
import copy
import time
import math
#from SthPack import CoordCalc

from KJH91_Projects.Project_ADC.Layoutgen_code.A_Basic_Building_Block import A02_ViaStack_KJH3
from KJH91_Projects.Project_ADC.Layoutgen_code.A_Basic_Building_Block import A15_PolyRes_KJH2
from KJH91_Projects.Project_ADC.Layoutgen_code.A_Basic_Building_Block import A09_NbodyRing_KJH3
from KJH91_Projects.Project_ADC.Layoutgen_code.A_Basic_Building_Block import A10_PbodyRing_KJH3
from KJH91_Projects.Project_ADC.Layoutgen_code.A_Basic_Building_Block import A14_Mosfet_KJH3

from KJH91_Projects.Project_ADC.Layoutgen_code.P00_RDAC import P00_00_RArray2


## ########################################################################################################################################################## Class_HEADER
class _Pulldown(StickDiagram_KJH1._StickDiagram_KJH):

	## Define input_parameters for Design calculation
	_ParametersForDesignCalculation = dict(
		
		# Num of Input
		_Num_Input=5,
		
		# Pulldown
		# PMOS/NMOS
		_NMOS_MosType='NMOS',  # 'NMOS'/'PMOS'
		# MOS Up/Dn
		_NMOS_MosUpDn='Up',  # 'Up'/'Dn'
		# Physical dimension
		_NMOS_NumberofGate	= 1,        # Number
		_NMOS_ChannelWidth	            = 852,      # Number
		_NMOS_ChannelLength	            = 30,       # Number
		_NMOS_GateSpacing		        = None,     # None/Number
		_NMOS_SDWidth			        = None,     # None/Number
		_NMOS_XVT				        = 'SLVT',   # 'XVT' ex)SLVT/LVT/RVT/HVT
		_NMOS_PCCrit				    = True,     # None/True
		
		# Source_node setting
		# Via setting
		_NMOS_Source_Via_TF              = False,     # True/False
		# Via close to POpin
		_NMOS_Source_Via_Close2POpin_TF  = False,     # True/False
		# Comb setting: If Via is True
		_NMOS_Source_Comb_TF             = False,     # True/False
		# Comb POPinward
		_NMOS_Source_Comb_POpinward_TF   = False,     # True/False
		# Comb vertical_length
		_NMOS_Source_Comb_Length         = None,     # None/Number
		
		# Drain_node_setting
		# Via setting
		_NMOS_Drain_Via_TF               = True,     # True/False
		# Via close to POpin
		_NMOS_Drain_Via_Close2POpin_TF   = True,     # True/False
		# Comb setting: If Via is True
		_NMOS_Drain_Comb_TF              = True,     # True/False
		# Comb POPinward
		_NMOS_Drain_Comb_POpinward_TF    = True,     # True/False
		# Comb vertical_length
		_NMOS_Drain_Comb_Length          = None,     # None/Number
		
		# POLY dummy setting
		_NMOS_PODummy_TF                 = True,  # TF
		# if _NMOSDummy == True
		_NMOS_PODummy_Length             = None,  # None/Value
		_NMOS_PODummy_Placement          = None,  # None/'Up'/'Dn'/
		
		# XVT setting
		# XVT setting : Exten XVT area if area is min
		_NMOS_Xvt_MinExten_TF            = True,     # True/False
		# XVT setting : None(Cent), Up, Dn
		_NMOS_Xvt_Placement              = 'Up',     # None/'Up'/'Dn'/
		
		# Poly Gate setting
		_NMOS_POGate_Comb_TF             = True,     # True/False
		# Poly Gate setting : vertical length
		_NMOS_POGate_Comb_length         = 100,     # None/Number
		# Poly Gate Via setting
		_NMOS_POGate_Via_TF              = True,     # None/'Up'/'Dn'/
		# Poly Gate Via setting :
		_NMOS_POGate_ViaMxMx             = [0 ,1],  # Ex) [1,5] -> ViaM1M5
		
										)

	## Initially Defined design_parameter
	def __init__(self, _DesignParameter=None, _Name=None):
		if _DesignParameter != None:
			self._DesignParameter = _DesignParameter
		else:
			self._DesignParameter = dict(
											_Name=self._NameDeclaration(_Name=_Name),
											_GDSFile=self._GDSObjDeclaration(_GDSFile=None),_XYcoordAsCent=dict(_XYcoordAsCent=0),
										)

	## ################################################################################################################################################ _CalculateDesignParameter
	def _CalculateDesignParameter(self,
	                              
	                              # Num of Input
	                              _Num_Input=5,
	                              
	                              # Pulldown
	                              # PMOS/NMOS
	                              _NMOS_MosType='NMOS',  # 'NMOS'/'PMOS'
	                              # MOS Up/Dn
	                              _NMOS_MosUpDn='Up',  # 'Up'/'Dn'
	                              # Physical dimension
	                              _NMOS_NumberofGate	= 1,        # Number
	                              _NMOS_ChannelWidth	            = 852,      # Number
	                              _NMOS_ChannelLength	            = 30,       # Number
	                              _NMOS_GateSpacing		        = None,     # None/Number
	                              _NMOS_SDWidth			        = None,     # None/Number
	                              _NMOS_XVT				        = 'SLVT',   # 'XVT' ex)SLVT/LVT/RVT/HVT
	                              _NMOS_PCCrit				    = True,     # None/True
	                              
	                              # Source_node setting
	                              # Via setting
	                              _NMOS_Source_Via_TF              = False,     # True/False
	                              # Via close to POpin
	                              _NMOS_Source_Via_Close2POpin_TF  = False,     # True/False
	                              # Comb setting: If Via is True
	                              _NMOS_Source_Comb_TF             = False,     # True/False
	                              # Comb POPinward
	                              _NMOS_Source_Comb_POpinward_TF   = False,     # True/False
	                              # Comb vertical_length
	                              _NMOS_Source_Comb_Length         = None,     # None/Number
	                              
	                              # Drain_node_setting
	                              # Via setting
	                              _NMOS_Drain_Via_TF               = True,     # True/False
	                              # Via close to POpin
	                              _NMOS_Drain_Via_Close2POpin_TF   = True,     # True/False
	                              # Comb setting: If Via is True
	                              _NMOS_Drain_Comb_TF              = True,     # True/False
	                              # Comb POPinward
	                              _NMOS_Drain_Comb_POpinward_TF    = True,     # True/False
	                              # Comb vertical_length
	                              _NMOS_Drain_Comb_Length          = None,     # None/Number
	                              
	                              # POLY dummy setting
	                              _NMOS_PODummy_TF                 = True,  # TF
	                              # if _NMOSDummy == True
	                              _NMOS_PODummy_Length             = None,  # None/Value
	                              _NMOS_PODummy_Placement          = None,  # None/'Up'/'Dn'/
	                              
	                              # XVT setting
	                              # XVT setting : Exten XVT area if area is min
	                              _NMOS_Xvt_MinExten_TF            = True,     # True/False
	                              # XVT setting : None(Cent), Up, Dn
	                              _NMOS_Xvt_Placement              = 'Up',     # None/'Up'/'Dn'/
	                              
	                              # Poly Gate setting
	                              _NMOS_POGate_Comb_TF             = True,     # True/False
	                              # Poly Gate setting : vertical length
	                              _NMOS_POGate_Comb_length         = 100,     # None/Number
	                              # Poly Gate Via setting
	                              _NMOS_POGate_Via_TF              = True,     # None/'Up'/'Dn'/
	                              # Poly Gate Via setting :
	                              _NMOS_POGate_ViaMxMx             = [0 ,1],  # Ex) [1,5] -> ViaM1M5
	                              
								  ):

		## ################################################################################################################################# Class_HEADER: Pre Defined Parameter Before Calculation
		# Load DRC library
		_DRCObj = DRC.DRC()

		# Define _name
		_Name = self._DesignParameter['_Name']['_Name']


		## ################################################################################################################################# Calculation_Start
		start_time = time.time()
		# end_time = time.time()
		# self.elapsed_time = end_time - start_time
		print('##############################')
		print('##     Calculation_Start    ##')
		print('##############################')
		
		## ########## ########## ########## ########## ########## ########## ########## ########## ########## ########## ########## ########## Nmos_1..2..3..

		for i in range(0,_Num_Input):
			## 와리가리
			if _NMOS_NumberofGate%2 ==0:
				if i%2 ==0:
					if i==0:
						if _NMOS_Source_Via_Close2POpin_TF == False:
							_NMOS_Source_Via_Close2POpin_TF = False
							_NMOS_Source_Comb_POpinward_TF = False
							_NMOS_Drain_Via_Close2POpin_TF = True
							_NMOS_Drain_Comb_POpinward_TF = True
						else:
							_NMOS_Source_Via_Close2POpin_TF = True
							_NMOS_Source_Comb_POpinward_TF = True
							_NMOS_Drain_Via_Close2POpin_TF = False
							_NMOS_Drain_Comb_POpinward_TF = False
					else:
						if _NMOS_Source_Via_Close2POpin_TF == True:
							_NMOS_Source_Via_Close2POpin_TF = False
							_NMOS_Source_Comb_POpinward_TF = False
							_NMOS_Drain_Via_Close2POpin_TF = True
							_NMOS_Drain_Comb_POpinward_TF = True
						else:
							_NMOS_Source_Via_Close2POpin_TF = True
							_NMOS_Source_Comb_POpinward_TF = True
							_NMOS_Drain_Via_Close2POpin_TF = False
							_NMOS_Drain_Comb_POpinward_TF = False
				else:
					if _NMOS_Source_Via_Close2POpin_TF == False:
						_NMOS_Source_Via_Close2POpin_TF = True
						_NMOS_Source_Comb_POpinward_TF = True
						_NMOS_Drain_Via_Close2POpin_TF = False
						_NMOS_Drain_Comb_POpinward_TF = False
					else:
						_NMOS_Source_Via_Close2POpin_TF = False
						_NMOS_Source_Comb_POpinward_TF = False
						_NMOS_Drain_Via_Close2POpin_TF = True
						_NMOS_Drain_Comb_POpinward_TF = True
			else:
				if i%2 ==0:
					if i==0:
						if _NMOS_Source_Via_Close2POpin_TF == False:
							_NMOS_Source_Via_Close2POpin_TF = False
							_NMOS_Source_Comb_POpinward_TF = False
							_NMOS_Drain_Via_Close2POpin_TF = True
							_NMOS_Drain_Comb_POpinward_TF = True
						else:
							_NMOS_Source_Via_Close2POpin_TF = True
							_NMOS_Source_Comb_POpinward_TF = False
							_NMOS_Drain_Via_Close2POpin_TF = False
							_NMOS_Drain_Comb_POpinward_TF = True
					else:
						if _NMOS_Source_Via_Close2POpin_TF == True:
							_NMOS_Source_Via_Close2POpin_TF = True
							_NMOS_Source_Comb_POpinward_TF = False
							_NMOS_Drain_Via_Close2POpin_TF = False
							_NMOS_Drain_Comb_POpinward_TF = True
						else:
							_NMOS_Source_Via_Close2POpin_TF = False
							_NMOS_Source_Comb_POpinward_TF = False
							_NMOS_Drain_Via_Close2POpin_TF = True
							_NMOS_Drain_Comb_POpinward_TF = True
				else:
					if _NMOS_Source_Via_Close2POpin_TF == False:
						_NMOS_Source_Via_Close2POpin_TF = False
						_NMOS_Source_Comb_POpinward_TF = True
						_NMOS_Drain_Via_Close2POpin_TF = True
						_NMOS_Drain_Comb_POpinward_TF = False
					else:
						_NMOS_Source_Via_Close2POpin_TF = True
						_NMOS_Source_Comb_POpinward_TF = True
						_NMOS_Drain_Via_Close2POpin_TF = False
						_NMOS_Drain_Comb_POpinward_TF = False


			## Copy Calculation_Parameters from low-level-block ex)copy.deepcopy(B16_nmos_power_v2._NMOS_POWER._ParametersForDesignCalculation)
			_Caculation_Parameters = copy.deepcopy(A14_Mosfet_KJH3._Mosfet._ParametersForDesignCalculation)
			## Define Calculation_Parameters ex) _Caculation_Parameters['_NMOSPOWER_PbodyContact_1_Length']  = _NMOSPOWER_PbodyContact_1_Length
			_Caculation_Parameters['_MosType']                      = _NMOS_MosType
			_Caculation_Parameters['_MosUpDn']                      = _NMOS_MosUpDn
			
			_Caculation_Parameters['_NumberofGate']                 = _NMOS_NumberofGate
			_Caculation_Parameters['_ChannelWidth']                 = _NMOS_ChannelWidth
			_Caculation_Parameters['_ChannelLength']                = _NMOS_ChannelLength
			_Caculation_Parameters['_GateSpacing']                  = _NMOS_GateSpacing
			_Caculation_Parameters['_SDWidth']                      = _NMOS_SDWidth
			_Caculation_Parameters['_XVT']                          = _NMOS_XVT
			_Caculation_Parameters['_PCCrit']                       = _NMOS_PCCrit
			
			_Caculation_Parameters['_Source_Via_TF']                = _NMOS_Source_Via_TF
			_Caculation_Parameters['_Source_Via_Close2POpin_TF']    = _NMOS_Source_Via_Close2POpin_TF
			_Caculation_Parameters['_Source_Comb_TF']               = _NMOS_Source_Comb_TF
			_Caculation_Parameters['_Source_Comb_POpinward_TF']     = _NMOS_Source_Comb_POpinward_TF
			_Caculation_Parameters['_Source_Comb_Length']           = _NMOS_Source_Comb_Length
			
			_Caculation_Parameters['_Drain_Via_TF']                 = _NMOS_Drain_Via_TF
			_Caculation_Parameters['_Drain_Via_Close2POpin_TF']     = _NMOS_Drain_Via_Close2POpin_TF
			_Caculation_Parameters['_Drain_Comb_TF']                = _NMOS_Drain_Comb_TF
			_Caculation_Parameters['_Drain_Comb_POpinward_TF']      = _NMOS_Drain_Comb_POpinward_TF
			_Caculation_Parameters['_Drain_Comb_Length']            = _NMOS_Drain_Comb_Length
			
			_Caculation_Parameters['_PODummy_TF']                   = _NMOS_PODummy_TF
			_Caculation_Parameters['_PODummy_Length']               = _NMOS_PODummy_Length
			_Caculation_Parameters['_PODummy_Placement']            = _NMOS_PODummy_Placement
			
			_Caculation_Parameters['_Xvt_MinExten_TF']              = _NMOS_Xvt_MinExten_TF
			_Caculation_Parameters['_Xvt_Placement']                = _NMOS_Xvt_Placement
			
			_Caculation_Parameters['_POGate_Comb_TF']               = _NMOS_POGate_Comb_TF
			_Caculation_Parameters['_POGate_Comb_length']           = _NMOS_POGate_Comb_length
			_Caculation_Parameters['_POGate_Via_TF']                = _NMOS_POGate_Via_TF
			_Caculation_Parameters['_POGate_ViaMxMx']               = _NMOS_POGate_ViaMxMx
			
			## Generate Sref: ex)self._DesignParameter['_NMOS_POWER'] = self._SrefElementDeclaration(_DesignObj=B16_nmos_power_v2._NMOS_POWER( _DesignParameter=None, _Name='{}:NMOS_POWER'.format(_Name)))[0]
			self._DesignParameter['SRF_NMOS{}'.format(i)] = self._SrefElementDeclaration(_DesignObj=A14_Mosfet_KJH3._Mosfet(_DesignParameter=None, _Name='{}:SRF_NMOS{}'.format(_Name,i)))[0]
			
			## Define Sref Reflection: ex)self._DesignParameter['_NMOS_POWER']['_Reflect'] = [0, 0, 0]
			self._DesignParameter['SRF_NMOS{}'.format(i)]['_Reflect'] = [0, 0, 0]
			
			## Define Sref Angle: ex)'_NMOS_POWER'
			self._DesignParameter['SRF_NMOS{}'.format(i)]['_Angle'] = 0
			
			## Calculate Sref Layer by using Calculation_Parameter: ex)'_NMOS_POWER'
			self._DesignParameter['SRF_NMOS{}'.format(i)]['_DesignObj']._CalculateDesignParameter(**_Caculation_Parameters)
			
			if i ==0:
				## Define Sref _XYcoordinate: ex)'_NMOS_POWER'
				self._DesignParameter['SRF_NMOS{}'.format(i)]['_XYCoordinates'] = [[0, 0]]
			else:
				
				if _NMOS_NumberofGate ==1: #or (_NMOS_NumberofGate%2) !=0 :
					## Define Sref _XYcoordinate: ex)'_NMOS_POWER'
					## Get_Scoord_v4.
					## Calculate Sref XYcoord
					tmpXY = []
					## initialized Sref coordinate
					self._DesignParameter['SRF_NMOS{}'.format(i)]['_XYCoordinates'] = [[0, 0]]
					## Calculate
					## Target_coord: _XY_type1
					tmp1 = self.get_param_KJH4('SRF_NMOS{}'.format(i-1),'BND_PODummyLayer')
					target_coord = tmp1[0][0][0]['_XY_down_left']
					## Approaching_coord: _XY_type2
					tmp2 = self.get_param_KJH4('SRF_NMOS{}'.format(i),'BND_PODummyLayer')
					approaching_coord = tmp2[0][-1][0]['_XY_down_right']
					## Sref coord
					tmp3 = self.get_param_KJH4('SRF_NMOS{}'.format(i))
					Scoord = tmp3[0][0]['_XY_origin']
					## Cal
					New_Scoord = self.get_Scoord_KJH4(target_coord, approaching_coord, Scoord)
					New_Scoord[0] = New_Scoord[0] - _DRCObj._PolygateMinSpace2
					tmpXY.append(New_Scoord)
					## Define Coordinates
					self._DesignParameter['SRF_NMOS{}'.format(i)]['_XYCoordinates'] = tmpXY
				else:
					## Define Sref _XYcoordinate: ex)'_NMOS_POWER'
					## Get_Scoord_v4.
					## Calculate Sref XYcoord
					tmpXY = []
					## initialized Sref coordinate
					self._DesignParameter['SRF_NMOS{}'.format(i)]['_XYCoordinates'] = [[0, 0]]
					## Calculate
					## Target_coord: _XY_type1
					tmp1 = self.get_param_KJH4('SRF_NMOS{}'.format(i-1),'BND_PODummyLayer')
					target_coord = tmp1[0][0][0]['_XY_down_left']
					## Approaching_coord: _XY_type2
					tmp2 = self.get_param_KJH4('SRF_NMOS{}'.format(i),'BND_PODummyLayer')
					approaching_coord = tmp2[0][-1][0]['_XY_down_left']
					## Sref coord
					tmp3 = self.get_param_KJH4('SRF_NMOS{}'.format(i))
					Scoord = tmp3[0][0]['_XY_origin']
					## Cal
					New_Scoord = self.get_Scoord_KJH4(target_coord, approaching_coord, Scoord)
					tmpXY.append(New_Scoord)
					## Define Coordinates
					self._DesignParameter['SRF_NMOS{}'.format(i)]['_XYCoordinates'] = tmpXY
		
		
		## ########## ########## ########## ########## ########## ########## ########## ########## ########## ########## ##########  BND Nmos Series connect Hrz m2
		## Boundary_element Generation
		## Generate Boundary_element: ex)LayerName: METAL1 / DIFF (_ODLayer) / POLY / PIMP (_PPLayer) / NWELL / SLVT LVT RVT HVT / OP(OPpress) / CONT (CA) / PCCRIT
		self._DesignParameter['BND_Nmos_SeriesConn_Hrz_M2'] = self._BoundaryElementDeclaration(
			_Layer=DesignParameters._LayerMapping['METAL2'][0],
			_Datatype=DesignParameters._LayerMapping['METAL2'][1],
			_XWidth=None,
			_YWidth=None,
			_XYCoordinates=[],
		)
		
		## Define Boundary_element _YWidth
		tmp = self.get_param_KJH4('SRF_NMOS0','BND_Drain_Hrz_M2')
		self._DesignParameter['BND_Nmos_SeriesConn_Hrz_M2']['_YWidth'] = tmp[0][0][0]['_Ywidth']
		
		## Define Boundary_element _XWidth
		tmp1 = self.get_param_KJH4('SRF_NMOS0','BND_Source_Hrz_M2')
		tmp2 = self.get_param_KJH4('SRF_NMOS1','BND_Drain_Hrz_M2')
		self._DesignParameter['BND_Nmos_SeriesConn_Hrz_M2']['_XWidth'] = abs( tmp1[0][0][0]['_XY_right'][0] - tmp2[0][0][0]['_XY_left'][0] )
		
		## Define Boundary_element _XYCoordinates
		self._DesignParameter['BND_Nmos_SeriesConn_Hrz_M2']['_XYCoordinates'] = [[0, 0]]
		
		## Calculate Sref XYcoord
		tmpXY = []
		## initialized Sref coordinate
		self._DesignParameter['BND_Nmos_SeriesConn_Hrz_M2']['_XYCoordinates'] = [[0, 0]]
		for i in range(0,_Num_Input-1):
			## Calculate
			if i%2 ==0:
				## Target_coord: _XY_type1
				tmp1 = self.get_param_KJH4('SRF_NMOS{}'.format(i),'BND_Source_Hrz_M2')
				target_coord = tmp1[0][0][0]['_XY_down_right']
			else:
				## Target_coord: _XY_type1
				tmp1 = self.get_param_KJH4('SRF_NMOS{}'.format(i),'BND_Source_Hrz_M2')
				target_coord = tmp1[0][0][0]['_XY_down_right']
				
			## Approaching_coord: _XY_type2
			tmp2 = self.get_param_KJH4('BND_Nmos_SeriesConn_Hrz_M2')
			approaching_coord = tmp2[0][0]['_XY_down_right']
			## Sref coord
			tmp3 = self.get_param_KJH4('BND_Nmos_SeriesConn_Hrz_M2')
			Scoord = tmp3[0][0]['_XY_origin']
			## Cal
			New_Scoord = self.get_Scoord_KJH4(target_coord, approaching_coord, Scoord)
			tmpXY.append(New_Scoord)
			
		## Define coordinates
		self._DesignParameter['BND_Nmos_SeriesConn_Hrz_M2']['_XYCoordinates'] = tmpXY
		
		
		# ## ########## ########## ########## ########## ########## ########## ########## ########## ########## ########## ##########  Exten Bp(PIMP) Layer
		# ## Boundary_element Generation
		# ## Generate Boundary_element: ex)LayerName: METAL1 / DIFF (_ODLayer) / POLY / PIMP (_PPLayer) / NWELL / SLVT LVT RVT HVT / OP(OPpress) / CONT (CA) / PCCRIT
		# self._DesignParameter['BND_Nmos_PP_Exten'] = self._BoundaryElementDeclaration(
		# 	_Layer=DesignParameters._LayerMapping['PIMP'][0],
		# 	_Datatype=DesignParameters._LayerMapping['PIMP'][1],
		# 	_XWidth=None,
		# 	_YWidth=None,
		# 	_XYCoordinates=[],
		# )
		#
		# ## Define Boundary_element _XWidth
		# tmp1 = self.get_param_KJH4('SRF_NMOS0', 'BND_PPLayer',)
		# tmp2 = self.get_param_KJH4('SRF_NMOS{}',format(_Num_Input-1), 'BND_PPLayer',)
		# self._DesignParameter['BND_Nmos_PP_Exten']['_XWidth'] = abs(tmp1[0][0][0]['_XY_right'][0] - tmp2[0][0][0][0]['_XY_left'][0])
		#
		# ## Define Boundary_element _YWidth
		# tmp = self.get_param_KJH4('SRF_NMOS0', 'BND_PPLayer', )
		# self._DesignParameter['BND_Nmos_PP_Exten']['_YWidth'] = tmp[0][0][0]['_Ywidth']
		#
		# ## Define Boundary_element _XYCoordinates
		# self._DesignParameter['BND_Nmos_PP_Exten']['_XYCoordinates'] = [[0, 0]]
		#
		# ## Get_Scoord_v4.
		# ## Calculate Sref XYcoord
		# tmpXY = []
		# ## initialized Sref coordinate
		# self._DesignParameter['BND_Nmos_PP_Exten']['_XYCoordinates'] = [[0, 0]]
		# ## Calculate
		# ## Target_coord: _XY_type1
		# tmp1 = self.get_param_KJH4('SRF_NMOS0', 'BND_PPLayer', )
		# target_coord = tmp1[0][0][0]['_XY_down_right']
		# ## Approaching_coord: _XY_type2
		# tmp2 = self.get_param_KJH4('BND_Nmos_PP_Exten')
		# approaching_coord = tmp2[0][0]['_XY_down_right']
		# ## Sref coord
		# tmp3 = self.get_param_KJH4('BND_Nmos_PP_Exten')
		# Scoord = tmp3[0][0]['_XY_origin']
		# ## Cal
		# New_Scoord = self.get_Scoord_KJH4(target_coord, approaching_coord, Scoord)
		# tmpXY.append(New_Scoord)
		# ## Define Coordinates
		# self._DesignParameter['BND_Nmos_PP_Exten']['_XYCoordinates'] = tmpXY
		
		## ########## ########## ########## ########## ########## ########## ########## ########## ########## ########## ##########  Exten Xvt Layer
		_XVTLayerMappingName = _NMOS_XVT
		_XVTLayer = 'BND_' + _NMOS_XVT + 'Layer'
		
		## Boundary_element Generation
		## Generate Boundary_element: ex)LayerName: METAL1 / DIFF (_ODLayer) / POLY / PIMP (_PPLayer) / NWELL / SLVT LVT RVT HVT / OP(OPpress) / CONT (CA) / PCCRIT
		self._DesignParameter['BND_Nmos_Xvt_Exten'] = self._BoundaryElementDeclaration(
			_Layer=DesignParameters._LayerMapping[_XVTLayerMappingName][0],
			_Datatype=DesignParameters._LayerMapping[_XVTLayerMappingName][1],
			_XWidth=None,
			_YWidth=None,
			_XYCoordinates=[],
		)
		
		## Define Boundary_element _XWidth
		tmp1 = self.get_param_KJH4('SRF_NMOS0', _XVTLayer, )
		tmp2 = self.get_param_KJH4('SRF_NMOS{}'.format(_Num_Input - 1), _XVTLayer, )
		self._DesignParameter['BND_Nmos_Xvt_Exten']['_XWidth'] = abs(tmp1[0][0][0]['_XY_right'][0] - tmp2[0][0][0]['_XY_left'][0])
		
		## Define Boundary_element _YWidth
		tmp = self.get_param_KJH4('SRF_NMOS0', _XVTLayer, )
		self._DesignParameter['BND_Nmos_Xvt_Exten']['_YWidth'] = tmp[0][0][0]['_Ywidth']
		
		## Define Boundary_element _XYCoordinates
		self._DesignParameter['BND_Nmos_Xvt_Exten']['_XYCoordinates'] = [[0, 0]]
		
		## Get_Scoord_v4.
		## Calculate Sref XYcoord
		tmpXY = []
		## initialized Sref coordinate
		self._DesignParameter['BND_Nmos_Xvt_Exten']['_XYCoordinates'] = [[0, 0]]
		## Calculate
		## Target_coord: _XY_type1
		tmp1 = self.get_param_KJH4('SRF_NMOS0', _XVTLayer, )
		target_coord = tmp1[0][0][0]['_XY_down_right']
		## Approaching_coord: _XY_type2
		tmp2 = self.get_param_KJH4('BND_Nmos_Xvt_Exten')
		approaching_coord = tmp2[0][0]['_XY_down_right']
		## Sref coord
		tmp3 = self.get_param_KJH4('BND_Nmos_Xvt_Exten')
		Scoord = tmp3[0][0]['_XY_origin']
		## Cal
		New_Scoord = self.get_Scoord_KJH4(target_coord, approaching_coord, Scoord)
		tmpXY.append(New_Scoord)
		## Define Coordinates
		self._DesignParameter['BND_Nmos_Xvt_Exten']['_XYCoordinates'] = tmpXY
		
		## ################################################################################################################################# Calculation_End
		print('##############################')
		print('##     Calculation_End      ##')
		print('##############################')
		# start_time = time.time()
		end_time = time.time()
		self.elapsed_time = end_time - start_time

## ########################################################################################################################################################## Start_Main
if __name__ == '__main__':
	''' Check Time'''
	start_time = time.time()

	from KJH91_Projects.Project_ADC.Library_and_Engine.Private import MyInfo
	from KJH91_Projects.Project_ADC.Library_and_Engine import DRCchecker_KJH0

	libname = 'Proj_ZZ01_Q00_00_Pulldown'
	cellname = 'Q00_00_Pulldown_99'
	_fileName = cellname + '.gds'

	''' Input Parameters for Layout Object '''
	InputParams = dict(
		
		# Num of Input
		_Num_Input = 5, #Number>2
		
		# Pulldown
			# PMOS/NMOS
		_NMOS_MosType='NMOS',                       # 'NMOS'/'PMOS' --> fixed
			# MOS Up/Dn
		_NMOS_MosUpDn='Up',                         # 'Up'/'Dn' --> fixed
		
			# Physical dimension
		_NMOS_NumberofGate	            = 5,        # Number
		_NMOS_ChannelWidth	            = 350,      # Number
		_NMOS_ChannelLength	            = 30,       # Number
		_NMOS_GateSpacing		        = None,     # None/Number --> fixed
		_NMOS_SDWidth			        = None,     # None/Number --> fixed
		_NMOS_XVT				        = 'SLVT',   # 'XVT' ex)SLVT/LVT/RVT/HVT
		_NMOS_PCCrit				    = True,     # None/True --> fixed
		
			# Source_node setting
				# Via setting
		_NMOS_Source_Via_TF              = True,     # True/False --> fixed
				# Via close to POpin
		_NMOS_Source_Via_Close2POpin_TF  = True,    # True/False --> First MOS
				# Comb setting: If Via is True
		_NMOS_Source_Comb_TF             = True,     # True/False --> fixed
				# Comb POPinward
		_NMOS_Source_Comb_POpinward_TF   = False,    # True/False --> Same as "_NMOS_Source_Via_Close2POpin_TF"
				# Comb vertical_length
		_NMOS_Source_Comb_Length         = None,     # None/Number --> fixed
		
			# Drain_node_setting
				# Via setting
		_NMOS_Drain_Via_TF               = True,     # True/False --> fixed
				# Via close to POpin
		_NMOS_Drain_Via_Close2POpin_TF   = True,     # True/False --> oppos to "_NMOS_Source_Via_Close2POpin_TF"
				# Comb setting: If Via is True
		_NMOS_Drain_Comb_TF              = True,     # True/False --> fixed
				# Comb POPinward
		_NMOS_Drain_Comb_POpinward_TF    = True,     # True/False --> Same as "_NMOS_Drain_Via_Close2POpin_TF"
				# Comb vertical_length
		_NMOS_Drain_Comb_Length          = None,     # None/Number --> fixed
		
			# POLY dummy setting
		_NMOS_PODummy_TF                 = True,  # TF --> fixed
				# if _NMOSDummy == True
		_NMOS_PODummy_Length             = None,  # None/Value --> fixed
		_NMOS_PODummy_Placement          = None,  # None/'Up'/'Dn'/ --> fixed
		
			# XVT setting
				# XVT setting : Exten XVT area if area is min
		_NMOS_Xvt_MinExten_TF            = True,     # True/False --> fixed
				# XVT setting : None(Cent), Up, Dn
		_NMOS_Xvt_Placement              = 'Up',     # None/'Up'/'Dn'/ --> fixed
		
			# Poly Gate setting
		_NMOS_POGate_Comb_TF             = True,     # True/False --> fixed
				# Poly Gate setting : vertical length
		_NMOS_POGate_Comb_length         = None,      # None/Number
				# Poly Gate Via setting
		_NMOS_POGate_Via_TF              = True,     # True/False --> fixed
				# Poly Gate Via setting :
		_NMOS_POGate_ViaMxMx             = [0 ,1],  # Ex) [1,5] -> ViaM1M5
		

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
	LayoutObj = _Pulldown(_DesignParameter=None, _Name=cellname)
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




