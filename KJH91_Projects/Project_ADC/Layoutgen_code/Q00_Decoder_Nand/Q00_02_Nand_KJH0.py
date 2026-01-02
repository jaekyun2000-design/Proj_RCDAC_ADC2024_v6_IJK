from KJH91_Projects.Project_ADC.Library_and_Engine import StickDiagram_KJH1
from KJH91_Projects.Project_ADC.Library_and_Engine import DesignParameters
from KJH91_Projects.Project_ADC.Library_and_Engine import DRC

import numpy as np
import copy
import time
import math
# from SthPack import CoordCalc

from KJH91_Projects.Project_ADC.Layoutgen_code.A_Basic_Building_Block import A02_ViaStack_KJH3
from KJH91_Projects.Project_ADC.Layoutgen_code.A_Basic_Building_Block import A15_PolyRes_KJH2
from KJH91_Projects.Project_ADC.Layoutgen_code.A_Basic_Building_Block import A09_NbodyRing_KJH3
from KJH91_Projects.Project_ADC.Layoutgen_code.A_Basic_Building_Block import A10_PbodyRing_KJH3
from KJH91_Projects.Project_ADC.Layoutgen_code.A_Basic_Building_Block import A14_Mosfet_KJH3
from KJH91_Projects.Project_ADC.Layoutgen_code.A_Basic_Building_Block import A08_PbodyContactPhyLen_KJH3
from KJH91_Projects.Project_ADC.Layoutgen_code.A_Basic_Building_Block import A07_NbodyContactPhyLen_KJH3


from KJH91_Projects.Project_ADC.Layoutgen_code.Q00_Decoder_Nand import Q00_00_Pulldown_KJH0
from KJH91_Projects.Project_ADC.Layoutgen_code.Q00_Decoder_Nand import Q00_01_Pullup_KJH0


