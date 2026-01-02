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


from KJH91_Projects.Project_ADC.Layoutgen_code.P00_RDAC_Fixed import P00_00_RArray2

## ########################################################################################################################################################## Class_HEADER
class _Guardring(StickDiagram_KJH1._StickDiagram_KJH):

	## Define input_parameters for Design calculation
	_ParametersForDesignCalculation = dict(
#ResArray
	#Array
	_Size		= [5 ,2],
	#Unit Resistor
	_ResWidth	=	1300,
	_ResLength	=	1500,
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
#ResArray
	#Array
	_Size		= [5 ,2],
	#Unit Resistor
	_ResWidth	=	1300,
	_ResLength	=	1500,

								  ):

		## ################################################################################################################################# Class_HEADER: Pre Defined Parameter Before Calculation
		# Load DRC library
		_DRCObj = DRC.DRC()

		# Define _name
		_Name = self._DesignParameter['_Name']['_Name']


		## ################################################################################################################################# Calculation_Start
		RDAC_start_time = time.time()
		print('##############################')
		print('##     Calculation_Start    ##')
		print('##############################')

		## ########## ########## ########## ########## ########## ########## ########## ########## ########## ########## ########## ########## SRF_RArray
			## SREF Generation
				## Copy Calculation_Parameters from low-level-block ex)copy.deepcopy(B16_nmos_power_v2._NMOS_POWER._ParametersForDesignCalculation)
		_Caculation_Parameters = copy.deepcopy(P00_00_RArray2._RArray._ParametersForDesignCalculation)
				## Define Calculation_Parameters ex) _Caculation_Parameters['_NMOSPOWER_PbodyContact_1_Length']  = _NMOSPOWER_PbodyContact_1_Length
		_Caculation_Parameters['_ResWidth']     = _ResWidth
		_Caculation_Parameters['_ResLength']    = _ResLength
		_Caculation_Parameters['_Size']         = _Size

				## Generate Sref: ex)self._DesignParameter['_NMOS_POWER'] = self._SrefElementDeclaration(_DesignObj=B16_nmos_power_v2._NMOS_POWER( _DesignParameter=None, _Name='{}:NMOS_POWER'.format(_Name)))[0]
		self._DesignParameter['SRF_RArray'] = self._SrefElementDeclaration(_DesignObj=P00_00_RArray2._RArray(_DesignParameter=None, _Name='{}:SRF_RArray'.format(_Name)))[0]

				## Define Sref Reflection: ex)self._DesignParameter['_NMOS_POWER']['_Reflect'] = [0, 0, 0]
		self._DesignParameter['SRF_RArray']['_Reflect'] = [0, 0, 0]

				## Define Sref Angle: ex)'_NMOS_POWER'
		self._DesignParameter['SRF_RArray']['_Angle'] = 0

				## Calculate Sref Layer by using Calculation_Parameter: ex)'_NMOS_POWER'
		self._DesignParameter['SRF_RArray']['_DesignObj']._CalculateDesignParameter(**_Caculation_Parameters)

				## Define Sref _XYcoordinate: ex)'_NMOS_POWER'
		self._DesignParameter['SRF_RArray']['_XYCoordinates'] = [[0, 0]]
		
		## ########## ########## ########## ########## ########## ########## ########## ########## ########## ########## ########## ########## SRF_Guardring
		## Pre-defined
		_NumCont=2

		_right_margin = 300
		_left_margin = 300
		_up_margin = 300
		_down_margin = 300
		
		## Guardring
		## Define Calculation_Parameters
		_Caculation_Parameters = copy.deepcopy(A10_PbodyRing_KJH3._PbodyRing._ParametersForDesignCalculation)
		_Caculation_Parameters['_XlengthIntn'] = None
		_Caculation_Parameters['_YlengthIntn'] = None
		_Caculation_Parameters['_NumContTop'] = _NumCont
		_Caculation_Parameters['_NumContBottom'] = _NumCont
		_Caculation_Parameters['_NumContLeft'] = _NumCont
		_Caculation_Parameters['_NumContRight'] = _NumCont
		# _Caculation_Parameters['_NwellWidth']       = _NwellWidth ## used only for DeepNwell
		
		## Find Outter boundary
		tmp = self.get_outter_KJH4('SRF_RArray','BND_PRES_cover2')
		
		## Define _XlengthIntn
		_Caculation_Parameters['_XlengthIntn'] = abs(tmp['_Mostright']['coord'][0] - tmp['_Mostleft']['coord'][0]) + _right_margin + _left_margin  # option: + _NwellWidth
		
		## Define _YlengthIntn
		_Caculation_Parameters['_YlengthIntn'] = abs(tmp['_Mostup']['coord'][0] - tmp['_Mostdown']['coord'][0]) + _up_margin + _down_margin  # option + _NwellWidth
		
		## Generate Sref
		self._DesignParameter['SRF_Pbodyring'] = self._SrefElementDeclaration(_DesignObj=A10_PbodyRing_KJH3._PbodyRing(_DesignParameter=None, _Name='{}:_Pbodyring'.format(_Name)))[0]
		
		## Define Sref Relection
		self._DesignParameter['SRF_Pbodyring']['_Reflect'] = [0, 0, 0]
		
		## Define Sref Angle
		self._DesignParameter['SRF_Pbodyring']['_Angle'] = 0
		
		## Calculate Sref Layer by using Calculation_Parameter
		self._DesignParameter['SRF_Pbodyring']['_DesignObj']._CalculateDesignParameter(**_Caculation_Parameters)
		
		## Define Sref _XYcoordinate
		self._DesignParameter['SRF_Pbodyring']['_XYCoordinates'] = [[0, 0]]
		
		## Calculate Sref XYcoord
		tmpXY = []
		## initialized Sref coordinate
		self._DesignParameter['SRF_Pbodyring']['_XYCoordinates'] = [[0, 0]]
		## Calculate
		## Target_coord
		target_coord = [tmp['_Mostleft']['coord'][0], tmp['_Mostdown']['coord'][0]]
		## Approaching_coord
		## x
		tmp2_1 = self.get_param_KJH4('SRF_Pbodyring', 'SRF_PbodyLeft', 'SRF_PbodyContactPhyLen', 'BND_Met1Layer')
		approaching_coordx = tmp2_1[0][0][0][0][0]['_XY_right'][0]
		## y
		tmp2_2 = self.get_param_KJH4('SRF_Pbodyring', 'SRF_PbodyBottom', 'SRF_PbodyContactPhyLen', 'BND_Met1Layer')
		approaching_coordy = tmp2_2[0][0][0][0][0]['_XY_up'][1]
		
		approaching_coord = [approaching_coordx, approaching_coordy]
		## Sref coord
		tmp3 = self.get_param_KJH4('SRF_Pbodyring')
		Scoord = tmp3[0][0]['_XY_origin']
		## Calculate
		New_Scoord = self.get_Scoord_KJH4(target_coord, approaching_coord, Scoord)
		New_Scoord[0] = New_Scoord[0] - _left_margin  # option: - _NwellWidth
		New_Scoord[1] = New_Scoord[1] - _down_margin  # option: - _NwellWidth
		tmpXY.append(New_Scoord)
		## Define
		self._DesignParameter['SRF_Pbodyring']['_XYCoordinates'] = tmpXY
		
		
		## ########## ########## ########## ########## ########## ########## ########## ########## ########## ########## ########## ########## Dummy Pin M1 Connection
		## ########## ########## ########## ########## ########## ########## ########## ########## ########## ########## ########## Dummy Pin M1 Connection : Up PinA Hrz M1
		# Define Boundary_element
		self._DesignParameter['BND_Up_PinA_Hrz_M1'] = self._BoundaryElementDeclaration(
			_Layer=DesignParameters._LayerMapping['METAL1'][0],
			_Datatype=DesignParameters._LayerMapping['METAL1'][1],
			_XWidth=None,
			_YWidth=None,
			_XYCoordinates=[],
		)
		
		# Define Boundary_element _YWidth
		tmp = self.get_param_KJH4('SRF_RArray','SRF_PolyRes','BND_PinA_M1')
		self._DesignParameter['BND_Up_PinA_Hrz_M1']['_YWidth'] = tmp[0][0][0][0]['_Ywidth']
		
		# Define Boundary_element _XWidth
		tmp1 = self.get_param_KJH4('SRF_Pbodyring', 'SRF_PbodyLeft', 'SRF_PbodyContactPhyLen', 'BND_Met1Layer')
		tmp2 = self.get_param_KJH4('SRF_Pbodyring', 'SRF_PbodyRight', 'SRF_PbodyContactPhyLen', 'BND_Met1Layer')
		self._DesignParameter['BND_Up_PinA_Hrz_M1']['_XWidth'] = abs( tmp1[0][0][0][0][0]['_XY_left'][0] - tmp2[0][0][0][0][0]['_XY_right'][0] )
		
		# Define Boundary_element _XYCoordinates
		self._DesignParameter['BND_Up_PinA_Hrz_M1']['_XYCoordinates'] = [[0,0]]
		
		## Get_Scoord_v4.
		## Calculate Sref XYcoord
		tmpXY = []
		## initialized Sref coordinate
		self._DesignParameter['BND_Up_PinA_Hrz_M1']['_XYCoordinates'] = [[0, 0]]
		## Calculate
		## Target_coord: _XY_type1
			##X
		tmp1_1 = self.get_param_KJH4('SRF_Pbodyring', 'SRF_PbodyLeft', 'SRF_PbodyContactPhyLen', 'BND_Met1Layer')
		target_coordx = tmp1_1[0][0][0][0][0]['_XY_left'][0]
			##Y
		tmp1_2 = self.get_param_KJH4('SRF_RArray','SRF_PolyRes_Dummy_Left','BND_PinA_M1')
		target_coordy = tmp1_2[0][0][0][0]['_XY_up'][1]
		target_coord=[target_coordx,target_coordy]
		
		## Approaching_coord: _XY_type2
		tmp2 = self.get_param_KJH4('BND_Up_PinA_Hrz_M1')
		approaching_coord = tmp2[0][0]['_XY_up_left']
		## Sref coord
		tmp3 = self.get_param_KJH4('BND_Up_PinA_Hrz_M1')
		Scoord = tmp3[0][0]['_XY_origin']
		## Cal
		New_Scoord = self.get_Scoord_KJH4(target_coord, approaching_coord, Scoord)
		tmpXY.append(New_Scoord)
		## Define Coordinates
		self._DesignParameter['BND_Up_PinA_Hrz_M1']['_XYCoordinates'] = tmpXY
		
		## ########## ########## ########## ########## ########## ########## ########## ########## ########## ########## ########## Dummy Pin M1 Connection : Up PinB Hrz M1
		# Define Boundary_element
		self._DesignParameter['BND_Up_PinB_Hrz_M1'] = self._BoundaryElementDeclaration(
			_Layer=DesignParameters._LayerMapping['METAL1'][0],
			_Datatype=DesignParameters._LayerMapping['METAL1'][1],
			_XWidth=None,
			_YWidth=None,
			_XYCoordinates=[],
		)
		
		# Define Boundary_element _YWidth
		tmp = self.get_param_KJH4('SRF_RArray', 'SRF_PolyRes', 'BND_PinA_M1')
		self._DesignParameter['BND_Up_PinB_Hrz_M1']['_YWidth'] = tmp[0][0][0][0]['_Ywidth']
		
		# Define Boundary_element _XWidth
		tmp1 = self.get_param_KJH4('SRF_Pbodyring', 'SRF_PbodyLeft', 'SRF_PbodyContactPhyLen', 'BND_Met1Layer')
		tmp2 = self.get_param_KJH4('SRF_Pbodyring', 'SRF_PbodyRight', 'SRF_PbodyContactPhyLen', 'BND_Met1Layer')
		self._DesignParameter['BND_Up_PinB_Hrz_M1']['_XWidth'] = abs(tmp1[0][0][0][0][0]['_XY_left'][0] - tmp2[0][0][0][0][0]['_XY_right'][0])
		
		# Define Boundary_element _XYCoordinates
		self._DesignParameter['BND_Up_PinB_Hrz_M1']['_XYCoordinates'] = [[0, 0]]
		
		## Get_Scoord_v4.
		## Calculate Sref XYcoord
		tmpXY = []
		## initialized Sref coordinate
		self._DesignParameter['BND_Up_PinB_Hrz_M1']['_XYCoordinates'] = [[0, 0]]
		## Calculate
		## Target_coord: _XY_type1
		##X
		tmp1_1 = self.get_param_KJH4('SRF_Pbodyring', 'SRF_PbodyLeft', 'SRF_PbodyContactPhyLen', 'BND_Met1Layer')
		target_coordx = tmp1_1[0][0][0][0][0]['_XY_left'][0]
		##Y
		tmp1_2 = self.get_param_KJH4('SRF_RArray', 'SRF_PolyRes_Dummy_Left', 'BND_PinB_M1')
		target_coordy = tmp1_2[0][0][0][0]['_XY_up'][1]
		target_coord = [target_coordx, target_coordy]
		
		## Approaching_coord: _XY_type2
		tmp2 = self.get_param_KJH4('BND_Up_PinB_Hrz_M1')
		approaching_coord = tmp2[0][0]['_XY_up_left']
		## Sref coord
		tmp3 = self.get_param_KJH4('BND_Up_PinB_Hrz_M1')
		Scoord = tmp3[0][0]['_XY_origin']
		## Cal
		New_Scoord = self.get_Scoord_KJH4(target_coord, approaching_coord, Scoord)
		tmpXY.append(New_Scoord)
		## Define Coordinates
		self._DesignParameter['BND_Up_PinB_Hrz_M1']['_XYCoordinates'] = tmpXY
		
		## ########## ########## ########## ########## ########## ########## ########## ########## ########## ########## ########## Dummy Pin M1 Connection : Down PinA Hrz M1
		# Define Boundary_element
		self._DesignParameter['BND_Down_PinA_Hrz_M1'] = self._BoundaryElementDeclaration(
			_Layer=DesignParameters._LayerMapping['METAL1'][0],
			_Datatype=DesignParameters._LayerMapping['METAL1'][1],
			_XWidth=None,
			_YWidth=None,
			_XYCoordinates=[],
		)
		
		# Define Boundary_element _YWidth
		tmp = self.get_param_KJH4('SRF_RArray', 'SRF_PolyRes', 'BND_PinA_M1')
		self._DesignParameter['BND_Down_PinA_Hrz_M1']['_YWidth'] = tmp[0][0][0][0]['_Ywidth']
		
		# Define Boundary_element _XWidth
		tmp1 = self.get_param_KJH4('SRF_Pbodyring', 'SRF_PbodyLeft', 'SRF_PbodyContactPhyLen', 'BND_Met1Layer')
		tmp2 = self.get_param_KJH4('SRF_Pbodyring', 'SRF_PbodyRight', 'SRF_PbodyContactPhyLen', 'BND_Met1Layer')
		self._DesignParameter['BND_Down_PinA_Hrz_M1']['_XWidth'] = abs(tmp1[0][0][0][0][0]['_XY_left'][0] - tmp2[0][0][0][0][0]['_XY_right'][0])
		
		# Define Boundary_element _XYCoordinates
		self._DesignParameter['BND_Down_PinA_Hrz_M1']['_XYCoordinates'] = [[0, 0]]
		
		## Get_Scoord_v4.
		## Calculate Sref XYcoord
		tmpXY = []
		## initialized Sref coordinate
		self._DesignParameter['BND_Down_PinA_Hrz_M1']['_XYCoordinates'] = [[0, 0]]
		## Calculate
		## Target_coord: _XY_type1
		##X
		tmp1_1 = self.get_param_KJH4('SRF_Pbodyring', 'SRF_PbodyLeft', 'SRF_PbodyContactPhyLen', 'BND_Met1Layer')
		target_coordx = tmp1_1[0][0][0][0][0]['_XY_left'][0]
		##Y
		tmp1_2 = self.get_param_KJH4('SRF_RArray', 'SRF_PolyRes_Dummy_Left', 'BND_PinA_M1')
		target_coordy = tmp1_2[0][-1][0][0]['_XY_up'][1]
		target_coord = [target_coordx, target_coordy]
		
		## Approaching_coord: _XY_type2
		tmp2 = self.get_param_KJH4('BND_Down_PinA_Hrz_M1')
		approaching_coord = tmp2[0][0]['_XY_up_left']
		## Sref coord
		tmp3 = self.get_param_KJH4('BND_Down_PinA_Hrz_M1')
		Scoord = tmp3[0][0]['_XY_origin']
		## Cal
		New_Scoord = self.get_Scoord_KJH4(target_coord, approaching_coord, Scoord)
		tmpXY.append(New_Scoord)
		## Define Coordinates
		self._DesignParameter['BND_Down_PinA_Hrz_M1']['_XYCoordinates'] = tmpXY
		
		## ########## ########## ########## ########## ########## ########## ########## ########## ########## ########## ########## Dummy Pin M1 Connection : Up PinB Hrz M1
		# Define Boundary_element
		self._DesignParameter['BND_Down_PinB_Hrz_M1'] = self._BoundaryElementDeclaration(
			_Layer=DesignParameters._LayerMapping['METAL1'][0],
			_Datatype=DesignParameters._LayerMapping['METAL1'][1],
			_XWidth=None,
			_YWidth=None,
			_XYCoordinates=[],
		)
		
		# Define Boundary_element _YWidth
		tmp = self.get_param_KJH4('SRF_RArray', 'SRF_PolyRes', 'BND_PinA_M1')
		self._DesignParameter['BND_Down_PinB_Hrz_M1']['_YWidth'] = tmp[0][0][0][0]['_Ywidth']
		
		# Define Boundary_element _XWidth
		tmp1 = self.get_param_KJH4('SRF_Pbodyring', 'SRF_PbodyLeft', 'SRF_PbodyContactPhyLen', 'BND_Met1Layer')
		tmp2 = self.get_param_KJH4('SRF_Pbodyring', 'SRF_PbodyRight', 'SRF_PbodyContactPhyLen', 'BND_Met1Layer')
		self._DesignParameter['BND_Down_PinB_Hrz_M1']['_XWidth'] = abs(tmp1[0][0][0][0][0]['_XY_left'][0] - tmp2[0][0][0][0][0]['_XY_right'][0])
		
		# Define Boundary_element _XYCoordinates
		self._DesignParameter['BND_Down_PinB_Hrz_M1']['_XYCoordinates'] = [[0, 0]]
		
		## Get_Scoord_v4.
		## Calculate Sref XYcoord
		tmpXY = []
		## initialized Sref coordinate
		self._DesignParameter['BND_Down_PinB_Hrz_M1']['_XYCoordinates'] = [[0, 0]]
		## Calculate
		## Target_coord: _XY_type1
		##X
		tmp1_1 = self.get_param_KJH4('SRF_Pbodyring', 'SRF_PbodyLeft', 'SRF_PbodyContactPhyLen', 'BND_Met1Layer')
		target_coordx = tmp1_1[0][0][0][0][0]['_XY_left'][0]
		##Y
		tmp1_2 = self.get_param_KJH4('SRF_RArray', 'SRF_PolyRes_Dummy_Left', 'BND_PinB_M1')
		target_coordy = tmp1_2[0][-1][0][0]['_XY_up'][1]
		target_coord = [target_coordx, target_coordy]
		
		## Approaching_coord: _XY_type2
		tmp2 = self.get_param_KJH4('BND_Down_PinB_Hrz_M1')
		approaching_coord = tmp2[0][0]['_XY_up_left']
		## Sref coord
		tmp3 = self.get_param_KJH4('BND_Down_PinB_Hrz_M1')
		Scoord = tmp3[0][0]['_XY_origin']
		## Cal
		New_Scoord = self.get_Scoord_KJH4(target_coord, approaching_coord, Scoord)
		tmpXY.append(New_Scoord)
		## Define Coordinates
		self._DesignParameter['BND_Down_PinB_Hrz_M1']['_XYCoordinates'] = tmpXY
		
		## ########## ########## ########## ########## ########## ########## ########## ########## ########## ########## ########## Dummy Pin M1 Connection : Left Vtc M1
		# Define Boundary_element
		self._DesignParameter['BND_Left_Vtc_M1'] = self._BoundaryElementDeclaration(
			_Layer=DesignParameters._LayerMapping['METAL1'][0],
			_Datatype=DesignParameters._LayerMapping['METAL1'][1],
			_XWidth=None,
			_YWidth=None,
			_XYCoordinates=[],
		)
		
		# Define Boundary_element _YWidth
		tmp1 = self.get_param_KJH4('SRF_Pbodyring', 'SRF_PbodyTop', 'SRF_PbodyContactPhyLen', 'BND_Met1Layer')
		tmp2 = self.get_param_KJH4('SRF_Pbodyring', 'SRF_PbodyBottom', 'SRF_PbodyContactPhyLen', 'BND_Met1Layer')
		self._DesignParameter['BND_Left_Vtc_M1']['_YWidth'] = abs(tmp1[0][0][0][0][0]['_XY_up'][1] - tmp2[0][0][0][0][0]['_XY_down'][1])
		
		# Define Boundary_element _XWidth
		tmp = self.get_param_KJH4('BND_Down_PinB_Hrz_M1')
		self._DesignParameter['BND_Left_Vtc_M1']['_XWidth'] = tmp[0][0]['_Ywidth']
		
		# Define Boundary_element _XYCoordinates
		self._DesignParameter['BND_Left_Vtc_M1']['_XYCoordinates'] = [[0, 0]]
		
		## Get_Scoord_v4.
		## Calculate Sref XYcoord
		tmpXY = []
		## initialized Sref coordinate
		self._DesignParameter['BND_Left_Vtc_M1']['_XYCoordinates'] = [[0, 0]]
		## Calculate
		## Target_coord: _XY_type1
		##X
		tmp1_1 = self.get_param_KJH4('SRF_RArray', 'SRF_PolyRes_Dummy_Left', 'BND_PinA_M1')
		target_coordx = tmp1_1[0][0][0][0]['_XY_cent'][0]
		##Y
		tmp1_2 = self.get_param_KJH4('SRF_Pbodyring', 'SRF_PbodyTop', 'SRF_PbodyContactPhyLen', 'BND_Met1Layer')
		target_coordy = tmp1_2[0][0][0][0][0]['_XY_up'][1]
		target_coord = [target_coordx, target_coordy]
		
		## Approaching_coord: _XY_type2
		tmp2 = self.get_param_KJH4('BND_Left_Vtc_M1')
		approaching_coord = tmp2[0][0]['_XY_up']
		## Sref coord
		tmp3 = self.get_param_KJH4('BND_Left_Vtc_M1')
		Scoord = tmp3[0][0]['_XY_origin']
		## Cal
		New_Scoord = self.get_Scoord_KJH4(target_coord, approaching_coord, Scoord)
		tmpXY.append(New_Scoord)
		## Define Coordinates
		self._DesignParameter['BND_Left_Vtc_M1']['_XYCoordinates'] = tmpXY
		
		## ########## ########## ########## ########## ########## ########## ########## ########## ########## ########## ########## Dummy Pin M1 Connection : Right Vtc M1
		# Define Boundary_element
		self._DesignParameter['BND_Right_Vtc_M1'] = self._BoundaryElementDeclaration(
			_Layer=DesignParameters._LayerMapping['METAL1'][0],
			_Datatype=DesignParameters._LayerMapping['METAL1'][1],
			_XWidth=None,
			_YWidth=None,
			_XYCoordinates=[],
		)
		
		# Define Boundary_element _YWidth
		tmp1 = self.get_param_KJH4('SRF_Pbodyring', 'SRF_PbodyTop', 'SRF_PbodyContactPhyLen', 'BND_Met1Layer')
		tmp2 = self.get_param_KJH4('SRF_Pbodyring', 'SRF_PbodyBottom', 'SRF_PbodyContactPhyLen', 'BND_Met1Layer')
		self._DesignParameter['BND_Right_Vtc_M1']['_YWidth'] = abs(tmp1[0][0][0][0][0]['_XY_up'][1] - tmp2[0][0][0][0][0]['_XY_down'][1])
		
		# Define Boundary_element _XWidth
		tmp = self.get_param_KJH4('BND_Down_PinB_Hrz_M1')
		self._DesignParameter['BND_Right_Vtc_M1']['_XWidth'] = tmp[0][0]['_Ywidth']
		
		# Define Boundary_element _XYCoordinates
		self._DesignParameter['BND_Right_Vtc_M1']['_XYCoordinates'] = [[0, 0]]
		
		## Get_Scoord_v4.
		## Calculate Sref XYcoord
		tmpXY = []
		## initialized Sref coordinate
		self._DesignParameter['BND_Right_Vtc_M1']['_XYCoordinates'] = [[0, 0]]
		## Calculate
		## Target_coord: _XY_type1
		##X
		tmp1_1 = self.get_param_KJH4('SRF_RArray', 'SRF_PolyRes_Dummy_Right', 'BND_PinA_M1')
		target_coordx = tmp1_1[0][0][0][0]['_XY_cent'][0]
		##Y
		tmp1_2 = self.get_param_KJH4('SRF_Pbodyring', 'SRF_PbodyTop', 'SRF_PbodyContactPhyLen', 'BND_Met1Layer')
		target_coordy = tmp1_2[0][0][0][0][0]['_XY_up'][1]
		target_coord = [target_coordx, target_coordy]
		
		## Approaching_coord: _XY_type2
		tmp2 = self.get_param_KJH4('BND_Right_Vtc_M1')
		approaching_coord = tmp2[0][0]['_XY_up']
		## Sref coord
		tmp3 = self.get_param_KJH4('BND_Right_Vtc_M1')
		Scoord = tmp3[0][0]['_XY_origin']
		## Cal
		New_Scoord = self.get_Scoord_KJH4(target_coord, approaching_coord, Scoord)
		tmpXY.append(New_Scoord)
		## Define Coordinates
		self._DesignParameter['BND_Right_Vtc_M1']['_XYCoordinates'] = tmpXY

		## ########## ########## ########## ########## ########## ########## ########## ########## ########## ########## ########## ########## VREF pin
		## ########## ########## ########## ########## ########## ########## ########## ########## ########## ########## ########## VREF pin: ViaM1M2
		## ########## ########## ########## ########## ########## ########## ########## ########## ########## ########## VREF pin: ViaM1M4: Gen SREF
		## Define ViaX Parameter
		_Caculation_Parameters = copy.deepcopy(A02_ViaStack_KJH3._ViaStack._ParametersForDesignCalculation)
		_Caculation_Parameters['_Layer1'] = 1
		_Caculation_Parameters['_Layer2'] = 2
		_Caculation_Parameters['_COX'] = None
		_Caculation_Parameters['_COY'] = None
		
		## Sref ViaX declaration
		self._DesignParameter['SRF_Vref_ViaM1M2'] = self._SrefElementDeclaration(_DesignObj=A02_ViaStack_KJH3._ViaStack(_DesignParameter=None, _Name='{}:SRF_Vref_ViaM1M2'.format(_Name)))[0]
		
		## Define Sref Relection
		self._DesignParameter['SRF_Vref_ViaM1M2']['_Reflect'] = [0, 0, 0]
		
		## Define Sref Angle
		self._DesignParameter['SRF_Vref_ViaM1M2']['_Angle'] = 0
		
		## Define _COX and _COY

		## Calcuate Overlapped XYcoord
		tmp1 = self.get_param_KJH4('SRF_RArray','SRF_PolyRes','SRF_PinA_ViaM0M1','SRF_ViaM0M1','BND_Met1Layer')
		tmp2 = self.get_param_KJH4('SRF_RArray','SRF_PolyRes','SRF_PinA_ViaM0M1','SRF_ViaM0M1','BND_Met1Layer')
		Ovlpcoord = self.get_ovlp_KJH2(tmp1[0][0][0][0][0][0], tmp2[0][0][0][0][0][0])

		## Calcuate _COX and _COY:  None or 'MinEnclosureX' or 'MinEnclosureY' or 'SameEnclosure'
		_COX, _COY = self._CalculateNumViaByXYWidth(Ovlpcoord[0]['_Xwidth'], Ovlpcoord[0]['_Ywidth'], 'MinEnclosureY')
		_Caculation_Parameters['_COX'] = _COX
		_Caculation_Parameters['_COY'] = _COY

		## tmp = self.get_param_KJH4('SRF_RArray','SRF_ResConn_ViaM1M3','SRF_ViaM2M3','BND_COLayer')
		## tmp2 = tmp[0][0][0]
		## for i in range(0,len(tmp2)):
		## 	if i == 0:
		## 		j = tmp2[0][0]['_XY_up'][1]
		## 		row = 1
		## 	else:
		## 		if j == tmp2[i][0]['_XY_up'][1]:
		## 			row=row+1
		## 		else:
		## 			pass
		##
		## _Caculation_Parameters['_COX'] = row
		## _Caculation_Parameters['_COY'] = int(len(tmp2)/row)
		
		## Generate Metal(x), Metal(x+1) and C0(Viax) layer:  Option: _CalculateDesignParameter, _CalculateDesignParameterXmin, _CalculateDesignParameterYmin, _CalculateDesignParameterXYsame
		self._DesignParameter['SRF_Vref_ViaM1M2']['_DesignObj']._CalculateDesignParameterYmin(**_Caculation_Parameters)
		
		# Define coord
		self._DesignParameter['SRF_Vref_ViaM1M2']['_XYCoordinates'] = [[0, 0]]
		
		## ########## ########## ########## ########## ########## ########## ########## ########## ########## ########## VREF pin: ViaM1M3: Cal coord.
		# Flag represent the start point of connection
		if _Size[1] % 2 == 0:
			flag = -1 # Start with PinB
		else:
			flag = +1 # Start with PinA
			
		tmpXY = []
		# Calculation
		for j in range(0, _Size[0]): #Row
			for i in range(0, _Size[1]): #Column
				if flag == -1:
					## Get_Scoord_v4.
					## Calculate Sref XYcoord
					## Calculate
					## Target_coord: _XY_type1
					tmp1 = self.get_param_KJH4('SRF_RArray', 'SRF_PolyRes', 'BND_PinB_M1')
					target_coord = tmp1[0][j*_Size[1]+i][0][0]['_XY_cent']
					## Approaching_coord: _XY_type2
					tmp2 = self.get_param_KJH4('SRF_Vref_ViaM1M2','SRF_ViaM1M2','BND_Met1Layer')
					approaching_coord = tmp2[0][0][0][0]['_XY_cent']
					## Sref coord
					tmp3 = self.get_param_KJH4('SRF_Vref_ViaM1M2')
					Scoord = tmp3[0][0]['_XY_origin']
					## Cal
					New_Scoord = self.get_Scoord_KJH4(target_coord, approaching_coord, Scoord)
					tmpXY.append(New_Scoord)
					flag = -flag
				else:
					## Get_Scoord_v4.
					## Calculate Sref XYcoord
					## Calculate
					## Target_coord: _XY_type1
					tmp1 = self.get_param_KJH4('SRF_RArray', 'SRF_PolyRes', 'BND_PinA_M1')
					target_coord = tmp1[0][j*_Size[1]+i][0][0]['_XY_cent']
					## Approaching_coord: _XY_type2
					tmp2 = self.get_param_KJH4('SRF_Vref_ViaM1M2','SRF_ViaM1M2','BND_Met1Layer')
					approaching_coord = tmp2[0][0][0][0]['_XY_cent']
					## Sref coord
					tmp3 = self.get_param_KJH4('SRF_Vref_ViaM1M2')
					Scoord = tmp3[0][0]['_XY_origin']
					## Cal
					New_Scoord = self.get_Scoord_KJH4(target_coord, approaching_coord, Scoord)
					tmpXY.append(New_Scoord)
					flag = -flag
			flag = -flag
		## Define Coordinates
		self._DesignParameter['SRF_Vref_ViaM1M2']['_XYCoordinates'] = tmpXY

		## ########## ########## ########## ########## ########## ########## ########## ########## ########## ########## ########## VREF pin: Hrz M4
		## Pre-defined
		Metal_width = 50
		additional_length = 80
		
		
		for j in range(0,_Size[0]):
			for i in range(0,_Size[1]):
				tmpXY = []
				# Define Boundary_element
				self._DesignParameter['BND_Vref{}_Hrz_M2'.format(j*_Size[1]+i)] = self._BoundaryElementDeclaration(
					_Layer=DesignParameters._LayerMapping['METAL2'][0],
					_Datatype=DesignParameters._LayerMapping['METAL2'][1],
					_XWidth=None,
					_YWidth=None,
					_XYCoordinates=[],
				)
				
				# Define Boundary_element _YWidth
				tmp = self.get_param_KJH4('SRF_Vref_ViaM1M2', 'SRF_ViaM1M2', 'BND_Met2Layer')
				self._DesignParameter['BND_Vref{}_Hrz_M2'.format(j*_Size[1]+i)]['_YWidth'] = tmp[0][0][0][0]['_Ywidth']
				
				# Define Boundary_element _XWidth
				tmp = self.get_param_KJH4('SRF_RArray','SRF_PolyRes','BND_PinA_M1')
				self._DesignParameter['BND_Vref{}_Hrz_M2'.format(j*_Size[1]+i)]['_XWidth'] = abs( tmp[0][0][0][0]['_XY_left'][0] - tmp[0][1][0][0]['_XY_left'][0] ) -2*Metal_width - additional_length*j - Metal_width*j
				
				# Define Boundary_element _XYCoordinates
				self._DesignParameter['BND_Vref{}_Hrz_M2'.format(j*_Size[1]+i)]['_XYCoordinates'] = [[0,0]]
		
				## Get_Scoord_v4.
					## Calculate Sref XYcoord
						## Calculate
							## Target_coord: _XY_type1
				tmp1 = self.get_param_KJH4('SRF_Vref_ViaM1M2', 'SRF_ViaM1M2', 'BND_Met2Layer')
				target_coord = tmp1[j * _Size[1] + i][0][0][0]['_XY_down_left']
							## Approaching_coord: _XY_type2
				tmp2 = self.get_param_KJH4('BND_Vref{}_Hrz_M2'.format(j*_Size[1]+i))
				approaching_coord = tmp2[0][0]['_XY_down_left']
							## Sref coord
				tmp3 = self.get_param_KJH4('BND_Vref{}_Hrz_M2'.format(j*_Size[1]+i))
				Scoord = tmp3[0][0]['_XY_origin']
							## Cal
				New_Scoord = self.get_Scoord_KJH4(target_coord, approaching_coord, Scoord)
				tmpXY.append(New_Scoord)

				## Define Coordinates
				self._DesignParameter['BND_Vref{}_Hrz_M2'.format(j*_Size[1]+i)]['_XYCoordinates'] = tmpXY

		## ########## ########## ########## ########## ########## ########## ########## ########## ########## ########## ########## VREF pin: Vtc M2
		##Pre-define
		additional_length2 = 100

		for j in range(0, _Size[0]):
			for i in range(0, _Size[1]):
				tmpXY = []
				# Define Boundary_element
				self._DesignParameter['BND_Vref{}_Vtc_M2'.format(j * _Size[1] + i)] = self._BoundaryElementDeclaration(
					_Layer=DesignParameters._LayerMapping['METAL2'][0],
					_Datatype=DesignParameters._LayerMapping['METAL2'][1],
					_XWidth=None,
					_YWidth=None,
					_XYCoordinates=[],
				)

				# Define Boundary_element _YWidth
				tmp1 = self.get_param_KJH4('BND_Vref{}_Hrz_M2'.format(j*_Size[1]+i))
				tmp2 = self.get_param_KJH4('SRF_Pbodyring', 'SRF_PbodyBottom', 'SRF_PbodyContactPhyLen', 'BND_Met1Layer')
				self._DesignParameter['BND_Vref{}_Vtc_M2'.format(j * _Size[1] + i)]['_YWidth'] = abs( tmp1[0][0]['_XY_up'][1] - tmp2[0][0][0][0][0]['_XY_down'][1] ) + 100 + additional_length2*(j*_Size[1]+i)

				# Define Boundary_element _XWidth
				self._DesignParameter['BND_Vref{}_Vtc_M2'.format(j * _Size[1] + i)]['_XWidth'] = Metal_width

				# Define Boundary_element _XYCoordinates
				self._DesignParameter['BND_Vref{}_Vtc_M2'.format(j * _Size[1] + i)]['_XYCoordinates'] = [[0, 0]]

				## Get_Scoord_v4.
				## Calculate Sref XYcoord
				## Calculate
				## Target_coord: _XY_type1
				tmp1 = self.get_param_KJH4('BND_Vref{}_Hrz_M2'.format(j*_Size[1]+i))
				target_coord = tmp1[0][0]['_XY_up_right']
				## Approaching_coord: _XY_type2
				tmp2 = self.get_param_KJH4('BND_Vref{}_Vtc_M2'.format(j * _Size[1] + i))
				approaching_coord = tmp2[0][0]['_XY_up_right']
				## Sref coord
				tmp3 = self.get_param_KJH4('BND_Vref{}_Vtc_M2'.format(j * _Size[1] + i))
				Scoord = tmp3[0][0]['_XY_origin']
				## Cal
				New_Scoord = self.get_Scoord_KJH4(target_coord, approaching_coord, Scoord)
				tmpXY.append(New_Scoord)

				## Define Coordinates
				self._DesignParameter['BND_Vref{}_Vtc_M2'.format(j * _Size[1] + i)]['_XYCoordinates'] = tmpXY

				## ########## ########## ########## ########## ########## ########## ########## ########## ########## ########## ########## VREF pin: ViaM2M3
				## Sref generation: ViaX
				## Define ViaX Parameter
				_Caculation_Parameters = copy.deepcopy(A02_ViaStack_KJH3._ViaStack._ParametersForDesignCalculation)
				_Caculation_Parameters['_Layer1'] = 2
				_Caculation_Parameters['_Layer2'] = 3
				_Caculation_Parameters['_COX'] = 2
				_Caculation_Parameters['_COY'] = 1

				## Sref ViaX declaration
				self._DesignParameter['SRF_Vref{}_ViaM2M3'.format(j * _Size[1] + i)] = self._SrefElementDeclaration(_DesignObj=A02_ViaStack_KJH3._ViaStack(_DesignParameter=None, _Name='{}:SRF_Vref{}_ViaM2M3'.format(_Name,j * _Size[1] + i)))[0]

				## Define Sref Relection
				self._DesignParameter['SRF_Vref{}_ViaM2M3'.format(j * _Size[1] + i)]['_Reflect'] = [0, 0, 0]

				## Define Sref Angle
				self._DesignParameter['SRF_Vref{}_ViaM2M3'.format(j * _Size[1] + i)]['_Angle'] = 0

				## Generate Metal(x), Metal(x+1) and C0(Viax) layer:  Option: _CalculateDesignParameter, _CalculateDesignParameterXmin, _CalculateDesignParameterYmin, _CalculateDesignParameterXYsame
				self._DesignParameter['SRF_Vref{}_ViaM2M3'.format(j * _Size[1] + i)]['_DesignObj']._CalculateDesignParameterYmin(**_Caculation_Parameters)

				## Calculate Sref XYcoord
				tmpXY = []
				## initialized Sref coordinate
				self._DesignParameter['SRF_Vref{}_ViaM2M3'.format(j * _Size[1] + i)]['_XYCoordinates'] = [[0, 0]]
				## Calculate
				## Target_coord
				tmp1 = self.get_param_KJH4('BND_Vref{}_Vtc_M2'.format(j * _Size[1] + i))
				if i ==_Size[1]-1:
					target_coord = tmp1[0][0]['_XY_down_right']
				else:
					pass
					target_coord = tmp1[0][0]['_XY_down_left']
				## Approaching_coord
				tmp2 = self.get_param_KJH4('SRF_Vref{}_ViaM2M3'.format(j * _Size[1] + i),'SRF_ViaM2M3','BND_Met2Layer')
				approaching_coord = tmp2[0][0][0][0]['_XY_down_left']
				## Sref coord
				tmp3 = self.get_param_KJH4('SRF_Vref{}_ViaM2M3'.format(j * _Size[1] + i))
				Scoord = tmp3[0][0]['_XY_origin']
				## Calculate
				New_Scoord = self.get_Scoord_KJH4(target_coord, approaching_coord, Scoord)

				if i ==_Size[1]-1:
					X_extension = 50
					New_Scoord[0] = New_Scoord[0] + X_extension

					## Boundary_element Generation
					Element_name = 'FuckingCode{}'.format(j)
					## Generate Boundary_element: ex)LayerName: METAL1 / DIFF (_ODLayer) / POLY / PIMP (_PPLayer) / NWELL / SLVT LVT RVT HVT / OP(OPpress) / CONT (CA) / PCCRIT
					self._DesignParameter[Element_name] = self._BoundaryElementDeclaration(
						_Layer=DesignParameters._LayerMapping['METAL2'][0],
						_Datatype=DesignParameters._LayerMapping['METAL2'][1],
						_XWidth=None,
						_YWidth=None,
						_XYCoordinates=[],
					)

					## Define Boundary_element _YWidth
					self._DesignParameter[Element_name]['_YWidth'] = 50

					## Define Boundary_element _XWidth
					self._DesignParameter[Element_name]['_XWidth'] = X_extension

					## Define Boundary_element _XYCoordinates
					self._DesignParameter[Element_name]['_XYCoordinates'] = [[0, 0]]

					## Calculate Sref XYcoord
					tmpXY2 = []
					## initialized Sref coordinate
					self._DesignParameter[Element_name]['_XYCoordinates'] = [[0, 0]]
					## Calculate
					## Target_coord: _XY_type1
					tmp1 = self.get_param_KJH4('BND_Vref{}_Vtc_M2'.format(j * _Size[1] + i))
					target_coord = tmp1[0][0]['_XY_down_right']
					## Approaching_coord: _XY_type2
					tmp2 = self.get_param_KJH4(Element_name)
					approaching_coord = tmp2[0][0]['_XY_down_left']
					## Sref coord
					tmp3 = self.get_param_KJH4(Element_name)
					Scoord = tmp3[0][0]['_XY_origin']
					## Cal
					New_Scoord2 = self.get_Scoord_KJH4(target_coord, approaching_coord, Scoord)
					tmpXY2.append(New_Scoord2)
					## Define coordinates
					self._DesignParameter[Element_name]['_XYCoordinates'] = tmpXY2

				else:
					pass
				tmpXY.append(New_Scoord)
				## Define
				self._DesignParameter['SRF_Vref{}_ViaM2M3'.format(j * _Size[1] + i)]['_XYCoordinates'] = tmpXY

		## ################################################################################################################################# Calculation_End
		print('##############################')
		print('##     Calculation_End      ##')
		print('##############################')


		RDAC_end_time = time.time()
		self.RDAC_elapsed_time = RDAC_end_time - RDAC_start_time

