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


## KJH91 Basic Building Blocks
from KJH91_Projects.Project_ADC.Layoutgen_code.E00_Slicer import Slicer
from KJH91_Projects.Project_ADC.Layoutgen_code.A_Basic_Building_Block import A14_Mosfet_KJH2
from KJH91_Projects.Project_ADC.Layoutgen_code.A_Basic_Building_Block import A02_ViaStack_KJH3

from KJH91_Projects.Project_ADC.Layoutgen_code.L00_SARLogicWtComparator_RCHybrid import L00_SARLogicWtComparator_KJH
from KJH91_Projects.Project_ADC.Layoutgen_code.H02_CDACWtDriver_YJH_RCHybrid import H02_01_CDACWtDriver_Unfolded
from KJH91_Projects.Project_ADC.Layoutgen_code.H02_CDACWtDriver_YJH_RCHybrid import H02_01_CDACWtDriver_Fold1_CC
from KJH91_Projects.Project_ADC.Layoutgen_code.H02_CDACWtDriver_YJH_RCHybrid import H02_01_CDACWtDriver_Fold1_DrvArranged
from KJH91_Projects.Project_ADC.Layoutgen_code.C13_C07C11C12TieCellsRouted_Fixed import C13_01_CtopCbotRouted_YJ_v01_00
from KJH91_Projects.Project_ADC.Layoutgen_code.D00_SARLogic_Inverter_KJH1 import D00_00_Inverter_KJH
from KJH91_Projects.Project_ADC.Layoutgen_code.R00_Combine_P00_Q05 import R00_00_Combine_KJH4

# Update: And 에서 inverter size 기존크기에 4배로
# Upadte: 100p delay
# Update250522: 시간단축