## ########################################################################################################################################################## Class_HEADER
class _Nand(StickDiagram_KJH1._StickDiagram_KJH):
    ## Define input_parameters for Design calculation
    _ParametersForDesignCalculation = dict(

        # Num of Input
        _Nand_Num_Input=4,  # Number>2

        # MOSFET
        # Common
        _Nand_NumberofGate=2,  # Number
        _Nand_ChannelLength	= 30,       # Number
        _Nand_POGate_ViaMxMx    = [0, 1],  # Ex) [1,5] -> ViaM1M5
        _Nand_XVT				= 'SLVT'  ,   # 'XVT' ex)SLVT/LVT/RVT/HVT

        # Pulldown(NMOS)
        # Physical dimension
        _Nand_NMOS_ChannelWidth	            = 800,      # Number
        # Source_node setting
        _Nand_NMOS_Source_Via_Close2POpin_TF  = False,    # True/False --> First MOS
        # Poly Gate setting
        # Poly Gate setting : vertical length
        _Nand_NMOS_POGate_Comb_length         = None,      # None/Number

        # Pulldown(PMOS)
        # Physical dimension
        _Nand_PMOS_ChannelWidth	            = 400,      # Number
        # Poly Gate setting
        # Poly Gate setting : vertical length
        _Nand_PMOS_POGate_Comb_length         = None,      # None/Number

        # Power Rail
        # Pbody_Pulldown(NMOS)
        _Nand_Pbody_NumCont=3,  # Number
        _Nand_Pbody_XvtTop2Pbody=None,  # Number/None(Minimum)
        # Nbody_Pullup(PMOS)
        _Nand_Nbody_NumCont=2,  # Number
        _Nand_Nbody_Xvtdown2Nbody=None,  # Number/None(Minimum)

        # PMOS and NMOS Height
        _Nand_PMOSXvt2NMOSXvt=1000,  # number

    )

    ## Initially Defined design_parameter
    def __init__(self, _DesignParameter=None, _Name=None):
        if _DesignParameter != None:
            self._DesignParameter = _DesignParameter
        else:
            self._DesignParameter = dict(
                _Name=self._NameDeclaration(_Name=_Name),
                _GDSFile=self._GDSObjDeclaration(_GDSFile=None), _XYcoordAsCent=dict(_XYcoordAsCent=0),
            )

    ## ################################################################################################################################################ _CalculateDesignParameter
    def _CalculateDesignParameter(self,

                                  # Num of Input
                                  _Nand_Num_Input=6,  # Number>2

                                  # MOSFET
                                  # Common
                                  _Nand_NumberofGate=2,  # Number
                                  _Nand_ChannelLength	= 30,       # Number
                                  _Nand_POGate_ViaMxMx    = [0, 1],  # Ex) [1,5] -> ViaM1M5
                                  _Nand_XVT				= 'SLVT'  ,   # 'XVT' ex)SLVT/LVT/RVT/HVT

                                  # Pulldown(NMOS)
                                  # Physical dimension
                                  _Nand_NMOS_ChannelWidth	            = 350,      # Number
                                  # Source_node setting
                                  _Nand_NMOS_Source_Via_Close2POpin_TF  = False,    # True/False --> First MOS
                                  # Poly Gate setting
                                  # Poly Gate setting : vertical length
                                  _Nand_NMOS_POGate_Comb_length         = None,      # None/Number

                                  # Pulldown(PMOS)
                                  # Physical dimension
                                  _Nand_PMOS_ChannelWidth	            = 350,      # Number
                                  # Poly Gate setting
                                  # Poly Gate setting : vertical length
                                  _Nand_PMOS_POGate_Comb_length         = None,      # None/Number

                                  # Power Rail
                                  # Pbody_Pulldown(NMOS)
                                  _Nand_Pbody_NumCont=3,  # Number
                                  _Nand_Pbody_XvtTop2Pbody=None,  # Number/None(Minimum)
                                  # Nbody_Pullup(PMOS)
                                  _Nand_Nbody_NumCont=2,  # Number
                                  _Nand_Nbody_Xvtdown2Nbody=None,  # Number/None(Minimum)

                                  # PMOS and NMOS Height
                                  _Nand_PMOSXvt2NMOSXvt=1000,  # number

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


        ## ########## ########## ########## ########## ########## ########## ########## ########## ########## ########## ########## ########## Pulldown
        ## ########## ########## ########## ########## ########## ########## ########## ########## ########## ########## ########## Pulldown: SRF_Pulldown gen.

        ## Copy Calculation_Parameters from low-level-block ex)copy.deepcopy(B16_nmos_power_v2._NMOS_POWER._ParametersForDesignCalculation)
        _Caculation_Parameters = copy.deepcopy(Q00_00_Pulldown_KJH0._Pulldown._ParametersForDesignCalculation)
        ## Define Calculation_Parameters ex) _Caculation_Parameters['_NMOSPOWER_PbodyContact_1_Length']  = _NMOSPOWER_PbodyContact_1_Length
        _Caculation_Parameters['_Num_Input'] = _Nand_Num_Input

        _Caculation_Parameters['_NMOS_MosType'] = 'NMOS'
        _Caculation_Parameters['_NMOS_MosUpDn'] = 'Up'

        _Caculation_Parameters['_NMOS_NumberofGate'] = _Nand_NumberofGate
        _Caculation_Parameters['_NMOS_ChannelWidth'] = _Nand_NMOS_ChannelWidth
        _Caculation_Parameters['_NMOS_ChannelLength'] = _Nand_ChannelLength
        _Caculation_Parameters['_NMOS_GateSpacing'] = None
        _Caculation_Parameters['_NMOS_SDWidth'] = None
        _Caculation_Parameters['_NMOS_XVT'] = _Nand_XVT
        _Caculation_Parameters['_NMOS_PCCrit'] = True

        _Caculation_Parameters['_NMOS_Source_Via_TF'] = True
        _Caculation_Parameters['_NMOS_Source_Via_Close2POpin_TF'] = _Nand_NMOS_Source_Via_Close2POpin_TF
        _Caculation_Parameters['_NMOS_Source_Comb_TF'] = True
        _Caculation_Parameters['_NMOS_Source_Comb_POpinward_TF'] = False
        _Caculation_Parameters['_NMOS_Source_Comb_Length'] = None

        _Caculation_Parameters['_NMOS_Drain_Via_TF'] = True
        _Caculation_Parameters['_NMOS_Drain_Via_Close2POpin_TF'] = True
        _Caculation_Parameters['_NMOS_Drain_Comb_TF'] = True
        _Caculation_Parameters['_NMOS_Drain_Comb_POpinward_TF'] = True
        _Caculation_Parameters['_NMOS_Drain_Comb_Length'] = None

        _Caculation_Parameters['_NMOS_PODummy_TF'] = True
        _Caculation_Parameters['_NMOS_PODummy_Length'] = None
        _Caculation_Parameters['_NMOS_PODummy_Placement'] = None

        _Caculation_Parameters['_NMOS_Xvt_MinExten_TF'] = True
        _Caculation_Parameters['_NMOS_Xvt_Placement'] = 'Dn'

        _Caculation_Parameters['_NMOS_POGate_Comb_TF'] = True
        _Caculation_Parameters['_NMOS_POGate_Comb_length'] = _Nand_NMOS_POGate_Comb_length
        _Caculation_Parameters['_NMOS_POGate_Via_TF'] = True
        _Caculation_Parameters['_NMOS_POGate_ViaMxMx'] = _Nand_POGate_ViaMxMx

        ## Generate Sref: ex)self._DesignParameter['_NMOS_POWER'] = self._SrefElementDeclaration(_DesignObj=B16_nmos_power_v2._NMOS_POWER( _DesignParameter=None, _Name='{}:NMOS_POWER'.format(_Name)))[0]
        self._DesignParameter['SRF_Pulldown'] = self._SrefElementDeclaration(_DesignObj=Q00_00_Pulldown_KJH0._Pulldown(_DesignParameter=None, _Name='{}:SRF_Pulldown'.format(_Name)))[0]

        ## Define Sref Reflection: ex)self._DesignParameter['_NMOS_POWER']['_Reflect'] = [0, 0, 0]
        self._DesignParameter['SRF_Pulldown']['_Reflect'] = [0, 0, 0]

        ## Define Sref Angle: ex)'_NMOS_POWER'
        self._DesignParameter['SRF_Pulldown']['_Angle'] = 0

        ## Calculate Sref Layer by using Calculation_Parameter: ex)'_NMOS_POWER'
        self._DesignParameter['SRF_Pulldown']['_DesignObj']._CalculateDesignParameter(**_Caculation_Parameters)

        ## Define Sref _XYcoordinate: ex)'_NMOS_POWER'
        self._DesignParameter['SRF_Pulldown']['_XYCoordinates'] = [[0, 0]]

        ## ########## ########## ########## ########## ########## ########## ########## ########## ########## ########## ########## Pulldown: Pbody
        ## Copy Calculation_Parameters from low-level-block ex)copy.deepcopy(B16_nmos_power_v2._NMOS_POWER._ParametersForDesignCalculation)
        _Caculation_Parameters = copy.deepcopy(A08_PbodyContactPhyLen_KJH3._PbodyContactPhyLen._ParametersForDesignCalculation)
        ## Define Calculation_Parameters ex) _Caculation_Parameters['_NMOSPOWER_PbodyContact_1_Length']  = _NMOSPOWER_PbodyContact_1_Length
        _Caculation_Parameters['_Length'] = None
        _Caculation_Parameters['_NumCont'] = _Nand_Pbody_NumCont
        _Caculation_Parameters['_Vtc_flag'] = False

        ## Calculate '_Length'
        tmp = self.get_outter_KJH4('SRF_Pulldown')
        _Caculation_Parameters['_Length'] = abs(tmp['_Mostright']['coord'][0] - tmp['_Mostleft']['coord'][0])

        ## Generate Sref: ex)self._DesignParameter['_NMOS_POWER'] = self._SrefElementDeclaration(_DesignObj=B16_nmos_power_v2._NMOS_POWER( _DesignParameter=None, _Name='{}:NMOS_POWER'.format(_Name)))[0]
        self._DesignParameter['SRF_Pbody'] = self._SrefElementDeclaration(_DesignObj=A08_PbodyContactPhyLen_KJH3._PbodyContactPhyLen(_DesignParameter=None, _Name='{}:SRF_Pbody'.format(_Name)))[0]

        ## Define Sref Reflection: ex)self._DesignParameter['_NMOS_POWER']['_Reflect'] = [0, 0, 0]
        self._DesignParameter['SRF_Pbody']['_Reflect'] = [0, 0, 0]

        ## Define Sref Angle: ex)'_NMOS_POWER'
        self._DesignParameter['SRF_Pbody']['_Angle'] = 0

        ## Calculate Sref Layer by using Calculation_Parameter: ex)'_NMOS_POWER'
        self._DesignParameter['SRF_Pbody']['_DesignObj']._CalculateDesignParameter(**_Caculation_Parameters)

        ## Define Sref _XYcoordinate: ex)'_NMOS_POWER'
        self._DesignParameter['SRF_Pbody']['_XYCoordinates'] = [[0, 0]]

        ## Get_Scoord_v4.
        ## Calculate Sref XYcoord
        tmpXY = []
        ## initialized Sref coordinate
        self._DesignParameter['SRF_Pbody']['_XYCoordinates'] = [[0, 0]]

        if _Nand_Pbody_XvtTop2Pbody == None:
            ## Calculate
            ## Target_coord: _XY_type1
            ## X
            tmp1_1 = self.get_outter_KJH4('SRF_Pulldown')
            target_coordx = np.round(0.5 * (tmp1_1['_Mostright']['coord'][0] + tmp1_1['_Mostleft']['coord'][0]))
            ## Y
            target_coordy = tmp1_1['_Mostdown']['coord'][0]

            target_coord = [target_coordx, target_coordy]
            ## Approaching_coord: _XY_type2
            tmp2 = self.get_param_KJH4('SRF_Pbody', 'SRF_PbodyContactPhyLen', 'BND_Met1Layer')
            approaching_coord = tmp2[0][0][0][0]['_XY_up']
            ## Sref coord
            tmp3 = self.get_param_KJH4('SRF_Pbody')
            Scoord = tmp3[0][0]['_XY_origin']
            ## Cal
            New_Scoord = self.get_Scoord_KJH4(target_coord, approaching_coord, Scoord)
            New_Scoord[1] = New_Scoord[1] - 50
            tmpXY.append(New_Scoord)
            ## Define Coordinates
            self._DesignParameter['SRF_Pbody']['_XYCoordinates'] = tmpXY

        else:
            ## Calculate
            ## Target_coord: _XY_type1
            # X
            tmp1_1 = self.get_outter_KJH4('SRF_Pulldown')
            target_coordx = np.round(0.5 * (tmp1_1['_Mostright']['coord'][0] + tmp1_1['_Mostleft']['coord'][0]))
            # Y
            tmp1_2 = self.get_param_KJH4('SRF_Pulldown', 'SRF_NMOS0', 'BND_{}Layer'.format(_Nand_XVT))
            target_coordy = tmp1_2[0][0][0][0]['_XY_up'][1]

            target_coord = [target_coordx, target_coordy]

            ## Approaching_coord: _XY_type2
            tmp2 = self.get_param_KJH4('SRF_Pbody', 'SRF_PbodyContactPhyLen', 'BND_Met1Layer')
            approaching_coord = tmp2[0][0][0][0]['_XY_up']
            ## Sref coord
            tmp3 = self.get_param_KJH4('SRF_Pbody')
            Scoord = tmp3[0][0]['_XY_origin']
            ## Cal
            New_Scoord = self.get_Scoord_KJH4(target_coord, approaching_coord, Scoord)
            New_Scoord[1] = New_Scoord[1] - _Nand_Pbody_XvtTop2Pbody
            tmpXY.append(New_Scoord)
            ## Define Coordinates
            self._DesignParameter['SRF_Pbody']['_XYCoordinates'] = tmpXY

        ## ########## ########## ########## ########## ########## ########## ########## ########## ########## ########## ########## Pulldown: Pbody, NMOS(-1)Source Vtc M1 conn
        ## Boundary_element Generation
        ## Generate Boundary_element: ex)LayerName: METAL1 / DIFF (_ODLayer) / POLY / PIMP (_PPLayer) / NWELL / SLVT LVT RVT HVT / OP(OPpress) / CONT (CA) / PCCRIT
        self._DesignParameter['BND_Nmos_Source_Vtc_M1'] = self._BoundaryElementDeclaration(
            _Layer=DesignParameters._LayerMapping['METAL1'][0],
            _Datatype=DesignParameters._LayerMapping['METAL1'][1],
            _XWidth=None,
            _YWidth=None,
            _XYCoordinates=[],
        )

        ## Define Boundary_element _YWidth
        tmp1 = self.get_param_KJH4('SRF_Pulldown', 'SRF_NMOS0', 'BND_Source_M1')
        tmp2 = self.get_param_KJH4('SRF_Pbody', 'SRF_PbodyContactPhyLen', 'BND_Met1Layer')
        self._DesignParameter['BND_Nmos_Source_Vtc_M1']['_YWidth'] = abs( tmp1[0][0][0][0]['_XY_up'][1] - tmp2[0][0][0][0]['_XY_down'][1])

        ## Define Boundary_element _XWidth
        tmp = self.get_param_KJH4('SRF_Pulldown', 'SRF_NMOS0', 'BND_Source_M1')
        self._DesignParameter['BND_Nmos_Source_Vtc_M1']['_XWidth'] = tmp[0][0][0][0]['_Xwidth']

        ## Define Boundary_element _XYCoordinates
        self._DesignParameter['BND_Nmos_Source_Vtc_M1']['_XYCoordinates'] = [[0, 0]]

        ## Calculate Sref XYcoord
        tmpXY = []
        tmp = self.get_param_KJH4('SRF_Pulldown', 'SRF_NMOS0', 'BND_Source_M1')
        for i in range(0, len(tmp[0][0])):
            ## Calculate Sref XYcoord
            ## Calculate
            ## Target_coord: _XY_type1
            tmp1 = self.get_param_KJH4('SRF_Pulldown', 'SRF_NMOS{}'.format(_Nand_Num_Input-1), 'BND_Source_M1')
            target_coord = tmp1[0][0][i][0]['_XY_up_left']
            ## Approaching_coord: _XY_type2
            tmp2 = self.get_param_KJH4('BND_Nmos_Source_Vtc_M1')
            approaching_coord = tmp2[0][0]['_XY_up_left']
            ## Sref coord
            tmp3 = self.get_param_KJH4('BND_Nmos_Source_Vtc_M1')
            Scoord = tmp3[0][0]['_XY_origin']
            ## Cal
            New_Scoord = self.get_Scoord_KJH4(target_coord, approaching_coord, Scoord)
            tmpXY.append(New_Scoord)
        ## Define coordinates
        self._DesignParameter['BND_Nmos_Source_Vtc_M1']['_XYCoordinates'] = tmpXY



        ## ########## ########## ########## ########## ########## ########## ########## ########## ########## ########## ########## ########## Pullup
        ## ########## ########## ########## ########## ########## ########## ########## ########## ########## ########## ########## Pullup: SRF_Pullup
        ## Copy Calculation_Parameters from low-level-block ex)copy.deepcopy(B16_nmos_power_v2._PMOS_POWER._ParametersForDesignCalculation)
        _Caculation_Parameters = copy.deepcopy(Q00_01_Pullup_KJH0._Pullup._ParametersForDesignCalculation)
        ## Define Calculation_Parameters ex) _Caculation_Parameters['_PMOSPOWER_PbodyContact_1_Length']  = _PMOSPOWER_PbodyContact_1_Length
        _Caculation_Parameters['_Num_Input'] = _Nand_Num_Input

        _Caculation_Parameters['_PMOS_MosType'] = 'PMOS'
        _Caculation_Parameters['_PMOS_MosUpDn'] = 'Dn'

        _Caculation_Parameters['_PMOS_NumberofGate'] = _Nand_NumberofGate
        _Caculation_Parameters['_PMOS_ChannelWidth'] = _Nand_PMOS_ChannelWidth
        _Caculation_Parameters['_PMOS_ChannelLength'] = _Nand_ChannelLength
        _Caculation_Parameters['_PMOS_GateSpacing'] = None
        _Caculation_Parameters['_PMOS_SDWidth'] = None
        _Caculation_Parameters['_PMOS_XVT'] = _Nand_XVT
        _Caculation_Parameters['_PMOS_PCCrit'] = True

        _Caculation_Parameters['_PMOS_Source_Via_TF'] = False
        _Caculation_Parameters['_PMOS_Source_Via_Close2POpin_TF'] = False
        _Caculation_Parameters['_PMOS_Source_Comb_TF'] = True
        _Caculation_Parameters['_PMOS_Source_Comb_POpinward_TF'] = False
        _Caculation_Parameters['_PMOS_Source_Comb_Length'] = None

        _Caculation_Parameters['_PMOS_Drain_Via_TF'] = True
        _Caculation_Parameters['_PMOS_Drain_Via_Close2POpin_TF'] = True
        _Caculation_Parameters['_PMOS_Drain_Comb_TF'] = True
        _Caculation_Parameters['_PMOS_Drain_Comb_POpinward_TF'] = True
        _Caculation_Parameters['_PMOS_Drain_Comb_Length'] = None

        _Caculation_Parameters['_PMOS_PODummy_TF'] = True
        _Caculation_Parameters['_PMOS_PODummy_Length'] = None
        _Caculation_Parameters['_PMOS_PODummy_Placement'] = None

        _Caculation_Parameters['_PMOS_Xvt_MinExten_TF'] = True
        _Caculation_Parameters['_PMOS_Xvt_Placement'] = 'Up'

        _Caculation_Parameters['_PMOS_POGate_Comb_TF'] = True
        _Caculation_Parameters['_PMOS_POGate_Comb_length'] = _Nand_NMOS_POGate_Comb_length
        _Caculation_Parameters['_PMOS_POGate_Via_TF'] = True
        _Caculation_Parameters['_PMOS_POGate_ViaMxMx'] = _Nand_POGate_ViaMxMx

        ## Generate Sref: ex)self._DesignParameter['_PMOS_POWER'] = self._SrefElementDeclaration(_DesignObj=B16_nmos_power_v2._PMOS_POWER( _DesignParameter=None, _Name='{}:NMOS_POWER'.format(_Name)))[0]
        self._DesignParameter['SRF_Pullup'] = self._SrefElementDeclaration(_DesignObj=Q00_01_Pullup_KJH0._Pullup(_DesignParameter=None, _Name='{}:SRF_Pullup'.format(_Name)))[0]

        ## Define Sref Reflection: ex)self._DesignParameter['_PMOS_POWER']['_Reflect'] = [0, 0, 0]
        self._DesignParameter['SRF_Pullup']['_Reflect'] = [0, 0, 0]

        ## Define Sref Angle: ex)'_PMOS_POWER'
        self._DesignParameter['SRF_Pullup']['_Angle'] = 0

        ## Calculate Sref Layer by using Calculation_Parameter: ex)'_PMOS_POWER'
        self._DesignParameter['SRF_Pullup']['_DesignObj']._CalculateDesignParameter(**_Caculation_Parameters)

        ## Define Sref _XYcoordinate: ex)'_PMOS_POWER'
        self._DesignParameter['SRF_Pullup']['_XYCoordinates'] = [[0, 0]]

              ## Get_Scoord_v4.
                    ## Calculate Sref XYcoord
        tmpXY = []
                        ## initialized Sref coordinate
        self._DesignParameter['SRF_Pullup']['_XYCoordinates'] = [[0, 0]]
                        ## Calculate
                            ## Target_coord: _XY_type1
                                ## X
        tmp1_1 = self.get_outter_KJH4('SRF_Pulldown')
        target_coordx = np.round(0.5*(tmp1_1['_Mostright']['coord'][0] + tmp1_1['_Mostleft']['coord'][0]))
                                ## Y
        tmp1_2 = self.get_param_KJH4('SRF_Pulldown','SRF_NMOS0','BND_{}Layer'.format(_Nand_XVT))
        target_coordy = tmp1_2[0][0][0][0]['_XY_up'][1]

        target_coord = [target_coordx,target_coordy]
                            ## Approaching_coord: _XY_type2
                                ## X
        tmp2_1 = self.get_outter_KJH4('SRF_Pullup')
        approaching_coordx = np.round (0.5*(tmp2_1['_Mostright']['coord'][0] + tmp2_1['_Mostleft']['coord'][0]))
                                ## Y
        tmp2 = self.get_param_KJH4('SRF_Pullup','SRF_PMOS0','BND_{}Layer'.format(_Nand_XVT))
        approaching_coordy = tmp2[0][0][0][0]['_XY_down'][1]

        approaching_coord = [approaching_coordx,approaching_coordy]
                            ## Sref coord
        tmp3 = self.get_param_KJH4('SRF_Pullup')
        Scoord = tmp3[0][0]['_XY_origin']
                            ## Cal
        New_Scoord = self.get_Scoord_KJH4(target_coord, approaching_coord, Scoord)
        New_Scoord[1] = New_Scoord[1] + _Nand_PMOSXvt2NMOSXvt
        tmpXY.append(New_Scoord)
                    ## Define Coordinates
        self._DesignParameter['SRF_Pullup']['_XYCoordinates'] = tmpXY


        ## ########## ########## ########## ########## ########## ########## ########## ########## ########## ########## ########## Pullup: Nbody
        ## ########## ########## ########## ########## ########## ########## ########## ########## ########## ########## Pullup: Nbody: Gen.
        ## Copy Calculation_Parameters from low-level-block ex)copy.deepcopy(B16_nmos_power_v2._NMOS_POWER._ParametersForDesignCalculation)
        _Caculation_Parameters = copy.deepcopy(A07_NbodyContactPhyLen_KJH3._NbodyContactPhyLen._ParametersForDesignCalculation)
        ## Define Calculation_Parameters ex) _Caculation_Parameters['_NMOSPOWER_PbodyContact_1_Length']  = _NMOSPOWER_PbodyContact_1_Length
        _Caculation_Parameters['_Length'] = None
        _Caculation_Parameters['_NumCont'] = _Nand_Nbody_NumCont
        _Caculation_Parameters['_Vtc_flag'] = False

        ## Calculate '_Length'
        tmp = self.get_outter_KJH4('SRF_Pullup')
        _Caculation_Parameters['_Length'] = abs(tmp['_Mostright']['coord'][0] - tmp['_Mostleft']['coord'][0])

        ## Generate Sref: ex)self._DesignParameter['_NMOS_POWER'] = self._SrefElementDeclaration(_DesignObj=B16_nmos_power_v2._NMOS_POWER( _DesignParameter=None, _Name='{}:NMOS_POWER'.format(_Name)))[0]
        self._DesignParameter['SRF_Nbody'] = self._SrefElementDeclaration(_DesignObj=A07_NbodyContactPhyLen_KJH3._NbodyContactPhyLen(_DesignParameter=None,_Name='{}:SRF_Nbody'.format(_Name)))[0]

        ## Define Sref Reflection: ex)self._DesignParameter['_NMOS_POWER']['_Reflect'] = [0, 0, 0]
        self._DesignParameter['SRF_Nbody']['_Reflect'] = [0, 0, 0]

        ## Define Sref Angle: ex)'_NMOS_POWER'
        self._DesignParameter['SRF_Nbody']['_Angle'] = 0

        ## Calculate Sref Layer by using Calculation_Parameter: ex)'_NMOS_POWER'
        self._DesignParameter['SRF_Nbody']['_DesignObj']._CalculateDesignParameter(**_Caculation_Parameters)

        ## Define Sref _XYcoordinate: ex)'_NMOS_POWER'
        self._DesignParameter['SRF_Nbody']['_XYCoordinates'] = [[0, 0]]

        ## Get_Scoord_v4.
        ## Calculate Sref XYcoord
        tmpXY = []
        ## initialized Sref coordinate
        self._DesignParameter['SRF_Nbody']['_XYCoordinates'] = [[0, 0]]

        if _Nand_Nbody_Xvtdown2Nbody == None:
            ## Calculate
            ## Target_coord: _XY_type1
            ## X
            tmp1_1 = self.get_outter_KJH4('SRF_Pullup')
            target_coordx = np.round( 0.5 * (tmp1_1['_Mostright']['coord'][0] + tmp1_1['_Mostleft']['coord'][0]) )
            ## Y
            target_coordy = tmp1_1['_Mostup']['coord'][0]

            target_coord = [target_coordx, target_coordy]
            ## Approaching_coord: _XY_type2
            tmp2 = self.get_param_KJH4('SRF_Nbody', 'SRF_NbodyContactPhyLen', 'BND_Met1Layer')
            approaching_coord = tmp2[0][0][0][0]['_XY_down']
            ## Sref coord
            tmp3 = self.get_param_KJH4('SRF_Nbody')
            Scoord = tmp3[0][0]['_XY_origin']
            ## Cal
            New_Scoord = self.get_Scoord_KJH4(target_coord, approaching_coord, Scoord)
            New_Scoord[1] = New_Scoord[1] + 50
            tmpXY.append(New_Scoord)
            ## Define Coordinates
            self._DesignParameter['SRF_Nbody']['_XYCoordinates'] = tmpXY

        else:
            ## Calculate
                ## Target_coord: _XY_type1
                    ##x
            tmp1_1 = self.get_outter_KJH4('SRF_Pullup')
            target_coordx = np.round( 0.5 * (tmp1_1['_Mostright']['coord'][0] + tmp1_1['_Mostleft']['coord'][0]) )
                    ##y
            tmp1 = self.get_param_KJH4('SRF_Pullup', 'SRF_PMOS0', 'BND_{}Layer'.format(_Nand_XVT))
            target_coordy = tmp1[0][0][0][0]['_XY_down'][1]
            target_coord = [target_coordx,target_coordy]

                ## Approaching_coord: _XY_type2
            tmp2 = self.get_param_KJH4('SRF_Nbody', 'SRF_NbodyContactPhyLen', 'BND_Met1Layer')
            approaching_coord = tmp2[0][0][0][0]['_XY_down']
                ## Sref coord
            tmp3 = self.get_param_KJH4('SRF_Nbody')
            Scoord = tmp3[0][0]['_XY_origin']
                ## Cal
            New_Scoord = self.get_Scoord_KJH4(target_coord, approaching_coord, Scoord)
            New_Scoord[1] = New_Scoord[1] + _Nand_Nbody_Xvtdown2Nbody
            tmpXY.append(New_Scoord)
            ## Define Coordinates
            self._DesignParameter['SRF_Nbody']['_XYCoordinates'] = tmpXY
	        
        ## ########## ########## ########## ########## ########## ########## ########## ########## ########## ########## Pullup: PMOSes source and Nbody connection
        ## Boundary_element Generation
        ## Generate Boundary_element: ex)LayerName: METAL1 / DIFF (_ODLayer) / POLY / PIMP (_PPLayer) / NWELL / SLVT LVT RVT HVT / OP(OPpress) / CONT (CA) / PCCRIT
        self._DesignParameter['BND_PMOS_Source2Nbody_Vtc_M1'] = self._BoundaryElementDeclaration(
            _Layer=DesignParameters._LayerMapping['METAL1'][0],
            _Datatype=DesignParameters._LayerMapping['METAL1'][1],
            _XWidth=None,
            _YWidth=None,
            _XYCoordinates=[],
        )

        ## Define Boundary_element _YWidth : ViaYmin 기준
        tmp1 = self.get_param_KJH4('SRF_Pullup','SRF_PMOS0','BND_Source_M1')
        tmp2 = self.get_param_KJH4('SRF_Nbody','SRF_NbodyContactPhyLen','BND_Met1Layer')
        self._DesignParameter['BND_PMOS_Source2Nbody_Vtc_M1']['_YWidth'] = abs (tmp1[0][0][0][0]['_XY_down'][1] - tmp2[0][0][0][0]['_XY_up'][1])

        ## Define Boundary_element _XWidth
        tmp = self.get_param_KJH4('SRF_Pullup','SRF_PMOS0','BND_Source_M1')
        self._DesignParameter['BND_PMOS_Source2Nbody_Vtc_M1']['_XWidth'] = tmp[0][0][0][0]['_Xwidth']

        ## Define Boundary_element _XYCoordinates
        self._DesignParameter['BND_PMOS_Source2Nbody_Vtc_M1']['_XYCoordinates'] = [[0, 0]]

        tmpXY = []
        tmp = self.get_param_KJH4('SRF_Pullup','SRF_PMOS0','BND_Source_M1')
        for j in range(0,_Nand_Num_Input):
	        for i in range(0,len(tmp[0][0])):
	            ## Calculate Sref XYcoord
	                ## Calculate
	                    ## Target_coord: _XY_type1
	            tmp1 = self.get_param_KJH4('SRF_Pullup','SRF_PMOS{}'.format(j),'BND_Source_M1')
	            target_coord = tmp1[0][0][i][0]['_XY_down_left']
	                    ## Approaching_coord: _XY_type2
	            tmp2 = self.get_param_KJH4('BND_PMOS_Source2Nbody_Vtc_M1')
	            approaching_coord = tmp2[0][0]['_XY_down_left']
	                    ## Sref coord
	            tmp3 = self.get_param_KJH4('BND_PMOS_Source2Nbody_Vtc_M1')
	            Scoord = tmp3[0][0]['_XY_origin']
	            ## Cal
	            New_Scoord = self.get_Scoord_KJH4(target_coord, approaching_coord, Scoord)
	            tmpXY.append(New_Scoord)
        ## Define coordinates
        self._DesignParameter['BND_PMOS_Source2Nbody_Vtc_M1']['_XYCoordinates'] = tmpXY
        
        ## ########## ########## ########## ########## ########## ########## ########## ########## ########## ########## ##########  Pullup: NWELL Exten
        ## Boundary_element Generation
        ## Generate Boundary_element: ex)LayerName: METAL1 / DIFF (_ODLayer) / POLY / PIMP (_PPLayer) / NWELL / SLVT LVT RVT HVT / OP(OPpress) / CONT (CA) / PCCRIT
        self._DesignParameter['BND_PMOS_NellExten'] = self._BoundaryElementDeclaration(
            _Layer=DesignParameters._LayerMapping['NWELL'][0],
            _Datatype=DesignParameters._LayerMapping['NWELL'][1],
            _XWidth=None,
            _YWidth=None,
            _XYCoordinates=[],
        )

        ## Define Boundary_element _YWidth
        tmp1 = self.get_param_KJH4('SRF_Nbody','SRF_NbodyContactPhyLen','BND_Nwell')
        tmp2 = self.get_param_KJH4('SRF_Pullup','SRF_PMOS0','BND_{}Layer'.format(_Nand_XVT))
        self._DesignParameter['BND_PMOS_NellExten']['_YWidth'] = abs( tmp1[0][0][0][0]['_XY_up'][1] - tmp2[0][0][0][0]['_XY_down'][1] )

        ## Define Boundary_element _XWidth
        tmp = self.get_param_KJH4('SRF_Nbody','SRF_NbodyContactPhyLen','BND_Nwell')
        self._DesignParameter['BND_PMOS_NellExten']['_XWidth'] = tmp[0][0][0][0]['_Xwidth']

        ## Define Boundary_element _XYCoordinates
        self._DesignParameter['BND_PMOS_NellExten']['_XYCoordinates'] = [[0, 0]]

        ## Calculate Sref XYcoord
        tmpXY = []
            ## initialized Sref coordinate
        self._DesignParameter['BND_PMOS_NellExten']['_XYCoordinates'] = [[0, 0]]
            ## Calculate
                ## Target_coord: _XY_type1
        tmp1 = self.get_param_KJH4('SRF_Nbody','SRF_NbodyContactPhyLen','BND_Nwell')
        target_coord = tmp1[0][0][0][0]['_XY_up_left']
                ## Approaching_coord: _XY_type2
        tmp2 = self.get_param_KJH4('BND_PMOS_NellExten')
        approaching_coord = tmp2[0][0]['_XY_up_left']
                ## Sref coord
        tmp3 = self.get_param_KJH4('BND_PMOS_NellExten')
        Scoord = tmp3[0][0]['_XY_origin']
                ## Cal
        New_Scoord = self.get_Scoord_KJH4(target_coord, approaching_coord, Scoord)
        tmpXY.append(New_Scoord)
            ## Define coordinates
        self._DesignParameter['BND_PMOS_NellExten']['_XYCoordinates'] = tmpXY
        
        ## ########## ########## ########## ########## ########## ########## ########## ########## ########## ########## ##########  IN/OUT
        ## ########## ########## ########## ########## ########## ########## ########## ########## ########## ##########   IN/OUT : Input
        for i in range(0,_Nand_Num_Input):
	        ## Boundary_element Generation
	        ## Generate Boundary_element: ex)LayerName: METAL1 / DIFF (_ODLayer) / POLY / PIMP (_PPLayer) / NWELL / SLVT LVT RVT HVT / OP(OPpress) / CONT (CA) / PCCRIT
	        self._DesignParameter['BND_Input{}_Vtc_M1'.format(i)] = self._BoundaryElementDeclaration(
	            _Layer=DesignParameters._LayerMapping['METAL1'][0],
	            _Datatype=DesignParameters._LayerMapping['METAL1'][1],
	            _XWidth=None,
	            _YWidth=None,
	            _XYCoordinates=[],
	        )
	
	        ## Define Boundary_element _XWidth
	        self._DesignParameter['BND_Input{}_Vtc_M1'.format(i)]['_XWidth'] = 50
	
	        ## Define Boundary_element _YWidth
	        tmp1 = self.get_param_KJH4('SRF_Pulldown','SRF_NMOS0', 'BND_Gate_Hrz_Mx')
	        tmp2 = self.get_param_KJH4('SRF_Pullup','SRF_PMOS0', 'BND_Gate_Hrz_Mx')
	        self._DesignParameter['BND_Input{}_Vtc_M1'.format(i)]['_YWidth'] =  abs( tmp2[0][0][0][0]['_XY_up'][1] - tmp1[0][0][0][0]['_XY_down'][1])
	
	        ## Define Boundary_element _XYCoordinates
	        self._DesignParameter['BND_Input{}_Vtc_M1'.format(i)]['_XYCoordinates'] = [[0, 0]]
	
	        ## Calculate Sref XYcoord
	        tmpXY = []
	        ## initialized Sref coordinate
	        self._DesignParameter['BND_Input{}_Vtc_M1'.format(i)]['_XYCoordinates'] = [[0, 0]]
	        ## Calculate
	        ## Target_coord: _XY_type1
	        tmp1 = self.get_param_KJH4('SRF_Pulldown','SRF_NMOS{}'.format(i), 'BND_Gate_Hrz_Mx')
	        target_coord = tmp1[0][0][0][0]['_XY_down']
	        ## Approaching_coord: _XY_type2
	        tmp2 = self.get_param_KJH4('BND_Input{}_Vtc_M1'.format(i))
	        approaching_coord = tmp2[0][0]['_XY_down']
	        ## Sref coord
	        tmp3 = self.get_param_KJH4('BND_Input{}_Vtc_M1'.format(i))
	        Scoord = tmp3[0][0]['_XY_origin']
	        ## Cal
	        New_Scoord = self.get_Scoord_KJH4(target_coord, approaching_coord, Scoord)
	        tmpXY.append(New_Scoord)
	        ## Define coordinates
	        self._DesignParameter['BND_Input{}_Vtc_M1'.format(i)]['_XYCoordinates'] = tmpXY
        
        ## ########## ########## ########## ########## ########## ########## ########## ########## ########## ##########   IN/OUT : Output
        ## Pre-defined
        Oupout_Hrz_Exten = 150
        ## ########## ########## ########## ########## ########## ########## ########## ########## ########## OUT: PMOS0 Hrz M2 Exten.
        ## Boundary_element Generation
        ## Generate Boundary_element: ex)LayerName: METAL1 / DIFF (_ODLayer) / POLY / PIMP (_PPLayer) / NWELL / SLVT LVT RVT HVT / OP(OPpress) / CONT (CA) / PCCRIT
        self._DesignParameter['BND_PMOS0_Drain_M2_Hrz_Exten'] = self._BoundaryElementDeclaration(
            _Layer=DesignParameters._LayerMapping['METAL2'][0],
            _Datatype=DesignParameters._LayerMapping['METAL2'][1],
            _XWidth=None,
            _YWidth=None,
            _XYCoordinates=[],
        )

        ## Define Boundary_element _XWidth
        # Most right
        tmp1 = self.get_param_KJH4('SRF_Pulldown', 'SRF_NMOS0', 'BND_Met1Layer')
        tmp2 = self.get_param_KJH4('SRF_Pullup', 'SRF_PMOS0', 'BND_Met1Layer')

        if tmp1[0][0][-1][0]['_XY_right'][0] > tmp2[0][0][-1][0]['_XY_right'][0]:
            most_right = tmp1[0][0][-1][0]['_XY_right'][0]
        else:
            most_right = tmp2[0][0][-1][0]['_XY_right'][0]

        # Xwidth
        tmp = self.get_param_KJH4('SRF_Pullup', 'SRF_PMOS0', 'BND_Drain_Hrz_M2')
        self._DesignParameter['BND_PMOS0_Drain_M2_Hrz_Exten']['_XWidth'] = abs(most_right - tmp[0][0][0][0]['_XY_left'][0])+Oupout_Hrz_Exten

        ## Define Boundary_element _YWidth
        self._DesignParameter['BND_PMOS0_Drain_M2_Hrz_Exten']['_YWidth'] = 50

        ## Define Boundary_element _XYCoordinates
        self._DesignParameter['BND_PMOS0_Drain_M2_Hrz_Exten']['_XYCoordinates'] = [[0, 0]]

        ## Get_Scoord_v4.
        ## Calculate Sref XYcoord
        tmpXY = []
        ## initialized Sref coordinate
        self._DesignParameter['BND_PMOS0_Drain_M2_Hrz_Exten']['_XYCoordinates'] = [[0, 0]]
        ## Calculate
        ## Target_coord: _XY_type1
        tmp1 = self.get_param_KJH4('SRF_Pullup', 'SRF_PMOS0', 'BND_Drain_Hrz_M2')
        target_coord = tmp1[0][0][0][0]['_XY_down_left']
        ## Approaching_coord: _XY_type2
        tmp2 = self.get_param_KJH4('BND_PMOS0_Drain_M2_Hrz_Exten')
        approaching_coord = tmp2[0][0]['_XY_down_left']
        ## Sref coord
        tmp3 = self.get_param_KJH4('BND_PMOS0_Drain_M2_Hrz_Exten')
        Scoord = tmp3[0][0]['_XY_origin']
        ## Cal
        New_Scoord = self.get_Scoord_KJH4(target_coord, approaching_coord, Scoord)
        tmpXY.append(New_Scoord)
        ## Define Coordinates
        self._DesignParameter['BND_PMOS0_Drain_M2_Hrz_Exten']['_XYCoordinates'] = tmpXY

        ## ########## ########## ########## ########## ########## ########## ########## ########## ########## OUT: NMOS0 Hrz M2 Exten.
        ## Boundary_element Generation
        ## Generate Boundary_element: ex)LayerName: METAL1 / DIFF (_ODLayer) / POLY / PIMP (_PPLayer) / NWELL / SLVT LVT RVT HVT / OP(OPpress) / CONT (CA) / PCCRIT
        self._DesignParameter['BND_NMOS0_Drain_M2_Hrz_Exten'] = self._BoundaryElementDeclaration(
            _Layer=DesignParameters._LayerMapping['METAL2'][0],
            _Datatype=DesignParameters._LayerMapping['METAL2'][1],
            _XWidth=None,
            _YWidth=None,
            _XYCoordinates=[],
        )

        ## Define Boundary_element _XWidth
        # Most right
        tmp1 = self.get_param_KJH4('SRF_Pulldown', 'SRF_NMOS0', 'BND_Met1Layer')
        tmp2 = self.get_param_KJH4('SRF_Pullup', 'SRF_PMOS0', 'BND_Met1Layer')

        if tmp1[0][0][-1][0]['_XY_right'][0] > tmp2[0][0][-1][0]['_XY_right'][0]:
            most_right = tmp1[0][0][-1][0]['_XY_right'][0]
        else:
            most_right = tmp2[0][0][-1][0]['_XY_right'][0]

        # Xwidth
        tmp = self.get_param_KJH4('SRF_Pulldown', 'SRF_NMOS0', 'BND_Drain_Hrz_M2')
        self._DesignParameter['BND_NMOS0_Drain_M2_Hrz_Exten']['_XWidth'] = abs(most_right - tmp[0][0][0][0]['_XY_left'][0])+Oupout_Hrz_Exten

        ## Define Boundary_element _YWidth
        self._DesignParameter['BND_NMOS0_Drain_M2_Hrz_Exten']['_YWidth'] = 50

        ## Define Boundary_element _XYCoordinates
        self._DesignParameter['BND_NMOS0_Drain_M2_Hrz_Exten']['_XYCoordinates'] = [[0, 0]]

        ## Get_Scoord_v4.
        ## Calculate Sref XYcoord
        tmpXY = []
        ## initialized Sref coordinate
        self._DesignParameter['BND_NMOS0_Drain_M2_Hrz_Exten']['_XYCoordinates'] = [[0, 0]]
        ## Calculate
        ## Target_coord: _XY_type1
        tmp1 = self.get_param_KJH4('SRF_Pulldown', 'SRF_NMOS0', 'BND_Drain_Hrz_M2')
        target_coord = tmp1[0][0][0][0]['_XY_down_left']
        ## Approaching_coord: _XY_type2
        tmp2 = self.get_param_KJH4('BND_NMOS0_Drain_M2_Hrz_Exten')
        approaching_coord = tmp2[0][0]['_XY_down_left']
        ## Sref coord
        tmp3 = self.get_param_KJH4('BND_NMOS0_Drain_M2_Hrz_Exten')
        Scoord = tmp3[0][0]['_XY_origin']
        ## Cal
        New_Scoord = self.get_Scoord_KJH4(target_coord, approaching_coord, Scoord)
        tmpXY.append(New_Scoord)
        ## Define Coordinates
        self._DesignParameter['BND_NMOS0_Drain_M2_Hrz_Exten']['_XYCoordinates'] = tmpXY

        ## ########## ########## ########## ########## ########## ########## ########## ########## ########## OUT: Vtc M2
        ## Boundary_element Generation
        ## Generate Boundary_element: ex)LayerName: METAL1 / DIFF (_ODLayer) / POLY / PIMP (_PPLayer) / NWELL / SLVT LVT RVT HVT / OP(OPpress) / CONT (CA) / PCCRIT
        self._DesignParameter['BND_Out_Vtc_M2'] = self._BoundaryElementDeclaration(
            _Layer=DesignParameters._LayerMapping['METAL2'][0],
            _Datatype=DesignParameters._LayerMapping['METAL2'][1],
            _XWidth=None,
            _YWidth=None,
            _XYCoordinates=[],
        )

        ## Define Boundary_element _XWidth
        self._DesignParameter['BND_Out_Vtc_M2']['_XWidth'] = 50

        ## Define Boundary_element _YWidth
        tmp1 = self.get_param_KJH4('BND_NMOS0_Drain_M2_Hrz_Exten')
        tmp2 = self.get_param_KJH4('BND_PMOS0_Drain_M2_Hrz_Exten')
        self._DesignParameter['BND_Out_Vtc_M2']['_YWidth'] = abs(tmp2[0][0]['_XY_up'][1] - tmp1[0][0]['_XY_down'][1])

        ## Define Boundary_element _XYCoordinates
        self._DesignParameter['BND_Out_Vtc_M2']['_XYCoordinates'] = [[0, 0]]

        ## Calculate Sref XYcoord
        tmpXY = []
        ## initialized Sref coordinate
        self._DesignParameter['BND_Out_Vtc_M2']['_XYCoordinates'] = [[0, 0]]
        ## Calculate
        ## Target_coord: _XY_type1
        tmp1 = self.get_param_KJH4('BND_NMOS0_Drain_M2_Hrz_Exten')
        target_coord = tmp1[0][0]['_XY_down_right']

        ## Approaching_coord: _XY_type2
        tmp2 = self.get_param_KJH4('BND_Out_Vtc_M2')
        approaching_coord = tmp2[0][0]['_XY_down_right']

        ## Sref coord
        tmp3 = self.get_param_KJH4('BND_Out_Vtc_M2')
        Scoord = tmp3[0][0]['_XY_origin']
        ## Cal
        New_Scoord = self.get_Scoord_KJH4(target_coord, approaching_coord, Scoord)
        tmpXY.append(New_Scoord)
        ## Define coordinates
        self._DesignParameter['BND_Out_Vtc_M2']['_XYCoordinates'] = tmpXY
        
        
        
        
        ## ########## ########## ########## ########## ########## ########## ########## ########## ########## ########## ########## ########## Erase Cont
        del self._DesignParameter['SRF_Pbody']['_DesignObj']._DesignParameter['SRF_PbodyContactPhyLen']['_DesignObj']._DesignParameter['BND_COLayer']
        del self._DesignParameter['SRF_Nbody']['_DesignObj']._DesignParameter['SRF_NbodyContactPhyLen']['_DesignObj']._DesignParameter['BND_COLayer']

        
        
        
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

    libname = 'Proj_ZZ01_Q00_02_Nand'
    cellname = 'Q00_02_Nand_99'
    _fileName = cellname + '.gds'

    ''' Input Parameters for Layout Object '''
    InputParams = dict(

        # Num of Input
        _Nand_Num_Input         = 4,  # Number>2

        # MOSFET
            # Common
        _Nand_NumberofGate      = 2,                        # Number
        _Nand_ChannelLength	    = 30,                       # Number
        _Nand_POGate_ViaMxMx    = [0, 1],                   # Ex) [1,5] -> ViaM1M5
        _Nand_XVT				= 'SLVT'  ,                 # 'XVT' ex)SLVT/LVT/RVT/HVT
            # Pulldown(NMOS)
		        # Physical dimension
		_Nand_NMOS_ChannelWidth	                = 800,      # Number
		        # Source_node setting
		_Nand_NMOS_Source_Via_Close2POpin_TF    = False,    # True/False --> First MOS
		        # Poly Gate setting
		            # Poly Gate setting : vertical length
		_Nand_NMOS_POGate_Comb_length           = None,     # None/Number
            # Pulldown(PMOS)
                # Physical dimension
		_Nand_PMOS_ChannelWidth	                = 400,      # Number
		        # Poly Gate setting
		            # Poly Gate setting : vertical length
		_Nand_PMOS_POGate_Comb_length           = None,     # None/Number

        # Power Rail
            #Pbody_Pulldown(NMOS)
        _Nand_Pbody_NumCont              = 2,     # Number
        _Nand_Pbody_XvtTop2Pbody         = None,  # Number/None(Minimum)
            #Nbody_Pullup(PMOS)
        _Nand_Nbody_NumCont              = 2,     # Number
        _Nand_Nbody_Xvtdown2Nbody        = None,  # Number/None(Minimum)

        # PMOS and NMOS Height
        _Nand_PMOSXvt2NMOSXvt            = 1000,  # number

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
    LayoutObj = _Nand(_DesignParameter=None, _Name=cellname)
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