## ########################################################################################################################################################## Start_Main
if __name__ == '__main__':

	''' Check Time'''
	start_time = time.time()

	from KJH91_Projects.Project_ADC.Library_and_Engine.Private import MyInfo
	from KJH91_Projects.Project_ADC.Library_and_Engine import DRCchecker_KJH0

	libname = 'Proj_ZZ01_P00_01_Guardring_Fixed'
	cellname = 'P00_01_Guardring_99'
	_fileName = cellname + '.gds'

	''' Input Parameters for Layout Object '''
	InputParams = dict(
#ResArray
	#Array
	_Size		= [3 ,7],
	#Unit Resistor
	_ResWidth	=	1300,
	_ResLength	=	1500,
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
	LayoutObj = _Guardring(_DesignParameter=None, _Name=cellname)
	LayoutObj._CalculateDesignParameter(**InputParams)
	LayoutObj._UpdateDesignParameter2GDSStructure(_DesignParameterInDictionary=LayoutObj._DesignParameter)
	testStreamFile = open('./{}'.format(_fileName), 'wb')
	tmp = LayoutObj._CreateGDSStream(LayoutObj._DesignParameter['_GDSFile']['_GDSFile'])
	tmp.write_binary_gds_stream(testStreamFile)
	testStreamFile.close()

	''' Check Time'''
	end_time = time.time()
	elapsed_time = end_time - start_time
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
	print('{} Hours   {} minutes   {} seconds'.format(h,m,s))
	# end of 'main():' ---------------------------------------------------------------------------------------------




