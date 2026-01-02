
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


## Define Class
class _Placement(StickDiagram_KJH1._StickDiagram_KJH):

    ## Input Parameters for Design Calculation: Used when import Sref
    _ParametersForDesignCalculation = dict(
    # Unit
        _GatetoGateDist=100,

        # Inputs of Nand,Nor
        _Unit_Num_EachStag_input = [4,3,2,2], # ex) [2,3,4] 가장 마지막단(TG driving) nand input4, Nor input3, Nand input2, Nor input2 ...

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
            _Nand_ChannelLength     = [30,50],  # Number
            _Nand_POGate_ViaMxMx    = [[0, 1],[0, 3]],  # Ex) [1,5] -> ViaM1M5
            _Nand_XVT               = ['SLVT','SLVT'],  # 'XVT' ex)SLVT/LVT/RVT/HVT
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
            _Nor_ChannelLength      = [30,80],  # Number
            _Nor_POGate_ViaMxMx     = [[0, 3],[0, 1]],  # Ex) [1,5] -> ViaM1M5
            _Nor_XVT	            = ['SLVT','SLVT'],   # 'XVT' ex)SLVT/LVT/RVT/HVT
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
        _Inv_XVT            ='SLVT',

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
        _Xgate_XVT              ='SLVT',

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
      _GatetoGateDist=100,

        # Inputs of Nand,Nor
        _Unit_Num_EachStag_input = [4,3,2,2], # ex) [2,3,4] 가장 마지막단(TG driving) nand input4, Nor input3, Nand input2, Nor input2 ...

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
            _Nand_ChannelLength     = [30,50],  # Number
            _Nand_POGate_ViaMxMx    = [[0, 1],[0, 3]],  # Ex) [1,5] -> ViaM1M5
            _Nand_XVT               = ['SLVT','SLVT'],  # 'XVT' ex)SLVT/LVT/RVT/HVT
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
            _Nor_ChannelLength      = [30,80],  # Number
            _Nor_POGate_ViaMxMx     = [[0, 3],[0, 1]],  # Ex) [1,5] -> ViaM1M5
            _Nor_XVT	            = ['SLVT','SLVT'],   # 'XVT' ex)SLVT/LVT/RVT/HVT
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
        _Inv_XVT            ='SLVT',

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
        _Xgate_XVT              ='SLVT',

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

        ## ########## ########## ########## ########## ########## ########## ########## ########## ########## ########## ########## ########## Calculate Pbody and Nbody height
        ## temp
        XvtTop2Pbody = 0
        XvtDown2Nbody = 0
        PmosMaxXvtSize = 0
        NmosMaxXvtSize = 0

        ## ########## ########## ########## ########## ########## ########## ########## ########## ########## ########## ########## P/Nbody height: Nand/Nor gen.
        for i in range(0,len(_Unit_Num_EachStag_input)):

            ## ########## ########## ########## ########## ########## ########## ########## ########## ########## P/Nbody height: Nand/Nor gen.: Nand
            if i%2 ==0:
                ##
                k = int(i/2)
                ## Copy Calculation_Parameters from low-level-block ex)copy.deepcopy(B16_nmos_power_v2._NMOS_POWER._ParametersForDesignCalculation)
                _Caculation_Parameters = copy.deepcopy(Q00_02_Nand_KJH0._Nand._ParametersForDesignCalculation)
                ## Define Calculation_Parameters ex) _Caculation_Parameters['_NMOSPOWER_PbodyContact_1_Length']  = _NMOSPOWER_PbodyContact_1_Length
                _Caculation_Parameters['_Nand_Num_Input']                       = _Unit_Num_EachStag_input[i]

                _Caculation_Parameters['_Nand_NumberofGate']                    = _Nand_NumberofGate[k]
                _Caculation_Parameters['_Nand_ChannelLength']                   = _Nand_ChannelLength[k]
                _Caculation_Parameters['_Nand_POGate_ViaMxMx']                  = _Nand_POGate_ViaMxMx[k]
                _Caculation_Parameters['_Nand_XVT']                             = _Nand_XVT[k]

                _Caculation_Parameters['_Nand_NMOS_ChannelWidth']               = _Nand_NMOS_ChannelWidth[k]
                _Caculation_Parameters['_Nand_NMOS_Source_Via_Close2POpin_TF']  = _Nand_NMOS_Source_Via_Close2POpin_TF[k]
                _Caculation_Parameters['_Nand_NMOS_POGate_Comb_length']         = _Unit_POGate_Comb_length
                _Caculation_Parameters['_Nand_PMOS_ChannelWidth']               = _Nand_PMOS_ChannelWidth[k]
                _Caculation_Parameters['_Nand_PMOS_POGate_Comb_length']         = _Unit_POGate_Comb_length

                _Caculation_Parameters['_Nand_Pbody_NumCont']                   = _Unit_Pbody_NumCont
                _Caculation_Parameters['_Nand_Pbody_XvtTop2Pbody']              = _Unit_Pbody_XvtTop2Pbody
                _Caculation_Parameters['_Nand_Nbody_NumCont']                   = _Unit_Nbody_NumCont
                _Caculation_Parameters['_Nand_Nbody_Xvtdown2Nbody']             = _Unit_Nbody_Xvtdown2Nbody
                _Caculation_Parameters['_Nand_PMOSXvt2NMOSXvt']                 = _Unit_PMOSXvt2NMOSXvt

                ## Generate Sref: ex)self._DesignParameter['_NMOS_POWER'] = self._SrefElementDeclaration(_DesignObj=B16_nmos_power_v2._NMOS_POWER( _DesignParameter=None, _Name='{}:NMOS_POWER'.format(_Name)))[0]
                self._DesignParameter['SRF_Nand{}'.format(i)] = self._SrefElementDeclaration(_DesignObj=Q00_02_Nand_KJH0._Nand(_DesignParameter=None, _Name='{}:SRF_Nand{}'.format(_Name,i)))[0]

                ## Define Sref Reflection: ex)self._DesignParameter['_NMOS_POWER']['_Reflect'] = [0, 0, 0]
                self._DesignParameter['SRF_Nand{}'.format(i)]['_Reflect'] = [0, 0, 0]

                ## Define Sref Angle: ex)'_NMOS_POWER'
                self._DesignParameter['SRF_Nand{}'.format(i)]['_Angle'] = 0

                ## Calculate Sref Layer by using Calculation_Parameter: ex)'_NMOS_POWER'
                self._DesignParameter['SRF_Nand{}'.format(i)]['_DesignObj']._CalculateDesignParameter(**_Caculation_Parameters)

                ## Define Sref _XYcoordinate: ex)'_NMOS_POWER'
                self._DesignParameter['SRF_Nand{}'.format(i)]['_XYCoordinates'] = [[0, 0]]

                ## Find XvtTop2Pbody_tmp and XvtDown2Nbody_tmp
                tmp1 = self.get_param_KJH4('SRF_Nand{}'.format(i),'SRF_Pullup', 'SRF_PMOS0', 'BND_{}Layer'.format(_Nand_XVT[k]))
                tmp2 = self.get_param_KJH4('SRF_Nand{}'.format(i), 'SRF_Nbody', 'SRF_NbodyContactPhyLen', 'BND_Met1Layer')
                XvtDown2Nbody_tmp = abs(tmp2[0][0][0][0][0]['_XY_down'][1] - tmp1[0][0][0][0][0]['_XY_down'][1])

                if XvtDown2Nbody_tmp > XvtDown2Nbody:
                    XvtDown2Nbody = XvtDown2Nbody_tmp

                tmp3 = self.get_param_KJH4('SRF_Nand{}'.format(i), 'SRF_Pulldown', 'SRF_NMOS0', 'BND_{}Layer'.format(_Nand_XVT[k]))
                tmp4 = self.get_param_KJH4('SRF_Nand{}'.format(i), 'SRF_Pbody', 'SRF_PbodyContactPhyLen', 'BND_Met1Layer')
                XvtTop2Pbody_tmp = abs(tmp3[0][0][0][0][0]['_XY_up'][1] - tmp4[0][0][0][0][0]['_XY_up'][1])

                if XvtTop2Pbody_tmp > XvtTop2Pbody:
                    XvtTop2Pbody = XvtTop2Pbody_tmp

                if tmp1[0][0][0][0][0]['_Ywidth'] > PmosMaxXvtSize:
                    PmosMaxXvtSize = tmp1[0][0][0][0][0]['_Ywidth']

                if tmp3[0][0][0][0][0]['_Ywidth'] > NmosMaxXvtSize:
                    NmosMaxXvtSize = tmp3[0][0][0][0][0]['_Ywidth']

            ## ########## ########## ########## ########## ########## ########## ########## ########## ########## P/Nbody height: Nand/Nor gen.: Nor
            else:
                k = int(i//2)
                ## Copy Calculation_Parameters from low-level-block ex)copy.deepcopy(B16_nmos_power_v2._NMOS_POWER._ParametersForDesignCalculation)
                _Caculation_Parameters = copy.deepcopy(Q01_02_Nor_KJH0._Nor._ParametersForDesignCalculation)
                ## Define Calculation_Parameters ex) _Caculation_Parameters['_NMOSPOWER_PbodyContact_1_Length']  = _NMOSPOWER_PbodyContact_1_Length
                _Caculation_Parameters['_Nor_Num_Input']                       = _Unit_Num_EachStag_input[i]

                _Caculation_Parameters['_Nor_ChannelLength']                   = _Nor_ChannelLength[k]
                _Caculation_Parameters['_Nor_POGate_ViaMxMx']                  = _Nor_POGate_ViaMxMx[k]
                _Caculation_Parameters['_Nor_XVT']                             = _Nor_XVT[k]

                _Caculation_Parameters['_Nor_NMOS_ChannelWidth']               = _Nor_NMOS_ChannelWidth[k]
                _Caculation_Parameters['_Nor_NMOS_NumberofGate']               = _Nor_NMOS_NumberofGate[k]
                _Caculation_Parameters['_Nor_NMOS_POGate_Comb_length']         = _Unit_POGate_Comb_length
                _Caculation_Parameters['_Nor_PMOS_ChannelWidth']               = _Nor_PMOS_ChannelWidth[k]
                _Caculation_Parameters['_Nor_PMOS_NumberofGate']               = _Nor_PMOS_NumberofGate[k]
                _Caculation_Parameters['_Nor_PMOS_Source_Via_Close2POpin_TF']  = _Nor_PMOS_Source_Via_Close2POpin_TF[k]
                _Caculation_Parameters['_Nor_PMOS_POGate_Comb_length']         = _Unit_POGate_Comb_length

                _Caculation_Parameters['_Nor_Pbody_NumCont']                   = _Unit_Pbody_NumCont
                _Caculation_Parameters['_Nor_Pbody_XvtTop2Pbody']              = _Unit_Pbody_XvtTop2Pbody
                _Caculation_Parameters['_Nor_Nbody_NumCont']                   = _Unit_Nbody_NumCont
                _Caculation_Parameters['_Nor_Nbody_Xvtdown2Nbody']             = _Unit_Nbody_Xvtdown2Nbody
                _Caculation_Parameters['_Nor_PMOSXvt2NMOSXvt']                 = _Unit_PMOSXvt2NMOSXvt

                ## Generate Sref: ex)self._DesignParameter['_NMOS_POWER'] = self._SrefElementDeclaration(_DesignObj=B16_nmos_power_v2._NMOS_POWER( _DesignParameter=None, _Name='{}:NMOS_POWER'.format(_Name)))[0]
                self._DesignParameter['SRF_Nor{}'.format(i)] = self._SrefElementDeclaration(_DesignObj=Q01_02_Nor_KJH0._Nor(_DesignParameter=None, _Name='{}:SRF_Nor{}'.format(_Name,i)))[0]

                ## Define Sref Reflection: ex)self._DesignParameter['_NMOS_POWER']['_Reflect'] = [0, 0, 0]
                self._DesignParameter['SRF_Nor{}'.format(i)]['_Reflect'] = [0, 0, 0]

                ## Define Sref Angle: ex)'_NMOS_POWER'
                self._DesignParameter['SRF_Nor{}'.format(i)]['_Angle'] = 0

                ## Calculate Sref Layer by using Calculation_Parameter: ex)'_NMOS_POWER'
                self._DesignParameter['SRF_Nor{}'.format(i)]['_DesignObj']._CalculateDesignParameter(**_Caculation_Parameters)

                ## Define Sref _XYcoordinate: ex)'_NMOS_POWER'
                self._DesignParameter['SRF_Nor{}'.format(i)]['_XYCoordinates'] = [[0, 0]]

                ## Find XvtTop2Pbody_tmp and XvtDown2Nbody_tmp
                tmp1 = self.get_param_KJH4('SRF_Nor{}'.format(i),'SRF_Pullup', 'SRF_PMOS0', 'BND_{}Layer'.format(_Nand_XVT[k]))
                tmp2 = self.get_param_KJH4('SRF_Nor{}'.format(i), 'SRF_Nbody', 'SRF_NbodyContactPhyLen', 'BND_Met1Layer')
                XvtDown2Nbody_tmp = abs(tmp2[0][0][0][0][0]['_XY_down'][1] - tmp1[0][0][0][0][0]['_XY_down'][1])

                if XvtDown2Nbody_tmp > XvtDown2Nbody:
                    XvtDown2Nbody = XvtDown2Nbody_tmp

                tmp3 = self.get_param_KJH4('SRF_Nor{}'.format(i),'SRF_Pulldown', 'SRF_NMOS0', 'BND_{}Layer'.format(_Nand_XVT[k]))
                tmp4 = self.get_param_KJH4('SRF_Nor{}'.format(i), 'SRF_Pbody', 'SRF_PbodyContactPhyLen', 'BND_Met1Layer')
                XvtTop2Pbody_tmp = abs(tmp3[0][0][0][0][0]['_XY_up'][1] - tmp4[0][0][0][0][0]['_XY_up'][1])

                if XvtTop2Pbody_tmp > XvtTop2Pbody:
                    XvtTop2Pbody = XvtTop2Pbody_tmp

                if tmp1[0][0][0][0][0]['_Ywidth'] > PmosMaxXvtSize:
                    PmosMaxXvtSize = tmp1[0][0][0][0][0]['_Ywidth']

                if tmp3[0][0][0][0][0]['_Ywidth'] > NmosMaxXvtSize:
                    NmosMaxXvtSize = tmp3[0][0][0][0][0]['_Ywidth']

        ## ########## ########## ########## ########## ########## ########## ########## ########## ########## P/Nbody height: Inv
        ## Copy Calculation_Parameters from low-level-block ex)copy.deepcopy(B16_nmos_power_v2._NMOS_POWER._ParametersForDesignCalculation)
        _Caculation_Parameters = copy.deepcopy(Q03_00_Inv_KJH0._Inv._ParametersForDesignCalculation)
        ## Define Calculation_Parameters ex) _Caculation_Parameters['_NMOSPOWER_PbodyContact_1_Length']  = _NMOSPOWER_PbodyContact_1_Length
        _Caculation_Parameters['_Inv_NumberofGate']                    = _Inv_NumberofGate
        _Caculation_Parameters['_Inv_ChannelLength']                   = _Inv_ChannelLength
        _Caculation_Parameters['_Inv_XVT']                             = _Inv_XVT

        _Caculation_Parameters['_Inv_NMOS_ChannelWidth']               = _Inv_NMOS_ChannelWidth
        _Caculation_Parameters['_Inv_NMOS_POGate_Comb_length']         = _Unit_POGate_Comb_length
        _Caculation_Parameters['_Inv_NMOS_POGate_ViaMxMx']             = _Inv_NMOS_POGate_ViaMxMx

        _Caculation_Parameters['_Inv_PMOS_ChannelWidth']               = _Inv_PMOS_ChannelWidth
        _Caculation_Parameters['_Inv_PMOS_POGate_Comb_length']         = _Unit_POGate_Comb_length
        _Caculation_Parameters['_Inv_PMOS_POGate_ViaMxMx']             = _Inv_PMOS_POGate_ViaMxMx

        _Caculation_Parameters['_Inv_Pbody_NumCont']                   = _Unit_Pbody_NumCont
        _Caculation_Parameters['_Inv_Pbody_XvtTop2Pbody']              = _Unit_Pbody_XvtTop2Pbody
        _Caculation_Parameters['_Inv_Nbody_NumCont']                   = _Unit_Nbody_NumCont
        _Caculation_Parameters['_Inv_Nbody_Xvtdown2Nbody']             = _Unit_Nbody_Xvtdown2Nbody
        _Caculation_Parameters['_Inv_PMOSXvt2NMOSXvt']                 = _Unit_PMOSXvt2NMOSXvt

        ## Generate Sref: ex)self._DesignParameter['_NMOS_POWER'] = self._SrefElementDeclaration(_DesignObj=B16_nmos_power_v2._NMOS_POWER( _DesignParameter=None, _Name='{}:NMOS_POWER'.format(_Name)))[0]
        self._DesignParameter['SRF_Inv'] = self._SrefElementDeclaration(_DesignObj=Q03_00_Inv_KJH0._Inv(_DesignParameter=None, _Name='{}:SRF_Inv'.format(_Name)))[0]

        ## Define Sref Reflection: ex)self._DesignParameter['_NMOS_POWER']['_Reflect'] = [0, 0, 0]
        self._DesignParameter['SRF_Inv']['_Reflect'] = [0, 0, 0]

        ## Define Sref Angle: ex)'_NMOS_POWER'
        self._DesignParameter['SRF_Inv']['_Angle'] = 0

        ## Calculate Sref Layer by using Calculation_Parameter: ex)'_NMOS_POWER'
        self._DesignParameter['SRF_Inv']['_DesignObj']._CalculateDesignParameter(**_Caculation_Parameters)

        ## Define Sref _XYcoordinate: ex)'_NMOS_POWER'
        self._DesignParameter['SRF_Inv']['_XYCoordinates'] = [[0, 0]]

        ## Find XvtTop2Pbody_tmp and XvtDown2Nbody_tmp
        tmp1 = self.get_param_KJH4('SRF_Inv', 'SRF_PMOS', 'BND_{}Layer'.format(_Inv_XVT))
        tmp2 = self.get_param_KJH4('SRF_Inv','SRF_Nbody', 'SRF_NbodyContactPhyLen', 'BND_Met1Layer')
        XvtDown2Nbody_tmp = abs(tmp2[0][0][0][0][0]['_XY_down'][1] - tmp1[0][0][0][0]['_XY_down'][1])

        if XvtDown2Nbody_tmp > XvtDown2Nbody:
            XvtDown2Nbody = XvtDown2Nbody_tmp

        tmp3 = self.get_param_KJH4('SRF_Inv', 'SRF_NMOS', 'BND_{}Layer'.format(_Inv_XVT))
        tmp4 = self.get_param_KJH4('SRF_Inv', 'SRF_Pbody', 'SRF_PbodyContactPhyLen', 'BND_Met1Layer')
        XvtTop2Pbody_tmp = abs(tmp3[0][0][0][0]['_XY_up'][1] - tmp4[0][0][0][0][0]['_XY_up'][1])

        if XvtTop2Pbody_tmp > XvtTop2Pbody:
            XvtTop2Pbody = XvtTop2Pbody_tmp

        if tmp1[0][0][0][0]['_Ywidth'] > PmosMaxXvtSize:
            PmosMaxXvtSize = tmp1[0][0][0][0]['_Ywidth']

        if tmp3[0][0][0][0]['_Ywidth'] > NmosMaxXvtSize:
            NmosMaxXvtSize = tmp3[0][0][0][0]['_Ywidth']

        ## ########## ########## ########## ########## ########## ########## ########## ########## ########## P/Nbody height: Xgate
        ## Copy Calculation_Parameters from low-level-block ex)copy.deepcopy(B16_nmos_power_v2._NMOS_POWER._ParametersForDesignCalculation)
        _Caculation_Parameters = copy.deepcopy(Q02_00_Xgate_KJH0._Xgate._ParametersForDesignCalculation)
        ## Define Calculation_Parameters ex) _Caculation_Parameters['_NMOSPOWER_PbodyContact_1_Length']  = _NMOSPOWER_PbodyContact_1_Length
        _Caculation_Parameters['_Xgate_NumberofGate']                    = _Xgate_NumberofGate
        _Caculation_Parameters['_Xgate_ChannelLength']                   = _Xgate_ChannelLength
        _Caculation_Parameters['_Xgate_XVT']                             = _Xgate_XVT

        _Caculation_Parameters['_Xgate_NMOS_ChannelWidth']               = _Xgate_NMOS_ChannelWidth
        _Caculation_Parameters['_Xgate_NMOS_POGate_Comb_length']         = _Unit_POGate_Comb_length
        _Caculation_Parameters['_Xgate_NMOS_POGate_ViaMxMx']             = _Xgate_NMOS_POGate_ViaMxMx

        _Caculation_Parameters['_Xgate_PMOS_ChannelWidth']               = _Xgate_PMOS_ChannelWidth
        _Caculation_Parameters['_Xgate_PMOS_POGate_Comb_length']         = _Unit_POGate_Comb_length
        _Caculation_Parameters['_Xgate_PMOS_POGate_ViaMxMx']             = _Xgate_PMOS_POGate_ViaMxMx

        _Caculation_Parameters['_Xgate_Pbody_NumCont']                   = _Unit_Pbody_NumCont
        _Caculation_Parameters['_Xgate_Pbody_XvtTop2Pbody']              = _Unit_Pbody_XvtTop2Pbody
        _Caculation_Parameters['_Xgate_Nbody_NumCont']                   = _Unit_Nbody_NumCont
        _Caculation_Parameters['_Xgate_Nbody_Xvtdown2Nbody']             = _Unit_Nbody_Xvtdown2Nbody
        _Caculation_Parameters['_Xgate_PMOSXvt2NMOSXvt']                 = _Unit_PMOSXvt2NMOSXvt

        ## Generate Sref: ex)self._DesignParameter['_NMOS_POWER'] = self._SrefElementDeclaration(_DesignObj=B16_nmos_power_v2._NMOS_POWER( _DesignParameter=None, _Name='{}:NMOS_POWER'.format(_Name)))[0]
        self._DesignParameter['SRF_Xgate'] = self._SrefElementDeclaration(_DesignObj=Q02_00_Xgate_KJH0._Xgate(_DesignParameter=None, _Name='{}:SRF_Xgate'.format(_Name)))[0]

        ## Define Sref Reflection: ex)self._DesignParameter['_NMOS_POWER']['_Reflect'] = [0, 0, 0]
        self._DesignParameter['SRF_Xgate']['_Reflect'] = [0, 0, 0]

        ## Define Sref Angle: ex)'_NMOS_POWER'
        self._DesignParameter['SRF_Xgate']['_Angle'] = 0

        ## Calculate Sref Layer by using Calculation_Parameter: ex)'_NMOS_POWER'
        self._DesignParameter['SRF_Xgate']['_DesignObj']._CalculateDesignParameter(**_Caculation_Parameters)

        ## Define Sref _XYcoordinate: ex)'_NMOS_POWER'
        self._DesignParameter['SRF_Xgate']['_XYCoordinates'] = [[0, 0]]

        ## Find XvtTop2Pbody_tmp and XvtDown2Nbody_tmp
        tmp1 = self.get_param_KJH4('SRF_Xgate', 'SRF_PMOS', 'BND_{}Layer'.format(_Xgate_XVT))
        tmp2 = self.get_param_KJH4('SRF_Xgate','SRF_Nbody', 'SRF_NbodyContactPhyLen', 'BND_Met1Layer')
        XvtDown2Nbody_tmp = abs(tmp2[0][0][0][0][0]['_XY_down'][1] - tmp1[0][0][0][0]['_XY_down'][1])

        if XvtDown2Nbody_tmp > XvtDown2Nbody:
            XvtDown2Nbody = XvtDown2Nbody_tmp

        tmp3 = self.get_param_KJH4('SRF_Xgate', 'SRF_NMOS', 'BND_{}Layer'.format(_Xgate_XVT))
        tmp4 = self.get_param_KJH4('SRF_Xgate', 'SRF_Pbody', 'SRF_PbodyContactPhyLen', 'BND_Met1Layer')
        XvtTop2Pbody_tmp = abs(tmp3[0][0][0][0]['_XY_up'][1] - tmp4[0][0][0][0][0]['_XY_up'][1])

        if XvtTop2Pbody_tmp > XvtTop2Pbody:
            XvtTop2Pbody = XvtTop2Pbody_tmp

        if tmp1[0][0][0][0]['_Ywidth'] > PmosMaxXvtSize:
            PmosMaxXvtSize = tmp1[0][0][0][0]['_Ywidth']

        if tmp3[0][0][0][0]['_Ywidth'] > NmosMaxXvtSize:
            NmosMaxXvtSize = tmp3[0][0][0][0]['_Ywidth']































        ## ########## ########## ########## ########## ########## ########## ########## ########## ########## ########## ########## ########## Real_placement
        ## ########## ########## ########## ########## ########## ########## ########## ########## ########## ########## ########## Real_placement: Nand/Nor gen.
        for i in range(0,len(_Unit_Num_EachStag_input)):

            # BSking is iteration of for loop
            if i ==1:
                BSking = _Unit_Num_EachStag_input[i-1]
            elif i==0:
                pass
            else:
                BSking = BSking * _Unit_Num_EachStag_input[i-1]

            ## ########## ########## ########## ########## ########## ########## ########## ########## ########## Real_placement: Nand/Nor gen.: Nand
            if i%2 ==0:
                if i ==0:
                    ##
                    k = int(i/2)
                    ## Copy Calculation_Parameters from low-level-block ex)copy.deepcopy(B16_nmos_power_v2._NMOS_POWER._ParametersForDesignCalculation)
                    _Caculation_Parameters = copy.deepcopy(Q00_02_Nand_KJH0._Nand._ParametersForDesignCalculation)
                    ## Define Calculation_Parameters ex) _Caculation_Parameters['_NMOSPOWER_PbodyContact_1_Length']  = _NMOSPOWER_PbodyContact_1_Length
                    _Caculation_Parameters['_Nand_Num_Input']                       = _Unit_Num_EachStag_input[i]

                    _Caculation_Parameters['_Nand_NumberofGate']                    = _Nand_NumberofGate[k]
                    _Caculation_Parameters['_Nand_ChannelLength']                   = _Nand_ChannelLength[k]
                    _Caculation_Parameters['_Nand_POGate_ViaMxMx']                  = _Nand_POGate_ViaMxMx[k]
                    _Caculation_Parameters['_Nand_XVT']                             = _Nand_XVT[k]

                    _Caculation_Parameters['_Nand_NMOS_ChannelWidth']               = _Nand_NMOS_ChannelWidth[k]
                    _Caculation_Parameters['_Nand_NMOS_Source_Via_Close2POpin_TF']  = _Nand_NMOS_Source_Via_Close2POpin_TF[k]
                    _Caculation_Parameters['_Nand_NMOS_POGate_Comb_length']         = _Unit_POGate_Comb_length
                    _Caculation_Parameters['_Nand_PMOS_ChannelWidth']               = _Nand_PMOS_ChannelWidth[k]
                    _Caculation_Parameters['_Nand_PMOS_POGate_Comb_length']         = _Unit_POGate_Comb_length

                    _Caculation_Parameters['_Nand_Pbody_NumCont']                   = _Unit_Pbody_NumCont
                    _Caculation_Parameters['_Nand_Pbody_XvtTop2Pbody']              = XvtTop2Pbody
                    _Caculation_Parameters['_Nand_Nbody_NumCont']                   = _Unit_Nbody_NumCont
                    _Caculation_Parameters['_Nand_Nbody_Xvtdown2Nbody']             = XvtDown2Nbody
                    _Caculation_Parameters['_Nand_PMOSXvt2NMOSXvt']                 = _Unit_PMOSXvt2NMOSXvt

                    ## Generate Sref: ex)self._DesignParameter['_NMOS_POWER'] = self._SrefElementDeclaration(_DesignObj=B16_nmos_power_v2._NMOS_POWER( _DesignParameter=None, _Name='{}:NMOS_POWER'.format(_Name)))[0]
                    self._DesignParameter['SRF_Nand{}'.format(i)] = self._SrefElementDeclaration(_DesignObj=Q00_02_Nand_KJH0._Nand(_DesignParameter=None, _Name='{}:SRF_Nand{}'.format(_Name,i)))[0]

                    ## Define Sref Reflection: ex)self._DesignParameter['_NMOS_POWER']['_Reflect'] = [0, 0, 0]
                    self._DesignParameter['SRF_Nand{}'.format(i)]['_Reflect'] = [0, 0, 0]

                    ## Define Sref Angle: ex)'_NMOS_POWER'
                    self._DesignParameter['SRF_Nand{}'.format(i)]['_Angle'] = 0

                    ## Calculate Sref Layer by using Calculation_Parameter: ex)'_NMOS_POWER'
                    self._DesignParameter['SRF_Nand{}'.format(i)]['_DesignObj']._CalculateDesignParameter(**_Caculation_Parameters)

                    ## Define Sref _XYcoordinate: ex)'_NMOS_POWER'
                    self._DesignParameter['SRF_Nand{}'.format(i)]['_XYCoordinates'] = [[0, 0]]

                else:
                    ##
                    k = int(i / 2)
                    ## Copy Calculation_Parameters from low-level-block ex)copy.deepcopy(B16_nmos_power_v2._NMOS_POWER._ParametersForDesignCalculation)
                    _Caculation_Parameters = copy.deepcopy(Q00_02_Nand_KJH0._Nand._ParametersForDesignCalculation)
                    ## Define Calculation_Parameters ex) _Caculation_Parameters['_NMOSPOWER_PbodyContact_1_Length']  = _NMOSPOWER_PbodyContact_1_Length
                    _Caculation_Parameters['_Nand_Num_Input'] = _Unit_Num_EachStag_input[i]

                    _Caculation_Parameters['_Nand_NumberofGate'] = _Nand_NumberofGate[k]
                    _Caculation_Parameters['_Nand_ChannelLength'] = _Nand_ChannelLength[k]
                    _Caculation_Parameters['_Nand_POGate_ViaMxMx'] = _Nand_POGate_ViaMxMx[k]
                    _Caculation_Parameters['_Nand_XVT'] = _Nand_XVT[k]

                    _Caculation_Parameters['_Nand_NMOS_ChannelWidth'] = _Nand_NMOS_ChannelWidth[k]
                    _Caculation_Parameters['_Nand_NMOS_Source_Via_Close2POpin_TF'] = _Nand_NMOS_Source_Via_Close2POpin_TF[k]
                    _Caculation_Parameters['_Nand_NMOS_POGate_Comb_length'] = _Unit_POGate_Comb_length
                    _Caculation_Parameters['_Nand_PMOS_ChannelWidth'] = _Nand_PMOS_ChannelWidth[k]
                    _Caculation_Parameters['_Nand_PMOS_POGate_Comb_length'] = _Unit_POGate_Comb_length

                    _Caculation_Parameters['_Nand_Pbody_NumCont'] = _Unit_Pbody_NumCont
                    _Caculation_Parameters['_Nand_Pbody_XvtTop2Pbody'] = XvtTop2Pbody
                    _Caculation_Parameters['_Nand_Nbody_NumCont'] = _Unit_Nbody_NumCont
                    _Caculation_Parameters['_Nand_Nbody_Xvtdown2Nbody'] = XvtDown2Nbody
                    _Caculation_Parameters['_Nand_PMOSXvt2NMOSXvt'] = _Unit_PMOSXvt2NMOSXvt

                    ## Generate Sref: ex)self._DesignParameter['_NMOS_POWER'] = self._SrefElementDeclaration(_DesignObj=B16_nmos_power_v2._NMOS_POWER( _DesignParameter=None, _Name='{}:NMOS_POWER'.format(_Name)))[0]
                    self._DesignParameter['SRF_Nand{}'.format(i)] = self._SrefElementDeclaration(_DesignObj=Q00_02_Nand_KJH0._Nand(_DesignParameter=None, _Name='{}:SRF_Nand{}'.format(_Name, i)))[0]

                    ## Define Sref Reflection: ex)self._DesignParameter['_NMOS_POWER']['_Reflect'] = [0, 0, 0]
                    self._DesignParameter['SRF_Nand{}'.format(i)]['_Reflect'] = [0, 0, 0]

                    ## Define Sref Angle: ex)'_NMOS_POWER'
                    self._DesignParameter['SRF_Nand{}'.format(i)]['_Angle'] = 0

                    ## Calculate Sref Layer by using Calculation_Parameter: ex)'_NMOS_POWER'
                    self._DesignParameter['SRF_Nand{}'.format(i)]['_DesignObj']._CalculateDesignParameter(**_Caculation_Parameters)

                    ## Define Sref _XYcoordinate: ex)'_NMOS_POWER'
                    self._DesignParameter['SRF_Nand{}'.format(i)]['_XYCoordinates'] = [[0, 0]]

                    ## Get_Scoord_v4.
                    ## Calculate Sref XYcoord
                    tmpXY = []
                    ## initialized Sref coordinate
                    self._DesignParameter['SRF_Nand{}'.format(i)]['_XYCoordinates'] = [[0, 0]]



                    for j in range(0,BSking):
                        ## Calculate
                        if j ==0:
                            ## Target_coord: _XY_type1
                            ##X
                            tmp1_1 = self.get_param_KJH4('SRF_Nor{}'.format(i-1), 'SRF_Pullup',  'SRF_PMOS{}'.format(_Unit_Num_EachStag_input[i-1]-1), 'BND_PODummyLayer')
                            tmp1_2 = self.get_param_KJH4('SRF_Nor{}'.format(i-1), 'SRF_Pulldown','SRF_NMOS{}'.format(_Unit_Num_EachStag_input[i-1]-1), 'BND_PODummyLayer')
                            target_coordx = min(tmp1_1[-1][0][0][0][0]['_XY_left'][0], tmp1_2[-1][0][0][0][0]['_XY_left'][0])
                            ##y
                            tmp1_3 = self.get_param_KJH4('SRF_Nor{}'.format(i-1), 'SRF_Pullup', 'SRF_PMOS{}'.format(_Unit_Num_EachStag_input[i-1]-1), 'BND_{}Layer'.format(_Nor_XVT[k-1]))
                            target_coordy = tmp1_3[-1][0][0][0][0]['_XY_down'][1]

                            target_coord = [target_coordx, target_coordy]
                        else:
                            ## Target_coord: _XY_type1
                            ##X
                            tmp1_1 = self.get_param_KJH4('SRF_Nand{}'.format(i), 'SRF_Pullup', 'SRF_PMOS{}'.format(_Unit_Num_EachStag_input[i]-1), 'BND_PODummyLayer')
                            tmp1_2 = self.get_param_KJH4('SRF_Nand{}'.format(i), 'SRF_Pulldown', 'SRF_NMOS{}'.format(_Unit_Num_EachStag_input[i]-1), 'BND_PODummyLayer')
                            target_coordx = min(tmp1_1[-1][0][0][0][0]['_XY_left'][0], tmp1_2[-1][0][0][0][0]['_XY_left'][0])
                            ##y
                            tmp1_3 = self.get_param_KJH4('SRF_Nand{}'.format(i), 'SRF_Pullup', 'SRF_PMOS{}'.format(_Unit_Num_EachStag_input[i]-1), 'BND_{}Layer'.format(_Nand_XVT[k - 1]))
                            target_coordy = tmp1_3[-1][0][0][0][0]['_XY_down'][1]

                            target_coord = [target_coordx, target_coordy]

                        ## Approaching_coord: _XY_type2
                        ##X
                        tmp2_1 = self.get_param_KJH4('SRF_Nand{}'.format(i), 'SRF_Pullup',  'SRF_PMOS0', 'BND_PODummyLayer')
                        tmp2_2 = self.get_param_KJH4('SRF_Nand{}'.format(i), 'SRF_Pulldown','SRF_NMOS0', 'BND_PODummyLayer')
                        approaching_coordx = max(tmp2_1[0][0][0][-1][0]['_XY_right'][0], tmp2_2[0][0][0][-1][0]['_XY_right'][0])
                        ##Y
                        tmp2_3 = self.get_param_KJH4('SRF_Nand{}'.format(i), 'SRF_Pullup', 'SRF_PMOS0', 'BND_{}Layer'.format(_Nand_XVT[k]))
                        approaching_coordy = tmp2_3[0][0][0][0][0]['_XY_down'][1]

                        approaching_coord = [approaching_coordx, approaching_coordy]
                        ## Sref coord
                        tmp3 = self.get_param_KJH4('SRF_Nand{}'.format(i))
                        Scoord = tmp3[0][0]['_XY_origin']
                        ## Cal
                        New_Scoord = self.get_Scoord_KJH4(target_coord, approaching_coord, Scoord)
                        New_Scoord[0] = New_Scoord[0] - _GatetoGateDist
                        tmpXY.append(New_Scoord)
                        ## Define Coordinates
                        self._DesignParameter['SRF_Nand{}'.format(i)]['_XYCoordinates'] = tmpXY

            ## ########## ########## ########## ########## ########## ########## ########## ########## ########## Real_placement: Nand/Nor gen.: Nor
            else:

                k = int(i//2)
                ## Copy Calculation_Parameters from low-level-block ex)copy.deepcopy(B16_nmos_power_v2._NMOS_POWER._ParametersForDesignCalculation)
                _Caculation_Parameters = copy.deepcopy(Q01_02_Nor_KJH0._Nor._ParametersForDesignCalculation)
                ## Define Calculation_Parameters ex) _Caculation_Parameters['_NMOSPOWER_PbodyContact_1_Length']  = _NMOSPOWER_PbodyContact_1_Length
                _Caculation_Parameters['_Nor_Num_Input']                       = _Unit_Num_EachStag_input[i]

                _Caculation_Parameters['_Nor_ChannelLength']                   = _Nor_ChannelLength[k]
                _Caculation_Parameters['_Nor_POGate_ViaMxMx']                  = _Nor_POGate_ViaMxMx[k]
                _Caculation_Parameters['_Nor_XVT']                             = _Nor_XVT[k]

                _Caculation_Parameters['_Nor_NMOS_ChannelWidth']               = _Nor_NMOS_ChannelWidth[k]
                _Caculation_Parameters['_Nor_NMOS_NumberofGate']               = _Nor_NMOS_NumberofGate[k]
                _Caculation_Parameters['_Nor_NMOS_POGate_Comb_length']         = _Unit_POGate_Comb_length
                _Caculation_Parameters['_Nor_PMOS_ChannelWidth']               = _Nor_PMOS_ChannelWidth[k]
                _Caculation_Parameters['_Nor_PMOS_NumberofGate']               = _Nor_PMOS_NumberofGate[k]
                _Caculation_Parameters['_Nor_PMOS_Source_Via_Close2POpin_TF']  = _Nor_PMOS_Source_Via_Close2POpin_TF[k]
                _Caculation_Parameters['_Nor_PMOS_POGate_Comb_length']         = _Unit_POGate_Comb_length

                _Caculation_Parameters['_Nor_Pbody_NumCont']                   = _Unit_Pbody_NumCont
                _Caculation_Parameters['_Nor_Pbody_XvtTop2Pbody']              = XvtTop2Pbody
                _Caculation_Parameters['_Nor_Nbody_NumCont']                   = _Unit_Nbody_NumCont
                _Caculation_Parameters['_Nor_Nbody_Xvtdown2Nbody']             = XvtDown2Nbody
                _Caculation_Parameters['_Nor_PMOSXvt2NMOSXvt']                 = _Unit_PMOSXvt2NMOSXvt

                ## Generate Sref: ex)self._DesignParameter['_NMOS_POWER'] = self._SrefElementDeclaration(_DesignObj=B16_nmos_power_v2._NMOS_POWER( _DesignParameter=None, _Name='{}:NMOS_POWER'.format(_Name)))[0]
                self._DesignParameter['SRF_Nor{}'.format(i)] = self._SrefElementDeclaration(_DesignObj=Q01_02_Nor_KJH0._Nor(_DesignParameter=None, _Name='{}:SRF_Nor{}'.format(_Name,i)))[0]

                ## Define Sref Reflection: ex)self._DesignParameter['_NMOS_POWER']['_Reflect'] = [0, 0, 0]
                self._DesignParameter['SRF_Nor{}'.format(i)]['_Reflect'] = [0, 0, 0]

                ## Define Sref Angle: ex)'_NMOS_POWER'
                self._DesignParameter['SRF_Nor{}'.format(i)]['_Angle'] = 0

                ## Calculate Sref Layer by using Calculation_Parameter: ex)'_NMOS_POWER'
                self._DesignParameter['SRF_Nor{}'.format(i)]['_DesignObj']._CalculateDesignParameter(**_Caculation_Parameters)

                ## Define Sref _XYcoordinate: ex)'_NMOS_POWER'
                self._DesignParameter['SRF_Nor{}'.format(i)]['_XYCoordinates'] = [[0, 0]]


                ## Get_Scoord_v4.
                ## Calculate Sref XYcoord
                tmpXY = []
                ## initialized Sref coordinate
                self._DesignParameter['SRF_Nor{}'.format(i)]['_XYCoordinates'] = [[0, 0]]

                for j in range(0, BSking):
                    ## Calculate
                    if j ==0:
                        ## Target_coord: _XY_type1
                        ##X
                        tmp1_1 = self.get_param_KJH4('SRF_Nand{}'.format(i - 1), 'SRF_Pullup',   'SRF_PMOS{}'.format(_Unit_Num_EachStag_input[i-1]-1), 'BND_PODummyLayer')
                        tmp1_2 = self.get_param_KJH4('SRF_Nand{}'.format(i - 1), 'SRF_Pulldown', 'SRF_NMOS{}'.format(_Unit_Num_EachStag_input[i-1]-1), 'BND_PODummyLayer')
                        target_coordx = min(tmp1_1[-1][0][0][0][0]['_XY_left'][0], tmp1_2[-1][0][0][0][0]['_XY_left'][0])
                        ##y
                        tmp1_3 = self.get_param_KJH4('SRF_Nand{}'.format(i - 1), 'SRF_Pullup', 'SRF_PMOS{}'.format(_Unit_Num_EachStag_input[i-1]-1), 'BND_{}Layer'.format(_Nand_XVT[k]))
                        target_coordy = tmp1_3[-1][0][0][0][0]['_XY_down'][1]

                        target_coord = [target_coordx, target_coordy]
                    else:
                        ## Target_coord: _XY_type1
                        ##X
                        tmp1_1 = self.get_param_KJH4('SRF_Nor{}'.format(i), 'SRF_Pullup', 'SRF_PMOS{}'.format(_Unit_Num_EachStag_input[i]-1), 'BND_PODummyLayer')
                        tmp1_2 = self.get_param_KJH4('SRF_Nor{}'.format(i), 'SRF_Pulldown', 'SRF_NMOS{}'.format(_Unit_Num_EachStag_input[i]-1), 'BND_PODummyLayer')
                        target_coordx = min(tmp1_1[-1][0][0][0][0]['_XY_left'][0], tmp1_2[-1][0][0][0][0]['_XY_left'][0])
                        ##y
                        tmp1_3 = self.get_param_KJH4('SRF_Nor{}'.format(i), 'SRF_Pullup', 'SRF_PMOS{}'.format(_Unit_Num_EachStag_input[i]-1), 'BND_{}Layer'.format(_Nor_XVT[k]))
                        target_coordy = tmp1_3[0][0][0][0][0]['_XY_down'][1]

                        target_coord = [target_coordx, target_coordy]
                    ## Approaching_coord: _XY_type2
                    ##X
                    tmp2_1 = self.get_param_KJH4('SRF_Nor{}'.format(i), 'SRF_Pullup', 'SRF_PMOS0', 'BND_PODummyLayer')
                    tmp2_2 = self.get_param_KJH4('SRF_Nor{}'.format(i), 'SRF_Pulldown', 'SRF_NMOS0', 'BND_PODummyLayer')
                    approaching_coordx = max(tmp2_1[0][0][0][-1][0]['_XY_right'][0], tmp2_2[0][0][0][-1][0]['_XY_right'][0])
                    ##Y
                    tmp2_3 = self.get_param_KJH4('SRF_Nor{}'.format(i), 'SRF_Pullup', 'SRF_PMOS0', 'BND_{}Layer'.format(_Nor_XVT[k]))
                    approaching_coordy = tmp2_3[0][0][0][0][0]['_XY_down'][1]

                    approaching_coord = [approaching_coordx, approaching_coordy]
                    ## Sref coord
                    tmp3 = self.get_param_KJH4('SRF_Nor{}'.format(i))
                    Scoord = tmp3[0][0]['_XY_origin']
                    ## Cal
                    New_Scoord = self.get_Scoord_KJH4(target_coord, approaching_coord, Scoord)
                    New_Scoord[0] = New_Scoord[0] - _GatetoGateDist
                    tmpXY.append(New_Scoord)
                    ## Define Coordinates
                    self._DesignParameter['SRF_Nor{}'.format(i)]['_XYCoordinates'] = tmpXY


        ## ########## ########## ########## ########## ########## ########## ########## ########## ########## Real_placement: Inv
        ## Copy Calculation_Parameters from low-level-block ex)copy.deepcopy(B16_nmos_power_v2._NMOS_POWER._ParametersForDesignCalculation)
        _Caculation_Parameters = copy.deepcopy(Q03_00_Inv_KJH0._Inv._ParametersForDesignCalculation)
        ## Define Calculation_Parameters ex) _Caculation_Parameters['_NMOSPOWER_PbodyContact_1_Length']  = _NMOSPOWER_PbodyContact_1_Length
        _Caculation_Parameters['_Inv_NumberofGate']                    = _Inv_NumberofGate
        _Caculation_Parameters['_Inv_ChannelLength']                   = _Inv_ChannelLength
        _Caculation_Parameters['_Inv_XVT']                             = _Inv_XVT

        _Caculation_Parameters['_Inv_NMOS_ChannelWidth']               = _Inv_NMOS_ChannelWidth
        _Caculation_Parameters['_Inv_NMOS_POGate_Comb_length']         = _Unit_POGate_Comb_length
        _Caculation_Parameters['_Inv_NMOS_POGate_ViaMxMx']             = _Inv_NMOS_POGate_ViaMxMx

        _Caculation_Parameters['_Inv_PMOS_ChannelWidth']               = _Inv_PMOS_ChannelWidth
        _Caculation_Parameters['_Inv_PMOS_POGate_Comb_length']         = _Unit_POGate_Comb_length
        _Caculation_Parameters['_Inv_PMOS_POGate_ViaMxMx']             = _Inv_PMOS_POGate_ViaMxMx

        _Caculation_Parameters['_Inv_Pbody_NumCont']                   = _Unit_Pbody_NumCont
        _Caculation_Parameters['_Inv_Pbody_XvtTop2Pbody']              = XvtTop2Pbody
        _Caculation_Parameters['_Inv_Nbody_NumCont']                   = _Unit_Nbody_NumCont
        _Caculation_Parameters['_Inv_Nbody_Xvtdown2Nbody']             = XvtDown2Nbody
        _Caculation_Parameters['_Inv_PMOSXvt2NMOSXvt']                 = _Unit_PMOSXvt2NMOSXvt

        ## Generate Sref: ex)self._DesignParameter['_NMOS_POWER'] = self._SrefElementDeclaration(_DesignObj=B16_nmos_power_v2._NMOS_POWER( _DesignParameter=None, _Name='{}:NMOS_POWER'.format(_Name)))[0]
        self._DesignParameter['SRF_Inv'] = self._SrefElementDeclaration(_DesignObj=Q03_00_Inv_KJH0._Inv(_DesignParameter=None, _Name='{}:SRF_Inv'.format(_Name)))[0]

        ## Define Sref Reflection: ex)self._DesignParameter['_NMOS_POWER']['_Reflect'] = [0, 0, 0]
        self._DesignParameter['SRF_Inv']['_Reflect'] = [0, 0, 0]

        ## Define Sref Angle: ex)'_NMOS_POWER'
        self._DesignParameter['SRF_Inv']['_Angle'] = 0

        ## Calculate Sref Layer by using Calculation_Parameter: ex)'_NMOS_POWER'
        self._DesignParameter['SRF_Inv']['_DesignObj']._CalculateDesignParameter(**_Caculation_Parameters)

        ## Define Sref _XYcoordinate: ex)'_NMOS_POWER'
        self._DesignParameter['SRF_Inv']['_XYCoordinates'] = [[0, 0]]

        ## Get_Scoord_v4.
        ## Calculate Sref XYcoord
        tmpXY = []
        ## initialized Sref coordinate
        self._DesignParameter['SRF_Inv']['_XYCoordinates'] = [[0, 0]]
        ## Calculate
        ## Target_coord: _XY_type1
        ##X
        tmp1_1 = self.get_param_KJH4('SRF_Nand0', 'SRF_Pullup', 'SRF_PMOS0', 'BND_PODummyLayer')
        tmp1_2 = self.get_param_KJH4('SRF_Nand0', 'SRF_Pulldown', 'SRF_NMOS0', 'BND_PODummyLayer')
        target_coordx = min(tmp1_1[0][0][0][-1][0]['_XY_right'][0], tmp1_2[0][0][0][-1][0]['_XY_right'][0])
        ##y
        tmp1_3 = self.get_param_KJH4('SRF_Nand0', 'SRF_Pullup', 'SRF_PMOS0', 'BND_{}Layer'.format(_Nand_XVT[0]))
        target_coordy = tmp1_3[0][0][0][0][0]['_XY_down'][1]

        target_coord = [target_coordx, target_coordy]
        ## Approaching_coord: _XY_type2
        ##X
        tmp2_1 = self.get_param_KJH4('SRF_Inv', 'SRF_PMOS', 'BND_PODummyLayer')
        tmp2_2 = self.get_param_KJH4('SRF_Inv', 'SRF_NMOS', 'BND_PODummyLayer')
        approaching_coordx = max(tmp2_1[0][0][0][0]['_XY_left'][0], tmp2_2[0][0][0][0]['_XY_left'][0])
        ##Y
        tmp2_3 = self.get_param_KJH4('SRF_Inv', 'SRF_PMOS', 'BND_{}Layer'.format(_Inv_XVT))
        approaching_coordy = tmp2_3[0][0][0][0]['_XY_down'][1]

        approaching_coord = [approaching_coordx, approaching_coordy]
        ## Sref coord
        tmp3 = self.get_param_KJH4('SRF_Inv')
        Scoord = tmp3[0][0]['_XY_origin']
        ## Cal
        New_Scoord = self.get_Scoord_KJH4(target_coord, approaching_coord, Scoord)
        New_Scoord[0] = New_Scoord[0] + _GatetoGateDist
        tmpXY.append(New_Scoord)
        ## Define Coordinates
        self._DesignParameter['SRF_Inv']['_XYCoordinates'] = tmpXY

        ## ########## ########## ########## ########## ########## ########## ########## ########## ########## Real_placement: Xgate
        ## Copy Calculation_Parameters from low-level-block ex)copy.deepcopy(B16_nmos_power_v2._NMOS_POWER._ParametersForDesignCalculation)
        _Caculation_Parameters = copy.deepcopy(Q02_00_Xgate_KJH0._Xgate._ParametersForDesignCalculation)
        ## Define Calculation_Parameters ex) _Caculation_Parameters['_NMOSPOWER_PbodyContact_1_Length']  = _NMOSPOWER_PbodyContact_1_Length
        _Caculation_Parameters['_Xgate_NumberofGate']                    = _Xgate_NumberofGate
        _Caculation_Parameters['_Xgate_ChannelLength']                   = _Xgate_ChannelLength
        _Caculation_Parameters['_Xgate_XVT']                             = _Xgate_XVT

        _Caculation_Parameters['_Xgate_NMOS_ChannelWidth']               = _Xgate_NMOS_ChannelWidth
        _Caculation_Parameters['_Xgate_NMOS_POGate_Comb_length']         = _Unit_POGate_Comb_length
        _Caculation_Parameters['_Xgate_NMOS_POGate_ViaMxMx']             = _Xgate_NMOS_POGate_ViaMxMx

        _Caculation_Parameters['_Xgate_PMOS_ChannelWidth']               = _Xgate_PMOS_ChannelWidth
        _Caculation_Parameters['_Xgate_PMOS_POGate_Comb_length']         = _Unit_POGate_Comb_length
        _Caculation_Parameters['_Xgate_PMOS_POGate_ViaMxMx']             = _Xgate_PMOS_POGate_ViaMxMx

        _Caculation_Parameters['_Xgate_Pbody_NumCont']                   = _Unit_Pbody_NumCont
        _Caculation_Parameters['_Xgate_Pbody_XvtTop2Pbody']              = XvtTop2Pbody
        _Caculation_Parameters['_Xgate_Nbody_NumCont']                   = _Unit_Nbody_NumCont
        _Caculation_Parameters['_Xgate_Nbody_Xvtdown2Nbody']             = XvtDown2Nbody
        _Caculation_Parameters['_Xgate_PMOSXvt2NMOSXvt']                 = _Unit_PMOSXvt2NMOSXvt

        ## Generate Sref: ex)self._DesignParameter['_NMOS_POWER'] = self._SrefElementDeclaration(_DesignObj=B16_nmos_power_v2._NMOS_POWER( _DesignParameter=None, _Name='{}:NMOS_POWER'.format(_Name)))[0]
        self._DesignParameter['SRF_Xgate'] = self._SrefElementDeclaration(_DesignObj=Q02_00_Xgate_KJH0._Xgate(_DesignParameter=None, _Name='{}:SRF_Xgate'.format(_Name)))[0]

        ## Define Sref Reflection: ex)self._DesignParameter['_NMOS_POWER']['_Reflect'] = [0, 0, 0]
        self._DesignParameter['SRF_Xgate']['_Reflect'] = [0, 0, 0]

        ## Define Sref Angle: ex)'_NMOS_POWER'
        self._DesignParameter['SRF_Xgate']['_Angle'] = 0

        ## Calculate Sref Layer by using Calculation_Parameter: ex)'_NMOS_POWER'
        self._DesignParameter['SRF_Xgate']['_DesignObj']._CalculateDesignParameter(**_Caculation_Parameters)

        ## Define Sref _XYcoordinate: ex)'_NMOS_POWER'
        self._DesignParameter['SRF_Xgate']['_XYCoordinates'] = [[0, 0]]

        ## Get_Scoord_v4.
        ## Calculate Sref XYcoord
        tmpXY = []
        ## initialized Sref coordinate
        self._DesignParameter['SRF_Xgate']['_XYCoordinates'] = [[0, 0]]
        ## Calculate
        ## Target_coord: _XY_type1
        ##X
        tmp1_1 = self.get_param_KJH4('SRF_Inv', 'SRF_PMOS', 'BND_PODummyLayer')
        tmp1_2 = self.get_param_KJH4('SRF_Inv', 'SRF_NMOS', 'BND_PODummyLayer')
        target_coordx = min(tmp1_1[0][0][-1][0]['_XY_right'][0], tmp1_2[0][0][-1][0]['_XY_right'][0])
        ##y
        tmp1_3 = self.get_param_KJH4('SRF_Inv', 'SRF_PMOS', 'BND_{}Layer'.format(_Inv_XVT))
        target_coordy = tmp1_3[0][0][0][0]['_XY_down'][1]

        target_coord = [target_coordx, target_coordy]
        ## Approaching_coord: _XY_type2
        ##X
        tmp2_1 = self.get_param_KJH4('SRF_Xgate', 'SRF_PMOS', 'BND_PODummyLayer')
        tmp2_2 = self.get_param_KJH4('SRF_Xgate', 'SRF_NMOS', 'BND_PODummyLayer')
        approaching_coordx = max(tmp2_1[0][0][0][0]['_XY_left'][0], tmp2_2[0][0][0][0]['_XY_left'][0])
        ##Y
        tmp2_3 = self.get_param_KJH4('SRF_Xgate', 'SRF_PMOS', 'BND_{}Layer'.format(_Xgate_XVT))
        approaching_coordy = tmp2_3[0][0][0][0]['_XY_down'][1]

        approaching_coord = [approaching_coordx, approaching_coordy]
        ## Sref coord
        tmp3 = self.get_param_KJH4('SRF_Xgate')
        Scoord = tmp3[0][0]['_XY_origin']
        ## Cal
        New_Scoord = self.get_Scoord_KJH4(target_coord, approaching_coord, Scoord)
        New_Scoord[0] = New_Scoord[0] + _GatetoGateDist
        tmpXY.append(New_Scoord)
        ## Define Coordinates
        self._DesignParameter['SRF_Xgate']['_XYCoordinates'] = tmpXY


















        ## ########## ########## ########## ########## ########## ########## ########## ########## ########## ########## ########## ########## Body_Cover.
        ## ########## ########## ########## ########## ########## ########## ########## ########## ########## ########## ########## Body_Cover.: Nbody
        ## ########## ########## ########## ########## ########## ########## ########## ########## ########## ########## Body_Cover.: Nbody: M1_Exten
        ## Boundary_element Generation
        ## Generate Boundary_element: ex)LayerName: METAL1 / DIFF (_ODLayer) / POLY / PIMP (_PPLayer) / NWELL / SLVT LVT RVT HVT / OP(OPpress) / CONT (CA) / PCCRIT
        self._DesignParameter['BND_Nbody_M1Exten'] = self._BoundaryElementDeclaration(
            _Layer=DesignParameters._LayerMapping['METAL1'][0],
            _Datatype=DesignParameters._LayerMapping['METAL1'][1],
            _XWidth=None,
            _YWidth=None,
            _XYCoordinates=[],
        )

        ## Define Boundary_element _YWidth
        tmp1 = self.get_param_KJH4('SRF_Xgate', 'SRF_Nbody', 'SRF_NbodyContactPhyLen', 'BND_Met1Layer')
        self._DesignParameter['BND_Nbody_M1Exten']['_YWidth'] = tmp1[0][0][0][0][0]['_Ywidth']

        ## Define Boundary_element _XWidth
        tmp1 = self.get_param_KJH4('SRF_Xgate', 'SRF_Nbody', 'SRF_NbodyContactPhyLen', 'BND_Met1Layer')
        if len(_Unit_Num_EachStag_input)%2 ==0:
            SRF_name = 'SRF_Nor{}'.format(len(_Unit_Num_EachStag_input)-1)
        else:
            SRF_name = 'SRF_Nand{}'.format(len(_Unit_Num_EachStag_input)-1)
        tmp2 = self.get_param_KJH4(SRF_name, 'SRF_Nbody', 'SRF_NbodyContactPhyLen', 'BND_Met1Layer')
        self._DesignParameter['BND_Nbody_M1Exten']['_XWidth'] = abs(tmp1[0][0][0][0][0]['_XY_right'][0] - tmp2[-1][0][0][0][0]['_XY_left'][0])

        ## Define Boundary_element _XYCoordinates
        self._DesignParameter['BND_Nbody_M1Exten']['_XYCoordinates'] = [[0, 0]]

        ## Calculate Sref XYcoord
        tmpXY = []
        ## initialized Sref coordinate
        self._DesignParameter['BND_Nbody_M1Exten']['_XYCoordinates'] = [[0, 0]]
        ## Calculate
        ## Target_coord: _XY_type1
        tmp1 = self.get_param_KJH4('SRF_Xgate', 'SRF_Nbody', 'SRF_NbodyContactPhyLen', 'BND_Met1Layer')
        target_coord = tmp1[0][0][0][0][0]['_XY_down_right']
        ## Approaching_coord: _XY_type2
        tmp2 = self.get_param_KJH4('BND_Nbody_M1Exten')
        approaching_coord = tmp2[0][0]['_XY_down_right']
        ## Sref coord
        tmp3 = self.get_param_KJH4('BND_Nbody_M1Exten')
        Scoord = tmp3[0][0]['_XY_origin']
        ## Cal
        New_Scoord = self.get_Scoord_KJH4(target_coord, approaching_coord, Scoord)
        tmpXY.append(New_Scoord)
        ## Define coordinates
        self._DesignParameter['BND_Nbody_M1Exten']['_XYCoordinates'] = tmpXY
        ## ########## ########## ########## ########## ########## ########## ########## ########## ########## ########## Body_Cover.: Nbody: RX_Exten
            ## Boundary_element Generation
                ## Generate Boundary_element: ex)LayerName: METAL1 / DIFF (_ODLayer) / POLY / PIMP (_PPLayer) / NWELL / SLVT LVT RVT HVT / OP(OPpress) / CONT (CA) / PCCRIT
        self._DesignParameter['BND_Nbody_RXExten'] = self._BoundaryElementDeclaration(
        _Layer=DesignParameters._LayerMapping['DIFF'][0],
        _Datatype=DesignParameters._LayerMapping['DIFF'][1],
        _XWidth=None,
        _YWidth=None,
        _XYCoordinates=[],
        )

                ## Define Boundary_element _YWidth
        tmp1 = self.get_param_KJH4('SRF_Xgate','SRF_Nbody','SRF_NbodyContactPhyLen','BND_ODLayer')
        self._DesignParameter['BND_Nbody_RXExten']['_YWidth'] = tmp1[0][0][0][0][0]['_Ywidth']

                ## Define Boundary_element _XWidth
        tmp1 = self.get_param_KJH4('SRF_Xgate','SRF_Nbody','SRF_NbodyContactPhyLen','BND_ODLayer')
        tmp2 = self.get_param_KJH4(SRF_name,'SRF_Nbody','SRF_NbodyContactPhyLen','BND_ODLayer')

        self._DesignParameter['BND_Nbody_RXExten']['_XWidth'] = abs( tmp1[0][0][0][0][0]['_XY_right'][0]- tmp2[-1][0][0][0][0]['_XY_left'][0])

                ## Define Boundary_element _XYCoordinates
        self._DesignParameter['BND_Nbody_RXExten']['_XYCoordinates'] = [[0, 0]]

                    ## Calculate Sref XYcoord
        tmpXY = []
                        ## initialized Sref coordinate
        self._DesignParameter['BND_Nbody_RXExten']['_XYCoordinates'] = [[0, 0]]
                        ## Calculate
                            ## Target_coord: _XY_type1
        tmp1 = self.get_param_KJH4('SRF_Xgate','SRF_Nbody','SRF_NbodyContactPhyLen','BND_ODLayer')
        target_coord = tmp1[0][0][0][0][0]['_XY_down_right']
                            ## Approaching_coord: _XY_type2
        tmp2 = self.get_param_KJH4('BND_Nbody_RXExten')
        approaching_coord = tmp2[0][0]['_XY_down_right']
                            ## Sref coord
        tmp3 = self.get_param_KJH4('BND_Nbody_RXExten')
        Scoord = tmp3[0][0]['_XY_origin']
                            ## Cal
        New_Scoord = self.get_Scoord_KJH4(target_coord, approaching_coord, Scoord)
        tmpXY.append(New_Scoord)
                            ## Define coordinates
        self._DesignParameter['BND_Nbody_RXExten']['_XYCoordinates'] = tmpXY

        ## ########## ########## ########## ########## ########## ########## ########## ########## ########## ########## Body_Cover.: Nbody: Nwell_Exten
            ## Boundary_element Generation
                ## Generate Boundary_element: ex)LayerName: METAL1 / DIFF (_ODLayer) / POLY / PIMP (_PPLayer) / NWELL / SLVT LVT RVT HVT / OP(OPpress) / CONT (CA) / PCCRIT
        self._DesignParameter['BND_Nbody_NwellExten'] = self._BoundaryElementDeclaration(
        _Layer=DesignParameters._LayerMapping['NWELL'][0],
        _Datatype=DesignParameters._LayerMapping['NWELL'][1],
        _XWidth=None,
        _YWidth=None,
        _XYCoordinates=[],
        )

                ## Define Boundary_element _YWidth
        tmp1 = self.get_param_KJH4('SRF_Xgate','BND_PMOS_NellExten')
        self._DesignParameter['BND_Nbody_NwellExten']['_YWidth'] = tmp1[0][0][0]['_Ywidth']

                ## Define Boundary_element _XWidth
        tmp1 = self.get_param_KJH4('SRF_Xgate','BND_PMOS_NellExten')
        tmp2 = self.get_param_KJH4(SRF_name,'BND_PMOS_NellExten')

        self._DesignParameter['BND_Nbody_NwellExten']['_XWidth'] = abs( tmp1[0][0][0]['_XY_right'][0]- tmp2[-1][0][0]['_XY_left'][0])

                ## Define Boundary_element _XYCoordinates
        self._DesignParameter['BND_Nbody_NwellExten']['_XYCoordinates'] = [[0, 0]]

                    ## Calculate Sref XYcoord
        tmpXY = []
                        ## initialized Sref coordinate
        self._DesignParameter['BND_Nbody_NwellExten']['_XYCoordinates'] = [[0, 0]]
                        ## Calculate
                            ## Target_coord: _XY_type1
        tmp1 = self.get_param_KJH4('SRF_Xgate','BND_PMOS_NellExten')
        target_coord = tmp1[0][0][0]['_XY_down_right']
                            ## Approaching_coord: _XY_type2
        tmp2 = self.get_param_KJH4('BND_Nbody_NwellExten')
        approaching_coord = tmp2[0][0]['_XY_down_right']
                            ## Sref coord
        tmp3 = self.get_param_KJH4('BND_Nbody_NwellExten')
        Scoord = tmp3[0][0]['_XY_origin']
                            ## Cal
        New_Scoord = self.get_Scoord_KJH4(target_coord, approaching_coord, Scoord)
        tmpXY.append(New_Scoord)
                            ## Define coordinates
        self._DesignParameter['BND_Nbody_NwellExten']['_XYCoordinates'] = tmpXY

        ## ########## ########## ########## ########## ########## ########## ########## ########## ########## ########## Body_Cover.: Nbody: XVT_Exten
        _XVTLayer = 'BND_' + _Xgate_XVT + 'Layer'

            ## Boundary_element Generation
                ## Generate Boundary_element: ex)LayerName: METAL1 / DIFF (_ODLayer) / POLY / PIMP (_PPLayer) / NWELL / SLVT LVT RVT HVT / OP(OPpress) / CONT (CA) / PCCRIT
        self._DesignParameter['BND_Nbody_XvtExten'] = self._BoundaryElementDeclaration(
        _Layer=DesignParameters._LayerMapping[_Xgate_XVT][0],
        _Datatype=DesignParameters._LayerMapping[_Xgate_XVT][1],
        _XWidth=None,
        _YWidth=None,
        _XYCoordinates=[],
        )

                ## Define Boundary_element _YWidth
        self._DesignParameter['BND_Nbody_XvtExten']['_YWidth'] = PmosMaxXvtSize

                ## Define Boundary_element _XWidth
        tmp1 = self.get_param_KJH4('SRF_Xgate','SRF_PMOS',_XVTLayer)
        tmp2 = self.get_param_KJH4(SRF_name,'SRF_Pullup','SRF_PMOS{}'.format(_Unit_Num_EachStag_input[-1]-1),_XVTLayer)

        self._DesignParameter['BND_Nbody_XvtExten']['_XWidth'] = abs( tmp1[0][0][0][0]['_XY_right'][0]- tmp2[-1][0][0][0][0]['_XY_left'][0])

                ## Define Boundary_element _XYCoordinates
        self._DesignParameter['BND_Nbody_XvtExten']['_XYCoordinates'] = [[0, 0]]

                    ## Calculate Sref XYcoord
        tmpXY = []
                        ## initialized Sref coordinate
        self._DesignParameter['BND_Nbody_XvtExten']['_XYCoordinates'] = [[0, 0]]
                        ## Calculate
                            ## Target_coord: _XY_type1
        tmp1 = self.get_param_KJH4('SRF_Xgate','SRF_PMOS',_XVTLayer)
        target_coord = tmp1[0][0][0][0]['_XY_down_right']
                            ## Approaching_coord: _XY_type2
        tmp2 = self.get_param_KJH4('BND_Nbody_XvtExten')
        approaching_coord = tmp2[0][0]['_XY_down_right']
                            ## Sref coord
        tmp3 = self.get_param_KJH4('BND_Nbody_XvtExten')
        Scoord = tmp3[0][0]['_XY_origin']
                            ## Cal
        New_Scoord = self.get_Scoord_KJH4(target_coord, approaching_coord, Scoord)
        tmpXY.append(New_Scoord)
                            ## Define coordinates
        self._DesignParameter['BND_Nbody_XvtExten']['_XYCoordinates'] = tmpXY

        ## ########## ########## ########## ########## ########## ########## ########## ########## ########## ########## Body_Cover.: Nbody: Bp_Exten

            ## Boundary_element Generation
                ## Generate Boundary_element: ex)LayerName: METAL1 / DIFF (_ODLayer) / POLY / PIMP (_PPLayer) / NWELL / SLVT LVT RVT HVT / OP(OPpress) / CONT (CA) / PCCRIT
        self._DesignParameter['BND_Nbody_BpExten'] = self._BoundaryElementDeclaration(
        _Layer=DesignParameters._LayerMapping['PIMP'][0],
        _Datatype=DesignParameters._LayerMapping['PIMP'][1],
        _XWidth=None,
        _YWidth=None,
        _XYCoordinates=[],
        )

                ## Define Boundary_element _YWidth
        self._DesignParameter['BND_Nbody_BpExten']['_YWidth'] = PmosMaxXvtSize

                ## Define Boundary_element _XWidth
        tmp1 = self.get_param_KJH4('SRF_Xgate','SRF_PMOS','BND_PPLayer')
        tmp2 = self.get_param_KJH4(SRF_name,'SRF_Pullup','SRF_PMOS{}'.format(_Unit_Num_EachStag_input[-1]-1),'BND_PPLayer')

        self._DesignParameter['BND_Nbody_BpExten']['_XWidth'] = abs( tmp1[0][0][0][0]['_XY_right'][0]- tmp2[-1][0][0][0][0]['_XY_left'][0])

                ## Define Boundary_element _XYCoordinates
        self._DesignParameter['BND_Nbody_BpExten']['_XYCoordinates'] = [[0, 0]]

                    ## Calculate Sref XYcoord
        tmpXY = []
                        ## initialized Sref coordinate
        self._DesignParameter['BND_Nbody_BpExten']['_XYCoordinates'] = [[0, 0]]
                        ## Calculate
                            ## Target_coord: _XY_type1
        tmp1 = self.get_param_KJH4('SRF_Xgate','SRF_PMOS','BND_PPLayer')
        target_coord = tmp1[0][0][0][0]['_XY_down_right']
                            ## Approaching_coord: _XY_type2
        tmp2 = self.get_param_KJH4('BND_Nbody_BpExten')
        approaching_coord = tmp2[0][0]['_XY_down_right']
                            ## Sref coord
        tmp3 = self.get_param_KJH4('BND_Nbody_BpExten')
        Scoord = tmp3[0][0]['_XY_origin']
                            ## Cal
        New_Scoord = self.get_Scoord_KJH4(target_coord, approaching_coord, Scoord)
        tmpXY.append(New_Scoord)
                            ## Define coordinates
        self._DesignParameter['BND_Nbody_BpExten']['_XYCoordinates'] = tmpXY

        ## ########## ########## ########## ########## ########## ########## ########## ########## ########## ########## ########## Body_Cover.: Pbody
        ## ########## ########## ########## ########## ########## ########## ########## ########## ########## ########## Body_Cover.: Pbody: M1_Exten
            ## Boundary_element Generation
                ## Generate Boundary_element: ex)LayerName: METAL1 / DIFF (_ODLayer) / POLY / PIMP (_PPLayer) / NWELL / SLVT LVT RVT HVT / OP(OPpress) / CONT (CA) / PCCRIT
        self._DesignParameter['BND_Pbody_M1Exten'] = self._BoundaryElementDeclaration(
        _Layer=DesignParameters._LayerMapping['METAL1'][0],
        _Datatype=DesignParameters._LayerMapping['METAL1'][1],
        _XWidth=None,
        _YWidth=None,
        _XYCoordinates=[],
        )

                ## Define Boundary_element _YWidth
        tmp1 = self.get_param_KJH4('SRF_Xgate','SRF_Pbody','SRF_PbodyContactPhyLen','BND_Met1Layer')
        self._DesignParameter['BND_Pbody_M1Exten']['_YWidth'] = tmp1[0][0][0][0][0]['_Ywidth']

                ## Define Boundary_element _XWidth
        tmp1 = self.get_param_KJH4('SRF_Xgate','SRF_Pbody','SRF_PbodyContactPhyLen','BND_Met1Layer')
        tmp2 = self.get_param_KJH4(SRF_name,'SRF_Pbody','SRF_PbodyContactPhyLen','BND_Met1Layer')

        self._DesignParameter['BND_Pbody_M1Exten']['_XWidth'] = abs( tmp1[0][0][0][0][0]['_XY_right'][0]- tmp2[-1][0][0][0][0]['_XY_left'][0])

                ## Define Boundary_element _XYCoordinates
        self._DesignParameter['BND_Pbody_M1Exten']['_XYCoordinates'] = [[0, 0]]

                    ## Calculate Sref XYcoord
        tmpXY = []
                        ## initialized Sref coordinate
        self._DesignParameter['BND_Pbody_M1Exten']['_XYCoordinates'] = [[0, 0]]
                        ## Calculate
                            ## Target_coord: _XY_type1
        tmp1 = self.get_param_KJH4('SRF_Xgate','SRF_Pbody','SRF_PbodyContactPhyLen','BND_Met1Layer')
        target_coord = tmp1[0][0][0][0][0]['_XY_down_right']
                            ## Approaching_coord: _XY_type2
        tmp2 = self.get_param_KJH4('BND_Pbody_M1Exten')
        approaching_coord = tmp2[0][0]['_XY_down_right']
                            ## Sref coord
        tmp3 = self.get_param_KJH4('BND_Pbody_M1Exten')
        Scoord = tmp3[0][0]['_XY_origin']
                            ## Cal
        New_Scoord = self.get_Scoord_KJH4(target_coord, approaching_coord, Scoord)
        tmpXY.append(New_Scoord)
                            ## Define coordinates
        self._DesignParameter['BND_Pbody_M1Exten']['_XYCoordinates'] = tmpXY

        ## ########## ########## ########## ########## ########## ########## ########## ########## ########## ########## Body_Cover.: Pbody: RX_Exten
            ## Boundary_element Generation
                ## Generate Boundary_element: ex)LayerName: METAL1 / DIFF (_ODLayer) / POLY / PIMP (_PPLayer) / NWELL / SLVT LVT RVT HVT / OP(OPpress) / CONT (CA) / PCCRIT
        self._DesignParameter['BND_Pbody_RXExten'] = self._BoundaryElementDeclaration(
        _Layer=DesignParameters._LayerMapping['DIFF'][0],
        _Datatype=DesignParameters._LayerMapping['DIFF'][1],
        _XWidth=None,
        _YWidth=None,
        _XYCoordinates=[],
        )

                ## Define Boundary_element _YWidth
        tmp1 = self.get_param_KJH4('SRF_Xgate','SRF_Pbody','SRF_PbodyContactPhyLen','BND_ODLayer')
        self._DesignParameter['BND_Pbody_RXExten']['_YWidth'] = tmp1[0][0][0][0][0]['_Ywidth']

                ## Define Boundary_element _XWidth
        tmp1 = self.get_param_KJH4('SRF_Xgate','SRF_Pbody','SRF_PbodyContactPhyLen','BND_ODLayer')
        tmp2 = self.get_param_KJH4(SRF_name,'SRF_Pbody','SRF_PbodyContactPhyLen','BND_ODLayer')

        self._DesignParameter['BND_Pbody_RXExten']['_XWidth'] = abs( tmp1[0][0][0][0][0]['_XY_right'][0]- tmp2[-1][0][0][0][0]['_XY_left'][0])

                ## Define Boundary_element _XYCoordinates
        self._DesignParameter['BND_Pbody_RXExten']['_XYCoordinates'] = [[0, 0]]

                    ## Calculate Sref XYcoord
        tmpXY = []
                        ## initialized Sref coordinate
        self._DesignParameter['BND_Pbody_RXExten']['_XYCoordinates'] = [[0, 0]]
                        ## Calculate
                            ## Target_coord: _XY_type1
        tmp1 = self.get_param_KJH4('SRF_Xgate','SRF_Pbody','SRF_PbodyContactPhyLen','BND_ODLayer')
        target_coord = tmp1[0][0][0][0][0]['_XY_down_right']
                            ## Approaching_coord: _XY_type2
        tmp2 = self.get_param_KJH4('BND_Pbody_RXExten')
        approaching_coord = tmp2[0][0]['_XY_down_right']
                            ## Sref coord
        tmp3 = self.get_param_KJH4('BND_Pbody_RXExten')
        Scoord = tmp3[0][0]['_XY_origin']
                            ## Cal
        New_Scoord = self.get_Scoord_KJH4(target_coord, approaching_coord, Scoord)
        tmpXY.append(New_Scoord)
                            ## Define coordinates
        self._DesignParameter['BND_Pbody_RXExten']['_XYCoordinates'] = tmpXY

        ## ########## ########## ########## ########## ########## ########## ########## ########## ########## ########## Body_Cover.: Pbody: Bp_Exten
            ## Boundary_element Generation
                ## Generate Boundary_element: ex)LayerName: METAL1 / DIFF (_ODLayer) / POLY / PIMP (_PPLayer) / NWELL / SLVT LVT RVT HVT / OP(OPpress) / CONT (CA) / PCCRIT
        self._DesignParameter['BND_Pbody_PPExten'] = self._BoundaryElementDeclaration(
        _Layer=DesignParameters._LayerMapping['PIMP'][0],
        _Datatype=DesignParameters._LayerMapping['PIMP'][1],
        _XWidth=None,
        _YWidth=None,
        _XYCoordinates=[],
        )

                ## Define Boundary_element _YWidth
        tmp1 = self.get_param_KJH4('SRF_Xgate','SRF_Pbody','SRF_PbodyContactPhyLen','BND_PPLayer')
        self._DesignParameter['BND_Pbody_PPExten']['_YWidth'] = tmp1[0][0][0][0][0]['_Ywidth']

                ## Define Boundary_element _XWidth
        tmp1 = self.get_param_KJH4('SRF_Xgate','SRF_Pbody','SRF_PbodyContactPhyLen','BND_PPLayer')
        tmp2 = self.get_param_KJH4(SRF_name,'SRF_Pbody','SRF_PbodyContactPhyLen','BND_PPLayer')

        self._DesignParameter['BND_Pbody_PPExten']['_XWidth'] = abs( tmp1[0][0][0][0][0]['_XY_right'][0]- tmp2[-1][0][0][0][0]['_XY_left'][0])

                ## Define Boundary_element _XYCoordinates
        self._DesignParameter['BND_Pbody_PPExten']['_XYCoordinates'] = [[0, 0]]

                    ## Calculate Sref XYcoord
        tmpXY = []
                        ## initialized Sref coordinate
        self._DesignParameter['BND_Pbody_PPExten']['_XYCoordinates'] = [[0, 0]]
                        ## Calculate
                            ## Target_coord: _XY_type1
        tmp1 = self.get_param_KJH4('SRF_Xgate','SRF_Pbody','SRF_PbodyContactPhyLen','BND_PPLayer')
        target_coord = tmp1[0][0][0][0][0]['_XY_down_right']
                            ## Approaching_coord: _XY_type2
        tmp2 = self.get_param_KJH4('BND_Pbody_PPExten')
        approaching_coord = tmp2[0][0]['_XY_down_right']
                            ## Sref coord
        tmp3 = self.get_param_KJH4('BND_Pbody_PPExten')
        Scoord = tmp3[0][0]['_XY_origin']
                            ## Cal
        New_Scoord = self.get_Scoord_KJH4(target_coord, approaching_coord, Scoord)
        tmpXY.append(New_Scoord)
                            ## Define coordinates
        self._DesignParameter['BND_Pbody_PPExten']['_XYCoordinates'] = tmpXY

        ## ########## ########## ########## ########## ########## ########## ########## ########## ########## ########## Body_Cover.: Pbody: XVT_Exten
        _XVTLayer = 'BND_' + _Xgate_XVT + 'Layer'

            ## Boundary_element Generation
                ## Generate Boundary_element: ex)LayerName: METAL1 / DIFF (_ODLayer) / POLY / PIMP (_PPLayer) / NWELL / SLVT LVT RVT HVT / OP(OPpress) / CONT (CA) / PCCRIT
        self._DesignParameter['BND_Pbody_XvtExten'] = self._BoundaryElementDeclaration(
        _Layer=DesignParameters._LayerMapping[_Xgate_XVT][0],
        _Datatype=DesignParameters._LayerMapping[_Xgate_XVT][1],
        _XWidth=None,
        _YWidth=None,
        _XYCoordinates=[],
        )

                ## Define Boundary_element _YWidth
        self._DesignParameter['BND_Pbody_XvtExten']['_YWidth'] = NmosMaxXvtSize

                ## Define Boundary_element _XWidth
        tmp1 = self.get_param_KJH4('SRF_Xgate','SRF_NMOS',_XVTLayer)
        tmp2 = self.get_param_KJH4(SRF_name,'SRF_Pulldown','SRF_NMOS{}'.format(_Unit_Num_EachStag_input[-1]-1),_XVTLayer)

        self._DesignParameter['BND_Pbody_XvtExten']['_XWidth'] = abs( tmp1[0][0][0][0]['_XY_right'][0]- tmp2[-1][0][0][0][0]['_XY_left'][0])

                ## Define Boundary_element _XYCoordinates
        self._DesignParameter['BND_Pbody_XvtExten']['_XYCoordinates'] = [[0, 0]]

                    ## Calculate Sref XYcoord
        tmpXY = []
                        ## initialized Sref coordinate
        self._DesignParameter['BND_Pbody_XvtExten']['_XYCoordinates'] = [[0, 0]]
                        ## Calculate
                            ## Target_coord: _XY_type1
        tmp1 = self.get_param_KJH4('SRF_Xgate','SRF_NMOS',_XVTLayer)
        target_coord = tmp1[0][0][0][0]['_XY_up_right']
                            ## Approaching_coord: _XY_type2
        tmp2 = self.get_param_KJH4('BND_Pbody_XvtExten')
        approaching_coord = tmp2[0][0]['_XY_up_right']
                            ## Sref coord
        tmp3 = self.get_param_KJH4('BND_Pbody_XvtExten')
        Scoord = tmp3[0][0]['_XY_origin']
                            ## Cal
        New_Scoord = self.get_Scoord_KJH4(target_coord, approaching_coord, Scoord)
        tmpXY.append(New_Scoord)
                            ## Define coordinates
        self._DesignParameter['BND_Pbody_XvtExten']['_XYCoordinates'] = tmpXY



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
    libname = 'Proj_ZZ01_Q04_00_Placement'
    ## CellName: ex)C01_cap_array_v2_84
    cellname = 'Q04_00_Placement_v1'
    _fileName = cellname + '.gds'

    ''' Input Parameters for Layout Object '''
    InputParams = dict(

    # Unit
        _GatetoGateDist = 100,

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
            _Nand_XVT               = ['SLVT','SLVT'],  # 'XVT' ex)SLVT/LVT/RVT/HVT
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
            _Nor_XVT	            = ['SLVT','SLVT'],   # 'XVT' ex)SLVT/LVT/RVT/HVT
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
        _Inv_XVT            ='SLVT',

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
        _Xgate_XVT              ='SLVT',

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
    LayoutObj = _Placement(_DesignParameter=None, _Name=cellname)
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