## Define Class
class _R00C13H02L00(StickDiagram_KJH1._StickDiagram_KJH):
	## Input Parameters for Design Calculation: Used when import Sref
	_ParametersForDesignCalculation = dict(
		_NumofRbit =2,

		_NumofCbit=8,
		_CDAC_Folding=None,  # None/True/False
		_Driver_CommonCentroidPlacementIfCDACFolded=False,  # 말 그대로 True이면 CommmonCentroid 배치가 됨.
		_Driver_DecimationIfDriverPlacedInCommonCentroid=True,
		_Driver_DecimationFactor=[2, 0, 0, 0, 0, 0, 0],  # [MSB, MSB-1 ... MSB-x]: 단 X<MSB  # 위 옵션 True시 작동; MSB부터 벡터로 작성; [3,2,2] 시 MSB0 -> 3:1, MSB1 -> 2:1, MSB2 -> 2:1, ... 1은 불가
		_SpaceBtwBootSWPosNeg=None,

		_Test_distance=330,
		_Routing_width=50,
		_Routing_distance=80,

		_SARLogic_YWidthOfCLKSrc=100,
		_SARLogic_SpaceBtwCLKSrcAndCLKSamp=100,
		_SARLogic_YWidthOfCLKSamp=100,

		_SARLogic_YWidthOfCompOut=100,
		_SARLogic_SpaceBtwCompOutAndCLKDout=100,
		_SARLogic_YWidthOfCLKDout=100,

		## DFF Common
		_SARLogic_DFF_Pbody_NumCont=2,  # number
		_SARLogic_DFF_Nbody_NumCont=2,  # number
		_SARLogic_DFF_PMOSXvt2NMOSXvt=1150,  # number
		_SARLogic_DFF_XvtTop2Pbody=None,  # number/None(Minimum)
		_SARLogic_DFF_Xvtdown2Nbody=None,  # number/None(Minimum)

		## Master Xgate1
		## Xgate common

		## Xgate NMOS
		_SARLogic_Mst_Xgate1_NMOS_NumberofGate=1,  # 1
		_SARLogic_Mst_Xgate1_NMOS_ChannelWidth=200,  # 100
		_SARLogic_Mst_Xgate1_NMOS_ChannelLength=30,
		_SARLogic_Mst_Xgate1_NMOS_XVT='HVT',
		_SARLogic_Mst_Xgate1_NMOS_POGate_Comb_length=100,

		## Xgate PMOS
		_SARLogic_Mst_Xgate1_PMOS_NumberofGate=1,  # 1
		_SARLogic_Mst_Xgate1_PMOS_ChannelWidth=400,  # 200
		_SARLogic_Mst_Xgate1_PMOS_ChannelLength=30,
		_SARLogic_Mst_Xgate1_PMOS_XVT='HVT',
		_SARLogic_Mst_Xgate1_PMOS_POGate_Comb_length=100,

		## Master Xgate2
		## Xgate common

		## Xgate NMOS
		_SARLogic_Mst_Xgate2_NMOS_NumberofGate=1,
		_SARLogic_Mst_Xgate2_NMOS_ChannelWidth=200,
		_SARLogic_Mst_Xgate2_NMOS_ChannelLength=30,
		_SARLogic_Mst_Xgate2_NMOS_XVT='SLVT',
		_SARLogic_Mst_Xgate2_NMOS_POGate_Comb_length=100,

		## Xgate PMOS
		_SARLogic_Mst_Xgate2_PMOS_NumberofGate=2,  # 2
		_SARLogic_Mst_Xgate2_PMOS_ChannelWidth=200,
		_SARLogic_Mst_Xgate2_PMOS_ChannelLength=30,
		_SARLogic_Mst_Xgate2_PMOS_XVT='SLVT',
		_SARLogic_Mst_Xgate2_PMOS_POGate_Comb_length=100,

		## Master Nor1
		## Nor1 common

		## NMOS
		## NMOS common
		_SARLogic_Mst_Nor1_NMOS_XVT='HVT',

		## NMOSA
		_SARLogic_Mst_Nor1_NMOSA_NumberofGate=2,
		_SARLogic_Mst_Nor1_NMOSA_ChannelWidth=200,
		_SARLogic_Mst_Nor1_NMOSA_ChannelLength=30,
		_SARLogic_Mst_Nor1_NMOSA_POGate_Comb_length=100,

		## NMOSB
		_SARLogic_Mst_Nor1_NMOSB_NumberofGate=2,
		_SARLogic_Mst_Nor1_NMOSB_ChannelWidth=200,
		_SARLogic_Mst_Nor1_NMOSB_ChannelLength=30,
		_SARLogic_Mst_Nor1_NMOSB_POGate_Comb_length=100,

		## PMOS
		## PMOS common
		_SARLogic_Mst_Nor1_PMOS_XVT='HVT',

		## PMOSA
		_SARLogic_Mst_Nor1_PMOSA_NumberofGate=4,
		_SARLogic_Mst_Nor1_PMOSA_ChannelWidth=400,
		_SARLogic_Mst_Nor1_PMOSA_ChannelLength=30,
		_SARLogic_Mst_Nor1_PMOSA_POGate_Comb_length=100,

		## PMOSB
		_SARLogic_Mst_Nor1_PMOSB_NumberofGate=4,
		_SARLogic_Mst_Nor1_PMOSB_ChannelWidth=400,
		_SARLogic_Mst_Nor1_PMOSB_ChannelLength=30,
		_SARLogic_Mst_Nor1_PMOSB_POGate_Comb_length=100,

		## Master Nor2
		## Nor2 common

		## NMOS
		## NMOS common
		_SARLogic_Mst_Nor2_NMOS_XVT='HVT',

		## NMOSA
		_SARLogic_Mst_Nor2_NMOSA_NumberofGate=2,
		_SARLogic_Mst_Nor2_NMOSA_ChannelWidth=200,
		_SARLogic_Mst_Nor2_NMOSA_ChannelLength=30,
		_SARLogic_Mst_Nor2_NMOSA_POGate_Comb_length=100,

		## NMOSB
		_SARLogic_Mst_Nor2_NMOSB_NumberofGate=2,
		_SARLogic_Mst_Nor2_NMOSB_ChannelWidth=200,
		_SARLogic_Mst_Nor2_NMOSB_ChannelLength=30,
		_SARLogic_Mst_Nor2_NMOSB_POGate_Comb_length=100,

		## PMOS
		## PMOS common
		_SARLogic_Mst_Nor2_PMOS_XVT='HVT',

		## PMOSA
		_SARLogic_Mst_Nor2_PMOSA_NumberofGate=4,
		_SARLogic_Mst_Nor2_PMOSA_ChannelWidth=400,
		_SARLogic_Mst_Nor2_PMOSA_ChannelLength=30,
		_SARLogic_Mst_Nor2_PMOSA_POGate_Comb_length=100,

		## PMOSB
		_SARLogic_Mst_Nor2_PMOSB_NumberofGate=4,
		_SARLogic_Mst_Nor2_PMOSB_ChannelWidth=400,
		_SARLogic_Mst_Nor2_PMOSB_ChannelLength=30,
		_SARLogic_Mst_Nor2_PMOSB_POGate_Comb_length=100,

		## Master Inv1 : Set pre-driver
		## Inv1 common

		## Inv1 NMOS
		_SARLogic_Mst_Inv1_NMOS_NumberofGate=1,
		_SARLogic_Mst_Inv1_NMOS_ChannelWidth=200,
		_SARLogic_Mst_Inv1_NMOS_ChannelLength=30,
		_SARLogic_Mst_Inv1_NMOS_XVT='SLVT',
		_SARLogic_Mst_Inv1_NMOS_POGate_Comb_length=100,

		## Inv1 PMOS
		_SARLogic_Mst_Inv1_PMOS_NumberofGate=1,
		_SARLogic_Mst_Inv1_PMOS_ChannelWidth=400,
		_SARLogic_Mst_Inv1_PMOS_ChannelLength=30,
		_SARLogic_Mst_Inv1_PMOS_XVT='SLVT',
		_SARLogic_Mst_Inv1_PMOS_POGate_Comb_length=100,

		## Master Inv2 : Set driver
		## Inv2 common

		## Inv2 NMOS
		_SARLogic_Mst_Inv2_NMOS_NumberofGate=1,
		_SARLogic_Mst_Inv2_NMOS_ChannelWidth=200,
		_SARLogic_Mst_Inv2_NMOS_ChannelLength=30,
		_SARLogic_Mst_Inv2_NMOS_XVT='SLVT',
		_SARLogic_Mst_Inv2_NMOS_POGate_Comb_length=100,

		## Inv2 PMOS
		_SARLogic_Mst_Inv2_PMOS_NumberofGate=1,
		_SARLogic_Mst_Inv2_PMOS_ChannelWidth=400,
		_SARLogic_Mst_Inv2_PMOS_ChannelLength=30,
		_SARLogic_Mst_Inv2_PMOS_XVT='SLVT',
		_SARLogic_Mst_Inv2_PMOS_POGate_Comb_length=100,

		## Master Inv3 : Clock driver
		## Inv3 common

		## Inv3 NMOS
		_SARLogic_Mst_Inv3_NMOS_NumberofGate=1,
		_SARLogic_Mst_Inv3_NMOS_ChannelWidth=200,
		_SARLogic_Mst_Inv3_NMOS_ChannelLength=30,
		_SARLogic_Mst_Inv3_NMOS_XVT='SLVT',
		_SARLogic_Mst_Inv3_NMOS_POGate_Comb_length=100,

		## Inv3 PMOS
		_SARLogic_Mst_Inv3_PMOS_NumberofGate=1,
		_SARLogic_Mst_Inv3_PMOS_ChannelWidth=400,
		_SARLogic_Mst_Inv3_PMOS_ChannelLength=30,
		_SARLogic_Mst_Inv3_PMOS_XVT='SLVT',
		_SARLogic_Mst_Inv3_PMOS_POGate_Comb_length=100,

		## Slave Xgate1
		## Xgate common

		## Xgate NMOS
		_SARLogic_Slv_Xgate1_NMOS_NumberofGate=1,
		_SARLogic_Slv_Xgate1_NMOS_ChannelWidth=200,
		_SARLogic_Slv_Xgate1_NMOS_ChannelLength=30,
		_SARLogic_Slv_Xgate1_NMOS_XVT='HVT',
		_SARLogic_Slv_Xgate1_NMOS_POGate_Comb_length=100,

		## Xgate NMOS
		_SARLogic_Slv_Xgate1_PMOS_NumberofGate=1,
		_SARLogic_Slv_Xgate1_PMOS_ChannelWidth=400,
		_SARLogic_Slv_Xgate1_PMOS_ChannelLength=30,
		_SARLogic_Slv_Xgate1_PMOS_XVT='HVT',
		_SARLogic_Slv_Xgate1_PMOS_POGate_Comb_length=100,

		## Slave Xgate2
		## Xgate common

		## Xgate NMOS
		_SARLogic_Slv_Xgate2_NMOS_NumberofGate=1,
		_SARLogic_Slv_Xgate2_NMOS_ChannelWidth=200,
		_SARLogic_Slv_Xgate2_NMOS_ChannelLength=30,
		_SARLogic_Slv_Xgate2_NMOS_XVT='SLVT',
		_SARLogic_Slv_Xgate2_NMOS_POGate_Comb_length=100,

		## Xgate NMOS
		_SARLogic_Slv_Xgate2_PMOS_NumberofGate=2,
		_SARLogic_Slv_Xgate2_PMOS_ChannelWidth=200,
		_SARLogic_Slv_Xgate2_PMOS_ChannelLength=30,
		_SARLogic_Slv_Xgate2_PMOS_XVT='SLVT',
		_SARLogic_Slv_Xgate2_PMOS_POGate_Comb_length=100,

		## Slave Nor1
		## Nor1 common

		## NMOS
		## NMOS common
		_SARLogic_Slv_Nor1_NMOS_XVT='HVT',

		## NMOSA
		_SARLogic_Slv_Nor1_NMOSA_NumberofGate=2,
		_SARLogic_Slv_Nor1_NMOSA_ChannelWidth=200,
		_SARLogic_Slv_Nor1_NMOSA_ChannelLength=30,
		_SARLogic_Slv_Nor1_NMOSA_POGate_Comb_length=100,

		## NMOSB
		_SARLogic_Slv_Nor1_NMOSB_NumberofGate=2,
		_SARLogic_Slv_Nor1_NMOSB_ChannelWidth=200,
		_SARLogic_Slv_Nor1_NMOSB_ChannelLength=30,
		_SARLogic_Slv_Nor1_NMOSB_POGate_Comb_length=100,

		## PMOS
		## PMOS common
		_SARLogic_Slv_Nor1_PMOS_XVT='HVT',

		## PMOSA
		_SARLogic_Slv_Nor1_PMOSA_NumberofGate=4,
		_SARLogic_Slv_Nor1_PMOSA_ChannelWidth=400,
		_SARLogic_Slv_Nor1_PMOSA_ChannelLength=30,
		_SARLogic_Slv_Nor1_PMOSA_POGate_Comb_length=100,

		## PMOSB
		_SARLogic_Slv_Nor1_PMOSB_NumberofGate=4,
		_SARLogic_Slv_Nor1_PMOSB_ChannelWidth=400,
		_SARLogic_Slv_Nor1_PMOSB_ChannelLength=30,
		_SARLogic_Slv_Nor1_PMOSB_POGate_Comb_length=100,

		## Slave Nor2
		## Nor2 common

		## NMOS
		## NMOS common
		_SARLogic_Slv_Nor2_NMOS_XVT='HVT',

		## NMOSA
		_SARLogic_Slv_Nor2_NMOSA_NumberofGate=2,
		_SARLogic_Slv_Nor2_NMOSA_ChannelWidth=200,
		_SARLogic_Slv_Nor2_NMOSA_ChannelLength=30,
		_SARLogic_Slv_Nor2_NMOSA_POGate_Comb_length=100,

		## NMOSB
		_SARLogic_Slv_Nor2_NMOSB_NumberofGate=2,
		_SARLogic_Slv_Nor2_NMOSB_ChannelWidth=200,
		_SARLogic_Slv_Nor2_NMOSB_ChannelLength=30,
		_SARLogic_Slv_Nor2_NMOSB_POGate_Comb_length=100,

		## PMOS
		## PMOS common
		_SARLogic_Slv_Nor2_PMOS_XVT='HVT',

		## PMOSA
		_SARLogic_Slv_Nor2_PMOSA_NumberofGate=4,
		_SARLogic_Slv_Nor2_PMOSA_ChannelWidth=400,
		_SARLogic_Slv_Nor2_PMOSA_ChannelLength=30,
		_SARLogic_Slv_Nor2_PMOSA_POGate_Comb_length=100,

		## PMOSB
		_SARLogic_Slv_Nor2_PMOSB_NumberofGate=4,
		_SARLogic_Slv_Nor2_PMOSB_ChannelWidth=400,
		_SARLogic_Slv_Nor2_PMOSB_ChannelLength=30,
		_SARLogic_Slv_Nor2_PMOSB_POGate_Comb_length=100,

		## Slave Inv1 : ReSet pre-driver
		## Inv1 common

		## Inv1 NMOS
		_SARLogic_Slv_Inv1_NMOS_NumberofGate=1,
		_SARLogic_Slv_Inv1_NMOS_ChannelWidth=200,
		_SARLogic_Slv_Inv1_NMOS_ChannelLength=30,
		_SARLogic_Slv_Inv1_NMOS_XVT='SLVT',
		_SARLogic_Slv_Inv1_NMOS_POGate_Comb_length=100,

		## Inv1 PMOS
		_SARLogic_Slv_Inv1_PMOS_NumberofGate=1,
		_SARLogic_Slv_Inv1_PMOS_ChannelWidth=400,
		_SARLogic_Slv_Inv1_PMOS_ChannelLength=30,
		_SARLogic_Slv_Inv1_PMOS_XVT='SLVT',
		_SARLogic_Slv_Inv1_PMOS_POGate_Comb_length=100,

		## Slave Inv2 : ReSet driver
		## Inv2 common

		## Inv2 NMOS
		_SARLogic_Slv_Inv2_NMOS_NumberofGate=1,
		_SARLogic_Slv_Inv2_NMOS_ChannelWidth=300,
		_SARLogic_Slv_Inv2_NMOS_ChannelLength=30,
		_SARLogic_Slv_Inv2_NMOS_XVT='SLVT',
		_SARLogic_Slv_Inv2_NMOS_POGate_Comb_length=100,

		## Inv2 PMOS
		_SARLogic_Slv_Inv2_PMOS_NumberofGate=1,
		_SARLogic_Slv_Inv2_PMOS_ChannelWidth=400,
		_SARLogic_Slv_Inv2_PMOS_ChannelLength=30,
		_SARLogic_Slv_Inv2_PMOS_XVT='SLVT',
		_SARLogic_Slv_Inv2_PMOS_POGate_Comb_length=100,

		## Slave Inv3 : Qb driver
		## Inv3 common

		## Inv3 NMOS
		_SARLogic_Slv_Inv3_NMOS_NumberofGate=5,  # 1
		_SARLogic_Slv_Inv3_NMOS_ChannelWidth=200,
		_SARLogic_Slv_Inv3_NMOS_ChannelLength=30,
		_SARLogic_Slv_Inv3_NMOS_XVT='SLVT',
		_SARLogic_Slv_Inv3_NMOS_POGate_Comb_length=100,

		## Inv3 PMOS
		_SARLogic_Slv_Inv3_PMOS_NumberofGate=5,  # 1
		_SARLogic_Slv_Inv3_PMOS_ChannelWidth=400,
		_SARLogic_Slv_Inv3_PMOS_ChannelLength=30,
		_SARLogic_Slv_Inv3_PMOS_XVT='SLVT',
		_SARLogic_Slv_Inv3_PMOS_POGate_Comb_length=100,

		# Top Clock  Tree Size
		_SARLogic_CLKBufTreeTop_NumOfStage=4,
		_SARLogic_CLKBufTreeTop_CLKSampBuf_SizeByStage=None,
		_SARLogic_CLKBufTreeTop_CLKSrcBuf_SizeByStage=None,
		# 스테이지에 따른 버퍼 사이즈(UnitBuffer의 배수로 각 스테이지의 크기가 결정 됨.)
		_SARLogic_CLKBufTreeTop_XOffSet=0,  # (8Bit DRC check:-79)

		## Top CLK Buffer Size
		_SARLogic_CLKBufTreeTop_Inv_NMOS_ChannelWidth=400,  # Number
		_SARLogic_CLKBufTreeTop_Inv_NMOS_ChannelLength=30,  # Number
		_SARLogic_CLKBufTreeTop_Inv_NMOS_NumberofGate=1,  # Number
		_SARLogic_CLKBufTreeTop_Inv_NMOS_XVT='SLVT',  # 'XVT' ex)SLVT/LVT/RVT/HVT
		_SARLogic_CLKBufTreeTop_Inv_NMOS_POGate_Comb_length=100,  # None/Number

		_SARLogic_CLKBufTreeTop_Inv_PMOS_ChannelWidth=800,  # Number
		_SARLogic_CLKBufTreeTop_Inv_PMOS_ChannelLength=30,  # Number
		_SARLogic_CLKBufTreeTop_Inv_PMOS_NumberofGate=1,  # Number
		_SARLogic_CLKBufTreeTop_Inv_PMOS_XVT='SLVT',  # 'XVT' ex)SLVT/LVT/RVT/HVT
		_SARLogic_CLKBufTreeTop_Inv_PMOS_POGate_Comb_length=100,  # None/Number

		# Top CLK BufferPowerRail Size
		_SARLogic_CLKBufTreeTop_NMOS_Pbody_NumCont=2,
		_SARLogic_CLKBufTreeTop_NMOS_Pbody_XvtTop2Pbody=None,
		_SARLogic_CLKBufTreeTop_PMOS_Nbody_NumCont=2,
		_SARLogic_CLKBufTreeTop_PMOS_Nbody_Xvtdown2Nbody=None,
		_SARLogic_CLKBufTreeTop_PMOSXvt2NMOSXvt=700,

		# Bottom Clock  Tree Size
		_SARLogic_CLKBufTreeBot_NumOfStage=4,
		_SARLogic_CLKBufTreeBot_CompOutBuf_SizeByStage=None,
		_SARLogic_CLKBufTreeBot_CLKDoutBuf_SizeByStage=None,
		# 스테이지에 따른 버퍼 사이즈(UnitBuffer의 배수로 각 스테이지의 크기가 결정 됨.)
		_SARLogic_CLKBufTreeBot_XOffSet=0,

		## Bottom CLK Buffer Size
		_SARLogic_CLKBufTreeBot_Inv_NMOS_ChannelWidth=400,  # Number
		_SARLogic_CLKBufTreeBot_Inv_NMOS_ChannelLength=30,  # Number
		_SARLogic_CLKBufTreeBot_Inv_NMOS_NumberofGate=1,  # Number
		_SARLogic_CLKBufTreeBot_Inv_NMOS_XVT='SLVT',  # 'XVT' ex)SLVT/LVT/RVT/HVT
		_SARLogic_CLKBufTreeBot_Inv_NMOS_POGate_Comb_length=100,  # None/Number

		_SARLogic_CLKBufTreeBot_Inv_PMOS_ChannelWidth=800,  # Number
		_SARLogic_CLKBufTreeBot_Inv_PMOS_ChannelLength=30,  # Number
		_SARLogic_CLKBufTreeBot_Inv_PMOS_NumberofGate=1,  # Number
		_SARLogic_CLKBufTreeBot_Inv_PMOS_XVT='SLVT',  # 'XVT' ex)SLVT/LVT/RVT/HVT
		_SARLogic_CLKBufTreeBot_Inv_PMOS_POGate_Comb_length=100,  # None/Number

		# Bottom CLK Buffer PowerRail Size
		_SARLogic_CLKBufTreeBot_NMOS_Pbody_NumCont=2,
		_SARLogic_CLKBufTreeBot_NMOS_Pbody_XvtTop2Pbody=None,
		_SARLogic_CLKBufTreeBot_PMOS_Nbody_NumCont=2,
		_SARLogic_CLKBufTreeBot_PMOS_Nbody_Xvtdown2Nbody=None,
		_SARLogic_CLKBufTreeBot_PMOSXvt2NMOSXvt=700,

		#### CDAC Pre-Driver Sizing
		## InvChain Common
		_CDACPreDriver_Pbody_NumCont=2,  # number
		_CDACPreDriver_Nbody_NumCont=2,  # number
		_CDACPreDriver_PMOSXvt2NMOSXvt=500,  # number
		_CDACPreDriver_XvtTop2Pbody=None,  # number/None(Minimum)
		_CDACPreDriver_Xvtdown2Nbody=None,  # number/None(Minimum)

		## Inverter Chain
		## Inv1 common
		_CDACPreDriver_NumberofGate=[2, 4, 6],  # Vector
		_CDACPreDriver_ChannelLength=30,  # Scalar
		_CDACPreDriver_XVT='SLVT',  # 'SLVT'

		## Inv1 NMOS
		_CDACPreDriver_Inv_NMOS_ChannelWidth=200,  # Scalar
		_CDACPreDriver_Inv_NMOS_POGate_Comb_length=100,  # Scalar

		## Inv1 PMOS
		_CDACPreDriver_Inv_PMOS_ChannelWidth=400,  # Scalar
		_CDACPreDriver_Inv_PMOS_POGate_Comb_length=100,  # Scalar

		## CLKDout(OutSamp) Inverter & AND Common Option
		_CLKDout_XVT_Common='SLVT',

		## CLKDout(OutSamp) Inverter Size
		_CLKDout_Inv_NMOS_ChannelWidth=400,  # Number
		_CLKDout_Inv_NMOS_ChannelLength=30,  # Number
		_CLKDout_Inv_NMOS_NumberofGate=1,  # Number
		_CLKDout_Inv_NMOS_POGate_Comb_length=100,  # None/Number

		_CLKDout_Inv_PMOS_ChannelWidth=800,  # Number
		_CLKDout_Inv_PMOS_ChannelLength=30,  # Number
		_CLKDout_Inv_PMOS_NumberofGate=1,  # Number
		_CLKDout_Inv_PMOS_POGate_Comb_length=100,  # None/Number

		## CLKDout(OutSamp) AND Size
		_CLKDout_AND_NAND_NMOS_ChannelWidth=400,
		_CLKDout_AND_NAND_NMOS_ChannelLength=30,
		_CLKDout_AND_NAND_NMOS_NumberofGate=2,

		_CLKDout_AND_NAND_PMOS_ChannelWidth=800,
		_CLKDout_AND_NAND_PMOS_ChannelLength=30,
		_CLKDout_AND_NAND_PMOS_NumberofGate=1,

		_CLKDout_AND_Inv_NMOS_ChannelWidth=400,
		_CLKDout_AND_Inv_NMOS_ChannelLength=30,
		_CLKDout_AND_Inv_NMOS_NumberofGate=1,
		_CLKDout_AND_Inv_NMOS_POGate_Comb_length=100,

		_CLKDout_AND_Inv_PMOS_ChannelWidth=800,
		_CLKDout_AND_Inv_PMOS_ChannelLength=30,
		_CLKDout_AND_Inv_PMOS_NumberofGate=1,
		_CLKDout_AND_Inv_PMOS_POGate_Comb_length=100,

		## StrongArm Latch
		_Comp_SALatch_CLKinputPMOSFinger1=None,  # 6
		_Comp_SALatch_CLKinputPMOSFinger2=None,  # 3
		_Comp_SALatch_PMOSFinger=None,  # 3
		_Comp_SALatch_PMOSChannelWidth=None,  # 500
		_Comp_SALatch_DATAinputNMOSFinger=None,  # 12
		_Comp_SALatch_NMOSFinger=None,  # 2
		_Comp_SALatch_CLKinputNMOSFinger=None,  # 8
		_Comp_SALatch_NMOSChannelWidth=None,  # 500
		_Comp_SALatch_CLKinputNMOSChannelWidth=None,  # 800
		_Comp_SALatch_ChannelLength=None,  # 30
		_Comp_SALatch_Dummy=True,
		_Comp_SALatch_XVT=None,
		_Comp_SALatch_GuardringWidth=None,
		_Comp_SALatch_Guardring=True,
		_Comp_SALatch_SlicerGuardringWidth=None,
		_Comp_SALatch_SlicerGuardring=None,
		_Comp_SALatch_NumSupplyCOY=None,
		_Comp_SALatch_NumSupplyCOX=None,
		_Comp_SALatch_SupplyMet1XWidth=None,
		_Comp_SALatch_SupplyMet1YWidth=None,
		_Comp_SALatch_VDD2VSSHeight=None,
		_Comp_SALatch_NumVIAPoly2Met1COX=None,
		_Comp_SALatch_NumVIAPoly2Met1COY=None,
		_Comp_SALatch_NumVIAMet12COX=None,
		_Comp_SALatch_NumVIAMet12COY=None,
		_Comp_SALatch_PowerLine=False,

		## StrongARMLatch Output Buffer Sizing
		# Inverter1
		_Comp_SAOutBuf_Inv1_NMOS_ChannelWidth=None,  # Number
		_Comp_SAOutBuf_Inv1_NMOS_ChannelLength=None,  # Number
		_Comp_SAOutBuf_Inv1_NMOS_NumberofGate=None,  # Number
		_Comp_SAOutBuf_Inv1_NMOS_XVT=None,  # 'XVT' ex)SLVT/LVT/RVT/HVT
		_Comp_SAOutBuf_Inv1_NMOS_POGate_Comb_length=None,  # None/Number

		_Comp_SAOutBuf_Inv1_PMOS_ChannelWidth=None,  # Number
		_Comp_SAOutBuf_Inv1_PMOS_ChannelLength=None,  # Number
		_Comp_SAOutBuf_Inv1_PMOS_NumberofGate=None,  # Number
		_Comp_SAOutBuf_Inv1_PMOS_XVT=None,  # 'XVT' ex)SLVT/LVT/RVT/HVT
		_Comp_SAOutBuf_Inv1_PMOS_POGate_Comb_length=None,  # None/Number

		# Inverter2
		_Comp_SAOutBuf_Inv2_NMOS_ChannelWidth=None,  # Number
		_Comp_SAOutBuf_Inv2_NMOS_ChannelLength=None,  # Number
		_Comp_SAOutBuf_Inv2_NMOS_NumberofGate=None,  # Number
		_Comp_SAOutBuf_Inv2_NMOS_XVT=None,  # 'XVT' ex)SLVT/LVT/RVT/HVT
		_Comp_SAOutBuf_Inv2_NMOS_POGate_Comb_length=None,  # None/Number

		_Comp_SAOutBuf_Inv2_PMOS_ChannelWidth=None,  # Number
		_Comp_SAOutBuf_Inv2_PMOS_ChannelLength=None,  # Number
		_Comp_SAOutBuf_Inv2_PMOS_NumberofGate=None,  # Number
		_Comp_SAOutBuf_Inv2_PMOS_XVT=None,  # 'XVT' ex)SLVT/LVT/RVT/HVT
		_Comp_SAOutBuf_Inv2_PMOS_POGate_Comb_length=None,  # None/Number

		## SR Latch Sizing
		_Comp_SRLatch_NAND_NMOS_ChannelWidth=None,  # Number
		_Comp_SRLatch_NAND_NMOS_ChannelLength=None,  # Number
		_Comp_SRLatch_NAND_NMOS_NumberofGate=None,  # Number
		_Comp_SRLatch_NAND_NMOS_XVT=None,  # 'XVT' ex)SLVT/LVT/RVT/HVT
		_Comp_SRLatch_NAND_NMOS_POGate_Comb_length=None,  # None/Number

		_Comp_SRLatch_NAND_PMOS_ChannelWidth=None,  # Number
		_Comp_SRLatch_NAND_PMOS_ChannelLength=None,  # Number
		_Comp_SRLatch_NAND_PMOS_NumberofGate=None,  # Number
		_Comp_SRLatch_NAND_PMOS_XVT=None,  # 'XVT' ex)SLVT/LVT/RVT/HVT
		_Comp_SRLatch_NAND_PMOS_POGate_Comb_length=None,  # None/Number

		# CLK Input Logic Gates
		_Comp_CLKSamp_Inv_NMOS_ChannelWidth=None,
		_Comp_CLKSamp_Inv_NMOS_ChannelLength=None,
		_Comp_CLKSamp_Inv_NMOS_NumberofGate=None,
		_Comp_CLKSamp_Inv_NMOS_XVT=None,
		_Comp_CLKSamp_Inv_NMOS_POGate_Comb_length=None,

		_Comp_CLKSamp_Inv_PMOS_ChannelWidth=None,
		_Comp_CLKSamp_Inv_PMOS_ChannelLength=None,
		_Comp_CLKSamp_Inv_PMOS_NumberofGate=None,
		_Comp_CLKSamp_Inv_PMOS_XVT=None,
		_Comp_CLKSamp_Inv_PMOS_POGate_Comb_length=None,

		_Comp_CLKSrc_Inv_NMOS_ChannelWidth=None,
		_Comp_CLKSrc_Inv_NMOS_ChannelLength=None,
		_Comp_CLKSrc_Inv_NMOS_NumberofGate=None,
		_Comp_CLKSrc_Inv_NMOS_XVT=None,
		_Comp_CLKSrc_Inv_NMOS_POGate_Comb_length=None,

		_Comp_CLKSrc_Inv_PMOS_ChannelWidth=None,
		_Comp_CLKSrc_Inv_PMOS_ChannelLength=None,
		_Comp_CLKSrc_Inv_PMOS_NumberofGate=None,
		_Comp_CLKSrc_Inv_PMOS_XVT=None,
		_Comp_CLKSrc_Inv_PMOS_POGate_Comb_length=None,

		## CLKSrc & CLKSample AND Gate
		_Comp_AND_NAND_NMOS_ChannelWidth=None,
		_Comp_AND_NAND_NMOS_ChannelLength=None,
		_Comp_AND_NAND_NMOS_NumberofGate=None,
		_Comp_AND_NAND_NMOS_XVT=None,

		_Comp_AND_NAND_PMOS_ChannelWidth=None,
		_Comp_AND_NAND_PMOS_ChannelLength=None,
		_Comp_AND_NAND_PMOS_NumberofGate=None,
		_Comp_AND_NAND_PMOS_XVT=None,

		_Comp_AND_Inv_NMOS_ChannelWidth=None,
		_Comp_AND_Inv_NMOS_ChannelLength=None,
		_Comp_AND_Inv_NMOS_NumberofGate=None,
		_Comp_AND_Inv_NMOS_XVT=None,
		_Comp_AND_Inv_NMOS_POGate_Comb_length=None,

		_Comp_AND_Inv_PMOS_ChannelWidth=None,
		_Comp_AND_Inv_PMOS_ChannelLength=None,
		_Comp_AND_Inv_PMOS_NumberofGate=None,
		_Comp_AND_Inv_PMOS_XVT=None,
		_Comp_AND_Inv_PMOS_POGate_Comb_length=None,

		## CLK Buffer
		# Inverter1
		_Comp_CLKBuf_Inv1_NMOS_ChannelWidth=None,  # Number
		_Comp_CLKBuf_Inv1_NMOS_ChannelLength=None,  # Number
		_Comp_CLKBuf_Inv1_NMOS_NumberofGate=None,  # Number
		_Comp_CLKBuf_Inv1_NMOS_XVT=None,  # 'XVT' ex)SLVT/LVT/RVT/HVT
		_Comp_CLKBuf_Inv1_NMOS_POGate_Comb_length=None,  # None/Number

		_Comp_CLKBuf_Inv1_PMOS_ChannelWidth=None,  # Number
		_Comp_CLKBuf_Inv1_PMOS_ChannelLength=None,  # Number
		_Comp_CLKBuf_Inv1_PMOS_NumberofGate=None,  # Number
		_Comp_CLKBuf_Inv1_PMOS_XVT=None,  # 'XVT' ex)SLVT/LVT/RVT/HVT
		_Comp_CLKBuf_Inv1_PMOS_POGate_Comb_length=None,  # None/Number

		# Inverter2
		_Comp_CLKBuf_Inv2_NMOS_ChannelWidth=None,  # Number
		_Comp_CLKBuf_Inv2_NMOS_ChannelLength=None,  # Number
		_Comp_CLKBuf_Inv2_NMOS_NumberofGate=None,  # Number
		_Comp_CLKBuf_Inv2_NMOS_XVT=None,  # 'XVT' ex)SLVT/LVT/RVT/HVT
		_Comp_CLKBuf_Inv2_NMOS_POGate_Comb_length=None,  # None/Number

		_Comp_CLKBuf_Inv2_PMOS_ChannelWidth=None,  # Number
		_Comp_CLKBuf_Inv2_PMOS_ChannelLength=None,  # Number
		_Comp_CLKBuf_Inv2_PMOS_NumberofGate=None,  # Number
		_Comp_CLKBuf_Inv2_PMOS_XVT=None,  # 'XVT' ex)SLVT/LVT/RVT/HVT
		_Comp_CLKBuf_Inv2_PMOS_POGate_Comb_length=None,  # None/Number

		# PowerRail Placement
		_Comp_BufSR_NMOS_Pbody_NumCont=None,
		_Comp_BufSR_NMOS_Pbody_XvtTop2Pbody=None,
		_Comp_BufSR_PMOS_Nbody_NumCont=None,
		_Comp_BufSR_PMOS_Nbody_Xvtdown2Nbody=None,
		_Comp_BufSR_PMOSXvt2NMOSXvt=None,

		_Comp_CLKInLogic_NMOS_Pbody_Xvtdown2Pbody=None,
		_Comp_CLKInLogic_PMOS_Nbody_NumCont=None,
		_Comp_CLKInLogic_PMOS_Nbody_Xvtdown2Nbody=None,
		_Comp_CLKInLogic_PMOSXvt2NMOSXvt=None,

		# Additional Buffer Between CLK_Sample Input of Comparator And Output of Tree Buffer
		## InvChain Common
		_Buf_CLKSamp_Pbody_NumCont=2,  # number
		_Buf_CLKSamp_Nbody_NumCont=2,  # number
		_Buf_CLKSamp_PMOSXvt2NMOSXvt=500,  # number
		_Buf_CLKSamp_XvtTop2Pbody=None,  # number/None(Minimum)
		_Buf_CLKSamp_Xvtdown2Nbody=None,  # number/None(Minimum)

		## Inverter Chain
		## Inv1 common
		_Buf_CLKSamp_NumberofGate=[2, 4, 6],  # Vector
		_Buf_CLKSamp_ChannelLength=30,  # Scalar
		_Buf_CLKSamp_XVT='SLVT',  # 'SLVT'

		## Inv1 NMOS
		_Buf_CLKSamp_Inv_NMOS_ChannelWidth=200,  # Scalar
		_Buf_CLKSamp_Inv_NMOS_POGate_Comb_length=100,  # Scalar

		## Inv1 PMOS
		_Buf_CLKSamp_Inv_PMOS_ChannelWidth=400,  # Scalar
		_Buf_CLKSamp_Inv_PMOS_POGate_Comb_length=100,  # Scalar

		# Additional Buffer Between CLK_Source Input of Comparator And Output of Tree Buffer
		## InvChain Common
		_Buf_CLKSrc_Pbody_NumCont=2,  # number
		_Buf_CLKSrc_Nbody_NumCont=2,  # number
		_Buf_CLKSrc_PMOSXvt2NMOSXvt=500,  # number
		_Buf_CLKSrc_XvtTop2Pbody=None,  # number/None(Minimum)
		_Buf_CLKSrc_Xvtdown2Nbody=None,  # number/None(Minimum)

		## Inverter Chain
		## Inv1 common
		_Buf_CLKSrc_NumberofGate=[2, 4, 6],  # Vector
		_Buf_CLKSrc_ChannelLength=30,  # Scalar
		_Buf_CLKSrc_XVT='SLVT',  # 'SLVT'

		## Inv1 NMOS
		_Buf_CLKSrc_Inv_NMOS_ChannelWidth=200,  # Scalar
		_Buf_CLKSrc_Inv_NMOS_POGate_Comb_length=100,  # Scalar

		## Inv1 PMOS
		_Buf_CLKSrc_Inv_PMOS_ChannelWidth=400,  # Scalar
		_Buf_CLKSrc_Inv_PMOS_POGate_Comb_length=100,  # Scalar

		# Additional Buffer Between Output of Comparator  And Input of Tree Buffer
		## InvChain Common
		_Buf_CompOut_Pbody_NumCont=2,  # number
		_Buf_CompOut_Nbody_NumCont=2,  # number
		_Buf_CompOut_PMOSXvt2NMOSXvt=500,  # number
		_Buf_CompOut_XvtTop2Pbody=None,  # number/None(Minimum)
		_Buf_CompOut_Xvtdown2Nbody=None,  # number/None(Minimum)

		## Inv1 common
		_Buf_CompOut_NumberofGate=[2, 4, 6],  # Vector
		_Buf_CompOut_ChannelLength=30,  # Scalar
		_Buf_CompOut_XVT='SLVT',  # 'SLVT'

		## Inv1 NMOS
		_Buf_CompOut_Inv_NMOS_ChannelWidth=200,  # Scalar
		_Buf_CompOut_Inv_NMOS_POGate_Comb_length=100,  # Scalar

		## Inv1 PMOS
		_Buf_CompOut_Inv_PMOS_ChannelWidth=400,  # Scalar
		_Buf_CompOut_Inv_PMOS_POGate_Comb_length=100,  # Scalar

		# # Additional Buffer Between Output of CLKDout  And Input of Tree Buffer
		# ## Inv1 common
		# _Buf_CLKDout_NumberofGate=[2, 4, 6],  # Vector
		# _Buf_CLKDout_ChannelLength=30,  # Scalar
		# _Buf_CLKDout_XVT='SLVT',  # 'SLVT'
		#
		# ## Inv1 NMOS
		# _Buf_CLKDout_Inv_NMOS_ChannelWidth=200,  # Scalar
		# _Buf_CLKDout_Inv_NMOS_POGate_Comb_length=100,  # Scalar
		#
		# ## Inv1 PMOS
		# _Buf_CLKDout_Inv_PMOS_ChannelWidth=400,  # Scalar
		# _Buf_CLKDout_Inv_PMOS_POGate_Comb_length=100,  # Scalar

		# # Element CDAC
		_CDAC_LayoutOption=[5, 6],
		_CDAC_ShieldingLayer=2,  # Poly:0, M1:1, M2:2 ...
		_CDAC_MetalWidth=50,
		_CDAC_MetalLength=5840,  # (8bit size: 1414/ 10bit size: 2800/ 12bit size: 4200)
		_CDAC_MetalSpacing=50,

		# #Unit Cap
		_CDAC_NumOfElement=1,

		# # Shielding & Top Connect node
		_CDAC_ConnectLength=400,
		_CDAC_ExtendLength=400,

		# # Dummy Cap Option
		_CDAC_DummyCap_TopBottomShort=False,  # False -> Bottom = GND
		_CDAC_NumOfDummyCaps=3,  # Number of dummy cap(one side)

		# # CommonCentroid With Driving node
		_CDAC_CapArrayWDrivingNodeDistance=300,  # DRC Rule
		_CDAC_DriveNodeDistance=254,  #
		_CDAC_YWidth_Bottom_Hrz=50,

		# Driver Sizing
		_Driver_SizeByBit=[32, 16, 8, 4, 2],

		# Driver(Inverter) NMOS
		_Driver_NMOS_NumberofGate=1,  # number
		_Driver_NMOS_ChannelWidth=340,  # number (8bit size: 340/ 10bit size: 680/ 12bit size: 1020)
		_Driver_NMOS_Channellength=30,  # number
		_Driver_NMOS_XVT='SLVT',  # 'XVT' ex)SLVT LVT RVT HVT

		# Driver(Inverter) PMOS
		_Driver_PMOS_NumberofGate=1,  # number
		_Driver_PMOS_ChannelWidth=900,  # number (8bit size: 900/ 10bit size: 1800/ 12bit size: 2700)
		_Driver_PMOS_Channellength=30,  # number
		_Driver_PMOS_XVT='SLVT',  # 'XVT' ex)SLVT LVT RVT HVT
		############################################################################################################################################ Bootstrap Sampler

		# Tr1 and Tr2
		# Input/Output node
		# INPUT node
		_Samp_Inputnode_width=600,  # number
		# OUTPUT node
		_Samp_Outputnode_width=600,  # number

		# Tr1
		_Samp_Tr1_NumberofGate=2,  # number
		_Samp_Tr1_ChannelWidth=300,  # number
		_Samp_Tr1_ChannelLength=30,  # number
		_Samp_Tr1_XVT='RVT',  # 'XVT' ex)SLVT LVT RVT HVT

		# Tr2
		_Samp_Tr2_NumberofGate=1,  # number
		_Samp_Tr2_ChannelWidth=1000,  # number
		_Samp_Tr2_ChannelLength=30,  # number
		_Samp_Tr2_XVT='SLVT',  # 'XVT' ex)SLVT LVT RVT HVT

		# Tr4
		_Samp_Tr4_NumberofGate=2,  # number
		_Samp_Tr4_ChannelWidth=500,  # number
		_Samp_Tr4_ChannelLength=30,  # number
		_Samp_Tr4_XVT='SLVT',  # 'XVT' ex)SLVT LVT RVT HVT

		# Tr5 Tr7 Tr9
		# PMOS: Tr5
		_Samp_Tr5_NumberofGate=1,
		_Samp_Tr5_ChannelWidth=1000,  # ref=1000
		_Samp_Tr5_ChannelLength=30,
		_Samp_Tr5_XVT='SLVT',

		# PMOS: Tr7
		_Samp_Tr7_NumberofGate=1,
		_Samp_Tr7_ChannelWidth=1000,
		_Samp_Tr7_ChannelLength=30,
		_Samp_Tr7_XVT='SLVT',

		# PMOS: Tr9
		_Samp_Tr9_NumberofGate=2,
		_Samp_Tr9_ChannelWidth=1000,  # ref = 1000
		_Samp_Tr9_ChannelLength=30,
		_Samp_Tr9_XVT='SLVT',

		# Tr8
		_Samp_Tr8_NumberofGate=2,  # number (ref:4)
		_Samp_Tr8_ChannelWidth=500,  # number (ref:500)
		_Samp_Tr8_ChannelLength=30,  # number (ref:30)
		_Samp_Tr8_XVT='SLVT',  # 'XVT' ex)SLVT LVT RVT HVT

		# Tr6 and Guardring
		# Tr6
		_Samp_Tr6_NumberofGate=1,  # number
		_Samp_Tr6_ChannelWidth=1000,  # number
		_Samp_Tr6_ChannelLength=30,  # number
		_Samp_Tr6_XVT='SLVT',  # 'XVT' ex)SLVT LVT RVT HVT

		# PMOS: Tr11 and Guardring
		# Tr11
		_Samp_Tr11_NumberofGate=2,
		_Samp_Tr11_ChannelWidth=1000,
		_Samp_Tr11_ChannelLength=30,
		_Samp_Tr11_XVT='SLVT',

		## VddTieCell4
		# VddTieCell4 NMOS
		_Samp_Tie4N_NumberofGate=4,  # number
		_Samp_Tie4N_ChannelWidth=250,  # number
		_Samp_Tie4N_ChannelLength=30,  # number
		_Samp_Tie4N_XVT='SLVT',  # 'XVT' ex)SLVT LVT RVT HVT

		# VddTieCell4 PMOS
		_Samp_Tie4P_NumberofGate=4,  # number
		_Samp_Tie4P_ChannelWidth=500,  # number
		_Samp_Tie4P_ChannelLength=30,  # number
		_Samp_Tie4P_XVT='SLVT',  # 'XVT' ex)SLVT LVT RVT HVT

		## VddTieCell8
		# VddTieCell8 NMOS
		_Samp_Tie8N_NumberofGate=4,  # number
		_Samp_Tie8N_ChannelWidth=250,  # number
		_Samp_Tie8N_ChannelLength=30,  # number
		_Samp_Tie8N_XVT='SLVT',  # 'XVT' ex)SLVT LVT RVT HVT

		# VddTieCell8 PMOS
		_Samp_Tie8P_NumberofGate=4,  # number
		_Samp_Tie8P_ChannelWidth=500,  # number
		_Samp_Tie8P_ChannelLength=30,  # number
		_Samp_Tie8P_XVT='SLVT',  # 'XVT' ex)SLVT LVT RVT HVT

		# Tr12
		_Samp_Tr12_NumberofGate=1,  # number
		_Samp_Tr12_ChannelWidth=1000,  # number
		_Samp_Tr12_ChannelLength=30,  # number
		_Samp_Tr12_XVT='SLVT',  # 'XVT' ex)SLVT LVT RVT HVT

		# Tr3
		_Samp_Tr3_NumberofGate=1,  # number
		_Samp_Tr3_ChannelWidth=1000,  # number
		_Samp_Tr3_ChannelLength=30,  # number
		_Samp_Tr3_XVT='SLVT',  # 'XVT' ex)SLVT LVT RVT HVT

		# Tr10 and Guardring
		# Tr10
		_Samp_Tr10_NumberofGate=1,  # number
		_Samp_Tr10_ChannelWidth=1000,  # number
		_Samp_Tr10_ChannelLength=30,  # number
		_Samp_Tr10_XVT='SLVT',  # 'XVT' ex)SLVT LVT RVT HVT

		# HDVNCAP_Array
		_Samp_HDVNCAP_Length=6000,
		_Samp_HDVNCAP_LayoutOption=[3, 4, 5, 6],
		_Samp_HDVNCAP_NumFigPair=53,
		_Samp_HDVNCAP_Array=3,  # number: 1xnumber
		_Samp_HDVNCAP_Cbot_Ctop_metalwidth=1000,  # number
		# Total HDVNCapSize = 601fF

		## BootStrapped Sampler CLKB Inverter
		_CLKBInv_NMOS_NumberofGate=16,
		_CLKBInv_NMOS_ChannelWidth=400,
		_CLKBInv_NMOS_ChannelLength=30,
		_CLKBInv_NMOS_XVT='SLVT',
		_CLKBInv_NMOS_POGate_Comb_length=None,

		_CLKBInv_PMOS_NumberofGate=16,
		_CLKBInv_Inv_PMOS_ChannelWidth=800,
		_CLKBInv_PMOS_ChannelLength=30,
		_CLKBInv_PMOS_XVT='SLVT',
		_CLKBInv_PMOS_POGate_Comb_length=None,

		_CLKBInv_Pbody_NumCont=2,
		_CLKBInv_XvtTop2Pbody=None,
		_CLKBInv_Nbody_NumCont=2,
		_CLKBInv_Xvtdown2Nbody=None,
		_CLKBInv_PMOSXvt2NMOSXvt=500,

        # RDAC and Decoder
        # RDAC and Decoder delta X displacement for DRC
        _RDAC_displacement=-100,

        # RDAC and Decoder Size : Consider "_Decoder_RBit" and "_Unit_Num_EachStag_input" ex) [2, 8] --> 4 : 2*8 = 2**4
        _RDAC_Size=[2, 16],

        # RDAC
        # Guardring
        RDAC_Guard_NumCont = 2,

        # Poly Resister unit
        RDAC_ResWidth		= 2000,
        RDAC_ResLength		= 1500,
        RDAC_CONUMX			= None,
        RDAC_CONUMY			= 2,

        # Decoder
        # _Unit to Unit distance for DRC of routing
        _Decoder_Unit2UnitDist=400,  # number must be 100의 배수

        # RDAC Bit
        #_Decoder_RBit = 5,

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
        _Nand_NumberofGate      = [2 ,2],  # Number
        _Nand_ChannelLength     = [30 ,30],  # Number
        _Nand_POGate_ViaMxMx    = [[0, 1] ,[0, 1]],  # Ex) [1,5] -> ViaM1M5
        # Pulldown(NMOS)
        # Physical dimension
        _Nand_NMOS_ChannelWidth                 = [400 ,500],  # Number
        # Source_node setting
        _Nand_NMOS_Source_Via_Close2POpin_TF    = [False ,False],  # True/False --> First MOS
        # Pulldown(PMOS)
        # Physical dimension
        _Nand_PMOS_ChannelWidth                 = [800 ,480],  # Number
        # Nor( _Unit_Num_EachStag_input에서 2,4,6,7...번째 해당하는 nor 생성)
        # MOSFET
        # Common
        _Nor_ChannelLength      = [30 ,30],  # Number
        _Nor_POGate_ViaMxMx     = [[0, 1] ,[0, 1]],  # Ex) [1,5] -> ViaM1M5
        # Pulldown(NMOS)
        # Physical dimension
        _Nor_NMOS_ChannelWidth	= [400 ,800],      # Number
        _Nor_NMOS_NumberofGate  = [1 ,3],        # Number
        # Pulldown(PMOS)
        # Physical dimension
        _Nor_PMOS_ChannelWidth	= [800 ,1600],      # Number
        _Nor_PMOS_NumberofGate  = [2 ,7],        # Number
        # Source_node setting
        _Nor_PMOS_Source_Via_Close2POpin_TF     = [False ,False],  # True/False --> First MOS
        # Inv
        # Common
        _Inv_NumberofGate   = 1,
        _Inv_ChannelLength  = 30,
        # NMosfet
        # Physical dimension
        _Inv_NMOS_ChannelWidth	= 400,      # Number
        # Poly Gate setting
        # Poly Gate Via setting :
        _Inv_NMOS_POGate_ViaMxMx    = [0 ,1],  # Ex) [1,5] -> ViaM1M5 -----> Fixed
        # PMosfet
        # Physical dimension
        _Inv_PMOS_ChannelWidth=800,  # Number
        # Poly Gate setting
        # Poly Gate Via setting :
        _Inv_PMOS_POGate_ViaMxMx=[0, 1],  # Ex) [1,5] -> ViaM1M5 -----> Fixed
        # Xgate
        # Common
        _Xgate_NumberofGate=1,
        _Xgate_ChannelLength=30,
        # NMosfet
        # Physical dimension
        _Xgate_NMOS_ChannelWidth=400,  # Number
        # Poly Gate setting
        # Poly Gate Via setting :
        _Xgate_NMOS_POGate_ViaMxMx=[0, 1],  # Ex) [1,5] -> ViaM1M5 -----> Fixed
        # PMosfet
        # Physical dimension
        _Xgate_PMOS_ChannelWidth=800,  # Number
        # Poly Gate setting
        # Poly Gate Via setting :
        _Xgate_PMOS_POGate_ViaMxMx=[0, 1],  # Ex) [1,5] -> ViaM1M5 -----> Fixed
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

								  _NumofRbit=None,

								  _NumofCbit=None,
								  _CDAC_Folding=None,  # None/True/False
								  _Driver_DecimationIfDriverPlacedInCommonCentroid=True,
								  _Driver_DecimationFactor=[2, 0, 0, 0, 0, 0, 0],  # [MSB, MSB-1 ... MSB-x]: 단 X<MSB  # 위 옵션 True시 작동; MSB부터 벡터로 작성; [3,2,2] 시 MSB0 -> 3:1, MSB1 -> 2:1, MSB2 -> 2:1, ... 1은 불가
								  _SpaceBtwBootSWPosNeg=None,

								  _Test_distance=330,
								  _Routing_width=50,
								  _Routing_distance=80,

								  _SARLogic_YWidthOfCLKSrc=100,
								  _SARLogic_SpaceBtwCLKSrcAndCLKSamp=100,
								  _SARLogic_YWidthOfCLKSamp=100,

								  _SARLogic_YWidthOfCompOut=100,
								  _SARLogic_SpaceBtwCompOutAndCLKDout=100,
								  _SARLogic_YWidthOfCLKDout=100,

								  ## DFF Common
								  _SARLogic_DFF_Pbody_NumCont=2,  # number
								  _SARLogic_DFF_Nbody_NumCont=2,  # number
								  _SARLogic_DFF_PMOSXvt2NMOSXvt=1150,  # number
								  _SARLogic_DFF_XvtTop2Pbody=None,  # number/None(Minimum)
								  _SARLogic_DFF_Xvtdown2Nbody=None,  # number/None(Minimum)

								  ## Master Xgate1
								  ## Xgate common

								  ## Xgate NMOS
								  _SARLogic_Mst_Xgate1_NMOS_NumberofGate=1,  # 1
								  _SARLogic_Mst_Xgate1_NMOS_ChannelWidth=200,  # 100
								  _SARLogic_Mst_Xgate1_NMOS_ChannelLength=30,
								  _SARLogic_Mst_Xgate1_NMOS_XVT='HVT',
								  _SARLogic_Mst_Xgate1_NMOS_POGate_Comb_length=100,

								  ## Xgate PMOS
								  _SARLogic_Mst_Xgate1_PMOS_NumberofGate=1,  # 1
								  _SARLogic_Mst_Xgate1_PMOS_ChannelWidth=400,  # 200
								  _SARLogic_Mst_Xgate1_PMOS_ChannelLength=30,
								  _SARLogic_Mst_Xgate1_PMOS_XVT='HVT',
								  _SARLogic_Mst_Xgate1_PMOS_POGate_Comb_length=100,

								  ## Master Xgate2
								  ## Xgate common

								  ## Xgate NMOS
								  _SARLogic_Mst_Xgate2_NMOS_NumberofGate=1,
								  _SARLogic_Mst_Xgate2_NMOS_ChannelWidth=200,
								  _SARLogic_Mst_Xgate2_NMOS_ChannelLength=30,
								  _SARLogic_Mst_Xgate2_NMOS_XVT='SLVT',
								  _SARLogic_Mst_Xgate2_NMOS_POGate_Comb_length=100,

								  ## Xgate PMOS
								  _SARLogic_Mst_Xgate2_PMOS_NumberofGate=2,  # 2
								  _SARLogic_Mst_Xgate2_PMOS_ChannelWidth=200,
								  _SARLogic_Mst_Xgate2_PMOS_ChannelLength=30,
								  _SARLogic_Mst_Xgate2_PMOS_XVT='SLVT',
								  _SARLogic_Mst_Xgate2_PMOS_POGate_Comb_length=100,

								  ## Master Nor1
								  ## Nor1 common

								  ## NMOS
								  ## NMOS common
								  _SARLogic_Mst_Nor1_NMOS_XVT='HVT',

								  ## NMOSA
								  _SARLogic_Mst_Nor1_NMOSA_NumberofGate=2,
								  _SARLogic_Mst_Nor1_NMOSA_ChannelWidth=200,
								  _SARLogic_Mst_Nor1_NMOSA_ChannelLength=30,
								  _SARLogic_Mst_Nor1_NMOSA_POGate_Comb_length=100,

								  ## NMOSB
								  _SARLogic_Mst_Nor1_NMOSB_NumberofGate=2,
								  _SARLogic_Mst_Nor1_NMOSB_ChannelWidth=200,
								  _SARLogic_Mst_Nor1_NMOSB_ChannelLength=30,
								  _SARLogic_Mst_Nor1_NMOSB_POGate_Comb_length=100,

								  ## PMOS
								  ## PMOS common
								  _SARLogic_Mst_Nor1_PMOS_XVT='HVT',

								  ## PMOSA
								  _SARLogic_Mst_Nor1_PMOSA_NumberofGate=4,
								  _SARLogic_Mst_Nor1_PMOSA_ChannelWidth=400,
								  _SARLogic_Mst_Nor1_PMOSA_ChannelLength=30,
								  _SARLogic_Mst_Nor1_PMOSA_POGate_Comb_length=100,

								  ## PMOSB
								  _SARLogic_Mst_Nor1_PMOSB_NumberofGate=4,
								  _SARLogic_Mst_Nor1_PMOSB_ChannelWidth=400,
								  _SARLogic_Mst_Nor1_PMOSB_ChannelLength=30,
								  _SARLogic_Mst_Nor1_PMOSB_POGate_Comb_length=100,

								  ## Master Nor2
								  ## Nor2 common

								  ## NMOS
								  ## NMOS common
								  _SARLogic_Mst_Nor2_NMOS_XVT='HVT',

								  ## NMOSA
								  _SARLogic_Mst_Nor2_NMOSA_NumberofGate=2,
								  _SARLogic_Mst_Nor2_NMOSA_ChannelWidth=200,
								  _SARLogic_Mst_Nor2_NMOSA_ChannelLength=30,
								  _SARLogic_Mst_Nor2_NMOSA_POGate_Comb_length=100,

								  ## NMOSB
								  _SARLogic_Mst_Nor2_NMOSB_NumberofGate=2,
								  _SARLogic_Mst_Nor2_NMOSB_ChannelWidth=200,
								  _SARLogic_Mst_Nor2_NMOSB_ChannelLength=30,
								  _SARLogic_Mst_Nor2_NMOSB_POGate_Comb_length=100,

								  ## PMOS
								  ## PMOS common
								  _SARLogic_Mst_Nor2_PMOS_XVT='HVT',

								  ## PMOSA
								  _SARLogic_Mst_Nor2_PMOSA_NumberofGate=4,
								  _SARLogic_Mst_Nor2_PMOSA_ChannelWidth=400,
								  _SARLogic_Mst_Nor2_PMOSA_ChannelLength=30,
								  _SARLogic_Mst_Nor2_PMOSA_POGate_Comb_length=100,

								  ## PMOSB
								  _SARLogic_Mst_Nor2_PMOSB_NumberofGate=4,
								  _SARLogic_Mst_Nor2_PMOSB_ChannelWidth=400,
								  _SARLogic_Mst_Nor2_PMOSB_ChannelLength=30,
								  _SARLogic_Mst_Nor2_PMOSB_POGate_Comb_length=100,

								  ## Master Inv1 : Set pre-driver
								  ## Inv1 common

								  ## Inv1 NMOS
								  _SARLogic_Mst_Inv1_NMOS_NumberofGate=1,
								  _SARLogic_Mst_Inv1_NMOS_ChannelWidth=200,
								  _SARLogic_Mst_Inv1_NMOS_ChannelLength=30,
								  _SARLogic_Mst_Inv1_NMOS_XVT='SLVT',
								  _SARLogic_Mst_Inv1_NMOS_POGate_Comb_length=100,

								  ## Inv1 PMOS
								  _SARLogic_Mst_Inv1_PMOS_NumberofGate=1,
								  _SARLogic_Mst_Inv1_PMOS_ChannelWidth=400,
								  _SARLogic_Mst_Inv1_PMOS_ChannelLength=30,
								  _SARLogic_Mst_Inv1_PMOS_XVT='SLVT',
								  _SARLogic_Mst_Inv1_PMOS_POGate_Comb_length=100,

								  ## Master Inv2 : Set driver
								  ## Inv2 common

								  ## Inv2 NMOS
								  _SARLogic_Mst_Inv2_NMOS_NumberofGate=1,
								  _SARLogic_Mst_Inv2_NMOS_ChannelWidth=200,
								  _SARLogic_Mst_Inv2_NMOS_ChannelLength=30,
								  _SARLogic_Mst_Inv2_NMOS_XVT='SLVT',
								  _SARLogic_Mst_Inv2_NMOS_POGate_Comb_length=100,

								  ## Inv2 PMOS
								  _SARLogic_Mst_Inv2_PMOS_NumberofGate=1,
								  _SARLogic_Mst_Inv2_PMOS_ChannelWidth=400,
								  _SARLogic_Mst_Inv2_PMOS_ChannelLength=30,
								  _SARLogic_Mst_Inv2_PMOS_XVT='SLVT',
								  _SARLogic_Mst_Inv2_PMOS_POGate_Comb_length=100,

								  ## Master Inv3 : Clock driver
								  ## Inv3 common

								  ## Inv3 NMOS
								  _SARLogic_Mst_Inv3_NMOS_NumberofGate=1,
								  _SARLogic_Mst_Inv3_NMOS_ChannelWidth=200,
								  _SARLogic_Mst_Inv3_NMOS_ChannelLength=30,
								  _SARLogic_Mst_Inv3_NMOS_XVT='SLVT',
								  _SARLogic_Mst_Inv3_NMOS_POGate_Comb_length=100,

								  ## Inv3 PMOS
								  _SARLogic_Mst_Inv3_PMOS_NumberofGate=1,
								  _SARLogic_Mst_Inv3_PMOS_ChannelWidth=400,
								  _SARLogic_Mst_Inv3_PMOS_ChannelLength=30,
								  _SARLogic_Mst_Inv3_PMOS_XVT='SLVT',
								  _SARLogic_Mst_Inv3_PMOS_POGate_Comb_length=100,

								  ## Slave Xgate1
								  ## Xgate common

								  ## Xgate NMOS
								  _SARLogic_Slv_Xgate1_NMOS_NumberofGate=1,
								  _SARLogic_Slv_Xgate1_NMOS_ChannelWidth=200,
								  _SARLogic_Slv_Xgate1_NMOS_ChannelLength=30,
								  _SARLogic_Slv_Xgate1_NMOS_XVT='HVT',
								  _SARLogic_Slv_Xgate1_NMOS_POGate_Comb_length=100,

								  ## Xgate NMOS
								  _SARLogic_Slv_Xgate1_PMOS_NumberofGate=1,
								  _SARLogic_Slv_Xgate1_PMOS_ChannelWidth=400,
								  _SARLogic_Slv_Xgate1_PMOS_ChannelLength=30,
								  _SARLogic_Slv_Xgate1_PMOS_XVT='HVT',
								  _SARLogic_Slv_Xgate1_PMOS_POGate_Comb_length=100,

								  ## Slave Xgate2
								  ## Xgate common

								  ## Xgate NMOS
								  _SARLogic_Slv_Xgate2_NMOS_NumberofGate=1,
								  _SARLogic_Slv_Xgate2_NMOS_ChannelWidth=200,
								  _SARLogic_Slv_Xgate2_NMOS_ChannelLength=30,
								  _SARLogic_Slv_Xgate2_NMOS_XVT='SLVT',
								  _SARLogic_Slv_Xgate2_NMOS_POGate_Comb_length=100,

								  ## Xgate NMOS
								  _SARLogic_Slv_Xgate2_PMOS_NumberofGate=2,
								  _SARLogic_Slv_Xgate2_PMOS_ChannelWidth=200,
								  _SARLogic_Slv_Xgate2_PMOS_ChannelLength=30,
								  _SARLogic_Slv_Xgate2_PMOS_XVT='SLVT',
								  _SARLogic_Slv_Xgate2_PMOS_POGate_Comb_length=100,

								  ## Slave Nor1
								  ## Nor1 common

								  ## NMOS
								  ## NMOS common
								  _SARLogic_Slv_Nor1_NMOS_XVT='HVT',

								  ## NMOSA
								  _SARLogic_Slv_Nor1_NMOSA_NumberofGate=2,
								  _SARLogic_Slv_Nor1_NMOSA_ChannelWidth=200,
								  _SARLogic_Slv_Nor1_NMOSA_ChannelLength=30,
								  _SARLogic_Slv_Nor1_NMOSA_POGate_Comb_length=100,

								  ## NMOSB
								  _SARLogic_Slv_Nor1_NMOSB_NumberofGate=2,
								  _SARLogic_Slv_Nor1_NMOSB_ChannelWidth=200,
								  _SARLogic_Slv_Nor1_NMOSB_ChannelLength=30,
								  _SARLogic_Slv_Nor1_NMOSB_POGate_Comb_length=100,

								  ## PMOS
								  ## PMOS common
								  _SARLogic_Slv_Nor1_PMOS_XVT='HVT',

								  ## PMOSA
								  _SARLogic_Slv_Nor1_PMOSA_NumberofGate=4,
								  _SARLogic_Slv_Nor1_PMOSA_ChannelWidth=400,
								  _SARLogic_Slv_Nor1_PMOSA_ChannelLength=30,
								  _SARLogic_Slv_Nor1_PMOSA_POGate_Comb_length=100,

								  ## PMOSB
								  _SARLogic_Slv_Nor1_PMOSB_NumberofGate=4,
								  _SARLogic_Slv_Nor1_PMOSB_ChannelWidth=400,
								  _SARLogic_Slv_Nor1_PMOSB_ChannelLength=30,
								  _SARLogic_Slv_Nor1_PMOSB_POGate_Comb_length=100,

								  ## Slave Nor2
								  ## Nor2 common

								  ## NMOS
								  ## NMOS common
								  _SARLogic_Slv_Nor2_NMOS_XVT='HVT',

								  ## NMOSA
								  _SARLogic_Slv_Nor2_NMOSA_NumberofGate=2,
								  _SARLogic_Slv_Nor2_NMOSA_ChannelWidth=200,
								  _SARLogic_Slv_Nor2_NMOSA_ChannelLength=30,
								  _SARLogic_Slv_Nor2_NMOSA_POGate_Comb_length=100,

								  ## NMOSB
								  _SARLogic_Slv_Nor2_NMOSB_NumberofGate=2,
								  _SARLogic_Slv_Nor2_NMOSB_ChannelWidth=200,
								  _SARLogic_Slv_Nor2_NMOSB_ChannelLength=30,
								  _SARLogic_Slv_Nor2_NMOSB_POGate_Comb_length=100,

								  ## PMOS
								  ## PMOS common
								  _SARLogic_Slv_Nor2_PMOS_XVT='HVT',

								  ## PMOSA
								  _SARLogic_Slv_Nor2_PMOSA_NumberofGate=4,
								  _SARLogic_Slv_Nor2_PMOSA_ChannelWidth=400,
								  _SARLogic_Slv_Nor2_PMOSA_ChannelLength=30,
								  _SARLogic_Slv_Nor2_PMOSA_POGate_Comb_length=100,

								  ## PMOSB
								  _SARLogic_Slv_Nor2_PMOSB_NumberofGate=4,
								  _SARLogic_Slv_Nor2_PMOSB_ChannelWidth=400,
								  _SARLogic_Slv_Nor2_PMOSB_ChannelLength=30,
								  _SARLogic_Slv_Nor2_PMOSB_POGate_Comb_length=100,

								  ## Slave Inv1 : ReSet pre-driver
								  ## Inv1 common

								  ## Inv1 NMOS
								  _SARLogic_Slv_Inv1_NMOS_NumberofGate=1,
								  _SARLogic_Slv_Inv1_NMOS_ChannelWidth=200,
								  _SARLogic_Slv_Inv1_NMOS_ChannelLength=30,
								  _SARLogic_Slv_Inv1_NMOS_XVT='SLVT',
								  _SARLogic_Slv_Inv1_NMOS_POGate_Comb_length=100,

								  ## Inv1 PMOS
								  _SARLogic_Slv_Inv1_PMOS_NumberofGate=1,
								  _SARLogic_Slv_Inv1_PMOS_ChannelWidth=400,
								  _SARLogic_Slv_Inv1_PMOS_ChannelLength=30,
								  _SARLogic_Slv_Inv1_PMOS_XVT='SLVT',
								  _SARLogic_Slv_Inv1_PMOS_POGate_Comb_length=100,

								  ## Slave Inv2 : ReSet driver
								  ## Inv2 common

								  ## Inv2 NMOS
								  _SARLogic_Slv_Inv2_NMOS_NumberofGate=1,
								  _SARLogic_Slv_Inv2_NMOS_ChannelWidth=300,
								  _SARLogic_Slv_Inv2_NMOS_ChannelLength=30,
								  _SARLogic_Slv_Inv2_NMOS_XVT='SLVT',
								  _SARLogic_Slv_Inv2_NMOS_POGate_Comb_length=100,

								  ## Inv2 PMOS
								  _SARLogic_Slv_Inv2_PMOS_NumberofGate=1,
								  _SARLogic_Slv_Inv2_PMOS_ChannelWidth=400,
								  _SARLogic_Slv_Inv2_PMOS_ChannelLength=30,
								  _SARLogic_Slv_Inv2_PMOS_XVT='SLVT',
								  _SARLogic_Slv_Inv2_PMOS_POGate_Comb_length=100,

								  ## Slave Inv3 : Qb driver
								  ## Inv3 common

								  ## Inv3 NMOS
								  _SARLogic_Slv_Inv3_NMOS_NumberofGate=5,  # 1
								  _SARLogic_Slv_Inv3_NMOS_ChannelWidth=200,
								  _SARLogic_Slv_Inv3_NMOS_ChannelLength=30,
								  _SARLogic_Slv_Inv3_NMOS_XVT='SLVT',
								  _SARLogic_Slv_Inv3_NMOS_POGate_Comb_length=100,

								  ## Inv3 PMOS
								  _SARLogic_Slv_Inv3_PMOS_NumberofGate=5,  # 1
								  _SARLogic_Slv_Inv3_PMOS_ChannelWidth=400,
								  _SARLogic_Slv_Inv3_PMOS_ChannelLength=30,
								  _SARLogic_Slv_Inv3_PMOS_XVT='SLVT',
								  _SARLogic_Slv_Inv3_PMOS_POGate_Comb_length=100,

								  # Top Clock  Tree Size
								  _SARLogic_CLKBufTreeTop_NumOfStage=4,
								  _SARLogic_CLKBufTreeTop_CLKSampBuf_SizeByStage=None,
								  _SARLogic_CLKBufTreeTop_CLKSrcBuf_SizeByStage=None,
								  # 스테이지에 따른 버퍼 사이즈(UnitBuffer의 배수로 각 스테이지의 크기가 결정 됨.)
								  _SARLogic_CLKBufTreeTop_XOffSet=0,

								  ## Top CLK Buffer Size
								  _SARLogic_CLKBufTreeTop_Inv_NMOS_ChannelWidth=400,  # Number
								  _SARLogic_CLKBufTreeTop_Inv_NMOS_ChannelLength=30,  # Number
								  _SARLogic_CLKBufTreeTop_Inv_NMOS_NumberofGate=1,  # Number
								  _SARLogic_CLKBufTreeTop_Inv_NMOS_XVT='SLVT',  # 'XVT' ex)SLVT/LVT/RVT/HVT
								  _SARLogic_CLKBufTreeTop_Inv_NMOS_POGate_Comb_length=100,  # None/Number

								  _SARLogic_CLKBufTreeTop_Inv_PMOS_ChannelWidth=800,  # Number
								  _SARLogic_CLKBufTreeTop_Inv_PMOS_ChannelLength=30,  # Number
								  _SARLogic_CLKBufTreeTop_Inv_PMOS_NumberofGate=1,  # Number
								  _SARLogic_CLKBufTreeTop_Inv_PMOS_XVT='SLVT',  # 'XVT' ex)SLVT/LVT/RVT/HVT
								  _SARLogic_CLKBufTreeTop_Inv_PMOS_POGate_Comb_length=100,  # None/Number

								  # Top CLK BufferPowerRail Size
								  _SARLogic_CLKBufTreeTop_NMOS_Pbody_NumCont=2,
								  _SARLogic_CLKBufTreeTop_NMOS_Pbody_XvtTop2Pbody=None,
								  _SARLogic_CLKBufTreeTop_PMOS_Nbody_NumCont=2,
								  _SARLogic_CLKBufTreeTop_PMOS_Nbody_Xvtdown2Nbody=None,
								  _SARLogic_CLKBufTreeTop_PMOSXvt2NMOSXvt=700,

								  # Bottom Clock  Tree Size
								  _SARLogic_CLKBufTreeBot_NumOfStage=4,
								  _SARLogic_CLKBufTreeBot_CompOutBuf_SizeByStage=None,
								  _SARLogic_CLKBufTreeBot_CLKDoutBuf_SizeByStage=None,
								  # 스테이지에 따른 버퍼 사이즈(UnitBuffer의 배수로 각 스테이지의 크기가 결정 됨.)
								  _SARLogic_CLKBufTreeBot_XOffSet=0,

								  ## Bottom CLK Buffer Size
								  _SARLogic_CLKBufTreeBot_Inv_NMOS_ChannelWidth=400,  # Number
								  _SARLogic_CLKBufTreeBot_Inv_NMOS_ChannelLength=30,  # Number
								  _SARLogic_CLKBufTreeBot_Inv_NMOS_NumberofGate=1,  # Number
								  _SARLogic_CLKBufTreeBot_Inv_NMOS_XVT='SLVT',  # 'XVT' ex)SLVT/LVT/RVT/HVT
								  _SARLogic_CLKBufTreeBot_Inv_NMOS_POGate_Comb_length=100,  # None/Number

								  _SARLogic_CLKBufTreeBot_Inv_PMOS_ChannelWidth=800,  # Number
								  _SARLogic_CLKBufTreeBot_Inv_PMOS_ChannelLength=30,  # Number
								  _SARLogic_CLKBufTreeBot_Inv_PMOS_NumberofGate=1,  # Number
								  _SARLogic_CLKBufTreeBot_Inv_PMOS_XVT='SLVT',  # 'XVT' ex)SLVT/LVT/RVT/HVT
								  _SARLogic_CLKBufTreeBot_Inv_PMOS_POGate_Comb_length=100,  # None/Number

								  # Bottom CLK Buffer PowerRail Size
								  _SARLogic_CLKBufTreeBot_NMOS_Pbody_NumCont=2,
								  _SARLogic_CLKBufTreeBot_NMOS_Pbody_XvtTop2Pbody=None,
								  _SARLogic_CLKBufTreeBot_PMOS_Nbody_NumCont=2,
								  _SARLogic_CLKBufTreeBot_PMOS_Nbody_Xvtdown2Nbody=None,
								  _SARLogic_CLKBufTreeBot_PMOSXvt2NMOSXvt=700,

								  #### CDAC Pre-Driver Sizing
								  ## InvChain Common
								  _CDACPreDriver_Pbody_NumCont=2,  # number
								  _CDACPreDriver_Nbody_NumCont=2,  # number
								  _CDACPreDriver_PMOSXvt2NMOSXvt=500,  # number
								  _CDACPreDriver_XvtTop2Pbody=None,  # number/None(Minimum)
								  _CDACPreDriver_Xvtdown2Nbody=None,  # number/None(Minimum)

								  ## Inverter Chain
								  ## Inv1 common
								  _CDACPreDriver_NumberofGate=[2, 4, 6],  # Vector
								  _CDACPreDriver_ChannelLength=30,  # Scalar
								  _CDACPreDriver_XVT='SLVT',  # 'SLVT'

								  ## Inv1 NMOS
								  _CDACPreDriver_Inv_NMOS_ChannelWidth=200,  # Scalar
								  _CDACPreDriver_Inv_NMOS_POGate_Comb_length=100,  # Scalar

								  ## Inv1 PMOS
								  _CDACPreDriver_Inv_PMOS_ChannelWidth=400,  # Scalar
								  _CDACPreDriver_Inv_PMOS_POGate_Comb_length=100,  # Scalar

								  ## CLKDout(OutSamp) Inverter & AND Common Option
								  _CLKDout_XVT_Common='SLVT',

								  ## CLKDout(OutSamp) Inverter Size
								  _CLKDout_Inv_NMOS_ChannelWidth=400,  # Number
								  _CLKDout_Inv_NMOS_ChannelLength=30,  # Number
								  _CLKDout_Inv_NMOS_NumberofGate=1,  # Number
								  _CLKDout_Inv_NMOS_POGate_Comb_length=100,  # None/Number

								  _CLKDout_Inv_PMOS_ChannelWidth=800,  # Number
								  _CLKDout_Inv_PMOS_ChannelLength=30,  # Number
								  _CLKDout_Inv_PMOS_NumberofGate=1,  # Number
								  _CLKDout_Inv_PMOS_POGate_Comb_length=100,  # None/Number

								  ## CLKDout(OutSamp) AND Size
								  _CLKDout_AND_NAND_NMOS_ChannelWidth=400,
								  _CLKDout_AND_NAND_NMOS_ChannelLength=30,
								  _CLKDout_AND_NAND_NMOS_NumberofGate=2,

								  _CLKDout_AND_NAND_PMOS_ChannelWidth=800,
								  _CLKDout_AND_NAND_PMOS_ChannelLength=30,
								  _CLKDout_AND_NAND_PMOS_NumberofGate=1,

								  _CLKDout_AND_Inv_NMOS_ChannelWidth=400,
								  _CLKDout_AND_Inv_NMOS_ChannelLength=30,
								  _CLKDout_AND_Inv_NMOS_NumberofGate=1,
								  _CLKDout_AND_Inv_NMOS_POGate_Comb_length=100,

								  _CLKDout_AND_Inv_PMOS_ChannelWidth=800,
								  _CLKDout_AND_Inv_PMOS_ChannelLength=30,
								  _CLKDout_AND_Inv_PMOS_NumberofGate=1,
								  _CLKDout_AND_Inv_PMOS_POGate_Comb_length=100,

								  ## StrongArm Latch
								  _Comp_SALatch_CLKinputPMOSFinger1=None,  # 6
								  _Comp_SALatch_CLKinputPMOSFinger2=None,  # 3
								  _Comp_SALatch_PMOSFinger=None,  # 3
								  _Comp_SALatch_PMOSChannelWidth=None,  # 500
								  _Comp_SALatch_DATAinputNMOSFinger=None,  # 12
								  _Comp_SALatch_NMOSFinger=None,  # 2
								  _Comp_SALatch_CLKinputNMOSFinger=None,  # 8
								  _Comp_SALatch_NMOSChannelWidth=None,  # 500
								  _Comp_SALatch_CLKinputNMOSChannelWidth=None,  # 800
								  _Comp_SALatch_ChannelLength=None,  # 30
								  _Comp_SALatch_Dummy=True,
								  _Comp_SALatch_XVT=None,
								  _Comp_SALatch_GuardringWidth=None,
								  _Comp_SALatch_Guardring=True,
								  _Comp_SALatch_SlicerGuardringWidth=None,
								  _Comp_SALatch_SlicerGuardring=None,
								  _Comp_SALatch_NumSupplyCOY=None,
								  _Comp_SALatch_NumSupplyCOX=None,
								  _Comp_SALatch_SupplyMet1XWidth=None,
								  _Comp_SALatch_SupplyMet1YWidth=None,
								  _Comp_SALatch_VDD2VSSHeight=None,
								  _Comp_SALatch_NumVIAPoly2Met1COX=None,
								  _Comp_SALatch_NumVIAPoly2Met1COY=None,
								  _Comp_SALatch_NumVIAMet12COX=None,
								  _Comp_SALatch_NumVIAMet12COY=None,
								  _Comp_SALatch_PowerLine=False,

								  ## StrongARMLatch Output Buffer Sizing
								  # Inverter1
								  _Comp_SAOutBuf_Inv1_NMOS_ChannelWidth=None,  # Number
								  _Comp_SAOutBuf_Inv1_NMOS_ChannelLength=None,  # Number
								  _Comp_SAOutBuf_Inv1_NMOS_NumberofGate=None,  # Number
								  _Comp_SAOutBuf_Inv1_NMOS_XVT=None,  # 'XVT' ex)SLVT/LVT/RVT/HVT
								  _Comp_SAOutBuf_Inv1_NMOS_POGate_Comb_length=None,  # None/Number

								  _Comp_SAOutBuf_Inv1_PMOS_ChannelWidth=None,  # Number
								  _Comp_SAOutBuf_Inv1_PMOS_ChannelLength=None,  # Number
								  _Comp_SAOutBuf_Inv1_PMOS_NumberofGate=None,  # Number
								  _Comp_SAOutBuf_Inv1_PMOS_XVT=None,  # 'XVT' ex)SLVT/LVT/RVT/HVT
								  _Comp_SAOutBuf_Inv1_PMOS_POGate_Comb_length=None,  # None/Number

								  # Inverter2
								  _Comp_SAOutBuf_Inv2_NMOS_ChannelWidth=None,  # Number
								  _Comp_SAOutBuf_Inv2_NMOS_ChannelLength=None,  # Number
								  _Comp_SAOutBuf_Inv2_NMOS_NumberofGate=None,  # Number
								  _Comp_SAOutBuf_Inv2_NMOS_XVT=None,  # 'XVT' ex)SLVT/LVT/RVT/HVT
								  _Comp_SAOutBuf_Inv2_NMOS_POGate_Comb_length=None,  # None/Number

								  _Comp_SAOutBuf_Inv2_PMOS_ChannelWidth=None,  # Number
								  _Comp_SAOutBuf_Inv2_PMOS_ChannelLength=None,  # Number
								  _Comp_SAOutBuf_Inv2_PMOS_NumberofGate=None,  # Number
								  _Comp_SAOutBuf_Inv2_PMOS_XVT=None,  # 'XVT' ex)SLVT/LVT/RVT/HVT
								  _Comp_SAOutBuf_Inv2_PMOS_POGate_Comb_length=None,  # None/Number

								  ## SR Latch Sizing
								  _Comp_SRLatch_NAND_NMOS_ChannelWidth=None,  # Number
								  _Comp_SRLatch_NAND_NMOS_ChannelLength=None,  # Number
								  _Comp_SRLatch_NAND_NMOS_NumberofGate=None,  # Number
								  _Comp_SRLatch_NAND_NMOS_XVT=None,  # 'XVT' ex)SLVT/LVT/RVT/HVT
								  _Comp_SRLatch_NAND_NMOS_POGate_Comb_length=None,  # None/Number

								  _Comp_SRLatch_NAND_PMOS_ChannelWidth=None,  # Number
								  _Comp_SRLatch_NAND_PMOS_ChannelLength=None,  # Number
								  _Comp_SRLatch_NAND_PMOS_NumberofGate=None,  # Number
								  _Comp_SRLatch_NAND_PMOS_XVT=None,  # 'XVT' ex)SLVT/LVT/RVT/HVT
								  _Comp_SRLatch_NAND_PMOS_POGate_Comb_length=None,  # None/Number

								  # CLK Input Logic Gates
								  _Comp_CLKSamp_Inv_NMOS_ChannelWidth=None,
								  _Comp_CLKSamp_Inv_NMOS_ChannelLength=None,
								  _Comp_CLKSamp_Inv_NMOS_NumberofGate=None,
								  _Comp_CLKSamp_Inv_NMOS_XVT=None,
								  _Comp_CLKSamp_Inv_NMOS_POGate_Comb_length=None,

								  _Comp_CLKSamp_Inv_PMOS_ChannelWidth=None,
								  _Comp_CLKSamp_Inv_PMOS_ChannelLength=None,
								  _Comp_CLKSamp_Inv_PMOS_NumberofGate=None,
								  _Comp_CLKSamp_Inv_PMOS_XVT=None,
								  _Comp_CLKSamp_Inv_PMOS_POGate_Comb_length=None,

								  _Comp_CLKSrc_Inv_NMOS_ChannelWidth=None,
								  _Comp_CLKSrc_Inv_NMOS_ChannelLength=None,
								  _Comp_CLKSrc_Inv_NMOS_NumberofGate=None,
								  _Comp_CLKSrc_Inv_NMOS_XVT=None,
								  _Comp_CLKSrc_Inv_NMOS_POGate_Comb_length=None,

								  _Comp_CLKSrc_Inv_PMOS_ChannelWidth=None,
								  _Comp_CLKSrc_Inv_PMOS_ChannelLength=None,
								  _Comp_CLKSrc_Inv_PMOS_NumberofGate=None,
								  _Comp_CLKSrc_Inv_PMOS_XVT=None,
								  _Comp_CLKSrc_Inv_PMOS_POGate_Comb_length=None,

								  ## CLKSrc & CLKSample AND Gate
								  _Comp_AND_NAND_NMOS_ChannelWidth=None,
								  _Comp_AND_NAND_NMOS_ChannelLength=None,
								  _Comp_AND_NAND_NMOS_NumberofGate=None,
								  _Comp_AND_NAND_NMOS_XVT=None,

								  _Comp_AND_NAND_PMOS_ChannelWidth=None,
								  _Comp_AND_NAND_PMOS_ChannelLength=None,
								  _Comp_AND_NAND_PMOS_NumberofGate=None,
								  _Comp_AND_NAND_PMOS_XVT=None,

								  _Comp_AND_Inv_NMOS_ChannelWidth=None,
								  _Comp_AND_Inv_NMOS_ChannelLength=None,
								  _Comp_AND_Inv_NMOS_NumberofGate=None,
								  _Comp_AND_Inv_NMOS_XVT=None,
								  _Comp_AND_Inv_NMOS_POGate_Comb_length=None,

								  _Comp_AND_Inv_PMOS_ChannelWidth=None,
								  _Comp_AND_Inv_PMOS_ChannelLength=None,
								  _Comp_AND_Inv_PMOS_NumberofGate=None,
								  _Comp_AND_Inv_PMOS_XVT=None,
								  _Comp_AND_Inv_PMOS_POGate_Comb_length=None,

								  ## CLK Buffer
								  # Inverter1
								  _Comp_CLKBuf_Inv1_NMOS_ChannelWidth=None,  # Number
								  _Comp_CLKBuf_Inv1_NMOS_ChannelLength=None,  # Number
								  _Comp_CLKBuf_Inv1_NMOS_NumberofGate=None,  # Number
								  _Comp_CLKBuf_Inv1_NMOS_XVT=None,  # 'XVT' ex)SLVT/LVT/RVT/HVT
								  _Comp_CLKBuf_Inv1_NMOS_POGate_Comb_length=None,  # None/Number

								  _Comp_CLKBuf_Inv1_PMOS_ChannelWidth=None,  # Number
								  _Comp_CLKBuf_Inv1_PMOS_ChannelLength=None,  # Number
								  _Comp_CLKBuf_Inv1_PMOS_NumberofGate=None,  # Number
								  _Comp_CLKBuf_Inv1_PMOS_XVT=None,  # 'XVT' ex)SLVT/LVT/RVT/HVT
								  _Comp_CLKBuf_Inv1_PMOS_POGate_Comb_length=None,  # None/Number

								  # Inverter2
								  _Comp_CLKBuf_Inv2_NMOS_ChannelWidth=None,  # Number
								  _Comp_CLKBuf_Inv2_NMOS_ChannelLength=None,  # Number
								  _Comp_CLKBuf_Inv2_NMOS_NumberofGate=None,  # Number
								  _Comp_CLKBuf_Inv2_NMOS_XVT=None,  # 'XVT' ex)SLVT/LVT/RVT/HVT
								  _Comp_CLKBuf_Inv2_NMOS_POGate_Comb_length=None,  # None/Number

								  _Comp_CLKBuf_Inv2_PMOS_ChannelWidth=None,  # Number
								  _Comp_CLKBuf_Inv2_PMOS_ChannelLength=None,  # Number
								  _Comp_CLKBuf_Inv2_PMOS_NumberofGate=None,  # Number
								  _Comp_CLKBuf_Inv2_PMOS_XVT=None,  # 'XVT' ex)SLVT/LVT/RVT/HVT
								  _Comp_CLKBuf_Inv2_PMOS_POGate_Comb_length=None,  # None/Number

								  # PowerRail Placement
								  _Comp_BufSR_NMOS_Pbody_NumCont=None,
								  _Comp_BufSR_NMOS_Pbody_XvtTop2Pbody=None,
								  _Comp_BufSR_PMOS_Nbody_NumCont=None,
								  _Comp_BufSR_PMOS_Nbody_Xvtdown2Nbody=None,
								  _Comp_BufSR_PMOSXvt2NMOSXvt=None,

								  _Comp_CLKInLogic_NMOS_Pbody_Xvtdown2Pbody=None,
								  _Comp_CLKInLogic_PMOS_Nbody_NumCont=None,
								  _Comp_CLKInLogic_PMOS_Nbody_Xvtdown2Nbody=None,
								  _Comp_CLKInLogic_PMOSXvt2NMOSXvt=None,

								  # Additional Buffer Between CLK_Sample Input of Comparator And Output of Tree Buffer
								  ## InvChain Common
								  _Buf_CLKSamp_Pbody_NumCont=2,  # number
								  _Buf_CLKSamp_Nbody_NumCont=2,  # number
								  _Buf_CLKSamp_PMOSXvt2NMOSXvt=500,  # number
								  _Buf_CLKSamp_XvtTop2Pbody=None,  # number/None(Minimum)
								  _Buf_CLKSamp_Xvtdown2Nbody=None,  # number/None(Minimum)

								  ## Inverter Chain
								  ## Inv1 common
								  _Buf_CLKSamp_NumberofGate=[2, 4, 6],  # Vector
								  _Buf_CLKSamp_ChannelLength=30,  # Scalar
								  _Buf_CLKSamp_XVT='SLVT',  # 'SLVT'

								  ## Inv1 NMOS
								  _Buf_CLKSamp_Inv_NMOS_ChannelWidth=200,  # Scalar
								  _Buf_CLKSamp_Inv_NMOS_POGate_Comb_length=100,  # Scalar

								  ## Inv1 PMOS
								  _Buf_CLKSamp_Inv_PMOS_ChannelWidth=400,  # Scalar
								  _Buf_CLKSamp_Inv_PMOS_POGate_Comb_length=100,  # Scalar

								  # Additional Buffer Between CLK_Source Input of Comparator And Output of Tree Buffer
								  ## InvChain Common
								  _Buf_CLKSrc_Pbody_NumCont=2,  # number
								  _Buf_CLKSrc_Nbody_NumCont=2,  # number
								  _Buf_CLKSrc_PMOSXvt2NMOSXvt=500,  # number
								  _Buf_CLKSrc_XvtTop2Pbody=None,  # number/None(Minimum)
								  _Buf_CLKSrc_Xvtdown2Nbody=None,  # number/None(Minimum)

								  ## Inverter Chain
								  ## Inv1 common
								  _Buf_CLKSrc_NumberofGate=[2, 4, 6],  # Vector
								  _Buf_CLKSrc_ChannelLength=30,  # Scalar
								  _Buf_CLKSrc_XVT='SLVT',  # 'SLVT'

								  ## Inv1 NMOS
								  _Buf_CLKSrc_Inv_NMOS_ChannelWidth=200,  # Scalar
								  _Buf_CLKSrc_Inv_NMOS_POGate_Comb_length=100,  # Scalar

								  ## Inv1 PMOS
								  _Buf_CLKSrc_Inv_PMOS_ChannelWidth=400,  # Scalar
								  _Buf_CLKSrc_Inv_PMOS_POGate_Comb_length=100,  # Scalar

								  # Additional Buffer Between Output of Comparator  And Input of Tree Buffer
								  ## InvChain Common
								  _Buf_CompOut_Pbody_NumCont=2,  # number
								  _Buf_CompOut_Nbody_NumCont=2,  # number
								  _Buf_CompOut_PMOSXvt2NMOSXvt=500,  # number
								  _Buf_CompOut_XvtTop2Pbody=None,  # number/None(Minimum)
								  _Buf_CompOut_Xvtdown2Nbody=None,  # number/None(Minimum)

								  ## Inv1 common
								  _Buf_CompOut_NumberofGate=[2, 4, 6],  # Vector
								  _Buf_CompOut_ChannelLength=30,  # Scalar
								  _Buf_CompOut_XVT='SLVT',  # 'SLVT'

								  ## Inv1 NMOS
								  _Buf_CompOut_Inv_NMOS_ChannelWidth=200,  # Scalar
								  _Buf_CompOut_Inv_NMOS_POGate_Comb_length=100,  # Scalar

								  ## Inv1 PMOS
								  _Buf_CompOut_Inv_PMOS_ChannelWidth=400,  # Scalar
								  _Buf_CompOut_Inv_PMOS_POGate_Comb_length=100,  # Scalar

								  # # Additional Buffer Between Output of CLKDout  And Input of Tree Buffer
								  # ## Inv1 common
								  # _Buf_CLKDout_NumberofGate=[2, 4, 6],  # Vector
								  # _Buf_CLKDout_ChannelLength=30,  # Scalar
								  # _Buf_CLKDout_XVT='SLVT',  # 'SLVT'
								  #
								  # ## Inv1 NMOS
								  # _Buf_CLKDout_Inv_NMOS_ChannelWidth=200,  # Scalar
								  # _Buf_CLKDout_Inv_NMOS_POGate_Comb_length=100,  # Scalar
								  #
								  # ## Inv1 PMOS
								  # _Buf_CLKDout_Inv_PMOS_ChannelWidth=400,  # Scalar
								  # _Buf_CLKDout_Inv_PMOS_POGate_Comb_length=100,  # Scalar

								  # # Element CDAC
								  _CDAC_LayoutOption=[5, 6],
								  _CDAC_ShieldingLayer=4,  # Poly:0, M1:1, M2:2 ...
								  _CDAC_MetalWidth=50,
								  _CDAC_MetalLength=1414,  # (8bit size: 1414/ 10bit size: 2800/ 12bit size: 4200)
								  _CDAC_MetalSpacing=50,

								  # #Unit Cap
								  _CDAC_NumOfElement=2,

								  # # Shielding & Top Connect node
								  _CDAC_ConnectLength=400,
								  _CDAC_ExtendLength=400,

								  # # Dummy Cap Option
								  _CDAC_DummyCap_TopBottomShort=False,  # False -> Bottom = GND
								  _CDAC_NumOfDummyCaps=3,  # Number of dummy cap(one side)

								  # # CommonCentroid With Driving node
								  _CDAC_CapArrayWDrivingNodeDistance=0,  # DRC Rule
								  _CDAC_DriveNodeDistance=400,  #
								  _CDAC_YWidth_Bottom_Hrz=50,

								  # Driver Sizing
								  _Driver_CommonCentroidPlacementIfCDACFolded=None,
								  _Driver_SizeByBit=[32, 16, 8, 4, 2],

								  # Driver(Inverter) NMOS
								  _Driver_NMOS_NumberofGate=1,  # number
								  _Driver_NMOS_ChannelWidth=340,
								  # number (8bit size: 340/ 10bit size: 680/ 12bit size: 1020)
								  _Driver_NMOS_Channellength=30,  # number
								  _Driver_NMOS_XVT='SLVT',  # 'XVT' ex)SLVT LVT RVT HVT

								  # Driver(Inverter) PMOS
								  _Driver_PMOS_NumberofGate=1,  # number
								  _Driver_PMOS_ChannelWidth=900,
								  # number (8bit size: 900/ 10bit size: 1800/ 12bit size: 2700)
								  _Driver_PMOS_Channellength=30,  # number
								  _Driver_PMOS_XVT='SLVT',  # 'XVT' ex)SLVT LVT RVT HVT
								  ############################################################################################################################################ Bootstrap Sampler

								  # Tr1 and Tr2
								  # Input/Output node
								  # INPUT node
								  _Samp_Inputnode_width=600,  # number
								  # OUTPUT node
								  _Samp_Outputnode_width=600,  # number

								  # Tr1
								  _Samp_Tr1_NumberofGate=2,  # number
								  _Samp_Tr1_ChannelWidth=300,  # number
								  _Samp_Tr1_ChannelLength=30,  # number
								  _Samp_Tr1_XVT='RVT',  # 'XVT' ex)SLVT LVT RVT HVT

								  # Tr2
								  _Samp_Tr2_NumberofGate=1,  # number
								  _Samp_Tr2_ChannelWidth=1000,  # number
								  _Samp_Tr2_ChannelLength=30,  # number
								  _Samp_Tr2_XVT='SLVT',  # 'XVT' ex)SLVT LVT RVT HVT

								  # Tr4
								  _Samp_Tr4_NumberofGate=2,  # number
								  _Samp_Tr4_ChannelWidth=500,  # number
								  _Samp_Tr4_ChannelLength=30,  # number
								  _Samp_Tr4_XVT='SLVT',  # 'XVT' ex)SLVT LVT RVT HVT

								  # Tr5 Tr7 Tr9
								  # PMOS: Tr5
								  _Samp_Tr5_NumberofGate=1,
								  _Samp_Tr5_ChannelWidth=1000,  # ref=1000
								  _Samp_Tr5_ChannelLength=30,
								  _Samp_Tr5_XVT='SLVT',

								  # PMOS: Tr7
								  _Samp_Tr7_NumberofGate=1,
								  _Samp_Tr7_ChannelWidth=1000,
								  _Samp_Tr7_ChannelLength=30,
								  _Samp_Tr7_XVT='SLVT',

								  # PMOS: Tr9
								  _Samp_Tr9_NumberofGate=2,
								  _Samp_Tr9_ChannelWidth=1000,  # ref = 1000
								  _Samp_Tr9_ChannelLength=30,
								  _Samp_Tr9_XVT='SLVT',

								  # Tr8
								  _Samp_Tr8_NumberofGate=2,  # number (ref:4)
								  _Samp_Tr8_ChannelWidth=500,  # number (ref:500)
								  _Samp_Tr8_ChannelLength=30,  # number (ref:30)
								  _Samp_Tr8_XVT='SLVT',  # 'XVT' ex)SLVT LVT RVT HVT

								  # Tr6 and Guardring
								  # Tr6
								  _Samp_Tr6_NumberofGate=1,  # number
								  _Samp_Tr6_ChannelWidth=1000,  # number
								  _Samp_Tr6_ChannelLength=30,  # number
								  _Samp_Tr6_XVT='SLVT',  # 'XVT' ex)SLVT LVT RVT HVT

								  # PMOS: Tr11 and Guardring
								  # Tr11
								  _Samp_Tr11_NumberofGate=2,
								  _Samp_Tr11_ChannelWidth=1000,
								  _Samp_Tr11_ChannelLength=30,
								  _Samp_Tr11_XVT='SLVT',

								  ## VddTieCell4
								  # VddTieCell4 NMOS
								  _Samp_Tie4N_NumberofGate=4,  # number
								  _Samp_Tie4N_ChannelWidth=250,  # number
								  _Samp_Tie4N_ChannelLength=30,  # number
								  _Samp_Tie4N_XVT='SLVT',  # 'XVT' ex)SLVT LVT RVT HVT

								  # VddTieCell4 PMOS
								  _Samp_Tie4P_NumberofGate=4,  # number
								  _Samp_Tie4P_ChannelWidth=500,  # number
								  _Samp_Tie4P_ChannelLength=30,  # number
								  _Samp_Tie4P_XVT='SLVT',  # 'XVT' ex)SLVT LVT RVT HVT

								  ## VddTieCell8
								  # VddTieCell8 NMOS
								  _Samp_Tie8N_NumberofGate=4,  # number
								  _Samp_Tie8N_ChannelWidth=250,  # number
								  _Samp_Tie8N_ChannelLength=30,  # number
								  _Samp_Tie8N_XVT='SLVT',  # 'XVT' ex)SLVT LVT RVT HVT

								  # VddTieCell8 PMOS
								  _Samp_Tie8P_NumberofGate=4,  # number
								  _Samp_Tie8P_ChannelWidth=500,  # number
								  _Samp_Tie8P_ChannelLength=30,  # number
								  _Samp_Tie8P_XVT='SLVT',  # 'XVT' ex)SLVT LVT RVT HVT

								  # Tr12
								  _Samp_Tr12_NumberofGate=1,  # number
								  _Samp_Tr12_ChannelWidth=1000,  # number
								  _Samp_Tr12_ChannelLength=30,  # number
								  _Samp_Tr12_XVT='SLVT',  # 'XVT' ex)SLVT LVT RVT HVT

								  # Tr3
								  _Samp_Tr3_NumberofGate=1,  # number
								  _Samp_Tr3_ChannelWidth=1000,  # number
								  _Samp_Tr3_ChannelLength=30,  # number
								  _Samp_Tr3_XVT='SLVT',  # 'XVT' ex)SLVT LVT RVT HVT

								  # Tr10 and Guardring
								  # Tr10
								  _Samp_Tr10_NumberofGate=1,  # number
								  _Samp_Tr10_ChannelWidth=1000,  # number
								  _Samp_Tr10_ChannelLength=30,  # number
								  _Samp_Tr10_XVT='SLVT',  # 'XVT' ex)SLVT LVT RVT HVT

								  # HDVNCAP_Array
								  _Samp_HDVNCAP_Length=6000,
								  _Samp_HDVNCAP_LayoutOption=[3, 4, 5, 6],
								  _Samp_HDVNCAP_NumFigPair=53,
								  _Samp_HDVNCAP_Array=3,  # number: 1xnumber
								  _Samp_HDVNCAP_Cbot_Ctop_metalwidth=1000,  # number
								  # Total HDVNCapSize = 601fF

								  ## BootStrapped Sampler CLKB Inverter
								  _CLKBInv_NMOS_NumberofGate=16,
								  _CLKBInv_NMOS_ChannelWidth=400,
								  _CLKBInv_NMOS_ChannelLength=30,
								  _CLKBInv_NMOS_XVT='SLVT',
								  _CLKBInv_NMOS_POGate_Comb_length=None,

								  _CLKBInv_PMOS_NumberofGate=16,
								  _CLKBInv_Inv_PMOS_ChannelWidth=800,
								  _CLKBInv_PMOS_ChannelLength=30,
								  _CLKBInv_PMOS_XVT='SLVT',
								  _CLKBInv_PMOS_POGate_Comb_length=None,

								  _CLKBInv_Pbody_NumCont=2,
								  _CLKBInv_XvtTop2Pbody=None,
								  _CLKBInv_Nbody_NumCont=2,
								  _CLKBInv_Xvtdown2Nbody=None,
								  _CLKBInv_PMOSXvt2NMOSXvt=500,

                                  # RDAC and Decoder
                                  # RDAC and Decoder delta X displacement for DRC
                                  _RDAC_displacement=-100,

                                  # RDAC and Decoder Size : Consider "_Decoder_RBit" and "_Unit_Num_EachStag_input" ex) [2, 8] --> 4 : 2*8 = 2**4
                                  _RDAC_Size=[2, 16],

                                  # RDAC
                                  # Guardring
                                  RDAC_Guard_NumCont = 2,

                                  # Poly Resister unit
                                  RDAC_ResWidth		= 2000,
                                  RDAC_ResLength		= 1500,
                                  RDAC_CONUMX			= None,
                                  RDAC_CONUMY			= 2,

                                  # Decoder
                                  # _Unit to Unit distance for DRC of routing
                                  _Decoder_Unit2UnitDist=400,  # number must be 100의 배수

                                  # RDAC Bit
                                  #_Decoder_RBit = 5,

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
                                  _Nand_NumberofGate      = [2 ,2],  # Number
                                  _Nand_ChannelLength     = [30 ,30],  # Number
                                  _Nand_POGate_ViaMxMx    = [[0, 1] ,[0, 1]],  # Ex) [1,5] -> ViaM1M5
                                  # Pulldown(NMOS)
                                  # Physical dimension
                                  _Nand_NMOS_ChannelWidth                 = [400 ,500],  # Number
                                  # Source_node setting
                                  _Nand_NMOS_Source_Via_Close2POpin_TF    = [False ,False],  # True/False --> First MOS
                                  # Pulldown(PMOS)
                                  # Physical dimension
                                  _Nand_PMOS_ChannelWidth                 = [800 ,480],  # Number
                                  # Nor( _Unit_Num_EachStag_input에서 2,4,6,7...번째 해당하는 nor 생성)
                                  # MOSFET
                                  # Common
                                  _Nor_ChannelLength      = [30 ,30],  # Number
                                  _Nor_POGate_ViaMxMx     = [[0, 1] ,[0, 1]],  # Ex) [1,5] -> ViaM1M5
                                  # Pulldown(NMOS)
                                  # Physical dimension
                                  _Nor_NMOS_ChannelWidth	= [400 ,800],      # Number
                                  _Nor_NMOS_NumberofGate  = [1 ,3],        # Number
                                  # Pulldown(PMOS)
                                  # Physical dimension
                                  _Nor_PMOS_ChannelWidth	= [800 ,1600],      # Number
                                  _Nor_PMOS_NumberofGate  = [2 ,7],        # Number
                                  # Source_node setting
                                  _Nor_PMOS_Source_Via_Close2POpin_TF     = [False ,False],  # True/False --> First MOS
                                  # Inv
                                  # Common
                                  _Inv_NumberofGate   = 1,
                                  _Inv_ChannelLength  = 30,
                                  # NMosfet
                                  # Physical dimension
                                  _Inv_NMOS_ChannelWidth	= 400,      # Number
                                  # Poly Gate setting
                                  # Poly Gate Via setting :
                                  _Inv_NMOS_POGate_ViaMxMx    = [0 ,1],  # Ex) [1,5] -> ViaM1M5 -----> Fixed
                                  # PMosfet
                                  # Physical dimension
                                  _Inv_PMOS_ChannelWidth=800,  # Number
                                  # Poly Gate setting
                                  # Poly Gate Via setting :
                                  _Inv_PMOS_POGate_ViaMxMx=[0, 1],  # Ex) [1,5] -> ViaM1M5 -----> Fixed
                                  # Xgate
                                  # Common
                                  _Xgate_NumberofGate=1,
                                  _Xgate_ChannelLength=30,
                                  # NMosfet
                                  # Physical dimension
                                  _Xgate_NMOS_ChannelWidth=400,  # Number
                                  # Poly Gate setting
                                  # Poly Gate Via setting :
                                  _Xgate_NMOS_POGate_ViaMxMx=[0, 1],  # Ex) [1,5] -> ViaM1M5 -----> Fixed
                                  # PMosfet
                                  # Physical dimension
                                  _Xgate_PMOS_ChannelWidth=800,  # Number
                                  # Poly Gate setting
                                  # Poly Gate Via setting :
                                  _Xgate_PMOS_POGate_ViaMxMx=[0, 1],  # Ex) [1,5] -> ViaM1M5 -----> Fixed

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
		
		
		## Pre-defined
		_Numofbit = _NumofCbit + _NumofRbit


		if _CDAC_Folding == True and _NumofCbit < 4:
			raise Exception("현재 ADC Generation code에서 CDAC Folding Option은 4Bit이상에서 사용 가능합니다.")

		print('###############################################')
		print('##                   {}Bit                   ##'.format(_Numofbit))
		print('##                 SAR Logic                 ##')
		print('##            Calculation_Start!!            ##')
		print('###############################################')

		_Caculation_Parameters1 = copy.deepcopy(L00_SARLogicWtComparator_KJH._SARLogicWtComparator._ParametersForDesignCalculation)
		## Define Calculation_Parameters ex) _Caculation_Parameters1['_NMOSPOWER_PbodyContact_1_Length']  = _NMOSPOWER_PbodyContact_1_Length
		_Caculation_Parameters1['_NumofBit'] = _Numofbit
		_Caculation_Parameters1['_Test_distance'] = _Test_distance
		_Caculation_Parameters1['_Routing_width'] = _Routing_width
		_Caculation_Parameters1['_Routing_distance'] = _Routing_distance

		_Caculation_Parameters1['_SARLogic_YWidthOfCLKSrc'] = _SARLogic_YWidthOfCLKSrc
		_Caculation_Parameters1['_SARLogic_SpaceBtwCLKSrcAndCLKSamp'] = _SARLogic_SpaceBtwCLKSrcAndCLKSamp
		_Caculation_Parameters1['_SARLogic_YWidthOfCLKSamp'] = _SARLogic_YWidthOfCLKSamp
		_Caculation_Parameters1['_SARLogic_YWidthOfCompOut'] = _SARLogic_YWidthOfCompOut
		_Caculation_Parameters1['_SARLogic_SpaceBtwCompOutAndCLKDout'] = _SARLogic_SpaceBtwCompOutAndCLKDout
		_Caculation_Parameters1['_SARLogic_YWidthOfCLKDout'] = _SARLogic_YWidthOfCLKDout
		## DFF Common
		_Caculation_Parameters1['_SARLogic_DFF_Pbody_NumCont'] = _SARLogic_DFF_Pbody_NumCont
		_Caculation_Parameters1['_SARLogic_DFF_Nbody_NumCont'] = _SARLogic_DFF_Nbody_NumCont
		_Caculation_Parameters1['_SARLogic_DFF_PMOSXvt2NMOSXvt'] = _SARLogic_DFF_PMOSXvt2NMOSXvt
		_Caculation_Parameters1['_SARLogic_DFF_XvtTop2Pbody'] = _SARLogic_DFF_XvtTop2Pbody
		_Caculation_Parameters1['_SARLogic_DFF_Xvtdown2Nbody'] = _SARLogic_DFF_Xvtdown2Nbody

		## Master Xgate1
		## Xgate NMOS
		_Caculation_Parameters1['_SARLogic_Mst_Xgate1_NMOS_NumberofGate'] = _SARLogic_Mst_Xgate1_NMOS_NumberofGate
		_Caculation_Parameters1['_SARLogic_Mst_Xgate1_NMOS_ChannelWidth'] = _SARLogic_Mst_Xgate1_NMOS_ChannelWidth
		_Caculation_Parameters1['_SARLogic_Mst_Xgate1_NMOS_ChannelLength'] = _SARLogic_Mst_Xgate1_NMOS_ChannelLength
		_Caculation_Parameters1['_SARLogic_Mst_Xgate1_NMOS_XVT'] = _SARLogic_Mst_Xgate1_NMOS_XVT
		_Caculation_Parameters1['_SARLogic_Mst_Xgate1_NMOS_POGate_Comb_length'] = _SARLogic_Mst_Xgate1_NMOS_POGate_Comb_length

		## Xgate PMOS
		_Caculation_Parameters1['_SARLogic_Mst_Xgate1_PMOS_NumberofGate'] = _SARLogic_Mst_Xgate1_PMOS_NumberofGate
		_Caculation_Parameters1['_SARLogic_Mst_Xgate1_PMOS_ChannelWidth'] = _SARLogic_Mst_Xgate1_PMOS_ChannelWidth
		_Caculation_Parameters1['_SARLogic_Mst_Xgate1_PMOS_ChannelLength'] = _SARLogic_Mst_Xgate1_PMOS_ChannelLength
		_Caculation_Parameters1['_SARLogic_Mst_Xgate1_PMOS_XVT'] = _SARLogic_Mst_Xgate1_PMOS_XVT
		_Caculation_Parameters1['_SARLogic_Mst_Xgate1_PMOS_POGate_Comb_length'] = _SARLogic_Mst_Xgate1_PMOS_POGate_Comb_length

		## Master Xgate2
		## Xgate NMOS
		_Caculation_Parameters1['_SARLogic_Mst_Xgate2_NMOS_NumberofGate'] = _SARLogic_Mst_Xgate2_NMOS_NumberofGate
		_Caculation_Parameters1['_SARLogic_Mst_Xgate2_NMOS_ChannelWidth'] = _SARLogic_Mst_Xgate2_NMOS_ChannelWidth
		_Caculation_Parameters1['_SARLogic_Mst_Xgate2_NMOS_ChannelLength'] = _SARLogic_Mst_Xgate2_NMOS_ChannelLength
		_Caculation_Parameters1['_SARLogic_Mst_Xgate2_NMOS_XVT'] = _SARLogic_Mst_Xgate2_NMOS_XVT
		_Caculation_Parameters1['_SARLogic_Mst_Xgate2_NMOS_POGate_Comb_length'] = _SARLogic_Mst_Xgate2_NMOS_POGate_Comb_length

		## Xgate PMOS
		_Caculation_Parameters1['_SARLogic_Mst_Xgate2_PMOS_NumberofGate'] = _SARLogic_Mst_Xgate2_PMOS_NumberofGate
		_Caculation_Parameters1['_SARLogic_Mst_Xgate2_PMOS_ChannelWidth'] = _SARLogic_Mst_Xgate2_PMOS_ChannelWidth
		_Caculation_Parameters1['_SARLogic_Mst_Xgate2_PMOS_ChannelLength'] = _SARLogic_Mst_Xgate2_PMOS_ChannelLength
		_Caculation_Parameters1['_SARLogic_Mst_Xgate2_PMOS_XVT'] = _SARLogic_Mst_Xgate2_PMOS_XVT
		_Caculation_Parameters1['_SARLogic_Mst_Xgate2_PMOS_POGate_Comb_length'] = _SARLogic_Mst_Xgate2_PMOS_POGate_Comb_length

		## Master Nor1
		## NMOS common
		_Caculation_Parameters1['_SARLogic_Mst_Nor1_NMOS_XVT'] = _SARLogic_Mst_Nor1_NMOS_XVT

		## Nor1 NMOSA
		_Caculation_Parameters1['_SARLogic_Mst_Nor1_NMOSA_NumberofGate'] = _SARLogic_Mst_Nor1_NMOSA_NumberofGate
		_Caculation_Parameters1['_SARLogic_Mst_Nor1_NMOSA_ChannelWidth'] = _SARLogic_Mst_Nor1_NMOSA_ChannelWidth
		_Caculation_Parameters1['_SARLogic_Mst_Nor1_NMOSA_ChannelLength'] = _SARLogic_Mst_Nor1_NMOSA_ChannelLength
		_Caculation_Parameters1['_SARLogic_Mst_Nor1_NMOSA_POGate_Comb_length'] = _SARLogic_Mst_Nor1_NMOSA_POGate_Comb_length

		## Nor1 NMOSB
		_Caculation_Parameters1['_SARLogic_Mst_Nor1_NMOSB_NumberofGate'] = _SARLogic_Mst_Nor1_NMOSB_NumberofGate
		_Caculation_Parameters1['_SARLogic_Mst_Nor1_NMOSB_ChannelWidth'] = _SARLogic_Mst_Nor1_NMOSB_ChannelWidth
		_Caculation_Parameters1['_SARLogic_Mst_Nor1_NMOSB_ChannelLength'] = _SARLogic_Mst_Nor1_NMOSB_ChannelLength
		_Caculation_Parameters1['_SARLogic_Mst_Nor1_NMOSB_POGate_Comb_length'] = _SARLogic_Mst_Nor1_NMOSB_POGate_Comb_length

		## PMOS common
		_Caculation_Parameters1['_SARLogic_Mst_Nor1_PMOS_XVT'] = _SARLogic_Mst_Nor1_PMOS_XVT

		## Nor1 PMOSA
		_Caculation_Parameters1['_SARLogic_Mst_Nor1_PMOSA_NumberofGate'] = _SARLogic_Mst_Nor1_PMOSA_NumberofGate
		_Caculation_Parameters1['_SARLogic_Mst_Nor1_PMOSA_ChannelWidth'] = _SARLogic_Mst_Nor1_PMOSA_ChannelWidth
		_Caculation_Parameters1['_SARLogic_Mst_Nor1_PMOSA_ChannelLength'] = _SARLogic_Mst_Nor1_PMOSA_ChannelLength
		_Caculation_Parameters1['_SARLogic_Mst_Nor1_PMOSA_POGate_Comb_length'] = _SARLogic_Mst_Nor1_PMOSA_POGate_Comb_length

		## Nor1 PMOSB
		_Caculation_Parameters1['_SARLogic_Mst_Nor1_PMOSB_NumberofGate'] = _SARLogic_Mst_Nor1_PMOSB_NumberofGate
		_Caculation_Parameters1['_SARLogic_Mst_Nor1_PMOSB_ChannelWidth'] = _SARLogic_Mst_Nor1_PMOSB_ChannelWidth
		_Caculation_Parameters1['_SARLogic_Mst_Nor1_PMOSB_ChannelLength'] = _SARLogic_Mst_Nor1_PMOSB_ChannelLength
		_Caculation_Parameters1['_SARLogic_Mst_Nor1_PMOSB_POGate_Comb_length'] = _SARLogic_Mst_Nor1_PMOSB_POGate_Comb_length

		## Master Nor2
		## NMOS common
		_Caculation_Parameters1['_SARLogic_Mst_Nor2_NMOS_XVT'] = _SARLogic_Mst_Nor2_NMOS_XVT

		## Nor2 NMOSA
		_Caculation_Parameters1['_SARLogic_Mst_Nor2_NMOSA_NumberofGate'] = _SARLogic_Mst_Nor2_NMOSA_NumberofGate
		_Caculation_Parameters1['_SARLogic_Mst_Nor2_NMOSA_ChannelWidth'] = _SARLogic_Mst_Nor2_NMOSA_ChannelWidth
		_Caculation_Parameters1['_SARLogic_Mst_Nor2_NMOSA_ChannelLength'] = _SARLogic_Mst_Nor2_NMOSA_ChannelLength
		_Caculation_Parameters1['_SARLogic_Mst_Nor2_NMOSA_POGate_Comb_length'] = _SARLogic_Mst_Nor2_NMOSA_POGate_Comb_length

		## Nor2 NMOSB
		_Caculation_Parameters1['_SARLogic_Mst_Nor2_NMOSB_NumberofGate'] = _SARLogic_Mst_Nor2_NMOSB_NumberofGate
		_Caculation_Parameters1['_SARLogic_Mst_Nor2_NMOSB_ChannelWidth'] = _SARLogic_Mst_Nor2_NMOSB_ChannelWidth
		_Caculation_Parameters1['_SARLogic_Mst_Nor2_NMOSB_ChannelLength'] = _SARLogic_Mst_Nor2_NMOSB_ChannelLength
		_Caculation_Parameters1['_SARLogic_Mst_Nor2_NMOSB_POGate_Comb_length'] = _SARLogic_Mst_Nor2_NMOSB_POGate_Comb_length

		## PMOS common
		_Caculation_Parameters1['_SARLogic_Mst_Nor2_PMOS_XVT'] = _SARLogic_Mst_Nor2_PMOS_XVT

		## Nor2 PMOSA
		_Caculation_Parameters1['_SARLogic_Mst_Nor2_PMOSA_NumberofGate'] = _SARLogic_Mst_Nor2_PMOSA_NumberofGate
		_Caculation_Parameters1['_SARLogic_Mst_Nor2_PMOSA_ChannelWidth'] = _SARLogic_Mst_Nor2_PMOSA_ChannelWidth
		_Caculation_Parameters1['_SARLogic_Mst_Nor2_PMOSA_ChannelLength'] = _SARLogic_Mst_Nor2_PMOSA_ChannelLength
		_Caculation_Parameters1['_SARLogic_Mst_Nor2_PMOSA_POGate_Comb_length'] = _SARLogic_Mst_Nor2_PMOSA_POGate_Comb_length

		## Nor2 PMOSB
		_Caculation_Parameters1['_SARLogic_Mst_Nor2_PMOSB_NumberofGate'] = _SARLogic_Mst_Nor2_PMOSB_NumberofGate
		_Caculation_Parameters1['_SARLogic_Mst_Nor2_PMOSB_ChannelWidth'] = _SARLogic_Mst_Nor2_PMOSB_ChannelWidth
		_Caculation_Parameters1['_SARLogic_Mst_Nor2_PMOSB_ChannelLength'] = _SARLogic_Mst_Nor2_PMOSB_ChannelLength
		_Caculation_Parameters1['_SARLogic_Mst_Nor2_PMOSB_POGate_Comb_length'] = _SARLogic_Mst_Nor2_PMOSB_POGate_Comb_length

		## Master Inv1
		## Xgate NMOS
		_Caculation_Parameters1['_SARLogic_Mst_Inv1_NMOS_NumberofGate'] = _SARLogic_Mst_Inv1_NMOS_NumberofGate
		_Caculation_Parameters1['_SARLogic_Mst_Inv1_NMOS_ChannelWidth'] = _SARLogic_Mst_Inv1_NMOS_ChannelWidth
		_Caculation_Parameters1['_SARLogic_Mst_Inv1_NMOS_ChannelLength'] = _SARLogic_Mst_Inv1_NMOS_ChannelLength
		_Caculation_Parameters1['_SARLogic_Mst_Inv1_NMOS_XVT'] = _SARLogic_Mst_Inv1_NMOS_XVT
		_Caculation_Parameters1['_SARLogic_Mst_Inv1_NMOS_POGate_Comb_length'] = _SARLogic_Mst_Inv1_NMOS_POGate_Comb_length

		## Xgate PMOS
		_Caculation_Parameters1['_SARLogic_Mst_Inv1_PMOS_NumberofGate'] = _SARLogic_Mst_Inv1_PMOS_NumberofGate
		_Caculation_Parameters1['_SARLogic_Mst_Inv1_PMOS_ChannelWidth'] = _SARLogic_Mst_Inv1_PMOS_ChannelWidth
		_Caculation_Parameters1['_SARLogic_Mst_Inv1_PMOS_ChannelLength'] = _SARLogic_Mst_Inv1_PMOS_ChannelLength
		_Caculation_Parameters1['_SARLogic_Mst_Inv1_PMOS_XVT'] = _SARLogic_Mst_Inv1_PMOS_XVT
		_Caculation_Parameters1['_SARLogic_Mst_Inv1_PMOS_POGate_Comb_length'] = _SARLogic_Mst_Inv1_PMOS_POGate_Comb_length

		## Master Inv2 : Set driver
		## Xgate NMOS
		_Caculation_Parameters1['_SARLogic_Mst_Inv2_NMOS_NumberofGate'] = _SARLogic_Mst_Inv2_NMOS_NumberofGate
		_Caculation_Parameters1['_SARLogic_Mst_Inv2_NMOS_ChannelWidth'] = _SARLogic_Mst_Inv2_NMOS_ChannelWidth
		_Caculation_Parameters1['_SARLogic_Mst_Inv2_NMOS_ChannelLength'] = _SARLogic_Mst_Inv2_NMOS_ChannelLength
		_Caculation_Parameters1['_SARLogic_Mst_Inv2_NMOS_XVT'] = _SARLogic_Mst_Inv2_NMOS_XVT
		_Caculation_Parameters1['_SARLogic_Mst_Inv2_NMOS_POGate_Comb_length'] = _SARLogic_Mst_Inv2_NMOS_POGate_Comb_length

		## Xgate PMOS
		_Caculation_Parameters1['_SARLogic_Mst_Inv2_PMOS_NumberofGate'] = _SARLogic_Mst_Inv2_PMOS_NumberofGate
		_Caculation_Parameters1['_SARLogic_Mst_Inv2_PMOS_ChannelWidth'] = _SARLogic_Mst_Inv2_PMOS_ChannelWidth
		_Caculation_Parameters1['_SARLogic_Mst_Inv2_PMOS_ChannelLength'] = _SARLogic_Mst_Inv2_PMOS_ChannelLength
		_Caculation_Parameters1['_SARLogic_Mst_Inv2_PMOS_XVT'] = _SARLogic_Mst_Inv2_PMOS_XVT
		_Caculation_Parameters1['_SARLogic_Mst_Inv2_PMOS_POGate_Comb_length'] = _SARLogic_Mst_Inv2_PMOS_POGate_Comb_length

		## Master Inv3 : Clock driver
		## Xgate NMOS
		_Caculation_Parameters1['_SARLogic_Mst_Inv3_NMOS_NumberofGate'] = _SARLogic_Mst_Inv3_NMOS_NumberofGate
		_Caculation_Parameters1['_SARLogic_Mst_Inv3_NMOS_ChannelWidth'] = _SARLogic_Mst_Inv3_NMOS_ChannelWidth
		_Caculation_Parameters1['_SARLogic_Mst_Inv3_NMOS_ChannelLength'] = _SARLogic_Mst_Inv3_NMOS_ChannelLength
		_Caculation_Parameters1['_SARLogic_Mst_Inv3_NMOS_XVT'] = _SARLogic_Mst_Inv3_NMOS_XVT
		_Caculation_Parameters1['_SARLogic_Mst_Inv3_NMOS_POGate_Comb_length'] = _SARLogic_Mst_Inv3_NMOS_POGate_Comb_length

		## Xgate PMOS
		_Caculation_Parameters1['_SARLogic_Mst_Inv3_PMOS_NumberofGate'] = _SARLogic_Mst_Inv3_PMOS_NumberofGate
		_Caculation_Parameters1['_SARLogic_Mst_Inv3_PMOS_ChannelWidth'] = _SARLogic_Mst_Inv3_PMOS_ChannelWidth
		_Caculation_Parameters1['_SARLogic_Mst_Inv3_PMOS_ChannelLength'] = _SARLogic_Mst_Inv3_PMOS_ChannelLength
		_Caculation_Parameters1['_SARLogic_Mst_Inv3_PMOS_XVT'] = _SARLogic_Mst_Inv3_PMOS_XVT
		_Caculation_Parameters1['_SARLogic_Mst_Inv3_PMOS_POGate_Comb_length'] = _SARLogic_Mst_Inv3_PMOS_POGate_Comb_length

		## Slave Xgate1
		## Xgate NMOS
		_Caculation_Parameters1['_SARLogic_Slv_Xgate1_NMOS_NumberofGate'] = _SARLogic_Slv_Xgate1_NMOS_NumberofGate
		_Caculation_Parameters1['_SARLogic_Slv_Xgate1_NMOS_ChannelWidth'] = _SARLogic_Slv_Xgate1_NMOS_ChannelWidth
		_Caculation_Parameters1['_SARLogic_Slv_Xgate1_NMOS_ChannelLength'] = _SARLogic_Slv_Xgate1_NMOS_ChannelLength
		_Caculation_Parameters1['_SARLogic_Slv_Xgate1_NMOS_XVT'] = _SARLogic_Slv_Xgate1_NMOS_XVT
		_Caculation_Parameters1['_SARLogic_Slv_Xgate1_NMOS_POGate_Comb_length'] = _SARLogic_Slv_Xgate1_NMOS_POGate_Comb_length

		## Xgate PMOS
		_Caculation_Parameters1['_SARLogic_Slv_Xgate1_PMOS_NumberofGate'] = _SARLogic_Slv_Xgate1_PMOS_NumberofGate
		_Caculation_Parameters1['_SARLogic_Slv_Xgate1_PMOS_ChannelWidth'] = _SARLogic_Slv_Xgate1_PMOS_ChannelWidth
		_Caculation_Parameters1['_SARLogic_Slv_Xgate1_PMOS_ChannelLength'] = _SARLogic_Slv_Xgate1_PMOS_ChannelLength
		_Caculation_Parameters1['_SARLogic_Slv_Xgate1_PMOS_XVT'] = _SARLogic_Slv_Xgate1_PMOS_XVT
		_Caculation_Parameters1['_SARLogic_Slv_Xgate1_PMOS_POGate_Comb_length'] = _SARLogic_Slv_Xgate1_PMOS_POGate_Comb_length

		## Slave Xgate2
		## Xgate NMOS
		_Caculation_Parameters1['_SARLogic_Slv_Xgate2_NMOS_NumberofGate'] = _SARLogic_Slv_Xgate2_NMOS_NumberofGate
		_Caculation_Parameters1['_SARLogic_Slv_Xgate2_NMOS_ChannelWidth'] = _SARLogic_Slv_Xgate2_NMOS_ChannelWidth
		_Caculation_Parameters1['_SARLogic_Slv_Xgate2_NMOS_ChannelLength'] = _SARLogic_Slv_Xgate2_NMOS_ChannelLength
		_Caculation_Parameters1['_SARLogic_Slv_Xgate2_NMOS_XVT'] = _SARLogic_Slv_Xgate2_NMOS_XVT
		_Caculation_Parameters1['_SARLogic_Slv_Xgate2_NMOS_POGate_Comb_length'] = _SARLogic_Slv_Xgate2_NMOS_POGate_Comb_length

		## Xgate PMOS
		_Caculation_Parameters1['_SARLogic_Slv_Xgate2_PMOS_NumberofGate'] = _SARLogic_Slv_Xgate2_PMOS_NumberofGate
		_Caculation_Parameters1['_SARLogic_Slv_Xgate2_PMOS_ChannelWidth'] = _SARLogic_Slv_Xgate2_PMOS_ChannelWidth
		_Caculation_Parameters1['_SARLogic_Slv_Xgate2_PMOS_ChannelLength'] = _SARLogic_Slv_Xgate2_PMOS_ChannelLength
		_Caculation_Parameters1['_SARLogic_Slv_Xgate2_PMOS_XVT'] = _SARLogic_Slv_Xgate2_PMOS_XVT
		_Caculation_Parameters1['_SARLogic_Slv_Xgate2_PMOS_POGate_Comb_length'] = _SARLogic_Slv_Xgate2_PMOS_POGate_Comb_length

		## Slave Nor1
		## NMOS common
		_Caculation_Parameters1['_SARLogic_Slv_Nor1_NMOS_XVT'] = _SARLogic_Slv_Nor1_NMOS_XVT

		## Nor1 NMOSA
		_Caculation_Parameters1['_SARLogic_Slv_Nor1_NMOSA_NumberofGate'] = _SARLogic_Slv_Nor1_NMOSA_NumberofGate
		_Caculation_Parameters1['_SARLogic_Slv_Nor1_NMOSA_ChannelWidth'] = _SARLogic_Slv_Nor1_NMOSA_ChannelWidth
		_Caculation_Parameters1['_SARLogic_Slv_Nor1_NMOSA_ChannelLength'] = _SARLogic_Slv_Nor1_NMOSA_ChannelLength
		_Caculation_Parameters1['_SARLogic_Slv_Nor1_NMOSA_POGate_Comb_length'] = _SARLogic_Slv_Nor1_NMOSA_POGate_Comb_length

		## Nor1 NMOSB
		_Caculation_Parameters1['_SARLogic_Slv_Nor1_NMOSB_NumberofGate'] = _SARLogic_Slv_Nor1_NMOSB_NumberofGate
		_Caculation_Parameters1['_SARLogic_Slv_Nor1_NMOSB_ChannelWidth'] = _SARLogic_Slv_Nor1_NMOSB_ChannelWidth
		_Caculation_Parameters1['_SARLogic_Slv_Nor1_NMOSB_ChannelLength'] = _SARLogic_Slv_Nor1_NMOSB_ChannelLength
		_Caculation_Parameters1['_SARLogic_Slv_Nor1_NMOSB_POGate_Comb_length'] = _SARLogic_Slv_Nor1_NMOSB_POGate_Comb_length

		## PMOS common
		_Caculation_Parameters1['_SARLogic_Slv_Nor1_PMOS_XVT'] = _SARLogic_Slv_Nor1_PMOS_XVT

		## Nor1 PMOSA
		_Caculation_Parameters1['_SARLogic_Slv_Nor1_PMOSA_NumberofGate'] = _SARLogic_Slv_Nor1_PMOSA_NumberofGate
		_Caculation_Parameters1['_SARLogic_Slv_Nor1_PMOSA_ChannelWidth'] = _SARLogic_Slv_Nor1_PMOSA_ChannelWidth
		_Caculation_Parameters1['_SARLogic_Slv_Nor1_PMOSA_ChannelLength'] = _SARLogic_Slv_Nor1_PMOSA_ChannelLength
		_Caculation_Parameters1['_SARLogic_Slv_Nor1_PMOSA_POGate_Comb_length'] = _SARLogic_Slv_Nor1_PMOSA_POGate_Comb_length

		## Nor1 PMOSB
		_Caculation_Parameters1['_SARLogic_Slv_Nor1_PMOSB_NumberofGate'] = _SARLogic_Slv_Nor1_PMOSB_NumberofGate
		_Caculation_Parameters1['_SARLogic_Slv_Nor1_PMOSB_ChannelWidth'] = _SARLogic_Slv_Nor1_PMOSB_ChannelWidth
		_Caculation_Parameters1['_SARLogic_Slv_Nor1_PMOSB_ChannelLength'] = _SARLogic_Slv_Nor1_PMOSB_ChannelLength
		_Caculation_Parameters1['_SARLogic_Slv_Nor1_PMOSB_POGate_Comb_length'] = _SARLogic_Slv_Nor1_PMOSB_POGate_Comb_length

		## Slave Nor2
		## NMOS common
		_Caculation_Parameters1['_SARLogic_Slv_Nor2_NMOS_XVT'] = _SARLogic_Slv_Nor2_NMOS_XVT

		## Nor2 NMOSA
		_Caculation_Parameters1['_SARLogic_Slv_Nor2_NMOSA_NumberofGate'] = _SARLogic_Slv_Nor2_NMOSA_NumberofGate
		_Caculation_Parameters1['_SARLogic_Slv_Nor2_NMOSA_ChannelWidth'] = _SARLogic_Slv_Nor2_NMOSA_ChannelWidth
		_Caculation_Parameters1['_SARLogic_Slv_Nor2_NMOSA_ChannelLength'] = _SARLogic_Slv_Nor2_NMOSA_ChannelLength
		_Caculation_Parameters1['_SARLogic_Slv_Nor2_NMOSA_POGate_Comb_length'] = _SARLogic_Slv_Nor2_NMOSA_POGate_Comb_length

		## Nor2 NMOSB
		_Caculation_Parameters1['_SARLogic_Slv_Nor2_NMOSB_NumberofGate'] = _SARLogic_Slv_Nor2_NMOSB_NumberofGate
		_Caculation_Parameters1['_SARLogic_Slv_Nor2_NMOSB_ChannelWidth'] = _SARLogic_Slv_Nor2_NMOSB_ChannelWidth
		_Caculation_Parameters1['_SARLogic_Slv_Nor2_NMOSB_ChannelLength'] = _SARLogic_Slv_Nor2_NMOSB_ChannelLength
		_Caculation_Parameters1['_SARLogic_Slv_Nor2_NMOSB_POGate_Comb_length'] = _SARLogic_Slv_Nor2_NMOSB_POGate_Comb_length

		## PMOS common
		_Caculation_Parameters1['_SARLogic_Slv_Nor2_PMOS_XVT'] = _SARLogic_Slv_Nor2_PMOS_XVT

		## Nor2 PMOSA
		_Caculation_Parameters1['_SARLogic_Slv_Nor2_PMOSA_NumberofGate'] = _SARLogic_Slv_Nor2_PMOSA_NumberofGate
		_Caculation_Parameters1['_SARLogic_Slv_Nor2_PMOSA_ChannelWidth'] = _SARLogic_Slv_Nor2_PMOSA_ChannelWidth
		_Caculation_Parameters1['_SARLogic_Slv_Nor2_PMOSA_ChannelLength'] = _SARLogic_Slv_Nor2_PMOSA_ChannelLength
		_Caculation_Parameters1['_SARLogic_Slv_Nor2_PMOSA_POGate_Comb_length'] = _SARLogic_Slv_Nor2_PMOSA_POGate_Comb_length

		## Nor2 PMOSB
		_Caculation_Parameters1['_SARLogic_Slv_Nor2_PMOSB_NumberofGate'] = _SARLogic_Slv_Nor2_PMOSB_NumberofGate
		_Caculation_Parameters1['_SARLogic_Slv_Nor2_PMOSB_ChannelWidth'] = _SARLogic_Slv_Nor2_PMOSB_ChannelWidth
		_Caculation_Parameters1['_SARLogic_Slv_Nor2_PMOSB_ChannelLength'] = _SARLogic_Slv_Nor2_PMOSB_ChannelLength
		_Caculation_Parameters1['_SARLogic_Slv_Nor2_PMOSB_POGate_Comb_length'] = _SARLogic_Slv_Nor2_PMOSB_POGate_Comb_length

		## Slave Inv1 : ReSet pre-driver
		## Xgate NMOS
		_Caculation_Parameters1['_SARLogic_Slv_Inv1_NMOS_NumberofGate'] = _SARLogic_Slv_Inv1_NMOS_NumberofGate
		_Caculation_Parameters1['_SARLogic_Slv_Inv1_NMOS_ChannelWidth'] = _SARLogic_Slv_Inv1_NMOS_ChannelWidth
		_Caculation_Parameters1['_SARLogic_Slv_Inv1_NMOS_ChannelLength'] = _SARLogic_Slv_Inv1_NMOS_ChannelLength
		_Caculation_Parameters1['_SARLogic_Slv_Inv1_NMOS_XVT'] = _SARLogic_Slv_Inv1_NMOS_XVT
		_Caculation_Parameters1['_SARLogic_Slv_Inv1_NMOS_POGate_Comb_length'] = _SARLogic_Slv_Inv1_NMOS_POGate_Comb_length

		## Xgate PMOS
		_Caculation_Parameters1['_SARLogic_Slv_Inv1_PMOS_NumberofGate'] = _SARLogic_Slv_Inv1_PMOS_NumberofGate
		_Caculation_Parameters1['_SARLogic_Slv_Inv1_PMOS_ChannelWidth'] = _SARLogic_Slv_Inv1_PMOS_ChannelWidth
		_Caculation_Parameters1['_SARLogic_Slv_Inv1_PMOS_ChannelLength'] = _SARLogic_Slv_Inv1_PMOS_ChannelLength
		_Caculation_Parameters1['_SARLogic_Slv_Inv1_PMOS_XVT'] = _SARLogic_Slv_Inv1_PMOS_XVT
		_Caculation_Parameters1['_SARLogic_Slv_Inv1_PMOS_POGate_Comb_length'] = _SARLogic_Slv_Inv1_PMOS_POGate_Comb_length

		## Slave Inv2 : ReSet driver
		## Xgate NMOS
		_Caculation_Parameters1['_SARLogic_Slv_Inv2_NMOS_NumberofGate'] = _SARLogic_Slv_Inv2_NMOS_NumberofGate
		_Caculation_Parameters1['_SARLogic_Slv_Inv2_NMOS_ChannelWidth'] = _SARLogic_Slv_Inv2_NMOS_ChannelWidth
		_Caculation_Parameters1['_SARLogic_Slv_Inv2_NMOS_ChannelLength'] = _SARLogic_Slv_Inv2_NMOS_ChannelLength
		_Caculation_Parameters1['_SARLogic_Slv_Inv2_NMOS_XVT'] = _SARLogic_Slv_Inv2_NMOS_XVT
		_Caculation_Parameters1['_SARLogic_Slv_Inv2_NMOS_POGate_Comb_length'] = _SARLogic_Slv_Inv2_NMOS_POGate_Comb_length

		## Xgate PMOS
		_Caculation_Parameters1['_SARLogic_Slv_Inv2_PMOS_NumberofGate'] = _SARLogic_Slv_Inv2_PMOS_NumberofGate
		_Caculation_Parameters1['_SARLogic_Slv_Inv2_PMOS_ChannelWidth'] = _SARLogic_Slv_Inv2_PMOS_ChannelWidth
		_Caculation_Parameters1['_SARLogic_Slv_Inv2_PMOS_ChannelLength'] = _SARLogic_Slv_Inv2_PMOS_ChannelLength
		_Caculation_Parameters1['_SARLogic_Slv_Inv2_PMOS_XVT'] = _SARLogic_Slv_Inv2_PMOS_XVT
		_Caculation_Parameters1['_SARLogic_Slv_Inv2_PMOS_POGate_Comb_length'] = _SARLogic_Slv_Inv2_PMOS_POGate_Comb_length

		## Slave Inv3 : Qb driver
		## Xgate NMOS
		_Caculation_Parameters1['_SARLogic_Slv_Inv3_NMOS_NumberofGate'] = _SARLogic_Slv_Inv3_NMOS_NumberofGate
		_Caculation_Parameters1['_SARLogic_Slv_Inv3_NMOS_ChannelWidth'] = _SARLogic_Slv_Inv3_NMOS_ChannelWidth
		_Caculation_Parameters1['_SARLogic_Slv_Inv3_NMOS_ChannelLength'] = _SARLogic_Slv_Inv3_NMOS_ChannelLength
		_Caculation_Parameters1['_SARLogic_Slv_Inv3_NMOS_XVT'] = _SARLogic_Slv_Inv3_NMOS_XVT
		_Caculation_Parameters1['_SARLogic_Slv_Inv3_NMOS_POGate_Comb_length'] = _SARLogic_Slv_Inv3_NMOS_POGate_Comb_length

		## Xgate PMOS
		_Caculation_Parameters1['_SARLogic_Slv_Inv3_PMOS_NumberofGate'] = _SARLogic_Slv_Inv3_PMOS_NumberofGate
		_Caculation_Parameters1['_SARLogic_Slv_Inv3_PMOS_ChannelWidth'] = _SARLogic_Slv_Inv3_PMOS_ChannelWidth
		_Caculation_Parameters1['_SARLogic_Slv_Inv3_PMOS_ChannelLength'] = _SARLogic_Slv_Inv3_PMOS_ChannelLength
		_Caculation_Parameters1['_SARLogic_Slv_Inv3_PMOS_XVT'] = _SARLogic_Slv_Inv3_PMOS_XVT
		_Caculation_Parameters1['_SARLogic_Slv_Inv3_PMOS_POGate_Comb_length'] = _SARLogic_Slv_Inv3_PMOS_POGate_Comb_length

		## CLK Buf Tree Top
		_Caculation_Parameters1['_SARLogic_CLKBufTreeTop_NumOfStage'] = _SARLogic_CLKBufTreeTop_NumOfStage
		_Caculation_Parameters1['_SARLogic_CLKBufTreeTop_CLKSampBuf_SizeByStage'] = _SARLogic_CLKBufTreeTop_CLKSampBuf_SizeByStage
		_Caculation_Parameters1['_SARLogic_CLKBufTreeTop_CLKSrcBuf_SizeByStage'] = _SARLogic_CLKBufTreeTop_CLKSrcBuf_SizeByStage
		_Caculation_Parameters1['_SARLogic_CLKBufTreeTop_XOffSet'] = _SARLogic_CLKBufTreeTop_XOffSet

		_Caculation_Parameters1['_SARLogic_CLKBufTreeTop_Inv_NMOS_ChannelWidth'] = _SARLogic_CLKBufTreeTop_Inv_NMOS_ChannelWidth
		_Caculation_Parameters1['_SARLogic_CLKBufTreeTop_Inv_NMOS_ChannelLength'] = _SARLogic_CLKBufTreeTop_Inv_NMOS_ChannelLength
		_Caculation_Parameters1['_SARLogic_CLKBufTreeTop_Inv_NMOS_NumberofGate'] = _SARLogic_CLKBufTreeTop_Inv_NMOS_NumberofGate
		_Caculation_Parameters1['_SARLogic_CLKBufTreeTop_Inv_NMOS_XVT'] = _SARLogic_CLKBufTreeTop_Inv_NMOS_XVT
		_Caculation_Parameters1['_SARLogic_CLKBufTreeTop_Inv_NMOS_POGate_Comb_length'] = _SARLogic_CLKBufTreeTop_Inv_NMOS_POGate_Comb_length

		_Caculation_Parameters1['_SARLogic_CLKBufTreeTop_Inv_PMOS_ChannelWidth'] = _SARLogic_CLKBufTreeTop_Inv_PMOS_ChannelWidth
		_Caculation_Parameters1['_SARLogic_CLKBufTreeTop_Inv_PMOS_ChannelLength'] = _SARLogic_CLKBufTreeTop_Inv_PMOS_ChannelLength
		_Caculation_Parameters1['_SARLogic_CLKBufTreeTop_Inv_PMOS_NumberofGate'] = _SARLogic_CLKBufTreeTop_Inv_PMOS_NumberofGate
		_Caculation_Parameters1['_SARLogic_CLKBufTreeTop_Inv_PMOS_XVT'] = _SARLogic_CLKBufTreeTop_Inv_PMOS_XVT
		_Caculation_Parameters1['_SARLogic_CLKBufTreeTop_Inv_PMOS_POGate_Comb_length'] = _SARLogic_CLKBufTreeTop_Inv_PMOS_POGate_Comb_length

		_Caculation_Parameters1['_SARLogic_CLKBufTreeTop_NMOS_Pbody_NumCont'] = _SARLogic_CLKBufTreeTop_NMOS_Pbody_NumCont
		_Caculation_Parameters1['_SARLogic_CLKBufTreeTop_NMOS_Pbody_XvtTop2Pbody'] = _SARLogic_CLKBufTreeTop_NMOS_Pbody_XvtTop2Pbody
		_Caculation_Parameters1['_SARLogic_CLKBufTreeTop_PMOS_Nbody_NumCont'] = _SARLogic_CLKBufTreeTop_PMOS_Nbody_NumCont
		_Caculation_Parameters1['_SARLogic_CLKBufTreeTop_PMOS_Nbody_Xvtdown2Nbody'] = _SARLogic_CLKBufTreeTop_PMOS_Nbody_Xvtdown2Nbody
		_Caculation_Parameters1['_SARLogic_CLKBufTreeTop_PMOSXvt2NMOSXvt'] = _SARLogic_CLKBufTreeTop_PMOSXvt2NMOSXvt

		## CLK Buf Tree Bot
		_Caculation_Parameters1['_SARLogic_CLKBufTreeBot_NumOfStage'] = _SARLogic_CLKBufTreeBot_NumOfStage
		_Caculation_Parameters1['_SARLogic_CLKBufTreeBot_CompOutBuf_SizeByStage'] = _SARLogic_CLKBufTreeBot_CompOutBuf_SizeByStage
		_Caculation_Parameters1['_SARLogic_CLKBufTreeBot_CLKDoutBuf_SizeByStage'] = _SARLogic_CLKBufTreeBot_CLKDoutBuf_SizeByStage
		_Caculation_Parameters1['_SARLogic_CLKBufTreeBot_XOffSet'] = _SARLogic_CLKBufTreeBot_XOffSet

		_Caculation_Parameters1['_SARLogic_CLKBufTreeBot_Inv_NMOS_ChannelWidth'] = _SARLogic_CLKBufTreeBot_Inv_NMOS_ChannelWidth
		_Caculation_Parameters1['_SARLogic_CLKBufTreeBot_Inv_NMOS_ChannelLength'] = _SARLogic_CLKBufTreeBot_Inv_NMOS_ChannelLength
		_Caculation_Parameters1['_SARLogic_CLKBufTreeBot_Inv_NMOS_NumberofGate'] = _SARLogic_CLKBufTreeBot_Inv_NMOS_NumberofGate
		_Caculation_Parameters1['_SARLogic_CLKBufTreeBot_Inv_NMOS_XVT'] = _SARLogic_CLKBufTreeBot_Inv_NMOS_XVT
		_Caculation_Parameters1['_SARLogic_CLKBufTreeBot_Inv_NMOS_POGate_Comb_length'] = _SARLogic_CLKBufTreeBot_Inv_NMOS_POGate_Comb_length

		_Caculation_Parameters1['_SARLogic_CLKBufTreeBot_Inv_PMOS_ChannelWidth'] = _SARLogic_CLKBufTreeBot_Inv_PMOS_ChannelWidth
		_Caculation_Parameters1['_SARLogic_CLKBufTreeBot_Inv_PMOS_ChannelLength'] = _SARLogic_CLKBufTreeBot_Inv_PMOS_ChannelLength
		_Caculation_Parameters1['_SARLogic_CLKBufTreeBot_Inv_PMOS_NumberofGate'] = _SARLogic_CLKBufTreeBot_Inv_PMOS_NumberofGate
		_Caculation_Parameters1['_SARLogic_CLKBufTreeBot_Inv_PMOS_XVT'] = _SARLogic_CLKBufTreeBot_Inv_PMOS_XVT
		_Caculation_Parameters1['_SARLogic_CLKBufTreeBot_Inv_PMOS_POGate_Comb_length'] = _SARLogic_CLKBufTreeBot_Inv_PMOS_POGate_Comb_length

		_Caculation_Parameters1['_SARLogic_CLKBufTreeBot_NMOS_Pbody_NumCont'] = _SARLogic_CLKBufTreeBot_NMOS_Pbody_NumCont
		_Caculation_Parameters1['_SARLogic_CLKBufTreeBot_NMOS_Pbody_XvtTop2Pbody'] = _SARLogic_CLKBufTreeBot_NMOS_Pbody_XvtTop2Pbody
		_Caculation_Parameters1['_SARLogic_CLKBufTreeBot_PMOS_Nbody_NumCont'] = _SARLogic_CLKBufTreeBot_PMOS_Nbody_NumCont
		_Caculation_Parameters1['_SARLogic_CLKBufTreeBot_PMOS_Nbody_Xvtdown2Nbody'] = _SARLogic_CLKBufTreeBot_PMOS_Nbody_Xvtdown2Nbody
		_Caculation_Parameters1['_SARLogic_CLKBufTreeBot_PMOSXvt2NMOSXvt'] = _SARLogic_CLKBufTreeBot_PMOSXvt2NMOSXvt

		_Caculation_Parameters1['_CDACPreDriver_Pbody_NumCont'] = _CDACPreDriver_Pbody_NumCont
		_Caculation_Parameters1['_CDACPreDriver_Nbody_NumCont'] = _CDACPreDriver_Nbody_NumCont
		_Caculation_Parameters1['_CDACPreDriver_PMOSXvt2NMOSXvt'] = _CDACPreDriver_PMOSXvt2NMOSXvt
		_Caculation_Parameters1['_CDACPreDriver_XvtTop2Pbody'] = _CDACPreDriver_XvtTop2Pbody
		_Caculation_Parameters1['_CDACPreDriver_Xvtdown2Nbody'] = _CDACPreDriver_Xvtdown2Nbody

		_Caculation_Parameters1['_CDACPreDriver_NumberofGate'] = _CDACPreDriver_NumberofGate
		_Caculation_Parameters1['_CDACPreDriver_ChannelLength'] = _CDACPreDriver_ChannelLength
		_Caculation_Parameters1['_CDACPreDriver_XVT'] = _CDACPreDriver_XVT

		_Caculation_Parameters1['_CLKDout_XVT_Common'] = _CLKDout_XVT_Common
		_Caculation_Parameters1['_CDACPreDriver_Inv_NMOS_ChannelWidth'] = _CDACPreDriver_Inv_NMOS_ChannelWidth
		_Caculation_Parameters1['_CDACPreDriver_Inv_NMOS_POGate_Comb_length'] = _CDACPreDriver_Inv_NMOS_POGate_Comb_length
		_Caculation_Parameters1['_CDACPreDriver_Inv_PMOS_ChannelWidth'] = _CDACPreDriver_Inv_PMOS_ChannelWidth
		_Caculation_Parameters1['_CDACPreDriver_Inv_PMOS_POGate_Comb_length'] = _CDACPreDriver_Inv_PMOS_POGate_Comb_length

		_Caculation_Parameters1['_CLKDout_Inv_NMOS_ChannelWidth'] = _CLKDout_Inv_NMOS_ChannelWidth
		_Caculation_Parameters1['_CLKDout_Inv_NMOS_ChannelLength'] = _CLKDout_Inv_NMOS_ChannelLength
		_Caculation_Parameters1['_CLKDout_Inv_NMOS_NumberofGate'] = _CLKDout_Inv_NMOS_NumberofGate
		_Caculation_Parameters1['_CLKDout_Inv_NMOS_POGate_Comb_length'] = _CLKDout_Inv_NMOS_POGate_Comb_length

		_Caculation_Parameters1['_CLKDout_Inv_PMOS_ChannelWidth'] = _CLKDout_Inv_PMOS_ChannelWidth
		_Caculation_Parameters1['_CLKDout_Inv_PMOS_ChannelLength'] = _CLKDout_Inv_PMOS_ChannelLength
		_Caculation_Parameters1['_CLKDout_Inv_PMOS_NumberofGate'] = _CLKDout_Inv_PMOS_NumberofGate
		_Caculation_Parameters1['_CLKDout_Inv_PMOS_POGate_Comb_length'] = _CLKDout_Inv_PMOS_POGate_Comb_length

		_Caculation_Parameters1['_CLKDout_AND_NAND_NMOS_ChannelWidth'] = _CLKDout_AND_NAND_NMOS_ChannelWidth
		_Caculation_Parameters1['_CLKDout_AND_NAND_NMOS_ChannelLength'] = _CLKDout_AND_NAND_NMOS_ChannelLength
		_Caculation_Parameters1['_CLKDout_AND_NAND_NMOS_NumberofGate'] = _CLKDout_AND_NAND_NMOS_NumberofGate

		_Caculation_Parameters1['_CLKDout_AND_NAND_PMOS_ChannelWidth'] = _CLKDout_AND_NAND_PMOS_ChannelWidth
		_Caculation_Parameters1['_CLKDout_AND_NAND_PMOS_ChannelLength'] = _CLKDout_AND_NAND_PMOS_ChannelLength
		_Caculation_Parameters1['_CLKDout_AND_NAND_PMOS_NumberofGate'] = _CLKDout_AND_NAND_PMOS_NumberofGate

		_Caculation_Parameters1['_CLKDout_AND_Inv_NMOS_ChannelWidth'] = _CLKDout_AND_Inv_NMOS_ChannelWidth
		_Caculation_Parameters1['_CLKDout_AND_Inv_NMOS_ChannelLength'] = _CLKDout_AND_Inv_NMOS_ChannelLength
		_Caculation_Parameters1['_CLKDout_AND_Inv_NMOS_NumberofGate'] = _CLKDout_AND_Inv_NMOS_NumberofGate
		_Caculation_Parameters1['_CLKDout_AND_Inv_NMOS_POGate_Comb_length'] = _CLKDout_AND_Inv_NMOS_POGate_Comb_length

		_Caculation_Parameters1['_CLKDout_AND_Inv_PMOS_ChannelWidth'] = _CLKDout_AND_Inv_PMOS_ChannelWidth
		_Caculation_Parameters1['_CLKDout_AND_Inv_PMOS_ChannelLength'] = _CLKDout_AND_Inv_PMOS_ChannelLength
		_Caculation_Parameters1['_CLKDout_AND_Inv_PMOS_NumberofGate'] = _CLKDout_AND_Inv_PMOS_NumberofGate
		_Caculation_Parameters1['_CLKDout_AND_Inv_PMOS_POGate_Comb_length'] = _CLKDout_AND_Inv_PMOS_POGate_Comb_length

		_Caculation_Parameters1['_Comp_SALatch_CLKinputPMOSFinger1'] = _Comp_SALatch_CLKinputPMOSFinger1
		_Caculation_Parameters1['_Comp_SALatch_CLKinputPMOSFinger2'] = _Comp_SALatch_CLKinputPMOSFinger2
		_Caculation_Parameters1['_Comp_SALatch_PMOSFinger'] = _Comp_SALatch_PMOSFinger
		_Caculation_Parameters1['_Comp_SALatch_PMOSChannelWidth'] = _Comp_SALatch_PMOSChannelWidth
		_Caculation_Parameters1['_Comp_SALatch_DATAinputNMOSFinger'] = _Comp_SALatch_DATAinputNMOSFinger
		_Caculation_Parameters1['_Comp_SALatch_NMOSFinger'] = _Comp_SALatch_NMOSFinger
		_Caculation_Parameters1['_Comp_SALatch_CLKinputNMOSFinger'] = _Comp_SALatch_CLKinputNMOSFinger
		_Caculation_Parameters1['_Comp_SALatch_NMOSChannelWidth'] = _Comp_SALatch_NMOSChannelWidth
		_Caculation_Parameters1['_Comp_SALatch_CLKinputNMOSChannelWidth'] = _Comp_SALatch_CLKinputNMOSChannelWidth
		_Caculation_Parameters1['_Comp_SALatch_ChannelLength'] = _Comp_SALatch_ChannelLength
		_Caculation_Parameters1['_Comp_SALatch_Dummy'] = _Comp_SALatch_Dummy
		_Caculation_Parameters1['_Comp_SALatch_XVT'] = _Comp_SALatch_XVT
		_Caculation_Parameters1['_Comp_SALatch_GuardringWidth'] = _Comp_SALatch_GuardringWidth
		_Caculation_Parameters1['_Comp_SALatch_Guardring'] = _Comp_SALatch_Guardring
		_Caculation_Parameters1['_Comp_SALatch_SlicerGuardringWidth'] = _Comp_SALatch_SlicerGuardringWidth
		_Caculation_Parameters1['_Comp_SALatch_SlicerGuardring'] = _Comp_SALatch_SlicerGuardring
		_Caculation_Parameters1['_Comp_SALatch_NumSupplyCOY'] = _Comp_SALatch_NumSupplyCOY
		_Caculation_Parameters1['_Comp_SALatch_NumSupplyCOX'] = _Comp_SALatch_NumSupplyCOX
		_Caculation_Parameters1['_Comp_SALatch_SupplyMet1XWidth'] = _Comp_SALatch_SupplyMet1XWidth
		_Caculation_Parameters1['_Comp_SALatch_SupplyMet1YWidth'] = _Comp_SALatch_SupplyMet1YWidth
		_Caculation_Parameters1['_Comp_SALatch_VDD2VSSHeight'] = _Comp_SALatch_VDD2VSSHeight
		_Caculation_Parameters1['_Comp_SALatch_NumVIAPoly2Met1COX'] = _Comp_SALatch_NumVIAPoly2Met1COX
		_Caculation_Parameters1['_Comp_SALatch_NumVIAPoly2Met1COY'] = _Comp_SALatch_NumVIAPoly2Met1COY
		_Caculation_Parameters1['_Comp_SALatch_NumVIAMet12COX'] = _Comp_SALatch_NumVIAMet12COX
		_Caculation_Parameters1['_Comp_SALatch_NumVIAMet12COY'] = _Comp_SALatch_NumVIAMet12COY
		_Caculation_Parameters1['_Comp_SALatch_PowerLine'] = _Comp_SALatch_PowerLine

		## StrongARMLatch Output Buffer Sizing
		# Inverter1
		_Caculation_Parameters1['_Comp_SAOutBuf_Inv1_NMOS_ChannelWidth'] = _Comp_SAOutBuf_Inv1_NMOS_ChannelWidth
		_Caculation_Parameters1['_Comp_SAOutBuf_Inv1_NMOS_ChannelLength'] = _Comp_SAOutBuf_Inv1_NMOS_ChannelLength
		_Caculation_Parameters1['_Comp_SAOutBuf_Inv1_NMOS_NumberofGate'] = _Comp_SAOutBuf_Inv1_NMOS_NumberofGate
		_Caculation_Parameters1['_Comp_SAOutBuf_Inv1_NMOS_XVT'] = _Comp_SAOutBuf_Inv1_NMOS_XVT
		_Caculation_Parameters1['_Comp_SAOutBuf_Inv1_NMOS_POGate_Comb_length'] = _Comp_SAOutBuf_Inv1_NMOS_POGate_Comb_length

		_Caculation_Parameters1['_Comp_SAOutBuf_Inv1_PMOS_ChannelWidth'] = _Comp_SAOutBuf_Inv1_PMOS_ChannelWidth
		_Caculation_Parameters1['_Comp_SAOutBuf_Inv1_PMOS_ChannelLength'] = _Comp_SAOutBuf_Inv1_PMOS_ChannelLength
		_Caculation_Parameters1['_Comp_SAOutBuf_Inv1_PMOS_NumberofGate'] = _Comp_SAOutBuf_Inv1_PMOS_NumberofGate
		_Caculation_Parameters1['_Comp_SAOutBuf_Inv1_PMOS_XVT'] = _Comp_SAOutBuf_Inv1_PMOS_XVT
		_Caculation_Parameters1['_Comp_SAOutBuf_Inv1_PMOS_POGate_Comb_length'] = _Comp_SAOutBuf_Inv1_PMOS_POGate_Comb_length

		# Inverter2
		_Caculation_Parameters1['_Comp_SAOutBuf_Inv2_NMOS_ChannelWidth'] = _Comp_SAOutBuf_Inv2_NMOS_ChannelWidth
		_Caculation_Parameters1['_Comp_SAOutBuf_Inv2_NMOS_ChannelLength'] = _Comp_SAOutBuf_Inv2_NMOS_ChannelLength
		_Caculation_Parameters1['_Comp_SAOutBuf_Inv2_NMOS_NumberofGate'] = _Comp_SAOutBuf_Inv2_NMOS_NumberofGate
		_Caculation_Parameters1['_Comp_SAOutBuf_Inv2_NMOS_XVT'] = _Comp_SAOutBuf_Inv2_NMOS_XVT
		_Caculation_Parameters1['_Comp_SAOutBuf_Inv2_NMOS_POGate_Comb_length'] = _Comp_SAOutBuf_Inv2_NMOS_POGate_Comb_length

		_Caculation_Parameters1['_Comp_SAOutBuf_Inv2_PMOS_ChannelWidth'] = _Comp_SAOutBuf_Inv2_PMOS_ChannelWidth
		_Caculation_Parameters1['_Comp_SAOutBuf_Inv2_PMOS_ChannelLength'] = _Comp_SAOutBuf_Inv2_PMOS_ChannelLength
		_Caculation_Parameters1['_Comp_SAOutBuf_Inv2_PMOS_NumberofGate'] = _Comp_SAOutBuf_Inv2_PMOS_NumberofGate
		_Caculation_Parameters1['_Comp_SAOutBuf_Inv2_PMOS_XVT'] = _Comp_SAOutBuf_Inv2_PMOS_XVT
		_Caculation_Parameters1['_Comp_SAOutBuf_Inv2_PMOS_POGate_Comb_length'] = _Comp_SAOutBuf_Inv2_PMOS_POGate_Comb_length

		## SR Latch Sizing
		_Caculation_Parameters1['_Comp_SRLatch_NAND_NMOS_ChannelWidth'] = _Comp_SRLatch_NAND_NMOS_ChannelWidth
		_Caculation_Parameters1['_Comp_SRLatch_NAND_NMOS_ChannelLength'] = _Comp_SRLatch_NAND_NMOS_ChannelLength
		_Caculation_Parameters1['_Comp_SRLatch_NAND_NMOS_NumberofGate'] = _Comp_SRLatch_NAND_NMOS_NumberofGate
		_Caculation_Parameters1['_Comp_SRLatch_NAND_NMOS_XVT'] = _Comp_SRLatch_NAND_NMOS_XVT
		_Caculation_Parameters1['_Comp_SRLatch_NAND_NMOS_POGate_Comb_length'] = _Comp_SRLatch_NAND_NMOS_POGate_Comb_length

		_Caculation_Parameters1['_Comp_SRLatch_NAND_PMOS_ChannelWidth'] = _Comp_SRLatch_NAND_PMOS_ChannelWidth
		_Caculation_Parameters1['_Comp_SRLatch_NAND_PMOS_ChannelLength'] = _Comp_SRLatch_NAND_PMOS_ChannelLength
		_Caculation_Parameters1['_Comp_SRLatch_NAND_PMOS_NumberofGate'] = _Comp_SRLatch_NAND_PMOS_NumberofGate
		_Caculation_Parameters1['_Comp_SRLatch_NAND_PMOS_XVT'] = _Comp_SRLatch_NAND_PMOS_XVT
		_Caculation_Parameters1['_Comp_SRLatch_NAND_PMOS_POGate_Comb_length'] = _Comp_SRLatch_NAND_PMOS_POGate_Comb_length

		# CLK Input Logic Gates
		_Caculation_Parameters1['_Comp_CLKSamp_Inv_NMOS_ChannelWidth'] = _Comp_CLKSamp_Inv_NMOS_ChannelWidth
		_Caculation_Parameters1['_Comp_CLKSamp_Inv_NMOS_ChannelLength'] = _Comp_CLKSamp_Inv_NMOS_ChannelLength
		_Caculation_Parameters1['_Comp_CLKSamp_Inv_NMOS_NumberofGate'] = _Comp_CLKSamp_Inv_NMOS_NumberofGate
		_Caculation_Parameters1['_Comp_CLKSamp_Inv_NMOS_XVT'] = _Comp_CLKSamp_Inv_NMOS_XVT
		_Caculation_Parameters1['_Comp_CLKSamp_Inv_NMOS_POGate_Comb_length'] = _Comp_CLKSamp_Inv_NMOS_POGate_Comb_length

		_Caculation_Parameters1['_Comp_CLKSamp_Inv_PMOS_ChannelWidth'] = _Comp_CLKSamp_Inv_PMOS_ChannelWidth
		_Caculation_Parameters1['_Comp_CLKSamp_Inv_PMOS_ChannelLength'] = _Comp_CLKSamp_Inv_PMOS_ChannelLength
		_Caculation_Parameters1['_Comp_CLKSamp_Inv_PMOS_NumberofGate'] = _Comp_CLKSamp_Inv_PMOS_NumberofGate
		_Caculation_Parameters1['_Comp_CLKSamp_Inv_PMOS_XVT'] = _Comp_CLKSamp_Inv_PMOS_XVT
		_Caculation_Parameters1['_Comp_CLKSamp_Inv_PMOS_POGate_Comb_length'] = _Comp_CLKSamp_Inv_PMOS_POGate_Comb_length

		_Caculation_Parameters1['_Comp_CLKSrc_Inv_NMOS_ChannelWidth'] = _Comp_CLKSrc_Inv_NMOS_ChannelWidth
		_Caculation_Parameters1['_Comp_CLKSrc_Inv_NMOS_ChannelLength'] = _Comp_CLKSrc_Inv_NMOS_ChannelLength
		_Caculation_Parameters1['_Comp_CLKSrc_Inv_NMOS_NumberofGate'] = _Comp_CLKSrc_Inv_NMOS_NumberofGate
		_Caculation_Parameters1['_Comp_CLKSrc_Inv_NMOS_XVT'] = _Comp_CLKSrc_Inv_NMOS_XVT
		_Caculation_Parameters1['_Comp_CLKSrc_Inv_NMOS_POGate_Comb_length'] = _Comp_CLKSrc_Inv_NMOS_POGate_Comb_length

		_Caculation_Parameters1['_Comp_CLKSrc_Inv_PMOS_ChannelWidth'] = _Comp_CLKSrc_Inv_PMOS_ChannelWidth
		_Caculation_Parameters1['_Comp_CLKSrc_Inv_PMOS_ChannelLength'] = _Comp_CLKSrc_Inv_PMOS_ChannelLength
		_Caculation_Parameters1['_Comp_CLKSrc_Inv_PMOS_NumberofGate'] = _Comp_CLKSrc_Inv_PMOS_NumberofGate
		_Caculation_Parameters1['_Comp_CLKSrc_Inv_PMOS_XVT'] = _Comp_CLKSrc_Inv_PMOS_XVT
		_Caculation_Parameters1['_Comp_CLKSrc_Inv_PMOS_POGate_Comb_length'] = _Comp_CLKSrc_Inv_PMOS_POGate_Comb_length

		## CLKSrc & CLKSample AND Gate
		_Caculation_Parameters1['_Comp_AND_NAND_NMOS_ChannelWidth'] = _Comp_AND_NAND_NMOS_ChannelWidth
		_Caculation_Parameters1['_Comp_AND_NAND_NMOS_ChannelLength'] = _Comp_AND_NAND_NMOS_ChannelLength
		_Caculation_Parameters1['_Comp_AND_NAND_NMOS_NumberofGate'] = _Comp_AND_NAND_NMOS_NumberofGate
		_Caculation_Parameters1['_Comp_AND_NAND_NMOS_XVT'] = _Comp_AND_NAND_NMOS_XVT

		_Caculation_Parameters1['_Comp_AND_NAND_PMOS_ChannelWidth'] = _Comp_AND_NAND_PMOS_ChannelWidth
		_Caculation_Parameters1['_Comp_AND_NAND_PMOS_ChannelLength'] = _Comp_AND_NAND_PMOS_ChannelLength
		_Caculation_Parameters1['_Comp_AND_NAND_PMOS_NumberofGate'] = _Comp_AND_NAND_PMOS_NumberofGate
		_Caculation_Parameters1['_Comp_AND_NAND_PMOS_XVT'] = _Comp_AND_NAND_PMOS_XVT

		_Caculation_Parameters1['_Comp_AND_Inv_NMOS_ChannelWidth'] = _Comp_AND_Inv_NMOS_ChannelWidth
		_Caculation_Parameters1['_Comp_AND_Inv_NMOS_ChannelLength'] = _Comp_AND_Inv_NMOS_ChannelLength
		_Caculation_Parameters1['_Comp_AND_Inv_NMOS_NumberofGate'] = _Comp_AND_Inv_NMOS_NumberofGate
		_Caculation_Parameters1['_Comp_AND_Inv_NMOS_XVT'] = _Comp_AND_Inv_NMOS_XVT
		_Caculation_Parameters1['_Comp_AND_Inv_NMOS_POGate_Comb_length'] = _Comp_AND_Inv_NMOS_POGate_Comb_length

		_Caculation_Parameters1['_Comp_AND_Inv_PMOS_ChannelWidth'] = _Comp_AND_Inv_PMOS_ChannelWidth
		_Caculation_Parameters1['_Comp_AND_Inv_PMOS_ChannelLength'] = _Comp_AND_Inv_PMOS_ChannelLength
		_Caculation_Parameters1['_Comp_AND_Inv_PMOS_NumberofGate'] = _Comp_AND_Inv_PMOS_NumberofGate
		_Caculation_Parameters1['_Comp_AND_Inv_PMOS_XVT'] = _Comp_AND_Inv_PMOS_XVT
		_Caculation_Parameters1['_Comp_AND_Inv_PMOS_POGate_Comb_length'] = _Comp_AND_Inv_PMOS_POGate_Comb_length

		## CLK Buffer
		# Inverter1
		_Caculation_Parameters1['_Comp_CLKBuf_Inv1_NMOS_ChannelWidth'] = _Comp_CLKBuf_Inv1_NMOS_ChannelWidth
		_Caculation_Parameters1['_Comp_CLKBuf_Inv1_NMOS_ChannelLength'] = _Comp_CLKBuf_Inv1_NMOS_ChannelLength
		_Caculation_Parameters1['_Comp_CLKBuf_Inv1_NMOS_NumberofGate'] = _Comp_CLKBuf_Inv1_NMOS_NumberofGate
		_Caculation_Parameters1['_Comp_CLKBuf_Inv1_NMOS_XVT'] = _Comp_CLKBuf_Inv1_NMOS_XVT
		_Caculation_Parameters1['_Comp_CLKBuf_Inv1_NMOS_POGate_Comb_length'] = _Comp_CLKBuf_Inv1_NMOS_POGate_Comb_length

		_Caculation_Parameters1['_Comp_CLKBuf_Inv1_PMOS_ChannelWidth'] = _Comp_CLKBuf_Inv1_PMOS_ChannelWidth
		_Caculation_Parameters1['_Comp_CLKBuf_Inv1_PMOS_ChannelLength'] = _Comp_CLKBuf_Inv1_PMOS_ChannelLength
		_Caculation_Parameters1['_Comp_CLKBuf_Inv1_PMOS_NumberofGate'] = _Comp_CLKBuf_Inv1_PMOS_NumberofGate
		_Caculation_Parameters1['_Comp_CLKBuf_Inv1_PMOS_XVT'] = _Comp_CLKBuf_Inv1_PMOS_XVT
		_Caculation_Parameters1['_Comp_CLKBuf_Inv1_PMOS_POGate_Comb_length'] = _Comp_CLKBuf_Inv1_PMOS_POGate_Comb_length

		# Inverter2
		_Caculation_Parameters1['_Comp_CLKBuf_Inv2_NMOS_ChannelWidth'] = _Comp_CLKBuf_Inv2_NMOS_ChannelWidth
		_Caculation_Parameters1['_Comp_CLKBuf_Inv2_NMOS_ChannelLength'] = _Comp_CLKBuf_Inv2_NMOS_ChannelLength
		_Caculation_Parameters1['_Comp_CLKBuf_Inv2_NMOS_NumberofGate'] = _Comp_CLKBuf_Inv2_NMOS_NumberofGate
		_Caculation_Parameters1['_Comp_CLKBuf_Inv2_NMOS_XVT'] = _Comp_CLKBuf_Inv2_NMOS_XVT
		_Caculation_Parameters1['_Comp_CLKBuf_Inv2_NMOS_POGate_Comb_length'] = _Comp_CLKBuf_Inv2_NMOS_POGate_Comb_length

		_Caculation_Parameters1['_Comp_CLKBuf_Inv2_PMOS_ChannelWidth'] = _Comp_CLKBuf_Inv2_PMOS_ChannelWidth
		_Caculation_Parameters1['_Comp_CLKBuf_Inv2_PMOS_ChannelLength'] = _Comp_CLKBuf_Inv2_PMOS_ChannelLength
		_Caculation_Parameters1['_Comp_CLKBuf_Inv2_PMOS_NumberofGate'] = _Comp_CLKBuf_Inv2_PMOS_NumberofGate
		_Caculation_Parameters1['_Comp_CLKBuf_Inv2_PMOS_XVT'] = _Comp_CLKBuf_Inv2_PMOS_XVT
		_Caculation_Parameters1['_Comp_CLKBuf_Inv2_PMOS_POGate_Comb_length'] = _Comp_CLKBuf_Inv2_PMOS_POGate_Comb_length

		# PowerRail Placement
		_Caculation_Parameters1['_Comp_BufSR_NMOS_Pbody_NumCont'] = _Comp_BufSR_NMOS_Pbody_NumCont
		_Caculation_Parameters1['_Comp_BufSR_NMOS_Pbody_XvtTop2Pbody'] = _Comp_BufSR_NMOS_Pbody_XvtTop2Pbody
		_Caculation_Parameters1['_Comp_BufSR_PMOS_Nbody_NumCont'] = _Comp_BufSR_PMOS_Nbody_NumCont
		_Caculation_Parameters1['_Comp_BufSR_PMOS_Nbody_Xvtdown2Nbody'] = _Comp_BufSR_PMOS_Nbody_Xvtdown2Nbody
		_Caculation_Parameters1['_Comp_BufSR_PMOSXvt2NMOSXvt'] = _Comp_BufSR_PMOSXvt2NMOSXvt

		_Caculation_Parameters1['_Comp_CLKInLogic_NMOS_Pbody_Xvtdown2Pbody'] = _Comp_CLKInLogic_NMOS_Pbody_Xvtdown2Pbody
		_Caculation_Parameters1['_Comp_CLKInLogic_PMOS_Nbody_NumCont'] = _Comp_CLKInLogic_PMOS_Nbody_NumCont
		_Caculation_Parameters1['_Comp_CLKInLogic_PMOS_Nbody_Xvtdown2Nbody'] = _Comp_CLKInLogic_PMOS_Nbody_Xvtdown2Nbody
		_Caculation_Parameters1['_Comp_CLKInLogic_PMOSXvt2NMOSXvt'] = _Comp_CLKInLogic_PMOSXvt2NMOSXvt

		_Caculation_Parameters1['_Buf_CLKSamp_Pbody_NumCont'] = _Buf_CLKSamp_Pbody_NumCont
		_Caculation_Parameters1['_Buf_CLKSamp_Nbody_NumCont'] = _Buf_CLKSamp_Nbody_NumCont
		_Caculation_Parameters1['_Buf_CLKSamp_PMOSXvt2NMOSXvt'] = _Buf_CLKSamp_PMOSXvt2NMOSXvt
		_Caculation_Parameters1['_Buf_CLKSamp_XvtTop2Pbody'] = _Buf_CLKSamp_XvtTop2Pbody
		_Caculation_Parameters1['_Buf_CLKSamp_Xvtdown2Nbody'] = _Buf_CLKSamp_Xvtdown2Nbody

		_Caculation_Parameters1['_Buf_CLKSamp_NumberofGate'] = _Buf_CLKSamp_NumberofGate
		_Caculation_Parameters1['_Buf_CLKSamp_ChannelLength'] = _Buf_CLKSamp_ChannelLength
		_Caculation_Parameters1['_Buf_CLKSamp_XVT'] = _Buf_CLKSamp_XVT

		_Caculation_Parameters1['_Buf_CLKSamp_Inv_NMOS_ChannelWidth'] = _Buf_CLKSamp_Inv_NMOS_ChannelWidth
		_Caculation_Parameters1['_Buf_CLKSamp_Inv_NMOS_POGate_Comb_length'] = _Buf_CLKSamp_Inv_NMOS_POGate_Comb_length
		_Caculation_Parameters1['_Buf_CLKSamp_Inv_PMOS_ChannelWidth'] = _Buf_CLKSamp_Inv_PMOS_ChannelWidth
		_Caculation_Parameters1['_Buf_CLKSamp_Inv_PMOS_POGate_Comb_length'] = _Buf_CLKSamp_Inv_PMOS_POGate_Comb_length

		_Caculation_Parameters1['_Buf_CLKSrc_Pbody_NumCont'] = _Buf_CLKSrc_Pbody_NumCont
		_Caculation_Parameters1['_Buf_CLKSrc_Nbody_NumCont'] = _Buf_CLKSrc_Nbody_NumCont
		_Caculation_Parameters1['_Buf_CLKSrc_PMOSXvt2NMOSXvt'] = _Buf_CLKSrc_PMOSXvt2NMOSXvt
		_Caculation_Parameters1['_Buf_CLKSrc_XvtTop2Pbody'] = _Buf_CLKSrc_XvtTop2Pbody
		_Caculation_Parameters1['_Buf_CLKSrc_Xvtdown2Nbody'] = _Buf_CLKSrc_Xvtdown2Nbody

		_Caculation_Parameters1['_Buf_CLKSrc_NumberofGate'] = _Buf_CLKSrc_NumberofGate
		_Caculation_Parameters1['_Buf_CLKSrc_ChannelLength'] = _Buf_CLKSrc_ChannelLength
		_Caculation_Parameters1['_Buf_CLKSrc_XVT'] = _Buf_CLKSrc_XVT

		_Caculation_Parameters1['_Buf_CLKSrc_Inv_NMOS_ChannelWidth'] = _Buf_CLKSrc_Inv_NMOS_ChannelWidth
		_Caculation_Parameters1['_Buf_CLKSrc_Inv_NMOS_POGate_Comb_length'] = _Buf_CLKSrc_Inv_NMOS_POGate_Comb_length
		_Caculation_Parameters1['_Buf_CLKSrc_Inv_PMOS_ChannelWidth'] = _Buf_CLKSrc_Inv_PMOS_ChannelWidth
		_Caculation_Parameters1['_Buf_CLKSrc_Inv_PMOS_POGate_Comb_length'] = _Buf_CLKSrc_Inv_PMOS_POGate_Comb_length

		_Caculation_Parameters1['_Buf_CompOut_Pbody_NumCont'] = _Buf_CompOut_Pbody_NumCont
		_Caculation_Parameters1['_Buf_CompOut_Nbody_NumCont'] = _Buf_CompOut_Nbody_NumCont
		_Caculation_Parameters1['_Buf_CompOut_PMOSXvt2NMOSXvt'] = _Buf_CompOut_PMOSXvt2NMOSXvt
		_Caculation_Parameters1['_Buf_CompOut_XvtTop2Pbody'] = _Buf_CompOut_XvtTop2Pbody
		_Caculation_Parameters1['_Buf_CompOut_Xvtdown2Nbody'] = _Buf_CompOut_Xvtdown2Nbody

		_Caculation_Parameters1['_Buf_CompOut_NumberofGate'] = _Buf_CompOut_NumberofGate
		_Caculation_Parameters1['_Buf_CompOut_ChannelLength'] = _Buf_CompOut_ChannelLength
		_Caculation_Parameters1['_Buf_CompOut_XVT'] = _Buf_CompOut_XVT

		_Caculation_Parameters1['_Buf_CompOut_Inv_NMOS_ChannelWidth'] = _Buf_CompOut_Inv_NMOS_ChannelWidth
		_Caculation_Parameters1['_Buf_CompOut_Inv_NMOS_POGate_Comb_length'] = _Buf_CompOut_Inv_NMOS_POGate_Comb_length
		_Caculation_Parameters1['_Buf_CompOut_Inv_PMOS_ChannelWidth'] = _Buf_CompOut_Inv_PMOS_ChannelWidth
		_Caculation_Parameters1['_Buf_CompOut_Inv_PMOS_POGate_Comb_length'] = _Buf_CompOut_Inv_PMOS_POGate_Comb_length

		self._DesignParameter['SRF_SARLogicWtComparator'] = self._SrefElementDeclaration(_DesignObj=L00_SARLogicWtComparator_KJH._SARLogicWtComparator(_DesignParameter=None,_Name='{}:SRF_SARLogicWtComparator'.format(_Name)))[0]

		## Define Sref Reflection: ex)self._DesignParameter['_NMOS_POWER']['_Reflect'] = [0, 0, 0]
		self._DesignParameter['SRF_SARLogicWtComparator']['_Reflect'] = [0, 0, 0]

		## Define Sref Angle: ex)'_NMOS_POWER'
		self._DesignParameter['SRF_SARLogicWtComparator']['_Angle'] = 0

		## Calculate Sref Layer by using Calculation_Parameter: ex)'_NMOS_POWER'
		self._DesignParameter['SRF_SARLogicWtComparator']['_DesignObj']._CalculateDesignParameter(
			**_Caculation_Parameters1)

		## initialize Sref _XYcoordinate: ex)'_NMOS_POWER'
		self._DesignParameter['SRF_SARLogicWtComparator']['_XYCoordinates'] = [[0, 0]]

		## Pre-Calculated centY coord
		# tmp = self.get_param_KJH4('SRF_SARLogicWtComparator','SRF_SARLogicWtBuffers','SRF_SARLogicWtCLKTree','SRF_SARLogic','BND_Nbody_M1Exten')
		# centY = tmp[0][0][0][0][0][0]['_XY_cent'][1]
		tmp1 = self.get_param_KJH4('SRF_SARLogicWtComparator', 'SRF_SARLogicWtBuffers', 'SRF_UpperCDACPreDriver', 'BND_Nbody_M1Exten')
		tmp1_2 = self.get_param_KJH4('SRF_SARLogicWtComparator', 'SRF_SARLogicWtBuffers', 'SRF_LowerCDACPreDriver', 'BND_Pbody_M1Exten')
		centY = int((tmp1[0][0][0][0][0]['_XY_cent'][1] + tmp1_2[0][0][0][0][0]['_XY_cent'][1]) / 2)

		print('###############################################')
		print('##              CDAC (Positive)              ##')
		print('##            Calculation_Start!!            ##')
		print('###############################################')

		## CDAC (SREF) Generation
		## Copy Calculation_Parameters from low-level-block ex)copy.deepcopy(B16_nmos_power_v2._NMOS_POWER._ParametersForDesignCalculation)
		_Caculation_Parameters0 = copy.deepcopy(H02_01_CDACWtDriver_Unfolded._CDACWtDriver_Unfolded._ParametersForDesignCalculation)
		## Define Calculation_Parameters ex) _Caculation_Parameters['_NMOSPOWER_PbodyContact_1_Length']  = _NMOSPOWER_PbodyContact_1_Length
		_Caculation_Parameters0['_NumOfBits'] = _NumofCbit
		_Caculation_Parameters0['_CDAC_LayoutOption'] = _CDAC_LayoutOption
		_Caculation_Parameters0['_CDAC_ShieldingLayer'] = _CDAC_ShieldingLayer
		_Caculation_Parameters0['_CDAC_BotNodeVtcExtensionMetalLayer'] = 2
		_Caculation_Parameters0['_CDAC_MetalWidth'] = _CDAC_MetalWidth
		_Caculation_Parameters0['_CDAC_MetalLength'] = _CDAC_MetalLength
		_Caculation_Parameters0['_CDAC_MetalSpacing'] = _CDAC_MetalSpacing
		_Caculation_Parameters0['_CDAC_NumOfElement'] = _CDAC_NumOfElement
		_Caculation_Parameters0['_CDAC_ConnectLength'] = _CDAC_ConnectLength
		_Caculation_Parameters0['_CDAC_ExtendLength'] = _CDAC_ExtendLength
		_Caculation_Parameters0['_CDAC_CapArrayWDrivingNodeDistance'] = _CDAC_CapArrayWDrivingNodeDistance
		_Caculation_Parameters0['_CDAC_DriveNodeDistance'] = _CDAC_DriveNodeDistance
		_Caculation_Parameters0['_CDAC_YWidth_Bottom_Hrz'] = _CDAC_YWidth_Bottom_Hrz
		_Caculation_Parameters0['_CDAC_DummyCap_TopBottomShort'] = _CDAC_DummyCap_TopBottomShort
		_Caculation_Parameters0['_CDAC_NumOfDummyCaps'] = _CDAC_NumOfDummyCaps
		_Caculation_Parameters0['_Driver_SizeByBit'] = _Driver_SizeByBit
		_Caculation_Parameters0['_Driver_NMOS_NumberofGate'] = _Driver_NMOS_NumberofGate
		_Caculation_Parameters0['_Driver_NMOS_ChannelWidth'] = _Driver_NMOS_ChannelWidth
		_Caculation_Parameters0['_Driver_NMOS_Channellength'] = _Driver_NMOS_Channellength
		_Caculation_Parameters0['_Driver_NMOS_XVT'] = _Driver_NMOS_XVT
		_Caculation_Parameters0['_Driver_PMOS_NumberofGate'] = _Driver_PMOS_NumberofGate
		_Caculation_Parameters0['_Driver_PMOS_ChannelWidth'] = _Driver_PMOS_ChannelWidth
		_Caculation_Parameters0['_Driver_PMOS_Channellength'] = _Driver_PMOS_Channellength
		_Caculation_Parameters0['_Driver_PMOS_XVT'] = _Driver_PMOS_XVT

		## CDAC (Positive)
		if _CDAC_Folding == True:
			if _Driver_CommonCentroidPlacementIfCDACFolded == True:
				self._DesignParameter['SRF_CDAC_Pos'] = self._SrefElementDeclaration(
					_DesignObj=H02_01_CDACWtDriver_Fold1_CC._CDACWtDriverFold1(_DesignParameter=None,
																			   _Name='{}:SRF_CDAC_Pos'.format(_Name)))[0]
			else:
				self._DesignParameter['SRF_CDAC_Pos'] = self._SrefElementDeclaration(
					_DesignObj=H02_01_CDACWtDriver_Fold1_DrvArranged._CDACWtDriverFold1(_DesignParameter=None,
																						_Name='{}:SRF_CDAC_Pos'.format(_Name)))[0]
		else:
			self._DesignParameter['SRF_CDAC_Pos'] = self._SrefElementDeclaration(
				_DesignObj=H02_01_CDACWtDriver_Unfolded._CDACWtDriver_Unfolded(_DesignParameter=None,
																			   _Name='{}:SRF_CDAC_Pos'.format(_Name)))[0]

		## Define Sref Reflection: ex)self._DesignParameter['_NMOS_POWER']['_Reflect'] = [0, 0, 0]
		self._DesignParameter['SRF_CDAC_Pos']['_Reflect'] = [0, 0, 0]

		## Define Sref Angle: ex)'_NMOS_POWER'
		self._DesignParameter['SRF_CDAC_Pos']['_Angle'] = 0

		## Calculate Sref Layer by using Calculation_Parameter: ex)'_NMOS_POWER'
		self._DesignParameter['SRF_CDAC_Pos']['_DesignObj']._CalculateDesignParameter(
			**_Caculation_Parameters0)

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
		if _CDAC_Folding == True:
			if _Driver_CommonCentroidPlacementIfCDACFolded == True:
				tmp2x = self.get_param_KJH4('SRF_CDAC_Pos', 'BND_CDACFold1_B{}_DrvInput_Vtc_M2'.format(_NumofCbit - 1))
			else:
				tmp2x = self.get_param_KJH4('SRF_CDAC_Pos', 'BND_CDACFold1_B{}_DrvOutput_Vtc_M2'.format(_NumofCbit - 1))
			# tmp2y = self.get_param_KJH4('SRF_CDAC_Pos', 'SRF_CDAC_LowerHalf', 'SRF_DriverArray', 'BND_{}C_Driver_Input_Hrz_M3'.format(1))
			tmp2y_1 = self.get_param_KJH4('SRF_CDAC_Pos', 'BND_CDACFold1_{}B{}_DrvInput_Hrz_M3'.format('Lo', 0))
			# approaching_coord = [tmp2x[0][0][0]['_XY_left'][0], tmp2y[0][0][0][0][0]['_XY_down'][1]]
			approaching_coord = [tmp2x[0][0][0]['_XY_left'][0], tmp2y_1[0][0][0]['_XY_down'][1]]
		else:
			tmp2x = self.get_param_KJH4('SRF_CDAC_Pos', 'BND_CDACTopNode_Hrz_M7')
			tmp2y = self.get_param_KJH4('SRF_CDAC_Pos', 'SRF_CDACWtDriver', 'SRF_DriverArray', 'BND_{}C_Driver_Input_Hrz_M3'.format(1))
			approaching_coord = [tmp2x[0][0][0]['_XY_left'][0], tmp2y[0][0][0][0][0]['_XY_down'][1]]
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


		print('###############################################')
		print('##              CDAC (Negative)              ##')
		print('##            Calculation_Start!!            ##')
		print('###############################################')

		## CDAC (Negative)
		if _CDAC_Folding == True:
			if _Driver_CommonCentroidPlacementIfCDACFolded == True:
				self._DesignParameter['SRF_CDAC_Neg'] = self._SrefElementDeclaration(
					_DesignObj=H02_01_CDACWtDriver_Fold1_CC._CDACWtDriverFold1(_DesignParameter=None,
																			   _Name='{}:SRF_CDAC_Neg'.format(_Name)))[0]
			else:
				self._DesignParameter['SRF_CDAC_Neg'] = self._SrefElementDeclaration(
					_DesignObj=H02_01_CDACWtDriver_Fold1_DrvArranged._CDACWtDriverFold1(_DesignParameter=None,
																						_Name='{}:SRF_CDAC_Neg'.format(
																							_Name)))[0]
		else:
			self._DesignParameter['SRF_CDAC_Neg'] = self._SrefElementDeclaration(
				_DesignObj=H02_01_CDACWtDriver_Unfolded._CDACWtDriver_Unfolded(_DesignParameter=None,
																			   _Name='{}:SRF_CDAC_Neg'.format(_Name)))[0]

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
		if _CDAC_Folding == True:
			if _Driver_CommonCentroidPlacementIfCDACFolded == True:
				tmp2x = self.get_param_KJH4('SRF_CDAC_Neg', 'BND_CDACFold1_B{}_DrvInput_Vtc_M2'.format(_NumofCbit - 1))
			else:
				tmp2x = self.get_param_KJH4('SRF_CDAC_Neg', 'BND_CDACFold1_B{}_DrvOutput_Vtc_M2'.format(_NumofCbit - 1))
			# tmp2y = self.get_param_KJH4('SRF_CDAC_Neg', 'SRF_CDAC_LowerHalf','SRF_DriverArray', 'BND_{}C_Driver_Input_Hrz_M3'.format(1))
			tmp2y_1 = self.get_param_KJH4('SRF_CDAC_Neg', 'BND_CDACFold1_{}B{}_DrvInput_Hrz_M3'.format('Lo', 0))
			# approaching_coord = [tmp2x[0][0][0]['_XY_left'][0], tmp2y[0][0][0][0][0]['_XY_down'][1]]
			approaching_coord = [tmp2x[0][0][0]['_XY_left'][0], tmp2y_1[0][0][0]['_XY_down'][1]]
		else:
			tmp2x = self.get_param_KJH4('SRF_CDAC_Neg', 'BND_CDACTopNode_Hrz_M7')
			tmp2y = self.get_param_KJH4('SRF_CDAC_Neg', 'SRF_CDACWtDriver', 'SRF_DriverArray', 'BND_{}C_Driver_Input_Hrz_M3'.format(1))
			approaching_coord = [tmp2x[0][0][0]['_XY_left'][0], tmp2y[0][0][0][0][0]['_XY_down'][1]]
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

		print('###############################################')
		print('##     Bootstrapped Switch (Positive)        ##')
		print('##            Calculation_Start!!            ##')
		print('###############################################')

		############ BootSW Generation
		## Bootstrap Sampler SREF Generation
		## Copy Calculation_Parameters from low-level-block ex)copy.deepcopy(B16_nmos_power_v2._NMOS_POWER._ParametersForDesignCalculation)
		_Caculation_Parameters = copy.deepcopy(C13_01_CtopCbotRouted_YJ_v01_00._CtopCbotRouted._ParametersForDesignCalculation)
		_Caculation_Parameters['_Inputnode_width'] = _Samp_Inputnode_width
		_Caculation_Parameters['_Outputnode_width'] = _Samp_Outputnode_width

		_Caculation_Parameters['_Tr1_NumberofGate'] = _Samp_Tr1_NumberofGate
		_Caculation_Parameters['_Tr1_ChannelWidth'] = _Samp_Tr1_ChannelWidth
		_Caculation_Parameters['_Tr1_ChannelLength'] = _Samp_Tr1_ChannelLength
		_Caculation_Parameters['_Tr1_XVT'] = _Samp_Tr1_XVT

		_Caculation_Parameters['_Tr2_NumberofGate'] = _Samp_Tr2_NumberofGate
		_Caculation_Parameters['_Tr2_ChannelWidth'] = _Samp_Tr2_ChannelWidth
		_Caculation_Parameters['_Tr2_ChannelLength'] = _Samp_Tr2_ChannelLength
		_Caculation_Parameters['_Tr2_XVT'] = _Samp_Tr2_XVT

		_Caculation_Parameters['_Tr4_NumberofGate'] = _Samp_Tr4_NumberofGate
		_Caculation_Parameters['_Tr4_ChannelWidth'] = _Samp_Tr4_ChannelWidth
		_Caculation_Parameters['_Tr4_ChannelLength'] = _Samp_Tr4_ChannelLength
		_Caculation_Parameters['_Tr4_XVT'] = _Samp_Tr4_XVT

		_Caculation_Parameters['_Tr5_NumberofGate'] = _Samp_Tr5_NumberofGate
		_Caculation_Parameters['_Tr5_ChannelWidth'] = _Samp_Tr5_ChannelWidth
		_Caculation_Parameters['_Tr5_ChannelLength'] = _Samp_Tr5_ChannelLength
		_Caculation_Parameters['_Tr5_XVT'] = _Samp_Tr5_XVT

		_Caculation_Parameters['_Tr7_NumberofGate'] = _Samp_Tr7_NumberofGate
		_Caculation_Parameters['_Tr7_ChannelWidth'] = _Samp_Tr7_ChannelWidth
		_Caculation_Parameters['_Tr7_ChannelLength'] = _Samp_Tr7_ChannelLength
		_Caculation_Parameters['_Tr7_XVT'] = _Samp_Tr7_XVT

		_Caculation_Parameters['_Tr9_NumberofGate'] = _Samp_Tr9_NumberofGate
		_Caculation_Parameters['_Tr9_ChannelWidth'] = _Samp_Tr9_ChannelWidth
		_Caculation_Parameters['_Tr9_ChannelLength'] = _Samp_Tr9_ChannelLength
		_Caculation_Parameters['_Tr9_XVT'] = _Samp_Tr9_XVT

		_Caculation_Parameters['_Tr8_NumberofGate'] = _Samp_Tr8_NumberofGate
		_Caculation_Parameters['_Tr8_ChannelWidth'] = _Samp_Tr8_ChannelWidth
		_Caculation_Parameters['_Tr8_ChannelLength'] = _Samp_Tr8_ChannelLength
		_Caculation_Parameters['_Tr8_XVT'] = _Samp_Tr8_XVT

		_Caculation_Parameters['_Tr6_NumberofGate'] = _Samp_Tr6_NumberofGate
		_Caculation_Parameters['_Tr6_ChannelWidth'] = _Samp_Tr6_ChannelWidth
		_Caculation_Parameters['_Tr6_ChannelLength'] = _Samp_Tr6_ChannelLength
		_Caculation_Parameters['_Tr6_XVT'] = _Samp_Tr6_XVT

		_Caculation_Parameters['_Tr11_NumberofGate'] = _Samp_Tr11_NumberofGate
		_Caculation_Parameters['_Tr11_ChannelWidth'] = _Samp_Tr11_ChannelWidth
		_Caculation_Parameters['_Tr11_ChannelLength'] = _Samp_Tr11_ChannelLength
		_Caculation_Parameters['_Tr11_XVT'] = _Samp_Tr11_XVT

		_Caculation_Parameters['_Tie4N_NumberofGate'] = _Samp_Tie4N_NumberofGate
		_Caculation_Parameters['_Tie4N_ChannelWidth'] = _Samp_Tie4N_ChannelWidth
		_Caculation_Parameters['_Tie4N_ChannelLength'] = _Samp_Tie4N_ChannelLength
		_Caculation_Parameters['_Tie4N_XVT'] = _Samp_Tie4N_XVT

		_Caculation_Parameters['_Tie4P_NumberofGate'] = _Samp_Tie4P_NumberofGate
		_Caculation_Parameters['_Tie4P_ChannelWidth'] = _Samp_Tie4P_ChannelWidth
		_Caculation_Parameters['_Tie4P_ChannelLength'] = _Samp_Tie4P_ChannelLength
		_Caculation_Parameters['_Tie4P_XVT'] = _Samp_Tie4P_XVT

		_Caculation_Parameters['_Tie8N_NumberofGate'] = _Samp_Tie8N_NumberofGate
		_Caculation_Parameters['_Tie8N_ChannelWidth'] = _Samp_Tie8N_ChannelWidth
		_Caculation_Parameters['_Tie8N_ChannelLength'] = _Samp_Tie8N_ChannelLength
		_Caculation_Parameters['_Tie8N_XVT'] = _Samp_Tie8N_XVT

		_Caculation_Parameters['_Tie8P_NumberofGate'] = _Samp_Tie8P_NumberofGate
		_Caculation_Parameters['_Tie8P_ChannelWidth'] = _Samp_Tie8P_ChannelWidth
		_Caculation_Parameters['_Tie8P_ChannelLength'] = _Samp_Tie8P_ChannelLength
		_Caculation_Parameters['_Tie8P_XVT'] = _Samp_Tie8P_XVT

		_Caculation_Parameters['_Tr12_NumberofGate'] = _Samp_Tr12_NumberofGate
		_Caculation_Parameters['_Tr12_ChannelWidth'] = _Samp_Tr12_ChannelWidth
		_Caculation_Parameters['_Tr12_ChannelLength'] = _Samp_Tr12_ChannelLength
		_Caculation_Parameters['_Tr12_XVT'] = _Samp_Tr12_XVT

		_Caculation_Parameters['_Tr3_NumberofGate'] = _Samp_Tr3_NumberofGate
		_Caculation_Parameters['_Tr3_ChannelWidth'] = _Samp_Tr3_ChannelWidth
		_Caculation_Parameters['_Tr3_ChannelLength'] = _Samp_Tr3_ChannelLength
		_Caculation_Parameters['_Tr3_XVT'] = _Samp_Tr3_XVT

		_Caculation_Parameters['_Tr10_NumberofGate'] = _Samp_Tr10_NumberofGate
		_Caculation_Parameters['_Tr10_ChannelWidth'] = _Samp_Tr10_ChannelWidth
		_Caculation_Parameters['_Tr10_ChannelLength'] = _Samp_Tr10_ChannelLength
		_Caculation_Parameters['_Tr10_XVT'] = _Samp_Tr10_XVT

		_Caculation_Parameters['_HDVNCAP_Length'] = _Samp_HDVNCAP_Length
		_Caculation_Parameters['_HDVNCAP_LayoutOption'] = _Samp_HDVNCAP_LayoutOption
		_Caculation_Parameters['_HDVNCAP_NumFigPair'] = _Samp_HDVNCAP_NumFigPair
		_Caculation_Parameters['_HDVNCAP_Array'] = _Samp_HDVNCAP_Array
		_Caculation_Parameters['_HDVNCAP_Cbot_Ctop_metalwidth'] = _Samp_HDVNCAP_Cbot_Ctop_metalwidth

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

		print('###############################################')
		print('##     Bootstrapped Switch (Negative)        ##')
		print('##            Calculation_Start!!            ##')
		print('###############################################')

		## BootSW (Negative) Placement
		## Generate Sref: ex)self._DesignParameter['_NMOS_POWER'] = self._SrefElementDeclaration(_DesignObj=B16_nmos_power_v2._NMOS_POWER( _DesignParameter=None, _Name='{}:NMOS_POWER'.format(_Name)))[0]
		self._DesignParameter['SRF_BootSW_Neg'] = self._SrefElementDeclaration(_DesignObj=C13_01_CtopCbotRouted_YJ_v01_00._CtopCbotRouted(_DesignParameter=None, _Name='{}:SRF_BootSW_Neg'.format(_Name)))[0]


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
		if _CDAC_Folding == True:
			tmp2 = self.get_param_KJH4('SRF_CDAC_Pos', 'BND_CDACTopNode_Vtc_M7')
			self._DesignParameter['BND_SampOutput2CDACTop_Pos_Vtc_M6']['_YWidth'] = abs(tmp1[0][0][0]['_XY_cent'][1] - tmp2[0][0][0]['_XY_cent'][1])
		else:
			tmp2 = self.get_param_KJH4('SRF_CDAC_Pos', 'BND_CDACTopNode_Hrz_M7')
			self._DesignParameter['BND_SampOutput2CDACTop_Pos_Vtc_M6']['_YWidth'] = abs(tmp1[0][0][0]['_XY_cent'][1] - tmp2[0][0][0]['_XY_down'][1])

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
		if _CDAC_Folding == True:
			tmp2 = self.get_param_KJH4('SRF_CDAC_Neg', 'BND_CDACTopNode_Vtc_M7')
			self._DesignParameter['BND_SampOutput2CDACTop_Neg_Vtc_M6']['_YWidth'] = abs(tmp1[0][0][0]['_XY_cent'][1] - tmp2[0][0][0]['_XY_cent'][1])
		else:
			tmp2 = self.get_param_KJH4('SRF_CDAC_Neg', 'BND_CDACTopNode_Hrz_M7')
			self._DesignParameter['BND_SampOutput2CDACTop_Neg_Vtc_M6']['_YWidth'] = abs(tmp1[0][0][0]['_XY_cent'][1] - tmp2[0][0][0]['_XY_down'][1])

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
		if _CDAC_Folding == True:
			## Define Boundary_element _YWidth
			self._DesignParameter['BND_SampOutput2CDACTop_Hrz_M7']['_YWidth'] = 400
			tmp2 = self.get_param_KJH4('SRF_CDAC_Pos', 'BND_CDACTopNode_Vtc_M7')
		else:
			## Define Boundary_element _YWidth
			tmp2 = self.get_param_KJH4('SRF_CDAC_Pos', 'BND_CDACTopNode_Hrz_M7')
			self._DesignParameter['BND_SampOutput2CDACTop_Hrz_M7']['_YWidth'] = tmp2[0][0][0]['_Ywidth']

		## Define Boundary_element _XWidth
		tmp1 = self.get_param_KJH4('BND_SampOutput2CDACTop_Pos_Vtc_M6')
		self._DesignParameter['BND_SampOutput2CDACTop_Hrz_M7']['_XWidth'] = abs(tmp1[0][0]['_XY_left'][0] - tmp2[0][0][0]['_XY_right'][0])

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
			if _CDAC_Folding == True:
				tmp1 = self.get_param_KJH4('SRF_CDAC_Pos','BND_CDACFold1_{}B{}_DrvInput_Hrz_M3'.format('Lo', _NumofCbit - 1 - j))
				self._DesignParameter['BND_CDAC_Pos_MSB{}DrvIn_Hrz_M3'.format(j)]['_YWidth'] = tmp1[0][0][0]['_Ywidth']
			else:
				tmp1 = self.get_param_KJH4('SRF_CDAC_Pos', 'SRF_CDACWtDriver', 'SRF_DriverArray', 'BND_{}C_Driver_Input_Hrz_M3'.format(2 ** (_NumofCbit - 1 - j)))
				self._DesignParameter['BND_CDAC_Pos_MSB{}DrvIn_Hrz_M3'.format(j)]['_YWidth'] = tmp1[0][0][0][0][0]['_Ywidth']

			## Define Boundary_element _XWidth
			if _CDAC_Folding == True:
				tmp2 = self.get_param_KJH4('SRF_SARLogicWtComparator', 'SRF_SARLogicWtBuffers', 'SRF_UpperCDACPreDriver',
										   'SRF_InvChain{}'.format(j), 'SRF_Output_ViaM2Mx', 'SRF_ViaM2M3', 'BND_Met2Layer')
				self._DesignParameter['BND_CDAC_Pos_MSB{}DrvIn_Hrz_M3'.format(j)]['_XWidth'] = \
					tmp2[0][0][0][0][0][0][0][0]['_XY_right'][0] - tmp1[0][0][0]['_XY_left'][0]
			else:
				tmp2 = self.get_param_KJH4('SRF_SARLogicWtComparator', 'SRF_SARLogicWtBuffers', 'SRF_UpperCDACPreDriver',
										   'SRF_InvChain{}'.format(j), 'SRF_Output_ViaM2Mx', 'SRF_ViaM2M3', 'BND_Met2Layer')
				self._DesignParameter['BND_CDAC_Pos_MSB{}DrvIn_Hrz_M3'.format(j)]['_XWidth'] = \
					tmp2[0][0][0][0][0][0][0][0]['_XY_right'][0] - tmp1[0][0][0][0][0]['_XY_left'][0]

			if self._DesignParameter['BND_CDAC_Pos_MSB{}DrvIn_Hrz_M3'.format(j)]['_XWidth'] < 0:
				self._DesignParameter['BND_CDAC_Pos_MSB{}DrvIn_Hrz_M3'.format(j)]['_XWidth'] = self._DesignParameter['BND_CDAC_Pos_MSB{}DrvIn_Hrz_M3'.format(j)]['_XWidth'] - 244

			## Calculate Sref XYcoord
			tmpXY = []
			## initialized Sref coordinate
			self._DesignParameter['BND_CDAC_Pos_MSB{}DrvIn_Hrz_M3'.format(j)]['_XYCoordinates'] = [[0, 0]]
			if _CDAC_Folding == True:
				target_coord = tmp1[0][0][0]['_XY_down_left']
			else:
				target_coord = tmp1[0][0][0][0][0]['_XY_down_left']
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
			tmp2 = self.get_param_KJH4('SRF_SARLogicWtComparator', 'SRF_SARLogicWtBuffers', 'SRF_UpperCDACPreDriver', 'SRF_InvChain{}'.format(_NumofCbit - 1 - j), 'SRF_Output_ViaM2Mx', 'SRF_ViaM2M3', 'BND_Met2Layer')
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
			if _CDAC_Folding == True:
				tmp1 = self.get_param_KJH4('SRF_CDAC_Neg', 'BND_CDACFold1_{}B{}_DrvInput_Hrz_M3'.format('Lo', _NumofCbit - 1 - j))
				self._DesignParameter['BND_CDAC_Neg_MSB{}DrvIn_Hrz_M3'.format(j)]['_YWidth'] = tmp1[0][0][0]['_Ywidth']
			else:
				tmp1 = self.get_param_KJH4('SRF_CDAC_Neg', 'SRF_CDACWtDriver', 'SRF_DriverArray', 'BND_{}C_Driver_Input_Hrz_M3'.format(2 ** (_NumofCbit - 1 - j)))
				self._DesignParameter['BND_CDAC_Neg_MSB{}DrvIn_Hrz_M3'.format(j)]['_YWidth'] = tmp1[0][0][0][0][0]['_Ywidth']

			## Define Boundary_element _XWidth
			if _CDAC_Folding == True:
				tmp2 = self.get_param_KJH4('SRF_SARLogicWtComparator', 'SRF_SARLogicWtBuffers', 'SRF_LowerCDACPreDriver', 'SRF_InvChain{}'.format(j), 'SRF_Output_ViaM2Mx', 'SRF_ViaM2M3', 'BND_Met2Layer')
				self._DesignParameter['BND_CDAC_Neg_MSB{}DrvIn_Hrz_M3'.format(j)]['_XWidth'] = tmp2[0][0][0][0][0][0][0][0]['_XY_right'][0] - tmp1[0][0][0]['_XY_left'][0]
			else:
				tmp2 = self.get_param_KJH4('SRF_SARLogicWtComparator', 'SRF_SARLogicWtBuffers', 'SRF_LowerCDACPreDriver', 'SRF_InvChain{}'.format(j), 'SRF_Output_ViaM2Mx', 'SRF_ViaM2M3', 'BND_Met2Layer')
				self._DesignParameter['BND_CDAC_Neg_MSB{}DrvIn_Hrz_M3'.format(j)]['_XWidth'] = tmp2[0][0][0][0][0][0][0][0]['_XY_right'][0] - tmp1[0][0][0][0][0]['_XY_left'][0]

			if self._DesignParameter['BND_CDAC_Neg_MSB{}DrvIn_Hrz_M3'.format(j)]['_XWidth'] < 0:
				self._DesignParameter['BND_CDAC_Neg_MSB{}DrvIn_Hrz_M3'.format(j)]['_XWidth'] = \
					self._DesignParameter['BND_CDAC_Neg_MSB{}DrvIn_Hrz_M3'.format(j)]['_XWidth'] - 244

			## Calculate Sref XYcoord
			tmpXY = []
			## initialized Sref coordinate
			self._DesignParameter['BND_CDAC_Neg_MSB{}DrvIn_Hrz_M3'.format(j)]['_XYCoordinates'] = [[0, 0]]
			## Calculate
			## Target_coord: _XY_type1
			if _CDAC_Folding == True:
				target_coord = tmp1[0][0][0]['_XY_up_left']
			else:
				target_coord = tmp1[0][0][0][0][0]['_XY_up_left']
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
			tmp2 = self.get_param_KJH4('SRF_SARLogicWtComparator', 'SRF_SARLogicWtBuffers', 'SRF_LowerCDACPreDriver', 'SRF_InvChain{}'.format(_NumofCbit - 1 - j), 'SRF_Output_ViaM2Mx', 'SRF_ViaM2M3', 'BND_Met2Layer')
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

		#### Comp Input P Via M6M7
		## Sref generation: ViaX
		## Define ViaX Parameter
		_Caculation_Parameters = copy.deepcopy(A02_ViaStack_KJH3._ViaStack._ParametersForDesignCalculation)
		_Caculation_Parameters['_Layer1'] = 6
		_Caculation_Parameters['_Layer2'] = 7
		_Caculation_Parameters['_COX'] = _COX
		_Caculation_Parameters['_COY'] = _COY

		## Sref ViaX declaration
		self._DesignParameter['SRF_CompInputN_ViaM6M7'] = self._SrefElementDeclaration(
			_DesignObj=A02_ViaStack_KJH3._ViaStack(_DesignParameter=None, _Name='{}:SRF_CompInputN_ViaM6M7'.format(_Name)))[0]

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

		#### Comp Input N Via M6M7
		## Sref generation: ViaX
		## Define ViaX Parameter
		_Caculation_Parameters = copy.deepcopy(A02_ViaStack_KJH3._ViaStack._ParametersForDesignCalculation)
		_Caculation_Parameters['_Layer1'] = 6
		_Caculation_Parameters['_Layer2'] = 7
		_Caculation_Parameters['_COX'] = _COX
		_Caculation_Parameters['_COY'] = _COY

		## Sref ViaX declaration
		self._DesignParameter['SRF_CompInputP_ViaM6M7'] = self._SrefElementDeclaration(
			_DesignObj=A02_ViaStack_KJH3._ViaStack(_DesignParameter=None, _Name='{}:SRF_CompInputP_ViaM6M7'.format(_Name)))[0]

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
		if _CDAC_Folding == True:
			tmp2 = self.get_param_KJH4('SRF_CDAC_Pos', 'BND_CDACUpperTopNode_Hrz_IA')
		else:
			tmp2 = self.get_param_KJH4('SRF_CDAC_Pos', 'BND_CDACTopNode_Hrz_M7')
		self._DesignParameter['BND_CompInputP_Vtc_IA']['_YWidth'] = abs(tmp1[0][0]['_XY_up'][1] - tmp2[0][0][0]['_XY_up'][1])

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
		if _CDAC_Folding == True:
			tmp2 = self.get_param_KJH4('SRF_CDAC_Neg', 'BND_CDACUpperTopNode_Hrz_IA')
		else:
			tmp2 = self.get_param_KJH4('SRF_CDAC_Neg', 'BND_CDACTopNode_Hrz_M7')
		self._DesignParameter['BND_CompInputN_Vtc_IA']['_YWidth'] = abs(tmp1[0][0]['_XY_down'][1] - tmp2[0][0][0]['_XY_up'][1])

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

		if _CDAC_Folding == True:
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
			tmp1_1 = self.get_param_KJH4('SRF_CDAC_Pos', 'BND_CDACLowerTopNode_Hrz_IA')
			tmp1_2 = self.get_param_KJH4('SRF_CDAC_Pos', 'BND_CDACUpperTopNode_Hrz_IA')
			tmp1_3 = self.get_param_KJH4('SRF_CDAC_Neg', 'BND_CDACUpperTopNode_Hrz_IA')
			tmp1_4 = self.get_param_KJH4('SRF_CDAC_Neg', 'BND_CDACLowerTopNode_Hrz_IA')
			tmp2 = self.get_param_KJH4('BND_CompInputN_Vtc_IA')
			self._DesignParameter['BND_CompInputExten_Hrz_IA']['_YWidth'] = tmp1_1[0][0][0]['_Ywidth']

			## Define Boundary_element _XWidth
			self._DesignParameter['BND_CompInputExten_Hrz_IA']['_XWidth'] = abs(tmp1_1[0][0][0]['_XY_right'][0] - tmp2[0][0]['_XY_left'][0])

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
			target_coord = [tmp2[0][0]['_XY_left'][0], tmp1_1[0][0][0]['_XY_down'][1]]
			New_Scoord = self.get_Scoord_KJH4(target_coord, approaching_coord, Scoord)
			tmpXY.append(New_Scoord)
			## Target_coord2: _XY_type1
			target_coord = [tmp2[0][0]['_XY_left'][0], tmp1_2[0][0][0]['_XY_down'][1]]
			New_Scoord = self.get_Scoord_KJH4(target_coord, approaching_coord, Scoord)
			tmpXY.append(New_Scoord)
			## Target_coord3: _XY_type1
			target_coord = [tmp2[0][0]['_XY_left'][0], tmp1_3[0][0][0]['_XY_up'][1]]
			New_Scoord = self.get_Scoord_KJH4(target_coord, approaching_coord, Scoord)
			tmpXY.append(New_Scoord)
			## Target_coord4: _XY_type1
			target_coord = [tmp2[0][0]['_XY_left'][0], tmp1_4[0][0][0]['_XY_up'][1]]
			New_Scoord = self.get_Scoord_KJH4(target_coord, approaching_coord, Scoord)
			tmpXY.append(New_Scoord)
			## Define coordinates
			self._DesignParameter['BND_CompInputExten_Hrz_IA']['_XYCoordinates'] = tmpXY

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

		#### Bootstrapped Sampler CLKB Inverter generation
		## Copy Calculation_Parameters from low-level-block ex)copy.deepcopy(B16_nmos_power_v2._NMOS_POWER._ParametersForDesignCalculation)
		_Caculation_Parameters = copy.deepcopy(D00_00_Inverter_KJH._Inverter._ParametersForDesignCalculation)
		## Define Calculation_Parameters ex) _Caculation_Parameters['_NMOSPOWER_PbodyContact_1_Length']  = _NMOSPOWER_PbodyContact_1_Length
		_Caculation_Parameters['_NMOS_MosType'] = 'NMOS'
		_Caculation_Parameters['_NMOS_MosUpDn'] = 'Up'

		_Caculation_Parameters['_NMOS_NumberofGate'] = _CLKBInv_NMOS_NumberofGate
		_Caculation_Parameters['_NMOS_ChannelWidth'] = _CLKBInv_NMOS_ChannelWidth
		_Caculation_Parameters['_NMOS_ChannelLength'] = _CLKBInv_NMOS_ChannelLength
		_Caculation_Parameters['_NMOS_GateSpacing'] = None
		_Caculation_Parameters['_NMOS_SDWidth'] = None
		_Caculation_Parameters['_NMOS_XVT'] = _CLKBInv_NMOS_XVT
		_Caculation_Parameters['_NMOS_PCCrit'] = True

		_Caculation_Parameters['_NMOS_Source_Via_TF'] = False
		_Caculation_Parameters['_NMOS_Source_Via_Close2POpin_TF'] = False
		_Caculation_Parameters['_NMOS_Source_Comb_TF'] = False
		_Caculation_Parameters['_NMOS_Source_Comb_POpinward_TF'] = False
		_Caculation_Parameters['_NMOS_Source_Comb_Length'] = None

		_Caculation_Parameters['_NMOS_Drain_Via_TF'] = True
		_Caculation_Parameters['_NMOS_Drain_Via_Close2POpin_TF'] = True
		_Caculation_Parameters['_NMOS_Drain_Comb_TF'] = True
		_Caculation_Parameters['_NMOS_Drain_Comb_POpinward_TF'] = True
		_Caculation_Parameters['_NMOS_Drain_Comb_Length'] = 0

		_Caculation_Parameters['_NMOS_PODummy_TF'] = True
		_Caculation_Parameters['_NMOS_PODummy_Length'] = None
		_Caculation_Parameters['_NMOS_PODummy_Placement'] = None

		_Caculation_Parameters['_NMOS_Xvt_MinExten_TF'] = False
		_Caculation_Parameters['_NMOS_Xvt_Placement'] = 'Up'

		_Caculation_Parameters['_NMOS_POGate_Comb_TF'] = True
		_Caculation_Parameters['_NMOS_POGate_Comb_length'] = _CLKBInv_NMOS_POGate_Comb_length
		_Caculation_Parameters['_NMOS_POGate_Via_TF'] = True
		_Caculation_Parameters['_NMOS_POGate_ViaMxMx'] = [0, 1]

		_Caculation_Parameters['_PMOS_MosType'] = 'PMOS'
		_Caculation_Parameters['_PMOS_MosUpDn'] = 'Dn'

		_Caculation_Parameters['_PMOS_NumberofGate'] = _CLKBInv_PMOS_NumberofGate
		_Caculation_Parameters['_PMOS_ChannelWidth'] = _CLKBInv_Inv_PMOS_ChannelWidth
		_Caculation_Parameters['_PMOS_ChannelLength'] = _CLKBInv_PMOS_ChannelLength
		_Caculation_Parameters['_PMOS_GateSpacing'] = None
		_Caculation_Parameters['_PMOS_SDWidth'] = None
		_Caculation_Parameters['_PMOS_XVT'] = _CLKBInv_PMOS_XVT
		_Caculation_Parameters['_PMOS_PCCrit'] = True

		_Caculation_Parameters['_PMOS_Source_Via_TF'] = False
		_Caculation_Parameters['_PMOS_Source_Via_Close2POpin_TF'] = False
		_Caculation_Parameters['_PMOS_Source_Comb_TF'] = False
		_Caculation_Parameters['_PMOS_Source_Comb_POpinward_TF'] = False
		_Caculation_Parameters['_PMOS_Source_Comb_Length'] = None

		_Caculation_Parameters['_PMOS_Drain_Via_TF'] = True
		_Caculation_Parameters['_PMOS_Drain_Via_Close2POpin_TF'] = True
		_Caculation_Parameters['_PMOS_Drain_Comb_TF'] = True
		_Caculation_Parameters['_PMOS_Drain_Comb_POpinward_TF'] = True
		_Caculation_Parameters['_PMOS_Drain_Comb_Length'] = 0

		_Caculation_Parameters['_PMOS_PODummy_TF'] = True
		_Caculation_Parameters['_PMOS_PODummy_Length'] = None
		_Caculation_Parameters['_PMOS_PODummy_Placement'] = None

		_Caculation_Parameters['_PMOS_Xvt_MinExten_TF'] = False
		_Caculation_Parameters['_PMOS_Xvt_Placement'] = 'Dn'

		_Caculation_Parameters['_PMOS_POGate_Comb_TF'] = True
		_Caculation_Parameters['_PMOS_POGate_Comb_length'] = _CLKBInv_PMOS_POGate_Comb_length
		_Caculation_Parameters['_PMOS_POGate_Via_TF'] = True
		_Caculation_Parameters['_PMOS_POGate_ViaMxMx'] = [0, 1]

		_Caculation_Parameters['_NMOS_Pbody_NumCont'] = _CLKBInv_Pbody_NumCont
		_Caculation_Parameters['_NMOS_Pbody_XvtTop2Pbody'] = _CLKBInv_XvtTop2Pbody
		_Caculation_Parameters['_PMOS_Nbody_NumCont'] = _CLKBInv_Nbody_NumCont
		_Caculation_Parameters['_PMOS_Nbody_Xvtdown2Nbody'] = _CLKBInv_Xvtdown2Nbody
		_Caculation_Parameters['_PMOSXvt2NMOSXvt'] = _CLKBInv_PMOSXvt2NMOSXvt

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

		## SRF_CLKBInvIn_ViaM3M4
		## Sref generation: ViaX
		## Define ViaX Parameter
		_Caculation_Parameters = copy.deepcopy(A02_ViaStack_KJH3._ViaStack._ParametersForDesignCalculation)
		_Caculation_Parameters['_Layer1'] = 3
		_Caculation_Parameters['_Layer2'] = 4
		_Caculation_Parameters['_COX'] = 1
		_Caculation_Parameters['_COY'] = 3

		## Sref ViaX declaration
		self._DesignParameter['SRF_CLKBInvIn_ViaM3M4'] = self._SrefElementDeclaration(
			_DesignObj=A02_ViaStack_KJH3._ViaStack(_DesignParameter=None,
												   _Name='{}:SRF_CLKBInvIn_ViaM3M4'.format(_Name)))[0]

		## Define Sref Relection
		self._DesignParameter['SRF_CLKBInvIn_ViaM3M4']['_Reflect'] = [0, 0, 0]

		## Define Sref Angle
		self._DesignParameter['SRF_CLKBInvIn_ViaM3M4']['_Angle'] = 0

		## Generate Metal(x), Metal(x+1) and C0(Viax) layer:  Option: _CalculateDesignParameter, _CalculateDesignParameterXmin, _CalculateDesignParameterYmin, _CalculateDesignParameterXYsame
		self._DesignParameter['SRF_CLKBInvIn_ViaM3M4']['_DesignObj']._CalculateDesignParameterXmin(
			**_Caculation_Parameters)

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

		## SRF_CLKBInvIn_ViaM1M3
		## Sref generation: ViaX
		## Define ViaX Parameter
		_Caculation_Parameters = copy.deepcopy(A02_ViaStack_KJH3._ViaStack._ParametersForDesignCalculation)
		_Caculation_Parameters['_Layer1'] = 1
		_Caculation_Parameters['_Layer2'] = 3
		_Caculation_Parameters['_COX'] = 1
		_Caculation_Parameters['_COY'] = 2

		## Sref ViaX declaration
		self._DesignParameter['SRF_CLKBInvIn_ViaM1M3'] = self._SrefElementDeclaration(
			_DesignObj=A02_ViaStack_KJH3._ViaStack(_DesignParameter=None,
												   _Name='{}:SRF_CLKBInvIn_ViaM1M3'.format(_Name)))[0]

		## Define Sref Relection
		self._DesignParameter['SRF_CLKBInvIn_ViaM1M3']['_Reflect'] = [0, 0, 0]

		## Define Sref Angle
		self._DesignParameter['SRF_CLKBInvIn_ViaM1M3']['_Angle'] = 0

		## Generate Metal(x), Metal(x+1) and C0(Viax) layer:  Option: _CalculateDesignParameter, _CalculateDesignParameterXmin, _CalculateDesignParameterYmin, _CalculateDesignParameterXYsame
		self._DesignParameter['SRF_CLKBInvIn_ViaM1M3']['_DesignObj']._CalculateDesignParameterXmin(
			**_Caculation_Parameters)

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

		'''
		### Decimation
		if (_Driver_DecimationIfDriverPlacedInCommonCentroid == True):
			for j in range(0, len(_Driver_DecimationFactor)):
				for i in range(0, 2 ** (_NumofCbit - 1 - j), -1):
					tmp = _Driver_DecimationFactor[j]
					if tmp == 0:
						pass
					else:
						if i % tmp != 0:
							del self._DesignParameter['SRF_CDAC_Pos']['_DesignObj']._DesignParameter['SRF_CDACWtDriver']['_DesignObj']._DesignParameter['SRF_DriverArray']['_DesignObj']._DesignParameter['SRF_{}C_DriverCell'.format(2 ** (_NumofCbit - 1 - j))]['_XYCoordinates'][i]
							del self._DesignParameter['SRF_CDAC_Pos']['_DesignObj']._DesignParameter['SRF_CDACWtDriver']['_DesignObj']._DesignParameter['SRF_DriverArray']['_DesignObj']._DesignParameter['BND_{}C_Driver_Input_Vtc_M2'.format(2 ** (_NumofCbit - 1 - j))]['_XYCoordinates'][i]
							del self._DesignParameter['SRF_CDAC_Pos']['_DesignObj']._DesignParameter['SRF_CDACWtDriver']['_DesignObj']._DesignParameter['BND_{}C_Driver_Drain_Vtc_M4'.format(2 ** (_NumofCbit - 1 - j))]['_XYCoordinates'][i]

							del self._DesignParameter['SRF_CDAC_Neg']['_DesignObj']._DesignParameter['SRF_CDACWtDriver']['_DesignObj']._DesignParameter['SRF_DriverArray']['_DesignObj']._DesignParameter['SRF_{}C_DriverCell'.format(2 ** (_NumofCbit - 1 - j))]['_XYCoordinates'][i]
							del self._DesignParameter['SRF_CDAC_Neg']['_DesignObj']._DesignParameter['SRF_CDACWtDriver']['_DesignObj']._DesignParameter['SRF_DriverArray']['_DesignObj']._DesignParameter['BND_{}C_Driver_Input_Vtc_M2'.format(2 ** (_NumofCbit - 1 - j))]['_XYCoordinates'][i]
							del self._DesignParameter['SRF_CDAC_Neg']['_DesignObj']._DesignParameter['SRF_CDACWtDriver']['_DesignObj']._DesignParameter['BND_{}C_Driver_Drain_Vtc_M4'.format(2 ** (_NumofCbit - 1 - j))]['_XYCoordinates'][i]
				else:
					pass
		else:
			pass
		'''

		if (_Driver_DecimationIfDriverPlacedInCommonCentroid == True):
			## No folding
			if (_CDAC_Folding == False):
				for j in range(0, len(_Driver_DecimationFactor)):
					for i in reversed(range(0, 2 ** (_NumofCbit - 1 - j))):
						tmp = _Driver_DecimationFactor[j]
						if tmp == 0:
							pass
						else:
							if i % tmp != 0:
								del self._DesignParameter['SRF_CDAC_Pos']['_DesignObj']._DesignParameter['SRF_CDACWtDriver']['_DesignObj']._DesignParameter['SRF_DriverArray']['_DesignObj']._DesignParameter['SRF_{}C_DriverCell'.format(2 ** (_NumofCbit - 1 - j))]['_XYCoordinates'][i]
								del self._DesignParameter['SRF_CDAC_Pos']['_DesignObj']._DesignParameter['SRF_CDACWtDriver']['_DesignObj']._DesignParameter['SRF_DriverArray']['_DesignObj']._DesignParameter['BND_{}C_Driver_Input_Vtc_M2'.format(2 ** (_NumofCbit - 1 - j))]['_XYCoordinates'][i]
								del self._DesignParameter['SRF_CDAC_Pos']['_DesignObj']._DesignParameter['SRF_CDACWtDriver']['_DesignObj']._DesignParameter['BND_{}C_Driver_Drain_Vtc_M4'.format(2 ** (_NumofCbit - 1 - j))]['_XYCoordinates'][i]

								del self._DesignParameter['SRF_CDAC_Neg']['_DesignObj']._DesignParameter['SRF_CDACWtDriver']['_DesignObj']._DesignParameter['SRF_DriverArray']['_DesignObj']._DesignParameter['SRF_{}C_DriverCell'.format(2 ** (_NumofCbit - 1 - j))]['_XYCoordinates'][i]
								del self._DesignParameter['SRF_CDAC_Neg']['_DesignObj']._DesignParameter['SRF_CDACWtDriver']['_DesignObj']._DesignParameter['SRF_DriverArray']['_DesignObj']._DesignParameter['BND_{}C_Driver_Input_Vtc_M2'.format(2 ** (_NumofCbit - 1 - j))]['_XYCoordinates'][i]
								del self._DesignParameter['SRF_CDAC_Neg']['_DesignObj']._DesignParameter['SRF_CDACWtDriver']['_DesignObj']._DesignParameter['BND_{}C_Driver_Drain_Vtc_M4'.format(2 ** (_NumofCbit - 1 - j))]['_XYCoordinates'][i]
							else:
								pass
			## Folding
			else:
				for j in range(0,len(_Driver_DecimationFactor)):
					for i in reversed(range(0, 2 ** (_NumofCbit - 2 - j))):
						tmp = _Driver_DecimationFactor[j]
						if tmp ==0:
							pass
						else:
							if i % tmp != 0:
								del self._DesignParameter['SRF_CDAC_Pos']['_DesignObj']._DesignParameter['SRF_CDAC_UpperHalf']['_DesignObj']._DesignParameter['SRF_DriverArray']['_DesignObj']._DesignParameter['SRF_{}C_DriverCell'.format(2 ** (_NumofCbit - 2 - j))]['_XYCoordinates'][i]
								del self._DesignParameter['SRF_CDAC_Pos']['_DesignObj']._DesignParameter['SRF_CDAC_UpperHalf']['_DesignObj']._DesignParameter['SRF_DriverArray']['_DesignObj']._DesignParameter['BND_{}C_Driver_Input_Vtc_M2'.format(2 ** (_NumofCbit - 2 - j))]['_XYCoordinates'][i]
								del self._DesignParameter['SRF_CDAC_Pos']['_DesignObj']._DesignParameter['SRF_CDAC_UpperHalf']['_DesignObj']._DesignParameter['BND_{}C_Driver_Drain_Vtc_M4'.format(2 ** (_NumofCbit - 2 - j))]['_XYCoordinates'][i]

								del self._DesignParameter['SRF_CDAC_Pos']['_DesignObj']._DesignParameter['SRF_CDAC_LowerHalf']['_DesignObj']._DesignParameter['SRF_DriverArray']['_DesignObj']._DesignParameter['SRF_{}C_DriverCell'.format(2 ** (_NumofCbit - 2 - j))]['_XYCoordinates'][i]
								del self._DesignParameter['SRF_CDAC_Pos']['_DesignObj']._DesignParameter['SRF_CDAC_LowerHalf']['_DesignObj']._DesignParameter['SRF_DriverArray']['_DesignObj']._DesignParameter['BND_{}C_Driver_Input_Vtc_M2'.format(2 ** (_NumofCbit - 2 - j))]['_XYCoordinates'][i]
								del self._DesignParameter['SRF_CDAC_Pos']['_DesignObj']._DesignParameter['SRF_CDAC_LowerHalf']['_DesignObj']._DesignParameter['BND_{}C_Driver_Drain_Vtc_M4'.format(2 ** (_NumofCbit - 2 - j))]['_XYCoordinates'][i]

								del self._DesignParameter['SRF_CDAC_Neg']['_DesignObj']._DesignParameter['SRF_CDAC_UpperHalf']['_DesignObj']._DesignParameter['SRF_DriverArray']['_DesignObj']._DesignParameter['SRF_{}C_DriverCell'.format(2 ** (_NumofCbit - 2 - j))]['_XYCoordinates'][i]
								del self._DesignParameter['SRF_CDAC_Neg']['_DesignObj']._DesignParameter['SRF_CDAC_UpperHalf']['_DesignObj']._DesignParameter['SRF_DriverArray']['_DesignObj']._DesignParameter['BND_{}C_Driver_Input_Vtc_M2'.format(2 ** (_NumofCbit - 2 - j))]['_XYCoordinates'][i]
								del self._DesignParameter['SRF_CDAC_Neg']['_DesignObj']._DesignParameter['SRF_CDAC_UpperHalf']['_DesignObj']._DesignParameter['BND_{}C_Driver_Drain_Vtc_M4'.format(2 ** (_NumofCbit - 2 - j))]['_XYCoordinates'][i]

								del self._DesignParameter['SRF_CDAC_Neg']['_DesignObj']._DesignParameter['SRF_CDAC_LowerHalf']['_DesignObj']._DesignParameter['SRF_DriverArray']['_DesignObj']._DesignParameter['SRF_{}C_DriverCell'.format(2 ** (_NumofCbit - 2 - j))]['_XYCoordinates'][i]
								del self._DesignParameter['SRF_CDAC_Neg']['_DesignObj']._DesignParameter['SRF_CDAC_LowerHalf']['_DesignObj']._DesignParameter['SRF_DriverArray']['_DesignObj']._DesignParameter['BND_{}C_Driver_Input_Vtc_M2'.format(2 ** (_NumofCbit - 2 - j))]['_XYCoordinates'][i]
								del self._DesignParameter['SRF_CDAC_Neg']['_DesignObj']._DesignParameter['SRF_CDAC_LowerHalf']['_DesignObj']._DesignParameter['BND_{}C_Driver_Drain_Vtc_M4'.format(2 ** (_NumofCbit - 2 - j))]['_XYCoordinates'][i]

							else:
								pass
		else:
			pass






		## ########## ########## ########## ########## ########## ########## ########## ########## ########## ########## ########## ########## SRF_RDACandDecoder_Pos
		## ########## ########## ########## ########## ########## ########## ########## ########## ########## ########## ########## SRF_RDACandDecoder_Pos: Gen and placement
		## Copy Calculation_Parameters from low-level-block ex)copy.deepcopy(B16_nmos_power_v2._NMOS_POWER._ParametersForDesignCalculation)
		_Caculation_Parameters = copy.deepcopy(R00_00_Combine_KJH4._Combine._ParametersForDesignCalculation)
		## Define Calculation_Parameters ex) _Caculation_Parameters['_NMOSPOWER_PbodyContact_1_Length']  = _NMOSPOWER_PbodyContact_1_Length
		_Caculation_Parameters['_RDAC_Pside'] = True

		_Caculation_Parameters['_RDAC_displacement'] = _RDAC_displacement

		_Caculation_Parameters['_RDAC_Size'] = _RDAC_Size

		_Caculation_Parameters['RDAC_Guard_NumCont'] = RDAC_Guard_NumCont
		_Caculation_Parameters['RDAC_ResWidth'] = RDAC_ResWidth
		_Caculation_Parameters['RDAC_ResLength'] = RDAC_ResLength

		_Caculation_Parameters['RDAC_CONUMX'] = RDAC_CONUMX
		_Caculation_Parameters['RDAC_CONUMY'] = RDAC_CONUMY

		_Caculation_Parameters['_Decoder_Unit2UnitDist'] = _Decoder_Unit2UnitDist

		_Caculation_Parameters['_Decoder_RBit'] = _NumofRbit

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
		if (_CDAC_Folding == False):
			tmp1_1 = self.get_param_KJH4('SRF_CDAC_Pos', 'SRF_CDACWtDriver', 'SRF_CapArray', 'SRF_DummyCaps', 'SRF_CapWtShield4DCAP', 'BND_Shield_Extend_VTC_M{}'.format(_CDAC_ShieldingLayer))
		else:
			tmp1_1 = self.get_param_KJH4('SRF_CDAC_Pos', 'SRF_CDAC_LowerHalf', 'SRF_CapArray', 'SRF_DummyCaps', 'SRF_CapWtShield4DCAP', 'BND_Shield_Extend_VTC_M{}'.format(_CDAC_ShieldingLayer))

		target_coordx = tmp1_1[0][0][0][-1][0][0][0]['_XY_right'][0]


		if (_CDAC_Folding == False):
			CapSize = 2 ** (_NumofCbit - 0 - 1)
			tmp1_2 = self.get_param_KJH4('SRF_CDAC_Pos', 'SRF_CDACWtDriver', 'SRF_DriverArray', 'BND_{}C_Driver_Input_Hrz_M3'.format(CapSize))
		else:
			CapSize = 2 ** (_NumofCbit - 1 - 1)
			tmp1_2 = self.get_param_KJH4('SRF_CDAC_Pos', 'SRF_CDAC_LowerHalf', 'SRF_DriverArray', 'BND_{}C_Driver_Input_Hrz_M3'.format(CapSize))

		target_coordy = tmp1_2[0][0][0][0][0]['_XY_up'][1]
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

		## ########## ########## ########## ########## ########## ########## ########## ########## ########## ########## ########## SRF_RDACandDecoder_Pos: Vref2CDAC routing
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

		## coord1
		## P1 calculation
		P1 = [0, 0]
		tmp = self.get_param_KJH4('SRF_RDACandDecoder_Pos','BND_XgateOut_Hrz_M5')
		P1 = tmp[0][0][0]['_XY_left']
		## P2 calculation
		P2 = [0, 0]
		if (_CDAC_Folding == False):
			tmp = self.get_param_KJH4('SRF_CDAC_Pos', 'SRF_CDACWtDriver', 'SRF_CapArray', 'BND_DummyUCAP_Bot_Hrz')
		else:
			tmp = self.get_param_KJH4('SRF_CDAC_Pos', 'SRF_CDAC_LowerHalf', 'SRF_CapArray', 'BND_DummyUCAP_Bot_Hrz')

		P2[0] = tmp[0][0][0][0][0]['_XY_up_right'][0]
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
		if (_CDAC_Folding == False):
			tmp = self.get_param_KJH4('SRF_CDAC_Pos', 'SRF_CDACWtDriver', 'SRF_CapArray', 'BND_DummyUCAP_Bot_Hrz')
		else:
			tmp = self.get_param_KJH4('SRF_CDAC_Pos', 'SRF_CDAC_LowerHalf', 'SRF_CapArray', 'BND_DummyUCAP_Bot_Hrz')

		P2[1] = tmp[0][0][0][0][0]['_XY_up_right'][1]
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

		tmpXY = self.get_PTH_KJH2(Path_name, Path_width, tmpXY, tmpMetal, tmpViaTF, tmpViaDir, tmpViaWid,_Name)

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
			Num_Invchain = len(_CDACPreDriver_NumberofGate)-1-i
			Num_InvinChain = len(_CDACPreDriver_NumberofGate[-1-i])-2

			tmp1 = self.get_param_KJH4('SRF_RDACandDecoder_Pos', 'BND_B_{}'.format(i))
			tmp2 = self.get_param_KJH4('SRF_SARLogicWtComparator','SRF_SARLogicWtBuffers','SRF_UpperCDACPreDriver','SRF_InvChain{}'.format(Num_Invchain),'SRF_IntConn_ViaM1M2','SRF_ViaM1M2','BND_Met2Layer') #SRF_Output_ViaM2Mx
			self._DesignParameter[Element_name]['_XWidth'] = abs(tmp2[0][0][0][0][-1][0][0][0]['_XY_right'][0] - tmp1[0][0][0]['_XY_right'][0])

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
			Num_Invchain = len(_CDACPreDriver_NumberofGate)-1-i
			Num_InvinChain = len(_CDACPreDriver_NumberofGate[-1-i])-2

			tmp1 = self.get_param_KJH4('SRF_RDACandDecoder_Pos', 'BND_Bb_{}'.format(i))
			tmp2 = self.get_param_KJH4('SRF_SARLogicWtComparator','SRF_SARLogicWtBuffers','SRF_UpperCDACPreDriver','SRF_InvChain{}'.format(Num_Invchain),'SRF_Output_ViaM2Mx','SRF_ViaM2M3','BND_Met2Layer') #SRF_Output_ViaM2Mx
			self._DesignParameter[Element_name]['_XWidth'] = abs(tmp2[0][0][0][0][0][0][0][0]['_XY_right'][0] - tmp1[0][0][0]['_XY_right'][0])

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
			Num_Invchain = len(_CDACPreDriver_NumberofGate)-1-i
			Num_InvinChain = len(_CDACPreDriver_NumberofGate[-1-i])-2

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
			Num_Invchain = len(_CDACPreDriver_NumberofGate)-1-i
			Num_InvinChain = len(_CDACPreDriver_NumberofGate[-1-i])-2

			tmp1 =self.get_param_KJH4('SRF_Bb_{}_Exten_ViaM3M4'.format(i),'SRF_ViaM3M4','BND_Met4Layer')
			tmp2 = self.get_param_KJH4('SRF_SARLogicWtComparator','SRF_SARLogicWtBuffers','SRF_UpperCDACPreDriver','SRF_InvChain{}'.format(Num_Invchain),'SRF_Output_ViaM2Mx','SRF_ViaM2M3','BND_Met2Layer') #SRF_Output_ViaM2Mx
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
			tmp1 = self.get_param_KJH4('SRF_Bb_{}_Exten_ViaM3M4'.format(i),'SRF_ViaM3M4','BND_Met4Layer')
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
			Num_Invchain = len(_CDACPreDriver_NumberofGate)-1-i
			Num_InvinChain = len(_CDACPreDriver_NumberofGate[-1-i])-2
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








		## ########## ########## ########## ########## ########## ########## ########## ########## ########## ########## ########## ########## SRF_RDACandDecoder_Neg
		## ########## ########## ########## ########## ########## ########## ########## ########## ########## ########## ########## SRF_RDACandDecoder_Pos: Gen and placement

		# 시간줄이기...
		# ## Copy Calculation_Parameters from low-level-block ex)copy.deepcopy(B16_nmos_power_v2._NMOS_POWER._ParametersForDesignCalculation)
		# _Caculation_Parameters = copy.deepcopy(R00_00_Combine_KJH4._Combine._ParametersForDesignCalculation)
		# ## Define Calculation_Parameters ex) _Caculation_Parameters['_NMOSPOWER_PbodyContact_1_Length']  = _NMOSPOWER_PbodyContact_1_Length
		# _Caculation_Parameters['_RDAC_Pside'] = False
		#
		# _Caculation_Parameters['_RDAC_displacement'] = _RDAC_displacement
		#
		# _Caculation_Parameters['_RDAC_Size'] = _RDAC_Size
		#
		# _Caculation_Parameters['RDAC_Guard_NumCont'] = RDAC_Guard_NumCont
		# _Caculation_Parameters['RDAC_ResWidth'] = RDAC_ResWidth
		# _Caculation_Parameters['RDAC_ResLength'] = RDAC_ResLength
		#
		# _Caculation_Parameters['RDAC_CONUMX'] = RDAC_CONUMX
		# _Caculation_Parameters['RDAC_CONUMY'] = RDAC_CONUMY
		#
		# _Caculation_Parameters['_Decoder_Unit2UnitDist'] = _Decoder_Unit2UnitDist
		#
		# _Caculation_Parameters['_Decoder_RBit'] = _NumofRbit
		#
		# _Caculation_Parameters['_Unit_Routing_Dist'] = _Unit_Routing_Dist
		# _Caculation_Parameters['_Unit_Xvt'] = _Unit_Xvt
		# _Caculation_Parameters['_Unit_GatetoGateDist'] = _Unit_GatetoGateDist
		# _Caculation_Parameters['_Unit_Num_EachStag_input'] = _Unit_Num_EachStag_input
		#
		# _Caculation_Parameters['_Unit_Pbody_NumCont'] = _Unit_Pbody_NumCont
		# _Caculation_Parameters['_Unit_Pbody_XvtTop2Pbody'] = _Unit_Pbody_XvtTop2Pbody
		# _Caculation_Parameters['_Unit_Nbody_NumCont'] = _Unit_Nbody_NumCont
		# _Caculation_Parameters['_Unit_Nbody_Xvtdown2Nbody'] = _Unit_Nbody_Xvtdown2Nbody
		# _Caculation_Parameters['_Unit_PMOSXvt2NMOSXvt'] = _Unit_PMOSXvt2NMOSXvt
		# _Caculation_Parameters['_Unit_POGate_Comb_length'] = _Unit_POGate_Comb_length
		#
		# _Caculation_Parameters['_Nand_NumberofGate'] = _Nand_NumberofGate
		# _Caculation_Parameters['_Nand_ChannelLength'] = _Nand_ChannelLength
		# _Caculation_Parameters['_Nand_POGate_ViaMxMx'] = _Nand_POGate_ViaMxMx
		#
		# _Caculation_Parameters['_Nand_NMOS_ChannelWidth'] = _Nand_NMOS_ChannelWidth
		# _Caculation_Parameters['_Nand_NMOS_Source_Via_Close2POpin_TF'] = _Nand_NMOS_Source_Via_Close2POpin_TF
		# _Caculation_Parameters['_Nand_PMOS_ChannelWidth'] = _Nand_PMOS_ChannelWidth
		#
		# _Caculation_Parameters['_Nor_ChannelLength'] = _Nor_ChannelLength
		# _Caculation_Parameters['_Nor_POGate_ViaMxMx'] = _Nor_POGate_ViaMxMx
		#
		# _Caculation_Parameters['_Nor_NMOS_ChannelWidth'] = _Nor_NMOS_ChannelWidth
		# _Caculation_Parameters['_Nor_NMOS_NumberofGate'] = _Nor_NMOS_NumberofGate
		#
		# _Caculation_Parameters['_Nor_PMOS_ChannelWidth'] = _Nor_PMOS_ChannelWidth
		# _Caculation_Parameters['_Nor_PMOS_NumberofGate'] = _Nor_PMOS_NumberofGate
		# _Caculation_Parameters['_Nor_PMOS_Source_Via_Close2POpin_TF'] = _Nor_PMOS_Source_Via_Close2POpin_TF
		#
		# _Caculation_Parameters['_Inv_NumberofGate'] = _Inv_NumberofGate
		# _Caculation_Parameters['_Inv_ChannelLength'] = _Inv_ChannelLength
		#
		# _Caculation_Parameters['_Inv_NMOS_ChannelWidth'] = _Inv_NMOS_ChannelWidth
		# _Caculation_Parameters['_Inv_NMOS_POGate_ViaMxMx'] = _Inv_NMOS_POGate_ViaMxMx
		#
		# _Caculation_Parameters['_Inv_PMOS_ChannelWidth'] = _Inv_PMOS_ChannelWidth
		# _Caculation_Parameters['_Inv_PMOS_POGate_ViaMxMx'] = _Inv_PMOS_POGate_ViaMxMx
		#
		# _Caculation_Parameters['_Xgate_NumberofGate'] = _Xgate_NumberofGate
		# _Caculation_Parameters['_Xgate_ChannelLength'] = _Xgate_ChannelLength
		#
		# _Caculation_Parameters['_Xgate_NMOS_ChannelWidth'] = _Xgate_NMOS_ChannelWidth
		# _Caculation_Parameters['_Xgate_NMOS_POGate_ViaMxMx'] = _Xgate_NMOS_POGate_ViaMxMx
		#
		# _Caculation_Parameters['_Xgate_PMOS_ChannelWidth'] = _Xgate_PMOS_ChannelWidth
		# _Caculation_Parameters['_Xgate_PMOS_POGate_ViaMxMx'] = _Xgate_PMOS_POGate_ViaMxMx


		## Generate Sref: ex)self._DesignParameter['_NMOS_POWER'] = self._SrefElementDeclaration(_DesignObj=B16_nmos_power_v2._NMOS_POWER( _DesignParameter=None, _Name='{}:NMOS_POWER'.format(_Name)))[0]
		self._DesignParameter['SRF_RDACandDecoder_Neg'] = self._SrefElementDeclaration(_DesignObj=R00_00_Combine_KJH4._Combine(_DesignParameter=None, _Name='{}:SRF_RDACandDecoder_Neg'.format(_Name)))[0]

		## Calculate Sref Layer by using Calculation_Parameter: ex)'_NMOS_POWER'
		# self._DesignParameter['SRF_RDACandDecoder_Neg']['_DesignObj']._CalculateDesignParameter(**_Caculation_Parameters) # 시간줄이기
		self._DesignParameter['SRF_RDACandDecoder_Neg'] = copy.deepcopy(self._DesignParameter['SRF_RDACandDecoder_Pos'])
		self.rename_srf_prefix(self._DesignParameter['SRF_RDACandDecoder_Neg'], 'SRF_RDACandDecoder_Pos', 'SRF_RDACandDecoder_Neg')


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
		if (_CDAC_Folding == False):
			tmp1_1 = self.get_param_KJH4('SRF_CDAC_Neg', 'SRF_CDACWtDriver', 'SRF_CapArray', 'SRF_DummyCaps', 'SRF_CapWtShield4DCAP', 'BND_Shield_Extend_VTC_M{}'.format(_CDAC_ShieldingLayer))
		else:
			tmp1_1 = self.get_param_KJH4('SRF_CDAC_Neg', 'SRF_CDAC_LowerHalf', 'SRF_CapArray', 'SRF_DummyCaps', 'SRF_CapWtShield4DCAP', 'BND_Shield_Extend_VTC_M{}'.format(_CDAC_ShieldingLayer))

		target_coordx = tmp1_1[0][0][0][-1][0][0][0]['_XY_right'][0]

		if (_CDAC_Folding == False):
			CapSize = 2 ** (_NumofCbit - 0 - 1)
			tmp1_2 = self.get_param_KJH4('SRF_CDAC_Neg', 'SRF_CDACWtDriver', 'SRF_DriverArray', 'BND_{}C_Driver_Input_Hrz_M3'.format(CapSize))
		else:
			CapSize = 2 ** (_NumofCbit - 1 - 1)
			tmp1_2 = self.get_param_KJH4('SRF_CDAC_Neg', 'SRF_CDAC_LowerHalf', 'SRF_DriverArray', 'BND_{}C_Driver_Input_Hrz_M3'.format(CapSize))

		target_coordy = tmp1_2[0][0][0][0][0]['_XY_up'][1]
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

		## coord1
		## P1 calculation
		P1 = [0, 0]
		tmp = self.get_param_KJH4('SRF_RDACandDecoder_Neg','BND_XgateOut_Hrz_M5')
		P1 = tmp[0][0][0]['_XY_left']
		## P2 calculation
		P2 = [0, 0]
		if (_CDAC_Folding == False):
			tmp = self.get_param_KJH4('SRF_CDAC_Neg', 'SRF_CDACWtDriver', 'SRF_CapArray', 'BND_DummyUCAP_Bot_Hrz')
		else:
			tmp = self.get_param_KJH4('SRF_CDAC_Neg', 'SRF_CDAC_LowerHalf', 'SRF_CapArray', 'BND_DummyUCAP_Bot_Hrz')

		P2[0] = tmp[0][0][0][0][0]['_XY_up_right'][0]
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
		if (_CDAC_Folding == False):
			tmp = self.get_param_KJH4('SRF_CDAC_Neg', 'SRF_CDACWtDriver', 'SRF_CapArray', 'BND_DummyUCAP_Bot_Hrz')
		else:
			tmp = self.get_param_KJH4('SRF_CDAC_Neg', 'SRF_CDAC_LowerHalf', 'SRF_CapArray', 'BND_DummyUCAP_Bot_Hrz')

		P2[1] = tmp[0][0][0][0][0]['_XY_up_right'][1]
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

		tmpXY = self.get_PTH_KJH2(Path_name, Path_width, tmpXY, tmpMetal, tmpViaTF, tmpViaDir, tmpViaWid,_Name)


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
			Num_Invchain = len(_CDACPreDriver_NumberofGate)-1-i
			Num_InvinChain = len(_CDACPreDriver_NumberofGate[-1-i])-2

			tmp1 = self.get_param_KJH4('SRF_RDACandDecoder_Neg', 'BND_B_{}'.format(i))
			tmp2 = self.get_param_KJH4('SRF_SARLogicWtComparator','SRF_SARLogicWtBuffers','SRF_LowerCDACPreDriver','SRF_InvChain{}'.format(Num_Invchain),'SRF_IntConn_ViaM1M2','SRF_ViaM1M2','BND_Met2Layer') #SRF_Output_ViaM2Mx
			self._DesignParameter[Element_name]['_XWidth'] = abs(tmp2[0][0][0][0][-1][0][0][0]['_XY_right'][0] - tmp1[0][0][0]['_XY_right'][0])

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
			Num_Invchain = len(_CDACPreDriver_NumberofGate)-1-i
			Num_InvinChain = len(_CDACPreDriver_NumberofGate[-1-i])-2

			tmp1 = self.get_param_KJH4('SRF_RDACandDecoder_Neg', 'BND_Bb_{}'.format(i))
			tmp2 = self.get_param_KJH4('SRF_SARLogicWtComparator','SRF_SARLogicWtBuffers','SRF_LowerCDACPreDriver','SRF_InvChain{}'.format(Num_Invchain),'SRF_Output_ViaM2Mx','SRF_ViaM2M3','BND_Met2Layer') #SRF_Output_ViaM2Mx
			self._DesignParameter[Element_name]['_XWidth'] = abs(tmp2[0][0][0][0][0][0][0][0]['_XY_right'][0] - tmp1[0][0][0]['_XY_right'][0])

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
			Num_Invchain = len(_CDACPreDriver_NumberofGate)-1-i
			Num_InvinChain = len(_CDACPreDriver_NumberofGate[-1-i])-2

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
			Num_Invchain = len(_CDACPreDriver_NumberofGate)-1-i
			Num_InvinChain = len(_CDACPreDriver_NumberofGate[-1-i])-2

			tmp1 =self.get_param_KJH4('SRF_Bb_{}_Exten_Neg_ViaM3M4'.format(i),'SRF_ViaM3M4','BND_Met4Layer')
			tmp2 = self.get_param_KJH4('SRF_SARLogicWtComparator','SRF_SARLogicWtBuffers','SRF_LowerCDACPreDriver','SRF_InvChain{}'.format(Num_Invchain),'SRF_Output_ViaM2Mx','SRF_ViaM2M3','BND_Met2Layer') #SRF_Output_ViaM2Mx
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
			tmp1 = self.get_param_KJH4('SRF_Bb_{}_Exten_Neg_ViaM3M4'.format(i),'SRF_ViaM3M4','BND_Met4Layer')
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
			Num_Invchain = len(_CDACPreDriver_NumberofGate)-1-i
			Num_InvinChain = len(_CDACPreDriver_NumberofGate[-1-i])-2
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


		print('##############################')
		print('##     Calculation_End      ##')
		print('##############################')


############################################################################################################################################################ START MAIN
if __name__ == '__main__':

	''' Check Time'''
	start_time = time.time()

	from KJH91_Projects.Project_ADC.Library_and_Engine.Private import MyInfo
	from KJH91_Projects.Project_ADC.Library_and_Engine import DRCchecker_KJH0

	'''주의 사항 및 업데이트 내용, Fold 일때 C(Switching) C(not swithcing)가 지금 꼬여있음. 수정해줄 필요가 있다.'''
	## LibraryName: ex)Proj_ADC_A_my_building_block
	libname = 'Proj_ZZ00_RcdacSar_S00_00_R00C13H02L00_KJH3_FixedVersion'
	## CellName: ex)C01_cap_array_v2_84
	cellname = 'S00_00_R00C13H02L00_97'
	_fileName = cellname + '.gds'

	''' Input Parameters for Layout Object '''
	InputParams = dict(
		############################################################################################################################################ SAR ADC Top
		_NumofRbit=4,
		_NumofCbit=6,

		_CDAC_Folding=False,  # None/True/False
		_Driver_CommonCentroidPlacementIfCDACFolded=True,  # 말 그대로 True이면 CommmonCentroid 배치가 됨.
		_Driver_DecimationIfDriverPlacedInCommonCentroid=True,
		_Driver_DecimationFactor=[0, 0, 0],
		# [MSB, MSB-1 ... MSB-x]: 단 X<MSB  # 위 옵션 True시 작동; MSB부터 벡터로 작성; [3,2,2] 시 MSB0 -> 3:1, MSB1 -> 2:1, MSB2 -> 2:1, ... 1은 불가
		_SpaceBtwBootSWPosNeg=200,  # Fixed

		############################################################################################################################################ SAR Logic
		## SAR Logic sizing
		_Test_distance=330,  # Fixed
		_Routing_width=50,  # Fixed
		_Routing_distance=80,  # Fixed

		_SARLogic_YWidthOfCLKSrc=100,  # Fixed (CLK spine)
		_SARLogic_SpaceBtwCLKSrcAndCLKSamp=100,  # Fixed (Dist. CLK spine and CLK_Samp)
		_SARLogic_YWidthOfCLKSamp=100,  # Fixed (CLK spine)

		_SARLogic_YWidthOfCompOut=100,  # Fixed
		_SARLogic_SpaceBtwCompOutAndCLKDout=100,  # Fixed
		_SARLogic_YWidthOfCLKDout=100,  # Fixed

		################################################################################################################################## SAR Logic: DFF
		## DFF Common
		_SARLogic_DFF_Pbody_NumCont=2,  # number (Fixed)
		_SARLogic_DFF_Nbody_NumCont=2,  # number (Fixed)
		_SARLogic_DFF_PMOSXvt2NMOSXvt=1150,  # number (Fixed)
		_SARLogic_DFF_XvtTop2Pbody=None,  # number/None(Minimum) (Fixed)
		_SARLogic_DFF_Xvtdown2Nbody=None,  # number/None(Minimum) (Fixed)

		## Master Xgate1
			## Xgate NMOS
			_SARLogic_Mst_Xgate1_NMOS_NumberofGate=1,  # 1
			_SARLogic_Mst_Xgate1_NMOS_ChannelWidth=400,  # 400
			_SARLogic_Mst_Xgate1_NMOS_ChannelLength=30,  # 30
			_SARLogic_Mst_Xgate1_NMOS_XVT='SLVT',
			_SARLogic_Mst_Xgate1_NMOS_POGate_Comb_length=100,  # (Fixed)
			## Xgate PMOS
			_SARLogic_Mst_Xgate1_PMOS_NumberofGate=1,  # 1
			_SARLogic_Mst_Xgate1_PMOS_ChannelWidth=800,  # 200
			_SARLogic_Mst_Xgate1_PMOS_ChannelLength=30,
			_SARLogic_Mst_Xgate1_PMOS_XVT='SLVT',
			_SARLogic_Mst_Xgate1_PMOS_POGate_Comb_length=100,  # (Fixed)

		## Master Xgate2
			## Xgate NMOS
			_SARLogic_Mst_Xgate2_NMOS_NumberofGate=1,
			_SARLogic_Mst_Xgate2_NMOS_ChannelWidth=400,
			_SARLogic_Mst_Xgate2_NMOS_ChannelLength=30,
			_SARLogic_Mst_Xgate2_NMOS_XVT='SLVT',
			_SARLogic_Mst_Xgate2_NMOS_POGate_Comb_length=100,  # (Fixed)
			## Xgate PMOS
			_SARLogic_Mst_Xgate2_PMOS_NumberofGate=1,
			_SARLogic_Mst_Xgate2_PMOS_ChannelWidth=800,
			_SARLogic_Mst_Xgate2_PMOS_ChannelLength=30,
			_SARLogic_Mst_Xgate2_PMOS_XVT='SLVT',
			_SARLogic_Mst_Xgate2_PMOS_POGate_Comb_length=100,  # (Fixed)

		## Master Nor1
			## NMOS
				## NMOS common
				_SARLogic_Mst_Nor1_NMOS_XVT='SLVT',
				## NMOSA
				_SARLogic_Mst_Nor1_NMOSA_NumberofGate=4,
				_SARLogic_Mst_Nor1_NMOSA_ChannelWidth=400,
				_SARLogic_Mst_Nor1_NMOSA_ChannelLength=30,
				_SARLogic_Mst_Nor1_NMOSA_POGate_Comb_length=100,  # (Fixed)
				## NMOSB
				_SARLogic_Mst_Nor1_NMOSB_NumberofGate=4,
				_SARLogic_Mst_Nor1_NMOSB_ChannelWidth=400,
				_SARLogic_Mst_Nor1_NMOSB_ChannelLength=30,
				_SARLogic_Mst_Nor1_NMOSB_POGate_Comb_length=100,  # (Fixed)

			## PMOS
				## PMOS common
				_SARLogic_Mst_Nor1_PMOS_XVT='SLVT',
				## PMOSA
				_SARLogic_Mst_Nor1_PMOSA_NumberofGate=8,
				_SARLogic_Mst_Nor1_PMOSA_ChannelWidth=800,
				_SARLogic_Mst_Nor1_PMOSA_ChannelLength=30,
				_SARLogic_Mst_Nor1_PMOSA_POGate_Comb_length=100,  # (Fixed)
				## PMOSB
				_SARLogic_Mst_Nor1_PMOSB_NumberofGate=8,
				_SARLogic_Mst_Nor1_PMOSB_ChannelWidth=800,
				_SARLogic_Mst_Nor1_PMOSB_ChannelLength=30,
				_SARLogic_Mst_Nor1_PMOSB_POGate_Comb_length=100,  # (Fixed)

		## Master Nor2
			## NMOS
				## NMOS common
				_SARLogic_Mst_Nor2_NMOS_XVT='SLVT',
				## NMOSA
				_SARLogic_Mst_Nor2_NMOSA_NumberofGate=1,
				_SARLogic_Mst_Nor2_NMOSA_ChannelWidth=400,
				_SARLogic_Mst_Nor2_NMOSA_ChannelLength=30,
				_SARLogic_Mst_Nor2_NMOSA_POGate_Comb_length=100,  # (Fixed)
				## NMOSB
				_SARLogic_Mst_Nor2_NMOSB_NumberofGate=1,
				_SARLogic_Mst_Nor2_NMOSB_ChannelWidth=400,
				_SARLogic_Mst_Nor2_NMOSB_ChannelLength=30,
				_SARLogic_Mst_Nor2_NMOSB_POGate_Comb_length=100,  # (Fixed)

			## PMOS
				## PMOS common
				_SARLogic_Mst_Nor2_PMOS_XVT='SLVT',
				## PMOSA
				_SARLogic_Mst_Nor2_PMOSA_NumberofGate=2,
				_SARLogic_Mst_Nor2_PMOSA_ChannelWidth=800,
				_SARLogic_Mst_Nor2_PMOSA_ChannelLength=30,
				_SARLogic_Mst_Nor2_PMOSA_POGate_Comb_length=100,  # (Fixed)
				## PMOSB
				_SARLogic_Mst_Nor2_PMOSB_NumberofGate=2,
				_SARLogic_Mst_Nor2_PMOSB_ChannelWidth=800,
				_SARLogic_Mst_Nor2_PMOSB_ChannelLength=30,
				_SARLogic_Mst_Nor2_PMOSB_POGate_Comb_length=100,  # (Fixed)

		## Master Inv1 : Set pre-driver
			## Inv1 NMOS
			_SARLogic_Mst_Inv1_NMOS_NumberofGate=1,
			_SARLogic_Mst_Inv1_NMOS_ChannelWidth=400,
			_SARLogic_Mst_Inv1_NMOS_ChannelLength=30,
			_SARLogic_Mst_Inv1_NMOS_XVT='SLVT',
			_SARLogic_Mst_Inv1_NMOS_POGate_Comb_length=100,  # (Fixed)

			## Inv1 PMOS
			_SARLogic_Mst_Inv1_PMOS_NumberofGate=1,
			_SARLogic_Mst_Inv1_PMOS_ChannelWidth=800,
			_SARLogic_Mst_Inv1_PMOS_ChannelLength=30,
			_SARLogic_Mst_Inv1_PMOS_XVT='SLVT',
			_SARLogic_Mst_Inv1_PMOS_POGate_Comb_length=100,  # (Fixed)

		## Master Inv2 : Set driver
			## Inv2 NMOS
			_SARLogic_Mst_Inv2_NMOS_NumberofGate=3,
			_SARLogic_Mst_Inv2_NMOS_ChannelWidth=400,
			_SARLogic_Mst_Inv2_NMOS_ChannelLength=30,
			_SARLogic_Mst_Inv2_NMOS_XVT='SLVT',
			_SARLogic_Mst_Inv2_NMOS_POGate_Comb_length=100,  # (Fixed)

			## Inv2 PMOS
			_SARLogic_Mst_Inv2_PMOS_NumberofGate=3,
			_SARLogic_Mst_Inv2_PMOS_ChannelWidth=800,
			_SARLogic_Mst_Inv2_PMOS_ChannelLength=30,
			_SARLogic_Mst_Inv2_PMOS_XVT='SLVT',
			_SARLogic_Mst_Inv2_PMOS_POGate_Comb_length=100,  # (Fixed)

		## Master Inv3 : Clock driver
			## Inv3 NMOS
			_SARLogic_Mst_Inv3_NMOS_NumberofGate=2,
			_SARLogic_Mst_Inv3_NMOS_ChannelWidth=400,
			_SARLogic_Mst_Inv3_NMOS_ChannelLength=30,
			_SARLogic_Mst_Inv3_NMOS_XVT='SLVT',
			_SARLogic_Mst_Inv3_NMOS_POGate_Comb_length=100,  # (Fixed)
			## Inv3 PMOS
			_SARLogic_Mst_Inv3_PMOS_NumberofGate=2,
			_SARLogic_Mst_Inv3_PMOS_ChannelWidth=800,
			_SARLogic_Mst_Inv3_PMOS_ChannelLength=30,
			_SARLogic_Mst_Inv3_PMOS_XVT='SLVT',
			_SARLogic_Mst_Inv3_PMOS_POGate_Comb_length=100,  # (Fixed)

		## Slave Xgate1
			## Xgate NMOS
			_SARLogic_Slv_Xgate1_NMOS_NumberofGate=4,
			_SARLogic_Slv_Xgate1_NMOS_ChannelWidth=400,
			_SARLogic_Slv_Xgate1_NMOS_ChannelLength=30,
			_SARLogic_Slv_Xgate1_NMOS_XVT='SLVT',
			_SARLogic_Slv_Xgate1_NMOS_POGate_Comb_length=100,  # (Fixed)
			## Xgate PMOS
			_SARLogic_Slv_Xgate1_PMOS_NumberofGate=4,
			_SARLogic_Slv_Xgate1_PMOS_ChannelWidth=800,
			_SARLogic_Slv_Xgate1_PMOS_ChannelLength=30,
			_SARLogic_Slv_Xgate1_PMOS_XVT='SLVT',
			_SARLogic_Slv_Xgate1_PMOS_POGate_Comb_length=100,  # (Fixed)

		## Slave Xgate2
			## Xgate NMOS
			_SARLogic_Slv_Xgate2_NMOS_NumberofGate=4,
			_SARLogic_Slv_Xgate2_NMOS_ChannelWidth=400,
			_SARLogic_Slv_Xgate2_NMOS_ChannelLength=30,
			_SARLogic_Slv_Xgate2_NMOS_XVT='SLVT',
			_SARLogic_Slv_Xgate2_NMOS_POGate_Comb_length=100,  # (Fixed)
			## Xgate PMOS
			_SARLogic_Slv_Xgate2_PMOS_NumberofGate=4,
			_SARLogic_Slv_Xgate2_PMOS_ChannelWidth=800,
			_SARLogic_Slv_Xgate2_PMOS_ChannelLength=30,
			_SARLogic_Slv_Xgate2_PMOS_XVT='SLVT',
			_SARLogic_Slv_Xgate2_PMOS_POGate_Comb_length=100,  # (Fixed)

		## Slave Nor1
			## NMOS
				## NMOS common
				_SARLogic_Slv_Nor1_NMOS_XVT='SLVT',
				## NMOSA
				_SARLogic_Slv_Nor1_NMOSA_NumberofGate=4,
				_SARLogic_Slv_Nor1_NMOSA_ChannelWidth=400,
				_SARLogic_Slv_Nor1_NMOSA_ChannelLength=30,
				_SARLogic_Slv_Nor1_NMOSA_POGate_Comb_length=100,  # (Fixed)
				## NMOSB
				_SARLogic_Slv_Nor1_NMOSB_NumberofGate=4,
				_SARLogic_Slv_Nor1_NMOSB_ChannelWidth=400,
				_SARLogic_Slv_Nor1_NMOSB_ChannelLength=30,
				_SARLogic_Slv_Nor1_NMOSB_POGate_Comb_length=100,  # (Fixed)
			## PMOS
				## PMOS common
				_SARLogic_Slv_Nor1_PMOS_XVT='SLVT',
				## PMOSA
				_SARLogic_Slv_Nor1_PMOSA_NumberofGate=8,
				_SARLogic_Slv_Nor1_PMOSA_ChannelWidth=800,
				_SARLogic_Slv_Nor1_PMOSA_ChannelLength=30,
				_SARLogic_Slv_Nor1_PMOSA_POGate_Comb_length=100,  # (Fixed)
				## PMOSB
				_SARLogic_Slv_Nor1_PMOSB_NumberofGate=8,
				_SARLogic_Slv_Nor1_PMOSB_ChannelWidth=800,
				_SARLogic_Slv_Nor1_PMOSB_ChannelLength=30,
				_SARLogic_Slv_Nor1_PMOSB_POGate_Comb_length=100,  # (Fixed)

		## Slave Nor2
			## NMOS
				## NMOS common
				_SARLogic_Slv_Nor2_NMOS_XVT='SLVT',
				## NMOSA
				_SARLogic_Slv_Nor2_NMOSA_NumberofGate=2,
				_SARLogic_Slv_Nor2_NMOSA_ChannelWidth=400,
				_SARLogic_Slv_Nor2_NMOSA_ChannelLength=30,
				_SARLogic_Slv_Nor2_NMOSA_POGate_Comb_length=100,  # (Fixed)
				## NMOSB
				_SARLogic_Slv_Nor2_NMOSB_NumberofGate=2,
				_SARLogic_Slv_Nor2_NMOSB_ChannelWidth=400,
				_SARLogic_Slv_Nor2_NMOSB_ChannelLength=30,
				_SARLogic_Slv_Nor2_NMOSB_POGate_Comb_length=100,  # (Fixed)
			## PMOS
				## PMOS common
				_SARLogic_Slv_Nor2_PMOS_XVT='SLVT',
				## PMOSA
				_SARLogic_Slv_Nor2_PMOSA_NumberofGate=4,
				_SARLogic_Slv_Nor2_PMOSA_ChannelWidth=800,
				_SARLogic_Slv_Nor2_PMOSA_ChannelLength=30,
				_SARLogic_Slv_Nor2_PMOSA_POGate_Comb_length=100,  # (Fixed)
				## PMOSB
				_SARLogic_Slv_Nor2_PMOSB_NumberofGate=4,
				_SARLogic_Slv_Nor2_PMOSB_ChannelWidth=800,
				_SARLogic_Slv_Nor2_PMOSB_ChannelLength=30,
				_SARLogic_Slv_Nor2_PMOSB_POGate_Comb_length=100,  # (Fixed)

		## Slave Inv1 : ReSet pre-driver
			## Inv1 NMOS
			_SARLogic_Slv_Inv1_NMOS_NumberofGate=1,
			_SARLogic_Slv_Inv1_NMOS_ChannelWidth=400,
			_SARLogic_Slv_Inv1_NMOS_ChannelLength=30,
			_SARLogic_Slv_Inv1_NMOS_XVT='SLVT',
			_SARLogic_Slv_Inv1_NMOS_POGate_Comb_length=100,  # (Fixed)
			## Inv1 PMOS
			_SARLogic_Slv_Inv1_PMOS_NumberofGate=1,
			_SARLogic_Slv_Inv1_PMOS_ChannelWidth=800,
			_SARLogic_Slv_Inv1_PMOS_ChannelLength=30,
			_SARLogic_Slv_Inv1_PMOS_XVT='SLVT',
			_SARLogic_Slv_Inv1_PMOS_POGate_Comb_length=100,  # (Fixed)

		## Slave Inv2 : ReSet driver
			## Inv2 NMOS
			_SARLogic_Slv_Inv2_NMOS_NumberofGate=2,
			_SARLogic_Slv_Inv2_NMOS_ChannelWidth=400,
			_SARLogic_Slv_Inv2_NMOS_ChannelLength=30,
			_SARLogic_Slv_Inv2_NMOS_XVT='SLVT',
			_SARLogic_Slv_Inv2_NMOS_POGate_Comb_length=100,  # (Fixed)
			## Inv2 PMOS
			_SARLogic_Slv_Inv2_PMOS_NumberofGate=2,
			_SARLogic_Slv_Inv2_PMOS_ChannelWidth=800,
			_SARLogic_Slv_Inv2_PMOS_ChannelLength=30,
			_SARLogic_Slv_Inv2_PMOS_XVT='SLVT',
			_SARLogic_Slv_Inv2_PMOS_POGate_Comb_length=100,  # (Fixed)

		## Slave Inv3 : Qb driver
			## Inv3 NMOS
			_SARLogic_Slv_Inv3_NMOS_NumberofGate=4,
			_SARLogic_Slv_Inv3_NMOS_ChannelWidth=400,
			_SARLogic_Slv_Inv3_NMOS_ChannelLength=30,
			_SARLogic_Slv_Inv3_NMOS_XVT='SLVT',
			_SARLogic_Slv_Inv3_NMOS_POGate_Comb_length=100,  # (Fixed)
			## Inv3 PMOS
			_SARLogic_Slv_Inv3_PMOS_NumberofGate=4,
			_SARLogic_Slv_Inv3_PMOS_ChannelWidth=800,
			_SARLogic_Slv_Inv3_PMOS_ChannelLength=30,
			_SARLogic_Slv_Inv3_PMOS_XVT='SLVT',
			_SARLogic_Slv_Inv3_PMOS_POGate_Comb_length=100,  # (Fixed)

		############################################################################################################################################ SAR Logic: Clock Tree
		################################################################################################################################## SAR Logic: Clock Tree: Top (CLK and CLKSamp)
		# Top Clock  Tree Size
		_SARLogic_CLKBufTreeTop_NumOfStage=4,
		_SARLogic_CLKBufTreeTop_CLKSampBuf_SizeByStage=[1, 2, 4, 8],
		_SARLogic_CLKBufTreeTop_CLKSrcBuf_SizeByStage=[1, 2, 4, 8],  # 스테이지에 따른 버퍼 사이즈(UnitBuffer의 배수로 각 스테이지의 크기가 결정 됨.)
		_SARLogic_CLKBufTreeTop_XOffSet=+45,  # (10Bit DRC check:+45)

		## Top CLK Buffer Tree Size
		_SARLogic_CLKBufTreeTop_Inv_NMOS_ChannelWidth=400,  # Number
		_SARLogic_CLKBufTreeTop_Inv_NMOS_ChannelLength=30,  # Number
		_SARLogic_CLKBufTreeTop_Inv_NMOS_NumberofGate=2,  # Number
		_SARLogic_CLKBufTreeTop_Inv_NMOS_XVT='SLVT',  # 'XVT' ex)SLVT/LVT/RVT/HVT
		_SARLogic_CLKBufTreeTop_Inv_NMOS_POGate_Comb_length=100,  # None/Number #(Fixed)

		_SARLogic_CLKBufTreeTop_Inv_PMOS_ChannelWidth=800,  # Number
		_SARLogic_CLKBufTreeTop_Inv_PMOS_ChannelLength=30,  # Number
		_SARLogic_CLKBufTreeTop_Inv_PMOS_NumberofGate=2,  # Number
		_SARLogic_CLKBufTreeTop_Inv_PMOS_XVT='SLVT',  # 'XVT' ex)SLVT/LVT/RVT/HVT
		_SARLogic_CLKBufTreeTop_Inv_PMOS_POGate_Comb_length=100,  # None/Number #(Fixed)

		# Top CLK BufferPowerRail Size
		_SARLogic_CLKBufTreeTop_NMOS_Pbody_NumCont=2,  # (Fixed)
		_SARLogic_CLKBufTreeTop_NMOS_Pbody_XvtTop2Pbody=None,  # (Fixed)
		_SARLogic_CLKBufTreeTop_PMOS_Nbody_NumCont=2,  # (Fixed)
		_SARLogic_CLKBufTreeTop_PMOS_Nbody_Xvtdown2Nbody=None,  # (Fixed)
		_SARLogic_CLKBufTreeTop_PMOSXvt2NMOSXvt=446,  # (Fixed)

		################################################################################################################################## SAR Logic: Clock Tree: Bot (Compout and CLKDout)
		# Bottom Clock  Tree Size
		_SARLogic_CLKBufTreeBot_NumOfStage=4,
		_SARLogic_CLKBufTreeBot_CompOutBuf_SizeByStage=[1, 2, 4, 8],
		_SARLogic_CLKBufTreeBot_CLKDoutBuf_SizeByStage=[1, 2, 4, 8],
		# 스테이지에 따른 버퍼 사이즈(UnitBuffer의 배수로 각 스테이지의 크기가 결정 됨.)
		_SARLogic_CLKBufTreeBot_XOffSet=0,  # (DRC check)

		## Bottom CLK Buffer Tree Size
		_SARLogic_CLKBufTreeBot_Inv_NMOS_ChannelWidth=400,  # Number
		_SARLogic_CLKBufTreeBot_Inv_NMOS_ChannelLength=30,  # Number
		_SARLogic_CLKBufTreeBot_Inv_NMOS_NumberofGate=2,  # Number
		_SARLogic_CLKBufTreeBot_Inv_NMOS_XVT='SLVT',  # 'XVT' ex)SLVT/LVT/RVT/HVT
		_SARLogic_CLKBufTreeBot_Inv_NMOS_POGate_Comb_length=100,  # None/Number #(Fixed)

		_SARLogic_CLKBufTreeBot_Inv_PMOS_ChannelWidth=800,  # Number
		_SARLogic_CLKBufTreeBot_Inv_PMOS_ChannelLength=30,  # Number
		_SARLogic_CLKBufTreeBot_Inv_PMOS_NumberofGate=2,  # Number
		_SARLogic_CLKBufTreeBot_Inv_PMOS_XVT='SLVT',  # 'XVT' ex)SLVT/LVT/RVT/HVT
		_SARLogic_CLKBufTreeBot_Inv_PMOS_POGate_Comb_length=100,  # None/Number #(Fixed)

		# Bottom CLK Buffer PowerRail Size
		_SARLogic_CLKBufTreeBot_NMOS_Pbody_NumCont=2,  # (Fixed)
		_SARLogic_CLKBufTreeBot_NMOS_Pbody_XvtTop2Pbody=None,  # (Fixed)
		_SARLogic_CLKBufTreeBot_PMOS_Nbody_NumCont=2,  # (Fixed)
		_SARLogic_CLKBufTreeBot_PMOS_Nbody_Xvtdown2Nbody=None,  # (Fixed)
		_SARLogic_CLKBufTreeBot_PMOSXvt2NMOSXvt=446,  # (Fixed)

		################################################################################################################################## SAR Logic: CDAC and RDAC pre-driver
		#### CDAC Pre-Driver Sizing
		## InvChain Common
		_CDACPreDriver_Pbody_NumCont=2,  # number #(Fixed)
		_CDACPreDriver_Nbody_NumCont=2,  # number #(Fixed)
		_CDACPreDriver_PMOSXvt2NMOSXvt=500,  # number #(Fixed)
		_CDACPreDriver_XvtTop2Pbody=None,  # number/None(Minimum) #(Fixed)
		_CDACPreDriver_Xvtdown2Nbody=None,  # number/None(Minimum) #(Fixed)

		## Inverter Chain
		## Inv1 common
		_CDACPreDriver_NumberofGate=[[1,1,3,9],[1,1,3,9],[1,1,3,9],[1,1,3,9],[1,1,3,9],[1,1,3,9],[1,1,3,9,7],[1,1,3,9,7],[1,1,3,9,7],[1,1,3,9,7]],  # Vector
		_CDACPreDriver_ChannelLength=30,  # Scalar
		_CDACPreDriver_XVT='SLVT',  # 'SLVT'

		## Inv1 NMOS
		_CDACPreDriver_Inv_NMOS_ChannelWidth=400,  # Scalar
		_CDACPreDriver_Inv_NMOS_POGate_Comb_length=100,  # Scalar #(Fixed)

		## Inv1 PMOS
		_CDACPreDriver_Inv_PMOS_ChannelWidth=800,  # Scalar
		_CDACPreDriver_Inv_PMOS_POGate_Comb_length=100,  # Scalar

		################################################################################################################################## SAR Logic: Inv and AND gate for Driving CLK_Outsamp
		## CLKDout(OutSamp) Inverter & AND Common Option
		_CLKDout_XVT_Common='SLVT',

		## CLKDout(OutSamp) Inverter Size
		_CLKDout_Inv_NMOS_ChannelWidth=400,
		_CLKDout_Inv_NMOS_ChannelLength=30,  # Number
		_CLKDout_Inv_NMOS_NumberofGate=1,  # Number
		_CLKDout_Inv_NMOS_POGate_Comb_length=100,  # None/Number

		_CLKDout_Inv_PMOS_ChannelWidth=800,
		_CLKDout_Inv_PMOS_ChannelLength=30,  # Number
		_CLKDout_Inv_PMOS_NumberofGate=1,  # Number
		_CLKDout_Inv_PMOS_POGate_Comb_length=100,  # None/Number

		## CLKDout(OutSamp) AND Size
			# Nand
			_CLKDout_AND_NAND_NMOS_ChannelWidth=400,
			_CLKDout_AND_NAND_NMOS_ChannelLength=30,
			_CLKDout_AND_NAND_NMOS_NumberofGate=2,

			_CLKDout_AND_NAND_PMOS_ChannelWidth=800,
			_CLKDout_AND_NAND_PMOS_ChannelLength=30,
			_CLKDout_AND_NAND_PMOS_NumberofGate=1,
			# Inv
			_CLKDout_AND_Inv_NMOS_ChannelWidth=400,
			_CLKDout_AND_Inv_NMOS_ChannelLength=30,
			_CLKDout_AND_Inv_NMOS_NumberofGate=4,
			_CLKDout_AND_Inv_NMOS_POGate_Comb_length=100,

			_CLKDout_AND_Inv_PMOS_ChannelWidth=800,
			_CLKDout_AND_Inv_PMOS_ChannelLength=30,
			_CLKDout_AND_Inv_PMOS_NumberofGate=4,
			_CLKDout_AND_Inv_PMOS_POGate_Comb_length=100,

		############################################################################################################################################ Comparator
		## StrongARM Latch
			# PMOS
			_Comp_SALatch_CLKinputPMOSFinger1=1,  #PMOS Reset Sw1 # random.randint(1, 15),  # 6
			_Comp_SALatch_CLKinputPMOSFinger2=1,  #PMOS Reset Sw2 # random.randint(1, 15),  # 3
			_Comp_SALatch_PMOSFinger=1,  		  #PMOS Latch	  # random.randint(1, 15),  # 3
			_Comp_SALatch_PMOSChannelWidth=1000,  #All PMOS width # random.randrange(200, 1050, 2),  # 500

			# NMOS
			_Comp_SALatch_DATAinputNMOSFinger=3,  #NMOS Input Tr # random.randint(3, 15),  # 12
			_Comp_SALatch_NMOSFinger=2,  		  #NMOS at Latch # random.randint(1, 15),  # 2
			_Comp_SALatch_CLKinputNMOSFinger=1,  #NMOS Tail # random.randint(1, 15),  # 8
			_Comp_SALatch_NMOSChannelWidth=330,  #Nmos width # random.randrange(200, 1050, 2),  # 500
			_Comp_SALatch_CLKinputNMOSChannelWidth=200,  # random.randrange(200, 1050, 2),  # 800

			# Common
			_Comp_SALatch_ChannelLength=30,  # random.randrange(30, 60, 2),  # 30
			_Comp_SALatch_Dummy=True,  # (Fixed)
			_Comp_SALatch_XVT='HVT',
			_Comp_SALatch_GuardringWidth=400,  # (Fixed)
			_Comp_SALatch_Guardring=True,  # (Fixed)
			_Comp_SALatch_SlicerGuardringWidth=400,  # (Fixed)
			_Comp_SALatch_SlicerGuardring=None,  # (Fixed)
			_Comp_SALatch_NumSupplyCOY=None,  # (Fixed)
			_Comp_SALatch_NumSupplyCOX=None,  # (Fixed)
			_Comp_SALatch_SupplyMet1XWidth=None,  # (Fixed)
			_Comp_SALatch_SupplyMet1YWidth=None,  # (Fixed)
			_Comp_SALatch_VDD2VSSHeight=None,  # (Fixed)
			_Comp_SALatch_NumVIAPoly2Met1COX=None,  # (Fixed)
			_Comp_SALatch_NumVIAPoly2Met1COY=None,  # (Fixed)
			_Comp_SALatch_NumVIAMet12COX=None,  # (Fixed)
			_Comp_SALatch_NumVIAMet12COY=None,  # (Fixed)
			_Comp_SALatch_PowerLine=False,  # (Fixed)

		## StrongARMLatch Data Output Buffer Sizing
			# Inverter1
			_Comp_SAOutBuf_Inv1_NMOS_ChannelWidth=1000,  # Number
			_Comp_SAOutBuf_Inv1_NMOS_ChannelLength=30,  # Number
			_Comp_SAOutBuf_Inv1_NMOS_NumberofGate=1,  # Number
			_Comp_SAOutBuf_Inv1_NMOS_XVT='SLVT',  # 'XVT' ex)SLVT/LVT/RVT/HVT
			_Comp_SAOutBuf_Inv1_NMOS_POGate_Comb_length=100,  # None/Number #(Fixed)

			_Comp_SAOutBuf_Inv1_PMOS_ChannelWidth=2000,  # Number
			_Comp_SAOutBuf_Inv1_PMOS_ChannelLength=30,  # Number
			_Comp_SAOutBuf_Inv1_PMOS_NumberofGate=1,  # Number
			_Comp_SAOutBuf_Inv1_PMOS_XVT='SLVT',  # 'XVT' ex)SLVT/LVT/RVT/HVT
			_Comp_SAOutBuf_Inv1_PMOS_POGate_Comb_length=100,  # None/Number #(Fixed)

			# Inverter2
			_Comp_SAOutBuf_Inv2_NMOS_ChannelWidth=1000,  # Number
			_Comp_SAOutBuf_Inv2_NMOS_ChannelLength=30,  # Number
			_Comp_SAOutBuf_Inv2_NMOS_NumberofGate=1,  # Number
			_Comp_SAOutBuf_Inv2_NMOS_XVT='SLVT',  # 'XVT' ex)SLVT/LVT/RVT/HVT
			_Comp_SAOutBuf_Inv2_NMOS_POGate_Comb_length=100,  # None/Number #(Fixed)

			_Comp_SAOutBuf_Inv2_PMOS_ChannelWidth=2000,  # Number
			_Comp_SAOutBuf_Inv2_PMOS_ChannelLength=30,  # Number
			_Comp_SAOutBuf_Inv2_PMOS_NumberofGate=1,  # Number
			_Comp_SAOutBuf_Inv2_PMOS_XVT='SLVT',  # 'XVT' ex)SLVT/LVT/RVT/HVT
			_Comp_SAOutBuf_Inv2_PMOS_POGate_Comb_length=100,  # None/Number #(Fixed)

			## SR Latch Size
			_Comp_SRLatch_NAND_NMOS_ChannelWidth=1000,  # Number
			_Comp_SRLatch_NAND_NMOS_ChannelLength=30,  # Number
			_Comp_SRLatch_NAND_NMOS_NumberofGate=2,  # Number
			_Comp_SRLatch_NAND_NMOS_XVT='SLVT',  # 'XVT' ex)SLVT/LVT/RVT/HVT
			_Comp_SRLatch_NAND_NMOS_POGate_Comb_length=100,  # None/Number #(Fixed)

			_Comp_SRLatch_NAND_PMOS_ChannelWidth=2000,  # Number
			_Comp_SRLatch_NAND_PMOS_ChannelLength=30,  # Number
			_Comp_SRLatch_NAND_PMOS_NumberofGate=1,  # Number
			_Comp_SRLatch_NAND_PMOS_XVT='SLVT',  # 'XVT' ex)SLVT/LVT/RVT/HVT
			_Comp_SRLatch_NAND_PMOS_POGate_Comb_length=100,  # None/Number #(Fixed)

		## StrongARMLatch Comparator CLK In Buffer Sizing
			# CLK_Samp Inv Buf
			_Comp_CLKSamp_Inv_NMOS_ChannelWidth=400,
			_Comp_CLKSamp_Inv_NMOS_ChannelLength=30,
			_Comp_CLKSamp_Inv_NMOS_NumberofGate=1,
			_Comp_CLKSamp_Inv_NMOS_XVT='SLVT',
			_Comp_CLKSamp_Inv_NMOS_POGate_Comb_length=100,  # (Fixed)

			_Comp_CLKSamp_Inv_PMOS_ChannelWidth=800,
			_Comp_CLKSamp_Inv_PMOS_ChannelLength=30,
			_Comp_CLKSamp_Inv_PMOS_NumberofGate=1,
			_Comp_CLKSamp_Inv_PMOS_XVT='SLVT',
			_Comp_CLKSamp_Inv_PMOS_POGate_Comb_length=100,  # (Fixed)

			# CLK_source Inv Buf
			_Comp_CLKSrc_Inv_NMOS_ChannelWidth=400,
			_Comp_CLKSrc_Inv_NMOS_ChannelLength=30,
			_Comp_CLKSrc_Inv_NMOS_NumberofGate=1,
			_Comp_CLKSrc_Inv_NMOS_XVT='SLVT',
			_Comp_CLKSrc_Inv_NMOS_POGate_Comb_length=100,  # (Fixed)

			_Comp_CLKSrc_Inv_PMOS_ChannelWidth=800,
			_Comp_CLKSrc_Inv_PMOS_ChannelLength=30,
			_Comp_CLKSrc_Inv_PMOS_NumberofGate=1,
			_Comp_CLKSrc_Inv_PMOS_XVT='SLVT',
			_Comp_CLKSrc_Inv_PMOS_POGate_Comb_length=100,  # (Fixed)

			## CLKSrc & CLKSample AND Gate
				# Nand
				_Comp_AND_NAND_NMOS_ChannelWidth=400,
				_Comp_AND_NAND_NMOS_ChannelLength=30,
				_Comp_AND_NAND_NMOS_NumberofGate=2,
				_Comp_AND_NAND_NMOS_XVT='SLVT',

				_Comp_AND_NAND_PMOS_ChannelWidth=800,
				_Comp_AND_NAND_PMOS_ChannelLength=30,
				_Comp_AND_NAND_PMOS_NumberofGate=1,
				_Comp_AND_NAND_PMOS_XVT='SLVT',

				# Inv
				_Comp_AND_Inv_NMOS_ChannelWidth=400,
				_Comp_AND_Inv_NMOS_ChannelLength=30,
				_Comp_AND_Inv_NMOS_NumberofGate=1,
				_Comp_AND_Inv_NMOS_XVT='SLVT',
				_Comp_AND_Inv_NMOS_POGate_Comb_length=100,  # (Fixed)

				_Comp_AND_Inv_PMOS_ChannelWidth=800,
				_Comp_AND_Inv_PMOS_ChannelLength=30,
				_Comp_AND_Inv_PMOS_NumberofGate=1,
				_Comp_AND_Inv_PMOS_XVT='SLVT',
				_Comp_AND_Inv_PMOS_POGate_Comb_length=100,  # (Fixed)

			## CLK_Comp Buffer
				# Inverter1
				_Comp_CLKBuf_Inv1_NMOS_ChannelWidth=400,  # Number
				_Comp_CLKBuf_Inv1_NMOS_ChannelLength=30,  # Number
				_Comp_CLKBuf_Inv1_NMOS_NumberofGate=2,  # Number
				_Comp_CLKBuf_Inv1_NMOS_XVT='SLVT',  # 'XVT' ex)SLVT/LVT/RVT/HVT
				_Comp_CLKBuf_Inv1_NMOS_POGate_Comb_length=100,  # None/Number #(Fixed)

				_Comp_CLKBuf_Inv1_PMOS_ChannelWidth=800,  # Number
				_Comp_CLKBuf_Inv1_PMOS_ChannelLength=30,  # Number
				_Comp_CLKBuf_Inv1_PMOS_NumberofGate=2,  # Number
				_Comp_CLKBuf_Inv1_PMOS_XVT='SLVT',  # 'XVT' ex)SLVT/LVT/RVT/HVT
				_Comp_CLKBuf_Inv1_PMOS_POGate_Comb_length=100,  # None/Number #(Fixed)

				# Inverter2
				_Comp_CLKBuf_Inv2_NMOS_ChannelWidth=400,  # Number
				_Comp_CLKBuf_Inv2_NMOS_ChannelLength=30,  # Number
				_Comp_CLKBuf_Inv2_NMOS_NumberofGate=4,  # Number
				_Comp_CLKBuf_Inv2_NMOS_XVT='SLVT',  # 'XVT' ex)SLVT/LVT/RVT/HVT
				_Comp_CLKBuf_Inv2_NMOS_POGate_Comb_length=100,  # None/Number #(Fixed)

				_Comp_CLKBuf_Inv2_PMOS_ChannelWidth=800,  # Number
				_Comp_CLKBuf_Inv2_PMOS_ChannelLength=30,  # Number
				_Comp_CLKBuf_Inv2_PMOS_NumberofGate=4,  # Number
				_Comp_CLKBuf_Inv2_PMOS_XVT='SLVT',  # 'XVT' ex)SLVT/LVT/RVT/HVT
				_Comp_CLKBuf_Inv2_PMOS_POGate_Comb_length=100,  # None/Number #(Fixed)

			# PowerRail Placement
			_Comp_BufSR_NMOS_Pbody_NumCont=2,  # (Fixed)
			_Comp_BufSR_NMOS_Pbody_XvtTop2Pbody=1250,  # (Fixed)
			_Comp_BufSR_PMOS_Nbody_NumCont=2,  # (Fixed)
			_Comp_BufSR_PMOS_Nbody_Xvtdown2Nbody=None,  # (Fixed)
			_Comp_BufSR_PMOSXvt2NMOSXvt=1000,

			_Comp_CLKInLogic_NMOS_Pbody_Xvtdown2Pbody=600,  # (Fixed)
			_Comp_CLKInLogic_PMOS_Nbody_NumCont=2,  # (Fixed)
			_Comp_CLKInLogic_PMOS_Nbody_Xvtdown2Nbody=None,  # (Fixed)
			_Comp_CLKInLogic_PMOSXvt2NMOSXvt=1000,

		############################################################################################################################################ CLK_Samp and CLK_source and Comp_out Buf
		# Additional CLKSamp Buffer for Comparator and Sampler
			## InvChain Common
			_Buf_CLKSamp_Pbody_NumCont=2,  # number #(Fixed)
			_Buf_CLKSamp_Nbody_NumCont=2,  # number #(Fixed)
			_Buf_CLKSamp_PMOSXvt2NMOSXvt=500,  # number
			_Buf_CLKSamp_XvtTop2Pbody=None,  # number/None(Minimum) #(Fixed)
			_Buf_CLKSamp_Xvtdown2Nbody=None,  # number/None(Minimum) #(Fixed)

			## Inverter Chain
				## Inv1 common
				_Buf_CLKSamp_NumberofGate=[2,4,8,16],  # Vector
				_Buf_CLKSamp_ChannelLength=30,  # Scalar
				_Buf_CLKSamp_XVT='SLVT',  # 'SLVT'
				## Inv1 NMOS
				_Buf_CLKSamp_Inv_NMOS_ChannelWidth=400,  # Scalar
				_Buf_CLKSamp_Inv_NMOS_POGate_Comb_length=100,  # Scalar #(Fixed)
				## Inv1 PMOS
				_Buf_CLKSamp_Inv_PMOS_ChannelWidth=800,  # Scalar
				_Buf_CLKSamp_Inv_PMOS_POGate_Comb_length=100,  # Scalar #(Fixed)

		# Additional CLK_source Buffer for Comparator
			## InvChain Common
			_Buf_CLKSrc_Pbody_NumCont=2,  # number #(Fixed)
			_Buf_CLKSrc_Nbody_NumCont=2,  # number #(Fixed)
			_Buf_CLKSrc_PMOSXvt2NMOSXvt=500,  # number
			_Buf_CLKSrc_XvtTop2Pbody=None,  # number/None(Minimum) #(Fixed)
			_Buf_CLKSrc_Xvtdown2Nbody=None,  # number/None(Minimum) #(Fixed)

			## Inverter Chain
				## Inv1 common
				_Buf_CLKSrc_NumberofGate=[1,2,4,8],  # Vector
				_Buf_CLKSrc_ChannelLength=30,  # Scalar
				_Buf_CLKSrc_XVT='SLVT',  # 'SLVT'
				## Inv1 NMOS
				_Buf_CLKSrc_Inv_NMOS_ChannelWidth=400,  # Scalar
				_Buf_CLKSrc_Inv_NMOS_POGate_Comb_length=100,  # Scalar #(Fixed)
				## Inv1 PMOS
				_Buf_CLKSrc_Inv_PMOS_ChannelWidth=800,  # Scalar
				_Buf_CLKSrc_Inv_PMOS_POGate_Comb_length=100,  # Scalar #(Fixed)

		# Additional Comp_out Buffer to drive logic
			## InvChain Common
			_Buf_CompOut_Pbody_NumCont=2,  # number #(Fixed)
			_Buf_CompOut_Nbody_NumCont=2,  # number #(Fixed)
			_Buf_CompOut_PMOSXvt2NMOSXvt=500,  # number
			_Buf_CompOut_XvtTop2Pbody=None,  # number/None(Minimum) #(Fixed)
			_Buf_CompOut_Xvtdown2Nbody=None,  # number/None(Minimum) #(Fixed)
			## Inverter Chain
				## Inv1 common
				_Buf_CompOut_NumberofGate=[2, 4],  # Vector
				_Buf_CompOut_ChannelLength=30,  # Scalar
				_Buf_CompOut_XVT='SLVT',  # 'SLVT'
				## Inv1 NMOS
				_Buf_CompOut_Inv_NMOS_ChannelWidth=400,  # Scalar
				_Buf_CompOut_Inv_NMOS_POGate_Comb_length=100,  # Scalar #(Fixed)
				## Inv1 PMOS
				_Buf_CompOut_Inv_PMOS_ChannelWidth=800,  # Scalar
				_Buf_CompOut_Inv_PMOS_POGate_Comb_length=100,  # Scalar #(Fixed)



		############################################################################################################################################ CDAC and CDAC Driver
			## CDAC
				# MOM Element of CDAC
				_CDAC_LayoutOption=[5,6],  # MOM cap으로 사용되는 Metal Layer
				_CDAC_ShieldingLayer=1,     # GND로 연결되는 Shielding Layer Poly:0, M1:1, M2:2 ...
				_CDAC_MetalWidth=50,        # MOM cap의 metal 두께
				_CDAC_MetalLength=2920,     # MOM cap의 Length # (8bit size: 1414/ 10bit size: 2800/ 12bit size: 4200)
				_CDAC_MetalSpacing=50,      # MOM cap의 거리

				# Unit Cap
				_CDAC_NumOfElement=4,       #MOM cap 몇개를 묶어서 하나의 Unit cap으로 할것인가 # (매우 복잡..) Driver Common Centroid가 아니면 1// 맞으면 2

				# Shielding & Top Connect node
				_CDAC_ConnectLength=400,    #shielding Layer에서 위쪽방향으로 extension 될때 거리
				_CDAC_ExtendLength=400,     #shielding layer extension후에 M7으로 연결되는 Via부분 length

				# Dummy Cap Option
				_CDAC_DummyCap_TopBottomShort=None, # True => Top - Bottom Short, False -> Bottom = GND, None => Floating Bottom Node, # True/False, False: Top plate를 GND로 Short 시킴(Top=Bot=GND), True: Top bot를 같은 node로 묶고 floating시킴
				_CDAC_NumOfDummyCaps=10,            # Number of dummy cap(one side)

				# CommonCentroid With Driving node
				_CDAC_CapArrayWDrivingNodeDistance=2000, # DRC Rule, "_CDAC_BotNodeVtcExtensionMetalLayer"의 길이 = CDAC과 Hrz M3(combine)사이 거리
				_CDAC_DriveNodeDistance=279,             # Hrz M3 사이거리
				_CDAC_YWidth_Bottom_Hrz=50,              # Unit cap들을 Combine 하는 Hrz M3의 두께

			## CDAC Driver
			## : Fold1_CC와 Unfolded는 Unit Drv에서 1,2,4,8.. 이런식으로 자동으로 사이징 된다.
			##   Fold1_DrvArrange의 경우는 직접 각 Cap마다 Drv 사이즈를 정할수 있다.

				# "Fold1_DrvArrange" Driver Sizing Option
				# : Driver(Inverter) Sizing Option [int, int, ...] (Drv. Arranged Version을 위한 옵션)
				#   _CalculateDesignParameter_DrvArranged(Fold1_DrvArranged) 일때만 동작하고 나머지에서는 아무런 영향 주지 않음
				#   ex) _Driver_SizeByBit=[8,4,2,1] 이면 [4C 2C C C(no switching)]에 매칭된다.
				#   그러나 1개 가장 오른쪽에 1개 1finger Drv가 하나 더 생긴다. 그것은 Fold이므로 반대편에 no switching C에 사용된다.
				#   이것 사용할때에는 Unit Drv를 잘 고려해야한다.
			_Driver_SizeByBit=[64, 64, 64, 64, 64, 64, 32, 16, 8, 4, 2, 1],  # Drv.CCPlacement == False일때 사용됨.

				# Unit Driver
					# Driver(Inverter) NMOS
					_Driver_NMOS_NumberofGate=1,    # number
					_Driver_NMOS_ChannelWidth=400,  # number (8bit size: 340/ 10bit size: 680/ 12bit size: 1020)
					_Driver_NMOS_Channellength=30,  # number
					_Driver_NMOS_XVT='SLVT',        # 'XVT' ex)SLVT LVT RVT HVT

					# Driver(Inverter) PMOS
					_Driver_PMOS_NumberofGate=1,    # number
					_Driver_PMOS_ChannelWidth=800,  # number (8bit size: 900/ 10bit size: 1800/ 12bit size: 2700)
					_Driver_PMOS_Channellength=30,  # number
					_Driver_PMOS_XVT='SLVT',        # 'XVT' ex)SLVT LVT RVT HVT





		############################################################################################################################################ Bootstrap Sampler


			# Tr1 and Tr2
			# Input/Output node
				# INPUT node
			_Samp_Inputnode_width=600,  # number
				# OUTPUT node
			_Samp_Outputnode_width=600,  # number

				# Tr1
				_Samp_Tr1_NumberofGate=2,  # number
				_Samp_Tr1_ChannelWidth=300,  # number
				_Samp_Tr1_ChannelLength=30,  # number
				_Samp_Tr1_XVT='RVT',  # 'XVT' ex)SLVT LVT RVT HVT

				# Tr2
				_Samp_Tr2_NumberofGate=1,  # number
				_Samp_Tr2_ChannelWidth=1000,  # number
				_Samp_Tr2_ChannelLength=30,  # number
				_Samp_Tr2_XVT='SLVT',  # 'XVT' ex)SLVT LVT RVT HVT

			# Tr4
			_Samp_Tr4_NumberofGate=2,  # number
			_Samp_Tr4_ChannelWidth=500,  # number
			_Samp_Tr4_ChannelLength=30,  # number
			_Samp_Tr4_XVT='SLVT',  # 'XVT' ex)SLVT LVT RVT HVT


			# Tr5 Tr7 Tr9
				# PMOS: Tr5
				_Samp_Tr5_NumberofGate=1,
				_Samp_Tr5_ChannelWidth=1000,  # ref=1000
				_Samp_Tr5_ChannelLength=30,
				_Samp_Tr5_XVT='SLVT',

				# PMOS: Tr7
				_Samp_Tr7_NumberofGate=1,
				_Samp_Tr7_ChannelWidth=1000,
				_Samp_Tr7_ChannelLength=30,
				_Samp_Tr7_XVT='SLVT',

				# PMOS: Tr9
				_Samp_Tr9_NumberofGate=2,
				_Samp_Tr9_ChannelWidth=1000,  # ref = 1000
				_Samp_Tr9_ChannelLength=30,
				_Samp_Tr9_XVT='SLVT',

			# Tr8
			_Samp_Tr8_NumberofGate=2,  # number (ref:4)
			_Samp_Tr8_ChannelWidth=500,  # number (ref:500)
			_Samp_Tr8_ChannelLength=30,  # number (ref:30)
			_Samp_Tr8_XVT='SLVT',  # 'XVT' ex)SLVT LVT RVT HVT

			# Tr6 and Guardring
				#Tr6
				_Samp_Tr6_NumberofGate=1,  # number
				_Samp_Tr6_ChannelWidth=1000,  # number
				_Samp_Tr6_ChannelLength=30,  # number
				_Samp_Tr6_XVT='SLVT',  # 'XVT' ex)SLVT LVT RVT HVT

			# PMOS: Tr11 and Guardring
				# Tr11
				_Samp_Tr11_NumberofGate=2,
				_Samp_Tr11_ChannelWidth=1000,
				_Samp_Tr11_ChannelLength=30,
				_Samp_Tr11_XVT='SLVT',

			## VddTieCell4
				# VddTieCell4 NMOS
				_Samp_Tie4N_NumberofGate=4,  # number
				_Samp_Tie4N_ChannelWidth=250,  # number
				_Samp_Tie4N_ChannelLength=30,  # number
				_Samp_Tie4N_XVT='SLVT',  # 'XVT' ex)SLVT LVT RVT HVT

				# VddTieCell4 PMOS
				_Samp_Tie4P_NumberofGate=4,  # number
				_Samp_Tie4P_ChannelWidth=500,  # number
				_Samp_Tie4P_ChannelLength=30,  # number
				_Samp_Tie4P_XVT='SLVT',  # 'XVT' ex)SLVT LVT RVT HVT

			## VddTieCell8
				# VddTieCell8 NMOS
				_Samp_Tie8N_NumberofGate=4,  # number
				_Samp_Tie8N_ChannelWidth=250,  # number
				_Samp_Tie8N_ChannelLength=30,  # number
				_Samp_Tie8N_XVT='SLVT',  # 'XVT' ex)SLVT LVT RVT HVT

				# VddTieCell8 PMOS
				_Samp_Tie8P_NumberofGate=4,  # number
				_Samp_Tie8P_ChannelWidth=500,  # number
				_Samp_Tie8P_ChannelLength=30,  # number
				_Samp_Tie8P_XVT='SLVT',  # 'XVT' ex)SLVT LVT RVT HVT

			# Tr12
			_Samp_Tr12_NumberofGate=1,  # number
			_Samp_Tr12_ChannelWidth=1000,  # number
			_Samp_Tr12_ChannelLength=30,  # number
			_Samp_Tr12_XVT='SLVT',  # 'XVT' ex)SLVT LVT RVT HVT

			# Tr3
			_Samp_Tr3_NumberofGate=1,  # number
			_Samp_Tr3_ChannelWidth=1000,  # number
			_Samp_Tr3_ChannelLength=30,  # number
			_Samp_Tr3_XVT='SLVT',  # 'XVT' ex)SLVT LVT RVT HVT

			# Tr10 and Guardring
				#Tr10
				_Samp_Tr10_NumberofGate=1,  # number
				_Samp_Tr10_ChannelWidth=1000,  # number
				_Samp_Tr10_ChannelLength=30,  # number
				_Samp_Tr10_XVT='SLVT',  # 'XVT' ex)SLVT LVT RVT HVT

			# HDVNCAP_Array
			_Samp_HDVNCAP_Length=6000,
			_Samp_HDVNCAP_LayoutOption=[3, 4, 5, 6],
			_Samp_HDVNCAP_NumFigPair=53,
			_Samp_HDVNCAP_Array=3,  # number: 1xnumber
			_Samp_HDVNCAP_Cbot_Ctop_metalwidth=1000,  # number
			# Total HDVNCapSize = 601fF

			## BootStrapped Sampler CLKB Inverter
			_CLKBInv_NMOS_NumberofGate=16,
			_CLKBInv_NMOS_ChannelWidth=400,
			_CLKBInv_NMOS_ChannelLength=30,
			_CLKBInv_NMOS_XVT='SLVT',
			_CLKBInv_NMOS_POGate_Comb_length=None,

			_CLKBInv_PMOS_NumberofGate=16,
			_CLKBInv_Inv_PMOS_ChannelWidth=800,
			_CLKBInv_PMOS_ChannelLength=30,
			_CLKBInv_PMOS_XVT='SLVT',
			_CLKBInv_PMOS_POGate_Comb_length=None,

			_CLKBInv_Pbody_NumCont=2,
			_CLKBInv_XvtTop2Pbody=None,
			_CLKBInv_Nbody_NumCont=2,
			_CLKBInv_Xvtdown2Nbody=None,
			_CLKBInv_PMOSXvt2NMOSXvt=500,




		############################################################################################################################################ RDAC and Decoder
			#RDAC and Decoder delta X displacement for DRC
			_RDAC_displacement = +11000,

			#RDAC and Decoder Size : Consider "_Decoder_RBit" and "_Unit_Num_EachStag_input" ex) [2, 8] --> 4 : 2*8 = 2**4
			_RDAC_Size = [1, 16],

			#RDAC
				# Guardring
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
				#_Decoder_RBit = 2, --> 위에서 겹침

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
								_Nand_NMOS_ChannelWidth                 = [800],  # Number
								# Source_node setting
								_Nand_NMOS_Source_Via_Close2POpin_TF    = [False],  # True/False --> First MOS
							# Pulldown(PMOS)
								# Physical dimension
								_Nand_PMOS_ChannelWidth                 = [400],  # Number
					# Nor( _Unit_Num_EachStag_input에서 2,4,6,7...번째 해당하는 nor 생성)----------> not used
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
	LayoutObj = _R00C13H02L00(_DesignParameter=None, _Name=cellname)
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

	with open('LayoutObj.pkl', 'wb') as f:
		pickle.dump(LayoutObj, f)

	# end of 'main():' ---------------------------------------------------------------------------------------------
