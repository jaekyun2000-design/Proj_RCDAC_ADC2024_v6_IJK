
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


## Define Class
class _pathtest(StickDiagram_KJH1._StickDiagram_KJH):

	## Input Parameters for Design Calculation: Used when import Sref
	_ParametersForDesignCalculation = dict(

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

		## Path_element Generation
		## Define Path_element ex)LayerName: METAL1 / DIFF (_ODLayer) / POLY / PIMP (_PPLayer) / NWELL / SLVT LVT RVT HVT / OP(OPpress) / CONT (CA) / PCCRIT
		self._DesignParameter['PTH_A'] = self._PathElementDeclaration(
		    _Layer=DesignParameters._LayerMapping['METAL1'][0],
		    _Datatype=DesignParameters._LayerMapping['METAL1'][1],
		    _XYCoordinates=[],
		    _Width=None,
		)


		## Path Width: ***** must be even number ***
		Path_width = 150
		self._DesignParameter['PTH_A']['_Width'] = Path_width

		tmpXY = []
		## P1--P2 coordiantes
		## P1 calculation
		P1 = [0,0]
		## P2 calculation
		P2 = [0,-100]
		## P1_P2
		P1_P2 = [P1, P2]
		tmpXY.append(P1_P2)

		## P3--P4 coordiantes
		## P3 calculation
		P3 = [0,-100]
		## P4 calculation
		P4 = [500,-100]
		## P1_P2
		P3_P4 = [P3, P4]
		tmpXY.append(P3_P4)

		## Define Coordinates
		tmpXY = self.get_PTHcoord_KJH(tmpXY, Path_width)
		self._DesignParameter['PTH_A']['_XYCoordinates'] = tmpXY

		tmp= self.get_param_KJH4('PTH_A')


		## Path_element Generation
		## Path Name:
		Path_name = 'A'

		## Path Width: ***** must be even number ***
		Path_width = 150

		## tmp
		tmpXY = []
		tmpMetal = []
		tmpViaTF = []
		tmpViaDir = []
		tmpViaWid = []
		
		## coord1
			## P1 calculation
		P1 = [0,5000]
			## P2 calculation
		P2 = [0,-1000]
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
		P1 = [0,-1000]
			## P2 calculation
		P2 = [5000,-1000]
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
		
		## coord3
			## P1 calculation
		P1 = [5000, -1000]
			## P2 calculation
		P2 = [5000, -8000]
			## Metal Layer
		Metal = 4
			## Via True=1/False=0
		ViaTF = 1
				## Via Vtc=1/Hrz=0/Ovl=2
		ViaDir = 1
				## Via width: None/[1,3]
		ViaWid = None
		
		tmpXY.append([P1, P2])
		tmpMetal.append(Metal)
		tmpViaTF.append(ViaTF)
		tmpViaDir.append(ViaDir)
		tmpViaWid.append(ViaWid)
		
		tmpXY = self.get_PTH_KJH(Path_name, Path_width, tmpXY, tmpMetal, tmpViaTF, tmpViaDir, tmpViaWid)


		# ## Define Coordinates
		# tmpXY = self.get_PTHcoord_KJH(tmpXY, Path_width)
		# self._DesignParameter['PTH_A']['_XYCoordinates'] = tmpXY

		# tmp= self.get_param_KJH4('PTH_A')

		print('##############################')
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
	cellname = 'Y00_A02_test'
	_fileName = cellname + '.gds'

	''' Input Parameters for Layout Object '''
	InputParams = dict(

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
	LayoutObj = _pathtest(_DesignParameter=None, _Name=cellname)
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
