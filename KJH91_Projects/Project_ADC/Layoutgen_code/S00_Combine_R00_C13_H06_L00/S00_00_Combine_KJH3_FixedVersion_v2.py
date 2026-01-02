## Import Basic Modules
## Engine
# from KJH91_Projects.Project_ADC.Layoutgen_code.E00_Slicer import StickDiagram
from KJH91_Projects.Project_ADC.Library_and_Engine import StickDiagram_KJH1
from KJH91_Projects.Project_ADC.Layoutgen_code.E00_Slicer import DesignParameters
from KJH91_Projects.Project_ADC.Layoutgen_code.E00_Slicer import DRC

## Library
import copy
import time
import numpy as np
import dill as pickle
import math

## KJH91 Basic Building Blocks
from KJH91_Projects.Project_ADC.Layoutgen_code.E00_Slicer import Slicer
from KJH91_Projects.Project_ADC.Layoutgen_code.A_Basic_Building_Block import A14_Mosfet_KJH2
from KJH91_Projects.Project_ADC.Layoutgen_code.A_Basic_Building_Block import A02_ViaStack_KJH3

from KJH91_Projects.Project_ADC.Layoutgen_code.L00_SARLogicWtComparator_RCHybrid_Fixed import L00_SARLogicWtComparator_KJH
from KJH91_Projects.Project_ADC.Layoutgen_code.C13_C07C11C12TieCellsRouted_Fixed import C13_01_CtopCbotRouted_YJ_v01_00
from KJH91_Projects.Project_ADC.Layoutgen_code.D00_SARLogic_Inverter_Fixed import D00_00_Inverter_KJH
from KJH91_Projects.Project_ADC.Layoutgen_code.R00_RDACWtDecoder_Fixed import R00_00_Combine_KJH4
from KJH91_Projects.Project_ADC.Layoutgen_code.H06_CDACWtDriver_Fixed import H06_00_CDACWtDriver


## Define Class
class _R00C13H06L00(StickDiagram_KJH1._StickDiagram_KJH):
	## Input Parameters for Design Calculation: Used when import Sref
	_ParametersForDesignCalculation = dict(
_NumofCbit=4,
_NumofRbit=0,

## SAR Logic
	## Clock Tree (Driving SAR Logic)
		## Clock Tree Updward (CLK Source Tree, CLK Samp Tree)
			## CLK Buffer Unit
				## Common
				_LOGIC_CLKBufTreeTop_UnitBuf_XVT='SLVT',
				## Nmos
				_LOGIC_CLKBufTreeTop_UnitBuf_NMOS_NumberofGate=1,  # Number
				_LOGIC_CLKBufTreeTop_UnitBuf_NMOS_ChannelWidth=400,  # Number
				_LOGIC_CLKBufTreeTop_UnitBuf_NMOS_ChannelLength=30,  # Number
				## Pmos
				_LOGIC_CLKBufTreeTop_UnitBuf_PMOS_NumberofGate=1,  # Number
				_LOGIC_CLKBufTreeTop_UnitBuf_PMOS_ChannelWidth=800,  # Number
				_LOGIC_CLKBufTreeTop_UnitBuf_PMOS_ChannelLength=30,  # Number
				# Height
				_LOGIC_CLKBufTreeTop_UnitBuf_PMOSXvt2NMOSXvt=446,  # number
			## Clock Buffer Tree structure
			_LOGIC_CLKBufTreeTop_BufTree1and2_NumOfStage=4,  # len[Buf0, Buf1, ... ] 스테이지 수 (아래 버퍼 사이즈 리스트의 길이와 같아야 함.)
			_LOGIC_CLKBufTreeTop_BufTree1_SizeofEachStage=[1, 2, 4, 8],  # CLKSampBuf: [Buf0, Buf1, Buf2 ...]
			_LOGIC_CLKBufTreeTop_BufTree2_SizeofEachStage=[1, 2, 4, 8],  # CLKSrcBuf: [Buf0, Buf1, Buf2 ...]
			_LOGIC_CLKBufTreeTop_XOffSet=0,
		## Clock Tree Dnward (CLK Source Tree, CLK Samp Tree)
			## CLK Buffer Unit
				## Common
				_LOGIC_CLKBufTreeBot_UnitBuf_XVT='SLVT',
				## Nmos
				_LOGIC_CLKBufTreeBot_UnitBuf_NMOS_NumberofGate=1,  # Number
				_LOGIC_CLKBufTreeBot_UnitBuf_NMOS_ChannelWidth=400,  # Number
				_LOGIC_CLKBufTreeBot_UnitBuf_NMOS_ChannelLength=30,  # Number
				## Pmos
				_LOGIC_CLKBufTreeBot_UnitBuf_PMOS_NumberofGate=1,  # Number
				_LOGIC_CLKBufTreeBot_UnitBuf_PMOS_ChannelWidth=800,  # Number
				_LOGIC_CLKBufTreeBot_UnitBuf_PMOS_ChannelLength=30,  # Number
				# Height
				_LOGIC_CLKBufTreeBot_UnitBuf_PMOSXvt2NMOSXvt=446,  # number
			## Clock Buffer Tree structure
			_LOGIC_CLKBufTreeBot_BufTree1and2_NumOfStage=4,  # len[Buf0, Buf1, ... ] 스테이지 수 (아래 버퍼 사이즈 리스트의 길이와 같아야 함.)
			_LOGIC_CLKBufTreeBot_BufTree1_SizeofEachStage=[1, 2, 4, 8],  # CompOutBuf: [Buf0, Buf1, Buf2 ...]
			_LOGIC_CLKBufTreeBot_BufTree2_SizeofEachStage=[1, 2, 4, 8],  # CLKDoutBuf: [Buf0, Buf1, Buf2 ...]
			_LOGIC_CLKBufTreeBot_XOffSet=0,

	## Clock Spine (Physical demension)
		## CLK Source: upward, 1st floor
		_LOGIC_YWidthOfCLKSrc=100,
		## CLK Samp: upward, 2nd floor
		_LOGIC_SpaceBtwCLKSrcAndCLKSamp=100,
		_LOGIC_YWidthOfCLKSamp=100,
		## Comparator Output: downward, Basement1
		_LOGIC_YWidthOfCompOut=100,
		## CLK Dout: downward, basement2
		_LOGIC_SpaceBtwCompOutAndCLKDout=100,
		_LOGIC_YWidthOfCLKDout=100,

	## SetResetDFF
		## DFF Common
		_LOGIC_Test_distance=320,
		_LOGIC_DFF_PMOSXvt2NMOSXvt    = 1150, # number

		## Master Xgate1
			## Xgate common
			_LOGIC_Mst_Xgate1_XVT='SLVT',
			## Xgate NMOS
			_LOGIC_Mst_Xgate1_NMOS_NumberofGate=1,
			_LOGIC_Mst_Xgate1_NMOS_ChannelWidth=300,
			_LOGIC_Mst_Xgate1_NMOS_ChannelLength=30,
			## Xgate PMOS
			_LOGIC_Mst_Xgate1_PMOS_NumberofGate=3,
			_LOGIC_Mst_Xgate1_PMOS_ChannelWidth=500,
			_LOGIC_Mst_Xgate1_PMOS_ChannelLength=30,

		## Master Xgate2
			## Xgate common
			_LOGIC_Mst_Xgate2_XVT='SLVT',
			## Xgate NMOS
			_LOGIC_Mst_Xgate2_NMOS_NumberofGate           = 2,
			_LOGIC_Mst_Xgate2_NMOS_ChannelWidth           = 800,
			_LOGIC_Mst_Xgate2_NMOS_ChannelLength          = 30,
			## Xgate PMOS
			_LOGIC_Mst_Xgate2_PMOS_NumberofGate           = 3,
			_LOGIC_Mst_Xgate2_PMOS_ChannelWidth           = 200,
			_LOGIC_Mst_Xgate2_PMOS_ChannelLength          = 30,

		## Master Nor1
			## Nor1 common
			_LOGIC_Mst_Nor1_XVT='SLVT',
			## NMOS
				## NMOSA
				_LOGIC_Mst_Nor1_NMOSA_NumberofGate           = 2,
				_LOGIC_Mst_Nor1_NMOSA_ChannelWidth           = 800,
				_LOGIC_Mst_Nor1_NMOSA_ChannelLength          = 30,
				## NMOSB
				_LOGIC_Mst_Nor1_NMOSB_NumberofGate           = 3,
				_LOGIC_Mst_Nor1_NMOSB_ChannelWidth           = 200,
				_LOGIC_Mst_Nor1_NMOSB_ChannelLength          = 30,
			## PMOS
				## PMOSA
				_LOGIC_Mst_Nor1_PMOSA_NumberofGate            = 2,
				_LOGIC_Mst_Nor1_PMOSA_ChannelWidth            = 800,
				_LOGIC_Mst_Nor1_PMOSA_ChannelLength           = 30,
				## PMOSB
				_LOGIC_Mst_Nor1_PMOSB_NumberofGate            = 3,
				_LOGIC_Mst_Nor1_PMOSB_ChannelWidth            = 200,
				_LOGIC_Mst_Nor1_PMOSB_ChannelLength           = 30,

		## Master Nor2
			## Nor2 common
			_LOGIC_Mst_Nor2_XVT='SLVT',
			## NMOS
				## NMOSA
				_LOGIC_Mst_Nor2_NMOSA_NumberofGate           = 2,
				_LOGIC_Mst_Nor2_NMOSA_ChannelWidth           = 800,
				_LOGIC_Mst_Nor2_NMOSA_ChannelLength          = 30,
				## NMOSB
				_LOGIC_Mst_Nor2_NMOSB_NumberofGate           = 3,
				_LOGIC_Mst_Nor2_NMOSB_ChannelWidth           = 200,
				_LOGIC_Mst_Nor2_NMOSB_ChannelLength          = 30,
			## PMOS
				## PMOSA
				_LOGIC_Mst_Nor2_PMOSA_NumberofGate            = 2,
				_LOGIC_Mst_Nor2_PMOSA_ChannelWidth            = 800,
				_LOGIC_Mst_Nor2_PMOSA_ChannelLength           = 30,
				## PMOSB
				_LOGIC_Mst_Nor2_PMOSB_NumberofGate            = 3,
				_LOGIC_Mst_Nor2_PMOSB_ChannelWidth            = 200,
				_LOGIC_Mst_Nor2_PMOSB_ChannelLength           = 30,

		## Master Inv1 : Set pre-driver
			## Inv1 common
			_LOGIC_Mst_Inv1_XVT='SLVT',
			## Inv1 NMOS
			_LOGIC_Mst_Inv1_NMOS_NumberofGate           = 1,
			_LOGIC_Mst_Inv1_NMOS_ChannelWidth           = 300,
			_LOGIC_Mst_Inv1_NMOS_ChannelLength          = 30,
			## Inv1 PMOS
			_LOGIC_Mst_Inv1_PMOS_NumberofGate           = 3,
			_LOGIC_Mst_Inv1_PMOS_ChannelWidth           = 500,
			_LOGIC_Mst_Inv1_PMOS_ChannelLength          = 30,

		## Master Inv2 : Set driver
			## Inv2 common
			_LOGIC_Mst_Inv2_XVT='SLVT',
			## Inv2 NMOS
			_LOGIC_Mst_Inv2_NMOS_NumberofGate           = 1,
			_LOGIC_Mst_Inv2_NMOS_ChannelWidth           = 300,
			_LOGIC_Mst_Inv2_NMOS_ChannelLength          = 30,
			## Inv2 PMOS
			_LOGIC_Mst_Inv2_PMOS_NumberofGate           = 3,
			_LOGIC_Mst_Inv2_PMOS_ChannelWidth           = 500,
			_LOGIC_Mst_Inv2_PMOS_ChannelLength          = 30,

		## Master Inv3 : Clock driver
			## Inv3 common
			_LOGIC_Mst_Inv3_XVT='SLVT',
			## Inv3 NMOS
			_LOGIC_Mst_Inv3_NMOS_NumberofGate           = 1,
			_LOGIC_Mst_Inv3_NMOS_ChannelWidth           = 300,
			_LOGIC_Mst_Inv3_NMOS_ChannelLength          = 30,
			## Inv3 PMOS
			_LOGIC_Mst_Inv3_PMOS_NumberofGate           = 3,
			_LOGIC_Mst_Inv3_PMOS_ChannelWidth           = 500,
			_LOGIC_Mst_Inv3_PMOS_ChannelLength          = 30,

		## Slave Xgate1
			## Xgate common
			_LOGIC_Slv_Xgate1_XVT='SLVT',
			## Xgate NMOS
			_LOGIC_Slv_Xgate1_NMOS_NumberofGate           = 1,
			_LOGIC_Slv_Xgate1_NMOS_ChannelWidth           = 300,
			_LOGIC_Slv_Xgate1_NMOS_ChannelLength          = 30,
			## Xgate PMOS
			_LOGIC_Slv_Xgate1_PMOS_NumberofGate           = 3,
			_LOGIC_Slv_Xgate1_PMOS_ChannelWidth           = 500,
			_LOGIC_Slv_Xgate1_PMOS_ChannelLength          = 30,

		## Slave Xgate2
			## Xgate common
			_LOGIC_Slv_Xgate2_XVT='SLVT',
			## Xgate NMOS
			_LOGIC_Slv_Xgate2_NMOS_NumberofGate           = 2,
			_LOGIC_Slv_Xgate2_NMOS_ChannelWidth           = 800,
			_LOGIC_Slv_Xgate2_NMOS_ChannelLength          = 30,
			## Xgate PMOS
			_LOGIC_Slv_Xgate2_PMOS_NumberofGate           = 3,
			_LOGIC_Slv_Xgate2_PMOS_ChannelWidth           = 200,
			_LOGIC_Slv_Xgate2_PMOS_ChannelLength          = 30,

		## Slave Nor1
			## Nor1 common
			_LOGIC_Slv_Nor1_XVT='SLVT',
			## NMOS
				## NMOSA
				_LOGIC_Slv_Nor1_NMOSA_NumberofGate           = 2,
				_LOGIC_Slv_Nor1_NMOSA_ChannelWidth           = 800,
				_LOGIC_Slv_Nor1_NMOSA_ChannelLength          = 30,
				## NMOSB
				_LOGIC_Slv_Nor1_NMOSB_NumberofGate           = 3,
				_LOGIC_Slv_Nor1_NMOSB_ChannelWidth           = 200,
				_LOGIC_Slv_Nor1_NMOSB_ChannelLength          = 30,
			## PMOS
				## PMOSA
				_LOGIC_Slv_Nor1_PMOSA_NumberofGate            = 2,
				_LOGIC_Slv_Nor1_PMOSA_ChannelWidth            = 800,
				_LOGIC_Slv_Nor1_PMOSA_ChannelLength           = 30,
				## PMOSB
				_LOGIC_Slv_Nor1_PMOSB_NumberofGate            = 3,
				_LOGIC_Slv_Nor1_PMOSB_ChannelWidth            = 200,
				_LOGIC_Slv_Nor1_PMOSB_ChannelLength           = 30,

		## Slave Nor2
			## Nor2 common
			_LOGIC_Slv_Nor2_XVT='SLVT',
			## NMOS
				## NMOSA
				_LOGIC_Slv_Nor2_NMOSA_NumberofGate           = 2,
				_LOGIC_Slv_Nor2_NMOSA_ChannelWidth           = 800,
				_LOGIC_Slv_Nor2_NMOSA_ChannelLength          = 30,
				## NMOSB
				_LOGIC_Slv_Nor2_NMOSB_NumberofGate           = 3,
				_LOGIC_Slv_Nor2_NMOSB_ChannelWidth           = 200,
				_LOGIC_Slv_Nor2_NMOSB_ChannelLength          = 30,
			## PMOS
				## PMOSA
				_LOGIC_Slv_Nor2_PMOSA_NumberofGate            = 2,
				_LOGIC_Slv_Nor2_PMOSA_ChannelWidth            = 800,
				_LOGIC_Slv_Nor2_PMOSA_ChannelLength           = 30,
				## PMOSB
				_LOGIC_Slv_Nor2_PMOSB_NumberofGate            = 3,
				_LOGIC_Slv_Nor2_PMOSB_ChannelWidth            = 200,
				_LOGIC_Slv_Nor2_PMOSB_ChannelLength           = 30,

		## Slave Inv1 : ReSet pre-driver
			## Inv1 common
			_LOGIC_Slv_Inv1_XVT='SLVT',
			## Inv1 NMOS
			_LOGIC_Slv_Inv1_NMOS_NumberofGate           = 1,
			_LOGIC_Slv_Inv1_NMOS_ChannelWidth           = 300,
			_LOGIC_Slv_Inv1_NMOS_ChannelLength          = 30,
			## Inv1 PMOS
			_LOGIC_Slv_Inv1_PMOS_NumberofGate           = 3,
			_LOGIC_Slv_Inv1_PMOS_ChannelWidth           = 500,
			_LOGIC_Slv_Inv1_PMOS_ChannelLength          = 30,

		## Slave Inv2 : ReSet driver
			## Inv2 common
			_LOGIC_Slv_Inv2_XVT='SLVT',
			## Inv2 NMOS
			_LOGIC_Slv_Inv2_NMOS_NumberofGate           = 1,
			_LOGIC_Slv_Inv2_NMOS_ChannelWidth           = 300,
			_LOGIC_Slv_Inv2_NMOS_ChannelLength          = 30,
			## Inv2 PMOS
			_LOGIC_Slv_Inv2_PMOS_NumberofGate           = 3,
			_LOGIC_Slv_Inv2_PMOS_ChannelWidth           = 500,
			_LOGIC_Slv_Inv2_PMOS_ChannelLength          = 30,

		## Slave Inv3 : Qb driver
			## Inv3 common
			_LOGIC_Slv_Inv3_XVT='SLVT',
			## Inv3 NMOS
			_LOGIC_Slv_Inv3_NMOS_NumberofGate           = 1,
			_LOGIC_Slv_Inv3_NMOS_ChannelWidth           = 300,
			_LOGIC_Slv_Inv3_NMOS_ChannelLength          = 30,
			## Inv3 PMOS
			_LOGIC_Slv_Inv3_PMOS_NumberofGate           = 3,
			_LOGIC_Slv_Inv3_PMOS_ChannelWidth           = 500,
			_LOGIC_Slv_Inv3_PMOS_ChannelLength          = 30,
	## DAC PreDriver
		## Inverter Chain
			## InvChain Common
			_LOGIC_DACPreDrv_PMOSXvt2NMOSXvt=500,  # number
			## Inverter Chain
				## Inv1 common
			_LOGIC_DACPreDrv_NumberofGate=[[1, 2, 4, 8],[1, 2, 4, 8], [1, 2, 4, 8], [1],      ],  # Vector
			_RDAC_InputComple_Inv_NumofGate = [], # Vector, _LOGIC_DACPreDrv_NumberofGate + _RDAC_InputComple_Inv_NumofGate로 입력됨
			_LOGIC_DACPreDrv_ChannelLength=30,  # Scalar
			_LOGIC_DACPreDrv_XVT='SLVT',  # 'SLVT'
				## Inv1 NMOS
			_LOGIC_DACPreDrv_Inv_NMOS_ChannelWidth=400,  # Scalar
				## Inv1 PMOS
			_LOGIC_DACPreDrv_Inv_PMOS_ChannelWidth=800,  # Scalar
	## CLKOutSamp(!=ClkSamp)
		## Common
			# XVT
			_LOGIC_CLKoutSamp_XVT = 'SLVT',
			# Height
			# _CLKOutSamp_PMOSXvt2NMOSXvt=1800,  # number, = _DFF_PMOSXvt2NMOSXvt
		## Inverter
			# Nmos
			_LOGIC_CLKoutSamp_Inv_NMOS_NumberofGate=1,  # Number
			_LOGIC_CLKoutSamp_Inv_NMOS_ChannelWidth=100,  # Number
			_LOGIC_CLKoutSamp_Inv_NMOS_ChannelLength=30,  # Number
			# Pmos
			_LOGIC_CLKoutSamp_Inv_PMOS_NumberofGate=1,  # Number
			_LOGIC_CLKoutSamp_Inv_PMOS_ChannelWidth=100,  # Number
			_LOGIC_CLKoutSamp_Inv_PMOS_ChannelLength=30,  # Number
		## AND
			## AND Common
			## Nand
				# NmosA
				_LOGIC_CLKoutSamp_And_Nand_NMOSA_NumberofGate=1,  # Number
				_LOGIC_CLKoutSamp_And_Nand_NMOSA_ChannelWidth=100,  # Number
				_LOGIC_CLKoutSamp_And_Nand_NMOSA_ChannelLength=30,  # Number
				# NMOSB
				_LOGIC_CLKoutSamp_And_Nand_NMOSB_NumberofGate=2,  # Number
				_LOGIC_CLKoutSamp_And_Nand_NMOSB_ChannelWidth=750,  # Number
				_LOGIC_CLKoutSamp_And_Nand_NMOSB_ChannelLength=30,  # Number
				# PMOSA
				_LOGIC_CLKoutSamp_And_Nand_PMOSA_NumberofGate=1,  # Number
				_LOGIC_CLKoutSamp_And_Nand_PMOSA_ChannelWidth=300,  # Number
				_LOGIC_CLKoutSamp_And_Nand_PMOSA_ChannelLength=30,  # Number
				# PMOSB
				_LOGIC_CLKoutSamp_And_Nand_PMOSB_NumberofGate=3,  # Number
				_LOGIC_CLKoutSamp_And_Nand_PMOSB_ChannelWidth=750,  # Number
				_LOGIC_CLKoutSamp_And_Nand_PMOSB_ChannelLength=30,  # Number
			## Inverter
				# Nmos
				_LOGIC_CLKoutSamp_And_Inv_NMOS_NumberofGate=1,  # Number
				_LOGIC_CLKoutSamp_And_Inv_NMOS_ChannelWidth=100,  # Number
				_LOGIC_CLKoutSamp_And_Inv_NMOS_ChannelLength=30,  # Number
				# Pmos
				_LOGIC_CLKoutSamp_And_Inv_PMOS_NumberofGate=1,  # Number
				_LOGIC_CLKoutSamp_And_Inv_PMOS_ChannelWidth=200,  # Number
				_LOGIC_CLKoutSamp_And_Inv_PMOS_ChannelLength=30,  # Number


## Comparator
	## StrongARM Latch
		# Common
		_COMP_SALatch_ChannelLength=30,  # random.randrange(30, 60, 2),  # 30
		_COMP_SALatch_XVT='HVT',

		# PMOS
		_COMP_SALatch_CLKinputPMOSFinger1=1,  #PMOS Reset Sw1 # random.randint(1, 15),  # 6
		_COMP_SALatch_CLKinputPMOSFinger2=1,  #PMOS Reset Sw2 # random.randint(1, 15),  # 3
		_COMP_SALatch_PMOSFinger=1,  		  #PMOS Latch	  # random.randint(1, 15),  # 3
		_COMP_SALatch_PMOSChannelWidth=1000,  #All PMOS width # random.randrange(200, 1050, 2),  # 500

		# NMOS
		_COMP_SALatch_DATAinputNMOSFinger=3,  #NMOS Input Tr # random.randint(3, 15),  # 12
		_COMP_SALatch_NMOSFinger=2,  		  #NMOS at Latch # random.randint(1, 15),  # 2
		_COMP_SALatch_CLKinputNMOSFinger=1,  #NMOS Tail # random.randint(1, 15),  # 8
		_COMP_SALatch_NMOSChannelWidth=330,  #Nmos width # random.randrange(200, 1050, 2),  # 500
		_COMP_SALatch_CLKinputNMOSChannelWidth=200,  # random.randrange(200, 1050, 2),  # 800

	## StrongArmOutBuffer and SRLatch
		## Common
			# XVT
			_COMP_SAOutBufAndSRLatch_XVT='SLVT',
			# Body
			_COMP_SAOutBufAndSRLatch_NMOS_Pbody_XvtTop2Pbody=None,  # Number/None(Minimum)
			_COMP_SAOutBufAndSRLatch_PMOS_Nbody_Xvtdown2Nbody=None,  # Number/None(Minimum)
			# Height
			_COMP_SAOutBufAndSRLatch_PMOSXvt2NMOSXvt=1800,  # number
		## StronArm Output Buffer
			## Inverter1(pre)
					#Nmos
				_COMP_SAOutBuf_Buf_Inv1_NMOS_NumberofGate          = 1,        # Number
				_COMP_SAOutBuf_Buf_Inv1_NMOS_ChannelWidth          = 400,      # Number
				_COMP_SAOutBuf_Buf_Inv1_NMOS_ChannelLength         = 30,       # Number
					#Pmos
				_COMP_SAOutBuf_Buf_Inv1_PMOS_NumberofGate          = 1,        # Number
				_COMP_SAOutBuf_Buf_Inv1_PMOS_ChannelWidth          = 800,      # Number
				_COMP_SAOutBuf_Buf_Inv1_PMOS_ChannelLength         = 30,       # Number
			## Inverter2
					#Nmos
				_COMP_SAOutBuf_Buf_Inv2_NMOS_NumberofGate          = 2,        # Number
				_COMP_SAOutBuf_Buf_Inv2_NMOS_ChannelWidth          = 400,      # Number
				_COMP_SAOutBuf_Buf_Inv2_NMOS_ChannelLength         = 30,       # Number
					#Pmos
				_COMP_SAOutBuf_Buf_Inv2_PMOS_NumberofGate          = 2,        # Number
				_COMP_SAOutBuf_Buf_Inv2_PMOS_ChannelWidth          = 800,      # Number
				_COMP_SAOutBuf_Buf_Inv2_PMOS_ChannelLength         = 30,       # Number
		## SRLatch
			## Nand(Set,Rst same)
				# NmosA
				_COMP_SRLatch_Nand_NMOSA_NumberofGate=1,  # Number
				_COMP_SRLatch_Nand_NMOSA_ChannelWidth=100,  # Number
				_COMP_SRLatch_Nand_NMOSA_ChannelLength=30,  # Number
				# NMOSB
				_COMP_SRLatch_Nand_NMOSB_NumberofGate=2,  # Number
				_COMP_SRLatch_Nand_NMOSB_ChannelWidth=750,  # Number
				_COMP_SRLatch_Nand_NMOSB_ChannelLength=30,  # Number
				# PMOSA
				_COMP_SRLatch_Nand_PMOSA_NumberofGate=2,  # Number
				_COMP_SRLatch_Nand_PMOSA_ChannelWidth=100,  # Number
				_COMP_SRLatch_Nand_PMOSA_ChannelLength=30,  # Number
				# PMOSB
				_COMP_SRLatch_Nand_PMOSB_NumberofGate=1,  # Number
				_COMP_SRLatch_Nand_PMOSB_ChannelWidth=750,  # Number
				_COMP_SRLatch_Nand_PMOSB_ChannelLength=30,  # Number

	## Comp clock Gen Logic: Clk_Samp Inv, Clk_Source Inv, AND Gate, CompClockBuff
		## Common
			# XVT
			_COMP_CompClkLogic_XVT='SLVT',
			# Body
			_COMP_CompClkLogic_NMOS_Pbody_XvtTop2Pbody=None,  # Number/None(Minimum)
			_COMP_CompClkLogic_PMOS_Nbody_Xvtdown2Nbody=None,  # Number/None(Minimum)
			# Height
			_COMP_CompClkLogic_PMOSXvt2NMOSXvt=1800,  # number
		## StronArm Output Buffer
			## Inverter1(pre)
					#Nmos
				_COMP_CompClkLogic_Buf_Inv1_NMOS_NumberofGate          = 2,        # Number
				_COMP_CompClkLogic_Buf_Inv1_NMOS_ChannelWidth          = 400,      # Number
				_COMP_CompClkLogic_Buf_Inv1_NMOS_ChannelLength         = 30,       # Number
					#Pmos
				_COMP_CompClkLogic_Buf_Inv1_PMOS_NumberofGate          = 2,        # Number
				_COMP_CompClkLogic_Buf_Inv1_PMOS_ChannelWidth          = 800,      # Number
				_COMP_CompClkLogic_Buf_Inv1_PMOS_ChannelLength         = 30,       # Number
			## Inverter2
					#Nmos
				_COMP_CompClkLogic_Buf_Inv2_NMOS_NumberofGate          = 4,        # Number
				_COMP_CompClkLogic_Buf_Inv2_NMOS_ChannelWidth          = 400,      # Number
				_COMP_CompClkLogic_Buf_Inv2_NMOS_ChannelLength         = 30,       # Number
					#Pmos
				_COMP_CompClkLogic_Buf_Inv2_PMOS_NumberofGate          = 4,        # Number
				_COMP_CompClkLogic_Buf_Inv2_PMOS_ChannelWidth          = 800,      # Number
				_COMP_CompClkLogic_Buf_Inv2_PMOS_ChannelLength         = 30,       # Number
		## AND
			## Nand
				# NmosA
				_COMP_CompClkLogic_Nand_NMOSA_NumberofGate=1,  # Number
				_COMP_CompClkLogic_Nand_NMOSA_ChannelWidth=100,  # Number
				_COMP_CompClkLogic_Nand_NMOSA_ChannelLength=30,  # Number
				# NMOSB
				_COMP_CompClkLogic_Nand_NMOSB_NumberofGate=2,  # Number
				_COMP_CompClkLogic_Nand_NMOSB_ChannelWidth=750,  # Number
				_COMP_CompClkLogic_Nand_NMOSB_ChannelLength=30,  # Number
				# PMOSA
				_COMP_CompClkLogic_Nand_PMOSA_NumberofGate=1,  # Number
				_COMP_CompClkLogic_Nand_PMOSA_ChannelWidth=300,  # Number
				_COMP_CompClkLogic_Nand_PMOSA_ChannelLength=30,  # Number
				# PMOSB
				_COMP_CompClkLogic_Nand_PMOSB_NumberofGate=3,  # Number
				_COMP_CompClkLogic_Nand_PMOSB_ChannelWidth=750,  # Number
				_COMP_CompClkLogic_Nand_PMOSB_ChannelLength=30,  # Number
			## Inverter
				# Nmos
				_COMP_CompClkLogic_Inv_NMOS_NumberofGate=1,  # Number
				_COMP_CompClkLogic_Inv_NMOS_ChannelWidth=100,  # Number
				_COMP_CompClkLogic_Inv_NMOS_ChannelLength=30,  # Number
				# Pmos
				_COMP_CompClkLogic_Inv_PMOS_NumberofGate=1,  # Number
				_COMP_CompClkLogic_Inv_PMOS_ChannelWidth=200,  # Number
				_COMP_CompClkLogic_Inv_PMOS_ChannelLength=30,  # Number

		## Clk_Source Inv
				#Nmos
			_COMP_CompClkLogic_ClkSrc_NMOS_NumberofGate          = 1,        # Number
			_COMP_CompClkLogic_ClkSrc_NMOS_ChannelWidth          = 400,      # Number
			_COMP_CompClkLogic_ClkSrc_NMOS_ChannelLength         = 30,       # Number
				#Pmos
			_COMP_CompClkLogic_ClkSrc_PMOS_NumberofGate          = 1,        # Number
			_COMP_CompClkLogic_ClkSrc_PMOS_ChannelWidth          = 800,      # Number
			_COMP_CompClkLogic_ClkSrc_PMOS_ChannelLength         = 30,       # Number
		## Clk_Samp Inv
				#Nmos
			_COMP_CompClkLogic_ClkSmp_NMOS_NumberofGate          = 1,        # Number
			_COMP_CompClkLogic_ClkSmp_NMOS_ChannelWidth          = 400,      # Number
			_COMP_CompClkLogic_ClkSmp_NMOS_ChannelLength         = 30,       # Number
				#Pmos
			_COMP_CompClkLogic_ClkSmp_PMOS_NumberofGate          = 1,        # Number
			_COMP_CompClkLogic_ClkSmp_PMOS_ChannelWidth          = 800,      # Number
			_COMP_CompClkLogic_ClkSmp_PMOS_ChannelLength         = 30,       # Number




## CLOCK AND DATA BUF : Comparator Dout Buf for driving Logic, CLKSamp and CLKScr Buff for Driving Sampler and Comparator
	## Top placed
		## CLK Samp
			## InvChain Common
				## Height
		_BUF_CLKSamp_PMOSXvt2NMOSXvt = 500,  # number
			## Inverter Chain
				## Inv1 common
		_BUF_CLKSamp_XVT='SLVT',
		_BUF_CLKSamp_NumberofGate = [1,2,4,8],  # Vector,
		_BUF_CLKSamp_ChanneLength = 30,
				## NMOS
		_BUF_CLKSamp_NMOSChannelWidth = 784,
				## PMOS
		_BUF_CLKSamp_PMOSChannelWidth = 833,
		## CLK Scr
			## InvChain Common
				## Height
		_BUF_CLKScr_PMOSXvt2NMOSXvt = 500,  # number
			## Inverter Chain
				## Inv1 common
		_BUF_CLKScr_XVT='SLVT',
		_BUF_CLKScr_NumberofGate = [1,2,4,8],  # Vector,
		_BUF_CLKScr_ChanneLength = 30,
				## NMOS
		_BUF_CLKScr_NMOSChannelWidth = 784,
				## PMOS
		_BUF_CLKScr_PMOSChannelWidth = 833,
	## Bottom Placed
		## CompOut
			## InvChain Common
				## Height
		_BUF_CompOut_PMOSXvt2NMOSXvt = 500,  # number
			## Inverter Chain
				## Inv1 common
		_BUF_CompOut_XVT='SLVT',
		_BUF_CompOut_NumberofGate = [1,2,4,8],  # Vector,
		_BUF_CompOut_ChanneLength = 30,
				## NMOS
		_BUF_CompOut_NMOSChannelWidth = 784,
				## PMOS
		_BUF_CompOut_PMOSChannelWidth = 833,



## CDAC
	## CDAC Configuration
	_CDAC_FoldingTF = True, #True/False
	_CDACDrv_ArrangedTF = False, #True= Arranged, False=CommonCent
	## CDAC Drv
		## Unit DRv
			## Common
				# XVT
			_CDACDrv_XVT = 'SLVT',
			## NMOS
			_CDACDrv_NMOS_NumberofGate=1,  # Number
			_CDACDrv_NMOS_ChannelWidth = 145, #Number
			_CDACDrv_NMOS_ChannelLength = 30, #Number
			## PMOS
			_CDACDrv_PMOS_NumberofGate=1,  # Number
			_CDACDrv_PMOS_ChannelWidth = 879, #Number
			_CDACDrv_PMOS_ChannelLength = 30, #Number
		## Option1: Decimation (CommonCentroid Only, _CDACDrv_ArrangedTF = 'False')
		##			ex) len(_CDACDrv_Decimation_Factor) == _NumofCbit// coresponse to [MSB, MSB-1, ... LSB(=UnitCap)] // If MSB=3, MSBDRv:128 --> 44(128을 3으로 나눈몫+나머지) // "1" means no decimation
		_CDACDrv_Decimation_Factor=[1, 1, 1, 1],
		## Option2: (Arragned Only, _CDACDrv_ArrangedTF = 'True')
		_CDACDrv_DesignatedEachSize = [8,4,3,3], # Vector, designates each driver size(multiples of Unit Drv size)
	## CDAC
			## Element CDAC
			_CDAC_LayoutOption=[3],  # Vector, Consecutive Number [3,4,5]
			_CDAC_MetalWidth=50,  # Number
			_CDAC_MetalLength=1410,  # Number (8bit size: 1414/ 10bit size: 2800/ 12bit size: 4200)
			_CDAC_MetalSpacing=50,  # Number

			## Unit Cap
			_CDAC_NumOfElement=2,  # Number

			## Shield
			_CDAC_ShieldingLayer=1,  # Poly:0, M1:1, M2:2 ...
			_CDAC_ConnectLength=411,  # Number
			_CDAC_ExtendLength=400,  # Number

			## Dummy Cap Option
			_CDAC_NumOfDummyCaps=9,  # Number, Number of dummy cap(one side)
			_CDAC_DummyCap_TopBottomShort=None,  # True => Top - Bottom Short, False -> Bottom = GND, None => Floating Bottom Node

			## CommonCentroid With Driving node
			_CDAC_CapArrayWDrivingNodeDistance=1611,  # Number
			_CDAC_DriveNodeDistance=279,  # Number
			_CDAC_YWidth_Bottom_Hrz=60,  # Number
			_CDAC_BotNodeVtcExtensionMetalLayer=1,




## Bootstrapped Switch
	# Input/Output node
		# INPUT node
		_Sampler_Inputnode_width = 500,  # number
		# OUTPUT node
		_Sampler_Outputnode_width = 500,  # number
	# TR1
		_Sampler_Tr1_NumberofGate	            = 1,       # Number
		_Sampler_Tr1_ChannelWidth	            = 100,     # Number
		_Sampler_Tr1_ChannelLength	            = 30,       # Number
		_Sampler_Tr1_XVT				        = 'SLVT',    # 'XVT' ex)SLVT/LVT/RVT/HVT
	# TR2
		_Sampler_Tr2_NumberofGate	            = 5,       # Number
		_Sampler_Tr2_ChannelWidth	            = 700,     # Number
		_Sampler_Tr2_ChannelLength	            = 30,       # Number
		_Sampler_Tr2_XVT				        = 'SLVT',    # 'XVT' ex)SLVT/LVT/RVT/HVT
	# TR4
		_Sampler_Tr4_NumberofGate	            = 4,       # Number
		_Sampler_Tr4_ChannelWidth	            = 500,     # Number
		_Sampler_Tr4_ChannelLength	            = 30,       # Number
		_Sampler_Tr4_XVT				        = 'RVT',    # 'XVT' ex)SLVT/LVT/RVT/HVT
	# TR5
		_Sampler_Tr5_NumberofGate	            = 2,       # Number
		_Sampler_Tr5_ChannelWidth	            = 1000,     # Number
		_Sampler_Tr5_ChannelLength	            = 30,       # Number
		_Sampler_Tr5_XVT				        = 'SLVT',    # 'XVT' ex)SLVT/LVT/RVT/HVT
	# TR7
		_Sampler_Tr7_NumberofGate               = 3,  # Number
		_Sampler_Tr7_ChannelWidth	            = 233,     # Number
		_Sampler_Tr7_ChannelLength	            = 30,       # Number
		_Sampler_Tr7_XVT				        = 'SLVT',    # 'XVT' ex)SLVT/LVT/RVT/HVT
	# TR9
		_Sampler_Tr9_NumberofGate               = 3,  # Number
		_Sampler_Tr9_ChannelWidth	            = 500,     # Number
		_Sampler_Tr9_ChannelLength	            = 30,       # Number
		_Sampler_Tr9_XVT				        = 'LVT',    # 'XVT' ex)SLVT/LVT/RVT/HVT
	# TR8
		_Sampler_Tr8_NumberofGate	            = 4,       # Number
		_Sampler_Tr8_ChannelWidth	            = 500,     # Number
		_Sampler_Tr8_ChannelLength	            = 30,       # Number
		_Sampler_Tr8_XVT				        = 'RVT',    # 'XVT' ex)SLVT/LVT/RVT/HVT
	# TR6
		_Sampler_Tr6_NumberofGate	            = 1,       # Number
		_Sampler_Tr6_ChannelWidth	            = 500,     # Number
		_Sampler_Tr6_ChannelLength	            = 30,       # Number
		_Sampler_Tr6_XVT				        = 'RVT',    # 'XVT' ex)SLVT/LVT/RVT/HVT
	# TR11
		_Sampler_Tr11_NumberofGate	            = 20,       # Number
		_Sampler_Tr11_ChannelWidth	            = 500,     # Number
		_Sampler_Tr11_ChannelLength	            = 30,       # Number
		_Sampler_Tr11_XVT				        = 'RVT',    # 'XVT' ex)SLVT/LVT/RVT/HVT
	# Tie4N
		_Sampler_Tie4N_NumberofGate     	    = 5,       # Number
		_Sampler_Tie4N_ChannelWidth	            = 250,     # Number
		_Sampler_Tie4N_ChannelLength	        = 30,       # Number
		_Sampler_Tie4N_XVT				        = 'SLVT',    # 'XVT' ex)SLVT/LVT/RVT/HVT
	# Tie4P
		_Sampler_Tie4P_NumberofGate	            = 5,       # Number
		_Sampler_Tie4P_ChannelWidth	            = 500,     # Number
		_Sampler_Tie4P_ChannelLength	        = 30,       # Number
		_Sampler_Tie4P_XVT				        = 'SLVT',    # 'XVT' ex)SLVT/LVT/RVT/HVT
	# Tie8N
		_Sampler_Tie8N_NumberofGate	            = 4,       # Number
		_Sampler_Tie8N_ChannelWidth	            = 250,     # Number
		_Sampler_Tie8N_ChannelLength	        = 30,       # Number
		_Sampler_Tie8N_XVT				        = 'SLVT',    # 'XVT' ex)SLVT/LVT/RVT/HVT
	# Tie8P
		_Sampler_Tie8P_NumberofGate	            = 4,       # Number
		_Sampler_Tie8P_ChannelWidth	            = 500,     # Number
		_Sampler_Tie8P_ChannelLength	        = 30,       # Number
		_Sampler_Tie8P_XVT				        = 'SLVT',    # 'XVT' ex)SLVT/LVT/RVT/HVT
	# TR12
		_Sampler_Tr12_NumberofGate	            = 4,       # Number
		_Sampler_Tr12_ChannelWidth	            = 1500,     # Number
		_Sampler_Tr12_ChannelLength	            = 30,       # Number
		_Sampler_Tr12_XVT				        = 'RVT',    # 'XVT' ex)SLVT/LVT/RVT/HVT
	# TR3
		_Sampler_Tr3_NumberofGate	            = 2,       # Number
		_Sampler_Tr3_ChannelWidth	            = 100,     # Number
		_Sampler_Tr3_ChannelLength	            = 30,       # Number
		_Sampler_Tr3_XVT				        = 'LVT',    # 'XVT' ex)SLVT/LVT/RVT/HVT
	# TR10
		_Sampler_Tr10_NumberofGate	            = 8,       # Number
		_Sampler_Tr10_ChannelWidth	            = 780,     # Number
		_Sampler_Tr10_ChannelLength	            = 30,       # Number
		_Sampler_Tr10_XVT				        = 'RVT',    # 'XVT' ex)SLVT/LVT/RVT/HVT

	# HDVNCAP
		_Sampler_HDVNCAP_Length = 7000,
		_Sampler_HDVNCAP_LayoutOption = [3,4,5,6], # Writedown [number1, number2, number3, ...]
		_Sampler_HDVNCAP_NumFigPair = 62, #number (ref:75)

		_Sampler_HDVNCAP_Array = 3, #number: 1xnumber
		_Sampler_HDVNCAP_Cbot_Ctop_metalwidth = 1000, #number

	# CLKBGen Inverter
		#Common
		_Sampler_ClkbGenInv_XVT                        = 'SLVT',
		#Nmos
		_Sampler_ClkbGenInv_NMOS_NumberofGate          = 1,        # Number
		_Sampler_ClkbGenInv_NMOS_ChannelWidth          = 100,      # Number
		_Sampler_ClkbGenInv_NMOS_ChannelLength         = 30,       # Number
		#Pmos
		_Sampler_ClkbGenInv_PMOS_NumberofGate          = 1,        # Number
		_Sampler_ClkbGenInv_PMOS_ChannelWidth          = 100,      # Number
		_Sampler_ClkbGenInv_PMOS_ChannelLength         = 30,       # Number
		#Body
		_Sampler_ClkbGenInv_NMOS_Pbody_XvtTop2Pbody    = None,     # Number/None(Minimum)
		_Sampler_ClkbGenInv_PMOS_Nbody_Xvtdown2Nbody   = None,     # Number/None(Minimum)
		#Height
		_Sampler_ClkbGenInv_PMOSXvt2NMOSXvt            = 1800,     # number


#RDAC and Decoder
	#RDAC and Decoder delta X displacement for DRC
	_RDAC_displacement = +1000,
	#RDAC and Decoder Size : Consider "_Decoder_RBit" and "_Unit_Num_EachStag_input" ex) [2, 8] --> 4 : 2*8 = 2**4
	_RDAC_Size = [1,16],
	#ResArray
		#Unit Resistor
		_RDAC_Array_ResWidth	=	5300,
		_RDAC_Array_ResLength	=	1500,

	## Decoder
		## Array
			# _Unit to Unit distance for DRC of routing
			_RDAC_Decoder_Unit2UnitDist=1000,  # number must be 100의 배수
		# Unit
			## Comoon
				# Routing
				_RDAC_Decoder_Unit_Routing_Dist=50,
				# Xvt
				_RDAC_Decoder_Unit_Xvt='SLVT',
				# Dist
				_RDAC_Decoder_Unit_GatetoGateDist = 100,
				# Inputs of Nand,Nor
				_RDAC_Decoder_Unit_Num_EachStag_input = [4], # ex) [2,3,4] 가장 마지막단(TG driving) nand input4, Nor input3, Nand input2, Nor input2 ...
				# Power rail
					# Pbody_Pulldown(NMOS)
					_RDAC_Decoder_Unit_Pbody_XvtTop2Pbody    = None,  # Number/None(Minimum)
					# Nbody_Pullup(PMOS)
					_RDAC_Decoder_Unit_Nbody_Xvtdown2Nbody   = None,  # Number/None(Minimum)
					# PMOS and NMOS Height
					_RDAC_Decoder_Unit_PMOSXvt2NMOSXvt       = 1200,  # number
			# Nand( _Decoder_Unit_Num_EachStag_input에서 1,3,5,7...번째 해당하는 nand 생성)
				# MOSFET
					# Common
					_RDAC_Decoder_Nand_NumberofGate      = [1,2],  # Number
					_RDAC_Decoder_Nand_ChannelLength     = [30,30],  # Number
					# Pulldown(NMOS)
						_RDAC_Decoder_Nand_NMOS_ChannelWidth                 = [350,500],  # Number
					# Pulldown(PMOS)
						_RDAC_Decoder_Nand_PMOS_ChannelWidth                 = [350,480],  # Number
			# Nor( _Decoder_Unit_Num_EachStag_input에서 2,4,6,7...번째 해당하는 nor 생성)
				# MOSFET
					# Common
					_RDAC_Decoder_Nor_NumberofGate=[2, 7],  # Number
					_RDAC_Decoder_Nor_ChannelLength      = [30,30],  # Number
					# Pulldown(NMOS)
						_RDAC_Decoder_Nor_NMOS_ChannelWidth	= [400,800],      # Number
					# Pulldown(PMOS)
						_RDAC_Decoder_Nor_PMOS_ChannelWidth	= [800,1600],      # Number
			# Inv
				#Common
				_RDAC_Decoder_Inv_NumberofGate   = 5,
				_RDAC_Decoder_Inv_ChannelLength  = 30,
				# NMosfet
					_RDAC_Decoder_Inv_NMOS_ChannelWidth	= 400,      # Number
				# PMosfet
					_RDAC_Decoder_Inv_PMOS_ChannelWidth  = 800,      # Number
			# Xgate
				# Common
				_RDAC_Decoder_Xgate_NumberofGate     = 3,
				_RDAC_Decoder_Xgate_ChannelLength    = 30,
				# NMosfet
					_RDAC_Decoder_Xgate_NMOS_ChannelWidth    = 400,      # Number
				# PMosfet
					_RDAC_Decoder_Xgate_PMOS_ChannelWidth    = 800,      # Number


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
_NumofCbit=4,
_NumofRbit=0,

## SAR Logic
	## Clock Tree (Driving SAR Logic)
		## Clock Tree Updward (CLK Source Tree, CLK Samp Tree)
			## CLK Buffer Unit
				## Common
				_LOGIC_CLKBufTreeTop_UnitBuf_XVT='SLVT',
				## Nmos
				_LOGIC_CLKBufTreeTop_UnitBuf_NMOS_NumberofGate=1,  # Number
				_LOGIC_CLKBufTreeTop_UnitBuf_NMOS_ChannelWidth=400,  # Number
				_LOGIC_CLKBufTreeTop_UnitBuf_NMOS_ChannelLength=30,  # Number
				## Pmos
				_LOGIC_CLKBufTreeTop_UnitBuf_PMOS_NumberofGate=1,  # Number
				_LOGIC_CLKBufTreeTop_UnitBuf_PMOS_ChannelWidth=800,  # Number
				_LOGIC_CLKBufTreeTop_UnitBuf_PMOS_ChannelLength=30,  # Number
				# Height
				_LOGIC_CLKBufTreeTop_UnitBuf_PMOSXvt2NMOSXvt=446,  # number
			## Clock Buffer Tree structure
			_LOGIC_CLKBufTreeTop_BufTree1and2_NumOfStage=4,  # len[Buf0, Buf1, ... ] 스테이지 수 (아래 버퍼 사이즈 리스트의 길이와 같아야 함.)
			_LOGIC_CLKBufTreeTop_BufTree1_SizeofEachStage=[1, 2, 4, 8],  # CLKSampBuf: [Buf0, Buf1, Buf2 ...]
			_LOGIC_CLKBufTreeTop_BufTree2_SizeofEachStage=[1, 2, 4, 8],  # CLKSrcBuf: [Buf0, Buf1, Buf2 ...]
			_LOGIC_CLKBufTreeTop_XOffSet=0,
		## Clock Tree Dnward (CLK Source Tree, CLK Samp Tree)
			## CLK Buffer Unit
				## Common
				_LOGIC_CLKBufTreeBot_UnitBuf_XVT='SLVT',
				## Nmos
				_LOGIC_CLKBufTreeBot_UnitBuf_NMOS_NumberofGate=1,  # Number
				_LOGIC_CLKBufTreeBot_UnitBuf_NMOS_ChannelWidth=400,  # Number
				_LOGIC_CLKBufTreeBot_UnitBuf_NMOS_ChannelLength=30,  # Number
				## Pmos
				_LOGIC_CLKBufTreeBot_UnitBuf_PMOS_NumberofGate=1,  # Number
				_LOGIC_CLKBufTreeBot_UnitBuf_PMOS_ChannelWidth=800,  # Number
				_LOGIC_CLKBufTreeBot_UnitBuf_PMOS_ChannelLength=30,  # Number
				# Height
				_LOGIC_CLKBufTreeBot_UnitBuf_PMOSXvt2NMOSXvt=446,  # number
			## Clock Buffer Tree structure
			_LOGIC_CLKBufTreeBot_BufTree1and2_NumOfStage=4,  # len[Buf0, Buf1, ... ] 스테이지 수 (아래 버퍼 사이즈 리스트의 길이와 같아야 함.)
			_LOGIC_CLKBufTreeBot_BufTree1_SizeofEachStage=[1, 2, 4, 8],  # CompOutBuf: [Buf0, Buf1, Buf2 ...]
			_LOGIC_CLKBufTreeBot_BufTree2_SizeofEachStage=[1, 2, 4, 8],  # CLKDoutBuf: [Buf0, Buf1, Buf2 ...]
			_LOGIC_CLKBufTreeBot_XOffSet=0,

	## Clock Spine (Physical demension)
		## CLK Source: upward, 1st floor
		_LOGIC_YWidthOfCLKSrc=100,
		## CLK Samp: upward, 2nd floor
		_LOGIC_SpaceBtwCLKSrcAndCLKSamp=100,
		_LOGIC_YWidthOfCLKSamp=100,
		## Comparator Output: downward, Basement1
		_LOGIC_YWidthOfCompOut=100,
		## CLK Dout: downward, basement2
		_LOGIC_SpaceBtwCompOutAndCLKDout=100,
		_LOGIC_YWidthOfCLKDout=100,

	## SetResetDFF
		## DFF Common
		_LOGIC_Test_distance=320,
		_LOGIC_DFF_PMOSXvt2NMOSXvt    = 1150, # number

		## Master Xgate1
			## Xgate common
			_LOGIC_Mst_Xgate1_XVT='SLVT',
			## Xgate NMOS
			_LOGIC_Mst_Xgate1_NMOS_NumberofGate=1,
			_LOGIC_Mst_Xgate1_NMOS_ChannelWidth=300,
			_LOGIC_Mst_Xgate1_NMOS_ChannelLength=30,
			## Xgate PMOS
			_LOGIC_Mst_Xgate1_PMOS_NumberofGate=3,
			_LOGIC_Mst_Xgate1_PMOS_ChannelWidth=500,
			_LOGIC_Mst_Xgate1_PMOS_ChannelLength=30,

		## Master Xgate2
			## Xgate common
			_LOGIC_Mst_Xgate2_XVT='SLVT',
			## Xgate NMOS
			_LOGIC_Mst_Xgate2_NMOS_NumberofGate           = 2,
			_LOGIC_Mst_Xgate2_NMOS_ChannelWidth           = 800,
			_LOGIC_Mst_Xgate2_NMOS_ChannelLength          = 30,
			## Xgate PMOS
			_LOGIC_Mst_Xgate2_PMOS_NumberofGate           = 3,
			_LOGIC_Mst_Xgate2_PMOS_ChannelWidth           = 200,
			_LOGIC_Mst_Xgate2_PMOS_ChannelLength          = 30,

		## Master Nor1
			## Nor1 common
			_LOGIC_Mst_Nor1_XVT='SLVT',
			## NMOS
				## NMOSA
				_LOGIC_Mst_Nor1_NMOSA_NumberofGate           = 2,
				_LOGIC_Mst_Nor1_NMOSA_ChannelWidth           = 800,
				_LOGIC_Mst_Nor1_NMOSA_ChannelLength          = 30,
				## NMOSB
				_LOGIC_Mst_Nor1_NMOSB_NumberofGate           = 3,
				_LOGIC_Mst_Nor1_NMOSB_ChannelWidth           = 200,
				_LOGIC_Mst_Nor1_NMOSB_ChannelLength          = 30,
			## PMOS
				## PMOSA
				_LOGIC_Mst_Nor1_PMOSA_NumberofGate            = 2,
				_LOGIC_Mst_Nor1_PMOSA_ChannelWidth            = 800,
				_LOGIC_Mst_Nor1_PMOSA_ChannelLength           = 30,
				## PMOSB
				_LOGIC_Mst_Nor1_PMOSB_NumberofGate            = 3,
				_LOGIC_Mst_Nor1_PMOSB_ChannelWidth            = 200,
				_LOGIC_Mst_Nor1_PMOSB_ChannelLength           = 30,

		## Master Nor2
			## Nor2 common
			_LOGIC_Mst_Nor2_XVT='SLVT',
			## NMOS
				## NMOSA
				_LOGIC_Mst_Nor2_NMOSA_NumberofGate           = 2,
				_LOGIC_Mst_Nor2_NMOSA_ChannelWidth           = 800,
				_LOGIC_Mst_Nor2_NMOSA_ChannelLength          = 30,
				## NMOSB
				_LOGIC_Mst_Nor2_NMOSB_NumberofGate           = 3,
				_LOGIC_Mst_Nor2_NMOSB_ChannelWidth           = 200,
				_LOGIC_Mst_Nor2_NMOSB_ChannelLength          = 30,
			## PMOS
				## PMOSA
				_LOGIC_Mst_Nor2_PMOSA_NumberofGate            = 2,
				_LOGIC_Mst_Nor2_PMOSA_ChannelWidth            = 800,
				_LOGIC_Mst_Nor2_PMOSA_ChannelLength           = 30,
				## PMOSB
				_LOGIC_Mst_Nor2_PMOSB_NumberofGate            = 3,
				_LOGIC_Mst_Nor2_PMOSB_ChannelWidth            = 200,
				_LOGIC_Mst_Nor2_PMOSB_ChannelLength           = 30,

		## Master Inv1 : Set pre-driver
			## Inv1 common
			_LOGIC_Mst_Inv1_XVT='SLVT',
			## Inv1 NMOS
			_LOGIC_Mst_Inv1_NMOS_NumberofGate           = 1,
			_LOGIC_Mst_Inv1_NMOS_ChannelWidth           = 300,
			_LOGIC_Mst_Inv1_NMOS_ChannelLength          = 30,
			## Inv1 PMOS
			_LOGIC_Mst_Inv1_PMOS_NumberofGate           = 3,
			_LOGIC_Mst_Inv1_PMOS_ChannelWidth           = 500,
			_LOGIC_Mst_Inv1_PMOS_ChannelLength          = 30,

		## Master Inv2 : Set driver
			## Inv2 common
			_LOGIC_Mst_Inv2_XVT='SLVT',
			## Inv2 NMOS
			_LOGIC_Mst_Inv2_NMOS_NumberofGate           = 1,
			_LOGIC_Mst_Inv2_NMOS_ChannelWidth           = 300,
			_LOGIC_Mst_Inv2_NMOS_ChannelLength          = 30,
			## Inv2 PMOS
			_LOGIC_Mst_Inv2_PMOS_NumberofGate           = 3,
			_LOGIC_Mst_Inv2_PMOS_ChannelWidth           = 500,
			_LOGIC_Mst_Inv2_PMOS_ChannelLength          = 30,

		## Master Inv3 : Clock driver
			## Inv3 common
			_LOGIC_Mst_Inv3_XVT='SLVT',
			## Inv3 NMOS
			_LOGIC_Mst_Inv3_NMOS_NumberofGate           = 1,
			_LOGIC_Mst_Inv3_NMOS_ChannelWidth           = 300,
			_LOGIC_Mst_Inv3_NMOS_ChannelLength          = 30,
			## Inv3 PMOS
			_LOGIC_Mst_Inv3_PMOS_NumberofGate           = 3,
			_LOGIC_Mst_Inv3_PMOS_ChannelWidth           = 500,
			_LOGIC_Mst_Inv3_PMOS_ChannelLength          = 30,

		## Slave Xgate1
			## Xgate common
			_LOGIC_Slv_Xgate1_XVT='SLVT',
			## Xgate NMOS
			_LOGIC_Slv_Xgate1_NMOS_NumberofGate           = 1,
			_LOGIC_Slv_Xgate1_NMOS_ChannelWidth           = 300,
			_LOGIC_Slv_Xgate1_NMOS_ChannelLength          = 30,
			## Xgate PMOS
			_LOGIC_Slv_Xgate1_PMOS_NumberofGate           = 3,
			_LOGIC_Slv_Xgate1_PMOS_ChannelWidth           = 500,
			_LOGIC_Slv_Xgate1_PMOS_ChannelLength          = 30,

		## Slave Xgate2
			## Xgate common
			_LOGIC_Slv_Xgate2_XVT='SLVT',
			## Xgate NMOS
			_LOGIC_Slv_Xgate2_NMOS_NumberofGate           = 2,
			_LOGIC_Slv_Xgate2_NMOS_ChannelWidth           = 800,
			_LOGIC_Slv_Xgate2_NMOS_ChannelLength          = 30,
			## Xgate PMOS
			_LOGIC_Slv_Xgate2_PMOS_NumberofGate           = 3,
			_LOGIC_Slv_Xgate2_PMOS_ChannelWidth           = 200,
			_LOGIC_Slv_Xgate2_PMOS_ChannelLength          = 30,

		## Slave Nor1
			## Nor1 common
			_LOGIC_Slv_Nor1_XVT='SLVT',
			## NMOS
				## NMOSA
				_LOGIC_Slv_Nor1_NMOSA_NumberofGate           = 2,
				_LOGIC_Slv_Nor1_NMOSA_ChannelWidth           = 800,
				_LOGIC_Slv_Nor1_NMOSA_ChannelLength          = 30,
				## NMOSB
				_LOGIC_Slv_Nor1_NMOSB_NumberofGate           = 3,
				_LOGIC_Slv_Nor1_NMOSB_ChannelWidth           = 200,
				_LOGIC_Slv_Nor1_NMOSB_ChannelLength          = 30,
			## PMOS
				## PMOSA
				_LOGIC_Slv_Nor1_PMOSA_NumberofGate            = 2,
				_LOGIC_Slv_Nor1_PMOSA_ChannelWidth            = 800,
				_LOGIC_Slv_Nor1_PMOSA_ChannelLength           = 30,
				## PMOSB
				_LOGIC_Slv_Nor1_PMOSB_NumberofGate            = 3,
				_LOGIC_Slv_Nor1_PMOSB_ChannelWidth            = 200,
				_LOGIC_Slv_Nor1_PMOSB_ChannelLength           = 30,

		## Slave Nor2
			## Nor2 common
			_LOGIC_Slv_Nor2_XVT='SLVT',
			## NMOS
				## NMOSA
				_LOGIC_Slv_Nor2_NMOSA_NumberofGate           = 2,
				_LOGIC_Slv_Nor2_NMOSA_ChannelWidth           = 800,
				_LOGIC_Slv_Nor2_NMOSA_ChannelLength          = 30,
				## NMOSB
				_LOGIC_Slv_Nor2_NMOSB_NumberofGate           = 3,
				_LOGIC_Slv_Nor2_NMOSB_ChannelWidth           = 200,
				_LOGIC_Slv_Nor2_NMOSB_ChannelLength          = 30,
			## PMOS
				## PMOSA
				_LOGIC_Slv_Nor2_PMOSA_NumberofGate            = 2,
				_LOGIC_Slv_Nor2_PMOSA_ChannelWidth            = 800,
				_LOGIC_Slv_Nor2_PMOSA_ChannelLength           = 30,
				## PMOSB
				_LOGIC_Slv_Nor2_PMOSB_NumberofGate            = 3,
				_LOGIC_Slv_Nor2_PMOSB_ChannelWidth            = 200,
				_LOGIC_Slv_Nor2_PMOSB_ChannelLength           = 30,

		## Slave Inv1 : ReSet pre-driver
			## Inv1 common
			_LOGIC_Slv_Inv1_XVT='SLVT',
			## Inv1 NMOS
			_LOGIC_Slv_Inv1_NMOS_NumberofGate           = 1,
			_LOGIC_Slv_Inv1_NMOS_ChannelWidth           = 300,
			_LOGIC_Slv_Inv1_NMOS_ChannelLength          = 30,
			## Inv1 PMOS
			_LOGIC_Slv_Inv1_PMOS_NumberofGate           = 3,
			_LOGIC_Slv_Inv1_PMOS_ChannelWidth           = 500,
			_LOGIC_Slv_Inv1_PMOS_ChannelLength          = 30,

		## Slave Inv2 : ReSet driver
			## Inv2 common
			_LOGIC_Slv_Inv2_XVT='SLVT',
			## Inv2 NMOS
			_LOGIC_Slv_Inv2_NMOS_NumberofGate           = 1,
			_LOGIC_Slv_Inv2_NMOS_ChannelWidth           = 300,
			_LOGIC_Slv_Inv2_NMOS_ChannelLength          = 30,
			## Inv2 PMOS
			_LOGIC_Slv_Inv2_PMOS_NumberofGate           = 3,
			_LOGIC_Slv_Inv2_PMOS_ChannelWidth           = 500,
			_LOGIC_Slv_Inv2_PMOS_ChannelLength          = 30,

		## Slave Inv3 : Qb driver
			## Inv3 common
			_LOGIC_Slv_Inv3_XVT='SLVT',
			## Inv3 NMOS
			_LOGIC_Slv_Inv3_NMOS_NumberofGate           = 1,
			_LOGIC_Slv_Inv3_NMOS_ChannelWidth           = 300,
			_LOGIC_Slv_Inv3_NMOS_ChannelLength          = 30,
			## Inv3 PMOS
			_LOGIC_Slv_Inv3_PMOS_NumberofGate           = 3,
			_LOGIC_Slv_Inv3_PMOS_ChannelWidth           = 500,
			_LOGIC_Slv_Inv3_PMOS_ChannelLength          = 30,
	## DAC PreDriver
		## Inverter Chain
			## InvChain Common
			_LOGIC_DACPreDrv_PMOSXvt2NMOSXvt=500,  # number
			## Inverter Chain
				## Inv1 common
			_LOGIC_DACPreDrv_NumberofGate=[[1, 2, 4, 8],[1, 2, 4, 8], [1, 2, 4, 8], [1],      ],  # Vector
			_RDAC_InputComple_Inv_NumofGate = [], # Vector, _LOGIC_DACPreDrv_NumberofGate + _RDAC_InputComple_Inv_NumofGate로 입력됨
			_LOGIC_DACPreDrv_ChannelLength=30,  # Scalar
			_LOGIC_DACPreDrv_XVT='SLVT',  # 'SLVT'
				## Inv1 NMOS
			_LOGIC_DACPreDrv_Inv_NMOS_ChannelWidth=400,  # Scalar
				## Inv1 PMOS
			_LOGIC_DACPreDrv_Inv_PMOS_ChannelWidth=800,  # Scalar
	## CLKOutSamp(!=ClkSamp)
		## Common
			# XVT
			_LOGIC_CLKoutSamp_XVT = 'SLVT',
			# Height
			# _CLKOutSamp_PMOSXvt2NMOSXvt=1800,  # number, = _DFF_PMOSXvt2NMOSXvt
		## Inverter
			# Nmos
			_LOGIC_CLKoutSamp_Inv_NMOS_NumberofGate=1,  # Number
			_LOGIC_CLKoutSamp_Inv_NMOS_ChannelWidth=100,  # Number
			_LOGIC_CLKoutSamp_Inv_NMOS_ChannelLength=30,  # Number
			# Pmos
			_LOGIC_CLKoutSamp_Inv_PMOS_NumberofGate=1,  # Number
			_LOGIC_CLKoutSamp_Inv_PMOS_ChannelWidth=100,  # Number
			_LOGIC_CLKoutSamp_Inv_PMOS_ChannelLength=30,  # Number
		## AND
			## AND Common
			## Nand
				# NmosA
				_LOGIC_CLKoutSamp_And_Nand_NMOSA_NumberofGate=1,  # Number
				_LOGIC_CLKoutSamp_And_Nand_NMOSA_ChannelWidth=100,  # Number
				_LOGIC_CLKoutSamp_And_Nand_NMOSA_ChannelLength=30,  # Number
				# NMOSB
				_LOGIC_CLKoutSamp_And_Nand_NMOSB_NumberofGate=2,  # Number
				_LOGIC_CLKoutSamp_And_Nand_NMOSB_ChannelWidth=750,  # Number
				_LOGIC_CLKoutSamp_And_Nand_NMOSB_ChannelLength=30,  # Number
				# PMOSA
				_LOGIC_CLKoutSamp_And_Nand_PMOSA_NumberofGate=1,  # Number
				_LOGIC_CLKoutSamp_And_Nand_PMOSA_ChannelWidth=300,  # Number
				_LOGIC_CLKoutSamp_And_Nand_PMOSA_ChannelLength=30,  # Number
				# PMOSB
				_LOGIC_CLKoutSamp_And_Nand_PMOSB_NumberofGate=3,  # Number
				_LOGIC_CLKoutSamp_And_Nand_PMOSB_ChannelWidth=750,  # Number
				_LOGIC_CLKoutSamp_And_Nand_PMOSB_ChannelLength=30,  # Number
			## Inverter
				# Nmos
				_LOGIC_CLKoutSamp_And_Inv_NMOS_NumberofGate=1,  # Number
				_LOGIC_CLKoutSamp_And_Inv_NMOS_ChannelWidth=100,  # Number
				_LOGIC_CLKoutSamp_And_Inv_NMOS_ChannelLength=30,  # Number
				# Pmos
				_LOGIC_CLKoutSamp_And_Inv_PMOS_NumberofGate=1,  # Number
				_LOGIC_CLKoutSamp_And_Inv_PMOS_ChannelWidth=200,  # Number
				_LOGIC_CLKoutSamp_And_Inv_PMOS_ChannelLength=30,  # Number


## Comparator
	## StrongARM Latch
		# Common
		_COMP_SALatch_ChannelLength=30,  # random.randrange(30, 60, 2),  # 30
		_COMP_SALatch_XVT='HVT',

		# PMOS
		_COMP_SALatch_CLKinputPMOSFinger1=1,  #PMOS Reset Sw1 # random.randint(1, 15),  # 6
		_COMP_SALatch_CLKinputPMOSFinger2=1,  #PMOS Reset Sw2 # random.randint(1, 15),  # 3
		_COMP_SALatch_PMOSFinger=1,  		  #PMOS Latch	  # random.randint(1, 15),  # 3
		_COMP_SALatch_PMOSChannelWidth=1000,  #All PMOS width # random.randrange(200, 1050, 2),  # 500

		# NMOS
		_COMP_SALatch_DATAinputNMOSFinger=3,  #NMOS Input Tr # random.randint(3, 15),  # 12
		_COMP_SALatch_NMOSFinger=2,  		  #NMOS at Latch # random.randint(1, 15),  # 2
		_COMP_SALatch_CLKinputNMOSFinger=1,  #NMOS Tail # random.randint(1, 15),  # 8
		_COMP_SALatch_NMOSChannelWidth=330,  #Nmos width # random.randrange(200, 1050, 2),  # 500
		_COMP_SALatch_CLKinputNMOSChannelWidth=200,  # random.randrange(200, 1050, 2),  # 800

	## StrongArmOutBuffer and SRLatch
		## Common
			# XVT
			_COMP_SAOutBufAndSRLatch_XVT='SLVT',
			# Body
			_COMP_SAOutBufAndSRLatch_NMOS_Pbody_XvtTop2Pbody=None,  # Number/None(Minimum)
			_COMP_SAOutBufAndSRLatch_PMOS_Nbody_Xvtdown2Nbody=None,  # Number/None(Minimum)
			# Height
			_COMP_SAOutBufAndSRLatch_PMOSXvt2NMOSXvt=1800,  # number
		## StronArm Output Buffer
			## Inverter1(pre)
					#Nmos
				_COMP_SAOutBuf_Buf_Inv1_NMOS_NumberofGate          = 1,        # Number
				_COMP_SAOutBuf_Buf_Inv1_NMOS_ChannelWidth          = 400,      # Number
				_COMP_SAOutBuf_Buf_Inv1_NMOS_ChannelLength         = 30,       # Number
					#Pmos
				_COMP_SAOutBuf_Buf_Inv1_PMOS_NumberofGate          = 1,        # Number
				_COMP_SAOutBuf_Buf_Inv1_PMOS_ChannelWidth          = 800,      # Number
				_COMP_SAOutBuf_Buf_Inv1_PMOS_ChannelLength         = 30,       # Number
			## Inverter2
					#Nmos
				_COMP_SAOutBuf_Buf_Inv2_NMOS_NumberofGate          = 2,        # Number
				_COMP_SAOutBuf_Buf_Inv2_NMOS_ChannelWidth          = 400,      # Number
				_COMP_SAOutBuf_Buf_Inv2_NMOS_ChannelLength         = 30,       # Number
					#Pmos
				_COMP_SAOutBuf_Buf_Inv2_PMOS_NumberofGate          = 2,        # Number
				_COMP_SAOutBuf_Buf_Inv2_PMOS_ChannelWidth          = 800,      # Number
				_COMP_SAOutBuf_Buf_Inv2_PMOS_ChannelLength         = 30,       # Number
		## SRLatch
			## Nand(Set,Rst same)
				# NmosA
				_COMP_SRLatch_Nand_NMOSA_NumberofGate=1,  # Number
				_COMP_SRLatch_Nand_NMOSA_ChannelWidth=100,  # Number
				_COMP_SRLatch_Nand_NMOSA_ChannelLength=30,  # Number
				# NMOSB
				_COMP_SRLatch_Nand_NMOSB_NumberofGate=2,  # Number
				_COMP_SRLatch_Nand_NMOSB_ChannelWidth=750,  # Number
				_COMP_SRLatch_Nand_NMOSB_ChannelLength=30,  # Number
				# PMOSA
				_COMP_SRLatch_Nand_PMOSA_NumberofGate=2,  # Number
				_COMP_SRLatch_Nand_PMOSA_ChannelWidth=100,  # Number
				_COMP_SRLatch_Nand_PMOSA_ChannelLength=30,  # Number
				# PMOSB
				_COMP_SRLatch_Nand_PMOSB_NumberofGate=1,  # Number
				_COMP_SRLatch_Nand_PMOSB_ChannelWidth=750,  # Number
				_COMP_SRLatch_Nand_PMOSB_ChannelLength=30,  # Number

	## Comp clock Gen Logic: Clk_Samp Inv, Clk_Source Inv, AND Gate, CompClockBuff
		## Common
			# XVT
			_COMP_CompClkLogic_XVT='SLVT',
			# Body
			_COMP_CompClkLogic_NMOS_Pbody_XvtTop2Pbody=None,  # Number/None(Minimum)
			_COMP_CompClkLogic_PMOS_Nbody_Xvtdown2Nbody=None,  # Number/None(Minimum)
			# Height
			_COMP_CompClkLogic_PMOSXvt2NMOSXvt=1800,  # number
		## StronArm Output Buffer
			## Inverter1(pre)
					#Nmos
				_COMP_CompClkLogic_Buf_Inv1_NMOS_NumberofGate          = 2,        # Number
				_COMP_CompClkLogic_Buf_Inv1_NMOS_ChannelWidth          = 400,      # Number
				_COMP_CompClkLogic_Buf_Inv1_NMOS_ChannelLength         = 30,       # Number
					#Pmos
				_COMP_CompClkLogic_Buf_Inv1_PMOS_NumberofGate          = 2,        # Number
				_COMP_CompClkLogic_Buf_Inv1_PMOS_ChannelWidth          = 800,      # Number
				_COMP_CompClkLogic_Buf_Inv1_PMOS_ChannelLength         = 30,       # Number
			## Inverter2
					#Nmos
				_COMP_CompClkLogic_Buf_Inv2_NMOS_NumberofGate          = 4,        # Number
				_COMP_CompClkLogic_Buf_Inv2_NMOS_ChannelWidth          = 400,      # Number
				_COMP_CompClkLogic_Buf_Inv2_NMOS_ChannelLength         = 30,       # Number
					#Pmos
				_COMP_CompClkLogic_Buf_Inv2_PMOS_NumberofGate          = 4,        # Number
				_COMP_CompClkLogic_Buf_Inv2_PMOS_ChannelWidth          = 800,      # Number
				_COMP_CompClkLogic_Buf_Inv2_PMOS_ChannelLength         = 30,       # Number
		## AND
			## Nand
				# NmosA
				_COMP_CompClkLogic_Nand_NMOSA_NumberofGate=1,  # Number
				_COMP_CompClkLogic_Nand_NMOSA_ChannelWidth=100,  # Number
				_COMP_CompClkLogic_Nand_NMOSA_ChannelLength=30,  # Number
				# NMOSB
				_COMP_CompClkLogic_Nand_NMOSB_NumberofGate=2,  # Number
				_COMP_CompClkLogic_Nand_NMOSB_ChannelWidth=750,  # Number
				_COMP_CompClkLogic_Nand_NMOSB_ChannelLength=30,  # Number
				# PMOSA
				_COMP_CompClkLogic_Nand_PMOSA_NumberofGate=1,  # Number
				_COMP_CompClkLogic_Nand_PMOSA_ChannelWidth=300,  # Number
				_COMP_CompClkLogic_Nand_PMOSA_ChannelLength=30,  # Number
				# PMOSB
				_COMP_CompClkLogic_Nand_PMOSB_NumberofGate=3,  # Number
				_COMP_CompClkLogic_Nand_PMOSB_ChannelWidth=750,  # Number
				_COMP_CompClkLogic_Nand_PMOSB_ChannelLength=30,  # Number
			## Inverter
				# Nmos
				_COMP_CompClkLogic_Inv_NMOS_NumberofGate=1,  # Number
				_COMP_CompClkLogic_Inv_NMOS_ChannelWidth=100,  # Number
				_COMP_CompClkLogic_Inv_NMOS_ChannelLength=30,  # Number
				# Pmos
				_COMP_CompClkLogic_Inv_PMOS_NumberofGate=1,  # Number
				_COMP_CompClkLogic_Inv_PMOS_ChannelWidth=200,  # Number
				_COMP_CompClkLogic_Inv_PMOS_ChannelLength=30,  # Number

		## Clk_Source Inv
				#Nmos
			_COMP_CompClkLogic_ClkSrc_NMOS_NumberofGate          = 1,        # Number
			_COMP_CompClkLogic_ClkSrc_NMOS_ChannelWidth          = 400,      # Number
			_COMP_CompClkLogic_ClkSrc_NMOS_ChannelLength         = 30,       # Number
				#Pmos
			_COMP_CompClkLogic_ClkSrc_PMOS_NumberofGate          = 1,        # Number
			_COMP_CompClkLogic_ClkSrc_PMOS_ChannelWidth          = 800,      # Number
			_COMP_CompClkLogic_ClkSrc_PMOS_ChannelLength         = 30,       # Number
		## Clk_Samp Inv
				#Nmos
			_COMP_CompClkLogic_ClkSmp_NMOS_NumberofGate          = 1,        # Number
			_COMP_CompClkLogic_ClkSmp_NMOS_ChannelWidth          = 400,      # Number
			_COMP_CompClkLogic_ClkSmp_NMOS_ChannelLength         = 30,       # Number
				#Pmos
			_COMP_CompClkLogic_ClkSmp_PMOS_NumberofGate          = 1,        # Number
			_COMP_CompClkLogic_ClkSmp_PMOS_ChannelWidth          = 800,      # Number
			_COMP_CompClkLogic_ClkSmp_PMOS_ChannelLength         = 30,       # Number




## CLOCK AND DATA BUF : Comparator Dout Buf for driving Logic, CLKSamp and CLKScr Buff for Driving Sampler and Comparator
	## Top placed
		## CLK Samp
			## InvChain Common
				## Height
		_BUF_CLKSamp_PMOSXvt2NMOSXvt = 500,  # number
			## Inverter Chain
				## Inv1 common
		_BUF_CLKSamp_XVT='SLVT',
		_BUF_CLKSamp_NumberofGate = [1,2,4,8],  # Vector,
		_BUF_CLKSamp_ChanneLength = 30,
				## NMOS
		_BUF_CLKSamp_NMOSChannelWidth = 784,
				## PMOS
		_BUF_CLKSamp_PMOSChannelWidth = 833,
		## CLK Scr
			## InvChain Common
				## Height
		_BUF_CLKScr_PMOSXvt2NMOSXvt = 500,  # number
			## Inverter Chain
				## Inv1 common
		_BUF_CLKScr_XVT='SLVT',
		_BUF_CLKScr_NumberofGate = [1,2,4,8],  # Vector,
		_BUF_CLKScr_ChanneLength = 30,
				## NMOS
		_BUF_CLKScr_NMOSChannelWidth = 784,
				## PMOS
		_BUF_CLKScr_PMOSChannelWidth = 833,
	## Bottom Placed
		## CompOut
			## InvChain Common
				## Height
		_BUF_CompOut_PMOSXvt2NMOSXvt = 500,  # number
			## Inverter Chain
				## Inv1 common
		_BUF_CompOut_XVT='SLVT',
		_BUF_CompOut_NumberofGate = [1,2,4,8],  # Vector,
		_BUF_CompOut_ChanneLength = 30,
				## NMOS
		_BUF_CompOut_NMOSChannelWidth = 784,
				## PMOS
		_BUF_CompOut_PMOSChannelWidth = 833,



## CDAC
	## CDAC Configuration
	_CDAC_FoldingTF = True, #True/False
	_CDACDrv_ArrangedTF = False, #True= Arranged, False=CommonCent
	## CDAC Drv
		## Unit DRv
			## Common
				# XVT
			_CDACDrv_XVT = 'SLVT',
			## NMOS
			_CDACDrv_NMOS_NumberofGate=1,  # Number
			_CDACDrv_NMOS_ChannelWidth = 145, #Number
			_CDACDrv_NMOS_ChannelLength = 30, #Number
			## PMOS
			_CDACDrv_PMOS_NumberofGate=1,  # Number
			_CDACDrv_PMOS_ChannelWidth = 879, #Number
			_CDACDrv_PMOS_ChannelLength = 30, #Number
		## Option1: Decimation (CommonCentroid Only, _CDACDrv_ArrangedTF = 'False')
		##			ex) len(_CDACDrv_Decimation_Factor) == _NumofCbit// coresponse to [MSB, MSB-1, ... LSB(=UnitCap)] // If MSB=3, MSBDRv:128 --> 44(128을 3으로 나눈몫+나머지) // "1" means no decimation
		_CDACDrv_Decimation_Factor=[1, 1, 1, 1],
		## Option2: (Arragned Only, _CDACDrv_ArrangedTF = 'True')
		_CDACDrv_DesignatedEachSize = [8,4,3,3], # Vector, designates each driver size(multiples of Unit Drv size)
	## CDAC
			## Element CDAC
			_CDAC_LayoutOption=[3],  # Vector, Consecutive Number [3,4,5]
			_CDAC_MetalWidth=50,  # Number
			_CDAC_MetalLength=1410,  # Number (8bit size: 1414/ 10bit size: 2800/ 12bit size: 4200)
			_CDAC_MetalSpacing=50,  # Number

			## Unit Cap
			_CDAC_NumOfElement=2,  # Number

			## Shield
			_CDAC_ShieldingLayer=1,  # Poly:0, M1:1, M2:2 ...
			_CDAC_ConnectLength=411,  # Number
			_CDAC_ExtendLength=400,  # Number

			## Dummy Cap Option
			_CDAC_NumOfDummyCaps=9,  # Number, Number of dummy cap(one side)
			_CDAC_DummyCap_TopBottomShort=None,  # True => Top - Bottom Short, False -> Bottom = GND, None => Floating Bottom Node

			## CommonCentroid With Driving node
			_CDAC_CapArrayWDrivingNodeDistance=1611,  # Number
			_CDAC_DriveNodeDistance=279,  # Number
			_CDAC_YWidth_Bottom_Hrz=60,  # Number
			_CDAC_BotNodeVtcExtensionMetalLayer=1,




## Bootstrapped Switch
	# Input/Output node
		# INPUT node
		_Sampler_Inputnode_width = 500,  # number
		# OUTPUT node
		_Sampler_Outputnode_width = 500,  # number
	# TR1
		_Sampler_Tr1_NumberofGate	            = 1,       # Number
		_Sampler_Tr1_ChannelWidth	            = 100,     # Number
		_Sampler_Tr1_ChannelLength	            = 30,       # Number
		_Sampler_Tr1_XVT				        = 'SLVT',    # 'XVT' ex)SLVT/LVT/RVT/HVT
	# TR2
		_Sampler_Tr2_NumberofGate	            = 5,       # Number
		_Sampler_Tr2_ChannelWidth	            = 700,     # Number
		_Sampler_Tr2_ChannelLength	            = 30,       # Number
		_Sampler_Tr2_XVT				        = 'SLVT',    # 'XVT' ex)SLVT/LVT/RVT/HVT
	# TR4
		_Sampler_Tr4_NumberofGate	            = 4,       # Number
		_Sampler_Tr4_ChannelWidth	            = 500,     # Number
		_Sampler_Tr4_ChannelLength	            = 30,       # Number
		_Sampler_Tr4_XVT				        = 'RVT',    # 'XVT' ex)SLVT/LVT/RVT/HVT
	# TR5
		_Sampler_Tr5_NumberofGate	            = 2,       # Number
		_Sampler_Tr5_ChannelWidth	            = 1000,     # Number
		_Sampler_Tr5_ChannelLength	            = 30,       # Number
		_Sampler_Tr5_XVT				        = 'SLVT',    # 'XVT' ex)SLVT/LVT/RVT/HVT
	# TR7
		_Sampler_Tr7_NumberofGate               = 3,  # Number
		_Sampler_Tr7_ChannelWidth	            = 233,     # Number
		_Sampler_Tr7_ChannelLength	            = 30,       # Number
		_Sampler_Tr7_XVT				        = 'SLVT',    # 'XVT' ex)SLVT/LVT/RVT/HVT
	# TR9
		_Sampler_Tr9_NumberofGate               = 3,  # Number
		_Sampler_Tr9_ChannelWidth	            = 500,     # Number
		_Sampler_Tr9_ChannelLength	            = 30,       # Number
		_Sampler_Tr9_XVT				        = 'LVT',    # 'XVT' ex)SLVT/LVT/RVT/HVT
	# TR8
		_Sampler_Tr8_NumberofGate	            = 4,       # Number
		_Sampler_Tr8_ChannelWidth	            = 500,     # Number
		_Sampler_Tr8_ChannelLength	            = 30,       # Number
		_Sampler_Tr8_XVT				        = 'RVT',    # 'XVT' ex)SLVT/LVT/RVT/HVT
	# TR6
		_Sampler_Tr6_NumberofGate	            = 1,       # Number
		_Sampler_Tr6_ChannelWidth	            = 500,     # Number
		_Sampler_Tr6_ChannelLength	            = 30,       # Number
		_Sampler_Tr6_XVT				        = 'RVT',    # 'XVT' ex)SLVT/LVT/RVT/HVT
	# TR11
		_Sampler_Tr11_NumberofGate	            = 20,       # Number
		_Sampler_Tr11_ChannelWidth	            = 500,     # Number
		_Sampler_Tr11_ChannelLength	            = 30,       # Number
		_Sampler_Tr11_XVT				        = 'RVT',    # 'XVT' ex)SLVT/LVT/RVT/HVT
	# Tie4N
		_Sampler_Tie4N_NumberofGate     	    = 5,       # Number
		_Sampler_Tie4N_ChannelWidth	            = 250,     # Number
		_Sampler_Tie4N_ChannelLength	        = 30,       # Number
		_Sampler_Tie4N_XVT				        = 'SLVT',    # 'XVT' ex)SLVT/LVT/RVT/HVT
	# Tie4P
		_Sampler_Tie4P_NumberofGate	            = 5,       # Number
		_Sampler_Tie4P_ChannelWidth	            = 500,     # Number
		_Sampler_Tie4P_ChannelLength	        = 30,       # Number
		_Sampler_Tie4P_XVT				        = 'SLVT',    # 'XVT' ex)SLVT/LVT/RVT/HVT
	# Tie8N
		_Sampler_Tie8N_NumberofGate	            = 4,       # Number
		_Sampler_Tie8N_ChannelWidth	            = 250,     # Number
		_Sampler_Tie8N_ChannelLength	        = 30,       # Number
		_Sampler_Tie8N_XVT				        = 'SLVT',    # 'XVT' ex)SLVT/LVT/RVT/HVT
	# Tie8P
		_Sampler_Tie8P_NumberofGate	            = 4,       # Number
		_Sampler_Tie8P_ChannelWidth	            = 500,     # Number
		_Sampler_Tie8P_ChannelLength	        = 30,       # Number
		_Sampler_Tie8P_XVT				        = 'SLVT',    # 'XVT' ex)SLVT/LVT/RVT/HVT
	# TR12
		_Sampler_Tr12_NumberofGate	            = 4,       # Number
		_Sampler_Tr12_ChannelWidth	            = 1500,     # Number
		_Sampler_Tr12_ChannelLength	            = 30,       # Number
		_Sampler_Tr12_XVT				        = 'RVT',    # 'XVT' ex)SLVT/LVT/RVT/HVT
	# TR3
		_Sampler_Tr3_NumberofGate	            = 2,       # Number
		_Sampler_Tr3_ChannelWidth	            = 100,     # Number
		_Sampler_Tr3_ChannelLength	            = 30,       # Number
		_Sampler_Tr3_XVT				        = 'LVT',    # 'XVT' ex)SLVT/LVT/RVT/HVT
	# TR10
		_Sampler_Tr10_NumberofGate	            = 8,       # Number
		_Sampler_Tr10_ChannelWidth	            = 780,     # Number
		_Sampler_Tr10_ChannelLength	            = 30,       # Number
		_Sampler_Tr10_XVT				        = 'RVT',    # 'XVT' ex)SLVT/LVT/RVT/HVT

	# HDVNCAP
		_Sampler_HDVNCAP_Length = 7000,
		_Sampler_HDVNCAP_LayoutOption = [3,4,5,6], # Writedown [number1, number2, number3, ...]
		_Sampler_HDVNCAP_NumFigPair = 62, #number (ref:75)

		_Sampler_HDVNCAP_Array = 3, #number: 1xnumber
		_Sampler_HDVNCAP_Cbot_Ctop_metalwidth = 1000, #number

	# CLKBGen Inverter
		#Common
		_Sampler_ClkbGenInv_XVT                        = 'SLVT',
		#Nmos
		_Sampler_ClkbGenInv_NMOS_NumberofGate          = 1,        # Number
		_Sampler_ClkbGenInv_NMOS_ChannelWidth          = 100,      # Number
		_Sampler_ClkbGenInv_NMOS_ChannelLength         = 30,       # Number
		#Pmos
		_Sampler_ClkbGenInv_PMOS_NumberofGate          = 1,        # Number
		_Sampler_ClkbGenInv_PMOS_ChannelWidth          = 100,      # Number
		_Sampler_ClkbGenInv_PMOS_ChannelLength         = 30,       # Number
		#Body
		_Sampler_ClkbGenInv_NMOS_Pbody_XvtTop2Pbody    = None,     # Number/None(Minimum)
		_Sampler_ClkbGenInv_PMOS_Nbody_Xvtdown2Nbody   = None,     # Number/None(Minimum)
		#Height
		_Sampler_ClkbGenInv_PMOSXvt2NMOSXvt            = 1800,     # number


#RDAC and Decoder
	#RDAC and Decoder delta X displacement for DRC
	_RDAC_displacement = +1000,
	#RDAC and Decoder Size : Consider "_Decoder_RBit" and "_Unit_Num_EachStag_input" ex) [2, 8] --> 4 : 2*8 = 2**4
	_RDAC_Size = [1,16],
	#ResArray
		#Unit Resistor
		_RDAC_Array_ResWidth	=	5300,
		_RDAC_Array_ResLength	=	1500,

	## Decoder
		## Array
			# _Unit to Unit distance for DRC of routing
			_RDAC_Decoder_Unit2UnitDist=1000,  # number must be 100의 배수
		# Unit
			## Comoon
				# Routing
				_RDAC_Decoder_Unit_Routing_Dist=50,
				# Xvt
				_RDAC_Decoder_Unit_Xvt='SLVT',
				# Dist
				_RDAC_Decoder_Unit_GatetoGateDist = 100,
				# Inputs of Nand,Nor
				_RDAC_Decoder_Unit_Num_EachStag_input = [4], # ex) [2,3,4] 가장 마지막단(TG driving) nand input4, Nor input3, Nand input2, Nor input2 ...
				# Power rail
					# Pbody_Pulldown(NMOS)
					_RDAC_Decoder_Unit_Pbody_XvtTop2Pbody    = None,  # Number/None(Minimum)
					# Nbody_Pullup(PMOS)
					_RDAC_Decoder_Unit_Nbody_Xvtdown2Nbody   = None,  # Number/None(Minimum)
					# PMOS and NMOS Height
					_RDAC_Decoder_Unit_PMOSXvt2NMOSXvt       = 1200,  # number
			# Nand( _Decoder_Unit_Num_EachStag_input에서 1,3,5,7...번째 해당하는 nand 생성)
				# MOSFET
					# Common
					_RDAC_Decoder_Nand_NumberofGate      = [1,2],  # Number
					_RDAC_Decoder_Nand_ChannelLength     = [30,30],  # Number
					# Pulldown(NMOS)
						_RDAC_Decoder_Nand_NMOS_ChannelWidth                 = [350,500],  # Number
					# Pulldown(PMOS)
						_RDAC_Decoder_Nand_PMOS_ChannelWidth                 = [350,480],  # Number
			# Nor( _Decoder_Unit_Num_EachStag_input에서 2,4,6,7...번째 해당하는 nor 생성)
				# MOSFET
					# Common
					_RDAC_Decoder_Nor_NumberofGate=[2, 7],  # Number
					_RDAC_Decoder_Nor_ChannelLength      = [30,30],  # Number
					# Pulldown(NMOS)
						_RDAC_Decoder_Nor_NMOS_ChannelWidth	= [400,800],      # Number
					# Pulldown(PMOS)
						_RDAC_Decoder_Nor_PMOS_ChannelWidth	= [800,1600],      # Number
			# Inv
				#Common
				_RDAC_Decoder_Inv_NumberofGate   = 5,
				_RDAC_Decoder_Inv_ChannelLength  = 30,
				# NMosfet
					_RDAC_Decoder_Inv_NMOS_ChannelWidth	= 400,      # Number
				# PMosfet
					_RDAC_Decoder_Inv_PMOS_ChannelWidth  = 800,      # Number
			# Xgate
				# Common
				_RDAC_Decoder_Xgate_NumberofGate     = 3,
				_RDAC_Decoder_Xgate_ChannelLength    = 30,
				# NMosfet
					_RDAC_Decoder_Xgate_NMOS_ChannelWidth    = 400,      # Number
				# PMosfet
					_RDAC_Decoder_Xgate_PMOS_ChannelWidth    = 800,      # Number


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

		################################################################################################### Pre-defined
		_Numofbit = _NumofCbit + _NumofRbit
		_SpaceBtwBootSWPosNeg = 200
		##
		A = _LOGIC_DACPreDrv_NumberofGate
		B = _RDAC_InputComple_Inv_NumofGate
		for sublist, b in zip(A[-len(B):], B):
			sublist.append(b)
		_LOGIC_DACPreDrv_NumberofGate2 = A
		################################################################################################### Raise Error
		# Error Raise1
		if _CDACDrv_ArrangedTF == True:
			if len(_CDACDrv_DesignatedEachSize) != _NumofCbit:
				raise NotImplementedError(f"_CDACDrv_DesignatedEachSize != _NumofCbit !!!")
		# Error Raise2
		if _NumofRbit !=0:
			if _RDAC_Size[0]*_RDAC_Size[1] > 2**_RDAC_Decoder_Unit_Num_EachStag_input[0]:
				raise NotImplementedError(f"RDAC Array Size > Nand Input")
		# Error Raise3
		if len(_LOGIC_DACPreDrv_NumberofGate) != _Numofbit:
			raise NotImplementedError(f"_LOGIC_DACPreDrv_NumberofGate != _Numofbit !!!")
		# Error Raise4
		if _NumofRbit !=0:
			tmp = _RDAC_Size[0]*_RDAC_Size[1]
			tmp_RBit = math.log(tmp,2)
			if tmp_RBit != _NumofRbit:
				raise NotImplementedError(f"RDAC Array Size != _NumofRbit !!!")
		# Error Raise4
		if _NumofRbit != 0:
			if len(_RDAC_InputComple_Inv_NumofGate) != _NumofRbit:
				raise NotImplementedError(f"Len(_RDAC_InputComple_Inv_NumofGate) != _NumofRbit !!!")
		# Error Raise5
		if _CDACDrv_ArrangedTF == False:
			if len(_CDACDrv_Decimation_Factor) != _NumofCbit:
				raise NotImplementedError(f"len(_CDACDrv_Decimation_Factor) != _NumofCbit !!!")
		###################################################################################################

		_Caculation_Parameters1 = copy.deepcopy(L00_SARLogicWtComparator_KJH._SARLogicWtComparator._ParametersForDesignCalculation)
		## Define Calculation_Parameters ex) _Caculation_Parameters1['_NMOSPOWER_PbodyContact_1_Length']  = _NMOSPOWER_PbodyContact_1_Length
		_Caculation_Parameters1['_NumofBit'] = _Numofbit
		## SAR Logic
			## Clock Tree (Driving SAR Logic)
				## Clock Tree Updward (CLK Source Tree, CLK Samp Tree)
					## CLK Buffer Unit
						## Common
		_Caculation_Parameters1['_LOGIC_CLKBufTreeTop_UnitBuf_XVT'] = _LOGIC_CLKBufTreeTop_UnitBuf_XVT
						## Nmos
		_Caculation_Parameters1['_LOGIC_CLKBufTreeTop_UnitBuf_NMOS_NumberofGate'] = _LOGIC_CLKBufTreeTop_UnitBuf_NMOS_NumberofGate
		_Caculation_Parameters1['_LOGIC_CLKBufTreeTop_UnitBuf_NMOS_ChannelWidth'] = _LOGIC_CLKBufTreeTop_UnitBuf_NMOS_ChannelWidth
		_Caculation_Parameters1['_LOGIC_CLKBufTreeTop_UnitBuf_NMOS_ChannelLength'] = _LOGIC_CLKBufTreeTop_UnitBuf_NMOS_ChannelLength
						## Pmos
		_Caculation_Parameters1['_LOGIC_CLKBufTreeTop_UnitBuf_PMOS_NumberofGate'] = _LOGIC_CLKBufTreeTop_UnitBuf_PMOS_NumberofGate
		_Caculation_Parameters1['_LOGIC_CLKBufTreeTop_UnitBuf_PMOS_ChannelWidth'] = _LOGIC_CLKBufTreeTop_UnitBuf_PMOS_ChannelWidth
		_Caculation_Parameters1['_LOGIC_CLKBufTreeTop_UnitBuf_PMOS_ChannelLength'] = _LOGIC_CLKBufTreeTop_UnitBuf_PMOS_ChannelLength
						## Height
		_Caculation_Parameters1['_LOGIC_CLKBufTreeTop_UnitBuf_PMOSXvt2NMOSXvt'] = _LOGIC_CLKBufTreeTop_UnitBuf_PMOSXvt2NMOSXvt
					## Clock Buffer Tree structure
		_Caculation_Parameters1['_LOGIC_CLKBufTreeTop_BufTree1and2_NumOfStage'] = _LOGIC_CLKBufTreeTop_BufTree1and2_NumOfStage
		_Caculation_Parameters1['_LOGIC_CLKBufTreeTop_BufTree1_SizeofEachStage'] = _LOGIC_CLKBufTreeTop_BufTree1_SizeofEachStage
		_Caculation_Parameters1['_LOGIC_CLKBufTreeTop_BufTree2_SizeofEachStage'] = _LOGIC_CLKBufTreeTop_BufTree2_SizeofEachStage
		_Caculation_Parameters1['_LOGIC_CLKBufTreeTop_XOffSet'] 				= _LOGIC_CLKBufTreeTop_XOffSet
				## Clock Tree Dnward (CLK Source Tree, CLK Samp Tree)
					## CLK Buffer Unit
						## Common
		_Caculation_Parameters1['_LOGIC_CLKBufTreeBot_UnitBuf_XVT'] = _LOGIC_CLKBufTreeBot_UnitBuf_XVT
						## Nmos
		_Caculation_Parameters1['_LOGIC_CLKBufTreeBot_UnitBuf_NMOS_NumberofGate'] = _LOGIC_CLKBufTreeBot_UnitBuf_NMOS_NumberofGate
		_Caculation_Parameters1['_LOGIC_CLKBufTreeBot_UnitBuf_NMOS_ChannelWidth'] = _LOGIC_CLKBufTreeBot_UnitBuf_NMOS_ChannelWidth
		_Caculation_Parameters1['_LOGIC_CLKBufTreeBot_UnitBuf_NMOS_ChannelLength'] = _LOGIC_CLKBufTreeBot_UnitBuf_NMOS_ChannelLength
						## Pmos
		_Caculation_Parameters1['_LOGIC_CLKBufTreeBot_UnitBuf_PMOS_NumberofGate'] = _LOGIC_CLKBufTreeBot_UnitBuf_PMOS_NumberofGate
		_Caculation_Parameters1['_LOGIC_CLKBufTreeBot_UnitBuf_PMOS_ChannelWidth'] = _LOGIC_CLKBufTreeBot_UnitBuf_PMOS_ChannelWidth
		_Caculation_Parameters1['_LOGIC_CLKBufTreeBot_UnitBuf_PMOS_ChannelLength'] = _LOGIC_CLKBufTreeBot_UnitBuf_PMOS_ChannelLength
						## Height
		_Caculation_Parameters1['_LOGIC_CLKBufTreeBot_UnitBuf_PMOSXvt2NMOSXvt'] = _LOGIC_CLKBufTreeBot_UnitBuf_PMOSXvt2NMOSXvt
					## Clock Buffer Tree structure
		_Caculation_Parameters1['_LOGIC_CLKBufTreeBot_BufTree1and2_NumOfStage'] = _LOGIC_CLKBufTreeBot_BufTree1and2_NumOfStage
		_Caculation_Parameters1['_LOGIC_CLKBufTreeBot_BufTree1_SizeofEachStage'] = _LOGIC_CLKBufTreeBot_BufTree1_SizeofEachStage
		_Caculation_Parameters1['_LOGIC_CLKBufTreeBot_BufTree2_SizeofEachStage'] = _LOGIC_CLKBufTreeBot_BufTree2_SizeofEachStage
		_Caculation_Parameters1['_LOGIC_CLKBufTreeBot_XOffSet'] = _LOGIC_CLKBufTreeBot_XOffSet
			## Clock Spine (Physical demension)
				## CLK Source: upward, 1st floor
		_Caculation_Parameters1['_LOGIC_YWidthOfCLKSrc'] = _LOGIC_YWidthOfCLKSrc
				## CLK Samp: upward, 2nd floor
		_Caculation_Parameters1['_LOGIC_SpaceBtwCLKSrcAndCLKSamp'] = _LOGIC_SpaceBtwCLKSrcAndCLKSamp
		_Caculation_Parameters1['_LOGIC_YWidthOfCLKSamp'] = _LOGIC_YWidthOfCLKSamp
				## Comparator Output: downward, Basement1
		_Caculation_Parameters1['_LOGIC_YWidthOfCompOut'] = _LOGIC_YWidthOfCompOut
				## CLK Dout: downward, basement2
		_Caculation_Parameters1['_LOGIC_SpaceBtwCompOutAndCLKDout'] = _LOGIC_SpaceBtwCompOutAndCLKDout
		_Caculation_Parameters1['_LOGIC_YWidthOfCLKDout'] = _LOGIC_YWidthOfCLKDout

			## SetResetDFF
				## DFF Common
		_Caculation_Parameters1['_LOGIC_Test_distance'] = _LOGIC_Test_distance
		_Caculation_Parameters1['_LOGIC_DFF_PMOSXvt2NMOSXvt'] = _LOGIC_DFF_PMOSXvt2NMOSXvt
				## Master Xgate1
					## Xgate common
		_Caculation_Parameters1['_LOGIC_Mst_Xgate1_XVT'] = _LOGIC_Mst_Xgate1_XVT
					## Xgate NMOS
		_Caculation_Parameters1['_LOGIC_Mst_Xgate1_NMOS_NumberofGate'] = _LOGIC_Mst_Xgate1_NMOS_NumberofGate
		_Caculation_Parameters1['_LOGIC_Mst_Xgate1_NMOS_ChannelWidth'] = _LOGIC_Mst_Xgate1_NMOS_ChannelWidth
		_Caculation_Parameters1['_LOGIC_Mst_Xgate1_NMOS_ChannelLength'] = _LOGIC_Mst_Xgate1_NMOS_ChannelLength
					## Xgate PMOS
		_Caculation_Parameters1['_LOGIC_Mst_Xgate1_PMOS_NumberofGate'] = _LOGIC_Mst_Xgate1_PMOS_NumberofGate
		_Caculation_Parameters1['_LOGIC_Mst_Xgate1_PMOS_ChannelWidth'] = _LOGIC_Mst_Xgate1_PMOS_ChannelWidth
		_Caculation_Parameters1['_LOGIC_Mst_Xgate1_PMOS_ChannelLength'] = _LOGIC_Mst_Xgate1_PMOS_ChannelLength
				## Master Xgate2
					## Xgate common
		_Caculation_Parameters1['_LOGIC_Mst_Xgate2_XVT'] = _LOGIC_Mst_Xgate2_XVT
					## Xgate NMOS
		_Caculation_Parameters1['_LOGIC_Mst_Xgate2_NMOS_NumberofGate'] = _LOGIC_Mst_Xgate2_NMOS_NumberofGate
		_Caculation_Parameters1['_LOGIC_Mst_Xgate2_NMOS_ChannelWidth'] = _LOGIC_Mst_Xgate2_NMOS_ChannelWidth
		_Caculation_Parameters1['_LOGIC_Mst_Xgate2_NMOS_ChannelLength'] = _LOGIC_Mst_Xgate2_NMOS_ChannelLength
					## Xgate PMOS
		_Caculation_Parameters1['_LOGIC_Mst_Xgate2_PMOS_NumberofGate'] = _LOGIC_Mst_Xgate2_PMOS_NumberofGate
		_Caculation_Parameters1['_LOGIC_Mst_Xgate2_PMOS_ChannelWidth'] = _LOGIC_Mst_Xgate2_PMOS_ChannelWidth
		_Caculation_Parameters1['_LOGIC_Mst_Xgate2_PMOS_ChannelLength'] = _LOGIC_Mst_Xgate2_PMOS_ChannelLength
				## Master Nor1
					## Nor1 common
		_Caculation_Parameters1['_LOGIC_Mst_Nor1_XVT'] = _LOGIC_Mst_Nor1_XVT
					## NMOS
						## NMOSA
		_Caculation_Parameters1['_LOGIC_Mst_Nor1_NMOSA_NumberofGate'] = _LOGIC_Mst_Nor1_NMOSA_NumberofGate
		_Caculation_Parameters1['_LOGIC_Mst_Nor1_NMOSA_ChannelWidth'] = _LOGIC_Mst_Nor1_NMOSA_ChannelWidth
		_Caculation_Parameters1['_LOGIC_Mst_Nor1_NMOSA_ChannelLength'] = _LOGIC_Mst_Nor1_NMOSA_ChannelLength
						## NMOSB
		_Caculation_Parameters1['_LOGIC_Mst_Nor1_NMOSB_NumberofGate'] = _LOGIC_Mst_Nor1_NMOSB_NumberofGate
		_Caculation_Parameters1['_LOGIC_Mst_Nor1_NMOSB_ChannelWidth'] = _LOGIC_Mst_Nor1_NMOSB_ChannelWidth
		_Caculation_Parameters1['_LOGIC_Mst_Nor1_NMOSB_ChannelLength'] = _LOGIC_Mst_Nor1_NMOSB_ChannelLength
					## PMOS
						## PMOSA
		_Caculation_Parameters1['_LOGIC_Mst_Nor1_PMOSA_NumberofGate'] = _LOGIC_Mst_Nor1_PMOSA_NumberofGate
		_Caculation_Parameters1['_LOGIC_Mst_Nor1_PMOSA_ChannelWidth'] = _LOGIC_Mst_Nor1_PMOSA_ChannelWidth
		_Caculation_Parameters1['_LOGIC_Mst_Nor1_PMOSA_ChannelLength'] = _LOGIC_Mst_Nor1_PMOSA_ChannelLength
						## PMOSB
		_Caculation_Parameters1['_LOGIC_Mst_Nor1_PMOSB_NumberofGate'] = _LOGIC_Mst_Nor1_PMOSB_NumberofGate
		_Caculation_Parameters1['_LOGIC_Mst_Nor1_PMOSB_ChannelWidth'] = _LOGIC_Mst_Nor1_PMOSB_ChannelWidth
		_Caculation_Parameters1['_LOGIC_Mst_Nor1_PMOSB_ChannelLength'] = _LOGIC_Mst_Nor1_PMOSB_ChannelLength
				## Master Nor2
					## Nor2 common
		_Caculation_Parameters1['_LOGIC_Mst_Nor2_XVT'] = _LOGIC_Mst_Nor2_XVT
					## NMOS
						## NMOSA
		_Caculation_Parameters1['_LOGIC_Mst_Nor2_NMOSA_NumberofGate'] = _LOGIC_Mst_Nor2_NMOSA_NumberofGate
		_Caculation_Parameters1['_LOGIC_Mst_Nor2_NMOSA_ChannelWidth'] = _LOGIC_Mst_Nor2_NMOSA_ChannelWidth
		_Caculation_Parameters1['_LOGIC_Mst_Nor2_NMOSA_ChannelLength'] = _LOGIC_Mst_Nor2_NMOSA_ChannelLength
						## NMOSB
		_Caculation_Parameters1['_LOGIC_Mst_Nor2_NMOSB_NumberofGate'] = _LOGIC_Mst_Nor2_NMOSB_NumberofGate
		_Caculation_Parameters1['_LOGIC_Mst_Nor2_NMOSB_ChannelWidth'] = _LOGIC_Mst_Nor2_NMOSB_ChannelWidth
		_Caculation_Parameters1['_LOGIC_Mst_Nor2_NMOSB_ChannelLength'] = _LOGIC_Mst_Nor2_NMOSB_ChannelLength
					## PMOS
						## PMOSA
		_Caculation_Parameters1['_LOGIC_Mst_Nor2_PMOSA_NumberofGate'] = _LOGIC_Mst_Nor2_PMOSA_NumberofGate
		_Caculation_Parameters1['_LOGIC_Mst_Nor2_PMOSA_ChannelWidth'] = _LOGIC_Mst_Nor2_PMOSA_ChannelWidth
		_Caculation_Parameters1['_LOGIC_Mst_Nor2_PMOSA_ChannelLength'] = _LOGIC_Mst_Nor2_PMOSA_ChannelLength
						## PMOSB
		_Caculation_Parameters1['_LOGIC_Mst_Nor2_PMOSB_NumberofGate'] = _LOGIC_Mst_Nor2_PMOSB_NumberofGate
		_Caculation_Parameters1['_LOGIC_Mst_Nor2_PMOSB_ChannelWidth'] = _LOGIC_Mst_Nor2_PMOSB_ChannelWidth
		_Caculation_Parameters1['_LOGIC_Mst_Nor2_PMOSB_ChannelLength'] = _LOGIC_Mst_Nor2_PMOSB_ChannelLength
				## Master Inv1 : Set pre-driver
					## Inv1 common
		_Caculation_Parameters1['_LOGIC_Mst_Inv1_XVT'] = _LOGIC_Mst_Inv1_XVT
					## Inv1 NMOS
		_Caculation_Parameters1['_LOGIC_Mst_Inv1_NMOS_NumberofGate'] = _LOGIC_Mst_Inv1_NMOS_NumberofGate
		_Caculation_Parameters1['_LOGIC_Mst_Inv1_NMOS_ChannelWidth'] = _LOGIC_Mst_Inv1_NMOS_ChannelWidth
		_Caculation_Parameters1['_LOGIC_Mst_Inv1_NMOS_ChannelLength'] = _LOGIC_Mst_Inv1_NMOS_ChannelLength
					## Inv1 PMOS
		_Caculation_Parameters1['_LOGIC_Mst_Inv1_PMOS_NumberofGate'] = _LOGIC_Mst_Inv1_PMOS_NumberofGate
		_Caculation_Parameters1['_LOGIC_Mst_Inv1_PMOS_ChannelWidth'] = _LOGIC_Mst_Inv1_PMOS_ChannelWidth
		_Caculation_Parameters1['_LOGIC_Mst_Inv1_PMOS_ChannelLength'] = _LOGIC_Mst_Inv1_PMOS_ChannelLength
				## Master Inv2 : Set driver
					## Inv2 common
		_Caculation_Parameters1['_LOGIC_Mst_Inv2_XVT'] = _LOGIC_Mst_Inv2_XVT
					## Inv2 NMOS
		_Caculation_Parameters1['_LOGIC_Mst_Inv2_NMOS_NumberofGate'] = _LOGIC_Mst_Inv2_NMOS_NumberofGate
		_Caculation_Parameters1['_LOGIC_Mst_Inv2_NMOS_ChannelWidth'] = _LOGIC_Mst_Inv2_NMOS_ChannelWidth
		_Caculation_Parameters1['_LOGIC_Mst_Inv2_NMOS_ChannelLength'] = _LOGIC_Mst_Inv2_NMOS_ChannelLength
					## Inv2 PMOS
		_Caculation_Parameters1['_LOGIC_Mst_Inv2_PMOS_NumberofGate'] = _LOGIC_Mst_Inv2_PMOS_NumberofGate
		_Caculation_Parameters1['_LOGIC_Mst_Inv2_PMOS_ChannelWidth'] = _LOGIC_Mst_Inv2_PMOS_ChannelWidth
		_Caculation_Parameters1['_LOGIC_Mst_Inv2_PMOS_ChannelLength'] = _LOGIC_Mst_Inv2_PMOS_ChannelLength
				## Master Inv3 : Clock driver
					## Inv3 common
		_Caculation_Parameters1['_LOGIC_Mst_Inv3_XVT'] = _LOGIC_Mst_Inv3_XVT
					## Inv3 NMOS
		_Caculation_Parameters1['_LOGIC_Mst_Inv3_NMOS_NumberofGate'] = _LOGIC_Mst_Inv3_NMOS_NumberofGate
		_Caculation_Parameters1['_LOGIC_Mst_Inv3_NMOS_ChannelWidth'] = _LOGIC_Mst_Inv3_NMOS_ChannelWidth
		_Caculation_Parameters1['_LOGIC_Mst_Inv3_NMOS_ChannelLength'] = _LOGIC_Mst_Inv3_NMOS_ChannelLength
					## Inv3 PMOS
		_Caculation_Parameters1['_LOGIC_Mst_Inv3_PMOS_NumberofGate'] = _LOGIC_Mst_Inv3_PMOS_NumberofGate
		_Caculation_Parameters1['_LOGIC_Mst_Inv3_PMOS_ChannelWidth'] = _LOGIC_Mst_Inv3_PMOS_ChannelWidth
		_Caculation_Parameters1['_LOGIC_Mst_Inv3_PMOS_ChannelLength'] = _LOGIC_Mst_Inv3_PMOS_ChannelLength

				## Slave Xgate1
					## Xgate common
		_Caculation_Parameters1['_LOGIC_Slv_Xgate1_XVT'] = _LOGIC_Slv_Xgate1_XVT
					## Xgate NMOS
		_Caculation_Parameters1['_LOGIC_Slv_Xgate1_NMOS_NumberofGate'] = _LOGIC_Slv_Xgate1_NMOS_NumberofGate
		_Caculation_Parameters1['_LOGIC_Slv_Xgate1_NMOS_ChannelWidth'] = _LOGIC_Slv_Xgate1_NMOS_ChannelWidth
		_Caculation_Parameters1['_LOGIC_Slv_Xgate1_NMOS_ChannelLength'] = _LOGIC_Slv_Xgate1_NMOS_ChannelLength
					## Xgate PMOS
		_Caculation_Parameters1['_LOGIC_Slv_Xgate1_PMOS_NumberofGate'] = _LOGIC_Slv_Xgate1_PMOS_NumberofGate
		_Caculation_Parameters1['_LOGIC_Slv_Xgate1_PMOS_ChannelWidth'] = _LOGIC_Slv_Xgate1_PMOS_ChannelWidth
		_Caculation_Parameters1['_LOGIC_Slv_Xgate1_PMOS_ChannelLength'] = _LOGIC_Slv_Xgate1_PMOS_ChannelLength
				## Slave Xgate2
					## Xgate common
		_Caculation_Parameters1['_LOGIC_Slv_Xgate2_XVT'] = _LOGIC_Slv_Xgate2_XVT
					## Xgate NMOS
		_Caculation_Parameters1['_LOGIC_Slv_Xgate2_NMOS_NumberofGate'] = _LOGIC_Slv_Xgate2_NMOS_NumberofGate
		_Caculation_Parameters1['_LOGIC_Slv_Xgate2_NMOS_ChannelWidth'] = _LOGIC_Slv_Xgate2_NMOS_ChannelWidth
		_Caculation_Parameters1['_LOGIC_Slv_Xgate2_NMOS_ChannelLength'] = _LOGIC_Slv_Xgate2_NMOS_ChannelLength
					## Xgate PMOS
		_Caculation_Parameters1['_LOGIC_Slv_Xgate2_PMOS_NumberofGate'] = _LOGIC_Slv_Xgate2_PMOS_NumberofGate
		_Caculation_Parameters1['_LOGIC_Slv_Xgate2_PMOS_ChannelWidth'] = _LOGIC_Slv_Xgate2_PMOS_ChannelWidth
		_Caculation_Parameters1['_LOGIC_Slv_Xgate2_PMOS_ChannelLength'] = _LOGIC_Slv_Xgate2_PMOS_ChannelLength
				## Slave Nor1
					## Nor1 common
		_Caculation_Parameters1['_LOGIC_Slv_Nor1_XVT'] = _LOGIC_Slv_Nor1_XVT
					## NMOS
						## NMOSA
		_Caculation_Parameters1['_LOGIC_Slv_Nor1_NMOSA_NumberofGate'] = _LOGIC_Slv_Nor1_NMOSA_NumberofGate
		_Caculation_Parameters1['_LOGIC_Slv_Nor1_NMOSA_ChannelWidth'] = _LOGIC_Slv_Nor1_NMOSA_ChannelWidth
		_Caculation_Parameters1['_LOGIC_Slv_Nor1_NMOSA_ChannelLength'] = _LOGIC_Slv_Nor1_NMOSA_ChannelLength
						## NMOSB
		_Caculation_Parameters1['_LOGIC_Slv_Nor1_NMOSB_NumberofGate'] = _LOGIC_Slv_Nor1_NMOSB_NumberofGate
		_Caculation_Parameters1['_LOGIC_Slv_Nor1_NMOSB_ChannelWidth'] = _LOGIC_Slv_Nor1_NMOSB_ChannelWidth
		_Caculation_Parameters1['_LOGIC_Slv_Nor1_NMOSB_ChannelLength'] = _LOGIC_Slv_Nor1_NMOSB_ChannelLength
					## PMOS
						## PMOSA
		_Caculation_Parameters1['_LOGIC_Slv_Nor1_PMOSA_NumberofGate'] = _LOGIC_Slv_Nor1_PMOSA_NumberofGate
		_Caculation_Parameters1['_LOGIC_Slv_Nor1_PMOSA_ChannelWidth'] = _LOGIC_Slv_Nor1_PMOSA_ChannelWidth
		_Caculation_Parameters1['_LOGIC_Slv_Nor1_PMOSA_ChannelLength'] = _LOGIC_Slv_Nor1_PMOSA_ChannelLength
						## PMOSB
		_Caculation_Parameters1['_LOGIC_Slv_Nor1_PMOSB_NumberofGate'] = _LOGIC_Slv_Nor1_PMOSB_NumberofGate
		_Caculation_Parameters1['_LOGIC_Slv_Nor1_PMOSB_ChannelWidth'] = _LOGIC_Slv_Nor1_PMOSB_ChannelWidth
		_Caculation_Parameters1['_LOGIC_Slv_Nor1_PMOSB_ChannelLength'] = _LOGIC_Slv_Nor1_PMOSB_ChannelLength
				## Slave Nor2
					## Nor2 common
		_Caculation_Parameters1['_LOGIC_Slv_Nor2_XVT'] = _LOGIC_Slv_Nor2_XVT
					## NMOS
						## NMOSA
		_Caculation_Parameters1['_LOGIC_Slv_Nor2_NMOSA_NumberofGate'] = _LOGIC_Slv_Nor2_NMOSA_NumberofGate
		_Caculation_Parameters1['_LOGIC_Slv_Nor2_NMOSA_ChannelWidth'] = _LOGIC_Slv_Nor2_NMOSA_ChannelWidth
		_Caculation_Parameters1['_LOGIC_Slv_Nor2_NMOSA_ChannelLength'] = _LOGIC_Slv_Nor2_NMOSA_ChannelLength
						## NMOSB
		_Caculation_Parameters1['_LOGIC_Slv_Nor2_NMOSB_NumberofGate'] = _LOGIC_Slv_Nor2_NMOSB_NumberofGate
		_Caculation_Parameters1['_LOGIC_Slv_Nor2_NMOSB_ChannelWidth'] = _LOGIC_Slv_Nor2_NMOSB_ChannelWidth
		_Caculation_Parameters1['_LOGIC_Slv_Nor2_NMOSB_ChannelLength'] = _LOGIC_Slv_Nor2_NMOSB_ChannelLength
					## PMOS
						## PMOSA
		_Caculation_Parameters1['_LOGIC_Slv_Nor2_PMOSA_NumberofGate'] = _LOGIC_Slv_Nor2_PMOSA_NumberofGate
		_Caculation_Parameters1['_LOGIC_Slv_Nor2_PMOSA_ChannelWidth'] = _LOGIC_Slv_Nor2_PMOSA_ChannelWidth
		_Caculation_Parameters1['_LOGIC_Slv_Nor2_PMOSA_ChannelLength'] = _LOGIC_Slv_Nor2_PMOSA_ChannelLength
						## PMOSB
		_Caculation_Parameters1['_LOGIC_Slv_Nor2_PMOSB_NumberofGate'] = _LOGIC_Slv_Nor2_PMOSB_NumberofGate
		_Caculation_Parameters1['_LOGIC_Slv_Nor2_PMOSB_ChannelWidth'] = _LOGIC_Slv_Nor2_PMOSB_ChannelWidth
		_Caculation_Parameters1['_LOGIC_Slv_Nor2_PMOSB_ChannelLength'] = _LOGIC_Slv_Nor2_PMOSB_ChannelLength
				## Slave Inv1 : ReSet pre-driver
					## Inv1 common
		_Caculation_Parameters1['_LOGIC_Slv_Inv1_XVT'] = _LOGIC_Slv_Inv1_XVT
					## Inv1 NMOS
		_Caculation_Parameters1['_LOGIC_Slv_Inv1_NMOS_NumberofGate'] = _LOGIC_Slv_Inv1_NMOS_NumberofGate
		_Caculation_Parameters1['_LOGIC_Slv_Inv1_NMOS_ChannelWidth'] = _LOGIC_Slv_Inv1_NMOS_ChannelWidth
		_Caculation_Parameters1['_LOGIC_Slv_Inv1_NMOS_ChannelLength'] = _LOGIC_Slv_Inv1_NMOS_ChannelLength
					## Inv1 PMOS
		_Caculation_Parameters1['_LOGIC_Slv_Inv1_PMOS_NumberofGate'] = _LOGIC_Slv_Inv1_PMOS_NumberofGate
		_Caculation_Parameters1['_LOGIC_Slv_Inv1_PMOS_ChannelWidth'] = _LOGIC_Slv_Inv1_PMOS_ChannelWidth
		_Caculation_Parameters1['_LOGIC_Slv_Inv1_PMOS_ChannelLength'] = _LOGIC_Slv_Inv1_PMOS_ChannelLength
				## Slave Inv2 : ReSet driver
					## Inv2 common
		_Caculation_Parameters1['_LOGIC_Slv_Inv2_XVT'] = _LOGIC_Slv_Inv2_XVT
					## Inv2 NMOS
		_Caculation_Parameters1['_LOGIC_Slv_Inv2_NMOS_NumberofGate'] = _LOGIC_Slv_Inv2_NMOS_NumberofGate
		_Caculation_Parameters1['_LOGIC_Slv_Inv2_NMOS_ChannelWidth'] = _LOGIC_Slv_Inv2_NMOS_ChannelWidth
		_Caculation_Parameters1['_LOGIC_Slv_Inv2_NMOS_ChannelLength'] = _LOGIC_Slv_Inv2_NMOS_ChannelLength
					## Inv2 PMOS
		_Caculation_Parameters1['_LOGIC_Slv_Inv2_PMOS_NumberofGate'] = _LOGIC_Slv_Inv2_PMOS_NumberofGate
		_Caculation_Parameters1['_LOGIC_Slv_Inv2_PMOS_ChannelWidth'] = _LOGIC_Slv_Inv2_PMOS_ChannelWidth
		_Caculation_Parameters1['_LOGIC_Slv_Inv2_PMOS_ChannelLength'] = _LOGIC_Slv_Inv2_PMOS_ChannelLength
				## Slave Inv3 : Qb driver
					## Inv3 common
		_Caculation_Parameters1['_LOGIC_Slv_Inv3_XVT'] = _LOGIC_Slv_Inv3_XVT
					## Inv3 NMOS
		_Caculation_Parameters1['_LOGIC_Slv_Inv3_NMOS_NumberofGate'] = _LOGIC_Slv_Inv3_NMOS_NumberofGate
		_Caculation_Parameters1['_LOGIC_Slv_Inv3_NMOS_ChannelWidth'] = _LOGIC_Slv_Inv3_NMOS_ChannelWidth
		_Caculation_Parameters1['_LOGIC_Slv_Inv3_NMOS_ChannelLength'] = _LOGIC_Slv_Inv3_NMOS_ChannelLength
					## Inv3 PMOS
		_Caculation_Parameters1['_LOGIC_Slv_Inv3_PMOS_NumberofGate'] = _LOGIC_Slv_Inv3_PMOS_NumberofGate
		_Caculation_Parameters1['_LOGIC_Slv_Inv3_PMOS_ChannelWidth'] = _LOGIC_Slv_Inv3_PMOS_ChannelWidth
		_Caculation_Parameters1['_LOGIC_Slv_Inv3_PMOS_ChannelLength'] = _LOGIC_Slv_Inv3_PMOS_ChannelLength

			## DAC PreDriver
				## Inverter Chain
					## InvChain Common
		_Caculation_Parameters1['_LOGIC_DACPreDrv_PMOSXvt2NMOSXvt'] = _LOGIC_DACPreDrv_PMOSXvt2NMOSXvt
				## Inverter Chain
					## Inv1 common
		_Caculation_Parameters1['_LOGIC_DACPreDrv_NumberofGate'] = A
		_Caculation_Parameters1['_LOGIC_DACPreDrv_ChannelLength'] = _LOGIC_DACPreDrv_ChannelLength
		_Caculation_Parameters1['_LOGIC_DACPreDrv_XVT'] = _LOGIC_DACPreDrv_XVT
					## Inv1 NMOS
		_Caculation_Parameters1['_LOGIC_DACPreDrv_Inv_NMOS_ChannelWidth'] = _LOGIC_DACPreDrv_Inv_NMOS_ChannelWidth
					## Inv1 PMOS
		_Caculation_Parameters1['_LOGIC_DACPreDrv_Inv_PMOS_ChannelWidth'] = _LOGIC_DACPreDrv_Inv_PMOS_ChannelWidth
			## CLKOutSamp(!=ClkSamp)
				## Common
					# XVT
		_Caculation_Parameters1['_LOGIC_CLKoutSamp_XVT'] = _LOGIC_CLKoutSamp_XVT
				## Inverter
					# Nmos
		_Caculation_Parameters1['_LOGIC_CLKoutSamp_Inv_NMOS_NumberofGate'] = _LOGIC_CLKoutSamp_Inv_NMOS_NumberofGate
		_Caculation_Parameters1['_LOGIC_CLKoutSamp_Inv_NMOS_ChannelWidth'] = _LOGIC_CLKoutSamp_Inv_NMOS_ChannelWidth
		_Caculation_Parameters1['_LOGIC_CLKoutSamp_Inv_NMOS_ChannelLength'] = _LOGIC_CLKoutSamp_Inv_NMOS_ChannelLength
					# Pmos
		_Caculation_Parameters1['_LOGIC_CLKoutSamp_Inv_PMOS_NumberofGate'] = _LOGIC_CLKoutSamp_Inv_PMOS_NumberofGate
		_Caculation_Parameters1['_LOGIC_CLKoutSamp_Inv_PMOS_ChannelWidth'] = _LOGIC_CLKoutSamp_Inv_PMOS_ChannelWidth
		_Caculation_Parameters1['_LOGIC_CLKoutSamp_Inv_PMOS_ChannelLength'] = _LOGIC_CLKoutSamp_Inv_PMOS_ChannelLength
				## AND
					## AND Common
					## Nand
						# NmosA
		_Caculation_Parameters1['_LOGIC_CLKoutSamp_And_Nand_NMOSA_NumberofGate'] = _LOGIC_CLKoutSamp_And_Nand_NMOSA_NumberofGate
		_Caculation_Parameters1['_LOGIC_CLKoutSamp_And_Nand_NMOSA_ChannelWidth'] = _LOGIC_CLKoutSamp_And_Nand_NMOSA_ChannelWidth
		_Caculation_Parameters1['_LOGIC_CLKoutSamp_And_Nand_NMOSA_ChannelLength'] = _LOGIC_CLKoutSamp_And_Nand_NMOSA_ChannelLength
						# NMOSB
		_Caculation_Parameters1['_LOGIC_CLKoutSamp_And_Nand_NMOSB_NumberofGate'] = _LOGIC_CLKoutSamp_And_Nand_NMOSB_NumberofGate
		_Caculation_Parameters1['_LOGIC_CLKoutSamp_And_Nand_NMOSB_ChannelWidth'] = _LOGIC_CLKoutSamp_And_Nand_NMOSB_ChannelWidth
		_Caculation_Parameters1['_LOGIC_CLKoutSamp_And_Nand_NMOSB_ChannelLength'] = _LOGIC_CLKoutSamp_And_Nand_NMOSB_ChannelLength
						# PMOSA
		_Caculation_Parameters1['_LOGIC_CLKoutSamp_And_Nand_PMOSA_NumberofGate'] = _LOGIC_CLKoutSamp_And_Nand_PMOSA_NumberofGate
		_Caculation_Parameters1['_LOGIC_CLKoutSamp_And_Nand_PMOSA_ChannelWidth'] = _LOGIC_CLKoutSamp_And_Nand_PMOSA_ChannelWidth
		_Caculation_Parameters1['_LOGIC_CLKoutSamp_And_Nand_PMOSA_ChannelLength'] = _LOGIC_CLKoutSamp_And_Nand_PMOSA_ChannelLength
						# PMOSB
		_Caculation_Parameters1['_LOGIC_CLKoutSamp_And_Nand_PMOSB_NumberofGate'] = _LOGIC_CLKoutSamp_And_Nand_PMOSB_NumberofGate
		_Caculation_Parameters1['_LOGIC_CLKoutSamp_And_Nand_PMOSB_ChannelWidth'] = _LOGIC_CLKoutSamp_And_Nand_PMOSB_ChannelWidth
		_Caculation_Parameters1['_LOGIC_CLKoutSamp_And_Nand_PMOSB_ChannelLength'] = _LOGIC_CLKoutSamp_And_Nand_PMOSB_ChannelLength
					## Inverter
						# Nmos
		_Caculation_Parameters1['_LOGIC_CLKoutSamp_And_Inv_NMOS_NumberofGate'] = _LOGIC_CLKoutSamp_And_Inv_NMOS_NumberofGate
		_Caculation_Parameters1['_LOGIC_CLKoutSamp_And_Inv_NMOS_ChannelWidth'] = _LOGIC_CLKoutSamp_And_Inv_NMOS_ChannelWidth
		_Caculation_Parameters1['_LOGIC_CLKoutSamp_And_Inv_NMOS_ChannelLength'] = _LOGIC_CLKoutSamp_And_Inv_NMOS_ChannelLength
						# Pmos
		_Caculation_Parameters1['_LOGIC_CLKoutSamp_And_Inv_PMOS_NumberofGate'] = _LOGIC_CLKoutSamp_And_Inv_PMOS_NumberofGate
		_Caculation_Parameters1['_LOGIC_CLKoutSamp_And_Inv_PMOS_ChannelWidth'] = _LOGIC_CLKoutSamp_And_Inv_PMOS_ChannelWidth
		_Caculation_Parameters1['_LOGIC_CLKoutSamp_And_Inv_PMOS_ChannelLength'] = _LOGIC_CLKoutSamp_And_Inv_PMOS_ChannelLength

		## Comparator
			## StrongARM Latch
				# Common
		_Caculation_Parameters1['_COMP_SALatch_ChannelLength'] = _COMP_SALatch_ChannelLength
		_Caculation_Parameters1['_COMP_SALatch_XVT'] = _COMP_SALatch_XVT
				# PMOS
		_Caculation_Parameters1['_COMP_SALatch_CLKinputPMOSFinger1'] = _COMP_SALatch_CLKinputPMOSFinger1
		_Caculation_Parameters1['_COMP_SALatch_CLKinputPMOSFinger2'] = _COMP_SALatch_CLKinputPMOSFinger2
		_Caculation_Parameters1['_COMP_SALatch_PMOSFinger'] = _COMP_SALatch_PMOSFinger
		_Caculation_Parameters1['_COMP_SALatch_PMOSChannelWidth'] = _COMP_SALatch_PMOSChannelWidth
				# NMOS
		_Caculation_Parameters1['_COMP_SALatch_DATAinputNMOSFinger'] = _COMP_SALatch_DATAinputNMOSFinger
		_Caculation_Parameters1['_COMP_SALatch_NMOSFinger'] = _COMP_SALatch_NMOSFinger
		_Caculation_Parameters1['_COMP_SALatch_CLKinputNMOSFinger'] = _COMP_SALatch_CLKinputNMOSFinger
		_Caculation_Parameters1['_COMP_SALatch_NMOSChannelWidth'] = _COMP_SALatch_NMOSChannelWidth
		_Caculation_Parameters1['_COMP_SALatch_CLKinputNMOSChannelWidth'] = _COMP_SALatch_CLKinputNMOSChannelWidth
			## StrongArmOutBuffer and SRLatch
				## Common
					# XVT
		_Caculation_Parameters1['_COMP_SAOutBufAndSRLatch_XVT'] = _COMP_SAOutBufAndSRLatch_XVT
					# Body
		_Caculation_Parameters1['_COMP_SAOutBufAndSRLatch_NMOS_Pbody_XvtTop2Pbody'] = _COMP_SAOutBufAndSRLatch_NMOS_Pbody_XvtTop2Pbody
		_Caculation_Parameters1['_COMP_SAOutBufAndSRLatch_PMOS_Nbody_Xvtdown2Nbody'] = _COMP_SAOutBufAndSRLatch_PMOS_Nbody_Xvtdown2Nbody
					# Height
		_Caculation_Parameters1['_COMP_SAOutBufAndSRLatch_PMOSXvt2NMOSXvt'] = _COMP_SAOutBufAndSRLatch_PMOSXvt2NMOSXvt
				## StronArm Output Buffer
					## Inverter1(pre)
						# Nmos
		_Caculation_Parameters1['_COMP_SAOutBuf_Buf_Inv1_NMOS_NumberofGate'] = _COMP_SAOutBuf_Buf_Inv1_NMOS_NumberofGate
		_Caculation_Parameters1['_COMP_SAOutBuf_Buf_Inv1_NMOS_ChannelWidth'] = _COMP_SAOutBuf_Buf_Inv1_NMOS_ChannelWidth
		_Caculation_Parameters1['_COMP_SAOutBuf_Buf_Inv1_NMOS_ChannelLength'] = _COMP_SAOutBuf_Buf_Inv1_NMOS_ChannelLength
						# Pmos
		_Caculation_Parameters1['_COMP_SAOutBuf_Buf_Inv1_PMOS_NumberofGate'] = _COMP_SAOutBuf_Buf_Inv1_PMOS_NumberofGate
		_Caculation_Parameters1['_COMP_SAOutBuf_Buf_Inv1_PMOS_ChannelWidth'] = _COMP_SAOutBuf_Buf_Inv1_PMOS_ChannelWidth
		_Caculation_Parameters1['_COMP_SAOutBuf_Buf_Inv1_PMOS_ChannelLength'] = _COMP_SAOutBuf_Buf_Inv1_PMOS_ChannelLength
					## Inverter2
						# Nmos
		_Caculation_Parameters1['_COMP_SAOutBuf_Buf_Inv2_NMOS_NumberofGate'] = _COMP_SAOutBuf_Buf_Inv2_NMOS_NumberofGate
		_Caculation_Parameters1['_COMP_SAOutBuf_Buf_Inv2_NMOS_ChannelWidth'] = _COMP_SAOutBuf_Buf_Inv2_NMOS_ChannelWidth
		_Caculation_Parameters1['_COMP_SAOutBuf_Buf_Inv2_NMOS_ChannelLength'] = _COMP_SAOutBuf_Buf_Inv2_NMOS_ChannelLength
						# Pmos
		_Caculation_Parameters1['_COMP_SAOutBuf_Buf_Inv2_PMOS_NumberofGate'] = _COMP_SAOutBuf_Buf_Inv2_PMOS_NumberofGate
		_Caculation_Parameters1['_COMP_SAOutBuf_Buf_Inv2_PMOS_ChannelWidth'] = _COMP_SAOutBuf_Buf_Inv2_PMOS_ChannelWidth
		_Caculation_Parameters1['_COMP_SAOutBuf_Buf_Inv2_PMOS_ChannelLength'] = _COMP_SAOutBuf_Buf_Inv2_PMOS_ChannelLength
				## SRLatch
					## Nand(Set,Rst same)
						# NmosA
		_Caculation_Parameters1['_COMP_SRLatch_Nand_NMOSA_NumberofGate'] = _COMP_SRLatch_Nand_NMOSA_NumberofGate
		_Caculation_Parameters1['_COMP_SRLatch_Nand_NMOSA_ChannelWidth'] = _COMP_SRLatch_Nand_NMOSA_ChannelWidth
		_Caculation_Parameters1['_COMP_SRLatch_Nand_NMOSA_ChannelLength'] = _COMP_SRLatch_Nand_NMOSA_ChannelLength
						# NMOSB
		_Caculation_Parameters1['_COMP_SRLatch_Nand_NMOSB_NumberofGate'] = _COMP_SRLatch_Nand_NMOSB_NumberofGate
		_Caculation_Parameters1['_COMP_SRLatch_Nand_NMOSB_ChannelWidth'] = _COMP_SRLatch_Nand_NMOSB_ChannelWidth
		_Caculation_Parameters1['_COMP_SRLatch_Nand_NMOSB_ChannelLength'] = _COMP_SRLatch_Nand_NMOSB_ChannelLength
						# PMOSA
		_Caculation_Parameters1['_COMP_SRLatch_Nand_PMOSA_NumberofGate'] = _COMP_SRLatch_Nand_PMOSA_NumberofGate
		_Caculation_Parameters1['_COMP_SRLatch_Nand_PMOSA_ChannelWidth'] = _COMP_SRLatch_Nand_PMOSA_ChannelWidth
		_Caculation_Parameters1['_COMP_SRLatch_Nand_PMOSA_ChannelLength'] = _COMP_SRLatch_Nand_PMOSA_ChannelLength
						# PMOSB
		_Caculation_Parameters1['_COMP_SRLatch_Nand_PMOSB_NumberofGate'] = _COMP_SRLatch_Nand_PMOSB_NumberofGate
		_Caculation_Parameters1['_COMP_SRLatch_Nand_PMOSB_ChannelWidth'] = _COMP_SRLatch_Nand_PMOSB_ChannelWidth
		_Caculation_Parameters1['_COMP_SRLatch_Nand_PMOSB_ChannelLength'] = _COMP_SRLatch_Nand_PMOSB_ChannelLength
			## Comp clock Gen Logic: Clk_Samp Inv, Clk_Source Inv, AND Gate, CompClockBuff
				## Common
					# XVT
		_Caculation_Parameters1['_COMP_CompClkLogic_XVT'] = _COMP_CompClkLogic_XVT
					# Body
		_Caculation_Parameters1['_COMP_CompClkLogic_NMOS_Pbody_XvtTop2Pbody'] = _COMP_CompClkLogic_NMOS_Pbody_XvtTop2Pbody
		_Caculation_Parameters1['_COMP_CompClkLogic_PMOS_Nbody_Xvtdown2Nbody'] = _COMP_CompClkLogic_PMOS_Nbody_Xvtdown2Nbody
					# Height
		_Caculation_Parameters1['_COMP_CompClkLogic_PMOSXvt2NMOSXvt'] = _COMP_CompClkLogic_PMOSXvt2NMOSXvt
				## StronArm Output Buffer
					## Inverter1(pre)
						#Nmos
		_Caculation_Parameters1['_COMP_CompClkLogic_Buf_Inv1_NMOS_NumberofGate'] = _COMP_CompClkLogic_Buf_Inv1_NMOS_NumberofGate
		_Caculation_Parameters1['_COMP_CompClkLogic_Buf_Inv1_NMOS_ChannelWidth'] = _COMP_CompClkLogic_Buf_Inv1_NMOS_ChannelWidth
		_Caculation_Parameters1['_COMP_CompClkLogic_Buf_Inv1_NMOS_ChannelLength'] = _COMP_CompClkLogic_Buf_Inv1_NMOS_ChannelLength
						# Pmos
		_Caculation_Parameters1['_COMP_CompClkLogic_Buf_Inv1_PMOS_NumberofGate'] = _COMP_CompClkLogic_Buf_Inv1_PMOS_NumberofGate
		_Caculation_Parameters1['_COMP_CompClkLogic_Buf_Inv1_PMOS_ChannelWidth'] = _COMP_CompClkLogic_Buf_Inv1_PMOS_ChannelWidth
		_Caculation_Parameters1['_COMP_CompClkLogic_Buf_Inv1_PMOS_ChannelLength'] = _COMP_CompClkLogic_Buf_Inv1_PMOS_ChannelLength
					## Inverter2
						# Nmos
		_Caculation_Parameters1['_COMP_CompClkLogic_Buf_Inv2_NMOS_NumberofGate'] = _COMP_CompClkLogic_Buf_Inv2_NMOS_NumberofGate
		_Caculation_Parameters1['_COMP_CompClkLogic_Buf_Inv2_NMOS_ChannelWidth'] = _COMP_CompClkLogic_Buf_Inv2_NMOS_ChannelWidth
		_Caculation_Parameters1['_COMP_CompClkLogic_Buf_Inv2_NMOS_ChannelLength'] = _COMP_CompClkLogic_Buf_Inv2_NMOS_ChannelLength
						# Pmos
		_Caculation_Parameters1['_COMP_CompClkLogic_Buf_Inv2_PMOS_NumberofGate'] = _COMP_CompClkLogic_Buf_Inv2_PMOS_NumberofGate
		_Caculation_Parameters1['_COMP_CompClkLogic_Buf_Inv2_PMOS_ChannelWidth'] = _COMP_CompClkLogic_Buf_Inv2_PMOS_ChannelWidth
		_Caculation_Parameters1['_COMP_CompClkLogic_Buf_Inv2_PMOS_ChannelLength'] = _COMP_CompClkLogic_Buf_Inv2_PMOS_ChannelLength
				## AND
					## Nand
						# NmosA
		_Caculation_Parameters1['_COMP_CompClkLogic_Nand_NMOSA_NumberofGate'] = _COMP_CompClkLogic_Nand_NMOSA_NumberofGate
		_Caculation_Parameters1['_COMP_CompClkLogic_Nand_NMOSA_ChannelWidth'] = _COMP_CompClkLogic_Nand_NMOSA_ChannelWidth
		_Caculation_Parameters1['_COMP_CompClkLogic_Nand_NMOSA_ChannelLength'] = _COMP_CompClkLogic_Nand_NMOSA_ChannelLength
						# NMOSB
		_Caculation_Parameters1['_COMP_CompClkLogic_Nand_NMOSB_NumberofGate'] = _COMP_CompClkLogic_Nand_NMOSB_NumberofGate
		_Caculation_Parameters1['_COMP_CompClkLogic_Nand_NMOSB_ChannelWidth'] = _COMP_CompClkLogic_Nand_NMOSB_ChannelWidth
		_Caculation_Parameters1['_COMP_CompClkLogic_Nand_NMOSB_ChannelLength'] = _COMP_CompClkLogic_Nand_NMOSB_ChannelLength
						# PMOSA
		_Caculation_Parameters1['_COMP_CompClkLogic_Nand_PMOSA_NumberofGate'] = _COMP_CompClkLogic_Nand_PMOSA_NumberofGate
		_Caculation_Parameters1['_COMP_CompClkLogic_Nand_PMOSA_ChannelWidth'] = _COMP_CompClkLogic_Nand_PMOSA_ChannelWidth
		_Caculation_Parameters1['_COMP_CompClkLogic_Nand_PMOSA_ChannelLength'] = _COMP_CompClkLogic_Nand_PMOSA_ChannelLength
						# PMOSB
		_Caculation_Parameters1['_COMP_CompClkLogic_Nand_PMOSB_NumberofGate'] = _COMP_CompClkLogic_Nand_PMOSB_NumberofGate
		_Caculation_Parameters1['_COMP_CompClkLogic_Nand_PMOSB_ChannelWidth'] = _COMP_CompClkLogic_Nand_PMOSB_ChannelWidth
		_Caculation_Parameters1['_COMP_CompClkLogic_Nand_PMOSB_ChannelLength'] = _COMP_CompClkLogic_Nand_PMOSB_ChannelLength
					## Inverter
						# Nmos
		_Caculation_Parameters1['_COMP_CompClkLogic_Inv_NMOS_NumberofGate'] = _COMP_CompClkLogic_Inv_NMOS_NumberofGate
		_Caculation_Parameters1['_COMP_CompClkLogic_Inv_NMOS_ChannelWidth'] = _COMP_CompClkLogic_Inv_NMOS_ChannelWidth
		_Caculation_Parameters1['_COMP_CompClkLogic_Inv_NMOS_ChannelLength'] = _COMP_CompClkLogic_Inv_NMOS_ChannelLength
						# Pmos
		_Caculation_Parameters1['_COMP_CompClkLogic_Inv_PMOS_NumberofGate'] = _COMP_CompClkLogic_Inv_PMOS_NumberofGate
		_Caculation_Parameters1['_COMP_CompClkLogic_Inv_PMOS_ChannelWidth'] = _COMP_CompClkLogic_Inv_PMOS_ChannelWidth
		_Caculation_Parameters1['_COMP_CompClkLogic_Inv_PMOS_ChannelLength'] = _COMP_CompClkLogic_Inv_PMOS_ChannelLength
				## Clk_Source Inv
						# Nmos
		_Caculation_Parameters1['_COMP_CompClkLogic_ClkSrc_NMOS_NumberofGate'] = _COMP_CompClkLogic_ClkSrc_NMOS_NumberofGate
		_Caculation_Parameters1['_COMP_CompClkLogic_ClkSrc_NMOS_ChannelWidth'] = _COMP_CompClkLogic_ClkSrc_NMOS_ChannelWidth
		_Caculation_Parameters1['_COMP_CompClkLogic_ClkSrc_NMOS_ChannelLength'] = _COMP_CompClkLogic_ClkSrc_NMOS_ChannelLength
						# Pmos
		_Caculation_Parameters1['_COMP_CompClkLogic_ClkSrc_PMOS_NumberofGate'] = _COMP_CompClkLogic_ClkSrc_PMOS_NumberofGate
		_Caculation_Parameters1['_COMP_CompClkLogic_ClkSrc_PMOS_ChannelWidth'] = _COMP_CompClkLogic_ClkSrc_PMOS_ChannelWidth
		_Caculation_Parameters1['_COMP_CompClkLogic_ClkSrc_PMOS_ChannelLength'] = _COMP_CompClkLogic_ClkSrc_PMOS_ChannelLength
				## Clk_Samp Inv
						#Nmos
		_Caculation_Parameters1['_COMP_CompClkLogic_ClkSmp_NMOS_NumberofGate'] = _COMP_CompClkLogic_ClkSmp_NMOS_NumberofGate
		_Caculation_Parameters1['_COMP_CompClkLogic_ClkSmp_NMOS_ChannelWidth'] = _COMP_CompClkLogic_ClkSmp_NMOS_ChannelWidth
		_Caculation_Parameters1['_COMP_CompClkLogic_ClkSmp_NMOS_ChannelLength'] = _COMP_CompClkLogic_ClkSmp_NMOS_ChannelLength
						# Pmos
		_Caculation_Parameters1['_COMP_CompClkLogic_ClkSmp_PMOS_NumberofGate'] = _COMP_CompClkLogic_ClkSmp_PMOS_NumberofGate
		_Caculation_Parameters1['_COMP_CompClkLogic_ClkSmp_PMOS_ChannelWidth'] = _COMP_CompClkLogic_ClkSmp_PMOS_ChannelWidth
		_Caculation_Parameters1['_COMP_CompClkLogic_ClkSmp_PMOS_ChannelLength'] = _COMP_CompClkLogic_ClkSmp_PMOS_ChannelLength

		## CLOCK AND DATA BUF : Comparator Dout Buf for driving Logic, CLKSamp and CLKScr Buff for Driving Sampler and Comparator
			## Top placed
				## CLK Samp
					## InvChain Common
						## Height
		_Caculation_Parameters1['_BUF_CLKSamp_PMOSXvt2NMOSXvt'] = _BUF_CLKSamp_PMOSXvt2NMOSXvt
					## Inverter Chain
						## Inv1 common
		_Caculation_Parameters1['_BUF_CLKSamp_XVT'] = _BUF_CLKSamp_XVT
		_Caculation_Parameters1['_BUF_CLKSamp_NumberofGate'] = _BUF_CLKSamp_NumberofGate
		_Caculation_Parameters1['_BUF_CLKSamp_ChanneLength'] = _BUF_CLKSamp_ChanneLength
						## NMOS
		_Caculation_Parameters1['_BUF_CLKSamp_NMOSChannelWidth'] = _BUF_CLKSamp_NMOSChannelWidth
						## PMOS
		_Caculation_Parameters1['_BUF_CLKSamp_PMOSChannelWidth'] = _BUF_CLKSamp_PMOSChannelWidth
				## CLK Scr
					## InvChain Common
						## Height
		_Caculation_Parameters1['_BUF_CLKScr_PMOSXvt2NMOSXvt'] = _BUF_CLKScr_PMOSXvt2NMOSXvt
					## Inverter Chain
						## Inv1 common
		_Caculation_Parameters1['_BUF_CLKScr_XVT'] = _BUF_CLKScr_XVT
		_Caculation_Parameters1['_BUF_CLKScr_NumberofGate'] = _BUF_CLKScr_NumberofGate
		_Caculation_Parameters1['_BUF_CLKScr_ChanneLength'] = _BUF_CLKScr_ChanneLength
						## NMOS
		_Caculation_Parameters1['_BUF_CLKScr_NMOSChannelWidth'] = _BUF_CLKScr_NMOSChannelWidth
						## PMOS
		_Caculation_Parameters1['_BUF_CLKScr_PMOSChannelWidth'] = _BUF_CLKScr_PMOSChannelWidth
			## Bottom Placed
				## CompOut
					## InvChain Common
						## Height
		_Caculation_Parameters1['_BUF_CompOut_PMOSXvt2NMOSXvt'] = _BUF_CompOut_PMOSXvt2NMOSXvt
					## Inverter Chain
						## Inv1 common
		_Caculation_Parameters1['_BUF_CompOut_XVT'] = _BUF_CompOut_XVT
		_Caculation_Parameters1['_BUF_CompOut_NumberofGate'] = _BUF_CompOut_NumberofGate
		_Caculation_Parameters1['_BUF_CompOut_ChanneLength'] = _BUF_CompOut_ChanneLength
						## NMOS
		_Caculation_Parameters1['_BUF_CompOut_NMOSChannelWidth'] = _BUF_CompOut_NMOSChannelWidth
						## PMOS
		_Caculation_Parameters1['_BUF_CompOut_PMOSChannelWidth'] = _BUF_CompOut_PMOSChannelWidth


		self._DesignParameter['SRF_SARLogicWtComparator'] = self._SrefElementDeclaration(_DesignObj=L00_SARLogicWtComparator_KJH._SARLogicWtComparator(_DesignParameter=None,_Name='{}:SRF_SARLogicWtComparator'.format(_Name)))[0]

		## Define Sref Reflection: ex)self._DesignParameter['_NMOS_POWER']['_Reflect'] = [0, 0, 0]
		self._DesignParameter['SRF_SARLogicWtComparator']['_Reflect'] = [0, 0, 0]

		## Define Sref Angle: ex)'_NMOS_POWER'
		self._DesignParameter['SRF_SARLogicWtComparator']['_Angle'] = 0

		## Calculate Sref Layer by using Calculation_Parameter: ex)'_NMOS_POWER'
		self._DesignParameter['SRF_SARLogicWtComparator']['_DesignObj']._CalculateDesignParameter(**_Caculation_Parameters1)

		## initialize Sref _XYcoordinate: ex)'_NMOS_POWER'
		self._DesignParameter['SRF_SARLogicWtComparator']['_XYCoordinates'] = [[0, 0]]

		###################################################################################################
		## Pre-Calculated centY coord
		# tmp = self.get_param_KJH4('SRF_SARLogicWtComparator','SRF_SARLogicWtBuffers','SRF_SARLogicWtCLKTree','SRF_SARLogic','BND_Nbody_M1Exten')
		# centY = tmp[0][0][0][0][0][0]['_XY_cent'][1]
		tmp1 = self.get_param_KJH4('SRF_SARLogicWtComparator', 'SRF_SARLogicWtBuffers', 'SRF_UpperCDACPreDriver', 'BND_Nbody_M1Exten')
		tmp1_2 = self.get_param_KJH4('SRF_SARLogicWtComparator', 'SRF_SARLogicWtBuffers', 'SRF_LowerCDACPreDriver', 'BND_Pbody_M1Exten')
		centY = int((tmp1[0][0][0][0][0]['_XY_cent'][1] + tmp1_2[0][0][0][0][0]['_XY_cent'][1]) / 2)
		###################################################################################################

		## CDAC (SREF) Generation
		## Copy Calculation_Parameters from low-level-block ex)copy.deepcopy(B16_nmos_power_v2._NMOS_POWER._ParametersForDesignCalculation)
		_Caculation_Parameters0 = copy.deepcopy(H06_00_CDACWtDriver._CDACWtDriver._ParametersForDesignCalculation)
		## Define Calculation_Parameters ex) _Caculation_Parameters['_NMOSPOWER_PbodyContact_1_Length']  = _NMOSPOWER_PbodyContact_1_Length
		_Caculation_Parameters0['_NumOfBits'] = _NumofCbit
		## CDAC
			## CDAC Configuration
		_Caculation_Parameters0['_CDAC_FoldingTF'] = _CDAC_FoldingTF
		_Caculation_Parameters0['_CDACDrv_ArrangedTF'] = _CDACDrv_ArrangedTF
			## CDAC Drv
				## Unit DRv
					## Common
						# XVT
		_Caculation_Parameters0['_CDACDrv_XVT'] = _CDACDrv_XVT
					## NMOS
		_Caculation_Parameters0['_CDACDrv_NMOS_NumberofGate'] = _CDACDrv_NMOS_NumberofGate
		_Caculation_Parameters0['_CDACDrv_NMOS_ChannelWidth'] = _CDACDrv_NMOS_ChannelWidth
		_Caculation_Parameters0['_CDACDrv_NMOS_ChannelLength'] = _CDACDrv_NMOS_ChannelLength
					## PMOS
		_Caculation_Parameters0['_CDACDrv_PMOS_NumberofGate'] = _CDACDrv_PMOS_NumberofGate
		_Caculation_Parameters0['_CDACDrv_PMOS_ChannelWidth'] = _CDACDrv_PMOS_ChannelWidth
		_Caculation_Parameters0['_CDACDrv_PMOS_ChannelLength'] = _CDACDrv_PMOS_ChannelLength
				## Option1: decimation
		_Caculation_Parameters0['_CDACDrv_Decimation_Factor'] = _CDACDrv_Decimation_Factor
				## Option(Arragned Only, _CDACDrv_ArrangedTF = 'True')
		_Caculation_Parameters0['_CDACDrv_DesignatedEachSize'] = _CDACDrv_DesignatedEachSize
			## CDAC
				## Element CDAC
		_Caculation_Parameters0['_CDAC_LayoutOption'] = _CDAC_LayoutOption
		_Caculation_Parameters0['_CDAC_MetalWidth'] = _CDAC_MetalWidth
		_Caculation_Parameters0['_CDAC_MetalLength'] = _CDAC_MetalLength
		_Caculation_Parameters0['_CDAC_MetalSpacing'] = _CDAC_MetalSpacing
				## Unit Cap
		_Caculation_Parameters0['_CDAC_NumOfElement'] = _CDAC_NumOfElement
				## Shield
		_Caculation_Parameters0['_CDAC_ShieldingLayer'] = _CDAC_ShieldingLayer
		_Caculation_Parameters0['_CDAC_ConnectLength'] = _CDAC_ConnectLength
		_Caculation_Parameters0['_CDAC_ExtendLength'] = _CDAC_ExtendLength
				## Dummy Cap Option
		_Caculation_Parameters0['_CDAC_NumOfDummyCaps'] = _CDAC_NumOfDummyCaps
		_Caculation_Parameters0['_CDAC_DummyCap_TopBottomShort'] = _CDAC_DummyCap_TopBottomShort
				## CommonCentroid With Driving node
		_Caculation_Parameters0['_CDAC_CapArrayWDrivingNodeDistance'] = _CDAC_CapArrayWDrivingNodeDistance
		_Caculation_Parameters0['_CDAC_DriveNodeDistance'] = _CDAC_DriveNodeDistance
		_Caculation_Parameters0['_CDAC_YWidth_Bottom_Hrz'] = _CDAC_YWidth_Bottom_Hrz
		_Caculation_Parameters0['_CDAC_BotNodeVtcExtensionMetalLayer'] = _CDAC_BotNodeVtcExtensionMetalLayer

		## CDAC (Positive)
		self._DesignParameter['SRF_CDAC_Pos'] = self._SrefElementDeclaration(_DesignObj=H06_00_CDACWtDriver._CDACWtDriver(_DesignParameter=None, _Name='{}:SRF_CDAC_Pos'.format(_Name)))[0]

		## Define Sref Reflection: ex)self._DesignParameter['_NMOS_POWER']['_Reflect'] = [0, 0, 0]
		self._DesignParameter['SRF_CDAC_Pos']['_Reflect'] = [0, 0, 0]

		## Define Sref Angle: ex)'_NMOS_POWER'
		self._DesignParameter['SRF_CDAC_Pos']['_Angle'] = 0

		## Calculate Sref Layer by using Calculation_Parameter: ex)'_NMOS_POWER'
		self._DesignParameter['SRF_CDAC_Pos']['_DesignObj']._CalculateDesignParameter(**_Caculation_Parameters0)

		## initialize Sref _XYcoordinate: ex)'_NMOS_POWER'
		self._DesignParameter['SRF_CDAC_Pos']['_XYCoordinates'] = [[0, 0]]
		## Calculate Sref XYcoord
		tmpXY = []
		## Calculate
		## Target_coord: _XY_type1
		## Define Boundary_element _XWidth
		self._DesignParameter['SRF_SARLogicWtComparator']['_DesignObj']._DesignParameter['SRF_Comparator']['_DesignObj']._DesignParameter['SRF_Slicer']['_DesignObj']._DesignParameter['_Guardring']['_Reflect'] = [0, 0, 0]
		self._DesignParameter['SRF_SARLogicWtComparator']['_DesignObj']._DesignParameter['SRF_Comparator']['_DesignObj']._DesignParameter['SRF_Slicer']['_DesignObj']._DesignParameter['_Guardring']['_Angle'] = 0
		tmp1x = self.get_param_KJH3('SRF_SARLogicWtComparator', 'SRF_Comparator', 'SRF_Slicer', '_Guardring', '_Met1Layerx')
		tmp1y = self.get_param_KJH4('SRF_SARLogicWtComparator', 'SRF_Buf_CLKSamp', 'SRF_Pbody', 'SRF_PbodyContactPhyLen', 'BND_Met1Layer')
		target_coord = [tmp1x[0][0][0][0][0][0]['_XY_left'][0], tmp1y[0][0][0][0][0][0]['_XY_down'][1]]
		## Approaching_coord: _XY_type2
		if _CDAC_FoldingTF == True:
			if _CDACDrv_ArrangedTF == False:
				tmp2x = self.get_param_KJH4('SRF_CDAC_Pos','SRF_CDACWtDriver', 'BND_CDACFold1_B{}_DrvInput_Vtc_M2'.format(_NumofCbit - 1))
			else:
				tmp2x = self.get_param_KJH4('SRF_CDAC_Pos','SRF_CDACWtDriver','BND_CDACFold1_B{}_DrvOutput_Vtc_M2'.format(_NumofCbit - 1))
			# tmp2y = self.get_param_KJH4('SRF_CDAC_Pos', 'SRF_CDAC_LowerHalf', 'SRF_DriverArray', 'BND_{}C_Driver_Input_Hrz_M3'.format(1))
			tmp2y_1 = self.get_param_KJH4('SRF_CDAC_Pos', 'SRF_CDACWtDriver','BND_CDACFold1_{}B{}_DrvInput_Hrz_M3'.format('Lo', 0))
			# approaching_coord = [tmp2x[0][0][0]['_XY_left'][0], tmp2y[0][0][0][0][0]['_XY_down'][1]]
			approaching_coord = [tmp2x[0][0][0][0]['_XY_left'][0], tmp2y_1[0][0][0][0]['_XY_down'][1]]
		else:
			tmp2x = self.get_param_KJH4('SRF_CDAC_Pos', 'SRF_CDACWtDriver','BND_CDACTopNode_Hrz_M7')
			tmp2y = self.get_param_KJH4('SRF_CDAC_Pos', 'SRF_CDACWtDriver','SRF_CDACWtDriver', 'SRF_DriverArray', 'BND_{}C_Driver_Input_Hrz_M3'.format(1))
			approaching_coord = [tmp2x[0][0][0][0]['_XY_left'][0], tmp2y[0][0][0][0][0][0]['_XY_down'][1]]
			## Sref coord
		tmp3 = self.get_param_KJH4('SRF_CDAC_Pos')
		Scoord = tmp3[0][0]['_XY_origin']
		XOffset = 2000
		YOffset = 100
		Scoord[0] = Scoord[0] + XOffset
		Scoord[1] = Scoord[1] + YOffset
		## Cal
		New_Scoord = self.get_Scoord_KJH4(target_coord, approaching_coord, Scoord)
		tmpXY.append(New_Scoord)
		## Define coordinates
		self._DesignParameter['SRF_CDAC_Pos']['_XYCoordinates'] = tmpXY
		###################################################################################################

		## Calculate Sref Layer by using Calculation_Parameter: ex)'_NMOS_POWER'
		# self._DesignParameter['SRF_CDAC_Neg']['_DesignObj']._CalculateDesignParameter(**_Caculation_Parameters0) #erase for 시간단축
		self._DesignParameter['SRF_CDAC_Neg'] = copy.deepcopy(self._DesignParameter['SRF_CDAC_Pos'])
		self.rename_srf_prefix(self._DesignParameter['SRF_CDAC_Neg'], 'SRF_CDAC_Pos', 'SRF_CDAC_Neg')

		## Define Sref Reflection: ex)self._DesignParameter['_NMOS_POWER']['_Reflect'] = [0, 0, 0]
		self._DesignParameter['SRF_CDAC_Neg']['_Reflect'] = [1, 0, 0]

		## Define Sref Angle: ex)'_NMOS_POWER'
		self._DesignParameter['SRF_CDAC_Neg']['_Angle'] = 0

		## initialize Sref _XYcoordinate: ex)'_NMOS_POWER'
		self._DesignParameter['SRF_CDAC_Neg']['_XYCoordinates'] = [[0, 0]]

		## Calculate Sref XYcoord
		tmpXY = []
		## Calculate
		## Target_coord: _XY_type1
		tmp1x = self.get_param_KJH3('SRF_SARLogicWtComparator', 'SRF_Comparator', 'SRF_Slicer', '_Guardring', '_Met1Layerx')
		tmp1y = self.get_param_KJH4('SRF_SARLogicWtComparator', 'SRF_Buf_CompOut', 'SRF_Nbody', 'SRF_NbodyContactPhyLen', 'BND_Met1Layer')
		target_coord = [tmp1x[0][0][0][0][0][0]['_XY_left'][0], tmp1y[0][0][0][0][0][0]['_XY_up'][1]]
		## Approaching_coord: _XY_type2
		if _CDAC_FoldingTF == True:
			if _CDACDrv_ArrangedTF == False:
				tmp2x = self.get_param_KJH4('SRF_CDAC_Neg','SRF_CDACWtDriver', 'BND_CDACFold1_B{}_DrvInput_Vtc_M2'.format(_NumofCbit - 1))
			else:
				tmp2x = self.get_param_KJH4('SRF_CDAC_Neg','SRF_CDACWtDriver', 'BND_CDACFold1_B{}_DrvOutput_Vtc_M2'.format(_NumofCbit - 1))
			# tmp2y = self.get_param_KJH4('SRF_CDAC_Neg', 'SRF_CDAC_LowerHalf','SRF_DriverArray', 'BND_{}C_Driver_Input_Hrz_M3'.format(1))
			tmp2y_1 = self.get_param_KJH4('SRF_CDAC_Neg','SRF_CDACWtDriver', 'BND_CDACFold1_{}B{}_DrvInput_Hrz_M3'.format('Lo', 0))
			# approaching_coord = [tmp2x[0][0][0]['_XY_left'][0], tmp2y[0][0][0][0][0]['_XY_down'][1]]
			approaching_coord = [tmp2x[0][0][0][0]['_XY_left'][0], tmp2y_1[0][0][0][0]['_XY_down'][1]]
		else:
			tmp2x = self.get_param_KJH4('SRF_CDAC_Neg', 'SRF_CDACWtDriver','BND_CDACTopNode_Hrz_M7')
			tmp2y = self.get_param_KJH4('SRF_CDAC_Neg', 'SRF_CDACWtDriver','SRF_CDACWtDriver', 'SRF_DriverArray', 'BND_{}C_Driver_Input_Hrz_M3'.format(1))
			approaching_coord = [tmp2x[0][0][0][0]['_XY_left'][0], tmp2y[0][0][0][0][0][0]['_XY_down'][1]]
			## Sref coord
		tmp3 = self.get_param_KJH4('SRF_CDAC_Neg')
		Scoord = tmp3[0][0]['_XY_origin']
		XOffset = 2000
		YOffset = -100
		Scoord[0] = Scoord[0] + XOffset
		Scoord[1] = Scoord[1] + YOffset
		## Cal
		New_Scoord = self.get_Scoord_KJH4(target_coord, approaching_coord, Scoord)
		tmpXY.append(New_Scoord)
		## Define coordinates
		self._DesignParameter['SRF_CDAC_Neg']['_XYCoordinates'] = tmpXY
		###################################################################################################

		############ BootSW Generation
		## Bootstrap Sampler SREF Generation
		## Copy Calculation_Parameters from low-level-block ex)copy.deepcopy(B16_nmos_power_v2._NMOS_POWER._ParametersForDesignCalculation)
		_Caculation_Parameters = copy.deepcopy(C13_01_CtopCbotRouted_YJ_v01_00._CtopCbotRouted._ParametersForDesignCalculation)
		## Bootstrapped Switch
			# Input/Output node
				# INPUT node
		_Caculation_Parameters['_Sampler_Inputnode_width'] = _Sampler_Inputnode_width
				# OUTPUT node
		_Caculation_Parameters['_Sampler_Outputnode_width'] = _Sampler_Outputnode_width
			# TR1
				# Physical dimension
		_Caculation_Parameters['_Sampler_Tr1_NumberofGate'] = _Sampler_Tr1_NumberofGate
		_Caculation_Parameters['_Sampler_Tr1_ChannelWidth'] = _Sampler_Tr1_ChannelWidth
		_Caculation_Parameters['_Sampler_Tr1_ChannelLength'] = _Sampler_Tr1_ChannelLength
		_Caculation_Parameters['_Sampler_Tr1_XVT'] = _Sampler_Tr1_XVT
			# TR2
				# Physical dimension
		_Caculation_Parameters['_Sampler_Tr2_NumberofGate'] = _Sampler_Tr2_NumberofGate
		_Caculation_Parameters['_Sampler_Tr2_ChannelWidth'] = _Sampler_Tr2_ChannelWidth
		_Caculation_Parameters['_Sampler_Tr2_ChannelLength'] = _Sampler_Tr2_ChannelLength
		_Caculation_Parameters['_Sampler_Tr2_XVT'] = _Sampler_Tr2_XVT
			# TR4
				# Physical dimension
		_Caculation_Parameters['_Sampler_Tr4_NumberofGate'] = _Sampler_Tr4_NumberofGate
		_Caculation_Parameters['_Sampler_Tr4_ChannelWidth'] = _Sampler_Tr4_ChannelWidth
		_Caculation_Parameters['_Sampler_Tr4_ChannelLength'] = _Sampler_Tr4_ChannelLength
		_Caculation_Parameters['_Sampler_Tr4_XVT'] = _Sampler_Tr4_XVT
			# TR5
				# Physical dimension
		_Caculation_Parameters['_Sampler_Tr5_NumberofGate'] = _Sampler_Tr5_NumberofGate
		_Caculation_Parameters['_Sampler_Tr5_ChannelWidth'] = _Sampler_Tr5_ChannelWidth
		_Caculation_Parameters['_Sampler_Tr5_ChannelLength'] = _Sampler_Tr5_ChannelLength
		_Caculation_Parameters['_Sampler_Tr5_XVT'] = _Sampler_Tr5_XVT
			# TR7
				# Physical dimension
		_Caculation_Parameters['_Sampler_Tr7_NumberofGate'] = _Sampler_Tr7_NumberofGate
		_Caculation_Parameters['_Sampler_Tr7_ChannelWidth'] = _Sampler_Tr7_ChannelWidth
		_Caculation_Parameters['_Sampler_Tr7_ChannelLength'] = _Sampler_Tr7_ChannelLength
		_Caculation_Parameters['_Sampler_Tr7_XVT'] = _Sampler_Tr7_XVT
			# TR9
				# Physical dimension
		_Caculation_Parameters['_Sampler_Tr9_NumberofGate'] = _Sampler_Tr9_NumberofGate
		_Caculation_Parameters['_Sampler_Tr9_ChannelWidth'] = _Sampler_Tr9_ChannelWidth
		_Caculation_Parameters['_Sampler_Tr9_ChannelLength'] = _Sampler_Tr9_ChannelLength
		_Caculation_Parameters['_Sampler_Tr9_XVT'] = _Sampler_Tr9_XVT
			# TR8
				# Physical dimension
		_Caculation_Parameters['_Sampler_Tr8_NumberofGate'] = _Sampler_Tr8_NumberofGate
		_Caculation_Parameters['_Sampler_Tr8_ChannelWidth'] = _Sampler_Tr8_ChannelWidth
		_Caculation_Parameters['_Sampler_Tr8_ChannelLength'] = _Sampler_Tr8_ChannelLength
		_Caculation_Parameters['_Sampler_Tr8_XVT'] = _Sampler_Tr8_XVT
			# TR6
				# Physical dimension
		_Caculation_Parameters['_Sampler_Tr6_NumberofGate'] = _Sampler_Tr6_NumberofGate
		_Caculation_Parameters['_Sampler_Tr6_ChannelWidth'] = _Sampler_Tr6_ChannelWidth
		_Caculation_Parameters['_Sampler_Tr6_ChannelLength'] = _Sampler_Tr6_ChannelLength
		_Caculation_Parameters['_Sampler_Tr6_XVT'] = _Sampler_Tr6_XVT
			# TR11
				# Physical dimension
		_Caculation_Parameters['_Sampler_Tr11_NumberofGate'] = _Sampler_Tr11_NumberofGate
		_Caculation_Parameters['_Sampler_Tr11_ChannelWidth'] = _Sampler_Tr11_ChannelWidth
		_Caculation_Parameters['_Sampler_Tr11_ChannelLength'] = _Sampler_Tr11_ChannelLength
		_Caculation_Parameters['_Sampler_Tr11_XVT'] = _Sampler_Tr11_XVT
			# Tie4N
				# Physical dimension
		_Caculation_Parameters['_Sampler_Tie4N_NumberofGate'] = _Sampler_Tie4N_NumberofGate
		_Caculation_Parameters['_Sampler_Tie4N_ChannelWidth'] = _Sampler_Tie4N_ChannelWidth
		_Caculation_Parameters['_Sampler_Tie4N_ChannelLength'] = _Sampler_Tie4N_ChannelLength
		_Caculation_Parameters['_Sampler_Tie4N_XVT'] = _Sampler_Tie4N_XVT
			# Tie4P
				# Physical dimension
		_Caculation_Parameters['_Sampler_Tie4P_NumberofGate'] = _Sampler_Tie4P_NumberofGate
		_Caculation_Parameters['_Sampler_Tie4P_ChannelWidth'] = _Sampler_Tie4P_ChannelWidth
		_Caculation_Parameters['_Sampler_Tie4P_ChannelLength'] = _Sampler_Tie4P_ChannelLength
		_Caculation_Parameters['_Sampler_Tie4P_XVT'] = _Sampler_Tie4P_XVT
			# Tie8N
				# Physical dimension
		_Caculation_Parameters['_Sampler_Tie8N_NumberofGate'] = _Sampler_Tie8N_NumberofGate
		_Caculation_Parameters['_Sampler_Tie8N_ChannelWidth'] = _Sampler_Tie8N_ChannelWidth
		_Caculation_Parameters['_Sampler_Tie8N_ChannelLength'] = _Sampler_Tie8N_ChannelLength
		_Caculation_Parameters['_Sampler_Tie8N_XVT'] = _Sampler_Tie8N_XVT
			# Tie8P
				# Physical dimension
		_Caculation_Parameters['_Sampler_Tie8P_NumberofGate'] = _Sampler_Tie8P_NumberofGate
		_Caculation_Parameters['_Sampler_Tie8P_ChannelWidth'] = _Sampler_Tie8P_ChannelWidth
		_Caculation_Parameters['_Sampler_Tie8P_ChannelLength'] = _Sampler_Tie8P_ChannelLength
		_Caculation_Parameters['_Sampler_Tie8P_XVT'] = _Sampler_Tie8P_XVT
			# TR12
				# Physical dimension
		_Caculation_Parameters['_Sampler_Tr12_NumberofGate'] = _Sampler_Tr12_NumberofGate
		_Caculation_Parameters['_Sampler_Tr12_ChannelWidth'] = _Sampler_Tr12_ChannelWidth
		_Caculation_Parameters['_Sampler_Tr12_ChannelLength'] = _Sampler_Tr12_ChannelLength
		_Caculation_Parameters['_Sampler_Tr12_XVT'] = _Sampler_Tr12_XVT
			# TR3
				# Physical dimension
		_Caculation_Parameters['_Sampler_Tr3_NumberofGate'] = _Sampler_Tr3_NumberofGate
		_Caculation_Parameters['_Sampler_Tr3_ChannelWidth'] = _Sampler_Tr3_ChannelWidth
		_Caculation_Parameters['_Sampler_Tr3_ChannelLength'] = _Sampler_Tr3_ChannelLength
		_Caculation_Parameters['_Sampler_Tr3_XVT'] = _Sampler_Tr3_XVT
			# TR10
				# Physical dimension
		_Caculation_Parameters['_Sampler_Tr10_NumberofGate'] = _Sampler_Tr10_NumberofGate
		_Caculation_Parameters['_Sampler_Tr10_ChannelWidth'] = _Sampler_Tr10_ChannelWidth
		_Caculation_Parameters['_Sampler_Tr10_ChannelLength'] = _Sampler_Tr10_ChannelLength
		_Caculation_Parameters['_Sampler_Tr10_XVT'] = _Sampler_Tr10_XVT
			# HDVNCAP
		_Caculation_Parameters['_Sampler_HDVNCAP_Length'] = _Sampler_HDVNCAP_Length
		_Caculation_Parameters['_Sampler_HDVNCAP_LayoutOption'] = _Sampler_HDVNCAP_LayoutOption
		_Caculation_Parameters['_Sampler_HDVNCAP_NumFigPair'] = _Sampler_HDVNCAP_NumFigPair

		_Caculation_Parameters['_Sampler_HDVNCAP_Array'] = _Sampler_HDVNCAP_Array
		_Caculation_Parameters['_Sampler_HDVNCAP_Cbot_Ctop_metalwidth'] = _Sampler_HDVNCAP_Cbot_Ctop_metalwidth

		## BootSW (Positive) Placement
		## Generate Sref: ex)self._DesignParameter['_NMOS_POWER'] = self._SrefElementDeclaration(_DesignObj=B16_nmos_power_v2._NMOS_POWER( _DesignParameter=None, _Name='{}:NMOS_POWER'.format(_Name)))[0]
		self._DesignParameter['SRF_BootSW_Pos'] = self._SrefElementDeclaration(_DesignObj=C13_01_CtopCbotRouted_YJ_v01_00._CtopCbotRouted(_DesignParameter=None, _Name='{}:SRF_BootSW_Pos'.format(_Name)))[0]

		## Define Sref Reflection: ex)self._DesignParameter['_NMOS_POWER']['_Reflect'] = [0, 0, 0]
		self._DesignParameter['SRF_BootSW_Pos']['_Reflect'] = [1, 0, 0]

		## Define Sref Angle: ex)'_NMOS_POWER'
		self._DesignParameter['SRF_BootSW_Pos']['_Angle'] = 0

		## Calculate Sref Layer by using Calculation_Parameter: ex)'_NMOS_POWER'
		self._DesignParameter['SRF_BootSW_Pos']['_DesignObj']._CalculateDesignParameter(**_Caculation_Parameters)

		## initialized Sref coordinate
		self._DesignParameter['SRF_BootSW_Pos']['_XYCoordinates'] = [[0, 0]]

		## Calculate Sref XYcoord
		tmpXY = []
		## Calculate
		## Target_coord: _XY_type1
		tmp1 = self.get_param_KJH3('SRF_SARLogicWtComparator', 'SRF_Comparator', 'SRF_Slicer', '_Guardring', '_Met1Layerx')
		target_coord = [tmp1[0][0][0][0][0][0]['_XY_left'][0], centY + int(_SpaceBtwBootSWPosNeg / 2)]
		## Approaching_coord: _XY_type2
		tmp2x = self.get_param_KJH4('SRF_BootSW_Pos', 'BND_Ctop_Vtc_M5')
		tmp2y = self.get_param_KJH4('SRF_BootSW_Pos', 'SRF_C13_00', 'SRF_C11', 'SRF_Tr11', 'SRF_Nbodyring', 'SRF_NbodyBottom', 'SRF_NbodyContactPhyLen', 'BND_Met1Layer')
		approaching_coord = [tmp2x[0][0][0]['_XY_right'][0], tmp2y[0][0][0][0][0][0][0][0][0]['_XY_down'][1]]
		## Sref coord
		tmp3 = self.get_param_KJH4('SRF_BootSW_Pos')
		Scoord = tmp3[0][0]['_XY_origin']
		XOffset = -200
		Scoord[0] = Scoord[0] + XOffset
		## Cal
		New_Scoord = self.get_Scoord_KJH4(target_coord, approaching_coord, Scoord)
		tmpXY.append(New_Scoord)
		## Define coordinates
		self._DesignParameter['SRF_BootSW_Pos']['_XYCoordinates'] = tmpXY
		###################################################################################################

		## Calculate Sref Layer by using Calculation_Parameter: ex)'_NMOS_POWER'
		# self._DesignParameter['SRF_BootSW_Neg']['_DesignObj']._CalculateDesignParameter(**_Caculation_Parameters) # 시간줄이기
		self._DesignParameter['SRF_BootSW_Neg'] = copy.deepcopy(self._DesignParameter['SRF_BootSW_Pos'])
		self.rename_srf_prefix(self._DesignParameter['SRF_BootSW_Neg'], 'SRF_BootSW_Pos', 'SRF_BootSW_Neg')


		## Define Sref Reflection: ex)self._DesignParameter['_NMOS_POWER']['_Reflect'] = [0, 0, 0]
		self._DesignParameter['SRF_BootSW_Neg']['_Reflect'] = [0, 0, 0]

		## Define Sref Angle: ex)'_NMOS_POWER'
		self._DesignParameter['SRF_BootSW_Neg']['_Angle'] = 0

		## initialized Sref coordinate
		self._DesignParameter['SRF_BootSW_Neg']['_XYCoordinates'] = [[0, 0]]

		## Calculate Sref XYcoord
		tmpXY = []
		## Calculate
		## Target_coord: _XY_type1
		tmp1 = self.get_param_KJH3('SRF_SARLogicWtComparator', 'SRF_Comparator', 'SRF_Slicer', '_Guardring', '_Met1Layerx')
		target_coord = [tmp1[0][0][0][0][0][0]['_XY_left'][0], centY - int(_SpaceBtwBootSWPosNeg / 2)]
		## Approaching_coord: _XY_type2
		tmp2x = self.get_param_KJH4('SRF_BootSW_Neg', 'BND_Ctop_Vtc_M5')
		tmp2y = self.get_param_KJH4('SRF_BootSW_Neg', 'SRF_C13_00', 'SRF_C11', 'SRF_Tr11', 'SRF_Nbodyring', 'SRF_NbodyBottom', 'SRF_NbodyContactPhyLen', 'BND_Met1Layer')
		approaching_coord = [tmp2x[0][0][0]['_XY_right'][0], tmp2y[0][0][0][0][0][0][0][0][0]['_XY_down'][1]]
		## Sref coord
		tmp3 = self.get_param_KJH4('SRF_BootSW_Neg')
		Scoord = tmp3[0][0]['_XY_origin']
		XOffset = -200
		Scoord[0] = Scoord[0] + XOffset
		## Cal
		New_Scoord = self.get_Scoord_KJH4(target_coord, approaching_coord, Scoord)
		tmpXY.append(New_Scoord)
		## Define coordinates
		self._DesignParameter['SRF_BootSW_Neg']['_XYCoordinates'] = tmpXY
		###################################################################################################
		## BND_NWellExtensionOfTr11
		## Boundary_element Generation
		## Generate Boundary_element: ex)LayerName: METAL1 / DIFF (_ODLayer) / POLY / PIMP (_PPLayer) / NWELL / SLVT LVT RVT HVT / OP(OPpress) / CONT (CA) / PCCRIT
		self._DesignParameter['BND_NWellExtensionOfTr11s'] = self._BoundaryElementDeclaration(
			_Layer=DesignParameters._LayerMapping['NWELL'][0],
			_Datatype=DesignParameters._LayerMapping['NWELL'][1],
			_XWidth=None,
			_YWidth=None,
			_XYCoordinates=[],
		)
		## Define Boundary_element _YWidth
		tmp1 = self.get_param_KJH4('SRF_BootSW_Pos', 'SRF_C13_00', 'SRF_C11', 'SRF_Tr11', 'SRF_Nbodyring', 'BND_ExtenNwell_Bottom')
		tmp2 = self.get_param_KJH4('SRF_BootSW_Neg', 'SRF_C13_00', 'SRF_C11', 'SRF_Tr11', 'SRF_Nbodyring', 'BND_ExtenNwell_Bottom')
		self._DesignParameter['BND_NWellExtensionOfTr11s']['_YWidth'] = abs(tmp1[0][0][0][0][0][0][0]['_XY_up'][1] - tmp2[0][0][0][0][0][0][0]['_XY_up'][1])

		## Define Boundary_element _XWidth
		self._DesignParameter['BND_NWellExtensionOfTr11s']['_XWidth'] = tmp1[0][0][0][0][0][0][0]['_Xwidth']

		## Define Boundary_element _XYCoordinates
		self._DesignParameter['BND_NWellExtensionOfTr11s']['_XYCoordinates'] = [[0, 0]]

		## Calculate Sref XYcoord
		tmpXY = []
		## Calculate
		## Target_coord: _XY_type1
		target_coord = tmp1[0][0][0][0][0][0][0]['_XY_up_left']
		## Approaching_coord: _XY_type2
		tmp2 = self.get_param_KJH4('BND_NWellExtensionOfTr11s')
		approaching_coord = tmp2[0][0]['_XY_up_left']
		## Sref coord
		tmp3 = self.get_param_KJH4('BND_NWellExtensionOfTr11s')
		Scoord = tmp3[0][0]['_XY_origin']
		## Cal
		New_Scoord = self.get_Scoord_KJH4(target_coord, approaching_coord, Scoord)
		tmpXY.append(New_Scoord)
		## Define coordinates
		self._DesignParameter['BND_NWellExtensionOfTr11s']['_XYCoordinates'] = tmpXY
		###################################################################################################

		### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###
		## BootSW -> CDAC Top Node Routing
		##### BND_SampOutput2CDACTop_Pos_Vtc_M6
		## Boundary_element Generation
		## Generate Boundary_element: ex)LayerName: METAL1 / DIFF (_ODLayer) / POLY / PIMP (_PPLayer) / NWELL / SLVT LVT RVT HVT / OP(OPpress) / CONT (CA) / PCCRIT
		self._DesignParameter['BND_SampOutput2CDACTop_Pos_Vtc_M6'] = self._BoundaryElementDeclaration(
			_Layer=DesignParameters._LayerMapping['METAL6'][0],
			_Datatype=DesignParameters._LayerMapping['METAL6'][1],
			_XWidth=None,
			_YWidth=None,
			_XYCoordinates=[],
		)
		## Define Boundary_element _YWidth
		tmp1 = self.get_param_KJH4('SRF_BootSW_Pos', 'BND_OutputNode_Hrz_M6')
		if _CDAC_FoldingTF == True:
			tmp2 = self.get_param_KJH4('SRF_CDAC_Pos', 'SRF_CDACWtDriver', 'BND_CDACTopNode_Vtc_M7')
			self._DesignParameter['BND_SampOutput2CDACTop_Pos_Vtc_M6']['_YWidth'] = abs(tmp1[0][0][0]['_XY_cent'][1] - tmp2[0][0][0][0]['_XY_cent'][1])
		else:
			tmp2 = self.get_param_KJH4('SRF_CDAC_Pos', 'SRF_CDACWtDriver', 'BND_CDACTopNode_Hrz_M7')
			self._DesignParameter['BND_SampOutput2CDACTop_Pos_Vtc_M6']['_YWidth'] = abs(tmp1[0][0][0]['_XY_cent'][1] - tmp2[0][0][0][0]['_XY_down'][1])

		## Define Boundary_element _XWidth
		self._DesignParameter['BND_SampOutput2CDACTop_Pos_Vtc_M6']['_XWidth'] = 400

		## Define Boundary_element _XYCoordinates
		self._DesignParameter['BND_SampOutput2CDACTop_Pos_Vtc_M6']['_XYCoordinates'] = [[0, 0]]

		## Calculate Sref XYcoord
		tmpXY = []
		## Calculate
		## Target_coord: _XY_type1
		target_coord = tmp1[0][0][0]['_XY_right']
		## Approaching_coord: _XY_type2
		tmp2 = self.get_param_KJH4('BND_SampOutput2CDACTop_Pos_Vtc_M6')
		approaching_coord = tmp2[0][0]['_XY_up_right']
		## Sref coord
		tmp3 = self.get_param_KJH4('BND_SampOutput2CDACTop_Pos_Vtc_M6')
		Scoord = tmp3[0][0]['_XY_origin']
		## Cal
		New_Scoord = self.get_Scoord_KJH4(target_coord, approaching_coord, Scoord)
		tmpXY.append(New_Scoord)
		## Define coordinates
		self._DesignParameter['BND_SampOutput2CDACTop_Pos_Vtc_M6']['_XYCoordinates'] = tmpXY
		###################################################################################################
		##### BND_SampOutput2CDACTop_Neg_Vtc_M6
		## Boundary_element Generation
		## Generate Boundary_element: ex)LayerName: METAL1 / DIFF (_ODLayer) / POLY / PIMP (_PPLayer) / NWELL / SLVT LVT RVT HVT / OP(OPpress) / CONT (CA) / PCCRIT
		self._DesignParameter['BND_SampOutput2CDACTop_Neg_Vtc_M6'] = self._BoundaryElementDeclaration(
			_Layer=DesignParameters._LayerMapping['METAL6'][0],
			_Datatype=DesignParameters._LayerMapping['METAL6'][1],
			_XWidth=None,
			_YWidth=None,
			_XYCoordinates=[],
		)
		## Define Boundary_element _YWidth
		tmp1 = self.get_param_KJH4('SRF_BootSW_Neg', 'BND_OutputNode_Hrz_M6')
		if _CDAC_FoldingTF == True:
			tmp2 = self.get_param_KJH4('SRF_CDAC_Neg', 'SRF_CDACWtDriver', 'BND_CDACTopNode_Vtc_M7')
			self._DesignParameter['BND_SampOutput2CDACTop_Neg_Vtc_M6']['_YWidth'] = abs(tmp1[0][0][0]['_XY_cent'][1] - tmp2[0][0][0][0]['_XY_cent'][1])
		else:
			tmp2 = self.get_param_KJH4('SRF_CDAC_Neg', 'SRF_CDACWtDriver', 'BND_CDACTopNode_Hrz_M7')
			self._DesignParameter['BND_SampOutput2CDACTop_Neg_Vtc_M6']['_YWidth'] = abs(tmp1[0][0][0]['_XY_cent'][1] - tmp2[0][0][0][0]['_XY_down'][1])

		## Define Boundary_element _XWidth
		self._DesignParameter['BND_SampOutput2CDACTop_Neg_Vtc_M6']['_XWidth'] = 400

		## Define Boundary_element _XYCoordinates
		self._DesignParameter['BND_SampOutput2CDACTop_Neg_Vtc_M6']['_XYCoordinates'] = [[0, 0]]

		## Calculate Sref XYcoord
		tmpXY = []
		## Calculate
		## Target_coord: _XY_type1
		target_coord = tmp1[0][0][0]['_XY_right']
		## Approaching_coord: _XY_type2
		tmp2 = self.get_param_KJH4('BND_SampOutput2CDACTop_Neg_Vtc_M6')
		approaching_coord = tmp2[0][0]['_XY_down_right']
		## Sref coord
		tmp3 = self.get_param_KJH4('BND_SampOutput2CDACTop_Neg_Vtc_M6')
		Scoord = tmp3[0][0]['_XY_origin']
		## Cal
		New_Scoord = self.get_Scoord_KJH4(target_coord, approaching_coord, Scoord)
		tmpXY.append(New_Scoord)
		## Define coordinates
		self._DesignParameter['BND_SampOutput2CDACTop_Neg_Vtc_M6']['_XYCoordinates'] = tmpXY
		###################################################################################################

		##### BND_SampOutput2CDACTop_Hrz_M7
		## Boundary_element Generation
		## Generate Boundary_element: ex)LayerName: METAL1 / DIFF (_ODLayer) / POLY / PIMP (_PPLayer) / NWELL / SLVT LVT RVT HVT / OP(OPpress) / CONT (CA) / PCCRIT
		self._DesignParameter['BND_SampOutput2CDACTop_Hrz_M7'] = self._BoundaryElementDeclaration(
			_Layer=DesignParameters._LayerMapping['METAL7'][0],
			_Datatype=DesignParameters._LayerMapping['METAL7'][1],
			_XWidth=None,
			_YWidth=None,
			_XYCoordinates=[],
		)
		if _CDAC_FoldingTF == True:
			## Define Boundary_element _YWidth
			self._DesignParameter['BND_SampOutput2CDACTop_Hrz_M7']['_YWidth'] = 400
			tmp2 = self.get_param_KJH4('SRF_CDAC_Pos', 'SRF_CDACWtDriver', 'BND_CDACTopNode_Vtc_M7')
		else:
			## Define Boundary_element _YWidth
			tmp2 = self.get_param_KJH4('SRF_CDAC_Pos', 'SRF_CDACWtDriver', 'BND_CDACTopNode_Hrz_M7')
			self._DesignParameter['BND_SampOutput2CDACTop_Hrz_M7']['_YWidth'] = tmp2[0][0][0][0]['_Ywidth']

		## Define Boundary_element _XWidth
		tmp1 = self.get_param_KJH4('BND_SampOutput2CDACTop_Pos_Vtc_M6')
		self._DesignParameter['BND_SampOutput2CDACTop_Hrz_M7']['_XWidth'] = abs(tmp1[0][0]['_XY_left'][0] - tmp2[0][0][0][0]['_XY_right'][0])

		## Define Boundary_element _XYCoordinates
		self._DesignParameter['BND_SampOutput2CDACTop_Hrz_M7']['_XYCoordinates'] = [[0, 0]]

		## Calculate Sref XYcoord
		tmpXY = []
		## Calculate
		## Target_coord: _XY_type1
		target_coord = tmp1[0][0]['_XY_down_left']
		## Approaching_coord: _XY_type2
		tmp2 = self.get_param_KJH4('BND_SampOutput2CDACTop_Hrz_M7')
		approaching_coord = tmp2[0][0]['_XY_down_left']
		## Sref coord
		tmp3 = self.get_param_KJH4('BND_SampOutput2CDACTop_Hrz_M7')
		Scoord = tmp3[0][0]['_XY_origin']
		## Cal
		New_Scoord = self.get_Scoord_KJH4(target_coord, approaching_coord, Scoord)
		tmpXY.append(New_Scoord)

		## Cal2 (Neg)
		tmp1 = self.get_param_KJH4('BND_SampOutput2CDACTop_Neg_Vtc_M6')
		target_coord = tmp1[0][0]['_XY_up_left']
		approaching_coord = tmp2[0][0]['_XY_up_left']
		New_Scoord = self.get_Scoord_KJH4(target_coord, approaching_coord, Scoord)
		tmpXY.append(New_Scoord)

		## Define coordinates
		self._DesignParameter['BND_SampOutput2CDACTop_Hrz_M7']['_XYCoordinates'] = tmpXY
		###################################################################################################

		#### Via -> BND_SampOutput2CDACTop_Neg_Vtc_M6 -> BND_CDACTopNode
		## Sref generation: ViaX
		## Define ViaX Parameter
		_Caculation_Parameters = copy.deepcopy(A02_ViaStack_KJH3._ViaStack._ParametersForDesignCalculation)
		_Caculation_Parameters['_Layer1'] = 6
		_Caculation_Parameters['_Layer2'] = 7
		_Caculation_Parameters['_COX'] = None
		_Caculation_Parameters['_COY'] = None

		## Sref ViaX declaration
		self._DesignParameter['SRF_SampOut2CDACTop_ViaM6M7'] = self._SrefElementDeclaration(_DesignObj=A02_ViaStack_KJH3._ViaStack(_DesignParameter=None, _Name='{}:SRF_SampOut2CDACTop_ViaM6M7'.format(_Name)))[0]

		## Define Sref Relection
		self._DesignParameter['SRF_SampOut2CDACTop_ViaM6M7']['_Reflect'] = [0, 0, 0]

		## Define Sref Angle
		self._DesignParameter['SRF_SampOut2CDACTop_ViaM6M7']['_Angle'] = 0

		## Calcuate Overlapped XYcoord
		tmp1 = self.get_param_KJH4('BND_SampOutput2CDACTop_Hrz_M7')
		tmp2 = self.get_param_KJH4('BND_SampOutput2CDACTop_Pos_Vtc_M6')
		Ovlpcoord = self.get_ovlp_KJH2(tmp1[0][0], tmp2[0][0])

		## Calcuate _COX and _COY:  None or 'MinEnclosureX' or 'MinEnclosureY' or 'SameEnclosure'
		_COX, _COY = self._CalculateNumViaByXYWidth(Ovlpcoord[0]['_Xwidth'], Ovlpcoord[0]['_Ywidth'], None)

		## Define _COX and _COY
		_Caculation_Parameters['_COX'] = _COX
		_Caculation_Parameters['_COY'] = _COY

		## Generate Metal(x), Metal(x+1) and C0(Viax) layer:  Option: _CalculateDesignParameter, _CalculateDesignParameterXmin, _CalculateDesignParameterYmin, _CalculateDesignParameterXYsame
		self._DesignParameter['SRF_SampOut2CDACTop_ViaM6M7']['_DesignObj']._CalculateDesignParameter(**_Caculation_Parameters)

		## Calculate Sref XYcoord
		tmpXY = []
		## initialized Sref coordinate
		self._DesignParameter['SRF_SampOut2CDACTop_ViaM6M7']['_XYCoordinates'] = [[0, 0]]
		## Calculate
		## Target_coord
		target_coord = [tmp2[0][0]['_XY_cent'][0], tmp1[0][0]['_XY_cent'][1]]
		## Approaching_coord
		tmp4 = self.get_param_KJH4('SRF_SampOut2CDACTop_ViaM6M7', 'SRF_ViaM6M7', 'BND_Met6Layer')
		approaching_coord = tmp4[0][0][0][0]['_XY_cent']
		## Sref coord
		tmp3 = self.get_param_KJH4('SRF_SampOut2CDACTop_ViaM6M7')
		Scoord = tmp3[0][0]['_XY_origin']
		## Calculate
		New_Scoord = self.get_Scoord_KJH4(target_coord, approaching_coord, Scoord)
		tmpXY.append(New_Scoord)
		# Cal 2 (Neg)
		target_coord = [tmp2[0][0]['_XY_cent'][0], tmp1[1][0]['_XY_cent'][1]]
		New_Scoord = self.get_Scoord_KJH4(target_coord, approaching_coord, Scoord)
		tmpXY.append(New_Scoord)
		## Define
		self._DesignParameter['SRF_SampOut2CDACTop_ViaM6M7']['_XYCoordinates'] = tmpXY
		###################################################################################################

		### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###
		## SAR Logic -> CDAC Driver Input Routing
		for j in range(_NumofCbit):
			## BND_CDAC_Pos_DrvIn_Hrz_M3
			## Generate Boundary_element: ex)LayerName: METAL1 / DIFF (_ODLayer) / POLY / PIMP (_PPLayer) / NWELL / SLVT LVT RVT HVT / OP(OPpress) / CONT (CA) / PCCRIT
			self._DesignParameter['BND_CDAC_Pos_MSB{}DrvIn_Hrz_M3'.format(j)] = self._BoundaryElementDeclaration(
				_Layer=DesignParameters._LayerMapping['METAL3'][0],
				_Datatype=DesignParameters._LayerMapping['METAL3'][1],
				_XWidth=None,
				_YWidth=None,
				_XYCoordinates=[],
			)
			## Define Boundary_element _YWidth
			if _CDAC_FoldingTF == True:
				tmp1 = self.get_param_KJH4('SRF_CDAC_Pos','SRF_CDACWtDriver','BND_CDACFold1_{}B{}_DrvInput_Hrz_M3'.format('Lo', _NumofCbit - 1 - j))
				self._DesignParameter['BND_CDAC_Pos_MSB{}DrvIn_Hrz_M3'.format(j)]['_YWidth'] = tmp1[0][0][0][0]['_Ywidth']
			else:
				tmp1 = self.get_param_KJH4('SRF_CDAC_Pos', 'SRF_CDACWtDriver','SRF_CDACWtDriver', 'SRF_DriverArray', 'BND_{}C_Driver_Input_Hrz_M3'.format(2 ** (_NumofCbit - 1 - j)))
				self._DesignParameter['BND_CDAC_Pos_MSB{}DrvIn_Hrz_M3'.format(j)]['_YWidth'] = tmp1[0][0][0][0][0][0]['_Ywidth']

			## Define Boundary_element _XWidth
			if _CDAC_FoldingTF == True:
				tmp2 = self.get_param_KJH4('SRF_SARLogicWtComparator', 'SRF_SARLogicWtBuffers', 'SRF_UpperCDACPreDriver',  'SRF_InvChain{}'.format(j), 'SRF_Output_ViaM2Mx', 'SRF_ViaM2M3', 'BND_Met2Layer')
				self._DesignParameter['BND_CDAC_Pos_MSB{}DrvIn_Hrz_M3'.format(j)]['_XWidth'] = tmp2[0][0][0][0][0][0][0][0]['_XY_right'][0] - tmp1[0][0][0][0]['_XY_left'][0]
			else:
				tmp2 = self.get_param_KJH4('SRF_SARLogicWtComparator', 'SRF_SARLogicWtBuffers', 'SRF_UpperCDACPreDriver', 'SRF_InvChain{}'.format(j), 'SRF_Output_ViaM2Mx', 'SRF_ViaM2M3', 'BND_Met2Layer')
				self._DesignParameter['BND_CDAC_Pos_MSB{}DrvIn_Hrz_M3'.format(j)]['_XWidth'] = tmp2[0][0][0][0][0][0][0][0]['_XY_right'][0] - tmp1[0][0][0][0][0][0]['_XY_left'][0]

			if self._DesignParameter['BND_CDAC_Pos_MSB{}DrvIn_Hrz_M3'.format(j)]['_XWidth'] < 0:
				self._DesignParameter['BND_CDAC_Pos_MSB{}DrvIn_Hrz_M3'.format(j)]['_XWidth'] = self._DesignParameter['BND_CDAC_Pos_MSB{}DrvIn_Hrz_M3'.format(j)]['_XWidth'] - 244

			## Calculate Sref XYcoord
			tmpXY = []
			## initialized Sref coordinate
			self._DesignParameter['BND_CDAC_Pos_MSB{}DrvIn_Hrz_M3'.format(j)]['_XYCoordinates'] = [[0, 0]]
			if _CDAC_FoldingTF == True:
				target_coord = tmp1[0][0][0][0]['_XY_down_left']
			else:
				target_coord = tmp1[0][0][0][0][0][0]['_XY_down_left']
			## Approaching_coord: _XY_type2
			tmp2 = self.get_param_KJH4('BND_CDAC_Pos_MSB{}DrvIn_Hrz_M3'.format(j))
			approaching_coord = tmp2[0][0]['_XY_down_left']
			## Sref coord
			tmp3 = self.get_param_KJH4('BND_CDAC_Pos_MSB{}DrvIn_Hrz_M3'.format(j))
			Scoord = tmp3[0][0]['_XY_origin']
			## Cal
			New_Scoord = self.get_Scoord_KJH4(target_coord, approaching_coord, Scoord)
			tmpXY.append(New_Scoord)
			## Define coordinates
			self._DesignParameter['BND_CDAC_Pos_MSB{}DrvIn_Hrz_M3'.format(j)]['_XYCoordinates'] = tmpXY
		###################################################################################################

			## BND_CDAC_Pos_DrvIn_Vtc_M4
			## Generate Boundary_element: ex)LayerName: METAL1 / DIFF (_ODLayer) / POLY / PIMP (_PPLayer) / NWELL / SLVT LVT RVT HVT / OP(OPpress) / CONT (CA) / PCCRIT
			self._DesignParameter['BND_CDAC_Pos_MSB{}DrvIn_Vtc_M4'.format(j)] = self._BoundaryElementDeclaration(
				_Layer=DesignParameters._LayerMapping['METAL4'][0],
				_Datatype=DesignParameters._LayerMapping['METAL4'][1],
				_XWidth=None,
				_YWidth=None,
				_XYCoordinates=[],
			)
			## Define Boundary_element _YWidth
			tmp1 = self.get_param_KJH4('BND_CDAC_Pos_MSB{}DrvIn_Hrz_M3'.format(j))
			tmp2 = self.get_param_KJH4('SRF_SARLogicWtComparator', 'SRF_SARLogicWtBuffers', 'SRF_UpperCDACPreDriver', 'SRF_InvChain{}'.format(_NumofCbit - 1 - j), 'SRF_Output_ViaM2Mx', 'SRF_ViaM2M3',
									   'BND_Met2Layer')
			self._DesignParameter['BND_CDAC_Pos_MSB{}DrvIn_Vtc_M4'.format(j)]['_YWidth'] = abs(tmp1[0][0]['_XY_cent'][1] - tmp2[0][0][0][0][0][0][0][0]['_XY_up'][1])

			## Define Boundary_element _XWidth
			self._DesignParameter['BND_CDAC_Pos_MSB{}DrvIn_Vtc_M4'.format(j)]['_XWidth'] = 50

			## Calculate Sref XYcoord
			tmpXY = []
			## initialized Sref coordinate
			self._DesignParameter['BND_CDAC_Pos_MSB{}DrvIn_Vtc_M4'.format(j)]['_XYCoordinates'] = [[0, 0]]
			## Calculate
			## Target_coord: _XY_type1
			target_coord = tmp1[0][0]['_XY_right']
			## Approaching_coord: _XY_type2
			tmp2 = self.get_param_KJH4('BND_CDAC_Pos_MSB{}DrvIn_Vtc_M4'.format(j))
			approaching_coord = tmp2[0][0]['_XY_up_right']
			## Sref coord
			tmp3 = self.get_param_KJH4('BND_CDAC_Pos_MSB{}DrvIn_Vtc_M4'.format(j))
			Scoord = tmp3[0][0]['_XY_origin']
			## Cal
			New_Scoord = self.get_Scoord_KJH4(target_coord, approaching_coord, Scoord)
			tmpXY.append(New_Scoord)
			## Define coordinates
			self._DesignParameter['BND_CDAC_Pos_MSB{}DrvIn_Vtc_M4'.format(j)]['_XYCoordinates'] = tmpXY
		###################################################################################################

			#####################################################
			## BND_CDAC_Neg_DrvIn_Hrz_M3
			## Generate Boundary_element: ex)LayerName: METAL1 / DIFF (_ODLayer) / POLY / PIMP (_PPLayer) / NWELL / SLVT LVT RVT HVT / OP(OPpress) / CONT (CA) / PCCRIT
			self._DesignParameter['BND_CDAC_Neg_MSB{}DrvIn_Hrz_M3'.format(j)] = self._BoundaryElementDeclaration(
				_Layer=DesignParameters._LayerMapping['METAL3'][0],
				_Datatype=DesignParameters._LayerMapping['METAL3'][1],
				_XWidth=None,
				_YWidth=None,
				_XYCoordinates=[],
			)
			## Define Boundary_element _YWidth
			if _CDAC_FoldingTF == True:
				tmp1 = self.get_param_KJH4('SRF_CDAC_Neg', 'SRF_CDACWtDriver', 'BND_CDACFold1_{}B{}_DrvInput_Hrz_M3'.format('Lo', _NumofCbit - 1 - j))
				self._DesignParameter['BND_CDAC_Neg_MSB{}DrvIn_Hrz_M3'.format(j)]['_YWidth'] = tmp1[0][0][0][0]['_Ywidth']
			else:
				tmp1 = self.get_param_KJH4('SRF_CDAC_Neg', 'SRF_CDACWtDriver','SRF_CDACWtDriver', 'SRF_DriverArray', 'BND_{}C_Driver_Input_Hrz_M3'.format(2 ** (_NumofCbit - 1 - j)))
				self._DesignParameter['BND_CDAC_Neg_MSB{}DrvIn_Hrz_M3'.format(j)]['_YWidth'] = tmp1[0][0][0][0][0][0]['_Ywidth']

			## Define Boundary_element _XWidth
			if _CDAC_FoldingTF == True:
				tmp2 = self.get_param_KJH4('SRF_SARLogicWtComparator', 'SRF_SARLogicWtBuffers', 'SRF_LowerCDACPreDriver', 'SRF_InvChain{}'.format(j), 'SRF_Output_ViaM2Mx', 'SRF_ViaM2M3', 'BND_Met2Layer')
				self._DesignParameter['BND_CDAC_Neg_MSB{}DrvIn_Hrz_M3'.format(j)]['_XWidth'] = tmp2[0][0][0][0][0][0][0][0]['_XY_right'][0] - tmp1[0][0][0][0]['_XY_left'][0]
			else:
				tmp2 = self.get_param_KJH4('SRF_SARLogicWtComparator', 'SRF_SARLogicWtBuffers', 'SRF_LowerCDACPreDriver', 'SRF_InvChain{}'.format(j), 'SRF_Output_ViaM2Mx', 'SRF_ViaM2M3', 'BND_Met2Layer')
				self._DesignParameter['BND_CDAC_Neg_MSB{}DrvIn_Hrz_M3'.format(j)]['_XWidth'] = tmp2[0][0][0][0][0][0][0][0]['_XY_right'][0] - tmp1[0][0][0][0][0][0]['_XY_left'][0]

			if self._DesignParameter['BND_CDAC_Neg_MSB{}DrvIn_Hrz_M3'.format(j)]['_XWidth'] < 0:
				self._DesignParameter['BND_CDAC_Neg_MSB{}DrvIn_Hrz_M3'.format(j)]['_XWidth'] = \
					self._DesignParameter['BND_CDAC_Neg_MSB{}DrvIn_Hrz_M3'.format(j)]['_XWidth'] - 244

			## Calculate Sref XYcoord
			tmpXY = []
			## initialized Sref coordinate
			self._DesignParameter['BND_CDAC_Neg_MSB{}DrvIn_Hrz_M3'.format(j)]['_XYCoordinates'] = [[0, 0]]
			## Calculate
			## Target_coord: _XY_type1
			if _CDAC_FoldingTF == True:
				target_coord = tmp1[0][0][0][0]['_XY_up_left']
			else:
				target_coord = tmp1[0][0][0][0][0][0]['_XY_up_left']
			## Approaching_coord: _XY_type2
			tmp2 = self.get_param_KJH4('BND_CDAC_Neg_MSB{}DrvIn_Hrz_M3'.format(j))
			approaching_coord = tmp2[0][0]['_XY_down_left']
			## Sref coord
			tmp3 = self.get_param_KJH4('BND_CDAC_Neg_MSB{}DrvIn_Hrz_M3'.format(j))
			Scoord = tmp3[0][0]['_XY_origin']
			## Cal
			New_Scoord = self.get_Scoord_KJH4(target_coord, approaching_coord, Scoord)
			tmpXY.append(New_Scoord)
			## Define coordinates
			self._DesignParameter['BND_CDAC_Neg_MSB{}DrvIn_Hrz_M3'.format(j)]['_XYCoordinates'] = tmpXY
		###################################################################################################

			## BND_CDAC_Neg_DrvIn_Vtc_M4
			## Generate Boundary_element: ex)LayerName: METAL1 / DIFF (_ODLayer) / POLY / PIMP (_PPLayer) / NWELL / SLVT LVT RVT HVT / OP(OPpress) / CONT (CA) / PCCRIT
			self._DesignParameter['BND_CDAC_Neg_MSB{}DrvIn_Vtc_M4'.format(j)] = self._BoundaryElementDeclaration(
				_Layer=DesignParameters._LayerMapping['METAL4'][0],
				_Datatype=DesignParameters._LayerMapping['METAL4'][1],
				_XWidth=None,
				_YWidth=None,
				_XYCoordinates=[],
			)
			## Define Boundary_element _YWidth
			tmp1 = self.get_param_KJH4('BND_CDAC_Neg_MSB{}DrvIn_Hrz_M3'.format(j))
			tmp2 = self.get_param_KJH4('SRF_SARLogicWtComparator', 'SRF_SARLogicWtBuffers', 'SRF_LowerCDACPreDriver', 'SRF_InvChain{}'.format(_NumofCbit - 1 - j), 'SRF_Output_ViaM2Mx', 'SRF_ViaM2M3',  'BND_Met2Layer')
			self._DesignParameter['BND_CDAC_Neg_MSB{}DrvIn_Vtc_M4'.format(j)]['_YWidth'] = abs(tmp1[0][0]['_XY_cent'][1] - tmp2[0][0][0][0][0][0][0][0]['_XY_down'][1])

			## Define Boundary_element _XWidth
			self._DesignParameter['BND_CDAC_Neg_MSB{}DrvIn_Vtc_M4'.format(j)]['_XWidth'] = 50

			## Calculate Sref XYcoord
			tmpXY = []
			## initialized Sref coordinate
			self._DesignParameter['BND_CDAC_Neg_MSB{}DrvIn_Vtc_M4'.format(j)]['_XYCoordinates'] = [[0, 0]]
			## Calculate
			## Target_coord: _XY_type1
			target_coord = tmp1[0][0]['_XY_right']
			## Approaching_coord: _XY_type2
			tmp2 = self.get_param_KJH4('BND_CDAC_Neg_MSB{}DrvIn_Vtc_M4'.format(j))
			approaching_coord = tmp2[0][0]['_XY_down_right']
			## Sref coord
			tmp3 = self.get_param_KJH4('BND_CDAC_Neg_MSB{}DrvIn_Vtc_M4'.format(j))
			Scoord = tmp3[0][0]['_XY_origin']
			## Cal
			New_Scoord = self.get_Scoord_KJH4(target_coord, approaching_coord, Scoord)
			tmpXY.append(New_Scoord)
			## Define coordinates
			self._DesignParameter['BND_CDAC_Neg_MSB{}DrvIn_Vtc_M4'.format(j)]['_XYCoordinates'] = tmpXY
		###################################################################################################

		#### 'BND_CDAC_Neg_MSB#DrvIn_Vtc_M4' <-> 'BND_CDAC_Neg_MSB#DrvIn_Hrz_M3'
		## Sref generation: ViaX
		## Define ViaX Parameter
		_Caculation_Parameters = copy.deepcopy(A02_ViaStack_KJH3._ViaStack._ParametersForDesignCalculation)
		_Caculation_Parameters['_Layer1'] = 3
		_Caculation_Parameters['_Layer2'] = 4
		_Caculation_Parameters['_COX'] = 2
		_Caculation_Parameters['_COY'] = 1

		## Sref ViaX declaration
		self._DesignParameter['SRF_CDAC_Neg_DrvIN_ViaM3M4'] = self._SrefElementDeclaration(_DesignObj=A02_ViaStack_KJH3._ViaStack(_DesignParameter=None, _Name='{}:SRF_CDAC_Neg_DrvIN_ViaM3M4'.format(_Name)))[0]

		## Define Sref Relection
		self._DesignParameter['SRF_CDAC_Neg_DrvIN_ViaM3M4']['_Reflect'] = [0, 0, 0]

		## Define Sref Angle
		self._DesignParameter['SRF_CDAC_Neg_DrvIN_ViaM3M4']['_Angle'] = 0

		## Generate Metal(x), Metal(x+1) and C0(Viax) layer:  Option: _CalculateDesignParameter, _CalculateDesignParameterXmin, _CalculateDesignParameterYmin, _CalculateDesignParameterXYsame
		self._DesignParameter['SRF_CDAC_Neg_DrvIN_ViaM3M4']['_DesignObj']._CalculateDesignParameterYmin(**_Caculation_Parameters)

		## initialized Sref coordinate
		self._DesignParameter['SRF_CDAC_Neg_DrvIN_ViaM3M4']['_XYCoordinates'] = [[0, 0]]

		## Calculate Sref XYcoord
		tmpXY = []
		## Calculate
		## Approaching_coord
		tmp2 = self.get_param_KJH4('SRF_CDAC_Neg_DrvIN_ViaM3M4', 'SRF_ViaM3M4', 'BND_Met3Layer')
		approaching_coord = tmp2[0][0][0][0]['_XY_right']
		## Sref coord
		tmp3 = self.get_param_KJH4('SRF_CDAC_Neg_DrvIN_ViaM3M4')
		Scoord = tmp3[0][0]['_XY_origin']
		## Calculate
		for i in range(_NumofCbit):
			tmp1 = self.get_param_KJH4('BND_CDAC_Neg_MSB{}DrvIn_Vtc_M4'.format(i))
			## Target_coord
			target_coord = tmp1[0][0]['_XY_down_right']
			New_Scoord = self.get_Scoord_KJH4(target_coord, approaching_coord, Scoord)
			tmpXY.append(New_Scoord)
			## Define
		self._DesignParameter['SRF_CDAC_Neg_DrvIN_ViaM3M4']['_XYCoordinates'] = tmpXY
		###################################################################################################

		#### 'BND_CDAC_Pos_MSB#DrvIn_Vtc_M4' <-> 'BND_CDAC_Pos_MSB#DrvIn_Hrz_M3'
		## Sref generation: ViaX
		## Define ViaX Parameter
		_Caculation_Parameters = copy.deepcopy(A02_ViaStack_KJH3._ViaStack._ParametersForDesignCalculation)
		_Caculation_Parameters['_Layer1'] = 3
		_Caculation_Parameters['_Layer2'] = 4
		_Caculation_Parameters['_COX'] = 2
		_Caculation_Parameters['_COY'] = 1

		## Sref ViaX declaration
		self._DesignParameter['SRF_CDAC_Pos_DrvIN_ViaM3M4'] = self._SrefElementDeclaration(_DesignObj=A02_ViaStack_KJH3._ViaStack(_DesignParameter=None, _Name='{}:SRF_CDAC_Pos_DrvIN_ViaM3M4'.format(_Name)))[0]

		## Define Sref Relection
		self._DesignParameter['SRF_CDAC_Pos_DrvIN_ViaM3M4']['_Reflect'] = [0, 0, 0]

		## Define Sref Angle
		self._DesignParameter['SRF_CDAC_Pos_DrvIN_ViaM3M4']['_Angle'] = 0

		## Generate Metal(x), Metal(x+1) and C0(Viax) layer:  Option: _CalculateDesignParameter, _CalculateDesignParameterXmin, _CalculateDesignParameterYmin, _CalculateDesignParameterXYsame
		self._DesignParameter['SRF_CDAC_Pos_DrvIN_ViaM3M4']['_DesignObj']._CalculateDesignParameterYmin(**_Caculation_Parameters)

		## initialized Sref coordinate
		self._DesignParameter['SRF_CDAC_Pos_DrvIN_ViaM3M4']['_XYCoordinates'] = [[0, 0]]

		## Calculate Sref XYcoord
		tmpXY = []
		## Calculate
		## Approaching_coord
		tmp2 = self.get_param_KJH4('SRF_CDAC_Pos_DrvIN_ViaM3M4', 'SRF_ViaM3M4', 'BND_Met3Layer')
		approaching_coord = tmp2[0][0][0][0]['_XY_right']
		## Sref coord
		tmp3 = self.get_param_KJH4('SRF_CDAC_Pos_DrvIN_ViaM3M4')
		Scoord = tmp3[0][0]['_XY_origin']
		## Calculate
		for i in range(_NumofCbit):
			tmp1 = self.get_param_KJH4('BND_CDAC_Pos_MSB{}DrvIn_Vtc_M4'.format(i))
			## Target_coord
			target_coord = tmp1[0][0]['_XY_up_right']
			New_Scoord = self.get_Scoord_KJH4(target_coord, approaching_coord, Scoord)
			tmpXY.append(New_Scoord)
			## Define
		self._DesignParameter['SRF_CDAC_Pos_DrvIN_ViaM3M4']['_XYCoordinates'] = tmpXY
		###################################################################################################

		# ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###
		# ## CDAC Top -> Comparator Input Routing
		## get_param_KJH3를 사용하기 위해 Angle과 Reflect를 초기화시킴.
		self._DesignParameter['SRF_SARLogicWtComparator']['_DesignObj']._DesignParameter['SRF_Comparator']['_DesignObj']._DesignParameter['SRF_Slicer']['_DesignObj']._DesignParameter['_NMOSSET']['_Angle'] = 0
		self._DesignParameter['SRF_SARLogicWtComparator']['_DesignObj']._DesignParameter['SRF_Comparator']['_DesignObj']._DesignParameter['SRF_Slicer']['_DesignObj']._DesignParameter['_NMOSSET']['_Reflect'] = [0, 0, 0]
		self._DesignParameter['SRF_SARLogicWtComparator']['_DesignObj']._DesignParameter['SRF_Comparator']['_DesignObj']._DesignParameter['SRF_Slicer']['_DesignObj']._DesignParameter['_NMOSSET']['_DesignObj']._DesignParameter['_VIANMOSPoly2Met1NMOS1']['_Angle'] = 0
		self._DesignParameter['SRF_SARLogicWtComparator']['_DesignObj']._DesignParameter['SRF_Comparator']['_DesignObj']._DesignParameter['SRF_Slicer']['_DesignObj']._DesignParameter['_NMOSSET']['_DesignObj']._DesignParameter['_VIANMOSPoly2Met1NMOS1']['_Reflect'] = [0, 0, 0]
		self._DesignParameter['SRF_SARLogicWtComparator']['_DesignObj']._DesignParameter['SRF_Comparator']['_DesignObj']._DesignParameter['SRF_Slicer']['_DesignObj']._DesignParameter['_NMOSSET']['_DesignObj']._DesignParameter['_VIANMOSPoly2Met1NMOS2']['_Angle'] = 0
		self._DesignParameter['SRF_SARLogicWtComparator']['_DesignObj']._DesignParameter['SRF_Comparator']['_DesignObj']._DesignParameter['SRF_Slicer']['_DesignObj']._DesignParameter['_NMOSSET']['_DesignObj']._DesignParameter['_VIANMOSPoly2Met1NMOS2']['_Reflect'] = [0, 0, 0]

		tmpP = self.get_param_KJH3('SRF_SARLogicWtComparator', 'SRF_Comparator', 'SRF_Slicer', '_NMOSSET', '_VIANMOSPoly2Met1NMOS1', '_Met1Layer')
		tmpN = self.get_param_KJH3('SRF_SARLogicWtComparator', 'SRF_Comparator', 'SRF_Slicer', '_NMOSSET', '_VIANMOSPoly2Met1NMOS2', '_Met1Layer')
		tmpCent = int((tmpP[0][0][0][0][0][0][0]['_XY_right'][0] + tmpN[0][0][0][0][0][0][0]['_XY_left'][0]) / 2)

		###################################################################################################

		#### Comp Input Via M1M6
		## Sref generation: ViaX
		## Define ViaX Parameter
		_Caculation_Parameters = copy.deepcopy(A02_ViaStack_KJH3._ViaStack._ParametersForDesignCalculation)
		_Caculation_Parameters['_Layer1'] = 1
		_Caculation_Parameters['_Layer2'] = 6
		_Caculation_Parameters['_COX'] = None
		_Caculation_Parameters['_COY'] = None

		## Sref ViaX declaration
		self._DesignParameter['SRF_CompInput_ViaM1M6'] = self._SrefElementDeclaration(
			_DesignObj=A02_ViaStack_KJH3._ViaStack(_DesignParameter=None, _Name='{}:SRF_CompInput_ViaM1M6'.format(_Name)))[0]

		## Define Sref Relection
		self._DesignParameter['SRF_CompInput_ViaM1M6']['_Reflect'] = [0, 0, 0]

		## Define Sref Angle
		self._DesignParameter['SRF_CompInput_ViaM1M6']['_Angle'] = 0

		## Calcuate _COX and _COY:  None or 'MinEnclosureX' or 'MinEnclosureY' or 'SameEnclosure'
		_COX, _COY = self._CalculateNumViaByXYWidth(tmpP[0][0][0][0][0][0][0]['_Xwidth'], tmpP[0][0][0][0][0][0][0]['_Ywidth'], None)

		## Define _COX and _COY
		_Caculation_Parameters['_COX'] = _COX
		_Caculation_Parameters['_COY'] = max(_COY, 2)

		## Generate Metal(x), Metal(x+1) and C0(Viax) layer:  Option: _CalculateDesignParameter, _CalculateDesignParameterXmin, _CalculateDesignParameterYmin, _CalculateDesignParameterXYsame
		self._DesignParameter['SRF_CompInput_ViaM1M6']['_DesignObj']._CalculateDesignParameter(**_Caculation_Parameters)

		## Calculate Sref XYcoord
		tmpXY = []
		## initialized Sref coordinate
		self._DesignParameter['SRF_CompInput_ViaM1M6']['_XYCoordinates'] = [[0, 0]]
		## Calculate
		## Target_coord
		target_coord = tmpP[0][0][0][0][0][0][0]['_XY_down']
		## Approaching_coord
		tmp2 = self.get_param_KJH4('SRF_CompInput_ViaM1M6', 'SRF_ViaM1M2', 'BND_Met1Layer')
		approaching_coord = tmp2[0][0][0][0]['_XY_down']
		## Sref coord
		tmp3 = self.get_param_KJH4('SRF_CompInput_ViaM1M6')
		Scoord = tmp3[0][0]['_XY_origin']
		## Calculate
		New_Scoord = self.get_Scoord_KJH4(target_coord, approaching_coord, Scoord)
		tmpXY.append(New_Scoord)
		## Calc 2 (VinN)
		target_coord = tmpN[0][0][0][0][0][0][0]['_XY_down']
		New_Scoord = self.get_Scoord_KJH4(target_coord, approaching_coord, Scoord)
		tmpXY.append(New_Scoord)
		## Define
		self._DesignParameter['SRF_CompInput_ViaM1M6']['_XYCoordinates'] = tmpXY
		################################################################################################### ################################################################################################### Via1개만 있음..

		#### Comp Input P Via M6M7
		## Sref generation: ViaX
		## Define ViaX Parameter
		_Caculation_Parameters = copy.deepcopy(A02_ViaStack_KJH3._ViaStack._ParametersForDesignCalculation)
		_Caculation_Parameters['_Layer1'] = 6
		_Caculation_Parameters['_Layer2'] = 7
		_Caculation_Parameters['_COX'] = _COX
		_Caculation_Parameters['_COY'] = _COY

		## Sref ViaX declaration
		self._DesignParameter['SRF_CompInputN_ViaM6M7'] = self._SrefElementDeclaration(_DesignObj=A02_ViaStack_KJH3._ViaStack(_DesignParameter=None, _Name='{}:SRF_CompInputN_ViaM6M7'.format(_Name)))[0]

		## Define Sref Relection
		self._DesignParameter['SRF_CompInputN_ViaM6M7']['_Reflect'] = [0, 0, 0]

		## Define Sref Angle
		self._DesignParameter['SRF_CompInputN_ViaM6M7']['_Angle'] = 0

		## Generate Metal(x), Metal(x+1) and C0(Viax) layer:  Option: _CalculateDesignParameter, _CalculateDesignParameterXmin, _CalculateDesignParameterYmin, _CalculateDesignParameterXYsame
		self._DesignParameter['SRF_CompInputN_ViaM6M7']['_DesignObj']._CalculateDesignParameter(**_Caculation_Parameters)

		## Calculate Sref XYcoord
		tmpXY = []
		## initialized Sref coordinate
		self._DesignParameter['SRF_CompInputN_ViaM6M7']['_XYCoordinates'] = [[0, 0]]
		## Calculate
		## Target_coord
		tmp1 = self.get_param_KJH4('SRF_CompInput_ViaM1M6', 'SRF_ViaM1M2', 'BND_Met1Layer')
		target_coord = tmp1[0][0][0][0]['_XY_down']
		## Approaching_coord
		tmp2 = self.get_param_KJH4('SRF_CompInputN_ViaM6M7', 'SRF_ViaM6M7', 'BND_Met6Layer')
		approaching_coord = tmp2[0][0][0][0]['_XY_up']
		## Sref coord
		tmp3 = self.get_param_KJH4('SRF_CompInputN_ViaM6M7')
		Scoord = tmp3[0][0]['_XY_origin']
		## Calculate
		New_Scoord = self.get_Scoord_KJH4(target_coord, approaching_coord, Scoord)
		tmpXY.append(New_Scoord)
		## Define
		self._DesignParameter['SRF_CompInputN_ViaM6M7']['_XYCoordinates'] = tmpXY
		###################################################################################################  ################################################################################################### Via1개만 있음..

		#### Comp Input N Via M6M7
		## Sref generation: ViaX
		## Define ViaX Parameter
		_Caculation_Parameters = copy.deepcopy(A02_ViaStack_KJH3._ViaStack._ParametersForDesignCalculation)
		_Caculation_Parameters['_Layer1'] = 6
		_Caculation_Parameters['_Layer2'] = 7
		_Caculation_Parameters['_COX'] = _COX
		_Caculation_Parameters['_COY'] = _COY

		## Sref ViaX declaration
		self._DesignParameter['SRF_CompInputP_ViaM6M7'] = self._SrefElementDeclaration(_DesignObj=A02_ViaStack_KJH3._ViaStack(_DesignParameter=None, _Name='{}:SRF_CompInputP_ViaM6M7'.format(_Name)))[0]

		## Define Sref Relection
		self._DesignParameter['SRF_CompInputP_ViaM6M7']['_Reflect'] = [0, 0, 0]

		## Define Sref Angle
		self._DesignParameter['SRF_CompInputP_ViaM6M7']['_Angle'] = 0

		## Generate Metal(x), Metal(x+1) and C0(Viax) layer:  Option: _CalculateDesignParameter, _CalculateDesignParameterXmin, _CalculateDesignParameterYmin, _CalculateDesignParameterXYsame
		self._DesignParameter['SRF_CompInputP_ViaM6M7']['_DesignObj']._CalculateDesignParameter(**_Caculation_Parameters)

		## Calculate Sref XYcoord
		tmpXY = []
		## initialized Sref coordinate
		self._DesignParameter['SRF_CompInputP_ViaM6M7']['_XYCoordinates'] = [[0, 0]]
		## Calculate
		## Target_coord
		tmp1 = self.get_param_KJH4('SRF_CompInput_ViaM1M6', 'SRF_ViaM1M2', 'BND_Met1Layer')
		target_coord = tmp1[1][0][0][0]['_XY_up']
		## Approaching_coord
		tmp2 = self.get_param_KJH4('SRF_CompInputP_ViaM6M7', 'SRF_ViaM6M7', 'BND_Met6Layer')
		approaching_coord = tmp2[0][0][0][0]['_XY_down']
		## Sref coord
		tmp3 = self.get_param_KJH4('SRF_CompInputP_ViaM6M7')
		Scoord = tmp3[0][0]['_XY_origin']
		## Calculate
		New_Scoord = self.get_Scoord_KJH4(target_coord, approaching_coord, Scoord)
		tmpXY.append(New_Scoord)
		## Define
		self._DesignParameter['SRF_CompInputP_ViaM6M7']['_XYCoordinates'] = tmpXY
		###################################################################################################

		## BND_CompInputP_Hrz_M7
		## Boundary_element Generation
		## Generate Boundary_element: ex)LayerName: METAL1 / DIFF (_ODLayer) / POLY / PIMP (_PPLayer) / NWELL / SLVT LVT RVT HVT / OP(OPpress) / CONT (CA) / PCCRIT
		self._DesignParameter['BND_CompInputN_Hrz_M7'] = self._BoundaryElementDeclaration(
			_Layer=DesignParameters._LayerMapping['METAL7'][0],
			_Datatype=DesignParameters._LayerMapping['METAL7'][1],
			_XWidth=None,
			_YWidth=None,
			_XYCoordinates=[],
		)
		## Define Boundary_element _YWidth
		tmp1 = self.get_param_KJH4('SRF_CompInputN_ViaM6M7', 'SRF_ViaM6M7', 'BND_Met6Layer')
		self._DesignParameter['BND_CompInputN_Hrz_M7']['_YWidth'] = tmp1[0][0][0][0]['_Ywidth']

		## Define Boundary_element _XWidth
		self._DesignParameter['BND_CompInputN_Hrz_M7']['_XWidth'] = abs(tmp1[0][0][0][0]['_XY_left'][0] - tmpCent) + 200

		## Define Boundary_element _XYCoordinates
		self._DesignParameter['BND_CompInputN_Hrz_M7']['_XYCoordinates'] = [[0, 0]]

		## Calculate Sref XYcoord
		tmpXY = []
		## Calculate
		## Target_coord: _XY_type1
		target_coord = tmp1[0][0][0][0]['_XY_up_left']
		## Approaching_coord: _XY_type2
		tmp2 = self.get_param_KJH4('BND_CompInputN_Hrz_M7')
		approaching_coord = tmp2[0][0]['_XY_up_left']
		## Sref coord
		tmp3 = self.get_param_KJH4('BND_CompInputN_Hrz_M7')
		Scoord = tmp3[0][0]['_XY_origin']
		## Cal
		New_Scoord = self.get_Scoord_KJH4(target_coord, approaching_coord, Scoord)
		tmpXY.append(New_Scoord)
		## Define coordinates
		self._DesignParameter['BND_CompInputN_Hrz_M7']['_XYCoordinates'] = tmpXY
		###################################################################################################

		## BND_CompInputN_Hrz_M7
		## Boundary_element Generation
		## Generate Boundary_element: ex)LayerName: METAL1 / DIFF (_ODLayer) / POLY / PIMP (_PPLayer) / NWELL / SLVT LVT RVT HVT / OP(OPpress) / CONT (CA) / PCCRIT
		self._DesignParameter['BND_CompInputP_Hrz_M7'] = self._BoundaryElementDeclaration(
			_Layer=DesignParameters._LayerMapping['METAL7'][0],
			_Datatype=DesignParameters._LayerMapping['METAL7'][1],
			_XWidth=None,
			_YWidth=None,
			_XYCoordinates=[],
		)
		## Define Boundary_element _YWidth
		tmp1 = self.get_param_KJH4('SRF_CompInputP_ViaM6M7', 'SRF_ViaM6M7', 'BND_Met6Layer')
		self._DesignParameter['BND_CompInputP_Hrz_M7']['_YWidth'] = tmp1[0][0][0][0]['_Ywidth']

		## Define Boundary_element _XWidth
		self._DesignParameter['BND_CompInputP_Hrz_M7']['_XWidth'] = abs(tmp1[0][0][0][0]['_XY_right'][0] - tmpCent) + 200

		## Define Boundary_element _XYCoordinates
		self._DesignParameter['BND_CompInputP_Hrz_M7']['_XYCoordinates'] = [[0, 0]]

		## Calculate Sref XYcoord
		tmpXY = []
		## Calculate
		## Target_coord: _XY_type1
		target_coord = tmp1[0][0][0][0]['_XY_up_right']
		## Approaching_coord: _XY_type2
		tmp2 = self.get_param_KJH4('BND_CompInputP_Hrz_M7')
		approaching_coord = tmp2[0][0]['_XY_up_right']
		## Sref coord
		tmp3 = self.get_param_KJH4('BND_CompInputP_Hrz_M7')
		Scoord = tmp3[0][0]['_XY_origin']
		## Cal
		New_Scoord = self.get_Scoord_KJH4(target_coord, approaching_coord, Scoord)
		tmpXY.append(New_Scoord)
		## Define coordinates
		self._DesignParameter['BND_CompInputP_Hrz_M7']['_XYCoordinates'] = tmpXY
		###################################################################################################

		## BND_CompInputP_Vtc_IA
		## Boundary_element Generation
		## Generate Boundary_element: ex)LayerName: METAL1 / DIFF (_ODLayer) / POLY / PIMP (_PPLayer) / NWELL / SLVT LVT RVT HVT / OP(OPpress) / CONT (CA) / PCCRIT
		self._DesignParameter['BND_CompInputP_Vtc_IA'] = self._BoundaryElementDeclaration(
			_Layer=DesignParameters._LayerMapping['METAL8'][0],
			_Datatype=DesignParameters._LayerMapping['METAL8'][1],
			_XWidth=None,
			_YWidth=None,
			_XYCoordinates=[],
		)
		## Define Boundary_element _YWidth
		tmp1 = self.get_param_KJH4('BND_CompInputP_Hrz_M7')
		if _CDAC_FoldingTF == True:
			tmp2 = self.get_param_KJH4('SRF_CDAC_Pos', 'SRF_CDACWtDriver','BND_CDACUpperTopNode_Hrz_IA')
		else:
			tmp2 = self.get_param_KJH4('SRF_CDAC_Pos', 'SRF_CDACWtDriver', 'BND_CDACTopNode_Hrz_M7')
		self._DesignParameter['BND_CompInputP_Vtc_IA']['_YWidth'] = abs(tmp1[0][0]['_XY_up'][1] - tmp2[0][0][0][0]['_XY_up'][1])

		## Define Boundary_element _XWidth
		self._DesignParameter['BND_CompInputP_Vtc_IA']['_XWidth'] = 400

		## Define Boundary_element _XYCoordinates
		self._DesignParameter['BND_CompInputP_Vtc_IA']['_XYCoordinates'] = [[0, 0]]

		## Calculate Sref XYcoord
		tmpXY = []
		## Calculate
		## Target_coord: _XY_type1
		target_coord = tmp1[0][0]['_XY_up_left']
		## Approaching_coord: _XY_type2
		tmp2 = self.get_param_KJH4('BND_CompInputP_Vtc_IA')
		approaching_coord = tmp2[0][0]['_XY_down_left']
		## Sref coord
		tmp3 = self.get_param_KJH4('BND_CompInputP_Vtc_IA')
		Scoord = tmp3[0][0]['_XY_origin']
		## Cal
		New_Scoord = self.get_Scoord_KJH4(target_coord, approaching_coord, Scoord)
		tmpXY.append(New_Scoord)
		## Define coordinates
		self._DesignParameter['BND_CompInputP_Vtc_IA']['_XYCoordinates'] = tmpXY
		###################################################################################################

		## BND_CompInputN_Vtc_IA
		## Boundary_element Generation
		## Generate Boundary_element: ex)LayerName: METAL1 / DIFF (_ODLayer) / POLY / PIMP (_PPLayer) / NWELL / SLVT LVT RVT HVT / OP(OPpress) / CONT (CA) / PCCRIT
		self._DesignParameter['BND_CompInputN_Vtc_IA'] = self._BoundaryElementDeclaration(
			_Layer=DesignParameters._LayerMapping['METAL8'][0],
			_Datatype=DesignParameters._LayerMapping['METAL8'][1],
			_XWidth=None,
			_YWidth=None,
			_XYCoordinates=[],
		)
		## Define Boundary_element _YWidth
		tmp1 = self.get_param_KJH4('BND_CompInputN_Hrz_M7')
		if _CDAC_FoldingTF == True:
			tmp2 = self.get_param_KJH4('SRF_CDAC_Neg', 'SRF_CDACWtDriver', 'BND_CDACUpperTopNode_Hrz_IA')
		else:
			tmp2 = self.get_param_KJH4('SRF_CDAC_Neg', 'SRF_CDACWtDriver', 'BND_CDACTopNode_Hrz_M7')
		self._DesignParameter['BND_CompInputN_Vtc_IA']['_YWidth'] = abs(tmp1[0][0]['_XY_down'][1] - tmp2[0][0][0][0]['_XY_up'][1])

		## Define Boundary_element _XWidth
		self._DesignParameter['BND_CompInputN_Vtc_IA']['_XWidth'] = 400

		## Define Boundary_element _XYCoordinates
		self._DesignParameter['BND_CompInputN_Vtc_IA']['_XYCoordinates'] = [[0, 0]]

		## Calculate Sref XYcoord
		tmpXY = []
		## Calculate
		## Target_coord: _XY_type1
		target_coord = tmp1[0][0]['_XY_down_right']
		## Approaching_coord: _XY_type2
		tmp2 = self.get_param_KJH4('BND_CompInputN_Vtc_IA')
		approaching_coord = tmp2[0][0]['_XY_up_right']
		## Sref coord
		tmp3 = self.get_param_KJH4('BND_CompInputN_Vtc_IA')
		Scoord = tmp3[0][0]['_XY_origin']
		## Cal
		New_Scoord = self.get_Scoord_KJH4(target_coord, approaching_coord, Scoord)
		tmpXY.append(New_Scoord)
		## Define coordinates
		self._DesignParameter['BND_CompInputN_Vtc_IA']['_XYCoordinates'] = tmpXY
		###################################################################################################

		if _CDAC_FoldingTF == True:
			## BND_CompInputExten_Hrz_IA
			## Boundary_element Generation
			## Generate Boundary_element: ex)LayerName: METAL1 / DIFF (_ODLayer) / POLY / PIMP (_PPLayer) / NWELL / SLVT LVT RVT HVT / OP(OPpress) / CONT (CA) / PCCRIT
			self._DesignParameter['BND_CompInputExten_Hrz_IA'] = self._BoundaryElementDeclaration(
				_Layer=DesignParameters._LayerMapping['METAL8'][0],
				_Datatype=DesignParameters._LayerMapping['METAL8'][1],
				_XWidth=None,
				_YWidth=None,
				_XYCoordinates=[],
			)
			## Define Boundary_element _YWidth
			tmp1_1 = self.get_param_KJH4('SRF_CDAC_Pos', 'SRF_CDACWtDriver', 'BND_CDACLowerTopNode_Hrz_IA')
			tmp1_2 = self.get_param_KJH4('SRF_CDAC_Pos', 'SRF_CDACWtDriver', 'BND_CDACUpperTopNode_Hrz_IA')
			tmp1_3 = self.get_param_KJH4('SRF_CDAC_Neg', 'SRF_CDACWtDriver', 'BND_CDACUpperTopNode_Hrz_IA')
			tmp1_4 = self.get_param_KJH4('SRF_CDAC_Neg', 'SRF_CDACWtDriver', 'BND_CDACLowerTopNode_Hrz_IA')
			tmp2 = self.get_param_KJH4('BND_CompInputN_Vtc_IA')
			self._DesignParameter['BND_CompInputExten_Hrz_IA']['_YWidth'] = tmp1_1[0][0][0][0]['_Ywidth']

			## Define Boundary_element _XWidth
			self._DesignParameter['BND_CompInputExten_Hrz_IA']['_XWidth'] = abs(tmp1_1[0][0][0][0]['_XY_right'][0] - tmp2[0][0]['_XY_left'][0])

			## Define Boundary_element _XYCoordinates
			self._DesignParameter['BND_CompInputExten_Hrz_IA']['_XYCoordinates'] = [[0, 0]]

			## Calculate Sref XYcoord
			tmpXY = []
			## Calculate
			## Approaching_coord: _XY_type2
			tmp3 = self.get_param_KJH4('BND_CompInputExten_Hrz_IA')
			approaching_coord = tmp3[0][0]['_XY_down_left']
			## Sref coord
			tmp4 = self.get_param_KJH4('BND_CompInputExten_Hrz_IA')
			Scoord = tmp4[0][0]['_XY_origin']
			## Cal
			## Target_coord1: _XY_type1
			target_coord = [tmp2[0][0]['_XY_left'][0], tmp1_1[0][0][0][0]['_XY_down'][1]]
			New_Scoord = self.get_Scoord_KJH4(target_coord, approaching_coord, Scoord)
			tmpXY.append(New_Scoord)
			## Target_coord2: _XY_type1
			target_coord = [tmp2[0][0]['_XY_left'][0], tmp1_2[0][0][0][0]['_XY_down'][1]]
			New_Scoord = self.get_Scoord_KJH4(target_coord, approaching_coord, Scoord)
			tmpXY.append(New_Scoord)
			## Target_coord3: _XY_type1
			target_coord = [tmp2[0][0]['_XY_left'][0], tmp1_3[0][0][0][0]['_XY_up'][1]]
			New_Scoord = self.get_Scoord_KJH4(target_coord, approaching_coord, Scoord)
			tmpXY.append(New_Scoord)
			## Target_coord4: _XY_type1
			target_coord = [tmp2[0][0]['_XY_left'][0], tmp1_4[0][0][0][0]['_XY_up'][1]]
			New_Scoord = self.get_Scoord_KJH4(target_coord, approaching_coord, Scoord)
			tmpXY.append(New_Scoord)
			## Define coordinates
			self._DesignParameter['BND_CompInputExten_Hrz_IA']['_XYCoordinates'] = tmpXY
		###################################################################################################

		### SRF_CompInput_ViaM7M8
		## Sref generation: ViaX
		## Define ViaX Parameter
		_Caculation_Parameters = copy.deepcopy(A02_ViaStack_KJH3._ViaStack._ParametersForDesignCalculation)
		_Caculation_Parameters['_Layer1'] = 7
		_Caculation_Parameters['_Layer2'] = 8
		_Caculation_Parameters['_COX'] = 1
		_Caculation_Parameters['_COY'] = 2

		## Sref ViaX declaration
		self._DesignParameter['SRF_CompInput_ViaM7M8'] = self._SrefElementDeclaration(_DesignObj=A02_ViaStack_KJH3._ViaStack(_DesignParameter=None, _Name='{}:SRF_CompInput_ViaM7M8'.format(_Name)))[0]

		## Define Sref Relection
		self._DesignParameter['SRF_CompInput_ViaM7M8']['_Reflect'] = [0, 0, 0]

		## Define Sref Angle
		self._DesignParameter['SRF_CompInput_ViaM7M8']['_Angle'] = 0

		## Generate Metal(x), Metal(x+1) and C0(Viax) layer:  Option: _CalculateDesignParameter, _CalculateDesignParameterXmin, _CalculateDesignParameterYmin, _CalculateDesignParameterXYsame
		self._DesignParameter['SRF_CompInput_ViaM7M8']['_DesignObj']._CalculateDesignParameterXmin(**_Caculation_Parameters)

		## Calculate Sref XYcoord
		tmpXY = []
		## initialized Sref coordinate
		self._DesignParameter['SRF_CompInput_ViaM7M8']['_XYCoordinates'] = [[0, 0]]
		## Calculate
		## Target_coord
		tmp1x = self.get_param_KJH4('BND_CompInputP_Vtc_IA')
		tmp1y = self.get_param_KJH4('BND_CompInputP_Hrz_M7')
		target_coord = [tmp1x[0][0]['_XY_right'][0], tmp1y[0][0]['_XY_up'][1]]
		## Approaching_coord
		tmp2 = self.get_param_KJH4('SRF_CompInput_ViaM7M8', 'SRF_ViaM7M8', 'BND_Met7Layer')
		approaching_coord = tmp2[0][0][0][0]['_XY_down_right']
		## Sref coord
		tmp3 = self.get_param_KJH4('SRF_CompInput_ViaM7M8')
		Scoord = tmp3[0][0]['_XY_origin']
		## Calculate
		New_Scoord = self.get_Scoord_KJH4(target_coord, approaching_coord, Scoord)
		tmpXY.append(New_Scoord)

		## Calc2
		approaching_coord = tmp2[0][0][0][0]['_XY_up_left']
		tmp1x = self.get_param_KJH4('BND_CompInputN_Vtc_IA')
		tmp1y = self.get_param_KJH4('BND_CompInputN_Hrz_M7')
		target_coord = [tmp1x[0][0]['_XY_left'][0], tmp1y[0][0]['_XY_down'][1]]
		New_Scoord = self.get_Scoord_KJH4(target_coord, approaching_coord, Scoord)
		tmpXY.append(New_Scoord)

		## Define
		self._DesignParameter['SRF_CompInput_ViaM7M8']['_XYCoordinates'] = tmpXY
		###################################################################################################

		### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###
		## BootSW CLK Signal Path Generation
		#### BND_BootSWCLKSignalPath_Hrz_M5
		## Boundary_element Generation
		## Generate Boundary_element: ex)LayerName: METAL1 / DIFF (_ODLayer) / POLY / PIMP (_PPLayer) / NWELL / SLVT LVT RVT HVT / OP(OPpress) / CONT (CA) / PCCRIT
		self._DesignParameter['BND_BootSWCLKSignalPath_Hrz_M5'] = self._BoundaryElementDeclaration(
			_Layer=DesignParameters._LayerMapping['METAL5'][0],
			_Datatype=DesignParameters._LayerMapping['METAL5'][1],
			_XWidth=None,
			_YWidth=None,
			_XYCoordinates=[],
		)
		## Define Boundary_element _XWidth
		tmp1 = self.get_param_KJH4('SRF_SARLogicWtComparator', 'BND_CLKSampANDIn_Vtc_M4')
		tmp2 = self.get_param_KJH4('SRF_BootSW_Neg', 'SRF_C13_00', 'SRF_C11', 'BND_Tr6Tr11GateRouting_Vtc_M2')
		self._DesignParameter['BND_BootSWCLKSignalPath_Hrz_M5']['_XWidth'] = abs(tmp1[0][0][0]['_XY_right'][0] - tmp2[0][0][0][0][0]['_XY_cent'][0])

		## Define Boundary_element _XWidth
		self._DesignParameter['BND_BootSWCLKSignalPath_Hrz_M5']['_YWidth'] = 50

		## Define Boundary_element _XYCoordinates
		self._DesignParameter['BND_BootSWCLKSignalPath_Hrz_M5']['_XYCoordinates'] = [[0, 0]]

		## Calculate Sref XYcoord
		tmpXY = []
		## Calculate
		## Target_coord: _XY_type1
		tmp1y = self.get_param_KJH4('SRF_SARLogicWtComparator', 'SRF_Comparator', 'BND_SlicerCLKInput_Hrz_M3')
		target_coord = [tmp1[0][0][0]['_XY_right'][0], tmp1y[0][0][0][0]['_XY_down'][1]]
		## Approaching_coord: _XY_type2
		tmp2 = self.get_param_KJH4('BND_BootSWCLKSignalPath_Hrz_M5')
		approaching_coord = tmp2[0][0]['_XY_down_right']
		## Sref coord
		tmp3 = self.get_param_KJH4('BND_BootSWCLKSignalPath_Hrz_M5')
		Scoord = tmp3[0][0]['_XY_origin']
		SpaceBtwCLKCompInAndCLKBootSWIn = 50
		Scoord[1] = Scoord[1] + SpaceBtwCLKCompInAndCLKBootSWIn
		## Cal
		New_Scoord = self.get_Scoord_KJH4(target_coord, approaching_coord, Scoord)
		tmpXY.append(New_Scoord)
		## Define coordinates
		self._DesignParameter['BND_BootSWCLKSignalPath_Hrz_M5']['_XYCoordinates'] = tmpXY
		###################################################################################################

		#### BND_BootSWCLKSignalPath_Vtc_M4
		## Boundary_element Generation
		## Generate Boundary_element: ex)LayerName: METAL1 / DIFF (_ODLayer) / POLY / PIMP (_PPLayer) / NWELL / SLVT LVT RVT HVT / OP(OPpress) / CONT (CA) / PCCRIT
		self._DesignParameter['BND_BootSWCLKSignalPath_Vtc_M4'] = self._BoundaryElementDeclaration(
			_Layer=DesignParameters._LayerMapping['METAL4'][0],
			_Datatype=DesignParameters._LayerMapping['METAL4'][1],
			_XWidth=None,
			_YWidth=None,
			_XYCoordinates=[],
		)
		## Define Boundary_element _XWidth
		self._DesignParameter['BND_BootSWCLKSignalPath_Vtc_M4']['_XWidth'] = 50

		## Define Boundary_element _XWidth
		tmp1 = self.get_param_KJH4('BND_BootSWCLKSignalPath_Hrz_M5')
		tmp2 = self.get_param_KJH4('SRF_SARLogicWtComparator','BND_BufCLKSampIn_Vtc_M4')
		self._DesignParameter['BND_BootSWCLKSignalPath_Vtc_M4']['_YWidth'] = abs(tmp2[0][0][0]['_XY_down'][1] - tmp1[0][0]['_XY_down'][1])

		## Define Boundary_element _XYCoordinates
		self._DesignParameter['BND_BootSWCLKSignalPath_Vtc_M4']['_XYCoordinates'] = [[0, 0]]

		## Calculate Sref XYcoord
		tmpXY = []
		## Calculate
		## Target_coord: _XY_type1
		tmp1 = self.get_param_KJH4('BND_BootSWCLKSignalPath_Hrz_M5')
		target_coord = tmp1[0][0]['_XY_down_right']
		## Approaching_coord: _XY_type2
		tmp2 = self.get_param_KJH4('BND_BootSWCLKSignalPath_Vtc_M4')
		approaching_coord = tmp2[0][0]['_XY_down_right']
		## Sref coord
		tmp3 = self.get_param_KJH4('BND_BootSWCLKSignalPath_Vtc_M4')
		Scoord = tmp3[0][0]['_XY_origin']
		## Cal
		New_Scoord = self.get_Scoord_KJH4(target_coord, approaching_coord, Scoord)
		tmpXY.append(New_Scoord)
		## Define coordinates
		self._DesignParameter['BND_BootSWCLKSignalPath_Vtc_M4']['_XYCoordinates'] = tmpXY

		###################################################################################################

		### SRF_BootSWCLKSignalPath_ViaM4M5
		## Sref generation: ViaX
		## Define ViaX Parameter
		_Caculation_Parameters = copy.deepcopy(A02_ViaStack_KJH3._ViaStack._ParametersForDesignCalculation)
		_Caculation_Parameters['_Layer1'] = 4
		_Caculation_Parameters['_Layer2'] = 5
		_Caculation_Parameters['_COX'] = 1
		_Caculation_Parameters['_COY'] = 4

		## Sref ViaX declaration
		self._DesignParameter['SRF_BootSWCLKSignalPath_ViaM4M5'] = self._SrefElementDeclaration(_DesignObj=A02_ViaStack_KJH3._ViaStack(_DesignParameter=None, _Name='{}:SRF_BootSWCLKSignalPath_ViaM4M5'.format(_Name)))[0]

		## Define Sref Relection
		self._DesignParameter['SRF_BootSWCLKSignalPath_ViaM4M5']['_Reflect'] = [0, 0, 0]

		## Define Sref Angle
		self._DesignParameter['SRF_BootSWCLKSignalPath_ViaM4M5']['_Angle'] = 0

		## Generate Metal(x), Metal(x+1) and C0(Viax) layer:  Option: _CalculateDesignParameter, _CalculateDesignParameterXmin, _CalculateDesignParameterYmin, _CalculateDesignParameterXYsame
		self._DesignParameter['SRF_BootSWCLKSignalPath_ViaM4M5']['_DesignObj']._CalculateDesignParameterXmin(**_Caculation_Parameters)

		## Calculate Sref XYcoord
		tmpXY = []
		## initialized Sref coordinate
		self._DesignParameter['SRF_BootSWCLKSignalPath_ViaM4M5']['_XYCoordinates'] = [[0, 0]]
		## Calculate
		## Target_coord
		tmp1 = self.get_param_KJH4('BND_BootSWCLKSignalPath_Hrz_M5')
		target_coord = tmp1[0][0]['_XY_down_right']
		## Approaching_coord
		tmp2 = self.get_param_KJH4('SRF_BootSWCLKSignalPath_ViaM4M5', 'SRF_ViaM4M5', 'BND_Met4Layer')
		approaching_coord = tmp2[0][0][0][0]['_XY_down_right']
		## Sref coord
		tmp3 = self.get_param_KJH4('SRF_BootSWCLKSignalPath_ViaM4M5')
		Scoord = tmp3[0][0]['_XY_origin']
		## Calculate
		New_Scoord = self.get_Scoord_KJH4(target_coord, approaching_coord, Scoord)
		tmpXY.append(New_Scoord)

		## Define
		self._DesignParameter['SRF_BootSWCLKSignalPath_ViaM4M5']['_XYCoordinates'] = tmpXY
		###################################################################################################

		### BND_Tr6Tr11GateRouteExten_Vtc_M4; Connecting BootSW Neg, Pos and 'BND_BootSWCLKSignalPath_Hrz_M5'
		## Boundary_element Generation
		## Generate Boundary_element: ex)LayerName: METAL1 / DIFF (_ODLayer) / POLY / PIMP (_PPLayer) / NWELL / SLVT LVT RVT HVT / OP(OPpress) / CONT (CA) / PCCRIT
		self._DesignParameter['BND_Tr6Tr11GateRouteExten_Vtc_M4'] = self._BoundaryElementDeclaration(
			_Layer=DesignParameters._LayerMapping['METAL4'][0],
			_Datatype=DesignParameters._LayerMapping['METAL4'][1],
			_XWidth=None,
			_YWidth=None,
			_XYCoordinates=[],
		)
		## Define Boundary_element _YWidth
		tmp1 = self.get_param_KJH4('SRF_BootSW_Pos', 'SRF_C13_00', 'SRF_C11', 'BND_Tr6Tr11GateRouting_Vtc_M2')
		tmp2 = self.get_param_KJH4('SRF_BootSW_Neg', 'SRF_C13_00', 'SRF_C11', 'BND_Tr6Tr11GateRouting_Vtc_M2')
		overlapAmount = 400
		self._DesignParameter['BND_Tr6Tr11GateRouteExten_Vtc_M4']['_YWidth'] = abs(tmp1[0][0][0][0][0]['_XY_up'][1] - tmp2[0][0][0][0][0]['_XY_up'][1]) + overlapAmount

		## Define Boundary_element _XWidth
		self._DesignParameter['BND_Tr6Tr11GateRouteExten_Vtc_M4']['_XWidth'] = tmp1[0][0][0][0][0]['_Xwidth']

		## Define Boundary_element _XYCoordinates
		self._DesignParameter['BND_Tr6Tr11GateRouteExten_Vtc_M4']['_XYCoordinates'] = [[0, 0]]

		## Calculate Sref XYcoord
		tmpXY = []
		## Calculate
		## Target_coord: _XY_type1
		target_coord = tmp2[0][0][0][0][0]['_XY_up_right']
		## Approaching_coord: _XY_type2
		tmp2 = self.get_param_KJH4('BND_Tr6Tr11GateRouteExten_Vtc_M4')
		approaching_coord = tmp2[0][0]['_XY_down_right']
		## Sref coord
		tmp3 = self.get_param_KJH4('BND_Tr6Tr11GateRouteExten_Vtc_M4')
		Scoord = tmp3[0][0]['_XY_origin']
		Scoord[1] = Scoord[1] - int(overlapAmount / 2)
		## Cal
		New_Scoord = self.get_Scoord_KJH4(target_coord, approaching_coord, Scoord)
		tmpXY.append(New_Scoord)
		## Define coordinates
		self._DesignParameter['BND_Tr6Tr11GateRouteExten_Vtc_M4']['_XYCoordinates'] = tmpXY
		###################################################################################################

		### BND_BootSWCLKSignalPath_Vtc_M5; Connecting BootSW Neg, Pos and 'BND_BootSWCLKSignalPath_Hrz_M5'
		## Boundary_element Generation
		## Generate Boundary_element: ex)LayerName: METAL1 / DIFF (_ODLayer) / POLY / PIMP (_PPLayer) / NWELL / SLVT LVT RVT HVT / OP(OPpress) / CONT (CA) / PCCRIT
		self._DesignParameter['BND_BootSWCLKSignalPath_Vtc_M5'] = self._BoundaryElementDeclaration(
			_Layer=DesignParameters._LayerMapping['METAL5'][0],
			_Datatype=DesignParameters._LayerMapping['METAL5'][1],
			_XWidth=None,
			_YWidth=None,
			_XYCoordinates=[],
		)
		## Define Boundary_element _YWidth
		tmp1 = self.get_param_KJH4('BND_Tr6Tr11GateRouteExten_Vtc_M4')
		tmp2 = self.get_param_KJH4('BND_BootSWCLKSignalPath_Hrz_M5')
		self._DesignParameter['BND_BootSWCLKSignalPath_Vtc_M5']['_YWidth'] = abs(tmp1[0][0]['_XY_cent'][1] - tmp2[0][0]['_XY_up'][1])

		## Define Boundary_element _XWidth
		self._DesignParameter['BND_BootSWCLKSignalPath_Vtc_M5']['_XWidth'] = 50

		## Define Boundary_element _XYCoordinates
		self._DesignParameter['BND_BootSWCLKSignalPath_Vtc_M5']['_XYCoordinates'] = [[0, 0]]

		## Calculate Sref XYcoord
		tmpXY = []
		## Calculate
		## Target_coord: _XY_type1
		target_coord = tmp2[0][0]['_XY_up_left']
		## Approaching_coord: _XY_type2
		tmp2 = self.get_param_KJH4('BND_BootSWCLKSignalPath_Vtc_M5')
		approaching_coord = tmp2[0][0]['_XY_up']
		## Sref coord
		tmp3 = self.get_param_KJH4('BND_BootSWCLKSignalPath_Vtc_M5')
		Scoord = tmp3[0][0]['_XY_origin']
		## Cal
		New_Scoord = self.get_Scoord_KJH4(target_coord, approaching_coord, Scoord)
		tmpXY.append(New_Scoord)
		## Define coordinates
		self._DesignParameter['BND_BootSWCLKSignalPath_Vtc_M5']['_XYCoordinates'] = tmpXY
		###################################################################################################

		### SRF_Tr6Tr11GateRouteExten_ViaM2M4
		## Sref generation: ViaX
		## Define ViaX Parameter
		_Caculation_Parameters = copy.deepcopy(A02_ViaStack_KJH3._ViaStack._ParametersForDesignCalculation)
		_Caculation_Parameters['_Layer1'] = 2
		_Caculation_Parameters['_Layer2'] = 4
		_Caculation_Parameters['_COX'] = None
		_Caculation_Parameters['_COY'] = None

		## Sref ViaX declaration
		self._DesignParameter['SRF_Tr6Tr11GateRouteExten_ViaM2M4'] = self._SrefElementDeclaration(_DesignObj=A02_ViaStack_KJH3._ViaStack(_DesignParameter=None, _Name='{}:SRF_Tr6Tr11GateRouteExten_ViaM2M4'.format(_Name)))[0]

		## Define Sref Relection
		self._DesignParameter['SRF_Tr6Tr11GateRouteExten_ViaM2M4']['_Reflect'] = [0, 0, 0]

		## Define Sref Angle
		self._DesignParameter['SRF_Tr6Tr11GateRouteExten_ViaM2M4']['_Angle'] = 0

		## Calcuate Overlapped XYcoord
		tmp2 = self.get_param_KJH4('BND_Tr6Tr11GateRouteExten_Vtc_M4')

		## Calcuate _COX and _COY:  None or 'MinEnclosureX' or 'MinEnclosureY' or 'SameEnclosure'
		_COX, _COY = self._CalculateNumViaByXYWidth(tmp2[0][0]['_Xwidth'], int(overlapAmount / 2), None)

		## Define _COX and _COY
		_Caculation_Parameters['_COX'] = _COX
		_Caculation_Parameters['_COY'] = _COY

		## Generate Metal(x), Metal(x+1) and C0(Viax) layer:  Option: _CalculateDesignParameter, _CalculateDesignParameterXmin, _CalculateDesignParameterYmin, _CalculateDesignParameterXYsame
		self._DesignParameter['SRF_Tr6Tr11GateRouteExten_ViaM2M4']['_DesignObj']._CalculateDesignParameter(**_Caculation_Parameters)

		## Calculate Sref XYcoord
		tmpXY = []
		## initialized Sref coordinate
		self._DesignParameter['SRF_Tr6Tr11GateRouteExten_ViaM2M4']['_XYCoordinates'] = [[0, 0]]
		## Calculate
		## Target_coord
		tmp1 = self.get_param_KJH4('BND_Tr6Tr11GateRouteExten_Vtc_M4')
		target_coord = tmp1[0][0]['_XY_up']
		## Approaching_coord
		tmp2 = self.get_param_KJH4('SRF_Tr6Tr11GateRouteExten_ViaM2M4', 'SRF_ViaM2M3', 'BND_Met2Layer')
		approaching_coord = tmp2[0][0][0][0]['_XY_up']
		## Sref coord
		tmp3 = self.get_param_KJH4('SRF_Tr6Tr11GateRouteExten_ViaM2M4')
		Scoord = tmp3[0][0]['_XY_origin']
		## Calculate
		New_Scoord = self.get_Scoord_KJH4(target_coord, approaching_coord, Scoord)
		tmpXY.append(New_Scoord)
		## Calc2
		target_coord = tmp1[0][0]['_XY_down']
		approaching_coord = tmp2[0][0][0][0]['_XY_down']
		New_Scoord = self.get_Scoord_KJH4(target_coord, approaching_coord, Scoord)
		tmpXY.append(New_Scoord)
		## Define
		self._DesignParameter['SRF_Tr6Tr11GateRouteExten_ViaM2M4']['_XYCoordinates'] = tmpXY
		###################################################################################################

		### SRF_BootSWCLKSignalCent_ViaM4M5
		## Sref generation: ViaX
		## Define ViaX Parameter
		_Caculation_Parameters = copy.deepcopy(A02_ViaStack_KJH3._ViaStack._ParametersForDesignCalculation)
		_Caculation_Parameters['_Layer1'] = 4
		_Caculation_Parameters['_Layer2'] = 5
		_Caculation_Parameters['_COX'] = 1
		_Caculation_Parameters['_COY'] = 3

		## Sref ViaX declaration
		self._DesignParameter['SRF_BootSWCLKSignalCent_ViaM4M5'] = self._SrefElementDeclaration(_DesignObj=A02_ViaStack_KJH3._ViaStack(_DesignParameter=None, _Name='{}:SRF_BootSWCLKSignalCent_ViaM4M5'.format(_Name)))[0]

		## Define Sref Relection
		self._DesignParameter['SRF_BootSWCLKSignalCent_ViaM4M5']['_Reflect'] = [0, 0, 0]

		## Define Sref Angle
		self._DesignParameter['SRF_BootSWCLKSignalCent_ViaM4M5']['_Angle'] = 0

		## Generate Metal(x), Metal(x+1) and C0(Viax) layer:  Option: _CalculateDesignParameter, _CalculateDesignParameterXmin, _CalculateDesignParameterYmin, _CalculateDesignParameterXYsame
		self._DesignParameter['SRF_BootSWCLKSignalCent_ViaM4M5']['_DesignObj']._CalculateDesignParameterXmin(**_Caculation_Parameters)

		## Calculate Sref XYcoord
		tmpXY = []
		## initialized Sref coordinate
		self._DesignParameter['SRF_BootSWCLKSignalCent_ViaM4M5']['_XYCoordinates'] = [[0, 0]]
		## Calculate
		## Target_coord
		tmp1 = self.get_param_KJH4('BND_BootSWCLKSignalPath_Vtc_M5')
		target_coord = tmp1[0][0]['_XY_down']
		## Approaching_coord
		tmp2 = self.get_param_KJH4('SRF_BootSWCLKSignalCent_ViaM4M5', 'SRF_ViaM4M5', 'BND_Met4Layer')
		approaching_coord = tmp2[0][0][0][0]['_XY_cent']
		## Sref coord
		tmp3 = self.get_param_KJH4('SRF_BootSWCLKSignalCent_ViaM4M5')
		Scoord = tmp3[0][0]['_XY_origin']
		## Calculate
		New_Scoord = self.get_Scoord_KJH4(target_coord, approaching_coord, Scoord)
		tmpXY.append(New_Scoord)

		## Define
		self._DesignParameter['SRF_BootSWCLKSignalCent_ViaM4M5']['_XYCoordinates'] = tmpXY
		###################################################################################################

		#### Bootstrapped Sampler CLKB Inverter generation
		## Copy Calculation_Parameters from low-level-block ex)copy.deepcopy(B16_nmos_power_v2._NMOS_POWER._ParametersForDesignCalculation)
		_Caculation_Parameters = copy.deepcopy(D00_00_Inverter_KJH._Inverter._ParametersForDesignCalculation)
		## Define Calculation_Parameters ex) _Caculation_Parameters['_NMOSPOWER_PbodyContact_1_Length']  = _NMOSPOWER_PbodyContact_1_Length
		## Inverter
			# Common
		_Caculation_Parameters['_XVT'] = _Sampler_ClkbGenInv_XVT
			# Nmos
		_Caculation_Parameters['_NMOS_NumberofGate'] = _Sampler_ClkbGenInv_NMOS_NumberofGate
		_Caculation_Parameters['_NMOS_ChannelWidth'] = _Sampler_ClkbGenInv_NMOS_ChannelWidth
		_Caculation_Parameters['_NMOS_ChannelLength'] = _Sampler_ClkbGenInv_NMOS_ChannelLength
			# Pmos
		_Caculation_Parameters['_PMOS_NumberofGate'] = _Sampler_ClkbGenInv_PMOS_NumberofGate
		_Caculation_Parameters['_PMOS_ChannelWidth'] = _Sampler_ClkbGenInv_PMOS_ChannelWidth
		_Caculation_Parameters['_PMOS_ChannelLength'] = _Sampler_ClkbGenInv_PMOS_ChannelLength
			# Body
		_Caculation_Parameters['_NMOS_Pbody_XvtTop2Pbody'] = _Sampler_ClkbGenInv_NMOS_Pbody_XvtTop2Pbody
		_Caculation_Parameters['_PMOS_Nbody_Xvtdown2Nbody'] = _Sampler_ClkbGenInv_PMOS_Nbody_Xvtdown2Nbody
			# Height
		_Caculation_Parameters['_PMOSXvt2NMOSXvt'] = _Sampler_ClkbGenInv_PMOSXvt2NMOSXvt


		## Sref ViaX declaration
		self._DesignParameter['SRF_SampCLKBInverter'] = self._SrefElementDeclaration(_DesignObj=D00_00_Inverter_KJH._Inverter(_DesignParameter=None, _Name='{}:SRF_SampCLKBInverter'.format(_Name)))[0]

		## Define Sref Relection
		self._DesignParameter['SRF_SampCLKBInverter']['_Reflect'] = [1, 0, 0]

		## Define Sref Angle
		self._DesignParameter['SRF_SampCLKBInverter']['_Angle'] = 180

		## Generate Metal(x), Metal(x+1) and C0(Viax) layer:  Option: _CalculateDesignParameter, _CalculateDesignParameterXmin, _CalculateDesignParameterYmin, _CalculateDesignParameterXYsame
		self._DesignParameter['SRF_SampCLKBInverter']['_DesignObj']._CalculateDesignParameter(**_Caculation_Parameters)

		## Calculate Sref XYcoord
		tmpXY = []
		## initialized Sref coordinate
		self._DesignParameter['SRF_SampCLKBInverter']['_XYCoordinates'] = [[0, 0]]
		## Calculate
		## Target_coord
		tmp1x = self.get_param_KJH4('SRF_BootSW_Pos', 'SRF_C13_00', 'SRF_C11', 'SRF_Tr11', 'SRF_Nbodyring', 'SRF_NbodyLeft', 'SRF_NbodyContactPhyLen', 'BND_Met1Layer')
		target_coord = [tmp1x[0][0][0][0][0][0][0][0][0]['_XY_left'][0], centY]
		## Approaching_coord
		tmp2x = self.get_param_KJH4('SRF_SampCLKBInverter', 'SRF_Nbody', 'SRF_NbodyContactPhyLen', 'BND_Met1Layer')
		tmp2y = self.get_param_KJH4('SRF_SampCLKBInverter', 'SRF_Pbody', 'SRF_PbodyContactPhyLen', 'BND_Met1Layer')
		tmp2y_1 = int((tmp2y[0][0][0][0][0]['_XY_down'][1] + tmp2x[0][0][0][0][0]['_XY_up'][1]) / 2)
		approaching_coord = [tmp2x[0][0][0][0][0]['_XY_left'][0], tmp2y_1]
		## Sref coord
		tmp3 = self.get_param_KJH4('SRF_SampCLKBInverter')
		Scoord = tmp3[0][0]['_XY_origin']
		SpaceBtwInvBodyAndGuardring = 500
		Scoord[0] = Scoord[0] - SpaceBtwInvBodyAndGuardring
		## Calculate
		New_Scoord = self.get_Scoord_KJH4(target_coord, approaching_coord, Scoord)
		tmpXY.append(New_Scoord)

		## Define
		self._DesignParameter['SRF_SampCLKBInverter']['_XYCoordinates'] = tmpXY
		###################################################################################################

		### BND_BootSWCLKB_Vtc_M2; Connecting Output of SRF_SampCLKBInverter and 'BND_BootSWCLKSignalPath_Hrz_M5'
		## Boundary_element Generation
		## Generate Boundary_element: ex)LayerName: METAL1 / DIFF (_ODLayer) / POLY / PIMP (_PPLayer) / NWELL / SLVT LVT RVT HVT / OP(OPpress) / CONT (CA) / PCCRIT
		self._DesignParameter['BND_BootSWCLKB_Vtc_M2'] = self._BoundaryElementDeclaration(
			_Layer=DesignParameters._LayerMapping['METAL2'][0],
			_Datatype=DesignParameters._LayerMapping['METAL2'][1],
			_XWidth=None,
			_YWidth=None,
			_XYCoordinates=[],
		)
		## Define Boundary_element _YWidth
		tmp1 = self.get_param_KJH4('SRF_BootSW_Pos', 'SRF_C13_00', 'SRF_C07', 'BND_Tr12Tr3Tr10_Gate_Hrz_M2')
		tmp2 = self.get_param_KJH4('SRF_BootSW_Neg', 'SRF_C13_00', 'SRF_C07', 'BND_Tr12Tr3Tr10_Gate_Hrz_M2')
		self._DesignParameter['BND_BootSWCLKB_Vtc_M2']['_YWidth'] = abs(tmp1[0][0][0][0][0]['_XY_down'][1] - tmp2[0][0][0][0][0]['_XY_down'][1])

		## Define Boundary_element _XWidth
		self._DesignParameter['BND_BootSWCLKB_Vtc_M2']['_XWidth'] = 100

		## Define Boundary_element _XYCoordinates
		self._DesignParameter['BND_BootSWCLKB_Vtc_M2']['_XYCoordinates'] = [[0, 0]]

		## Calculate Sref XYcoord
		tmpXY = []
		## Calculate
		## Target_coord: _XY_type1
		target_coord = tmp2[0][0][0][0][0]['_XY_down']
		## Approaching_coord: _XY_type2
		tmp2 = self.get_param_KJH4('BND_BootSWCLKB_Vtc_M2')
		approaching_coord = tmp2[0][0]['_XY_down']
		## Sref coord
		tmp3 = self.get_param_KJH4('BND_BootSWCLKB_Vtc_M2')
		Scoord = tmp3[0][0]['_XY_origin']
		## Cal
		New_Scoord = self.get_Scoord_KJH4(target_coord, approaching_coord, Scoord)
		tmpXY.append(New_Scoord)
		## Define coordinates
		self._DesignParameter['BND_BootSWCLKB_Vtc_M2']['_XYCoordinates'] = tmpXY
		###################################################################################################

		### BND_BootSWCLKBInvIn_Hrz_M3; Connecting Output of SRF_SampCLKBInverter and 'BND_BootSWCLKSignalPath_Hrz_M5'
		## Boundary_element Generation
		## Generate Boundary_element: ex)LayerName: METAL1 / DIFF (_ODLayer) / POLY / PIMP (_PPLayer) / NWELL / SLVT LVT RVT HVT / OP(OPpress) / CONT (CA) / PCCRIT
		self._DesignParameter['BND_BootSWCLKBInvIn_Hrz_M3'] = self._BoundaryElementDeclaration(
			_Layer=DesignParameters._LayerMapping['METAL3'][0],
			_Datatype=DesignParameters._LayerMapping['METAL3'][1],
			_XWidth=None,
			_YWidth=None,
			_XYCoordinates=[],
		)
		## Define Boundary_element _XWidth
		# tmp1 = self.get_param_KJH4('SRF_BootSW_Pos','SRF_C13_00','SRF_C07','SRF_Tr12Tr3Tr10','SRF_Tr12Tr3Tr10_Gate_ViaM0M4','SRF_ViaM3M4','BND_Met4Layer')
		# tmp2 = self.get_param_KJH4('SRF_BootSW_Neg','SRF_C13_00','SRF_C07','SRF_Tr12Tr3Tr10','SRF_Tr12Tr3Tr10_Gate_ViaM0M4','SRF_ViaM3M4','BND_Met4Layer')
		tmp1 = self.get_param_KJH4('BND_BootSWCLKB_Vtc_M2')
		tmp2 = self.get_param_KJH4('SRF_SampCLKBInverter', 'BND_Out_Vtc_M2')
		self._DesignParameter['BND_BootSWCLKBInvIn_Hrz_M3']['_XWidth'] = abs(tmp1[0][0]['_XY_cent'][0] - tmp2[0][0][0]['_XY_cent'][0])

		## Define Boundary_element _XWidth
		self._DesignParameter['BND_BootSWCLKBInvIn_Hrz_M3']['_YWidth'] = 50

		## Define Boundary_element _XYCoordinates
		self._DesignParameter['BND_BootSWCLKBInvIn_Hrz_M3']['_XYCoordinates'] = [[0, 0]]

		## Calculate Sref XYcoord
		tmpXY = []
		## Calculate
		## Target_coord: _XY_type1
		target_coord = tmp1[0][0]['_XY_cent']
		## Approaching_coord: _XY_type2
		tmp2 = self.get_param_KJH4('BND_BootSWCLKBInvIn_Hrz_M3')
		approaching_coord = tmp2[0][0]['_XY_left']
		## Sref coord
		tmp3 = self.get_param_KJH4('BND_BootSWCLKBInvIn_Hrz_M3')
		Scoord = tmp3[0][0]['_XY_origin']
		## Cal
		New_Scoord = self.get_Scoord_KJH4(target_coord, approaching_coord, Scoord)
		tmpXY.append(New_Scoord)
		## Define coordinates
		self._DesignParameter['BND_BootSWCLKBInvIn_Hrz_M3']['_XYCoordinates'] = tmpXY
		###################################################################################################

		## SRF_BootSWCLKBInvIn_ViaM2M3
		## Sref generation: ViaX
		## Define ViaX Parameter
		_Caculation_Parameters = copy.deepcopy(A02_ViaStack_KJH3._ViaStack._ParametersForDesignCalculation)
		_Caculation_Parameters['_Layer1'] = 2
		_Caculation_Parameters['_Layer2'] = 3
		_Caculation_Parameters['_COX'] = 1
		_Caculation_Parameters['_COY'] = 2

		## Sref ViaX declaration
		self._DesignParameter['SRF_BootSWCLKBInvIn_ViaM2M3'] = self._SrefElementDeclaration(
			_DesignObj=A02_ViaStack_KJH3._ViaStack(_DesignParameter=None, _Name='{}:SRF_BootSWCLKBInvIn_ViaM2M3'.format(_Name)))[0]

		## Define Sref Relection
		self._DesignParameter['SRF_BootSWCLKBInvIn_ViaM2M3']['_Reflect'] = [0, 0, 0]

		## Define Sref Angle
		self._DesignParameter['SRF_BootSWCLKBInvIn_ViaM2M3']['_Angle'] = 0

		## Generate Metal(x), Metal(x+1) and C0(Viax) layer:  Option: _CalculateDesignParameter, _CalculateDesignParameterXmin, _CalculateDesignParameterYmin, _CalculateDesignParameterXYsame
		self._DesignParameter['SRF_BootSWCLKBInvIn_ViaM2M3']['_DesignObj']._CalculateDesignParameterXmin(**_Caculation_Parameters)

		## Calculate Sref XYcoord
		tmpXY = []
		## initialized Sref coordinate
		self._DesignParameter['SRF_BootSWCLKBInvIn_ViaM2M3']['_XYCoordinates'] = [[0, 0]]
		## Calculate
		## Target_coord
		tmp1 = self.get_param_KJH4('BND_BootSWCLKBInvIn_Hrz_M3')
		target_coord = tmp1[0][0]['_XY_left']
		## Approaching_coord
		tmp2 = self.get_param_KJH4('SRF_BootSWCLKBInvIn_ViaM2M3', 'SRF_ViaM2M3', 'BND_Met2Layer')
		approaching_coord = tmp2[0][0][0][0]['_XY_cent']
		## Sref coord
		tmp3 = self.get_param_KJH4('SRF_BootSWCLKBInvIn_ViaM2M3')
		Scoord = tmp3[0][0]['_XY_origin']
		## Calculate
		New_Scoord = self.get_Scoord_KJH4(target_coord, approaching_coord, Scoord)
		tmpXY.append(New_Scoord)
		## Calc 2
		approaching_coord = tmp2[0][0][0][0]['_XY_cent']
		target_coord = tmp1[0][0]['_XY_right']
		New_Scoord = self.get_Scoord_KJH4(target_coord, approaching_coord, Scoord)
		tmpXY.append(New_Scoord)
		## Define
		self._DesignParameter['SRF_BootSWCLKBInvIn_ViaM2M3']['_XYCoordinates'] = tmpXY
		###################################################################################################

		### BND_BootSWCLKBInvIn_Hrz_M3; Connecting Output of SRF_SampCLKBInverter and 'BND_BootSWCLKSignalPath_Hrz_M5'
		## Boundary_element Generation
		## Generate Boundary_element: ex)LayerName: METAL1 / DIFF (_ODLayer) / POLY / PIMP (_PPLayer) / NWELL / SLVT LVT RVT HVT / OP(OPpress) / CONT (CA) / PCCRIT
		self._DesignParameter['BND_CLKBInvIn_Hrz_M3'] = self._BoundaryElementDeclaration(
			_Layer=DesignParameters._LayerMapping['METAL3'][0],
			_Datatype=DesignParameters._LayerMapping['METAL3'][1],
			_XWidth=None,
			_YWidth=None,
			_XYCoordinates=[],
		)
		## Define Boundary_element _XWidth
		tmp1 = self.get_param_KJH4('BND_Tr6Tr11GateRouteExten_Vtc_M4')
		tmp2 = self.get_param_KJH4('SRF_SampCLKBInverter', 'BND_Input_Vtc_M1')
		self._DesignParameter['BND_CLKBInvIn_Hrz_M3']['_XWidth'] = abs(tmp1[0][0]['_XY_cent'][0] - tmp2[0][0][0]['_XY_cent'][0])

		## Define Boundary_element _XWidth
		self._DesignParameter['BND_CLKBInvIn_Hrz_M3']['_YWidth'] = 50

		## Define Boundary_element _XYCoordinates
		self._DesignParameter['BND_CLKBInvIn_Hrz_M3']['_XYCoordinates'] = [[0, 0]]

		## Calculate Sref XYcoord
		tmpXY = []
		## Calculate
		## Target_coord: _XY_type1
		target_coord = tmp2[0][0][0]['_XY_cent']
		## Approaching_coord: _XY_type2
		tmp2 = self.get_param_KJH4('BND_CLKBInvIn_Hrz_M3')
		approaching_coord = tmp2[0][0]['_XY_left']
		## Sref coord
		tmp3 = self.get_param_KJH4('BND_CLKBInvIn_Hrz_M3')
		Scoord = tmp3[0][0]['_XY_origin']
		## Cal
		New_Scoord = self.get_Scoord_KJH4(target_coord, approaching_coord, Scoord)
		tmpXY.append(New_Scoord)
		## Define coordinates
		self._DesignParameter['BND_CLKBInvIn_Hrz_M3']['_XYCoordinates'] = tmpXY
		###################################################################################################

		## SRF_CLKBInvIn_ViaM3M4
		## Sref generation: ViaX
		## Define ViaX Parameter
		_Caculation_Parameters = copy.deepcopy(A02_ViaStack_KJH3._ViaStack._ParametersForDesignCalculation)
		_Caculation_Parameters['_Layer1'] = 3
		_Caculation_Parameters['_Layer2'] = 4
		_Caculation_Parameters['_COX'] = 1
		_Caculation_Parameters['_COY'] = 3

		## Sref ViaX declaration
		self._DesignParameter['SRF_CLKBInvIn_ViaM3M4'] = self._SrefElementDeclaration(_DesignObj=A02_ViaStack_KJH3._ViaStack(_DesignParameter=None, _Name='{}:SRF_CLKBInvIn_ViaM3M4'.format(_Name)))[0]

		## Define Sref Relection
		self._DesignParameter['SRF_CLKBInvIn_ViaM3M4']['_Reflect'] = [0, 0, 0]

		## Define Sref Angle
		self._DesignParameter['SRF_CLKBInvIn_ViaM3M4']['_Angle'] = 0

		## Generate Metal(x), Metal(x+1) and C0(Viax) layer:  Option: _CalculateDesignParameter, _CalculateDesignParameterXmin, _CalculateDesignParameterYmin, _CalculateDesignParameterXYsame
		self._DesignParameter['SRF_CLKBInvIn_ViaM3M4']['_DesignObj']._CalculateDesignParameterXmin(**_Caculation_Parameters)

		## Calculate Sref XYcoord
		tmpXY = []
		## initialized Sref coordinate
		self._DesignParameter['SRF_CLKBInvIn_ViaM3M4']['_XYCoordinates'] = [[0, 0]]
		## Calculate
		## Target_coord
		tmp1 = self.get_param_KJH4('BND_CLKBInvIn_Hrz_M3')
		target_coord = tmp1[0][0]['_XY_right']
		## Approaching_coord
		tmp2 = self.get_param_KJH4('SRF_CLKBInvIn_ViaM3M4', 'SRF_ViaM3M4', 'BND_Met3Layer')
		approaching_coord = tmp2[0][0][0][0]['_XY_cent']
		## Sref coord
		tmp3 = self.get_param_KJH4('SRF_CLKBInvIn_ViaM3M4')
		Scoord = tmp3[0][0]['_XY_origin']
		## Calculate
		New_Scoord = self.get_Scoord_KJH4(target_coord, approaching_coord, Scoord)
		tmpXY.append(New_Scoord)

		## Define
		self._DesignParameter['SRF_CLKBInvIn_ViaM3M4']['_XYCoordinates'] = tmpXY
		###################################################################################################

		## SRF_CLKBInvIn_ViaM1M3
		## Sref generation: ViaX
		## Define ViaX Parameter
		_Caculation_Parameters = copy.deepcopy(A02_ViaStack_KJH3._ViaStack._ParametersForDesignCalculation)
		_Caculation_Parameters['_Layer1'] = 1
		_Caculation_Parameters['_Layer2'] = 3
		_Caculation_Parameters['_COX'] = 1
		_Caculation_Parameters['_COY'] = 2

		## Sref ViaX declaration
		self._DesignParameter['SRF_CLKBInvIn_ViaM1M3'] = self._SrefElementDeclaration(_DesignObj=A02_ViaStack_KJH3._ViaStack(_DesignParameter=None, _Name='{}:SRF_CLKBInvIn_ViaM1M3'.format(_Name)))[0]

		## Define Sref Relection
		self._DesignParameter['SRF_CLKBInvIn_ViaM1M3']['_Reflect'] = [0, 0, 0]

		## Define Sref Angle
		self._DesignParameter['SRF_CLKBInvIn_ViaM1M3']['_Angle'] = 0

		## Generate Metal(x), Metal(x+1) and C0(Viax) layer:  Option: _CalculateDesignParameter, _CalculateDesignParameterXmin, _CalculateDesignParameterYmin, _CalculateDesignParameterXYsame
		self._DesignParameter['SRF_CLKBInvIn_ViaM1M3']['_DesignObj']._CalculateDesignParameterXmin(**_Caculation_Parameters)

		## Calculate Sref XYcoord
		tmpXY = []
		## initialized Sref coordinate
		self._DesignParameter['SRF_CLKBInvIn_ViaM1M3']['_XYCoordinates'] = [[0, 0]]
		## Calculate
		## Target_coord
		tmp1 = self.get_param_KJH4('BND_CLKBInvIn_Hrz_M3')
		target_coord = tmp1[0][0]['_XY_left']
		## Approaching_coord
		tmp2 = self.get_param_KJH4('SRF_CLKBInvIn_ViaM1M3', 'SRF_ViaM1M2', 'BND_Met1Layer')
		approaching_coord = tmp2[0][0][0][0]['_XY_cent']
		## Sref coord
		tmp3 = self.get_param_KJH4('SRF_CLKBInvIn_ViaM1M3')
		Scoord = tmp3[0][0]['_XY_origin']
		## Calculate
		New_Scoord = self.get_Scoord_KJH4(target_coord, approaching_coord, Scoord)
		tmpXY.append(New_Scoord)

		## Define
		self._DesignParameter['SRF_CLKBInvIn_ViaM1M3']['_XYCoordinates'] = tmpXY
		###################################################################################################

		if _NumofRbit !=0:
			## ########## ########## ########## ########## ########## ########## ########## ########## ########## ########## ########## ########## SRF_RDACandDecoder_Pos
			## ########## ########## ########## ########## ########## ########## ########## ########## ########## ########## ########## SRF_RDACandDecoder_Pos: Gen and placement
			## Copy Calculation_Parameters from low-level-block ex)copy.deepcopy(B16_nmos_power_v2._NMOS_POWER._ParametersForDesignCalculation)
			_Caculation_Parameters = copy.deepcopy(R00_00_Combine_KJH4._Combine._ParametersForDesignCalculation)
			## Define Calculation_Parameters ex) _Caculation_Parameters['_NMOSPOWER_PbodyContact_1_Length']  = _NMOSPOWER_PbodyContact_1_Length

			# RDAC and Decoder
				# Pside or Nside
			_Caculation_Parameters['_RDAC_Pside'] = True
				# RDAC and Decoder delta X displacement for DRC
			_Caculation_Parameters['_RDAC_displacement'] = _RDAC_displacement
				# RDAC and Decoder Size : Consider "_Decoder_RBit" and "_Unit_Num_EachStag_input" ex) [2, 8] --> 4 : 2*8 = 2**4
			_Caculation_Parameters['_RDAC_Size'] = _RDAC_Size

				# ResArray
					# Unit Resistor
			_Caculation_Parameters['_RDAC_Array_ResWidth'] = _RDAC_Array_ResWidth
			_Caculation_Parameters['_RDAC_Array_ResLength'] = _RDAC_Array_ResLength

				## Decoder
					## Array
						# _Unit to Unit distance for DRC of routing
			_Caculation_Parameters['_RDAC_Decoder_Unit2UnitDist'] = _RDAC_Decoder_Unit2UnitDist
					# Unit
						## Comoon
							# Routing
			_Caculation_Parameters['_RDAC_Decoder_Unit_Routing_Dist'] = _RDAC_Decoder_Unit_Routing_Dist
							# Xvt
			_Caculation_Parameters['_RDAC_Decoder_Unit_Xvt'] = _RDAC_Decoder_Unit_Xvt
							# Dist
			_Caculation_Parameters['_RDAC_Decoder_Unit_GatetoGateDist'] = _RDAC_Decoder_Unit_GatetoGateDist
							# Inputs of Nand,Nor
			_Caculation_Parameters['_RDAC_Decoder_Unit_Num_EachStag_input'] = _RDAC_Decoder_Unit_Num_EachStag_input
							# Power rail
								# Pbody_Pulldown(NMOS)
			_Caculation_Parameters['_RDAC_Decoder_Unit_Pbody_XvtTop2Pbody'] = _RDAC_Decoder_Unit_Pbody_XvtTop2Pbody
								# Nbody_Pullup(PMOS)
			_Caculation_Parameters['_RDAC_Decoder_Unit_Nbody_Xvtdown2Nbody'] = _RDAC_Decoder_Unit_Nbody_Xvtdown2Nbody
								# PMOS and NMOS Height
			_Caculation_Parameters['_RDAC_Decoder_Unit_PMOSXvt2NMOSXvt'] = _RDAC_Decoder_Unit_PMOSXvt2NMOSXvt
						# Nand( _Decoder_Unit_Num_EachStag_input에서 1,3,5,7...번째 해당하는 nand 생성)
							# MOSFET
								# Common
			_Caculation_Parameters['_RDAC_Decoder_Nand_NumberofGate'] = _RDAC_Decoder_Nand_NumberofGate
			_Caculation_Parameters['_RDAC_Decoder_Nand_ChannelLength'] = _RDAC_Decoder_Nand_ChannelLength
								# Pulldown(NMOS)
			_Caculation_Parameters['_RDAC_Decoder_Nand_NMOS_ChannelWidth'] = _RDAC_Decoder_Nand_NMOS_ChannelWidth
								# Pulldown(PMOS)
			_Caculation_Parameters['_RDAC_Decoder_Nand_PMOS_ChannelWidth'] = _RDAC_Decoder_Nand_PMOS_ChannelWidth
						# Nor( _Decoder_Unit_Num_EachStag_input에서 2,4,6,7...번째 해당하는 nor 생성)
							# MOSFET
								# Common
			_Caculation_Parameters['_RDAC_Decoder_Nor_NumberofGate'] = _RDAC_Decoder_Nor_NumberofGate
			_Caculation_Parameters['_RDAC_Decoder_Nor_ChannelLength'] = _RDAC_Decoder_Nor_ChannelLength
								# Pulldown(NMOS)
			_Caculation_Parameters['_RDAC_Decoder_Nor_NMOS_ChannelWidth'] = _RDAC_Decoder_Nor_NMOS_ChannelWidth
								# Pulldown(PMOS)
			_Caculation_Parameters['_RDAC_Decoder_Nor_PMOS_ChannelWidth'] = _RDAC_Decoder_Nor_PMOS_ChannelWidth
						# Inv
							# Common
			_Caculation_Parameters['_RDAC_Decoder_Inv_NumberofGate'] = _RDAC_Decoder_Inv_NumberofGate
			_Caculation_Parameters['_RDAC_Decoder_Inv_ChannelLength'] = _RDAC_Decoder_Inv_ChannelLength
							# NMosfet
			_Caculation_Parameters['_RDAC_Decoder_Inv_NMOS_ChannelWidth'] = _RDAC_Decoder_Inv_NMOS_ChannelWidth
							# PMosfet
			_Caculation_Parameters['_RDAC_Decoder_Inv_PMOS_ChannelWidth'] = _RDAC_Decoder_Inv_PMOS_ChannelWidth
						# Xgate
							# Common
			_Caculation_Parameters['_RDAC_Decoder_Xgate_NumberofGate'] = _RDAC_Decoder_Xgate_NumberofGate
			_Caculation_Parameters['_RDAC_Decoder_Xgate_ChannelLength'] = _RDAC_Decoder_Xgate_ChannelLength
							# NMosfet
			_Caculation_Parameters['_RDAC_Decoder_Xgate_NMOS_ChannelWidth'] = _RDAC_Decoder_Xgate_NMOS_ChannelWidth
							# PMosfet
			_Caculation_Parameters['_RDAC_Decoder_Xgate_PMOS_ChannelWidth'] = _RDAC_Decoder_Xgate_PMOS_ChannelWidth


			## Generate Sref: ex)self._DesignParameter['_NMOS_POWER'] = self._SrefElementDeclaration(_DesignObj=B16_nmos_power_v2._NMOS_POWER( _DesignParameter=None, _Name='{}:NMOS_POWER'.format(_Name)))[0]
			self._DesignParameter['SRF_RDACandDecoder_Pos'] = self._SrefElementDeclaration(_DesignObj=R00_00_Combine_KJH4._Combine(_DesignParameter=None, _Name='{}:SRF_RDACandDecoder_Pos'.format(_Name)))[0]

			## Define Sref Reflection: ex)self._DesignParameter['_NMOS_POWER']['_Reflect'] = [0, 0, 0]
			self._DesignParameter['SRF_RDACandDecoder_Pos']['_Reflect'] = [0, 0, 0]

			## Define Sref Angle: ex)'_NMOS_POWER'
			self._DesignParameter['SRF_RDACandDecoder_Pos']['_Angle'] = 0

			## Calculate Sref Layer by using Calculation_Parameter: ex)'_NMOS_POWER'
			self._DesignParameter['SRF_RDACandDecoder_Pos']['_DesignObj']._CalculateDesignParameter(**_Caculation_Parameters)

			## Define Sref _XYcoordinate: ex)'_NMOS_POWER'
			self._DesignParameter['SRF_RDACandDecoder_Pos']['_XYCoordinates'] = [[0, 0]]


			## Get_Scoord_v4.
			## Calculate Sref XYcoord
			tmpXY = []
			## initialized Sref coordinate
			self._DesignParameter['SRF_RDACandDecoder_Pos']['_XYCoordinates'] = [[0, 0]]

			## Calculate
			## Target_coord: _XY_type1  'BND_CDAC_Pos_MSB{}DrvIn_Hrz_M3'.format(j) CapSize = 2 ** (_NumOfBits - i - 1)
			if (_CDAC_FoldingTF == False):
				tmp1_1 = self.get_param_KJH4('SRF_CDAC_Pos', 'SRF_CDACWtDriver','SRF_CDACWtDriver', 'SRF_CapArray', 'SRF_DummyCaps', 'SRF_CapWtShield4DCAP', 'BND_Shield_Extend_VTC_M{}'.format(_CDAC_ShieldingLayer))
			else:
				tmp1_1 = self.get_param_KJH4('SRF_CDAC_Pos', 'SRF_CDACWtDriver','SRF_CDAC_LowerHalf', 'SRF_CapArray', 'SRF_DummyCaps', 'SRF_CapWtShield4DCAP', 'BND_Shield_Extend_VTC_M{}'.format(_CDAC_ShieldingLayer))

			target_coordx = tmp1_1[0][0][0][0][-1][0][0][0]['_XY_right'][0]


			if (_CDAC_FoldingTF == False):
				CapSize = 2 ** (_NumofCbit - 0 - 1)
				tmp1_2 = self.get_param_KJH4('SRF_CDAC_Pos', 'SRF_CDACWtDriver','SRF_CDACWtDriver', 'SRF_DriverArray', 'BND_{}C_Driver_Input_Hrz_M3'.format(CapSize))
			else:
				CapSize = 2 ** (_NumofCbit - 1 - 1)
				tmp1_2 = self.get_param_KJH4('SRF_CDAC_Pos', 'SRF_CDACWtDriver','SRF_CDAC_LowerHalf', 'SRF_DriverArray', 'BND_{}C_Driver_Input_Hrz_M3'.format(CapSize))

			target_coordy = tmp1_2[0][0][0][0][0][0]['_XY_up'][1]
			target_coord = [target_coordx,target_coordy]
			## Approaching_coord: _XY_type2
			tmp2_1 = self.get_param_KJH4('SRF_RDACandDecoder_Pos','BND_XgateOut_Hrz_M5')
			approaching_coordx = tmp2_1[0][0][0]['_XY_left'][0]
			tmp2_2 = self.get_param_KJH4('SRF_RDACandDecoder_Pos','BND_B_{}'.format(_NumofRbit-1))
			approaching_coordy = tmp2_2[0][0][0]['_XY_down'][1]
			approaching_coord = [approaching_coordx,approaching_coordy]
			## Sref coord
			tmp3 = self.get_param_KJH4('SRF_RDACandDecoder_Pos')
			Scoord = tmp3[0][0]['_XY_origin']
			## Cal
			New_Scoord = self.get_Scoord_KJH4(target_coord, approaching_coord, Scoord)
			New_Scoord[0] = New_Scoord[0] + 3000
			New_Scoord[1] = New_Scoord[1] + 500
			tmpXY.append(New_Scoord)
			## Define Coordinates
			self._DesignParameter['SRF_RDACandDecoder_Pos']['_XYCoordinates'] = tmpXY
			###################################################################################################

			##  SRF_RDACandDecoder_Pos: Vref2CDAC routing
			###### Path_element Generation 2
			## Path Name:
			Path_name = 'RdacVref2Cdac'

			## Path Width: ***** must be even number ***
			Path_width = 50

			## tmp
			tmpXY = []
			tmpMetal = []
			tmpViaTF = []
			tmpViaDir = []
			tmpViaWid = []

			if _CDAC_FoldingTF == False:
				## coord1
				## P1 calculation
				P1 = [0, 0]
				tmp = self.get_param_KJH4('SRF_RDACandDecoder_Pos','BND_XgateOut_Hrz_M5')
				P1 = tmp[0][0][0]['_XY_left']
				## P2 calculation
				P2 = [0, 0]
				tmp = self.get_param_KJH4('SRF_CDAC_Pos', 'SRF_CDACWtDriver','SRF_CDACWtDriver', 'SRF_CapArray', 'BND_DummyUCAP_Bot_Hrz')

				P2[0] = tmp[0][0][0][0][0][0]['_XY_up_right'][0]
				P2[1] = np.array(P1[1])
				## Metal Layer
				Metal = 5
				## Via: True=1/False=0
				ViaTF = 1
				## Via: Vtc=1/Hrz=0/Ovl=2
				ViaDir = 1
				## Via width: None/[1,3]
				ViaWid = [1,2]

				tmpXY.append([P1, P2])
				tmpMetal.append(Metal)
				tmpViaTF.append(ViaTF)
				tmpViaDir.append(ViaDir)
				tmpViaWid.append(ViaWid)

				## coord2
				## P1 calculation
				P1 = [0, 0]
				P1 = np.array(P2)
				## P2 calculation
				P2 = [0, 0]
				P2[0] = np.array(P1[0])
				tmp = self.get_param_KJH4('SRF_CDAC_Pos', 'SRF_CDACWtDriver','SRF_CDACWtDriver', 'SRF_CapArray', 'BND_DummyUCAP_Bot_Hrz')

				P2[1] = tmp[0][0][0][0][0][0]['_XY_up_right'][1]
				## Metal Layer
				Metal = 3
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
			# Cap Folding
			else:
				## coord1
				## P1 calculation
				tmp = self.get_param_KJH4('SRF_RDACandDecoder_Pos', 'BND_XgateOut_Hrz_M5')
				P1 = tmp[0][0][0]['_XY_left']
				## P2 calculation
				P2 = [P1[0]-200,P1[1]]
				## Metal Layer
				Metal = 5
				## Via: True=1/False=0
				ViaTF = 1
				## Via: Vtc=1/Hrz=0/Ovl=2
				ViaDir = 1
				## Via width: None/[1,3]
				ViaWid = [1,2]

				tmpXY.append([P1, P2])
				tmpMetal.append(Metal)
				tmpViaTF.append(ViaTF)
				tmpViaDir.append(ViaDir)
				tmpViaWid.append(ViaWid)

				## coord2
				## P1 calculation
				P1 = copy.deepcopy(P2)  # = [0, -1000]
				## P2 calculation
				if _CDACDrv_ArrangedTF == False:
					tmp = self.get_param_KJH4('SRF_CDAC_Pos', 'SRF_CDACWtDriver','SRF_CDAC_UpperHalf', 'SRF_CapArray', 'BND_DummyUCAP_Bot_Hrz')
					P2 = [P1[0], tmp[0][0][0][0][0][0]['_XY_cent'][1]]
				else:
					tmp = self.get_param_KJH4('SRF_CDAC_Pos', 'SRF_CDACWtDriver', 'SRF_CDAC_UpperHalf', 'BND_DummyUCAP_Bot_Hrz')
					P2 = [P1[0],tmp[0][0][0][0][0]['_XY_cent'][1]]
				## Metal Layer
				Metal = 4
				## Via True=1/False=0
				ViaTF = 1
				## Via Vtc=1/Hrz=0/Ovl=2
				ViaDir = 0
				## Via width: None/[1,3]
				ViaWid = [2,1]

				tmpXY.append([P1, P2])
				tmpMetal.append(Metal)
				tmpViaTF.append(ViaTF)
				tmpViaDir.append(ViaDir)
				tmpViaWid.append(ViaWid)

				## coord3
				## P1 calculation
				P1 = copy.deepcopy(P2)  # = [0, -1000]
				## P2 calculation
				if _CDACDrv_ArrangedTF == False:
					tmp = self.get_param_KJH4('SRF_CDAC_Pos', 'SRF_CDACWtDriver','SRF_CDAC_UpperHalf', 'SRF_CapArray', 'BND_DummyUCAP_Bot_Hrz')
					P2 = tmp[0][0][0][0][0][0]['_XY_cent']
				else:
					tmp = self.get_param_KJH4('SRF_CDAC_Pos', 'SRF_CDACWtDriver', 'SRF_CDAC_UpperHalf', 'BND_DummyUCAP_Bot_Hrz')
					P2 = tmp[0][0][0][0][0]['_XY_cent']

				## Metal Layer
				Metal = 3
				## Via True=1/False=0
				ViaTF = 0
				## Via Vtc=1/Hrz=0/Ovl=2
				ViaDir = 0
				## Via width: None/[1,3]
				ViaWid = None

				tmpXY.append([P1, P2])
				tmpMetal.append(Metal)
				tmpViaTF.append(ViaTF)
				tmpViaDir.append(ViaDir)
				tmpViaWid.append(ViaWid)

			tmpXY = self.get_PTH_KJH2(Path_name, Path_width, tmpXY, tmpMetal, tmpViaTF, tmpViaDir, tmpViaWid,_Name)
			###################################################################################################

			## ########## ########## ########## ########## ########## ########## ########## ########## ########## ########## ########## SRF_RDACandDecoder_Pos: Decder Bin. Connect
			## ########## ########## ########## ########## ########## ########## ########## ########## ########## ########## SRF_RDACandDecoder_Pos: Decder Bin. Connect: Hrz M3
			## ########## ########## ########## ########## ########## ########## ########## ########## ########## SRF_RDACandDecoder_Pos: Decder Bin. Connect: Hrz M3: B
			for i in range(0,_NumofRbit):
				## Boundary_element Generation 'BND_B_{}'.format(i)
				Element_name = 'BND_B_{}_Exten'.format(i)
				## Generate Boundary_element: ex)LayerName: METAL1 / DIFF (_ODLayer) / POLY / PIMP (_PPLayer) / NWELL / SLVT LVT RVT HVT / OP(OPpress) / CONT (CA) / PCCRIT
				self._DesignParameter[Element_name] = self._BoundaryElementDeclaration(
					_Layer=DesignParameters._LayerMapping['METAL3'][0],
					_Datatype=DesignParameters._LayerMapping['METAL3'][1],
					_XWidth=None,
					_YWidth=None,
					_XYCoordinates=[],
				)

				## Define Boundary_element _YWidth
				tmp =self.get_param_KJH4('SRF_RDACandDecoder_Pos','BND_B_{}'.format(i))
				self._DesignParameter[Element_name]['_YWidth'] = tmp[0][0][0]['_Ywidth']

				## Define Boundary_element _XWidth
				Num_Invchain = len(_LOGIC_DACPreDrv_NumberofGate2)-1-i
				Num_InvinChain = len(_LOGIC_DACPreDrv_NumberofGate2[-1-i])-2

				tmp1 = self.get_param_KJH4('SRF_RDACandDecoder_Pos', 'BND_B_{}'.format(i))
				tmp2 = self.get_param_KJH4('SRF_SARLogicWtComparator','SRF_SARLogicWtBuffers','SRF_UpperCDACPreDriver','SRF_InvChain{}'.format(Num_Invchain),'SRF_IntConn_ViaM1M2','SRF_ViaM1M2','BND_Met2Layer') #SRF_Output_ViaM2Mx
				self._DesignParameter[Element_name]['_XWidth'] = (tmp2[0][0][0][0][-1][0][0][0]['_XY_right'][0] - tmp1[0][0][0]['_XY_right'][0])

				## Define Boundary_element _XYCoordinates
				self._DesignParameter[Element_name]['_XYCoordinates'] = [[0, 0]]

				## Calculate Sref XYcoord
				tmpXY = []
				## initialized Sref coordinate
				self._DesignParameter[Element_name]['_XYCoordinates'] = [[0, 0]]
				## Calculate
				## Target_coord: _XY_type1
				tmp1 = self.get_param_KJH4('SRF_RDACandDecoder_Pos','BND_B_{}'.format(i))
				target_coord = tmp1[0][0][0]['_XY_down_right']
				## Approaching_coord: _XY_type2
				tmp2 = self.get_param_KJH4(Element_name)
				approaching_coord = tmp2[0][0]['_XY_down_left']
				## Sref coord
				tmp3 = self.get_param_KJH4(Element_name)
				Scoord = tmp3[0][0]['_XY_origin']
				## Cal
				New_Scoord = self.get_Scoord_KJH4(target_coord, approaching_coord, Scoord)
				tmpXY.append(New_Scoord)
				## Define coordinates
				self._DesignParameter[Element_name]['_XYCoordinates'] = tmpXY
			###################################################################################################

			## ########## ########## ########## ########## ########## ########## ########## ########## ########## SRF_RDACandDecoder_Pos: Decder Bin. Connect: Hrz M3: Bb
				## Boundary_element Generation 'BND_B_{}'.format(i)
				Element_name = 'BND_Bb_{}_Exten'.format(i)
				## Generate Boundary_element: ex)LayerName: METAL1 / DIFF (_ODLayer) / POLY / PIMP (_PPLayer) / NWELL / SLVT LVT RVT HVT / OP(OPpress) / CONT (CA) / PCCRIT
				self._DesignParameter[Element_name] = self._BoundaryElementDeclaration(
					_Layer=DesignParameters._LayerMapping['METAL3'][0],
					_Datatype=DesignParameters._LayerMapping['METAL3'][1],
					_XWidth=None,
					_YWidth=None,
					_XYCoordinates=[],
				)

				## Define Boundary_element _YWidth
				tmp =self.get_param_KJH4('SRF_RDACandDecoder_Pos','BND_Bb_{}'.format(i))
				self._DesignParameter[Element_name]['_YWidth'] = tmp[0][0][0]['_Ywidth']

				## Define Boundary_element _XWidth
				Num_Invchain = len(_LOGIC_DACPreDrv_NumberofGate2)-1-i
				Num_InvinChain = len(_LOGIC_DACPreDrv_NumberofGate2[-1-i])-2

				tmp1 = self.get_param_KJH4('SRF_RDACandDecoder_Pos', 'BND_Bb_{}'.format(i))
				tmp2 = self.get_param_KJH4('SRF_SARLogicWtComparator','SRF_SARLogicWtBuffers','SRF_UpperCDACPreDriver','SRF_InvChain{}'.format(Num_Invchain),'SRF_Output_ViaM2Mx','SRF_ViaM2M3','BND_Met2Layer') #SRF_Output_ViaM2Mx
				self._DesignParameter[Element_name]['_XWidth'] = (tmp2[0][0][0][0][0][0][0][0]['_XY_right'][0] - tmp1[0][0][0]['_XY_right'][0])

				## Define Boundary_element _XYCoordinates
				self._DesignParameter[Element_name]['_XYCoordinates'] = [[0, 0]]

				## Calculate Sref XYcoord
				tmpXY = []
				## initialized Sref coordinate
				self._DesignParameter[Element_name]['_XYCoordinates'] = [[0, 0]]
				## Calculate
				## Target_coord: _XY_type1
				tmp1 = self.get_param_KJH4('SRF_RDACandDecoder_Pos','BND_Bb_{}'.format(i))
				target_coord = tmp1[0][0][0]['_XY_down_right']
				## Approaching_coord: _XY_type2
				tmp2 = self.get_param_KJH4(Element_name)
				approaching_coord = tmp2[0][0]['_XY_down_left']
				## Sref coord
				tmp3 = self.get_param_KJH4(Element_name)
				Scoord = tmp3[0][0]['_XY_origin']
				## Cal
				New_Scoord = self.get_Scoord_KJH4(target_coord, approaching_coord, Scoord)
				tmpXY.append(New_Scoord)
				## Define coordinates
				self._DesignParameter[Element_name]['_XYCoordinates'] = tmpXY
			###################################################################################################

			## ########## ########## ########## ########## ########## ########## ########## ########## ########## ########## SRF_RDACandDecoder_Pos: Decder Bin. Connect: ViaM3M4 of HrzM3
			## ########## ########## ########## ########## ########## ########## ########## ########## ########## SRF_RDACandDecoder_Pos: Decder Bin. Connect: ViaM3M4 of HrzM3: B

			for i in range(0,_NumofRbit):
				## Sref generation: ViaX
				ViaName = 'SRF_B_{}_Exten_ViaM3M4'.format(i)
				## Define ViaX Parameter
				_Caculation_Parameters = copy.deepcopy(A02_ViaStack_KJH3._ViaStack._ParametersForDesignCalculation)
				_Caculation_Parameters['_Layer1'] = 3
				_Caculation_Parameters['_Layer2'] = 4
				_Caculation_Parameters['_COX'] = 4
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
				tmp1 = self.get_param_KJH4('BND_B_{}_Exten'.format(i))
				target_coord = tmp1[0][0]['_XY_right']
				## Approaching_coord
				tmp2 = self.get_param_KJH4(ViaName,'SRF_ViaM3M4','BND_Met3Layer')
				approaching_coord = tmp2[0][0][0][0]['_XY_right']
				## Sref coord
				tmp3 = self.get_param_KJH4(ViaName)
				Scoord = tmp3[0][0]['_XY_origin']
				## Calculate
				New_Scoord = self.get_Scoord_KJH4(target_coord, approaching_coord, Scoord)
				tmpXY.append(New_Scoord)
				## Define
				self._DesignParameter[ViaName]['_XYCoordinates'] = tmpXY
			###################################################################################################

			## ########## ########## ########## ########## ########## ########## ########## ########## ########## SRF_RDACandDecoder_Pos: Decder Bin. Connect: ViaM3M4 of HrzM3: Bb
				## Sref generation: ViaX
				ViaName = 'SRF_Bb_{}_Exten_ViaM3M4'.format(i)
				## Define ViaX Parameter
				_Caculation_Parameters = copy.deepcopy(A02_ViaStack_KJH3._ViaStack._ParametersForDesignCalculation)
				_Caculation_Parameters['_Layer1'] = 3
				_Caculation_Parameters['_Layer2'] = 4
				_Caculation_Parameters['_COX'] = 4
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
				tmp1 = self.get_param_KJH4('BND_Bb_{}_Exten'.format(i))
				target_coord = tmp1[0][0]['_XY_right']
				## Approaching_coord
				tmp2 = self.get_param_KJH4(ViaName,'SRF_ViaM3M4','BND_Met3Layer')
				approaching_coord = tmp2[0][0][0][0]['_XY_right']
				## Sref coord
				tmp3 = self.get_param_KJH4(ViaName)
				Scoord = tmp3[0][0]['_XY_origin']
				## Calculate
				New_Scoord = self.get_Scoord_KJH4(target_coord, approaching_coord, Scoord)
				tmpXY.append(New_Scoord)
				## Define
				self._DesignParameter[ViaName]['_XYCoordinates'] = tmpXY
			###################################################################################################

			## ########## ########## ########## ########## ########## ########## ########## ########## ########## ########## SRF_RDACandDecoder_Pos: Decder Bin. Connect: VtcM4
			## ########## ########## ########## ########## ########## ########## ########## ########## ########## SRF_RDACandDecoder_Pos: Decder Bin. Connect: VtcM4: B
			for i in range(0,_NumofRbit):
				## Boundary_element Generation 'BND_B_{}'.format(i)
				Element_name = 'BND_B_{}_Exten_Vtc_M4'.format(i)
				## Generate Boundary_element: ex)LayerName: METAL1 / DIFF (_ODLayer) / POLY / PIMP (_PPLayer) / NWELL / SLVT LVT RVT HVT / OP(OPpress) / CONT (CA) / PCCRIT
				self._DesignParameter[Element_name] = self._BoundaryElementDeclaration(
					_Layer=DesignParameters._LayerMapping['METAL4'][0],
					_Datatype=DesignParameters._LayerMapping['METAL4'][1],
					_XWidth=None,
					_YWidth=None,
					_XYCoordinates=[],
				)

				## Define Boundary_element _YWidth 'BND_B_{}_Exten_ViaM3M4'.format(i)
				Num_Invchain = len(_LOGIC_DACPreDrv_NumberofGate2)-1-i
				Num_InvinChain = len(_LOGIC_DACPreDrv_NumberofGate2[-1-i])-2

				tmp1 =self.get_param_KJH4('SRF_B_{}_Exten_ViaM3M4'.format(i),'SRF_ViaM3M4','BND_Met4Layer')
				tmp2 = self.get_param_KJH4('SRF_SARLogicWtComparator','SRF_SARLogicWtBuffers','SRF_UpperCDACPreDriver','SRF_InvChain{}'.format(Num_Invchain),'SRF_IntConn_ViaM1M2','SRF_ViaM1M2','BND_Met2Layer') #SRF_Output_ViaM2Mx
				self._DesignParameter[Element_name]['_YWidth'] = abs(tmp2[0][0][0][0][-1][0][0][0]['_XY_up'][1] - tmp1[0][0][0][0]['_XY_up'][1])

				## Define Boundary_element _XWidth
				self._DesignParameter[Element_name]['_XWidth'] = 100

				## Define Boundary_element _XYCoordinates
				self._DesignParameter[Element_name]['_XYCoordinates'] = [[0, 0]]

				## Calculate Sref XYcoord
				tmpXY = []
				## initialized Sref coordinate
				self._DesignParameter[Element_name]['_XYCoordinates'] = [[0, 0]]
				## Calculate
				## Target_coord: _XY_type1
				tmp1 = self.get_param_KJH4('SRF_B_{}_Exten_ViaM3M4'.format(i),'SRF_ViaM3M4','BND_Met4Layer')
				target_coord = tmp1[0][0][0][0]['_XY_up_right']
				## Approaching_coord: _XY_type2
				tmp2 = self.get_param_KJH4(Element_name)
				approaching_coord = tmp2[0][0]['_XY_up_right']
				## Sref coord
				tmp3 = self.get_param_KJH4(Element_name)
				Scoord = tmp3[0][0]['_XY_origin']
				## Cal
				New_Scoord = self.get_Scoord_KJH4(target_coord, approaching_coord, Scoord)
				tmpXY.append(New_Scoord)
				## Define coordinates
				self._DesignParameter[Element_name]['_XYCoordinates'] = tmpXY
			###################################################################################################

				## ########## ########## ########## ########## ########## ########## ########## ########## ########## SRF_RDACandDecoder_Pos: Decder Bin. Connect: VtcM4: Bb
				## Boundary_element Generation 'BND_B_{}'.format(i)
				Element_name = 'BND_Bb_{}_Exten_Vtc_M4'.format(i)
				## Generate Boundary_element: ex)LayerName: METAL1 / DIFF (_ODLayer) / POLY / PIMP (_PPLayer) / NWELL / SLVT LVT RVT HVT / OP(OPpress) / CONT (CA) / PCCRIT
				self._DesignParameter[Element_name] = self._BoundaryElementDeclaration(
					_Layer=DesignParameters._LayerMapping['METAL4'][0],
					_Datatype=DesignParameters._LayerMapping['METAL4'][1],
					_XWidth=None,
					_YWidth=None,
					_XYCoordinates=[],
				)

				## Define Boundary_element _YWidth 'BND_B_{}_Exten_ViaM3M4'.format(i)
				Num_Invchain = len(_LOGIC_DACPreDrv_NumberofGate2) - 1 - i
				Num_InvinChain = len(_LOGIC_DACPreDrv_NumberofGate2[-1 - i]) - 2

				tmp1 = self.get_param_KJH4('SRF_Bb_{}_Exten_ViaM3M4'.format(i), 'SRF_ViaM3M4', 'BND_Met4Layer')
				tmp2 = self.get_param_KJH4('SRF_SARLogicWtComparator', 'SRF_SARLogicWtBuffers', 'SRF_UpperCDACPreDriver', 'SRF_InvChain{}'.format(Num_Invchain), 'SRF_Output_ViaM2Mx', 'SRF_ViaM2M3',
										   'BND_Met2Layer')  # SRF_Output_ViaM2Mx
				self._DesignParameter[Element_name]['_YWidth'] = abs(tmp2[0][0][0][0][0][0][0][0]['_XY_up'][1] - tmp1[0][0][0][0]['_XY_up'][1])

				## Define Boundary_element _XWidth
				self._DesignParameter[Element_name]['_XWidth'] = 100

				## Define Boundary_element _XYCoordinates
				self._DesignParameter[Element_name]['_XYCoordinates'] = [[0, 0]]

				## Calculate Sref XYcoord
				tmpXY = []
				## initialized Sref coordinate
				self._DesignParameter[Element_name]['_XYCoordinates'] = [[0, 0]]
				## Calculate
				## Target_coord: _XY_type1
				tmp1 = self.get_param_KJH4('SRF_Bb_{}_Exten_ViaM3M4'.format(i), 'SRF_ViaM3M4', 'BND_Met4Layer')
				target_coord = tmp1[0][0][0][0]['_XY_up_right']
				## Approaching_coord: _XY_type2
				tmp2 = self.get_param_KJH4(Element_name)
				approaching_coord = tmp2[0][0]['_XY_up_right']
				## Sref coord
				tmp3 = self.get_param_KJH4(Element_name)
				Scoord = tmp3[0][0]['_XY_origin']
				## Cal
				New_Scoord = self.get_Scoord_KJH4(target_coord, approaching_coord, Scoord)
				tmpXY.append(New_Scoord)
				## Define coordinates
				self._DesignParameter[Element_name]['_XYCoordinates'] = tmpXY
			###################################################################################################

			## ########## ########## ########## ########## ########## ########## ########## ########## ########## ########## SRF_RDACandDecoder_Pos: Decder Bin. Connect: ViaM2M4
			## Sref generation: ViaX
			ViaName = 'SRF_IntConn_Pos_ViaM2M4'
			## Define ViaX Parameter
			_Caculation_Parameters = copy.deepcopy(A02_ViaStack_KJH3._ViaStack._ParametersForDesignCalculation)
			_Caculation_Parameters['_Layer1'] = 2
			_Caculation_Parameters['_Layer2'] = 4
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
			for i in range(0,_NumofRbit):
				## Calculate
				## Target_coord
				Num_Invchain = len(_LOGIC_DACPreDrv_NumberofGate2)-1-i
				Num_InvinChain = len(_LOGIC_DACPreDrv_NumberofGate2[-1-i])-2
				tmp1 = self.get_param_KJH4('SRF_SARLogicWtComparator','SRF_SARLogicWtBuffers','SRF_UpperCDACPreDriver','SRF_InvChain{}'.format(Num_Invchain),'SRF_IntConn_ViaM1M2','SRF_ViaM1M2','BND_Met2Layer') #SRF_Output_ViaM2Mx
				target_coord = tmp1[0][0][0][0][-1][0][0][0]['_XY_up_left']
				## Approaching_coord
				tmp2 = self.get_param_KJH4(ViaName,'SRF_ViaM2M3','BND_Met2Layer')
				approaching_coord = tmp2[0][0][0][0]['_XY_down_left']
				## Sref coord
				tmp3 = self.get_param_KJH4(ViaName)
				Scoord = tmp3[0][0]['_XY_origin']
				## Calculate
				New_Scoord = self.get_Scoord_KJH4(target_coord, approaching_coord, Scoord)
				tmpXY.append(New_Scoord)
			## Define
			self._DesignParameter[ViaName]['_XYCoordinates'] = tmpXY
			###################################################################################################

			## ########## ########## ########## ########## ########## ########## ########## ########## ########## ########## ########## ########## SRF_RDACandDecoder_Neg
			## ########## ########## ########## ########## ########## ########## ########## ########## ########## ########## ########## SRF_RDACandDecoder_Pos: Gen and placement
			#시간줄이기... --> 똑같이 하면 안됨.
			## Copy Calculation_Parameters from low-level-block ex)copy.deepcopy(B16_nmos_power_v2._NMOS_POWER._ParametersForDesignCalculation)
			_Caculation_Parameters = copy.deepcopy(R00_00_Combine_KJH4._Combine._ParametersForDesignCalculation)
			## Define Calculation_Parameters ex) _Caculation_Parameters['_NMOSPOWER_PbodyContact_1_Length']  = _NMOSPOWER_PbodyContact_1_Length
			# RDAC and Decoder
				# Pside or Nside
			_Caculation_Parameters['_RDAC_Pside'] = False
				# RDAC and Decoder delta X displacement for DRC
			_Caculation_Parameters['_RDAC_displacement'] = _RDAC_displacement
				# RDAC and Decoder Size : Consider "_Decoder_RBit" and "_Unit_Num_EachStag_input" ex) [2, 8] --> 4 : 2*8 = 2**4
			_Caculation_Parameters['_RDAC_Size'] = _RDAC_Size

				# ResArray
					# Unit Resistor
			_Caculation_Parameters['_RDAC_Array_ResWidth'] = _RDAC_Array_ResWidth
			_Caculation_Parameters['_RDAC_Array_ResLength'] = _RDAC_Array_ResLength

				## Decoder
					## Array
						# _Unit to Unit distance for DRC of routing
			_Caculation_Parameters['_RDAC_Decoder_Unit2UnitDist'] = _RDAC_Decoder_Unit2UnitDist
					# Unit
						## Comoon
							# Routing
			_Caculation_Parameters['_RDAC_Decoder_Unit_Routing_Dist'] = _RDAC_Decoder_Unit_Routing_Dist
							# Xvt
			_Caculation_Parameters['_RDAC_Decoder_Unit_Xvt'] = _RDAC_Decoder_Unit_Xvt
							# Dist
			_Caculation_Parameters['_RDAC_Decoder_Unit_GatetoGateDist'] = _RDAC_Decoder_Unit_GatetoGateDist
							# Inputs of Nand,Nor
			_Caculation_Parameters['_RDAC_Decoder_Unit_Num_EachStag_input'] = _RDAC_Decoder_Unit_Num_EachStag_input
							# Power rail
								# Pbody_Pulldown(NMOS)
			_Caculation_Parameters['_RDAC_Decoder_Unit_Pbody_XvtTop2Pbody'] = _RDAC_Decoder_Unit_Pbody_XvtTop2Pbody
								# Nbody_Pullup(PMOS)
			_Caculation_Parameters['_RDAC_Decoder_Unit_Nbody_Xvtdown2Nbody'] = _RDAC_Decoder_Unit_Nbody_Xvtdown2Nbody
								# PMOS and NMOS Height
			_Caculation_Parameters['_RDAC_Decoder_Unit_PMOSXvt2NMOSXvt'] = _RDAC_Decoder_Unit_PMOSXvt2NMOSXvt
						# Nand( _Decoder_Unit_Num_EachStag_input에서 1,3,5,7...번째 해당하는 nand 생성)
							# MOSFET
								# Common
			_Caculation_Parameters['_RDAC_Decoder_Nand_NumberofGate'] = _RDAC_Decoder_Nand_NumberofGate
			_Caculation_Parameters['_RDAC_Decoder_Nand_ChannelLength'] = _RDAC_Decoder_Nand_ChannelLength
								# Pulldown(NMOS)
			_Caculation_Parameters['_RDAC_Decoder_Nand_NMOS_ChannelWidth'] = _RDAC_Decoder_Nand_NMOS_ChannelWidth
								# Pulldown(PMOS)
			_Caculation_Parameters['_RDAC_Decoder_Nand_PMOS_ChannelWidth'] = _RDAC_Decoder_Nand_PMOS_ChannelWidth
						# Nor( _Decoder_Unit_Num_EachStag_input에서 2,4,6,7...번째 해당하는 nor 생성)
							# MOSFET
								# Common
			_Caculation_Parameters['_RDAC_Decoder_Nor_NumberofGate'] = _RDAC_Decoder_Nor_NumberofGate
			_Caculation_Parameters['_RDAC_Decoder_Nor_ChannelLength'] = _RDAC_Decoder_Nor_ChannelLength
								# Pulldown(NMOS)
			_Caculation_Parameters['_RDAC_Decoder_Nor_NMOS_ChannelWidth'] = _RDAC_Decoder_Nor_NMOS_ChannelWidth
								# Pulldown(PMOS)
			_Caculation_Parameters['_RDAC_Decoder_Nor_PMOS_ChannelWidth'] = _RDAC_Decoder_Nor_PMOS_ChannelWidth
						# Inv
							# Common
			_Caculation_Parameters['_RDAC_Decoder_Inv_NumberofGate'] = _RDAC_Decoder_Inv_NumberofGate
			_Caculation_Parameters['_RDAC_Decoder_Inv_ChannelLength'] = _RDAC_Decoder_Inv_ChannelLength
							# NMosfet
			_Caculation_Parameters['_RDAC_Decoder_Inv_NMOS_ChannelWidth'] = _RDAC_Decoder_Inv_NMOS_ChannelWidth
							# PMosfet
			_Caculation_Parameters['_RDAC_Decoder_Inv_PMOS_ChannelWidth'] = _RDAC_Decoder_Inv_PMOS_ChannelWidth
						# Xgate
							# Common
			_Caculation_Parameters['_RDAC_Decoder_Xgate_NumberofGate'] = _RDAC_Decoder_Xgate_NumberofGate
			_Caculation_Parameters['_RDAC_Decoder_Xgate_ChannelLength'] = _RDAC_Decoder_Xgate_ChannelLength
							# NMosfet
			_Caculation_Parameters['_RDAC_Decoder_Xgate_NMOS_ChannelWidth'] = _RDAC_Decoder_Xgate_NMOS_ChannelWidth
							# PMosfet
			_Caculation_Parameters['_RDAC_Decoder_Xgate_PMOS_ChannelWidth'] = _RDAC_Decoder_Xgate_PMOS_ChannelWidth


			## Generate Sref: ex)self._DesignParameter['_NMOS_POWER'] = self._SrefElementDeclaration(_DesignObj=B16_nmos_power_v2._NMOS_POWER( _DesignParameter=None, _Name='{}:NMOS_POWER'.format(_Name)))[0]
			self._DesignParameter['SRF_RDACandDecoder_Neg'] = self._SrefElementDeclaration(_DesignObj=R00_00_Combine_KJH4._Combine(_DesignParameter=None, _Name='{}:SRF_RDACandDecoder_Neg'.format(_Name)))[0]

			## Calculate Sref Layer by using Calculation_Parameter: ex)'_NMOS_POWER'
			self._DesignParameter['SRF_RDACandDecoder_Neg']['_DesignObj']._CalculateDesignParameter(**_Caculation_Parameters) # 시간줄이기
			# self._DesignParameter['SRF_RDACandDecoder_Neg'] = copy.deepcopy(self._DesignParameter['SRF_RDACandDecoder_Pos'])
			# self.rename_srf_prefix(self._DesignParameter['SRF_RDACandDecoder_Neg'], 'SRF_RDACandDecoder_Pos', 'SRF_RDACandDecoder_Neg')


			## Define Sref Reflection: ex)self._DesignParameter['_NMOS_POWER']['_Reflect'] = [0, 0, 0]
			self._DesignParameter['SRF_RDACandDecoder_Neg']['_Reflect'] = [1, 0, 0]

			## Define Sref Angle: ex)'_NMOS_POWER'
			self._DesignParameter['SRF_RDACandDecoder_Neg']['_Angle'] = 0

			## Define Sref _XYcoordinate: ex)'_NMOS_POWER'
			self._DesignParameter['SRF_RDACandDecoder_Neg']['_XYCoordinates'] = [[0, 0]]


			## Get_Scoord_v4.
			## Calculate Sref XYcoord
			tmpXY = []
			## initialized Sref coordinate
			self._DesignParameter['SRF_RDACandDecoder_Neg']['_XYCoordinates'] = [[0, 0]]

			## Calculate
			## Target_coord: _XY_type1  'BND_CDAC_Neg_MSB{}DrvIn_Hrz_M3'.format(j) CapSize = 2 ** (_NumOfBits - i - 1)
			if (_CDAC_FoldingTF == False):
				tmp1_1 = self.get_param_KJH4('SRF_CDAC_Neg', 'SRF_CDACWtDriver','SRF_CDACWtDriver', 'SRF_CapArray', 'SRF_DummyCaps', 'SRF_CapWtShield4DCAP', 'BND_Shield_Extend_VTC_M{}'.format(_CDAC_ShieldingLayer))
			else:
				tmp1_1 = self.get_param_KJH4('SRF_CDAC_Neg', 'SRF_CDACWtDriver','SRF_CDAC_LowerHalf', 'SRF_CapArray', 'SRF_DummyCaps', 'SRF_CapWtShield4DCAP', 'BND_Shield_Extend_VTC_M{}'.format(_CDAC_ShieldingLayer))

			target_coordx = tmp1_1[0][0][0][0][-1][0][0][0]['_XY_right'][0]

			if (_CDAC_FoldingTF == False):
				CapSize = 2 ** (_NumofCbit - 0 - 1)
				tmp1_2 = self.get_param_KJH4('SRF_CDAC_Neg','SRF_CDACWtDriver', 'SRF_CDACWtDriver', 'SRF_DriverArray', 'BND_{}C_Driver_Input_Hrz_M3'.format(CapSize))
			else:
				CapSize = 2 ** (_NumofCbit - 1 - 1)
				tmp1_2 = self.get_param_KJH4('SRF_CDAC_Neg','SRF_CDACWtDriver', 'SRF_CDAC_LowerHalf', 'SRF_DriverArray', 'BND_{}C_Driver_Input_Hrz_M3'.format(CapSize))

			target_coordy = tmp1_2[0][0][0][0][0][0]['_XY_up'][1]
			target_coord = [target_coordx,target_coordy]
			## Approaching_coord: _XY_type2
			tmp2_1 = self.get_param_KJH4('SRF_RDACandDecoder_Neg','BND_XgateOut_Hrz_M5')
			approaching_coordx = tmp2_1[0][0][0]['_XY_left'][0]
			tmp2_2 = self.get_param_KJH4('SRF_RDACandDecoder_Neg','BND_B_{}'.format(_NumofRbit-1))
			approaching_coordy = tmp2_2[0][0][0]['_XY_down'][1]
			approaching_coord = [approaching_coordx,approaching_coordy]
			## Sref coord
			tmp3 = self.get_param_KJH4('SRF_RDACandDecoder_Neg')
			Scoord = tmp3[0][0]['_XY_origin']
			## Cal
			New_Scoord = self.get_Scoord_KJH4(target_coord, approaching_coord, Scoord)
			New_Scoord[0] = New_Scoord[0] + 3000
			New_Scoord[1] = New_Scoord[1] - 500
			tmpXY.append(New_Scoord)
			## Define Coordinates
			self._DesignParameter['SRF_RDACandDecoder_Neg']['_XYCoordinates'] = tmpXY
			###################################################################################################

			## ########## ########## ########## ########## ########## ########## ########## ########## ########## ########## ########## SRF_RDACandDecoder_Neg: Vref2CDAC routing
			###### Path_element Generation 2
			## Path Name:
			Path_name = 'RdacVref2Cdac_Neg'

			## Path Width: ***** must be even number ***
			Path_width = 50

			## tmp
			tmpXY = []
			tmpMetal = []
			tmpViaTF = []
			tmpViaDir = []
			tmpViaWid = []

			if _CDAC_FoldingTF == False:
				## coord1
				## P1 calculation
				P1 = [0, 0]
				tmp = self.get_param_KJH4('SRF_RDACandDecoder_Neg','BND_XgateOut_Hrz_M5')
				P1 = tmp[0][0][0]['_XY_left']
				## P2 calculation
				P2 = [0, 0]
				tmp = self.get_param_KJH4('SRF_CDAC_Neg', 'SRF_CDACWtDriver','SRF_CDACWtDriver', 'SRF_CapArray', 'BND_DummyUCAP_Bot_Hrz')

				P2[0] = tmp[0][0][0][0][0][0]['_XY_up_right'][0]
				P2[1] = np.array(P1[1])
				## Metal Layer
				Metal = 5
				## Via: True=1/False=0
				ViaTF = 1
				## Via: Vtc=1/Hrz=0/Ovl=2
				ViaDir = 1
				## Via width: None/[1,3]
				ViaWid = [1,2]

				tmpXY.append([P1, P2])
				tmpMetal.append(Metal)
				tmpViaTF.append(ViaTF)
				tmpViaDir.append(ViaDir)
				tmpViaWid.append(ViaWid)

				## coord2
				## P1 calculation
				P1 = [0, 0]
				P1 = np.array(P2)
				## P2 calculation
				P2 = [0, 0]
				P2[0] = np.array(P1[0])
				tmp = self.get_param_KJH4('SRF_CDAC_Neg', 'SRF_CDACWtDriver','SRF_CDACWtDriver', 'SRF_CapArray', 'BND_DummyUCAP_Bot_Hrz')

				P2[1] = tmp[0][0][0][0][0][0]['_XY_up_right'][1]
				## Metal Layer
				Metal = 3
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
			## Cap Fold
			else:
				## coord1
				## P1 calculation
				tmp = self.get_param_KJH4('SRF_RDACandDecoder_Neg', 'BND_XgateOut_Hrz_M5')
				P1 = tmp[0][0][0]['_XY_left']
				## P2 calculation
				P2 = [P1[0] - 200, P1[1]]
				## Metal Layer
				Metal = 5
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

				## coord2
				## P1 calculation
				P1 = copy.deepcopy(P2)  # = [0, -1000]
				## P2 calculation
				if _CDACDrv_ArrangedTF == False:
					tmp = self.get_param_KJH4('SRF_CDAC_Neg', 'SRF_CDACWtDriver','SRF_CDAC_UpperHalf', 'SRF_CapArray', 'BND_DummyUCAP_Bot_Hrz')
					P2 = [P1[0], tmp[0][0][0][0][0][0]['_XY_cent'][1]]
				else:
					tmp = self.get_param_KJH4('SRF_CDAC_Neg', 'SRF_CDACWtDriver', 'SRF_CDAC_UpperHalf', 'BND_DummyUCAP_Bot_Hrz')
					P2 = [P1[0],tmp[0][0][0][0][0]['_XY_cent'][1]]
				## Metal Layer
				Metal = 4
				## Via True=1/False=0
				ViaTF = 1
				## Via Vtc=1/Hrz=0/Ovl=2
				ViaDir = 0
				## Via width: None/[1,3]
				ViaWid = [2, 1]

				tmpXY.append([P1, P2])
				tmpMetal.append(Metal)
				tmpViaTF.append(ViaTF)
				tmpViaDir.append(ViaDir)
				tmpViaWid.append(ViaWid)

				## coord3
				## P1 calculation
				P1 = copy.deepcopy(P2)  # = [0, -1000]
				## P2 calculation
				if _CDACDrv_ArrangedTF == False:
					tmp = self.get_param_KJH4('SRF_CDAC_Neg', 'SRF_CDACWtDriver','SRF_CDAC_UpperHalf', 'SRF_CapArray', 'BND_DummyUCAP_Bot_Hrz')
					P2 = tmp[0][0][0][0][0][0]['_XY_cent']
				else:
					tmp = self.get_param_KJH4('SRF_CDAC_Neg', 'SRF_CDACWtDriver', 'SRF_CDAC_UpperHalf', 'BND_DummyUCAP_Bot_Hrz')
					P2 = tmp[0][0][0][0][0]['_XY_cent']
				## Metal Layer
				Metal = 3
				## Via True=1/False=0
				ViaTF = 0
				## Via Vtc=1/Hrz=0/Ovl=2
				ViaDir = 0
				## Via width: None/[1,3]
				ViaWid = None

				tmpXY.append([P1, P2])
				tmpMetal.append(Metal)
				tmpViaTF.append(ViaTF)
				tmpViaDir.append(ViaDir)
				tmpViaWid.append(ViaWid)

			tmpXY = self.get_PTH_KJH2(Path_name, Path_width, tmpXY, tmpMetal, tmpViaTF, tmpViaDir, tmpViaWid,_Name)
			###################################################################################################

			## ########## ########## ########## ########## ########## ########## ########## ########## ########## ########## ########## SRF_RDACandDecoder_Neg: Decder Bin. Connect
			## ########## ########## ########## ########## ########## ########## ########## ########## ########## ########## SRF_RDACandDecoder_Neg: Decder Bin. Connect: Hrz M3
			## ########## ########## ########## ########## ########## ########## ########## ########## ########## SRF_RDACandDecoder_Neg: Decder Bin. Connect: Hrz M3: B
			for i in range(0,_NumofRbit):
				## Boundary_element Generation 'BND_B_{}'.format(i)
				Element_name = 'BND_B_{}_Exten_Neg'.format(i)
				## Generate Boundary_element: ex)LayerName: METAL1 / DIFF (_ODLayer) / POLY / PIMP (_PPLayer) / NWELL / SLVT LVT RVT HVT / OP(OPpress) / CONT (CA) / PCCRIT
				self._DesignParameter[Element_name] = self._BoundaryElementDeclaration(
					_Layer=DesignParameters._LayerMapping['METAL3'][0],
					_Datatype=DesignParameters._LayerMapping['METAL3'][1],
					_XWidth=None,
					_YWidth=None,
					_XYCoordinates=[],
				)

				## Define Boundary_element _YWidth
				tmp =self.get_param_KJH4('SRF_RDACandDecoder_Neg','BND_B_{}'.format(i))
				self._DesignParameter[Element_name]['_YWidth'] = tmp[0][0][0]['_Ywidth']

				## Define Boundary_element _XWidth
				Num_Invchain = len(_LOGIC_DACPreDrv_NumberofGate2)-1-i
				Num_InvinChain = len(_LOGIC_DACPreDrv_NumberofGate2[-1-i])-2

				tmp1 = self.get_param_KJH4('SRF_RDACandDecoder_Neg', 'BND_B_{}'.format(i))
				tmp2 = self.get_param_KJH4('SRF_SARLogicWtComparator','SRF_SARLogicWtBuffers','SRF_LowerCDACPreDriver','SRF_InvChain{}'.format(Num_Invchain),'SRF_IntConn_ViaM1M2','SRF_ViaM1M2','BND_Met2Layer') #SRF_Output_ViaM2Mx
				self._DesignParameter[Element_name]['_XWidth'] = (tmp2[0][0][0][0][-1][0][0][0]['_XY_right'][0] - tmp1[0][0][0]['_XY_right'][0])

				## Define Boundary_element _XYCoordinates
				self._DesignParameter[Element_name]['_XYCoordinates'] = [[0, 0]]

				## Calculate Sref XYcoord
				tmpXY = []
				## initialized Sref coordinate
				self._DesignParameter[Element_name]['_XYCoordinates'] = [[0, 0]]
				## Calculate
				## Target_coord: _XY_type1
				tmp1 = self.get_param_KJH4('SRF_RDACandDecoder_Neg','BND_B_{}'.format(i))
				target_coord = tmp1[0][0][0]['_XY_up_right']
				## Approaching_coord: _XY_type2
				tmp2 = self.get_param_KJH4(Element_name)
				approaching_coord = tmp2[0][0]['_XY_down_left']
				## Sref coord
				tmp3 = self.get_param_KJH4(Element_name)
				Scoord = tmp3[0][0]['_XY_origin']
				## Cal
				New_Scoord = self.get_Scoord_KJH4(target_coord, approaching_coord, Scoord)
				tmpXY.append(New_Scoord)
				## Define coordinates
				self._DesignParameter[Element_name]['_XYCoordinates'] = tmpXY
			###################################################################################################

			## ########## ########## ########## ########## ########## ########## ########## ########## ########## SRF_RDACandDecoder_Neg: Decder Bin. Connect: Hrz M3: Bb
				## Boundary_element Generation 'BND_B_{}'.format(i)
				Element_name = 'BND_Bb_{}_Exten_Neg'.format(i)
				## Generate Boundary_element: ex)LayerName: METAL1 / DIFF (_ODLayer) / POLY / PIMP (_PPLayer) / NWELL / SLVT LVT RVT HVT / OP(OPpress) / CONT (CA) / PCCRIT
				self._DesignParameter[Element_name] = self._BoundaryElementDeclaration(
					_Layer=DesignParameters._LayerMapping['METAL3'][0],
					_Datatype=DesignParameters._LayerMapping['METAL3'][1],
					_XWidth=None,
					_YWidth=None,
					_XYCoordinates=[],
				)

				## Define Boundary_element _YWidth
				tmp =self.get_param_KJH4('SRF_RDACandDecoder_Neg','BND_Bb_{}'.format(i))
				self._DesignParameter[Element_name]['_YWidth'] = tmp[0][0][0]['_Ywidth']

				## Define Boundary_element _XWidth
				Num_Invchain = len(_LOGIC_DACPreDrv_NumberofGate2)-1-i
				Num_InvinChain = len(_LOGIC_DACPreDrv_NumberofGate2[-1-i])-2

				tmp1 = self.get_param_KJH4('SRF_RDACandDecoder_Neg', 'BND_Bb_{}'.format(i))
				tmp2 = self.get_param_KJH4('SRF_SARLogicWtComparator','SRF_SARLogicWtBuffers','SRF_LowerCDACPreDriver','SRF_InvChain{}'.format(Num_Invchain),'SRF_Output_ViaM2Mx','SRF_ViaM2M3','BND_Met2Layer') #SRF_Output_ViaM2Mx
				self._DesignParameter[Element_name]['_XWidth'] = (tmp2[0][0][0][0][0][0][0][0]['_XY_right'][0] - tmp1[0][0][0]['_XY_right'][0])

				## Define Boundary_element _XYCoordinates
				self._DesignParameter[Element_name]['_XYCoordinates'] = [[0, 0]]

				## Calculate Sref XYcoord
				tmpXY = []
				## initialized Sref coordinate
				self._DesignParameter[Element_name]['_XYCoordinates'] = [[0, 0]]
				## Calculate
				## Target_coord: _XY_type1
				tmp1 = self.get_param_KJH4('SRF_RDACandDecoder_Neg','BND_Bb_{}'.format(i))
				target_coord = tmp1[0][0][0]['_XY_up_right']
				## Approaching_coord: _XY_type2
				tmp2 = self.get_param_KJH4(Element_name)
				approaching_coord = tmp2[0][0]['_XY_down_left']
				## Sref coord
				tmp3 = self.get_param_KJH4(Element_name)
				Scoord = tmp3[0][0]['_XY_origin']
				## Cal
				New_Scoord = self.get_Scoord_KJH4(target_coord, approaching_coord, Scoord)
				tmpXY.append(New_Scoord)
				## Define coordinates
				self._DesignParameter[Element_name]['_XYCoordinates'] = tmpXY
			###################################################################################################

			## ########## ########## ########## ########## ########## ########## ########## ########## ########## ########## SRF_RDACandDecoder_Neg: Decder Bin. Connect: ViaM3M4 of HrzM3
			## ########## ########## ########## ########## ########## ########## ########## ########## ########## SRF_RDACandDecoder_Neg: Decder Bin. Connect: ViaM3M4 of HrzM3: B

			for i in range(0,_NumofRbit):
				## Sref generation: ViaX
				ViaName = 'SRF_B_{}_Exten_Neg_ViaM3M4'.format(i)
				## Define ViaX Parameter
				_Caculation_Parameters = copy.deepcopy(A02_ViaStack_KJH3._ViaStack._ParametersForDesignCalculation)
				_Caculation_Parameters['_Layer1'] = 3
				_Caculation_Parameters['_Layer2'] = 4
				_Caculation_Parameters['_COX'] = 4
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
				tmp1 = self.get_param_KJH4('BND_B_{}_Exten_Neg'.format(i))
				target_coord = tmp1[0][0]['_XY_right']
				## Approaching_coord
				tmp2 = self.get_param_KJH4(ViaName,'SRF_ViaM3M4','BND_Met3Layer')
				approaching_coord = tmp2[0][0][0][0]['_XY_right']
				## Sref coord
				tmp3 = self.get_param_KJH4(ViaName)
				Scoord = tmp3[0][0]['_XY_origin']
				## Calculate
				New_Scoord = self.get_Scoord_KJH4(target_coord, approaching_coord, Scoord)
				tmpXY.append(New_Scoord)
				## Define
				self._DesignParameter[ViaName]['_XYCoordinates'] = tmpXY
			###################################################################################################

			## ########## ########## ########## ########## ########## ########## ########## ########## ########## SRF_RDACandDecoder_Neg: Decder Bin. Connect: ViaM3M4 of HrzM3: Bb
				## Sref generation: ViaX
				ViaName = 'SRF_Bb_{}_Exten_Neg_ViaM3M4'.format(i)
				## Define ViaX Parameter
				_Caculation_Parameters = copy.deepcopy(A02_ViaStack_KJH3._ViaStack._ParametersForDesignCalculation)
				_Caculation_Parameters['_Layer1'] = 3
				_Caculation_Parameters['_Layer2'] = 4
				_Caculation_Parameters['_COX'] = 4
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
				tmp1 = self.get_param_KJH4('BND_Bb_{}_Exten_Neg'.format(i))
				target_coord = tmp1[0][0]['_XY_right']
				## Approaching_coord
				tmp2 = self.get_param_KJH4(ViaName,'SRF_ViaM3M4','BND_Met3Layer')
				approaching_coord = tmp2[0][0][0][0]['_XY_right']
				## Sref coord
				tmp3 = self.get_param_KJH4(ViaName)
				Scoord = tmp3[0][0]['_XY_origin']
				## Calculate
				New_Scoord = self.get_Scoord_KJH4(target_coord, approaching_coord, Scoord)
				tmpXY.append(New_Scoord)
				## Define
				self._DesignParameter[ViaName]['_XYCoordinates'] = tmpXY
			###################################################################################################

			## ########## ########## ########## ########## ########## ########## ########## ########## ########## ########## SRF_RDACandDecoder_Neg: Decder Bin. Connect: VtcM4
			## ########## ########## ########## ########## ########## ########## ########## ########## ########## SRF_RDACandDecoder_Neg: Decder Bin. Connect: VtcM4: B
			for i in range(0,_NumofRbit):
				## Boundary_element Generation 'BND_B_{}'.format(i)
				Element_name = 'BND_B_{}_Exten_Neg_Vtc_M4'.format(i)
				## Generate Boundary_element: ex)LayerName: METAL1 / DIFF (_ODLayer) / POLY / PIMP (_PPLayer) / NWELL / SLVT LVT RVT HVT / OP(OPpress) / CONT (CA) / PCCRIT
				self._DesignParameter[Element_name] = self._BoundaryElementDeclaration(
					_Layer=DesignParameters._LayerMapping['METAL4'][0],
					_Datatype=DesignParameters._LayerMapping['METAL4'][1],
					_XWidth=None,
					_YWidth=None,
					_XYCoordinates=[],
				)

				## Define Boundary_element _YWidth 'BND_B_{}_Exten_Neg_ViaM3M4'.format(i)
				Num_Invchain = len(_LOGIC_DACPreDrv_NumberofGate2)-1-i
				Num_InvinChain = len(_LOGIC_DACPreDrv_NumberofGate2[-1-i])-2

				tmp1 =self.get_param_KJH4('SRF_B_{}_Exten_Neg_ViaM3M4'.format(i),'SRF_ViaM3M4','BND_Met4Layer')
				tmp2 = self.get_param_KJH4('SRF_SARLogicWtComparator','SRF_SARLogicWtBuffers','SRF_LowerCDACPreDriver','SRF_InvChain{}'.format(Num_Invchain),'SRF_IntConn_ViaM1M2','SRF_ViaM1M2','BND_Met2Layer') #SRF_Output_ViaM2Mx
				self._DesignParameter[Element_name]['_YWidth'] = abs(tmp2[0][0][0][0][-1][0][0][0]['_XY_down'][1] - tmp1[0][0][0][0]['_XY_down'][1])

				## Define Boundary_element _XWidth
				self._DesignParameter[Element_name]['_XWidth'] = 100

				## Define Boundary_element _XYCoordinates
				self._DesignParameter[Element_name]['_XYCoordinates'] = [[0, 0]]

				## Calculate Sref XYcoord
				tmpXY = []
				## initialized Sref coordinate
				self._DesignParameter[Element_name]['_XYCoordinates'] = [[0, 0]]
				## Calculate
				## Target_coord: _XY_type1
				tmp1 = self.get_param_KJH4('SRF_B_{}_Exten_Neg_ViaM3M4'.format(i),'SRF_ViaM3M4','BND_Met4Layer')
				target_coord = tmp1[0][0][0][0]['_XY_down_right']
				## Approaching_coord: _XY_type2
				tmp2 = self.get_param_KJH4(Element_name)
				approaching_coord = tmp2[0][0]['_XY_down_right']
				## Sref coord
				tmp3 = self.get_param_KJH4(Element_name)
				Scoord = tmp3[0][0]['_XY_origin']
				## Cal
				New_Scoord = self.get_Scoord_KJH4(target_coord, approaching_coord, Scoord)
				tmpXY.append(New_Scoord)
				## Define coordinates
				self._DesignParameter[Element_name]['_XYCoordinates'] = tmpXY
			###################################################################################################

				## ########## ########## ########## ########## ########## ########## ########## ########## ########## SRF_RDACandDecoder_Neg: Decder Bin. Connect: VtcM4: Bb
				## Boundary_element Generation 'BND_B_{}'.format(i)
				Element_name = 'BND_Bb_{}_Exten_Neg_Vtc_M4'.format(i)
				## Generate Boundary_element: ex)LayerName: METAL1 / DIFF (_ODLayer) / POLY / PIMP (_PPLayer) / NWELL / SLVT LVT RVT HVT / OP(OPpress) / CONT (CA) / PCCRIT
				self._DesignParameter[Element_name] = self._BoundaryElementDeclaration(
					_Layer=DesignParameters._LayerMapping['METAL4'][0],
					_Datatype=DesignParameters._LayerMapping['METAL4'][1],
					_XWidth=None,
					_YWidth=None,
					_XYCoordinates=[],
				)

				## Define Boundary_element _YWidth 'BND_B_{}_Exten_Neg_ViaM3M4'.format(i)
				Num_Invchain = len(_LOGIC_DACPreDrv_NumberofGate2) - 1 - i
				Num_InvinChain = len(_LOGIC_DACPreDrv_NumberofGate2[-1 - i]) - 2

				tmp1 = self.get_param_KJH4('SRF_Bb_{}_Exten_Neg_ViaM3M4'.format(i), 'SRF_ViaM3M4', 'BND_Met4Layer')
				tmp2 = self.get_param_KJH4('SRF_SARLogicWtComparator', 'SRF_SARLogicWtBuffers', 'SRF_LowerCDACPreDriver', 'SRF_InvChain{}'.format(Num_Invchain), 'SRF_Output_ViaM2Mx', 'SRF_ViaM2M3',
										   'BND_Met2Layer')  # SRF_Output_ViaM2Mx
				self._DesignParameter[Element_name]['_YWidth'] = abs(tmp2[0][0][0][0][0][0][0][0]['_XY_down'][1] - tmp1[0][0][0][0]['_XY_down'][1])

				## Define Boundary_element _XWidth
				self._DesignParameter[Element_name]['_XWidth'] = 100

				## Define Boundary_element _XYCoordinates
				self._DesignParameter[Element_name]['_XYCoordinates'] = [[0, 0]]

				## Calculate Sref XYcoord
				tmpXY = []
				## initialized Sref coordinate
				self._DesignParameter[Element_name]['_XYCoordinates'] = [[0, 0]]
				## Calculate
				## Target_coord: _XY_type1
				tmp1 = self.get_param_KJH4('SRF_Bb_{}_Exten_Neg_ViaM3M4'.format(i), 'SRF_ViaM3M4', 'BND_Met4Layer')
				target_coord = tmp1[0][0][0][0]['_XY_down_right']
				## Approaching_coord: _XY_type2
				tmp2 = self.get_param_KJH4(Element_name)
				approaching_coord = tmp2[0][0]['_XY_down_right']
				## Sref coord
				tmp3 = self.get_param_KJH4(Element_name)
				Scoord = tmp3[0][0]['_XY_origin']
				## Cal
				New_Scoord = self.get_Scoord_KJH4(target_coord, approaching_coord, Scoord)
				tmpXY.append(New_Scoord)
				## Define coordinates
				self._DesignParameter[Element_name]['_XYCoordinates'] = tmpXY
			###################################################################################################

			## ########## ########## ########## ########## ########## ########## ########## ########## ########## ########## SRF_RDACandDecoder_Neg: Decder Bin. Connect: ViaM2M4
			## Sref generation: ViaX
			ViaName = 'SRF_IntConn_Neg_ViaM2M4'
			## Define ViaX Parameter
			_Caculation_Parameters = copy.deepcopy(A02_ViaStack_KJH3._ViaStack._ParametersForDesignCalculation)
			_Caculation_Parameters['_Layer1'] = 2
			_Caculation_Parameters['_Layer2'] = 4
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
			for i in range(0,_NumofRbit):
				## Calculate
				## Target_coord
				Num_Invchain = len(_LOGIC_DACPreDrv_NumberofGate2)-1-i
				Num_InvinChain = len(_LOGIC_DACPreDrv_NumberofGate2[-1-i])-2
				tmp1 = self.get_param_KJH4('SRF_SARLogicWtComparator','SRF_SARLogicWtBuffers','SRF_LowerCDACPreDriver','SRF_InvChain{}'.format(Num_Invchain),'SRF_IntConn_ViaM1M2','SRF_ViaM1M2','BND_Met2Layer') #SRF_Output_ViaM2Mx
				target_coord = tmp1[0][0][0][0][-1][0][0][0]['_XY_up_left']
				## Approaching_coord
				tmp2 = self.get_param_KJH4(ViaName,'SRF_ViaM2M3','BND_Met2Layer')
				approaching_coord = tmp2[0][0][0][0]['_XY_down_left']
				## Sref coord
				tmp3 = self.get_param_KJH4(ViaName)
				Scoord = tmp3[0][0]['_XY_origin']
				## Calculate
				New_Scoord = self.get_Scoord_KJH4(target_coord, approaching_coord, Scoord)
				tmpXY.append(New_Scoord)
			## Define
			self._DesignParameter[ViaName]['_XYCoordinates'] = tmpXY
		###################################################################################################
			## Dummy Inverter distconnection
			if _CDAC_FoldingTF == False:
				if _CDACDrv_ArrangedTF == True:
					del self._DesignParameter['SRF_CDAC_Pos']['_DesignObj']._DesignParameter['SRF_CDACWtDriver']['_DesignObj']._DesignParameter['SRF_CDACWtDriver']['_DesignObj']._DesignParameter['BND_DummyUCAP_Driver_Drain_Vtc_M4']
					del self._DesignParameter['SRF_CDAC_Neg']['_DesignObj']._DesignParameter['SRF_CDACWtDriver']['_DesignObj']._DesignParameter['SRF_CDACWtDriver']['_DesignObj']._DesignParameter['BND_DummyUCAP_Driver_Drain_Vtc_M4']
					del self._DesignParameter['SRF_CDAC_Pos']['_DesignObj']._DesignParameter['SRF_CDACWtDriver']['_DesignObj']._DesignParameter['SRF_CDACWtDriver']['_DesignObj']._DesignParameter['BND_DummyUCAP_BottomNode_Hrz_M3']
					del self._DesignParameter['SRF_CDAC_Neg']['_DesignObj']._DesignParameter['SRF_CDACWtDriver']['_DesignObj']._DesignParameter['SRF_CDACWtDriver']['_DesignObj']._DesignParameter['BND_DummyUCAP_BottomNode_Hrz_M3']
					del self._DesignParameter['SRF_CDAC_Pos']['_DesignObj']._DesignParameter['SRF_CDACWtDriver']['_DesignObj']._DesignParameter['SRF_CDACWtDriver']['_DesignObj']._DesignParameter['SRF_DummyUCAP_Driver_OutputNode_ViaM3M4']
					del self._DesignParameter['SRF_CDAC_Neg']['_DesignObj']._DesignParameter['SRF_CDACWtDriver']['_DesignObj']._DesignParameter['SRF_CDACWtDriver']['_DesignObj']._DesignParameter['SRF_DummyUCAP_Driver_OutputNode_ViaM3M4']
				else:
					del self._DesignParameter['SRF_CDAC_Pos']['_DesignObj']._DesignParameter['SRF_CDACWtDriver']['_DesignObj']._DesignParameter['SRF_CDACWtDriver']['_DesignObj']._DesignParameter['BND_Dummy_Driver_Drain_Vtc_M4']
					del self._DesignParameter['SRF_CDAC_Neg']['_DesignObj']._DesignParameter['SRF_CDACWtDriver']['_DesignObj']._DesignParameter['SRF_CDACWtDriver']['_DesignObj']._DesignParameter['BND_Dummy_Driver_Drain_Vtc_M4']
					del self._DesignParameter['SRF_CDAC_Pos']['_DesignObj']._DesignParameter['SRF_CDACWtDriver']['_DesignObj']._DesignParameter['SRF_CDACWtDriver']['_DesignObj']._DesignParameter['BND_DummyUCAP_BottomNode_Hrz_M3']
					del self._DesignParameter['SRF_CDAC_Neg']['_DesignObj']._DesignParameter['SRF_CDACWtDriver']['_DesignObj']._DesignParameter['SRF_CDACWtDriver']['_DesignObj']._DesignParameter['BND_DummyUCAP_BottomNode_Hrz_M3']
					del self._DesignParameter['SRF_CDAC_Pos']['_DesignObj']._DesignParameter['SRF_CDACWtDriver']['_DesignObj']._DesignParameter['SRF_CDACWtDriver']['_DesignObj']._DesignParameter['SRF_Dummy_Driver_OutputNode_ViaM3M4']
					del self._DesignParameter['SRF_CDAC_Neg']['_DesignObj']._DesignParameter['SRF_CDACWtDriver']['_DesignObj']._DesignParameter['SRF_CDACWtDriver']['_DesignObj']._DesignParameter['SRF_Dummy_Driver_OutputNode_ViaM3M4']
			else:
				if  _CDACDrv_ArrangedTF == True:
					del self._DesignParameter['SRF_CDAC_Pos']['_DesignObj']._DesignParameter['SRF_CDACWtDriver']['_DesignObj']._DesignParameter['BND_CDACFold1_UppB0_DrvOutput_Hrz_M3']
					del self._DesignParameter['SRF_CDAC_Neg']['_DesignObj']._DesignParameter['SRF_CDACWtDriver']['_DesignObj']._DesignParameter['BND_CDACFold1_UppB0_DrvOutput_Hrz_M3']

				else:
					del self._DesignParameter['SRF_CDAC_Pos']['_DesignObj']._DesignParameter['SRF_CDACWtDriver']['_DesignObj']._DesignParameter['SRF_CDAC_UpperHalf']['_DesignObj']._DesignParameter['BND_Dummy_Driver_Drain_Vtc_M4']
					del self._DesignParameter['SRF_CDAC_Neg']['_DesignObj']._DesignParameter['SRF_CDACWtDriver']['_DesignObj']._DesignParameter['SRF_CDAC_UpperHalf']['_DesignObj']._DesignParameter['BND_Dummy_Driver_Drain_Vtc_M4']
					del self._DesignParameter['SRF_CDAC_Pos']['_DesignObj']._DesignParameter['SRF_CDACWtDriver']['_DesignObj']._DesignParameter['SRF_CDAC_UpperHalf']['_DesignObj']._DesignParameter['BND_DummyUCAP_BottomNode_Hrz_M3']
					del self._DesignParameter['SRF_CDAC_Neg']['_DesignObj']._DesignParameter['SRF_CDACWtDriver']['_DesignObj']._DesignParameter['SRF_CDAC_UpperHalf']['_DesignObj']._DesignParameter['BND_DummyUCAP_BottomNode_Hrz_M3']
					del self._DesignParameter['SRF_CDAC_Pos']['_DesignObj']._DesignParameter['SRF_CDACWtDriver']['_DesignObj']._DesignParameter['SRF_CDAC_UpperHalf']['_DesignObj']._DesignParameter['SRF_Dummy_Driver_OutputNode_ViaM3M4']
					del self._DesignParameter['SRF_CDAC_Neg']['_DesignObj']._DesignParameter['SRF_CDACWtDriver']['_DesignObj']._DesignParameter['SRF_CDAC_UpperHalf']['_DesignObj']._DesignParameter['SRF_Dummy_Driver_OutputNode_ViaM3M4']
		###################################################################################################
		###################################################################################################
		print('##############################')
		print('##     Calculation_End      ##')
		print('##############################')
		###################################################################################################
		## Neg연결하기 --> 완료
		## CDAC Only -->완료
		## Folding일때 DummyC에 넣기 --> 완료
		## unfolding일때 dummyC에 잘 연결되지만 inverter와 연결 끊기 -->완료
		## PreDrv (vector)할때 RDAC은 최소 개는 필요하고 안맞으면 갯수 맞게끔 조절하기 -->complete
		## RDAC에서 input 갯수랑 RDAC size랑 연동시키기 --> complete
		## Decimation update --> complete
		## bit != PreDRv lenght erro riase --> complete
############################################################################################################################################################ START MAIN
if __name__ == '__main__':

	''' Check Time'''
	start_time = time.time()

	from KJH91_Projects.Project_ADC.Library_and_Engine.Private import MyInfo
	from KJH91_Projects.Project_ADC.Library_and_Engine import DRCchecker_KJH0

	'''v2 update(250620): decimation update'''

	## LibraryName: ex)Proj_ADC_A_my_building_block
	libname = 'Proj_ZZ01_S00_00_R00C13H06L00_v2'
	## CellName: ex)C01_cap_array_v2_84
	cellname = 'S00_00_R00C13H06L00_v2_99'
	_fileName = cellname + '.gds'

	''' Input Parameters for Layout Object '''
	InputParams = dict(
_NumofCbit=8,
_NumofRbit=4,

## SAR Logic
	## Clock Tree (Driving SAR Logic)
		## Clock Tree Updward (CLK Source Tree, CLK Samp Tree)
			## CLK Buffer Unit
				## Common
				_LOGIC_CLKBufTreeTop_UnitBuf_XVT='SLVT',
				## Nmos
				_LOGIC_CLKBufTreeTop_UnitBuf_NMOS_NumberofGate=1,  # Number
				_LOGIC_CLKBufTreeTop_UnitBuf_NMOS_ChannelWidth=400,  # Number
				_LOGIC_CLKBufTreeTop_UnitBuf_NMOS_ChannelLength=30,  # Number
				## Pmos
				_LOGIC_CLKBufTreeTop_UnitBuf_PMOS_NumberofGate=1,  # Number
				_LOGIC_CLKBufTreeTop_UnitBuf_PMOS_ChannelWidth=800,  # Number
				_LOGIC_CLKBufTreeTop_UnitBuf_PMOS_ChannelLength=30,  # Number
				# Height
				_LOGIC_CLKBufTreeTop_UnitBuf_PMOSXvt2NMOSXvt=446,  # number
			## Clock Buffer Tree structure
			_LOGIC_CLKBufTreeTop_BufTree1and2_NumOfStage=4,  # len[Buf0, Buf1, ... ] 스테이지 수 (아래 버퍼 사이즈 리스트의 길이와 같아야 함.)
			_LOGIC_CLKBufTreeTop_BufTree1_SizeofEachStage=[1, 2, 4, 8],  # CLKSampBuf: [Buf0, Buf1, Buf2 ...]
			_LOGIC_CLKBufTreeTop_BufTree2_SizeofEachStage=[1, 2, 4, 8],  # CLKSrcBuf: [Buf0, Buf1, Buf2 ...]
			_LOGIC_CLKBufTreeTop_XOffSet=0,
		## Clock Tree Dnward (CLK Source Tree, CLK Samp Tree)
			## CLK Buffer Unit
				## Common
				_LOGIC_CLKBufTreeBot_UnitBuf_XVT='SLVT',
				## Nmos
				_LOGIC_CLKBufTreeBot_UnitBuf_NMOS_NumberofGate=1,  # Number
				_LOGIC_CLKBufTreeBot_UnitBuf_NMOS_ChannelWidth=400,  # Number
				_LOGIC_CLKBufTreeBot_UnitBuf_NMOS_ChannelLength=30,  # Number
				## Pmos
				_LOGIC_CLKBufTreeBot_UnitBuf_PMOS_NumberofGate=1,  # Number
				_LOGIC_CLKBufTreeBot_UnitBuf_PMOS_ChannelWidth=800,  # Number
				_LOGIC_CLKBufTreeBot_UnitBuf_PMOS_ChannelLength=30,  # Number
				# Height
				_LOGIC_CLKBufTreeBot_UnitBuf_PMOSXvt2NMOSXvt=446,  # number
			## Clock Buffer Tree structure
			_LOGIC_CLKBufTreeBot_BufTree1and2_NumOfStage=4,  # len[Buf0, Buf1, ... ] 스테이지 수 (아래 버퍼 사이즈 리스트의 길이와 같아야 함.)
			_LOGIC_CLKBufTreeBot_BufTree1_SizeofEachStage=[1, 2, 4, 8],  # CompOutBuf: [Buf0, Buf1, Buf2 ...]
			_LOGIC_CLKBufTreeBot_BufTree2_SizeofEachStage=[1, 2, 4, 8],  # CLKDoutBuf: [Buf0, Buf1, Buf2 ...]
			_LOGIC_CLKBufTreeBot_XOffSet=0,

	## Clock Spine (Physical demension)
		## CLK Source: upward, 1st floor
		_LOGIC_YWidthOfCLKSrc=100,
		## CLK Samp: upward, 2nd floor
		_LOGIC_SpaceBtwCLKSrcAndCLKSamp=100,
		_LOGIC_YWidthOfCLKSamp=100,
		## Comparator Output: downward, Basement1
		_LOGIC_YWidthOfCompOut=100,
		## CLK Dout: downward, basement2
		_LOGIC_SpaceBtwCompOutAndCLKDout=100,
		_LOGIC_YWidthOfCLKDout=100,

	## SetResetDFF
		## DFF Common
		_LOGIC_Test_distance=320,
		_LOGIC_DFF_PMOSXvt2NMOSXvt    = 1150, # number

		## Master Xgate1
			## Xgate common
			_LOGIC_Mst_Xgate1_XVT='SLVT',
			## Xgate NMOS
			_LOGIC_Mst_Xgate1_NMOS_NumberofGate=1,
			_LOGIC_Mst_Xgate1_NMOS_ChannelWidth=300,
			_LOGIC_Mst_Xgate1_NMOS_ChannelLength=30,
			## Xgate PMOS
			_LOGIC_Mst_Xgate1_PMOS_NumberofGate=3,
			_LOGIC_Mst_Xgate1_PMOS_ChannelWidth=500,
			_LOGIC_Mst_Xgate1_PMOS_ChannelLength=30,

		## Master Xgate2
			## Xgate common
			_LOGIC_Mst_Xgate2_XVT='SLVT',
			## Xgate NMOS
			_LOGIC_Mst_Xgate2_NMOS_NumberofGate           = 2,
			_LOGIC_Mst_Xgate2_NMOS_ChannelWidth           = 800,
			_LOGIC_Mst_Xgate2_NMOS_ChannelLength          = 30,
			## Xgate PMOS
			_LOGIC_Mst_Xgate2_PMOS_NumberofGate           = 3,
			_LOGIC_Mst_Xgate2_PMOS_ChannelWidth           = 200,
			_LOGIC_Mst_Xgate2_PMOS_ChannelLength          = 30,

		## Master Nor1
			## Nor1 common
			_LOGIC_Mst_Nor1_XVT='SLVT',
			## NMOS
				## NMOSA
				_LOGIC_Mst_Nor1_NMOSA_NumberofGate           = 2,
				_LOGIC_Mst_Nor1_NMOSA_ChannelWidth           = 800,
				_LOGIC_Mst_Nor1_NMOSA_ChannelLength          = 30,
				## NMOSB
				_LOGIC_Mst_Nor1_NMOSB_NumberofGate           = 3,
				_LOGIC_Mst_Nor1_NMOSB_ChannelWidth           = 200,
				_LOGIC_Mst_Nor1_NMOSB_ChannelLength          = 30,
			## PMOS
				## PMOSA
				_LOGIC_Mst_Nor1_PMOSA_NumberofGate            = 2,
				_LOGIC_Mst_Nor1_PMOSA_ChannelWidth            = 800,
				_LOGIC_Mst_Nor1_PMOSA_ChannelLength           = 30,
				## PMOSB
				_LOGIC_Mst_Nor1_PMOSB_NumberofGate            = 3,
				_LOGIC_Mst_Nor1_PMOSB_ChannelWidth            = 200,
				_LOGIC_Mst_Nor1_PMOSB_ChannelLength           = 30,

		## Master Nor2
			## Nor2 common
			_LOGIC_Mst_Nor2_XVT='SLVT',
			## NMOS
				## NMOSA
				_LOGIC_Mst_Nor2_NMOSA_NumberofGate           = 2,
				_LOGIC_Mst_Nor2_NMOSA_ChannelWidth           = 800,
				_LOGIC_Mst_Nor2_NMOSA_ChannelLength          = 30,
				## NMOSB
				_LOGIC_Mst_Nor2_NMOSB_NumberofGate           = 3,
				_LOGIC_Mst_Nor2_NMOSB_ChannelWidth           = 200,
				_LOGIC_Mst_Nor2_NMOSB_ChannelLength          = 30,
			## PMOS
				## PMOSA
				_LOGIC_Mst_Nor2_PMOSA_NumberofGate            = 2,
				_LOGIC_Mst_Nor2_PMOSA_ChannelWidth            = 800,
				_LOGIC_Mst_Nor2_PMOSA_ChannelLength           = 30,
				## PMOSB
				_LOGIC_Mst_Nor2_PMOSB_NumberofGate            = 3,
				_LOGIC_Mst_Nor2_PMOSB_ChannelWidth            = 200,
				_LOGIC_Mst_Nor2_PMOSB_ChannelLength           = 30,

		## Master Inv1 : Set pre-driver
			## Inv1 common
			_LOGIC_Mst_Inv1_XVT='SLVT',
			## Inv1 NMOS
			_LOGIC_Mst_Inv1_NMOS_NumberofGate           = 1,
			_LOGIC_Mst_Inv1_NMOS_ChannelWidth           = 300,
			_LOGIC_Mst_Inv1_NMOS_ChannelLength          = 30,
			## Inv1 PMOS
			_LOGIC_Mst_Inv1_PMOS_NumberofGate           = 3,
			_LOGIC_Mst_Inv1_PMOS_ChannelWidth           = 500,
			_LOGIC_Mst_Inv1_PMOS_ChannelLength          = 30,

		## Master Inv2 : Set driver
			## Inv2 common
			_LOGIC_Mst_Inv2_XVT='SLVT',
			## Inv2 NMOS
			_LOGIC_Mst_Inv2_NMOS_NumberofGate           = 1,
			_LOGIC_Mst_Inv2_NMOS_ChannelWidth           = 300,
			_LOGIC_Mst_Inv2_NMOS_ChannelLength          = 30,
			## Inv2 PMOS
			_LOGIC_Mst_Inv2_PMOS_NumberofGate           = 3,
			_LOGIC_Mst_Inv2_PMOS_ChannelWidth           = 500,
			_LOGIC_Mst_Inv2_PMOS_ChannelLength          = 30,

		## Master Inv3 : Clock driver
			## Inv3 common
			_LOGIC_Mst_Inv3_XVT='SLVT',
			## Inv3 NMOS
			_LOGIC_Mst_Inv3_NMOS_NumberofGate           = 1,
			_LOGIC_Mst_Inv3_NMOS_ChannelWidth           = 300,
			_LOGIC_Mst_Inv3_NMOS_ChannelLength          = 30,
			## Inv3 PMOS
			_LOGIC_Mst_Inv3_PMOS_NumberofGate           = 3,
			_LOGIC_Mst_Inv3_PMOS_ChannelWidth           = 500,
			_LOGIC_Mst_Inv3_PMOS_ChannelLength          = 30,

		## Slave Xgate1
			## Xgate common
			_LOGIC_Slv_Xgate1_XVT='SLVT',
			## Xgate NMOS
			_LOGIC_Slv_Xgate1_NMOS_NumberofGate           = 1,
			_LOGIC_Slv_Xgate1_NMOS_ChannelWidth           = 300,
			_LOGIC_Slv_Xgate1_NMOS_ChannelLength          = 30,
			## Xgate PMOS
			_LOGIC_Slv_Xgate1_PMOS_NumberofGate           = 3,
			_LOGIC_Slv_Xgate1_PMOS_ChannelWidth           = 500,
			_LOGIC_Slv_Xgate1_PMOS_ChannelLength          = 30,

		## Slave Xgate2
			## Xgate common
			_LOGIC_Slv_Xgate2_XVT='SLVT',
			## Xgate NMOS
			_LOGIC_Slv_Xgate2_NMOS_NumberofGate           = 2,
			_LOGIC_Slv_Xgate2_NMOS_ChannelWidth           = 800,
			_LOGIC_Slv_Xgate2_NMOS_ChannelLength          = 30,
			## Xgate PMOS
			_LOGIC_Slv_Xgate2_PMOS_NumberofGate           = 3,
			_LOGIC_Slv_Xgate2_PMOS_ChannelWidth           = 200,
			_LOGIC_Slv_Xgate2_PMOS_ChannelLength          = 30,

		## Slave Nor1
			## Nor1 common
			_LOGIC_Slv_Nor1_XVT='SLVT',
			## NMOS
				## NMOSA
				_LOGIC_Slv_Nor1_NMOSA_NumberofGate           = 2,
				_LOGIC_Slv_Nor1_NMOSA_ChannelWidth           = 800,
				_LOGIC_Slv_Nor1_NMOSA_ChannelLength          = 30,
				## NMOSB
				_LOGIC_Slv_Nor1_NMOSB_NumberofGate           = 3,
				_LOGIC_Slv_Nor1_NMOSB_ChannelWidth           = 200,
				_LOGIC_Slv_Nor1_NMOSB_ChannelLength          = 30,
			## PMOS
				## PMOSA
				_LOGIC_Slv_Nor1_PMOSA_NumberofGate            = 2,
				_LOGIC_Slv_Nor1_PMOSA_ChannelWidth            = 800,
				_LOGIC_Slv_Nor1_PMOSA_ChannelLength           = 30,
				## PMOSB
				_LOGIC_Slv_Nor1_PMOSB_NumberofGate            = 3,
				_LOGIC_Slv_Nor1_PMOSB_ChannelWidth            = 200,
				_LOGIC_Slv_Nor1_PMOSB_ChannelLength           = 30,

		## Slave Nor2
			## Nor2 common
			_LOGIC_Slv_Nor2_XVT='SLVT',
			## NMOS
				## NMOSA
				_LOGIC_Slv_Nor2_NMOSA_NumberofGate           = 2,
				_LOGIC_Slv_Nor2_NMOSA_ChannelWidth           = 800,
				_LOGIC_Slv_Nor2_NMOSA_ChannelLength          = 30,
				## NMOSB
				_LOGIC_Slv_Nor2_NMOSB_NumberofGate           = 3,
				_LOGIC_Slv_Nor2_NMOSB_ChannelWidth           = 200,
				_LOGIC_Slv_Nor2_NMOSB_ChannelLength          = 30,
			## PMOS
				## PMOSA
				_LOGIC_Slv_Nor2_PMOSA_NumberofGate            = 2,
				_LOGIC_Slv_Nor2_PMOSA_ChannelWidth            = 800,
				_LOGIC_Slv_Nor2_PMOSA_ChannelLength           = 30,
				## PMOSB
				_LOGIC_Slv_Nor2_PMOSB_NumberofGate            = 3,
				_LOGIC_Slv_Nor2_PMOSB_ChannelWidth            = 200,
				_LOGIC_Slv_Nor2_PMOSB_ChannelLength           = 30,

		## Slave Inv1 : ReSet pre-driver
			## Inv1 common
			_LOGIC_Slv_Inv1_XVT='SLVT',
			## Inv1 NMOS
			_LOGIC_Slv_Inv1_NMOS_NumberofGate           = 1,
			_LOGIC_Slv_Inv1_NMOS_ChannelWidth           = 300,
			_LOGIC_Slv_Inv1_NMOS_ChannelLength          = 30,
			## Inv1 PMOS
			_LOGIC_Slv_Inv1_PMOS_NumberofGate           = 3,
			_LOGIC_Slv_Inv1_PMOS_ChannelWidth           = 500,
			_LOGIC_Slv_Inv1_PMOS_ChannelLength          = 30,

		## Slave Inv2 : ReSet driver
			## Inv2 common
			_LOGIC_Slv_Inv2_XVT='SLVT',
			## Inv2 NMOS
			_LOGIC_Slv_Inv2_NMOS_NumberofGate           = 1,
			_LOGIC_Slv_Inv2_NMOS_ChannelWidth           = 300,
			_LOGIC_Slv_Inv2_NMOS_ChannelLength          = 30,
			## Inv2 PMOS
			_LOGIC_Slv_Inv2_PMOS_NumberofGate           = 3,
			_LOGIC_Slv_Inv2_PMOS_ChannelWidth           = 500,
			_LOGIC_Slv_Inv2_PMOS_ChannelLength          = 30,

		## Slave Inv3 : Qb driver
			## Inv3 common
			_LOGIC_Slv_Inv3_XVT='SLVT',
			## Inv3 NMOS
			_LOGIC_Slv_Inv3_NMOS_NumberofGate           = 1,
			_LOGIC_Slv_Inv3_NMOS_ChannelWidth           = 300,
			_LOGIC_Slv_Inv3_NMOS_ChannelLength          = 30,
			## Inv3 PMOS
			_LOGIC_Slv_Inv3_PMOS_NumberofGate           = 3,
			_LOGIC_Slv_Inv3_PMOS_ChannelWidth           = 500,
			_LOGIC_Slv_Inv3_PMOS_ChannelLength          = 30,
	## DAC PreDriver
		## Inverter Chain
			## InvChain Common
			_LOGIC_DACPreDrv_PMOSXvt2NMOSXvt=500,  # number
			## Inverter Chain
				## Inv1 common
			_LOGIC_DACPreDrv_NumberofGate=[[1, 2, 4, 8],[1, 2, 4, 8], [1, 2, 4, 8], [1],[1],[1],[1],[1],    [1],[1],[1],[1]],  # Vector
			_RDAC_InputComple_Inv_NumofGate = [1,2,3,1], # Vector, _LOGIC_DACPreDrv_NumberofGate + _RDAC_InputComple_Inv_NumofGate로 입력됨
			_LOGIC_DACPreDrv_ChannelLength=30,  # Scalar
			_LOGIC_DACPreDrv_XVT='SLVT',  # 'SLVT'
				## Inv1 NMOS
			_LOGIC_DACPreDrv_Inv_NMOS_ChannelWidth=400,  # Scalar
				## Inv1 PMOS
			_LOGIC_DACPreDrv_Inv_PMOS_ChannelWidth=800,  # Scalar
	## CLKOutSamp(!=ClkSamp)
		## Common
			# XVT
			_LOGIC_CLKoutSamp_XVT = 'SLVT',
			# Height
			# _CLKOutSamp_PMOSXvt2NMOSXvt=1800,  # number, = _DFF_PMOSXvt2NMOSXvt
		## Inverter
			# Nmos
			_LOGIC_CLKoutSamp_Inv_NMOS_NumberofGate=1,  # Number
			_LOGIC_CLKoutSamp_Inv_NMOS_ChannelWidth=100,  # Number
			_LOGIC_CLKoutSamp_Inv_NMOS_ChannelLength=30,  # Number
			# Pmos
			_LOGIC_CLKoutSamp_Inv_PMOS_NumberofGate=1,  # Number
			_LOGIC_CLKoutSamp_Inv_PMOS_ChannelWidth=100,  # Number
			_LOGIC_CLKoutSamp_Inv_PMOS_ChannelLength=30,  # Number
		## AND
			## AND Common
			## Nand
				# NmosA
				_LOGIC_CLKoutSamp_And_Nand_NMOSA_NumberofGate=1,  # Number
				_LOGIC_CLKoutSamp_And_Nand_NMOSA_ChannelWidth=100,  # Number
				_LOGIC_CLKoutSamp_And_Nand_NMOSA_ChannelLength=30,  # Number
				# NMOSB
				_LOGIC_CLKoutSamp_And_Nand_NMOSB_NumberofGate=2,  # Number
				_LOGIC_CLKoutSamp_And_Nand_NMOSB_ChannelWidth=750,  # Number
				_LOGIC_CLKoutSamp_And_Nand_NMOSB_ChannelLength=30,  # Number
				# PMOSA
				_LOGIC_CLKoutSamp_And_Nand_PMOSA_NumberofGate=1,  # Number
				_LOGIC_CLKoutSamp_And_Nand_PMOSA_ChannelWidth=300,  # Number
				_LOGIC_CLKoutSamp_And_Nand_PMOSA_ChannelLength=30,  # Number
				# PMOSB
				_LOGIC_CLKoutSamp_And_Nand_PMOSB_NumberofGate=3,  # Number
				_LOGIC_CLKoutSamp_And_Nand_PMOSB_ChannelWidth=750,  # Number
				_LOGIC_CLKoutSamp_And_Nand_PMOSB_ChannelLength=30,  # Number
			## Inverter
				# Nmos
				_LOGIC_CLKoutSamp_And_Inv_NMOS_NumberofGate=1,  # Number
				_LOGIC_CLKoutSamp_And_Inv_NMOS_ChannelWidth=100,  # Number
				_LOGIC_CLKoutSamp_And_Inv_NMOS_ChannelLength=30,  # Number
				# Pmos
				_LOGIC_CLKoutSamp_And_Inv_PMOS_NumberofGate=1,  # Number
				_LOGIC_CLKoutSamp_And_Inv_PMOS_ChannelWidth=200,  # Number
				_LOGIC_CLKoutSamp_And_Inv_PMOS_ChannelLength=30,  # Number


## Comparator
	## StrongARM Latch
		# Common
		_COMP_SALatch_ChannelLength=30,  # random.randrange(30, 60, 2),  # 30
		_COMP_SALatch_XVT='HVT',

		# PMOS
		_COMP_SALatch_CLKinputPMOSFinger1=1,  #PMOS Reset Sw1 # random.randint(1, 15),  # 6
		_COMP_SALatch_CLKinputPMOSFinger2=1,  #PMOS Reset Sw2 # random.randint(1, 15),  # 3
		_COMP_SALatch_PMOSFinger=1,  		  #PMOS Latch	  # random.randint(1, 15),  # 3
		_COMP_SALatch_PMOSChannelWidth=1000,  #All PMOS width # random.randrange(200, 1050, 2),  # 500

		# NMOS
		_COMP_SALatch_DATAinputNMOSFinger=3,  #NMOS Input Tr # random.randint(3, 15),  # 12
		_COMP_SALatch_NMOSFinger=2,  		  #NMOS at Latch # random.randint(1, 15),  # 2
		_COMP_SALatch_CLKinputNMOSFinger=1,  #NMOS Tail # random.randint(1, 15),  # 8
		_COMP_SALatch_NMOSChannelWidth=330,  #Nmos width # random.randrange(200, 1050, 2),  # 500
		_COMP_SALatch_CLKinputNMOSChannelWidth=200,  # random.randrange(200, 1050, 2),  # 800

	## StrongArmOutBuffer and SRLatch
		## Common
			# XVT
			_COMP_SAOutBufAndSRLatch_XVT='SLVT',
			# Body
			_COMP_SAOutBufAndSRLatch_NMOS_Pbody_XvtTop2Pbody=None,  # Number/None(Minimum)
			_COMP_SAOutBufAndSRLatch_PMOS_Nbody_Xvtdown2Nbody=None,  # Number/None(Minimum)
			# Height
			_COMP_SAOutBufAndSRLatch_PMOSXvt2NMOSXvt=1800,  # number
		## StronArm Output Buffer
			## Inverter1(pre)
					#Nmos
				_COMP_SAOutBuf_Buf_Inv1_NMOS_NumberofGate          = 1,        # Number
				_COMP_SAOutBuf_Buf_Inv1_NMOS_ChannelWidth          = 400,      # Number
				_COMP_SAOutBuf_Buf_Inv1_NMOS_ChannelLength         = 30,       # Number
					#Pmos
				_COMP_SAOutBuf_Buf_Inv1_PMOS_NumberofGate          = 1,        # Number
				_COMP_SAOutBuf_Buf_Inv1_PMOS_ChannelWidth          = 800,      # Number
				_COMP_SAOutBuf_Buf_Inv1_PMOS_ChannelLength         = 30,       # Number
			## Inverter2
					#Nmos
				_COMP_SAOutBuf_Buf_Inv2_NMOS_NumberofGate          = 2,        # Number
				_COMP_SAOutBuf_Buf_Inv2_NMOS_ChannelWidth          = 400,      # Number
				_COMP_SAOutBuf_Buf_Inv2_NMOS_ChannelLength         = 30,       # Number
					#Pmos
				_COMP_SAOutBuf_Buf_Inv2_PMOS_NumberofGate          = 2,        # Number
				_COMP_SAOutBuf_Buf_Inv2_PMOS_ChannelWidth          = 800,      # Number
				_COMP_SAOutBuf_Buf_Inv2_PMOS_ChannelLength         = 30,       # Number
		## SRLatch
			## Nand(Set,Rst same)
				# NmosA
				_COMP_SRLatch_Nand_NMOSA_NumberofGate=1,  # Number
				_COMP_SRLatch_Nand_NMOSA_ChannelWidth=100,  # Number
				_COMP_SRLatch_Nand_NMOSA_ChannelLength=30,  # Number
				# NMOSB
				_COMP_SRLatch_Nand_NMOSB_NumberofGate=2,  # Number
				_COMP_SRLatch_Nand_NMOSB_ChannelWidth=750,  # Number
				_COMP_SRLatch_Nand_NMOSB_ChannelLength=30,  # Number
				# PMOSA
				_COMP_SRLatch_Nand_PMOSA_NumberofGate=2,  # Number
				_COMP_SRLatch_Nand_PMOSA_ChannelWidth=100,  # Number
				_COMP_SRLatch_Nand_PMOSA_ChannelLength=30,  # Number
				# PMOSB
				_COMP_SRLatch_Nand_PMOSB_NumberofGate=1,  # Number
				_COMP_SRLatch_Nand_PMOSB_ChannelWidth=750,  # Number
				_COMP_SRLatch_Nand_PMOSB_ChannelLength=30,  # Number

	## Comp clock Gen Logic: Clk_Samp Inv, Clk_Source Inv, AND Gate, CompClockBuff
		## Common
			# XVT
			_COMP_CompClkLogic_XVT='SLVT',
			# Body
			_COMP_CompClkLogic_NMOS_Pbody_XvtTop2Pbody=None,  # Number/None(Minimum)
			_COMP_CompClkLogic_PMOS_Nbody_Xvtdown2Nbody=None,  # Number/None(Minimum)
			# Height
			_COMP_CompClkLogic_PMOSXvt2NMOSXvt=1800,  # number
		## StronArm Output Buffer
			## Inverter1(pre)
					#Nmos
				_COMP_CompClkLogic_Buf_Inv1_NMOS_NumberofGate          = 2,        # Number
				_COMP_CompClkLogic_Buf_Inv1_NMOS_ChannelWidth          = 400,      # Number
				_COMP_CompClkLogic_Buf_Inv1_NMOS_ChannelLength         = 30,       # Number
					#Pmos
				_COMP_CompClkLogic_Buf_Inv1_PMOS_NumberofGate          = 2,        # Number
				_COMP_CompClkLogic_Buf_Inv1_PMOS_ChannelWidth          = 800,      # Number
				_COMP_CompClkLogic_Buf_Inv1_PMOS_ChannelLength         = 30,       # Number
			## Inverter2
					#Nmos
				_COMP_CompClkLogic_Buf_Inv2_NMOS_NumberofGate          = 4,        # Number
				_COMP_CompClkLogic_Buf_Inv2_NMOS_ChannelWidth          = 400,      # Number
				_COMP_CompClkLogic_Buf_Inv2_NMOS_ChannelLength         = 30,       # Number
					#Pmos
				_COMP_CompClkLogic_Buf_Inv2_PMOS_NumberofGate          = 4,        # Number
				_COMP_CompClkLogic_Buf_Inv2_PMOS_ChannelWidth          = 800,      # Number
				_COMP_CompClkLogic_Buf_Inv2_PMOS_ChannelLength         = 30,       # Number
		## AND
			## Nand
				# NmosA
				_COMP_CompClkLogic_Nand_NMOSA_NumberofGate=1,  # Number
				_COMP_CompClkLogic_Nand_NMOSA_ChannelWidth=100,  # Number
				_COMP_CompClkLogic_Nand_NMOSA_ChannelLength=30,  # Number
				# NMOSB
				_COMP_CompClkLogic_Nand_NMOSB_NumberofGate=2,  # Number
				_COMP_CompClkLogic_Nand_NMOSB_ChannelWidth=750,  # Number
				_COMP_CompClkLogic_Nand_NMOSB_ChannelLength=30,  # Number
				# PMOSA
				_COMP_CompClkLogic_Nand_PMOSA_NumberofGate=1,  # Number
				_COMP_CompClkLogic_Nand_PMOSA_ChannelWidth=300,  # Number
				_COMP_CompClkLogic_Nand_PMOSA_ChannelLength=30,  # Number
				# PMOSB
				_COMP_CompClkLogic_Nand_PMOSB_NumberofGate=3,  # Number
				_COMP_CompClkLogic_Nand_PMOSB_ChannelWidth=750,  # Number
				_COMP_CompClkLogic_Nand_PMOSB_ChannelLength=30,  # Number
			## Inverter
				# Nmos
				_COMP_CompClkLogic_Inv_NMOS_NumberofGate=1,  # Number
				_COMP_CompClkLogic_Inv_NMOS_ChannelWidth=100,  # Number
				_COMP_CompClkLogic_Inv_NMOS_ChannelLength=30,  # Number
				# Pmos
				_COMP_CompClkLogic_Inv_PMOS_NumberofGate=1,  # Number
				_COMP_CompClkLogic_Inv_PMOS_ChannelWidth=200,  # Number
				_COMP_CompClkLogic_Inv_PMOS_ChannelLength=30,  # Number

		## Clk_Source Inv
				#Nmos
			_COMP_CompClkLogic_ClkSrc_NMOS_NumberofGate          = 1,        # Number
			_COMP_CompClkLogic_ClkSrc_NMOS_ChannelWidth          = 400,      # Number
			_COMP_CompClkLogic_ClkSrc_NMOS_ChannelLength         = 30,       # Number
				#Pmos
			_COMP_CompClkLogic_ClkSrc_PMOS_NumberofGate          = 1,        # Number
			_COMP_CompClkLogic_ClkSrc_PMOS_ChannelWidth          = 800,      # Number
			_COMP_CompClkLogic_ClkSrc_PMOS_ChannelLength         = 30,       # Number
		## Clk_Samp Inv
				#Nmos
			_COMP_CompClkLogic_ClkSmp_NMOS_NumberofGate          = 1,        # Number
			_COMP_CompClkLogic_ClkSmp_NMOS_ChannelWidth          = 400,      # Number
			_COMP_CompClkLogic_ClkSmp_NMOS_ChannelLength         = 30,       # Number
				#Pmos
			_COMP_CompClkLogic_ClkSmp_PMOS_NumberofGate          = 1,        # Number
			_COMP_CompClkLogic_ClkSmp_PMOS_ChannelWidth          = 800,      # Number
			_COMP_CompClkLogic_ClkSmp_PMOS_ChannelLength         = 30,       # Number




## CLOCK AND DATA BUF : Comparator Dout Buf for driving Logic, CLKSamp and CLKScr Buff for Driving Sampler and Comparator
	## Top placed
		## CLK Samp
			## InvChain Common
				## Height
		_BUF_CLKSamp_PMOSXvt2NMOSXvt = 500,  # number
			## Inverter Chain
				## Inv1 common
		_BUF_CLKSamp_XVT='SLVT',
		_BUF_CLKSamp_NumberofGate = [1,2,4,8],  # Vector,
		_BUF_CLKSamp_ChanneLength = 30,
				## NMOS
		_BUF_CLKSamp_NMOSChannelWidth = 784,
				## PMOS
		_BUF_CLKSamp_PMOSChannelWidth = 833,
		## CLK Scr
			## InvChain Common
				## Height
		_BUF_CLKScr_PMOSXvt2NMOSXvt = 500,  # number
			## Inverter Chain
				## Inv1 common
		_BUF_CLKScr_XVT='SLVT',
		_BUF_CLKScr_NumberofGate = [1,2,4,8],  # Vector,
		_BUF_CLKScr_ChanneLength = 30,
				## NMOS
		_BUF_CLKScr_NMOSChannelWidth = 784,
				## PMOS
		_BUF_CLKScr_PMOSChannelWidth = 833,
	## Bottom Placed
		## CompOut
			## InvChain Common
				## Height
		_BUF_CompOut_PMOSXvt2NMOSXvt = 500,  # number
			## Inverter Chain
				## Inv1 common
		_BUF_CompOut_XVT='SLVT',
		_BUF_CompOut_NumberofGate = [1,2,4,8],  # Vector,
		_BUF_CompOut_ChanneLength = 30,
				## NMOS
		_BUF_CompOut_NMOSChannelWidth = 784,
				## PMOS
		_BUF_CompOut_PMOSChannelWidth = 833,



## CDAC
	## CDAC Configuration
	_CDAC_FoldingTF = False, #True/False
	_CDACDrv_ArrangedTF = False, #True= Arranged, False=CommonCent
	## CDAC Drv
		## Unit DRv
			## Common
				# XVT
			_CDACDrv_XVT = 'SLVT',
			## NMOS
			_CDACDrv_NMOS_NumberofGate=1,  # Number
			_CDACDrv_NMOS_ChannelWidth = 145, #Number
			_CDACDrv_NMOS_ChannelLength = 30, #Number
			## PMOS
			_CDACDrv_PMOS_NumberofGate=1,  # Number
			_CDACDrv_PMOS_ChannelWidth = 879, #Number
			_CDACDrv_PMOS_ChannelLength = 30, #Number
		## Option1: Decimation (CommonCentroid Only, _CDACDrv_ArrangedTF = 'False')
		##			ex) len(_CDACDrv_Decimation_Factor) == _NumofCbit// coresponse to [MSB, MSB-1, ... LSB(=UnitCap)] // If MSB=3, MSBDRv:128 --> 43(128을 3으로 나눈몫+1) // "1" means no decimation
		_CDACDrv_Decimation_Factor=[3, 1, 5, 1, 1, 1, 1, 1],
		## Option2: (Arragned Only, _CDACDrv_ArrangedTF = 'True')
		_CDACDrv_DesignatedEachSize = [8,4,3,3], # Vector, designates each driver size(multiples of Unit Drv size)
	## CDAC
			## Element CDAC
			_CDAC_LayoutOption=[3],  # Vector, Consecutive Number [3,4,5]
			_CDAC_MetalWidth=50,  # Number
			_CDAC_MetalLength=1410,  # Number (8bit size: 1414/ 10bit size: 2800/ 12bit size: 4200)
			_CDAC_MetalSpacing=50,  # Number

			## Unit Cap
			_CDAC_NumOfElement=2,  # Number

			## Shield
			_CDAC_ShieldingLayer=1,  # Poly:0, M1:1, M2:2 ...
			_CDAC_ConnectLength=411,  # Number
			_CDAC_ExtendLength=400,  # Number

			## Dummy Cap Option
			_CDAC_NumOfDummyCaps=9,  # Number, Number of dummy cap(one side)
			_CDAC_DummyCap_TopBottomShort=None,  # True => Top - Bottom Short, False -> Bottom = GND, None => Floating Bottom Node

			## CommonCentroid With Driving node
			_CDAC_CapArrayWDrivingNodeDistance=1611,  # Number
			_CDAC_DriveNodeDistance=279,  # Number
			_CDAC_YWidth_Bottom_Hrz=60,  # Number
			_CDAC_BotNodeVtcExtensionMetalLayer=1,




## Bootstrapped Switch
	# Input/Output node
		# INPUT node
		_Sampler_Inputnode_width = 500,  # number
		# OUTPUT node
		_Sampler_Outputnode_width = 500,  # number
	# TR1
		_Sampler_Tr1_NumberofGate	            = 1,       # Number
		_Sampler_Tr1_ChannelWidth	            = 100,     # Number
		_Sampler_Tr1_ChannelLength	            = 30,       # Number
		_Sampler_Tr1_XVT				        = 'SLVT',    # 'XVT' ex)SLVT/LVT/RVT/HVT
	# TR2
		_Sampler_Tr2_NumberofGate	            = 5,       # Number
		_Sampler_Tr2_ChannelWidth	            = 700,     # Number
		_Sampler_Tr2_ChannelLength	            = 30,       # Number
		_Sampler_Tr2_XVT				        = 'SLVT',    # 'XVT' ex)SLVT/LVT/RVT/HVT
	# TR4
		_Sampler_Tr4_NumberofGate	            = 4,       # Number
		_Sampler_Tr4_ChannelWidth	            = 500,     # Number
		_Sampler_Tr4_ChannelLength	            = 30,       # Number
		_Sampler_Tr4_XVT				        = 'RVT',    # 'XVT' ex)SLVT/LVT/RVT/HVT
	# TR5
		_Sampler_Tr5_NumberofGate	            = 2,       # Number
		_Sampler_Tr5_ChannelWidth	            = 1000,     # Number
		_Sampler_Tr5_ChannelLength	            = 30,       # Number
		_Sampler_Tr5_XVT				        = 'SLVT',    # 'XVT' ex)SLVT/LVT/RVT/HVT
	# TR7
		_Sampler_Tr7_NumberofGate               = 3,  # Number
		_Sampler_Tr7_ChannelWidth	            = 233,     # Number
		_Sampler_Tr7_ChannelLength	            = 30,       # Number
		_Sampler_Tr7_XVT				        = 'SLVT',    # 'XVT' ex)SLVT/LVT/RVT/HVT
	# TR9
		_Sampler_Tr9_NumberofGate               = 3,  # Number
		_Sampler_Tr9_ChannelWidth	            = 500,     # Number
		_Sampler_Tr9_ChannelLength	            = 30,       # Number
		_Sampler_Tr9_XVT				        = 'LVT',    # 'XVT' ex)SLVT/LVT/RVT/HVT
	# TR8
		_Sampler_Tr8_NumberofGate	            = 4,       # Number
		_Sampler_Tr8_ChannelWidth	            = 500,     # Number
		_Sampler_Tr8_ChannelLength	            = 30,       # Number
		_Sampler_Tr8_XVT				        = 'RVT',    # 'XVT' ex)SLVT/LVT/RVT/HVT
	# TR6
		_Sampler_Tr6_NumberofGate	            = 1,       # Number
		_Sampler_Tr6_ChannelWidth	            = 500,     # Number
		_Sampler_Tr6_ChannelLength	            = 30,       # Number
		_Sampler_Tr6_XVT				        = 'RVT',    # 'XVT' ex)SLVT/LVT/RVT/HVT
	# TR11
		_Sampler_Tr11_NumberofGate	            = 20,       # Number
		_Sampler_Tr11_ChannelWidth	            = 500,     # Number
		_Sampler_Tr11_ChannelLength	            = 30,       # Number
		_Sampler_Tr11_XVT				        = 'RVT',    # 'XVT' ex)SLVT/LVT/RVT/HVT
	# Tie4N
		_Sampler_Tie4N_NumberofGate     	    = 5,       # Number
		_Sampler_Tie4N_ChannelWidth	            = 250,     # Number
		_Sampler_Tie4N_ChannelLength	        = 30,       # Number
		_Sampler_Tie4N_XVT				        = 'SLVT',    # 'XVT' ex)SLVT/LVT/RVT/HVT
	# Tie4P
		_Sampler_Tie4P_NumberofGate	            = 5,       # Number
		_Sampler_Tie4P_ChannelWidth	            = 500,     # Number
		_Sampler_Tie4P_ChannelLength	        = 30,       # Number
		_Sampler_Tie4P_XVT				        = 'SLVT',    # 'XVT' ex)SLVT/LVT/RVT/HVT
	# Tie8N
		_Sampler_Tie8N_NumberofGate	            = 4,       # Number
		_Sampler_Tie8N_ChannelWidth	            = 250,     # Number
		_Sampler_Tie8N_ChannelLength	        = 30,       # Number
		_Sampler_Tie8N_XVT				        = 'SLVT',    # 'XVT' ex)SLVT/LVT/RVT/HVT
	# Tie8P
		_Sampler_Tie8P_NumberofGate	            = 4,       # Number
		_Sampler_Tie8P_ChannelWidth	            = 500,     # Number
		_Sampler_Tie8P_ChannelLength	        = 30,       # Number
		_Sampler_Tie8P_XVT				        = 'SLVT',    # 'XVT' ex)SLVT/LVT/RVT/HVT
	# TR12
		_Sampler_Tr12_NumberofGate	            = 4,       # Number
		_Sampler_Tr12_ChannelWidth	            = 1500,     # Number
		_Sampler_Tr12_ChannelLength	            = 30,       # Number
		_Sampler_Tr12_XVT				        = 'RVT',    # 'XVT' ex)SLVT/LVT/RVT/HVT
	# TR3
		_Sampler_Tr3_NumberofGate	            = 2,       # Number
		_Sampler_Tr3_ChannelWidth	            = 100,     # Number
		_Sampler_Tr3_ChannelLength	            = 30,       # Number
		_Sampler_Tr3_XVT				        = 'LVT',    # 'XVT' ex)SLVT/LVT/RVT/HVT
	# TR10
		_Sampler_Tr10_NumberofGate	            = 8,       # Number
		_Sampler_Tr10_ChannelWidth	            = 780,     # Number
		_Sampler_Tr10_ChannelLength	            = 30,       # Number
		_Sampler_Tr10_XVT				        = 'RVT',    # 'XVT' ex)SLVT/LVT/RVT/HVT

	# HDVNCAP
		_Sampler_HDVNCAP_Length = 7000,
		_Sampler_HDVNCAP_LayoutOption = [3,4,5,6], # Writedown [number1, number2, number3, ...]
		_Sampler_HDVNCAP_NumFigPair = 62, #number (ref:75)

		_Sampler_HDVNCAP_Array = 3, #number: 1xnumber
		_Sampler_HDVNCAP_Cbot_Ctop_metalwidth = 1000, #number

	# CLKBGen Inverter
		#Common
		_Sampler_ClkbGenInv_XVT                        = 'SLVT',
		#Nmos
		_Sampler_ClkbGenInv_NMOS_NumberofGate          = 1,        # Number
		_Sampler_ClkbGenInv_NMOS_ChannelWidth          = 100,      # Number
		_Sampler_ClkbGenInv_NMOS_ChannelLength         = 30,       # Number
		#Pmos
		_Sampler_ClkbGenInv_PMOS_NumberofGate          = 1,        # Number
		_Sampler_ClkbGenInv_PMOS_ChannelWidth          = 100,      # Number
		_Sampler_ClkbGenInv_PMOS_ChannelLength         = 30,       # Number
		#Body
		_Sampler_ClkbGenInv_NMOS_Pbody_XvtTop2Pbody    = None,     # Number/None(Minimum)
		_Sampler_ClkbGenInv_PMOS_Nbody_Xvtdown2Nbody   = None,     # Number/None(Minimum)
		#Height
		_Sampler_ClkbGenInv_PMOSXvt2NMOSXvt            = 1800,     # number


#RDAC and Decoder
	#RDAC and Decoder delta X displacement for DRC
	_RDAC_displacement = +1000,
	#RDAC and Decoder Size : Consider "_Decoder_RBit" and "_Unit_Num_EachStag_input" ex) [2, 8] --> 4 : 2*8 = 2**4
	_RDAC_Size = [1,16],
	#ResArray
		#Unit Resistor
		_RDAC_Array_ResWidth	=	5300,
		_RDAC_Array_ResLength	=	1500,

	## Decoder
		## Array
			# _Unit to Unit distance for DRC of routing
			_RDAC_Decoder_Unit2UnitDist=1000,  # number must be 100의 배수
		# Unit
			## Comoon
				# Routing
				_RDAC_Decoder_Unit_Routing_Dist=50,
				# Xvt
				_RDAC_Decoder_Unit_Xvt='SLVT',
				# Dist
				_RDAC_Decoder_Unit_GatetoGateDist = 100,
				# Inputs of Nand,Nor
				_RDAC_Decoder_Unit_Num_EachStag_input = [5], # ex) [2,3,4] 가장 마지막단(TG driving) nand input4, Nor input3, Nand input2, Nor input2 ...
				# Power rail
					# Pbody_Pulldown(NMOS)
					_RDAC_Decoder_Unit_Pbody_XvtTop2Pbody    = None,  # Number/None(Minimum)
					# Nbody_Pullup(PMOS)
					_RDAC_Decoder_Unit_Nbody_Xvtdown2Nbody   = None,  # Number/None(Minimum)
					# PMOS and NMOS Height
					_RDAC_Decoder_Unit_PMOSXvt2NMOSXvt       = 1200,  # number
			# Nand( _Decoder_Unit_Num_EachStag_input에서 1,3,5,7...번째 해당하는 nand 생성)
				# MOSFET
					# Common
					_RDAC_Decoder_Nand_NumberofGate      = [1,2],  # Number
					_RDAC_Decoder_Nand_ChannelLength     = [30,30],  # Number
					# Pulldown(NMOS)
						_RDAC_Decoder_Nand_NMOS_ChannelWidth                 = [350,500],  # Number
					# Pulldown(PMOS)
						_RDAC_Decoder_Nand_PMOS_ChannelWidth                 = [350,480],  # Number
			# Nor( _Decoder_Unit_Num_EachStag_input에서 2,4,6,7...번째 해당하는 nor 생성)
				# MOSFET
					# Common
					_RDAC_Decoder_Nor_NumberofGate=[2, 7],  # Number
					_RDAC_Decoder_Nor_ChannelLength      = [30,30],  # Number
					# Pulldown(NMOS)
						_RDAC_Decoder_Nor_NMOS_ChannelWidth	= [400,800],      # Number
					# Pulldown(PMOS)
						_RDAC_Decoder_Nor_PMOS_ChannelWidth	= [800,1600],      # Number
			# Inv
				#Common
				_RDAC_Decoder_Inv_NumberofGate   = 5,
				_RDAC_Decoder_Inv_ChannelLength  = 30,
				# NMosfet
					_RDAC_Decoder_Inv_NMOS_ChannelWidth	= 400,      # Number
				# PMosfet
					_RDAC_Decoder_Inv_PMOS_ChannelWidth  = 800,      # Number
			# Xgate
				# Common
				_RDAC_Decoder_Xgate_NumberofGate     = 3,
				_RDAC_Decoder_Xgate_ChannelLength    = 30,
				# NMosfet
					_RDAC_Decoder_Xgate_NMOS_ChannelWidth    = 400,      # Number
				# PMosfet
					_RDAC_Decoder_Xgate_PMOS_ChannelWidth    = 800,      # Number


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
	LayoutObj = _R00C13H06L00(_DesignParameter=None, _Name=cellname)
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
	print('{} Hours   {} minutes   {} seconds'.format(h,m,s))

	with open('LayoutObj.pkl', 'wb') as f:
		pickle.dump(LayoutObj, f)

	# end of 'main():' ---------------------------------------------------------------------------------------------
