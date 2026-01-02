from KJH91_Projects.Project_ADC.Library_and_Engine import StickDiagram_KJH1
from KJH91_Projects.Project_ADC.Library_and_Engine import DesignParameters
from KJH91_Projects.Project_ADC.Library_and_Engine import DRC

import numpy as np
import copy
import math
import time
#from SthPack import CoordCalc

from KJH91_Projects.Project_ADC.Layoutgen_code.A_Basic_Building_Block import A02_ViaStack_KJH3
from KJH91_Projects.Project_ADC.Layoutgen_code.A_Basic_Building_Block import A15_PolyRes_KJH2


## ########################################################################################################################################################## Class_HEADER
class _RArray(StickDiagram_KJH1._StickDiagram_KJH):

	## Define input_parameters for Design calculation
	_ParametersForDesignCalculation = dict(

_ResWidth	=	2500,
_ResLength	=	1500,
_CONUMX		=	None,
_CONUMY		=	None,

_Size	= None,

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

_ResWidth	=	2500,
_ResLength	=	1500,
_CONUMX		=	None,
_CONUMY		=	None,

_Size		=	None,

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

		## ########## ########## ########## ########## ########## ########## ########## ########## ########## ########## ########## ########## SRF_RArray
		## Pre-defined
		unit_left_right_distance = 200
		unit_up_down_distance = 200
		
			## SREF Generation
				## Copy Calculation_Parameters from low-level-block ex)copy.deepcopy(B16_nmos_power_v2._NMOS_POWER._ParametersForDesignCalculation)
		_Caculation_Parameters = copy.deepcopy(A15_PolyRes_KJH2._PolyRes_KJH._ParametersForDesignCalculation)
				## Define Calculation_Parameters ex) _Caculation_Parameters['_NMOSPOWER_PbodyContact_1_Length']  = _NMOSPOWER_PbodyContact_1_Length
		_Caculation_Parameters['_ResWidth'] = _ResWidth
		_Caculation_Parameters['_ResLength'] = _ResLength
		_Caculation_Parameters['_CONUMX'] = _CONUMX
		_Caculation_Parameters['_CONUMY'] = _CONUMY

				## Generate Sref: ex)self._DesignParameter['_NMOS_POWER'] = self._SrefElementDeclaration(_DesignObj=B16_nmos_power_v2._NMOS_POWER( _DesignParameter=None, _Name='{}:NMOS_POWER'.format(_Name)))[0]
		self._DesignParameter['SRF_PolyRes'] = self._SrefElementDeclaration(_DesignObj=A15_PolyRes_KJH2._PolyRes_KJH(_DesignParameter=None, _Name='{}:SRF_PolyRes'.format(_Name)))[0]

				## Define Sref Reflection: ex)self._DesignParameter['_NMOS_POWER']['_Reflect'] = [0, 0, 0]
		self._DesignParameter['SRF_PolyRes']['_Reflect'] = [0, 0, 0]

				## Define Sref Angle: ex)'_NMOS_POWER'
		self._DesignParameter['SRF_PolyRes']['_Angle'] = 0

				## Calculate Sref Layer by using Calculation_Parameter: ex)'_NMOS_POWER'
		self._DesignParameter['SRF_PolyRes']['_DesignObj']._CalculateDesignParameter(**_Caculation_Parameters)

				## Define Sref _XYcoordinate: ex)'_NMOS_POWER'
		self._DesignParameter['SRF_PolyRes']['_XYCoordinates'] = [[0, 0]]

				## Get_Scoord_v4.
					## Calculate Sref XYcoord
		tmpXY = [[0,0]]
						## initialized Sref coordinate
		self._DesignParameter['SRF_PolyRes']['_XYCoordinates'] = [[0, 0]]

					## Get_Outter : tmp['_Most--']['coord'] ex) down, left, right, up
						## Most right
		tmp = self.get_outter_KJH4('SRF_PolyRes')
		output_element = tmp['_Mostright']['index']
		output_elementname_right = tmp['_Layercoord'][output_element[0]][1]

						## Most left
		tmp = self.get_outter_KJH4('SRF_PolyRes')
		output_element = tmp['_Mostleft']['index']
		output_elementname_left = tmp['_Layercoord'][output_element[0]][1]

						## Most up
		tmp = self.get_outter_KJH4('SRF_PolyRes')
		output_element = tmp['_Mostup']['index']
		output_elementname_up = tmp['_Layercoord'][output_element[0]][1]

						## Most down
		tmp = self.get_outter_KJH4('SRF_PolyRes')
		output_element = tmp['_Mostdown']['index']
		output_elementname_down = tmp['_Layercoord'][output_element[0]][1]

		for j in range(0,_Size[0]):
			if j ==0:
				for i in range(0,_Size[1]-1):
									## Calculate
										## Target_coord: _XY_type1
					tmp1 = self.get_param_KJH4(output_elementname_right[0],output_elementname_right[1])
					target_coord = tmp1[i][0][0]['_XY_right']
										## Approaching_coord: _XY_type2
					tmp2 = self.get_param_KJH4(output_elementname_left[0],output_elementname_left[1])
					approaching_coord = tmp2[0][0][0]['_XY_left']
										## Sref coord
					tmp3 = self.get_param_KJH4('SRF_PolyRes')
					Scoord = tmp3[0][0]['_XY_origin']
										## Cal
					New_Scoord = self.get_Scoord_KJH4(target_coord, approaching_coord, Scoord)
					New_Scoord[0] = New_Scoord[0] + unit_left_right_distance
					tmpXY.append(New_Scoord)
										## Define Coordinates
					self._DesignParameter['SRF_PolyRes']['_XYCoordinates'] = tmpXY
			else:
				if j%2==0:
					for i in range(0,_Size[1]):
						if i ==0:
											## Calculate
												## Target_coord: _XY_type1
							tmp1 = self.get_param_KJH4(output_elementname_down[0],output_elementname_down[1])
							target_coord = tmp1[-1][0][0]['_XY_down']
												## Approaching_coord: _XY_type2
							tmp2 = self.get_param_KJH4(output_elementname_up[0],output_elementname_up[1])
							approaching_coord = tmp2[0][0][0]['_XY_up']
												## Sref coord
							tmp3 = self.get_param_KJH4('SRF_PolyRes')
							Scoord = tmp3[0][0]['_XY_origin']
												## Cal
							New_Scoord = self.get_Scoord_KJH4(target_coord, approaching_coord, Scoord)
							New_Scoord[1] = New_Scoord[1] - unit_up_down_distance
							tmpXY.append(New_Scoord)
												## Define Coordinates
							self._DesignParameter['SRF_PolyRes']['_XYCoordinates'] = tmpXY

						else:
											## Calculate
												## Target_coord: _XY_type1
							tmp1 = self.get_param_KJH4(output_elementname_right[0],output_elementname_right[1])
							target_coord = tmp1[-1][0][0]['_XY_right']
												## Approaching_coord: _XY_type2
							tmp2 = self.get_param_KJH4(output_elementname_left[0],output_elementname_left[1])
							approaching_coord = tmp2[0][0][0]['_XY_left']
												## Sref coord
							tmp3 = self.get_param_KJH4('SRF_PolyRes')
							Scoord = tmp3[0][0]['_XY_origin']
												## Cal
							New_Scoord = self.get_Scoord_KJH4(target_coord, approaching_coord, Scoord)
							New_Scoord[0] = New_Scoord[0] + unit_left_right_distance
							tmpXY.append(New_Scoord)
												## Define Coordinates
							self._DesignParameter['SRF_PolyRes']['_XYCoordinates'] = tmpXY
				else:
					for i in range(0,_Size[1]):
						if i ==0:
											## Calculate
												## Target_coord: _XY_type1
							tmp1 = self.get_param_KJH4(output_elementname_down[0],output_elementname_down[1])
							target_coord = tmp1[-1][0][0]['_XY_down']
												## Approaching_coord: _XY_type2
							tmp2 = self.get_param_KJH4(output_elementname_up[0],output_elementname_up[1])
							approaching_coord = tmp2[0][0][0]['_XY_up']
												## Sref coord
							tmp3 = self.get_param_KJH4('SRF_PolyRes')
							Scoord = tmp3[0][0]['_XY_origin']
												## Cal
							New_Scoord = self.get_Scoord_KJH4(target_coord, approaching_coord, Scoord)
							New_Scoord[1] = New_Scoord[1] - unit_up_down_distance
							tmpXY.append(New_Scoord)
												## Define Coordinates
							self._DesignParameter['SRF_PolyRes']['_XYCoordinates'] = tmpXY

						else:
											## Calculate
												## Target_coord: _XY_type1
							tmp1 = self.get_param_KJH4(output_elementname_left[0],output_elementname_left[1])
							target_coord = tmp1[-1][0][0]['_XY_left']
												## Approaching_coord: _XY_type2
							tmp2 = self.get_param_KJH4(output_elementname_right[0],output_elementname_right[1])
							approaching_coord = tmp2[0][0][0]['_XY_right']
												## Sref coord
							tmp3 = self.get_param_KJH4('SRF_PolyRes')
							Scoord = tmp3[0][0]['_XY_origin']
												## Cal
							New_Scoord = self.get_Scoord_KJH4(target_coord, approaching_coord, Scoord)
							New_Scoord[0] = New_Scoord[0] - unit_left_right_distance
							tmpXY.append(New_Scoord)
												## Define Coordinates
							self._DesignParameter['SRF_PolyRes']['_XYCoordinates'] = tmpXY
			
		## ########## ########## ########## ########## ########## ########## ########## ########## ########## ########## ########## ########## BND_PPLayer
		#Define Boundary_element
		self._DesignParameter['BND_PP_cover'] = self._BoundaryElementDeclaration(
																				_Layer=DesignParameters._LayerMapping['PIMP'][0],
																				_Datatype=DesignParameters._LayerMapping['PIMP'][1],
																				_XWidth=None,
																				_YWidth=None,
																				_XYCoordinates=[ ],
																			   )

		#Define Boundary_element _YWidth
		tmp = self.get_param_KJH4('SRF_PolyRes','BND_PPLayer')
		self._DesignParameter['BND_PP_cover']['_YWidth'] = tmp[0][0][0]['_XY_up'][1] - tmp[-1][0][0]['_XY_down'][1]

		#Define Boundary_element _XWidth
		self._DesignParameter['BND_PP_cover']['_XWidth'] = abs( tmp[0][0][0]['_XY_left'][0] - tmp[_Size[1]-1][0][0]['_XY_right'][0] )

		#Define coord
		self._DesignParameter['BND_PP_cover']['_XYCoordinates'] = [[0,0]]

		# Calculate Sref XYcoord
		# Target_coord
		tmp1 = self.get_param_KJH4('SRF_PolyRes','BND_PPLayer')
		target_coord = tmp1[0][0][0]['_XY_up_left']
		# Approaching_coord
		tmp2 = self.get_param_KJH4('BND_PP_cover')
		approaching_coord = tmp2[0][0]['_XY_up_left']
		# Sref coord
		tmp3 = self.get_param_KJH4('BND_PP_cover')
		Scoord = tmp3[0][0]['_XY_origin']
		# Cal
		New_Scoord = self.get_Scoord_KJH4(target_coord, approaching_coord, Scoord)

		# Define coord
		self._DesignParameter['BND_PP_cover']['_XYCoordinates'] = [New_Scoord]
		
		## ########## ########## ########## ########## ########## ########## ########## ########## ########## ########## ########## ########## BND_PRES cover
		#Define Boundary_element
		self._DesignParameter['BND_PRES_cover'] = self._BoundaryElementDeclaration(
																				_Layer=DesignParameters._LayerMapping['PRES'][0],
																				_Datatype=DesignParameters._LayerMapping['PRES'][1],
																				_XWidth=None,
																				_YWidth=None,
																				_XYCoordinates=[ ],
																			   )

		#Define Boundary_element _YWidth
		tmp = self.get_param_KJH4('SRF_PolyRes','BND_PRESLayer')
		self._DesignParameter['BND_PRES_cover']['_YWidth'] = tmp[0][0][0]['_XY_up'][1] - tmp[-1][0][0]['_XY_down'][1]

		#Define Boundary_element _XWidth
		self._DesignParameter['BND_PRES_cover']['_XWidth'] = abs( tmp[0][0][0]['_XY_left'][0] - tmp[_Size[1]-1][0][0]['_XY_right'][0] )

		#Define coord
		self._DesignParameter['BND_PRES_cover']['_XYCoordinates'] = [[0,0]]

		# Calculate Sref XYcoord
		# Target_coord
		tmp1 = self.get_param_KJH4('SRF_PolyRes','BND_PRESLayer')
		target_coord = tmp1[0][0][0]['_XY_up_left']
		# Approaching_coord
		tmp2 = self.get_param_KJH4('BND_PRES_cover')
		approaching_coord = tmp2[0][0]['_XY_up_left']
		# Sref coord
		tmp3 = self.get_param_KJH4('BND_PRES_cover')
		Scoord = tmp3[0][0]['_XY_origin']
		# Cal
		New_Scoord = self.get_Scoord_KJH4(target_coord, approaching_coord, Scoord)

		# Define coord
		self._DesignParameter['BND_PRES_cover']['_XYCoordinates'] = [New_Scoord]


		## ########## ########## ########## ########## ########## ########## ########## ########## ########## ########## ########## ########## BND Res connect M1
		#Define Boundary_element
		self._DesignParameter['BND_ResConn_Hrz_M1'] = self._BoundaryElementDeclaration(
																				_Layer=DesignParameters._LayerMapping['METAL1'][0],
																				_Datatype=DesignParameters._LayerMapping['METAL1'][1],
																				_XWidth=None,
																				_YWidth=None,
																				_XYCoordinates=[ ],
																			   )

		#Define Boundary_element _YWidth
		tmp = self.get_param_KJH4('SRF_PolyRes','SRF_PinA_ViaM0M1','SRF_ViaM0M1','BND_Met1Layer')
		self._DesignParameter['BND_ResConn_Hrz_M1']['_YWidth'] = tmp[0][0][0][0][0]['_Ywidth']

		#Define Boundary_element _XWidth
		tmp = self.get_param_KJH4('SRF_PolyRes','SRF_PinA_ViaM0M1','SRF_ViaM0M1','BND_Met1Layer')
		self._DesignParameter['BND_ResConn_Hrz_M1']['_XWidth'] = abs( tmp[0][0][0][0][0]['_XY_left'][0] - tmp[1][0][0][0][0]['_XY_right'][0] )

		#Define coord
		self._DesignParameter['BND_ResConn_Hrz_M1']['_XYCoordinates'] = [[0,0]]

		# Calculate Sref XYcoord
		tmpXY =[]

			# Flag represent the start point of connection
		if _Size[1]%2 ==0:
			flag = -1
		else:
			flag = +1

			# Calculation
		for j in range(0,_Size[0]):
			for i in range(0,_Size[1]-1):

				if j %2 ==0:
					if flag == 1:
						# Target_coord
						tmp1 = self.get_param_KJH4('SRF_PolyRes','SRF_PinB_ViaM0M1','SRF_ViaM0M1','BND_Met1Layer')
						target_coord = tmp1[j*_Size[1]+i][0][0][0][0]['_XY_up_left']
						# Approaching_coord
						tmp2 = self.get_param_KJH4('BND_ResConn_Hrz_M1')
						approaching_coord = tmp2[0][0]['_XY_up_left']
						# Sref coord
						tmp3 = self.get_param_KJH4('BND_ResConn_Hrz_M1')
						Scoord = tmp3[0][0]['_XY_origin']
						# Cal
						New_Scoord = self.get_Scoord_KJH4(target_coord, approaching_coord, Scoord)
						tmpXY.append(New_Scoord)
						flag = -flag

					else:
						# Target_coord
						tmp1 = self.get_param_KJH4('SRF_PolyRes','SRF_PinA_ViaM0M1','SRF_ViaM0M1','BND_Met1Layer')
						target_coord = tmp1[j*_Size[1]+i][0][0][0][0]['_XY_up_left']
						# Approaching_coord
						tmp2 = self.get_param_KJH4('BND_ResConn_Hrz_M1')
						approaching_coord = tmp2[0][0]['_XY_up_left']
						# Sref coord
						tmp3 = self.get_param_KJH4('BND_ResConn_Hrz_M1')
						Scoord = tmp3[0][0]['_XY_origin']
						# Cal
						New_Scoord = self.get_Scoord_KJH4(target_coord, approaching_coord, Scoord)
						tmpXY.append(New_Scoord)
						flag = -flag
				else:
					if flag == 1:
						# Target_coord
						tmp1 = self.get_param_KJH4('SRF_PolyRes', 'SRF_PinB_ViaM0M1', 'SRF_ViaM0M1', 'BND_Met1Layer')
						target_coord = tmp1[j*_Size[1] + i][0][0][0][0]['_XY_up_right']
						# Approaching_coord
						tmp2 = self.get_param_KJH4('BND_ResConn_Hrz_M1')
						approaching_coord = tmp2[0][0]['_XY_up_right']
						# Sref coord
						tmp3 = self.get_param_KJH4('BND_ResConn_Hrz_M1')
						Scoord = tmp3[0][0]['_XY_origin']
						# Cal
						New_Scoord = self.get_Scoord_KJH4(target_coord, approaching_coord, Scoord)
						tmpXY.append(New_Scoord)
						flag = -flag

					else:
						# Target_coord
						tmp1 = self.get_param_KJH4('SRF_PolyRes', 'SRF_PinA_ViaM0M1', 'SRF_ViaM0M1', 'BND_Met1Layer')
						target_coord = tmp1[j*_Size[1] + i][0][0][0][0]['_XY_up_right']
						# Approaching_coord
						tmp2 = self.get_param_KJH4('BND_ResConn_Hrz_M1')
						approaching_coord = tmp2[0][0]['_XY_up_right']
						# Sref coord
						tmp3 = self.get_param_KJH4('BND_ResConn_Hrz_M1')
						Scoord = tmp3[0][0]['_XY_origin']
						# Cal
						New_Scoord = self.get_Scoord_KJH4(target_coord, approaching_coord, Scoord)
						tmpXY.append(New_Scoord)
						flag = -flag
		# Define coord
		self._DesignParameter['BND_ResConn_Hrz_M1']['_XYCoordinates'] = tmpXY


		## ########## ########## ########## ########## ########## ########## ########## ########## ########## ########## ########## ########## BND Res connect Vtc M1 or M2
		## ########## ########## ########## ########## ########## ########## ########## ########## ########## ########## ########## BND Res connect Vtc M1 or M2: Define M1

		#Define Boundary_element
		self._DesignParameter['BND_ResConn_Vtc_M1'] = self._BoundaryElementDeclaration(
																				_Layer=DesignParameters._LayerMapping['METAL1'][0],
																				_Datatype=DesignParameters._LayerMapping['METAL1'][1],
																				_XWidth=None,
																				_YWidth=None,
																				_XYCoordinates=[ ],
																			   )

		#Define Boundary_element _YWidth
		tmp1 = self.get_param_KJH4('SRF_PolyRes','SRF_PinA_ViaM0M1','SRF_ViaM0M1','BND_Met1Layer')
		tmp2 = self.get_param_KJH4('SRF_PolyRes','SRF_PinB_ViaM0M1','SRF_ViaM0M1','BND_Met1Layer')
		if _Size[0] == 1:
			ywidht = 0
		else:
			ywidht = abs( tmp2[0][0][0][0][0]['_XY_up'][1] - tmp1[_Size[1]][0][0][0][0]['_XY_down'][1] )

		self._DesignParameter['BND_ResConn_Vtc_M1']['_YWidth'] = ywidht

		#Define Boundary_element _XWidth
		tmp = self.get_param_KJH4('SRF_PolyRes','SRF_PinA_ViaM0M1','SRF_ViaM0M1','BND_Met1Layer')
		self._DesignParameter['BND_ResConn_Vtc_M1']['_XWidth'] = tmp[0][0][0][0][0]['_Xwidth']

		#Define coord
		self._DesignParameter['BND_ResConn_Vtc_M1']['_XYCoordinates'] = [[0,0]]

		## ########## ########## ########## ########## ########## ########## ########## ########## ########## ########## ########## BND Res connect Vtc M1 or M2: Define M6
		# Define Boundary_element
		self._DesignParameter['BND_ResConn_Vtc_M4'] = self._BoundaryElementDeclaration(
			_Layer=DesignParameters._LayerMapping['METAL4'][0],
			_Datatype=DesignParameters._LayerMapping['METAL4'][1],
			_XWidth=None,
			_YWidth=None,
			_XYCoordinates=[],
		)

		# Define Boundary_element _YWidth
		tmp1 = self.get_param_KJH4('SRF_PolyRes', 'SRF_PinA_ViaM0M1', 'SRF_ViaM0M1', 'BND_Met1Layer')
		tmp2 = self.get_param_KJH4('SRF_PolyRes', 'SRF_PinB_ViaM0M1', 'SRF_ViaM0M1', 'BND_Met1Layer')
		if _Size[0] == 1:
			ywidht2 = 0
		else:
			ywidht2 = abs(tmp1[0][0][0][0][0]['_XY_up'][1] - tmp2[_Size[1]][0][0][0][0]['_XY_down'][1])

		self._DesignParameter['BND_ResConn_Vtc_M4']['_YWidth'] = ywidht2

		# Define Boundary_element _XWidth
		tmp = self.get_param_KJH4('SRF_PolyRes', 'SRF_PinA_ViaM0M1', 'SRF_ViaM0M1', 'BND_Met1Layer')
		self._DesignParameter['BND_ResConn_Vtc_M4']['_XWidth'] = tmp[0][0][0][0][0]['_Xwidth']

		# Define coord
		self._DesignParameter['BND_ResConn_Vtc_M4']['_XYCoordinates'] = [[0, 0]]
		## ########## ########## ########## ########## ########## ########## ########## ########## ########## ########## BND Res connect Vtc M1 or M2: Define M2: ViaM1M4

		## Sref generation: ViaX
		## Define ViaX Parameter
		_Caculation_Parameters = copy.deepcopy(A02_ViaStack_KJH3._ViaStack._ParametersForDesignCalculation)
		_Caculation_Parameters['_Layer1'] = 1
		_Caculation_Parameters['_Layer2'] = 4
		_Caculation_Parameters['_COX'] = None
		_Caculation_Parameters['_COY'] = None

		## Sref ViaX declaration
		self._DesignParameter['SRF_ResConn_ViaM1M4'] = self._SrefElementDeclaration(_DesignObj=A02_ViaStack_KJH3._ViaStack(_DesignParameter=None, _Name='{}:SRF_ResConn_ViaM1M4'.format(_Name)))[0]

		## Define Sref Relection
		self._DesignParameter['SRF_ResConn_ViaM1M4']['_Reflect'] = [0, 0, 0]

		## Define Sref Angle
		self._DesignParameter['SRF_ResConn_ViaM1M4']['_Angle'] = 0

		## Calcuate Overlapped XYcoord
		tmp1 = self.get_param_KJH4('SRF_PolyRes','SRF_PinA_ViaM0M1','SRF_ViaM0M1','BND_Met1Layer')
		tmp2 = self.get_param_KJH4('SRF_PolyRes','SRF_PinA_ViaM0M1','SRF_ViaM0M1','BND_Met1Layer')
		Ovlpcoord = self.get_ovlp_KJH2(tmp1[0][0][0][0][0], tmp2[0][0][0][0][0])

		## Calcuate _COX and _COY:  None or 'MinEnclosureX' or 'MinEnclosureY' or 'SameEnclosure'
		_COX, _COY = self._CalculateNumViaByXYWidth(Ovlpcoord[0]['_Xwidth'], Ovlpcoord[0]['_Ywidth'], 'MinEnclosureY')

		## Define _COX and _COY
		_Caculation_Parameters['_COX'] = _COX
		_Caculation_Parameters['_COY'] = _COY

		## Generate Metal(x), Metal(x+1) and C0(Viax) layer:  Option: _CalculateDesignParameter, _CalculateDesignParameterXmin, _CalculateDesignParameterYmin, _CalculateDesignParameterXYsame
		self._DesignParameter['SRF_ResConn_ViaM1M4']['_DesignObj']._CalculateDesignParameterYmin(**_Caculation_Parameters)

		# Define coord
		self._DesignParameter['SRF_ResConn_ViaM1M4']['_XYCoordinates'] = [[0, 0]]

		## ########## ########## ########## ########## ########## ########## ########## ########## ########## ########## ########## BND Res connect Vtc M1 or M2: Calculate Coord.
		# Calculate Sref XYcoord
		tmpXY = []
		tmpXY1 = []
		tmpXY2 = []

			# Flag represent the start point of connection
		# Column
		if _Size[1]%2 == 0:
			flag = -1
		else:
			flag = +1

		# Calculation
		#Row
		for j in range(0, _Size[0]):

			# Check the direction of pin of last column resistor
			for i in range(0, _Size[1]):
				flag = -flag

			# Last Row pass
			if j == _Size[0] - 1:
				pass
			# Ordinary Row
			else:
				if flag==1:
					pass
					### M3
					# Target_coord
					tmp1 = self.get_param_KJH4('SRF_PolyRes', 'SRF_PinA_ViaM0M1', 'SRF_ViaM0M1', 'BND_Met1Layer')
					target_coord = tmp1[j*_Size[1] + i][0][0][0][0]['_XY_up_left']
					# Approaching_coord
					tmp2 = self.get_param_KJH4('BND_ResConn_Vtc_M4')
					approaching_coord = tmp2[0][0]['_XY_up_left']
					# Sref coord
					tmp3 = self.get_param_KJH4('BND_ResConn_Vtc_M4')
					Scoord = tmp3[0][0]['_XY_origin']
					# Cal
					New_Scoord = self.get_Scoord_KJH4(target_coord, approaching_coord, Scoord)
					tmpXY.append(New_Scoord)
					flag=-flag

					### Via1
					# Target_coord
					tmp1 = self.get_param_KJH4('SRF_PolyRes', 'SRF_PinA_ViaM0M1', 'SRF_ViaM0M1', 'BND_Met1Layer')
					target_coord = tmp1[j * _Size[1] + i][0][0][0][0]['_XY_cent']
					# Approaching_coord
					tmp2 = self.get_param_KJH4('SRF_ResConn_ViaM1M4','SRF_ViaM1M2','BND_Met1Layer')
					approaching_coord = tmp2[0][0][0][0]['_XY_cent']
					# Sref coord
					tmp3 = self.get_param_KJH4('SRF_ResConn_ViaM1M4')
					Scoord = tmp3[0][0]['_XY_origin']
					# Cal
					New_Scoord = self.get_Scoord_KJH4(target_coord, approaching_coord, Scoord)
					tmpXY2.append(New_Scoord)

					### Via2
					# Target_coord
					tmp1 = self.get_param_KJH4('SRF_PolyRes', 'SRF_PinB_ViaM0M1', 'SRF_ViaM0M1', 'BND_Met1Layer')
					target_coord = tmp1[j * _Size[1] + i +1 ][0][0][0][0]['_XY_cent']
					# Approaching_coord
					tmp2 = self.get_param_KJH4('SRF_ResConn_ViaM1M4','SRF_ViaM1M2','BND_Met1Layer')
					approaching_coord = tmp2[0][0][0][0]['_XY_cent']
					# Sref coord
					tmp3 = self.get_param_KJH4('SRF_ResConn_ViaM1M4')
					Scoord = tmp3[0][0]['_XY_origin']
					# Cal
					New_Scoord = self.get_Scoord_KJH4(target_coord, approaching_coord, Scoord)
					tmpXY2.append(New_Scoord)

				else:
					# Target_coord
					tmp1 = self.get_param_KJH4('SRF_PolyRes', 'SRF_PinB_ViaM0M1', 'SRF_ViaM0M1', 'BND_Met1Layer')
					target_coord = tmp1[j * _Size[1] + i][0][0][0][0]['_XY_up_left']
					# Approaching_coord
					tmp2 = self.get_param_KJH4('BND_ResConn_Vtc_M1')
					approaching_coord = tmp2[0][0]['_XY_up_left']
					# Sref coord
					tmp3 = self.get_param_KJH4('BND_ResConn_Vtc_M1')
					Scoord = tmp3[0][0]['_XY_origin']
					# Cal
					New_Scoord = self.get_Scoord_KJH4(target_coord, approaching_coord, Scoord)
					tmpXY1.append(New_Scoord)
					flag = -flag
		# Define coord
		self._DesignParameter['BND_ResConn_Vtc_M4']['_XYCoordinates'] = tmpXY
		# Define coord
		self._DesignParameter['BND_ResConn_Vtc_M1']['_XYCoordinates'] = tmpXY1
		# Define coord
		self._DesignParameter['SRF_ResConn_ViaM1M4']['_XYCoordinates'] = tmpXY2

		## ########## ########## ########## ########## ########## ########## ########## ########## ########## ########## ########## ########## SRF PolyRes Dummy
		## ########## ########## ########## ########## ########## ########## ########## ########## ########## ########## ########## SRF PolyRes Dummy: Up
			## SREF Generation
				## Copy Calculation_Parameters from low-level-block ex)copy.deepcopy(B16_nmos_power_v2._NMOS_POWER._ParametersForDesignCalculation)
		_Caculation_Parameters = copy.deepcopy(A15_PolyRes_KJH2._PolyRes_KJH._ParametersForDesignCalculation)
				## Define Calculation_Parameters ex) _Caculation_Parameters['_NMOSPOWER_PbodyContact_1_Length']  = _NMOSPOWER_PbodyContact_1_Length
		_Caculation_Parameters['_ResWidth'] = _ResWidth
		_Caculation_Parameters['_ResLength'] = _ResLength
		_Caculation_Parameters['_CONUMX'] = _CONUMX
		_Caculation_Parameters['_CONUMY'] = _CONUMY

				## Generate Sref: ex)self._DesignParameter['_NMOS_POWER'] = self._SrefElementDeclaration(_DesignObj=B16_nmos_power_v2._NMOS_POWER( _DesignParameter=None, _Name='{}:NMOS_POWER'.format(_Name)))[0]
		self._DesignParameter['SRF_PolyRes_Dummy_Up'] = self._SrefElementDeclaration(_DesignObj=A15_PolyRes_KJH2._PolyRes_KJH(_DesignParameter=None, _Name='{}:SRF_PolyRes_Dummy_Up'.format(_Name)))[0]

				## Define Sref Reflection: ex)self._DesignParameter['_NMOS_POWER']['_Reflect'] = [0, 0, 0]
		self._DesignParameter['SRF_PolyRes_Dummy_Up']['_Reflect'] = [0, 0, 0]

				## Define Sref Angle: ex)'_NMOS_POWER'
		self._DesignParameter['SRF_PolyRes_Dummy_Up']['_Angle'] = 0

				## Calculate Sref Layer by using Calculation_Parameter: ex)'_NMOS_POWER'
		self._DesignParameter['SRF_PolyRes_Dummy_Up']['_DesignObj']._CalculateDesignParameter(**_Caculation_Parameters)

				## Define Sref _XYcoordinate: ex)'_NMOS_POWER'
		self._DesignParameter['SRF_PolyRes_Dummy_Up']['_XYCoordinates'] = [[0, 0]]

				## Get_Outter : tmp['_Most--']['coord'] ex) down, left, right, up
						## Most right
		tmp = self.get_outter_KJH4('SRF_PolyRes_Dummy_Up')
		output_element = tmp['_Mostright']['index']
		output_elementname_right_dummy = tmp['_Layercoord'][output_element[0]][1]

						## Most left
		tmp = self.get_outter_KJH4('SRF_PolyRes_Dummy_Up')
		output_element = tmp['_Mostleft']['index']
		output_elementname_left_dummy = tmp['_Layercoord'][output_element[0]][1]

						## Most up
		tmp = self.get_outter_KJH4('SRF_PolyRes_Dummy_Up')
		output_element = tmp['_Mostup']['index']
		output_elementname_up_dummy = tmp['_Layercoord'][output_element[0]][1]

						## Most down
		tmp = self.get_outter_KJH4('SRF_PolyRes_Dummy_Up')
		output_element = tmp['_Mostdown']['index']
		output_elementname_down_dummy = tmp['_Layercoord'][output_element[0]][1]

		## Get_Scoord_v4.
		## Calculate Sref XYcoord
		tmpXY = []
		## initialized Sref coordinate
		self._DesignParameter['SRF_PolyRes_Dummy_Up']['_XYCoordinates'] = [[0, 0]]
		for i in range(0,_Size[1]):
			if i ==0:
				## Calculate
				## Target_coord: _XY_type1
				tmp1 = self.get_param_KJH4(output_elementname_up[0],output_elementname_up[1])
				target_coord = tmp1[0][0][0]['_XY_up']
				## Approaching_coord: _XY_type2
				tmp2 = self.get_param_KJH4(output_elementname_down_dummy[0],output_elementname_down_dummy[1])
				approaching_coord = tmp2[0][0][0]['_XY_down']
				## Sref coord
				tmp3 = self.get_param_KJH4('SRF_PolyRes_Dummy_Up')
				Scoord = tmp3[0][0]['_XY_origin']
				## Cal
				New_Scoord = self.get_Scoord_KJH4(target_coord, approaching_coord, Scoord)
				tmpXY.append(New_Scoord)
				New_Scoord[1] = New_Scoord[1] + unit_up_down_distance
				## Define Coordinates
				self._DesignParameter['SRF_PolyRes_Dummy_Up']['_XYCoordinates'] = tmpXY
			else:
				## Calculate
				## Target_coord: _XY_type1
				tmp1 = self.get_param_KJH4(output_elementname_right_dummy[0],output_elementname_right_dummy[1])
				target_coord = tmp1[i-1][0][0]['_XY_right']
				## Approaching_coord: _XY_type2
				tmp2 = self.get_param_KJH4(output_elementname_left_dummy[0],output_elementname_left_dummy[1])
				approaching_coord = tmp2[0][0][0]['_XY_left']
				## Sref coord
				tmp3 = self.get_param_KJH4('SRF_PolyRes_Dummy_Up')
				Scoord = tmp3[0][0]['_XY_origin']
				## Cal
				New_Scoord = self.get_Scoord_KJH4(target_coord, approaching_coord, Scoord)
				New_Scoord[0] = New_Scoord[0] + unit_left_right_distance
				tmpXY.append(New_Scoord)
				## Define Coordinates
				self._DesignParameter['SRF_PolyRes_Dummy_Up']['_XYCoordinates'] = tmpXY

		## ########## ########## ########## ########## ########## ########## ########## ########## ########## ########## ########## SRF PolyRes Dummy: Dn
		## SREF Generation
		## Copy Calculation_Parameters from low-level-block ex)copy.deepcopy(B16_nmos_power_v2._NMOS_POWER._ParametersForDesignCalculation)
		_Caculation_Parameters = copy.deepcopy(A15_PolyRes_KJH2._PolyRes_KJH._ParametersForDesignCalculation)
		## Define Calculation_Parameters ex) _Caculation_Parameters['_NMOSPOWER_PbodyContact_1_Length']  = _NMOSPOWER_PbodyContact_1_Length
		_Caculation_Parameters['_ResWidth'] = _ResWidth
		_Caculation_Parameters['_ResLength'] = _ResLength
		_Caculation_Parameters['_CONUMX'] = _CONUMX
		_Caculation_Parameters['_CONUMY'] = _CONUMY

		## Generate Sref: ex)self._DesignParameter['_NMOS_POWER'] = self._SrefElementDeclaration(_DesignObj=B16_nmos_power_v2._NMOS_POWER( _DesignParameter=None, _Name='{}:NMOS_POWER'.format(_Name)))[0]
		self._DesignParameter['SRF_PolyRes_Dummy_Down'] = self._SrefElementDeclaration(_DesignObj=A15_PolyRes_KJH2._PolyRes_KJH(_DesignParameter=None, _Name='{}:SRF_PolyRes_Dummy_Down'.format(_Name)))[0]

		## Define Sref Reflection: ex)self._DesignParameter['_NMOS_POWER']['_Reflect'] = [0, 0, 0]
		self._DesignParameter['SRF_PolyRes_Dummy_Down']['_Reflect'] = [0, 0, 0]

		## Define Sref Angle: ex)'_NMOS_POWER'
		self._DesignParameter['SRF_PolyRes_Dummy_Down']['_Angle'] = 0

		## Calculate Sref Layer by using Calculation_Parameter: ex)'_NMOS_POWER'
		self._DesignParameter['SRF_PolyRes_Dummy_Down']['_DesignObj']._CalculateDesignParameter(**_Caculation_Parameters)

		## Define Sref _XYcoordinate: ex)'_NMOS_POWER'
		self._DesignParameter['SRF_PolyRes_Dummy_Down']['_XYCoordinates'] = [[0, 0]]

		## Get_Outter : tmp['_Most--']['coord'] ex) down, left, right, up
		## Most right
		tmp = self.get_outter_KJH4('SRF_PolyRes_Dummy_Down')
		output_element = tmp['_Mostright']['index']
		output_elementname_right_dummy = tmp['_Layercoord'][output_element[0]][1]

		## Most left
		tmp = self.get_outter_KJH4('SRF_PolyRes_Dummy_Down')
		output_element = tmp['_Mostleft']['index']
		output_elementname_left_dummy = tmp['_Layercoord'][output_element[0]][1]

		## Most up
		tmp = self.get_outter_KJH4('SRF_PolyRes_Dummy_Down')
		output_element = tmp['_Mostup']['index']
		output_elementname_up_dummy = tmp['_Layercoord'][output_element[0]][1]

		## Most down
		tmp = self.get_outter_KJH4('SRF_PolyRes_Dummy_Down')
		output_element = tmp['_Mostdown']['index']
		output_elementname_down_dummy = tmp['_Layercoord'][output_element[0]][1]

		## Get_Scoord_v4.
		## Calculate Sref XYcoord
		tmpXY = []
		## initialized Sref coordinate
		self._DesignParameter['SRF_PolyRes_Dummy_Down']['_XYCoordinates'] = [[0, 0]]
		for i in range(0, _Size[1]):
			if i == 0:
				## Calculate
				## Target_coord: _XY_type1
				tmp1 = self.get_param_KJH4(output_elementname_down[0], output_elementname_down[1])
				if _Size[0]%2 ==0:
					target_coord = tmp1[-1][0][0]['_XY_down']
				else:
					target_coord = tmp1[-_Size[1]][0][0]['_XY_down']

				## Approaching_coord: _XY_type2
				tmp2 = self.get_param_KJH4(output_elementname_up_dummy[0], output_elementname_up_dummy[1])
				approaching_coord = tmp2[0][0][0]['_XY_up']
				## Sref coord
				tmp3 = self.get_param_KJH4('SRF_PolyRes_Dummy_Down')
				Scoord = tmp3[0][0]['_XY_origin']
				## Cal
				New_Scoord = self.get_Scoord_KJH4(target_coord, approaching_coord, Scoord)
				New_Scoord[1] = New_Scoord[1] - unit_up_down_distance
				tmpXY.append(New_Scoord)
				## Define Coordinates
				self._DesignParameter['SRF_PolyRes_Dummy_Down']['_XYCoordinates'] = tmpXY
			else:
				## Calculate
				## Target_coord: _XY_type1
				tmp1 = self.get_param_KJH4(output_elementname_right_dummy[0], output_elementname_right_dummy[1])
				target_coord = tmp1[i - 1][0][0]['_XY_right']
				## Approaching_coord: _XY_type2
				tmp2 = self.get_param_KJH4(output_elementname_left_dummy[0], output_elementname_left_dummy[1])
				approaching_coord = tmp2[0][0][0]['_XY_left']
				## Sref coord
				tmp3 = self.get_param_KJH4('SRF_PolyRes_Dummy_Down')
				Scoord = tmp3[0][0]['_XY_origin']
				## Cal
				New_Scoord = self.get_Scoord_KJH4(target_coord, approaching_coord, Scoord)
				New_Scoord[0] = New_Scoord[0] + unit_left_right_distance
				tmpXY.append(New_Scoord)
				## Define Coordinates
				self._DesignParameter['SRF_PolyRes_Dummy_Down']['_XYCoordinates'] = tmpXY

		## ########## ########## ########## ########## ########## ########## ########## ########## ########## ########## ########## SRF PolyRes Dummy: Left
		## SREF Generation
		## Copy Calculation_Parameters from low-level-block ex)copy.deepcopy(B16_nmos_power_v2._NMOS_POWER._ParametersForDesignCalculation)
		_Caculation_Parameters = copy.deepcopy(A15_PolyRes_KJH2._PolyRes_KJH._ParametersForDesignCalculation)
		## Define Calculation_Parameters ex) _Caculation_Parameters['_NMOSPOWER_PbodyContact_1_Length']  = _NMOSPOWER_PbodyContact_1_Length
		_Caculation_Parameters['_ResWidth'] = _ResWidth
		_Caculation_Parameters['_ResLength'] = _ResLength
		_Caculation_Parameters['_CONUMX'] = _CONUMX
		_Caculation_Parameters['_CONUMY'] = _CONUMY

		## Generate Sref: ex)self._DesignParameter['_NMOS_POWER'] = self._SrefElementDeclaration(_DesignObj=B16_nmos_power_v2._NMOS_POWER( _DesignParameter=None, _Name='{}:NMOS_POWER'.format(_Name)))[0]
		self._DesignParameter['SRF_PolyRes_Dummy_Left'] = self._SrefElementDeclaration(_DesignObj=A15_PolyRes_KJH2._PolyRes_KJH(_DesignParameter=None, _Name='{}:SRF_PolyRes_Dummy_Left'.format(_Name)))[0]

		## Define Sref Reflection: ex)self._DesignParameter['_NMOS_POWER']['_Reflect'] = [0, 0, 0]
		self._DesignParameter['SRF_PolyRes_Dummy_Left']['_Reflect'] = [0, 0, 0]

		## Define Sref Angle: ex)'_NMOS_POWER'
		self._DesignParameter['SRF_PolyRes_Dummy_Left']['_Angle'] = 0

		## Calculate Sref Layer by using Calculation_Parameter: ex)'_NMOS_POWER'
		self._DesignParameter['SRF_PolyRes_Dummy_Left']['_DesignObj']._CalculateDesignParameter(**_Caculation_Parameters)

		## Define Sref _XYcoordinate: ex)'_NMOS_POWER'
		self._DesignParameter['SRF_PolyRes_Dummy_Left']['_XYCoordinates'] = [[0, 0]]

		## Get_Outter : tmp['_Most--']['coord'] ex) down, left, right, up
		## Most right
		tmp = self.get_outter_KJH4('SRF_PolyRes_Dummy_Left')
		output_element = tmp['_Mostright']['index']
		output_elementname_right_dummy = tmp['_Layercoord'][output_element[0]][1]

		## Most left
		tmp = self.get_outter_KJH4('SRF_PolyRes_Dummy_Left')
		output_element = tmp['_Mostleft']['index']
		output_elementname_left_dummy = tmp['_Layercoord'][output_element[0]][1]

		## Most up
		tmp = self.get_outter_KJH4('SRF_PolyRes_Dummy_Left')
		output_element = tmp['_Mostup']['index']
		output_elementname_up_dummy = tmp['_Layercoord'][output_element[0]][1]

		## Most down
		tmp = self.get_outter_KJH4('SRF_PolyRes_Dummy_Left')
		output_element = tmp['_Mostdown']['index']
		output_elementname_down_dummy = tmp['_Layercoord'][output_element[0]][1]

		## Get_Scoord_v4.
		## Calculate Sref XYcoord
		tmpXY = []
		## initialized Sref coordinate
		self._DesignParameter['SRF_PolyRes_Dummy_Left']['_XYCoordinates'] = [[0, 0]]
		for i in range(0, _Size[0]+2):
			if i == 0:
				## Calculate
				tmp = self.get_outter_KJH4('SRF_PolyRes_Dummy_Up')
				output_element = tmp['_Mostleft']['index']
				wow = tmp['_Layercoord'][output_element[0]][1]
				## Target_coord: _XY_type1
				tmp1 = self.get_param_KJH4(wow[0], wow[1])
				target_coord = tmp1[0][0][0]['_XY_left']
				## Approaching_coord: _XY_type2
				tmp2 = self.get_param_KJH4(output_elementname_right_dummy[0], output_elementname_right_dummy[1])
				approaching_coord = tmp2[0][0][0]['_XY_right']
				## Sref coord
				tmp3 = self.get_param_KJH4('SRF_PolyRes_Dummy_Left')
				Scoord = tmp3[0][0]['_XY_origin']
				## Cal
				New_Scoord = self.get_Scoord_KJH4(target_coord, approaching_coord, Scoord)
				New_Scoord[0] = New_Scoord[0] - unit_left_right_distance
				tmpXY.append(New_Scoord)
				## Define Coordinates
				self._DesignParameter['SRF_PolyRes_Dummy_Left']['_XYCoordinates'] = tmpXY
			else:
				## Calculate
				## Target_coord: _XY_type1
				tmp1 = self.get_param_KJH4(output_elementname_down_dummy[0], output_elementname_down_dummy[1])
				target_coord = tmp1[i-1][0][0]['_XY_down']
				## Approaching_coord: _XY_type2
				tmp2 = self.get_param_KJH4(output_elementname_up_dummy[0], output_elementname_up_dummy[1])
				approaching_coord = tmp2[0][0][0]['_XY_up']
				## Sref coord
				tmp3 = self.get_param_KJH4('SRF_PolyRes_Dummy_Left')
				Scoord = tmp3[0][0]['_XY_origin']
				## Cal
				New_Scoord = self.get_Scoord_KJH4(target_coord, approaching_coord, Scoord)
				New_Scoord[1] = New_Scoord[1] - unit_up_down_distance
				tmpXY.append(New_Scoord)
				## Define Coordinates
				self._DesignParameter['SRF_PolyRes_Dummy_Left']['_XYCoordinates'] = tmpXY

		## ########## ########## ########## ########## ########## ########## ########## ########## ########## ########## ########## SRF PolyRes Dummy: Right
		## SREF Generation
		## Copy Calculation_Parameters from low-level-block ex)copy.deepcopy(B16_nmos_power_v2._NMOS_POWER._ParametersForDesignCalculation)
		_Caculation_Parameters = copy.deepcopy(A15_PolyRes_KJH2._PolyRes_KJH._ParametersForDesignCalculation)
		## Define Calculation_Parameters ex) _Caculation_Parameters['_NMOSPOWER_PbodyContact_1_Length']  = _NMOSPOWER_PbodyContact_1_Length
		_Caculation_Parameters['_ResWidth'] = _ResWidth
		_Caculation_Parameters['_ResLength'] = _ResLength
		_Caculation_Parameters['_CONUMX'] = _CONUMX
		_Caculation_Parameters['_CONUMY'] = _CONUMY

		## Generate Sref: ex)self._DesignParameter['_NMOS_POWER'] = self._SrefElementDeclaration(_DesignObj=B16_nmos_power_v2._NMOS_POWER( _DesignParameter=None, _Name='{}:NMOS_POWER'.format(_Name)))[0]
		self._DesignParameter['SRF_PolyRes_Dummy_Right'] = self._SrefElementDeclaration(_DesignObj=A15_PolyRes_KJH2._PolyRes_KJH(_DesignParameter=None, _Name='{}:SRF_PolyRes_Dummy_Right'.format(_Name)))[0]

		## Define Sref Reflection: ex)self._DesignParameter['_NMOS_POWER']['_Reflect'] = [0, 0, 0]
		self._DesignParameter['SRF_PolyRes_Dummy_Right']['_Reflect'] = [0, 0, 0]

		## Define Sref Angle: ex)'_NMOS_POWER'
		self._DesignParameter['SRF_PolyRes_Dummy_Right']['_Angle'] = 0

		## Calculate Sref Layer by using Calculation_Parameter: ex)'_NMOS_POWER'
		self._DesignParameter['SRF_PolyRes_Dummy_Right']['_DesignObj']._CalculateDesignParameter(**_Caculation_Parameters)

		## Define Sref _XYcoordinate: ex)'_NMOS_POWER'
		self._DesignParameter['SRF_PolyRes_Dummy_Right']['_XYCoordinates'] = [[0, 0]]

		## Get_Outter : tmp['_Most--']['coord'] ex) down, left, right, up
		## Most right
		tmp = self.get_outter_KJH4('SRF_PolyRes_Dummy_Right')
		output_element = tmp['_Mostright']['index']
		output_elementname_right_dummy = tmp['_Layercoord'][output_element[0]][1]

		## Most left
		tmp = self.get_outter_KJH4('SRF_PolyRes_Dummy_Right')
		output_element = tmp['_Mostleft']['index']
		output_elementname_left_dummy = tmp['_Layercoord'][output_element[0]][1]

		## Most up
		tmp = self.get_outter_KJH4('SRF_PolyRes_Dummy_Right')
		output_element = tmp['_Mostup']['index']
		output_elementname_up_dummy = tmp['_Layercoord'][output_element[0]][1]

		## Most down
		tmp = self.get_outter_KJH4('SRF_PolyRes_Dummy_Right')
		output_element = tmp['_Mostdown']['index']
		output_elementname_down_dummy = tmp['_Layercoord'][output_element[0]][1]

		## Get_Scoord_v4.
		## Calculate Sref XYcoord
		tmpXY = []
		## initialized Sref coordinate
		self._DesignParameter['SRF_PolyRes_Dummy_Right']['_XYCoordinates'] = [[0, 0]]
		for i in range(0, _Size[0] + 2):
			if i == 0:
				## Calculate
				tmp = self.get_outter_KJH4('SRF_PolyRes_Dummy_Up')
				output_element = tmp['_Mostright']['index']
				wow = tmp['_Layercoord'][output_element[0]][1]
				## Target_coord: _XY_type1
				tmp1 = self.get_param_KJH4(wow[0], wow[1])
				target_coord = tmp1[_Size[1]-1][0][0]['_XY_right']
				## Approaching_coord: _XY_type2
				tmp2 = self.get_param_KJH4(output_elementname_right_dummy[0], output_elementname_right_dummy[1])
				approaching_coord = tmp2[0][0][0]['_XY_left']
				## Sref coord
				tmp3 = self.get_param_KJH4('SRF_PolyRes_Dummy_Right')
				Scoord = tmp3[0][0]['_XY_origin']
				## Cal
				New_Scoord = self.get_Scoord_KJH4(target_coord, approaching_coord, Scoord)
				New_Scoord[0] = New_Scoord[0] + unit_left_right_distance
				tmpXY.append(New_Scoord)
				## Define Coordinates
				self._DesignParameter['SRF_PolyRes_Dummy_Right']['_XYCoordinates'] = tmpXY
			else:
				## Calculate
				## Target_coord: _XY_type1
				tmp1 = self.get_param_KJH4(output_elementname_down_dummy[0], output_elementname_down_dummy[1])
				target_coord = tmp1[i - 1][0][0]['_XY_down']
				## Approaching_coord: _XY_type2
				tmp2 = self.get_param_KJH4(output_elementname_up_dummy[0], output_elementname_up_dummy[1])
				approaching_coord = tmp2[0][0][0]['_XY_up']
				## Sref coord
				tmp3 = self.get_param_KJH4('SRF_PolyRes_Dummy_Right')
				Scoord = tmp3[0][0]['_XY_origin']
				## Cal
				New_Scoord = self.get_Scoord_KJH4(target_coord, approaching_coord, Scoord)
				New_Scoord[1] = New_Scoord[1] - unit_up_down_distance
				tmpXY.append(New_Scoord)
				## Define Coordinates
				self._DesignParameter['SRF_PolyRes_Dummy_Right']['_XYCoordinates'] = tmpXY



		## ########## ########## ########## ########## ########## ########## ########## ########## ########## ########## ########## ########## BND_PPLayer
		# Define Boundary_element
		self._DesignParameter['BND_PP_cover2'] = self._BoundaryElementDeclaration(
			_Layer=DesignParameters._LayerMapping['PIMP'][0],
			_Datatype=DesignParameters._LayerMapping['PIMP'][1],
			_XWidth=None,
			_YWidth=None,
			_XYCoordinates=[],
		)

		# Define Boundary_element _YWidth
		tmp = self.get_param_KJH4('SRF_PolyRes_Dummy_Left', 'BND_PPLayer')
		self._DesignParameter['BND_PP_cover2']['_YWidth'] = tmp[0][0][0]['_XY_up'][1] - tmp[-1][0][0]['_XY_down'][1]

		# Define Boundary_element _XWidth
		tmp1 = self.get_param_KJH4('SRF_PolyRes_Dummy_Left',  'BND_PPLayer')
		tmp2 = self.get_param_KJH4('SRF_PolyRes_Dummy_Right', 'BND_PPLayer')
		self._DesignParameter['BND_PP_cover2']['_XWidth'] = abs(tmp1[0][0][0]['_XY_left'][0] - tmp2[0][0][0]['_XY_right'][0])

		# Define coord
		self._DesignParameter['BND_PP_cover2']['_XYCoordinates'] = [[0, 0]]

		# Calculate Sref XYcoord
		# Target_coord
		tmp1 = self.get_param_KJH4('SRF_PolyRes_Dummy_Left', 'BND_PPLayer')
		target_coord = tmp1[0][0][0]['_XY_up_left']
		# Approaching_coord
		tmp2 = self.get_param_KJH4('BND_PP_cover2')
		approaching_coord = tmp2[0][0]['_XY_up_left']
		# Sref coord
		tmp3 = self.get_param_KJH4('BND_PP_cover2')
		Scoord = tmp3[0][0]['_XY_origin']
		# Cal
		New_Scoord = self.get_Scoord_KJH4(target_coord, approaching_coord, Scoord)

		# Define coord
		self._DesignParameter['BND_PP_cover2']['_XYCoordinates'] = [New_Scoord]

		## ########## ########## ########## ########## ########## ########## ########## ########## ########## ########## ########## ########## BND_PRES cover
		# Define Boundary_element
		self._DesignParameter['BND_PRES_cover2'] = self._BoundaryElementDeclaration(
			_Layer=DesignParameters._LayerMapping['PRES'][0],
			_Datatype=DesignParameters._LayerMapping['PRES'][1],
			_XWidth=None,
			_YWidth=None,
			_XYCoordinates=[],
		)

		# Define Boundary_element _YWidth
		tmp = self.get_param_KJH4('SRF_PolyRes_Dummy_Left', 'BND_PRESLayer')
		self._DesignParameter['BND_PRES_cover2']['_YWidth'] = tmp[0][0][0]['_XY_up'][1] - tmp[-1][0][0]['_XY_down'][1]

		# Define Boundary_element _XWidth
		tmp1 = self.get_param_KJH4('SRF_PolyRes_Dummy_Left',  'BND_PRESLayer')
		tmp2 = self.get_param_KJH4('SRF_PolyRes_Dummy_Right', 'BND_PRESLayer')
		self._DesignParameter['BND_PRES_cover2']['_XWidth'] = abs(tmp1[0][0][0]['_XY_left'][0] - tmp2[0][0][0]['_XY_right'][0])

		# Define coord
		self._DesignParameter['BND_PRES_cover2']['_XYCoordinates'] = [[0, 0]]

		# Calculate Sref XYcoord
		# Target_coord
		tmp1 = self.get_param_KJH4('SRF_PolyRes_Dummy_Left', 'BND_PRESLayer')
		target_coord = tmp1[0][0][0]['_XY_up_left']
		# Approaching_coord
		tmp2 = self.get_param_KJH4('BND_PRES_cover2')
		approaching_coord = tmp2[0][0]['_XY_up_left']
		# Sref coord
		tmp3 = self.get_param_KJH4('BND_PRES_cover2')
		Scoord = tmp3[0][0]['_XY_origin']
		# Cal
		New_Scoord = self.get_Scoord_KJH4(target_coord, approaching_coord, Scoord)

		# Define coord
		self._DesignParameter['BND_PRES_cover2']['_XYCoordinates'] = [New_Scoord]
		#
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

	libname = 'Proj_ZZ01_P00_00_RArray2'
	cellname = 'P00_00_RArray_99'
	_fileName = cellname + '.gds'

	''' Input Parameters for Layout Object '''
	InputParams = dict(

_ResWidth	=	1300,
_ResLength	=	1500,
_CONUMX		=	2,
_CONUMY		=	2,

_Size		= [3,15],

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
	LayoutObj = _RArray(_DesignParameter=None, _Name=cellname)
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
	# Checker.cell_deletion()
	Checker.Upload2FTP()
	Checker.StreamIn(tech=DesignParameters._Technology)
	# Checker_KJH0.DRCchecker()

	print('#############################      Finished      ################################')
	print('{} Hours   {} minutes   {} seconds'.format(h, m, s))
	# end of 'main():' ---------------------------------------------------------------------------------------------




