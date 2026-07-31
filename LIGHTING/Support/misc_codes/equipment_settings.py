##################################################################################
"""IMPORT DEPENDENCIES"""
from time import sleep
from powi.equipment import ACSource, PowerMeter, ElectronicLoad, Oscilloscope, LecroyScope, LEDControl, Keithley_DC_2230G, RnS_DC_HMPSeries, Tektronix_SigGen_AFG31000, Keysight_33500B
from powi.equipment import headers, create_folder, footers, waveform_counter, soak, convert_argv_to_int_list, tts, prompt, roundup, export_df_to_excel
from misc_codes.equipment_address import *
from misc_codes.general_settings import *
from itertools import permutations
##################################################################################

try:
    ac = ACSource(EQUIPMENT_ADDRESS.AC_SOURCE)
    
except:
    print("AC Source Error")
    pass

try:
    pms = PowerMeter(EQUIPMENT_ADDRESS.POWER_METER_SOURCE)
except:
    print("Power Meter Source Error")
    pass

try:
    pml = PowerMeter(EQUIPMENT_ADDRESS.POWER_METER_LOAD_1)
except:
    print("Power Meter Load 1 Error")
    pass

try:
    pml2 = PowerMeter(EQUIPMENT_ADDRESS.POWER_METER_LOAD_2)
except:
    print("Power Meter Load 2 Error")
    pass

try:
    pml3 = PowerMeter(EQUIPMENT_ADDRESS.POWER_METER_LOAD_3)
except:
    print("Power Meter Load 3 Error")
    pass

# try:
#     pml4 = PowerMeter(EQUIPMENT_ADDRESS.POWER_METER_LOAD_4)
# except:
#     print("Power Meter Load 4 Error")
#     pass

try:
    eload = ElectronicLoad(EQUIPMENT_ADDRESS.ELOAD)
except:
    print("Eload Error")
    pass


try:
    sig_gen = Tektronix_SigGen_AFG31000(EQUIPMENT_ADDRESS.SIG_GEN)
    # sig_gen = Keysight_33500B(EQUIPMENT_ADDRESS.SIG_GEN)
except:
    print("Sig Gen Error")
    pass


try:
    dimmer = RnS_DC_HMPSeries(EQUIPMENT_ADDRESS.DC_SOURCE_DIMMER)
except:
    print("Dimmer Error")
    pass

try: scope = Oscilloscope(EQUIPMENT_ADDRESS.SCOPE)
except: 
    print("Scope Errror")
    pass

# lscope = LecroyScope("169.254.94.235")
# try: 
# except: pass

try: led_ctrl = LEDControl()
except: pass


class EQUIPMENT_FUNCTIONS():

    def __init__(self):
        # pms.current_range(2)
        # pms.voltage_range(150)

        # pml.current_range(5)
        # pml.voltage_range(30)
        pass

    # def simple_AC_ON(self):
    #     ac.turn_on()

    def ANALOG_DC_ON(self, channel, voltage, current):
        dimmer.set_volt_curr(channel, voltage, current)
        dimmer.channel_state(channel, 'ON')

    
    def ANALOG_DC_OFF(self):
        dimmer.channel_state_all('OFF')

    def LED_VOLTAGE(self, voltage):
        led_ctrl.voltage(voltage)

    def SIG_GEN(self, duty, frequency):
        sig_gen.set_load_impedance(channel = 1, impedance = 'INF') 
        # sig_gen.out_cont_pulse(channel = 1, frequency = frequency, phase = '0 DEG', low = '0V', high = '10V', units = 'VPP', duty = duty, width = 'ABC')
        sig_gen.out_cont_pulse(channel = 1, frequency = frequency, phase = '0 DEG', low = '0V', high = '3.3V', units = 'VPP', duty = duty, width = 'ABC')
        sig_gen.channel_state(channel = 1, state ='ON')
        soak(1)

    def SIG_GEN_10VPP(self, duty, frequency):
        sig_gen.set_load_impedance(channel = 1, impedance = 'INF') 
        sig_gen.out_cont_pulse(channel = 1, frequency = frequency, phase = '0 DEG', low = '0V', high = '10V', units = 'VPP', duty = duty, width = 'ABC')
        # sig_gen.out_cont_pulse(channel = 1, frequency = frequency, phase = '0 DEG', low = '0V', high = '3.3V', units = 'VPP', duty = duty, width = 'ABC')
        sig_gen.channel_state(channel = 1, state ='ON')
        soak(1)

    class SCOPE():
        def SCOPE_SCREENSHOT(self, filename, path):
            global waveform_counter
            scope.get_screenshot(filename + '.png', path)
            print(filename)
            # lscope.get_screenshot(filename + '.png', path)
            # waveform_counter += 1
    
        def SCOPE_SCREENSHOT_LOOPER(self, filename, path):
            iter = 0
            while '' == input(">> Press ENTER to continue capture. To stop press other keys to stop: "):
                fname = filename.split('.png')[0] + f'_{iter}' + '.png'
                iter += 1
                self.SCOPE_SCREENSHOT(fname, path)
        
        def RUN_SINGLE(self):
            scope.run_single()

        def RUN(self):
            scope.run()

        def STOP(self):
            scope.stop()

        def MODE_AUTO(self):
            scope.trigger_mode(mode='AUTO')

        def MODE_NORM(self):
            scope.trigger_mode(mode='NORM')

        def TIME_SCALE(self, time_scale):
            """
            Parameters:
            <TimeScale> Range: 25E-12 to 50
                        Increment: 1E-12
                        *RST: 10E-9
                        Default unit: s/div
            """
            scope.time_scale(time_scale)

        def CHANNEL_SETTINGS(self, state, channel=1, scale=1, position=0, label='IOUT', color='LIGHT_BLUE', rel_x_position=50, bandwidth=500, coupling='DCLimit', offset=0):
            """
            COLOR OPTIONS:

            - LIGHT_BLUE
            - YELLOW
            - PINK
            - GREEN
            - BLUE
            - ORANGE


            returns : state of the channel ('ON' or 'OFF')
            """
            scope.channel_settings(state, channel, scale, position, label, color, rel_x_position, bandwidth, coupling, offset)

        def CHANNEL_SCALE(self, channel, scale):
            scope.channel_scale(channel, scale)
        
        def EDGE_TRIGGER(self, trigger_channel, trigger_level, trigger_edge):
            scope.edge_trigger(trigger_channel, trigger_level, trigger_edge)

        def ADJUST_ZOOM_SCALE_POS(self, scale, pos):
            scope.write(f"LAYout:ZOOM:HORZ:REL:SPAN 'Diagram1', 'Zoom1', {scale}")
            scope.write(f"LAYout:ZOOM:HORZ:REL:POS 'Diagram1', 'Zoom1', {pos}")

        def LABEL(self, channel, label, rel_x_position):
            scope.channel_label(channel, label, rel_x_position)
        
        def TIME_POSITION(self, time_position):
            scope.time_position(time_position)

        def POSITION_SCALE(self, time_position, time_scale):
            scope.position_scale(time_position, time_scale)

        def CURSOR(self, channel, cursor_set, X1, X2, Y1, Y2, type="VERT"):
            """type options: VERT, HOR, EITH"""
            scope.cursor(channel, cursor_set, X1, X2, Y1, Y2, type)

        def RECALL_SAVESET(self, address):
            scope.write(f"MMEM:RCL {address}")
        

    def ELOAD_CR_ON(self, channel, cr_load, von):
        eload.channel[channel].von = von
        eload.channel[channel].cr = cr_load
        eload.channel[channel].turn_on()

    def ELOAD_CC_ON(self, channel, cc_load):
        eload.channel[channel].cc = cc_load
        eload.channel[channel].turn_on()

    def MULTIPLE_ELOAD_CC_ON(self, cc1=0.01, cc2=0.01, cc3=0.01):
       self.ELOAD_CC_ON(EQUIPMENT_ADDRESS.ELOAD_CHANNEL_1, cc1)
       self.ELOAD_CC_ON(EQUIPMENT_ADDRESS.ELOAD_CHANNEL_2, cc2)
       self.ELOAD_CC_ON(EQUIPMENT_ADDRESS.ELOAD_CHANNEL_3, cc3)
       
    
    def ELOAD_CV_ON(self, channel, cv):
        eload.channel[channel].cv = cv
        eload.channel[channel].turn_on()

    def ELOAD_OFF(self, channel):
        eload.channel[channel].turn_off()

    def ELOAD_ALL_OFF(self):
        self.ELOAD_OFF(EQUIPMENT_ADDRESS.ELOAD_CHANNEL_1)
        self.ELOAD_OFF(EQUIPMENT_ADDRESS.ELOAD_CHANNEL_2)
        self.ELOAD_OFF(EQUIPMENT_ADDRESS.ELOAD_CHANNEL_3)
        self.ELOAD_OFF(EQUIPMENT_ADDRESS.ELOAD_CHANNEL_4)
    
    def ELOAD_LOAD_TRANSIENT(self, channel, low, high, ton, toff):
        eload.channel[channel].dynamic(low, high, ton, toff)
        eload.channel[channel].turn_on()


    def AC_TURN_ON(self, voltage, type='AC'):
        ac.voltage = voltage
        ac.coupling = type
        ac.turn_on()

    def AC_CURRENT_PEAK(self, peak):
        ac.current_peak(peak)

    def DC_TURN_ON(self, voltage, type='DC'):
        ac.voltage = voltage
        ac.coupling = type
        ac.turn_on()

    def AC_TURN_OFF(self):
        ac.turn_off()

    def AC_CYCLING(self, pulse_count, vin, start_soak_time, off_time, on_time, end_soak_time):
        ac.ac_cycling(pulse_count, vin, start_soak_time, off_time, on_time, end_soak_time)
    
    def DISCHARGE_OUTPUT(self, times):    
        ac.turn_off()
        for i in range(times):
            for i in range(1,9):
                # eload.channel[i].cr = 100
                eload.channel[i].short_on()
                eload.channel[i].turn_on()
            sleep(1)

            for i in range(1,9):
                eload.channel[i].turn_off()
                eload.channel[i].short_off()
            sleep(1)

    def _sigfig(self, number, sigfig):
        try: a = float(f"{number:.{sigfig}f}")
        except: a = "NaN"
        return a

    def two_sig_fig(self, number):
        try: a = float(f"{number:.{2}f}")
        except: a = "NaN"
        return a

    def _pm_measurements(self):

        vac = self._sigfig(pms.voltage, 6)
        iin = self._sigfig(pms.current, 10)*1000
        pin = self._sigfig(pms.power, 6)
        pf = self._sigfig(pms.pf, 6)
        thd = self._sigfig(pms.thd, 2)
        vo1 = self._sigfig(pml.voltage, 6)
        io1 = self._sigfig(pml.current, 6)*1000
        po1 = self._sigfig(pml.power, 2)
        
        return vac, iin, pin, pf, thd, vo1, io1, po1
    
    def _pm_measurements_source(self):
        vac = self._sigfig(pms.voltage, 6)
        iin = self._sigfig(pms.current, 10)*1000
        pin = self._sigfig(pms.power, 6)
        pf = self._sigfig(pms.pf, 6)
        thd = self._sigfig(pms.thd, 2)

        return vac, iin, pin, pf, thd

    def _pm_measurements1(self):
        vo1 = self._sigfig(pml.voltage, 6)
        io1 = self._sigfig(pml.current, 6)*1000
        po1 = self._sigfig(pml.power, 6)
        
        return vo1, io1, po1

    def _pm_measurements2(self):
        vo2 = self._sigfig(pml2.voltage, 6)
        io2 = self._sigfig(pml2.current, 6)*1000
        po2 = self._sigfig(pml2.power, 6)
        
        return vo2, io2, po2
    
    def _pm_measurements3(self):
        vo3 = self._sigfig(pml3.voltage, 6)
        io3 = self._sigfig(pml3.current, 6)*1000
        po3 = self._sigfig(pml3.power, 6)
        
        return vo3, io3, po3

    def OUTPUT_VOLTAGE_POWER_METER(self):
        vo1 = self._sigfig(pml.voltage, 6)
        return vo1

    def OUTPUT_CURRENT_POWER_METER(self):
        io1 = self._sigfig(pml.current, 6)
        return io1
    
    def INPUT_CURRENT_POWER_METER(self):
        iin1 = self._sigfig(pms.current, 6)
        return iin1
    
    def INPUT_POWER_POWER_METER(self):
        pin1 = self._sigfig(pms.power, 6)
        return pin1
    
    def INPUT_POWER_FACTOR_POWER_METER(self):
        pf1 = self._sigfig(pms.pf, 6)
        return pf1
    
    def OUTPUT_POWER_POWER_METER(self):
        po1 = self._sigfig(pml.power, 6)
        return po1
    
    def INPUT_VOLTAGE_POWER_METER(self):
        vin1 = self._sigfig(pms.voltage, 6)
        return vin1
    
    def GET_HARMONICS(self):
        harmonic_content, percent_content = pms.get_harmonics()
        return harmonic_content, percent_content
    
    def COLLECT_DATA_SINGLE_OUTPUT_CR_LOAD(self, vin, vout, cr):

        vac, iin, pin, pf, thd, vo1, io1, po1 = self._pm_measurements()

        try: vreg1 = self._sigfig(100*(vo1-vout)/vo1, 2)
        except: vreg1 = "NaN"

        
        try:
            iout = vout/cr
            ireg1 = self._sigfig(100*(io1-(iout))/io1, 2)
        except: ireg1 = "NaN"

        try: eff = self._sigfig(100*po1/pin, 2)
        except: eff = "NaN"

        output_list = [cr, vin, ac.set_freq(vin), vac, iin, pin, pf, thd, vo1, io1, po1, vreg1, ireg1, eff]

        return output_list
    
    def COLLECT_DATA_SINGLE_OUTPUT_CC_LOAD_1_PDEL_SCOPE(self, vin, vout, cc, percent, scope_channel_list):

        vac, iin, pin, pf, thd, vo1, io1, po1 = self._pm_measurements()

        try: vreg1 = self._sigfig(100*(vo1-vout)/vo1, 6)
        except: vreg1 = "NaN"

        try: ireg1 = self._sigfig(100*(io1-(cc*1000))/io1, 6)
        except: ireg1 = "NaN"

        try: eff = self._sigfig(100*po1/pin, 6)
        except: eff = "NaN"

        output_list = [percent, vin, ac.set_freq(vin), vac, iin, pin, pf, thd, vo1, io1, po1, vreg1, eff]
        

        for channel in scope_channel_list:
            scope.stop()
            try:
                labels, values = scope.get_measure(channel)
                for i in range(len(values)):
                    output_list.append(values[i])
            except:
                pass

        ## uncomment this
        # output_list.append(scope.get_cursor(1)["y1 position"])
        # output_list.append(scope.get_cursor(1)["y2 position"])
        # print(output_list)
        return output_list
    
    def COLLECT_DATA_SINGLE_OUTPUT_CC_LOAD_1_PDEL(self, vin, vout, cc, percent):

        vac, iin, pin, pf, thd, vo1, io1, po1 = self._pm_measurements()

        try: vreg1 = self._sigfig(100*(vo1-vout)/vo1, 6)
        except: vreg1 = "NaN"

        try: ireg1 = self._sigfig(100*(io1-(cc*1000))/io1, 6)
        except: ireg1 = "NaN"

        try: eff = self._sigfig(100*po1/pin, 6)
        except: eff = "NaN"

        scope.stop()
        sleep(1)
        scope_measurement = scope.get_measure_dict(1)
        # print(scope_measurement)
        try:
            pkpk = EQUIPMENT_FUNCTIONS()._sigfig(scope_measurement['Peak to peak'], 4)
            pkpk = pkpk*1000
        except:
            pkpk = 0
        output_list = [percent, vin, ac.set_freq(vin), vac, iin, pin, pf, thd, vo1, io1, po1, vreg1, eff, pkpk]

        return output_list

    def COLLECT_DATA_SINGLE_OUTPUT_NO_LOAD(self, vin):

        vac, iin, pin, pf, thd, vo1, io1, po1 = self._pm_measurements()
        output_list = [vin, ac.set_freq(vin), vac, iin, pin, pf, thd, vo1, io1, po1]
        return output_list
    

    

    def COLLECT_DATA_SINGLE_OUTPUT_RBIAS(self, vin, iteration, rbias):

        vac, iin, pin, pf, thd, vo1, io1, po1 = self._pm_measurements()
        rbias = self._sigfig(rbias, 2)

        try: eff = self._sigfig(100*po1/pin, 6)
        except: eff = "NaN"

        scope.stop()
        vbias_measurement = scope.get_measure_dict(1)
        try:
            vbias = EQUIPMENT_FUNCTIONS()._sigfig(vbias_measurement['RMS'], 4)
        except:
            vbias = 0

        vbp_measurement = scope.get_measure_dict(2)
        try:
            vbp = EQUIPMENT_FUNCTIONS()._sigfig(vbp_measurement['RMS'], 4)
        except:
            vbp = 0

        try:
            ibias = (vbias - vbp)*1000000 / rbias
        except:
            ibias = 0

        scope.run()

        output_list = [iteration, vin, ac.set_freq(vin), rbias, vbias, vbp, ibias, eff]
        return output_list
    

    def COLLECT_DATA_SINGLE_OUTPUT_300mW_EFF(self, output_list):

        vac, iin, pin, pf, thd, vo1, io1, po1 = self._pm_measurements()

        try: eff = self._sigfig(100*po1/pin, 6)
        except: eff = "NaN"

        output_list.append(pin)
        output_list.append(po1)
        output_list.append(eff)

        return output_list
    
    def COLLECT_DATA_SINGLE_OUTPUT_NL_after_300mW(self, output_list):

        vac, iin, pin, pf, thd, vo1, io1, po1 = self._pm_measurements()

        output_list.append(pin)

        return output_list

    def COLLECT_DATA_SINGLE_OUTPUT_CC_LOAD_1(self, vin, vout, cc, percent):

        vac, iin, pin, pf, thd, vo1, io1, po1 = self._pm_measurements()

        try: vreg1 = self._sigfig(100*(vo1-vout)/vo1, 6)
        except: vreg1 = "NaN"

        try: ireg1 = self._sigfig(100*(io1-(cc*1000))/io1, 6)
        except: ireg1 = "NaN"

        try: eff = self._sigfig(100*po1/pin, 6)
        except: eff = "NaN"

        output_list = [percent, vin, ac.set_freq(vin), vac, iin, pin, pf, thd, vo1, io1, po1, vreg1, eff]

        return output_list

    def COLLECT_DATA_SINGLE_OUTPUT_CC_LOAD_1_COMPLETE(self, vin, vout, cc, vbulk):

        vac, iin, pin, pf, thd, vo1, io1, po1 = self._pm_measurements()
        vo2, io2, po2 = self._pm_measurements2()

        try: vreg1 = self._sigfig(100*(vo1-vout)/vo1, 6)
        except: vreg1 = "NaN"

        try: ireg1 = self._sigfig(100*(io1-(cc*1000))/io1, 6)
        except: ireg1 = "NaN"

        try: eff = self._sigfig(100*po1/pin, 6)
        except: eff = "NaN"

        # vbulk = vo2
        # ['Vac (rms)', 'Freq (Hz)', 'Vin (rms)', 'Iin (mA)', 'Pin (W)', 'PF', '% THD', 'Vo (V)', 'Io (mA)', 'Po (W)', '%V Reg', '%Ireg', 'Efficiency', 'Vbulk (V)']

        output_list = [vin, ac.set_freq(vin), vac, iin, pin, pf, thd, vo1, io1, po1, ireg1, eff, vbulk]

        return output_list    
    
    def COLLECT_DATA_SINGLE_OUTPUT_CC_LOAD_2(self, vin, vout1, vout2, cc1, cc2, percent):

        vac, iin, pin, pf, thd, vo1, io1, po1 = self._pm_measurements()
        vo2, io2, po2 = self._pm_measurements2()

        try: vreg1 = self._sigfig(100*(vo1-vout1)/vo1, 6)
        except: vreg1 = "NaN"

        try: vreg2 = self._sigfig(100*(vo2-vout2)/vo2, 6)
        except: vreg2 = "NaN"

        try: ireg1 = self._sigfig(100*(io1-(cc1*1000))/io1, 6)
        except: ireg1 = "NaN"

        try: ireg2 = self._sigfig(100*(io2-(cc2*1000))/io2, 6)
        except: ireg2 = "NaN"

        try: eff_total = self._sigfig(100*(po2+po1)/pin, 6)
        except: eff_total = "NaN"

        timestamp = datetime.now().time()
        
        output_list = [percent, vin, ac.set_freq(vin), vac, iin, pin, pf, thd, vo1, io1, po1, vreg1, vo2, io2, po2, vreg2, eff_total]

        return output_list
    
    def COLLECT_DATA_DUAL_MODE_EFFICIENCY(self, vin, vout1, vout2, cc1, cc2, percent1, percent2):

        vac, iin, pin, pf, thd, vo1, io1, po1 = self._pm_measurements()
        vo2, io2, po2 = self._pm_measurements2()

        try: vreg1 = self._sigfig(100*(vo1-vout1)/vo1, 6)
        except: vreg1 = "NaN"

        try: vreg2 = self._sigfig(100*(vo2-vout2)/vo2, 6)
        except: vreg2 = "NaN"

        try: ireg1 = self._sigfig(100*(io1-(cc1*1000))/io1, 6)
        except: ireg1 = "NaN"

        try: ireg2 = self._sigfig(100*(io2-(cc2*1000))/io2, 6)
        except: ireg2 = "NaN"

        try: eff_total = self._sigfig(100*(po2+po1)/pin, 6)
        except: eff_total = "NaN"

        timestamp = datetime.now().time()
        
        output_list = [percent1, percent2, vin, ac.set_freq(vin), vac, iin, pin, pf, thd, vo1, io1, po1, vreg1, vo2, io2, po2, vreg2, eff_total]

        return output_list

    def BLANK_SPACE(self, df):

        output_list = [""] * len(df.columns)

        return output_list
    
    def COLLECT_DATA_SINGLE_OUTPUT_DIMMING(self, vin, vout, cc, dim):

        vac, iin, pin, pf, thd, vo1, io1, po1 = self._pm_measurements()

        try: vreg1 = self._sigfig(100*(vo1-vout)/vo1, 6)
        except: vreg1 = "NaN"

        try: ireg1 = self._sigfig(100*(io1-(cc*1000))/io1, 6)
        except: ireg1 = "NaN"

        try: eff = self._sigfig(100*po1/pin, 6)
        except: eff = "NaN"
 
        timestamp = datetime.now().time()

        output_list = [timestamp, dim, cc, vin, ac.set_freq(vin), vac, iin, pin, pf, thd, vo1, io1, po1, vreg1, ireg1, eff]

        return output_list
    
    def COLLECT_DATA_SINGLE_OUTPUT_CC_LOAD_WIRELESS(self, vin, vout, cc, channel_list):

        vac, iin, pin, pf, thd, vo1, io1, po1 = self._pm_measurements()

        try: vreg1 = self._sigfig(100*(vo1-vout)/vo1, 6)
        except: vreg1 = "NaN"

        try: ireg1 = self._sigfig(100*(io1-(cc))/io1, 6)
        except: ireg1 = "NaN"

        try: eff = self._sigfig(100*po1/pin, 6)
        except: eff = "NaN"

        # from misc_codes.logger import read_uart_data
        # a = read_uart_data()
        # ce = a[1]
        # chs = a[0]
        # trough = a[2]
        # peak = a[3]
        # print(a)

        from i2c_reader import read_eeprom
        isense_adc, vbus_adc, chs, ce, trough, peak, vcoil_adc, duty_holder, rp8, pin_adc, pf_adc, pout_adc, eff_adc, vin_adc, state, status_if_pout_comms_received, fod_status = read_eeprom()

        scope.stop()
        scope_comms_measurement = scope.get_measure_dict(1)
        scope_measurement = scope.get_measure_dict(4)
        # print(scope_measurement)
        # scope_measurement2 = scope.get_measure_dict(2)
        comms = EQUIPMENT_FUNCTIONS()._sigfig(scope_comms_measurement['Max'], 4)/1000
        fsw = EQUIPMENT_FUNCTIONS()._sigfig(scope_measurement['Frequency'], 4)/1000
        duty = EQUIPMENT_FUNCTIONS()._sigfig(scope_measurement['Pos. duty cycle'], 2)
        # vcoil_max = EQUIPMENT_FUNCTIONS()._sigfig(scope_measurement2['Max'], 4)
        scope.run()

        print("="*60)
        print(f"duty_holder = {duty_holder}, duty = {duty} %, freq = {fsw:2f} kHz")
        print()
        print(f"VbusSen = {vin_adc}, Vin (actual) = {vac} Vac, Vin = {vin} Vac")
        print(f"Vbat = {vo1} V, Icharge = {io1} A")
        print()
        # print(f"Vcoil_adc = {vcoil_adc}, Vcoil_max = {vcoil_max} V")
        # print(f"FOD Status: {fod_status}")
        print()
        print(f"Efficiency = {eff} %")
        print(f"CHS = {chs*100/255:.2f} %")
        print(f"CE = {ce}")
        print(f"COMMS_count = T: {trough}, P: {peak}")
        
        if state == 1: print(f"Tx State = A-ping")
        if state == 2: print(f"Tx State = D-ping")
        if state == 3: print(f"Tx State = LCS")

        if comms > 2:
            print("COMMS STABLE")
            rp8 = 10
        else:
            print("NO COMMS")
            rp8 = 0
        print("="*60)


        output_list = [datetime.now().time(), cc, vin, ac.set_freq(vin), vac, iin, pin, pf, thd, vo1, io1, po1, vreg1, ireg1, eff,
                       ce, chs, trough, peak, isense_adc, vbus_adc, vcoil_adc, duty_holder, rp8,
                       pin_adc, pf_adc, pout_adc, eff_adc, vin_adc, state, status_if_pout_comms_received, fod_status]
        # output_list = [cc, vin, ac.set_freq(vin), vac, iin, pin, pf, thd, vo1, io1, po1, vreg1, ireg1, eff]
        
        for channel in channel_list:
            try:
                labels, values = scope.get_measure(channel)
                for i in range(len(values)):
                    output_list.append(values[i])
            except:
                pass

        return output_list
    
    def COLLECT_DATA_SINGLE_OUTPUT_CC_LOAD_SCOPE(self, vin, vout, cc, FO, channel_list):

        vac, iin, pin, pf, thd, vo1, io1, po1 = self._pm_measurements()

        try: vreg1 = self._sigfig(100*(vo1-vout)/vo1, 6)
        except: vreg1 = "NaN"

        try: ireg1 = self._sigfig(100*(io1-(cc))/io1, 6)
        except: ireg1 = "NaN"

        try: eff = self._sigfig(100*po1/pin, 6)
        except: eff = "NaN"

        output_list = [cc, vin, ac.set_freq(vin), vac, iin, pin, pf, thd, vo1, io1, po1, vreg1, ireg1, eff, FO]

        for channel in channel_list:
            try:
                labels, values = scope.get_measure(channel)
                for i in range(len(values)):
                    output_list.append(values[i])
            except:
                pass

        output_list.append(scope.get_cursor(1)["y1 position"])
        output_list.append(scope.get_cursor(1)["y2 position"])

        return output_list

    def COLLECT_DATA_SINGLE_OUTPUT_CC_LOAD_BROWNIN_WIRELESS(self, vin, vout, cc, channel_list):

        # Note: Use saveset in the oscilloscope

        vac, iin, pin, pf, thd, vo1, io1, po1 = self._pm_measurements()

        try: vreg1 = self._sigfig(100*(vo1-vout)/vo1, 6)
        except: vreg1 = "NaN"

        try: ireg1 = self._sigfig(100*(io1-(cc))/io1, 6)
        except: ireg1 = "NaN"

        try: eff = self._sigfig(100*po1/pin, 6)
        except: eff = "NaN"

        
        output_list = [cc, vin, ac.set_freq(vin), vac, iin, pin, pf, thd, vo1, io1, po1, vreg1, ireg1, eff]

        for channel in channel_list:
            try:
                labels, values = scope.get_measure(channel)
                for i in range(len(values)):
                    output_list.append(values[i])
            except:
                pass

        print(output_list)

        return output_list

    def APPEND_SCOPE_LABELS(self, header_list, channel):
        """
            Append labels for the specified channel to the current header_list
        """
        labels, values = scope.get_measure(channel)
        print(channel)
        for i in range(len(values)):
            # label = f"{scope.query_channel_label(channel)} {labels[i]}"
            label = f"CH{(channel)} {labels[i]}"

            header_list.append(label)

        return header_list
    
    def APPEND_SCOPE_CURSOR_LABELS(self, header_list, cursor_set):
        if scope.query_cursor_state(cursor_set):
            label = f"Cursor_{cursor_set}"
            header_list.append(label)
            
        return header_list


    def COLLECT_DATA_SINGLE_OUTPUT_LED_LOAD(self, vin, led, iout):

        vac, iin, pin, pf, thd, vo1, io1, po1 = self._pm_measurements()

        try: vreg1 = self._sigfig(100*(vo1-led)/vo1, 2)
        except: vreg1 = "NaN"

        try: ireg1 = self._sigfig(100*(io1-(iout*1000)/io1, 2))
        except: ireg1 = "NaN"

        try: eff = self._sigfig(100*po1/pin, 2)
        except: eff = "NaN"

        output_list = [led, vin, ac.set_freq(vin), vac, iin, pin, pf, thd, vo1, io1, po1, vreg1, ireg1, eff]

        return output_list
    
    def COLLECT_DATA_SINGLE_OUTPUT_LED_LOAD_DIM(self, vin, led, iout, dim):

        vac, iin, pin, pf, thd, vo1, io1, po1 = self._pm_measurements()

        try: vreg1 = self._sigfig(100*(vo1-led)/vo1, 2)
        except: vreg1 = "NaN"

        try: ireg1 = self._sigfig(100*(io1-(iout*1000))/io1, 2)
        except: ireg1 = "NaN"

        try: eff = self._sigfig(100*po1/pin, 2)
        except: eff = "NaN"

        try: percent = self._sigfig(io1*100/iout, 5)
        except: percent = "NaN"

        output_list = [percent, dim, led, vin, ac.set_freq(vin), vac, iin, pin, pf, thd, vo1, io1, po1, vreg1, ireg1, eff]

        return output_list
    
    def COLLECT_DATA_2CV_1CC_PARAMETRICS(self, vin, vout_nom_1, vout_nom_2, vout_nom_3,
                             iout_nom_1, iout_nom_2, iout_nom_3, vds_channel):

        vac, iin, pin, pf, thd, vo1, io1, po1 = self._pm_measurements()
        vo2, io2, po2 = self._pm_measurements2()
        vo3, io3, po3 = self._pm_measurements3()

        try: vreg1 = self._sigfig(100*(vo1-vout_nom_1)/vo1, 2)
        except: vreg1 = "NaN"
        try: ireg1 = self._sigfig(100*(io1-(iout_nom_1*1000))/(iout_nom_1*1000), 3)
        except: ireg1 = "NaN"

        try: vreg2 = self._sigfig(100*(vo2-vout_nom_2)/vo2, 2)
        except: vreg2 = "NaN"
        try: ireg2 = self._sigfig(100*(io2-(iout_nom_2*1000))/(iout_nom_2*1000), 3)
        except: ireg2 = "NaN"

        try: vreg3 = self._sigfig(100*(vo3-vout_nom_3)/vo3, 2)
        except: vreg3 = "NaN"
        try: ireg3 = self._sigfig(100*(io3-(iout_nom_3*1000))/(iout_nom_3*1000), 3)
        except: ireg3 = "NaN"

        try: eff = self._sigfig(100*(po1+po2+po3)/pin, 2)
        except: eff = "NaN"

        total_po = po1 + po2 + po3 
        try:
            labels, values = scope.get_measure(vds_channel)
            vds_max = values[0]
        except:
            vds_max = 0

        output_list = [vin, ac.set_freq(vin),
                       vac, iin, pin,
                       pf, thd,
                       vo1, io1, po1, vreg1, ireg1,
                       vo2, io2, po2, vreg2, ireg2,
                       vo3, io3, po3, vreg3, ireg3,
                       total_po, eff, vds_max]

        return output_list
    
    def COLLECT_DATA_1CV_1CC_PARAMETRICS(self, vin, vout_nom_1, vout_nom_2,
                             iout_nom_1, iout_nom_2, scope_channel_list):

        vac, iin, pin, pf, thd, vo1, io1, po1 = self._pm_measurements()
        vo2, io2, po2 = self._pm_measurements2()

        try: vreg1 = self._sigfig(100*(vo1-vout_nom_1)/vo1, 2)
        except: vreg1 = "NaN"
        try: 
            ireg1 = self._sigfig(100*(io1-(iout_nom_1*1000))/(iout_nom_1*1000), 3)
            # print(io1)
            # print(iout_nom_1)
        except: ireg1 = "NaN"

        try: vreg2 = self._sigfig(100*(vo2-vout_nom_2)/vo2, 2)
        except: vreg2 = "NaN"
        try: ireg2 = self._sigfig(100*(io2-(iout_nom_2*1000))/(iout_nom_2*1000), 3)
        except: ireg2 = "NaN"

        try: eff = self._sigfig(100*(po1+po2)/pin, 2)
        except: eff = "NaN"


        try: 
            total_po = po1 + po2
            total_po = self._sigfig(total_po, 2)
        except: total_po = "NaN"
                
        output_list = [vin, ac.set_freq(vin),
                       vac, iin, pin,
                       pf, thd,
                       vo1, io1, po1, ireg1,
                       vo2, io2, po2, vreg2,
                       total_po, eff]
        
        try:
            for channel in scope_channel_list:
                scope.stop()
                try:
                    labels, values = scope.get_measure(channel)
                    for i in range(len(values)):
                        output_list.append(self._sigfig(values[i], 2))
                except:
                    pass
        except:
            pass

        return output_list
    
    def COLLECT_DATA_1CV_1CC_PARAMETRICS_with_dimming(self, vin, vout_nom_1, vout_nom_2,
                             iout_nom_1, iout_nom_2, dim_freq, duty, scope_channel_list):

        vac, iin, pin, pf, thd, vo1, io1, po1 = self._pm_measurements()
        vo2, io2, po2 = self._pm_measurements2()

        try: vreg1 = self._sigfig(100*(vo1-vout_nom_1)/vo1, 2)
        except: vreg1 = "NaN"
        try: 
            ireg1 = self._sigfig(100*(io1-(iout_nom_1*1000))/(iout_nom_1*1000), 3)
            # print(io1)
            # print(iout_nom_1)
        except: ireg1 = "NaN"

        try: vreg2 = self._sigfig(100*(vo2-vout_nom_2)/vo2, 2)
        except: vreg2 = "NaN"
        try: ireg2 = self._sigfig(100*(io2-(iout_nom_2*1000))/(iout_nom_2*1000), 3)
        except: ireg2 = "NaN"

        try: eff = self._sigfig(100*(po1+po2)/pin, 2)
        except: eff = "NaN"

        try:
            total_po = po1 + po2
            total_po = self._sigfig(total_po, 2)
        except: total_po = "NaN"
        # try:
        #     labels, values = scope.get_measure(vds_channel)
        #     vds_max = values[0]
        # except:
        #     vds_max = 0

        # output_list = [vin, ac.set_freq(vin),
        #                vac, iin, pin,
        #                pf, thd,
        #                vo1, io1, po1, vreg1, ireg1,
        #                vo2, io2, po2, vreg2, ireg2,
        #                total_po, eff]
        
        output_list = [vin, ac.set_freq(vin),
                       vac, iin, pin,
                       pf, thd,
                       vo1, io1, po1, ireg1,
                       vo2, io2, po2, vreg2,
                       total_po, eff, dim_freq, duty]
        
        try:
            for channel in scope_channel_list:
                scope.stop()
                try:
                    labels, values = scope.get_measure(channel)
                    for i in range(len(values)):
                        output_list.append(self._sigfig(values[i], 2))
                except:
                    pass
        except:
            pass

        return output_list


    def COLLECT_DATA_1CC(self, vin, vout_nom_1,
                             iout_nom_1, vds_channel):

        vac, iin, pin, pf, thd, vo1, io1, po1 = self._pm_measurements()

        try: vreg1 = self._sigfig(100*(vo1-vout_nom_1)/vo1, 2)
        except: vreg1 = "NaN"
        try: ireg1 = self._sigfig(100*(io1-(iout_nom_1*1000))/(iout_nom_1*1000), 3)
        except: ireg1 = "NaN"

       
        try: eff = self._sigfig(100*(po1)/pin, 2)
        except: eff = "NaN"

        total_po = po1
        try:
            labels, values = scope.get_measure(vds_channel)
            vds_max = values[0]
        except:
            vds_max = 0

        output_list = [vin, ac.set_freq(vin),
                       vac, iin, pin,
                       pf, thd,
                       vo1, io1, po1, vreg1, ireg1,
                       total_po, eff, vds_max]

        return output_list

    def COLLECT_DATA_2CV_1CC(self, vin, vout_nom_1, vout_nom_2, vout_nom_3,
                             iout_nom_1, iout_nom_2, iout_nom_3, vds_channel, iled_channel):

        vac, iin, pin, pf, thd, vo1, io1, po1 = self._pm_measurements()
        vo2, io2, po2 = self._pm_measurements2()
        vo3, io3, po3 = self._pm_measurements3()

        try: vreg1 = self._sigfig(100*(vo1-vout_nom_1)/vo1, 2)
        except: vreg1 = "NaN"
        try: ireg1 = self._sigfig(100*(io1-(iout_nom_1*1000))/(iout_nom_1*1000), 3)
        except: ireg1 = "NaN"

        try: vreg2 = self._sigfig(100*(vo2-vout_nom_2)/vo2, 2)
        except: vreg2 = "NaN"
        try: ireg2 = self._sigfig(100*(io2-(iout_nom_2*1000))/(iout_nom_2*1000), 3)
        except: ireg2 = "NaN"

        try: vreg3 = self._sigfig(100*(vo3-vout_nom_3)/vo3, 2)
        except: vreg3 = "NaN"
        try: ireg3 = self._sigfig(100*(io3-(iout_nom_3*1000))/(iout_nom_3*1000), 3)
        except: ireg3 = "NaN"

        try: eff = self._sigfig(100*(po1+po2+po3)/pin, 2)
        except: eff = "NaN"

        total_po = po1 + po2 + po3 
        try:
            labels, values = scope.get_measure(vds_channel)
            vds_max = values[0]
        except:
            vds_max = 0

        try:
            labels, values = scope.get_measure(iled_channel)
            iled_mean = values[1]
            iled_pkpk = values[0]*1000
            iled_mean = io1

        except:
            iled_mean = 0
            iled_pkpk = 0

        output_list = [vin, ac.set_freq(vin),
                       vac, iin, pin,
                       pf, thd,
                       vo1, io1, po1, vreg1, ireg1,
                       vo2, io2, po2, vreg2, ireg2,
                       vo3, io3, po3, vreg3, ireg3,
                       total_po, eff, vds_max, iled_mean, iled_pkpk]

        return output_list
    
    def COLLECT_DATA_2CV_1CC_with_VDS_MAX(self, vin, vout_nom_1, vout_nom_2, vout_nom_3,
                             iout_nom_1, iout_nom_2, iout_nom_3, voltage_rating, scope_channel):

        vac, iin, pin, pf, thd, vo1, io1, po1 = self._pm_measurements()
        vo2, io2, po2 = self._pm_measurements2()
        vo3, io3, po3 = self._pm_measurements3()

        try: vreg1 = self._sigfig(100*(vo1-vout_nom_1)/vo1, 2)
        except: vreg1 = "NaN"
        try: ireg1 = self._sigfig(100*(io1-(iout_nom_1*1000))/(iout_nom_1*1000), 3)
        except: ireg1 = "NaN"

        try: vreg2 = self._sigfig(100*(vo2-vout_nom_2)/vo2, 2)
        except: vreg2 = "NaN"
        try: ireg2 = self._sigfig(100*(io2-(iout_nom_2*1000))/(iout_nom_2*1000), 3)
        except: ireg2 = "NaN"

        try: vreg3 = self._sigfig(100*(vo3-vout_nom_3)/vo3, 2)
        except: vreg3 = "NaN"
        try: ireg3 = self._sigfig(100*(io3-(iout_nom_3*1000))/(iout_nom_3*1000), 3)
        except: ireg3 = "NaN"

        try: eff = self._sigfig(100*(po1+po2+po3)/pin, 2)
        except: eff = "NaN"

        total_po = po1 + po2 + po3 
     
        vds_max = scope.get_measure_dict(scope_channel)['Max']

        derating = vds_max*100/voltage_rating

        try:
            vds_fsw = 1/(1000*scope.get_cursor(scope_channel)['delta x'])
        except:
            vds_fsw = 0


        output_list = [vin, ac.set_freq(vin),
                       vac, iin, pin,
                       pf, thd,
                       vo1, io1, po1, vreg1, ireg1,
                       vo2, io2, po2, vreg2, ireg2,
                       vo3, io3, po3, vreg3, ireg3,
                       total_po, eff, vds_max, derating, vds_fsw]

        return output_list
    
    def COLLECT_DATA_2CV_1CC_dimming(self, vin, vout_nom_1, vout_nom_2, vout_nom_3,
                             iout_nom_1, iout_nom_2, iout_nom_3, duty):

        vac, iin, pin, pf, thd, vo1, io1, po1 = self._pm_measurements()
        vo2, io2, po2 = self._pm_measurements2()
        vo3, io3, po3 = self._pm_measurements3()

        try: vreg1 = self._sigfig(100*(vo1-vout_nom_1)/vo1, 2)
        except: vreg1 = "NaN"
        try: ireg1 = self._sigfig(100*(io1-(iout_nom_1*1000))/(iout_nom_1*1000), 3)
        except: ireg1 = "NaN"

        try: vreg2 = self._sigfig(100*(vo2-vout_nom_2)/vo2, 2)
        except: vreg2 = "NaN"
        try: ireg2 = self._sigfig(100*(io2-(iout_nom_2*1000))/(iout_nom_2*1000), 3)
        except: ireg2 = "NaN"

        try: vreg3 = self._sigfig(100*(vo3-vout_nom_3)/vo3, 2)
        except: vreg3 = "NaN"
        try: ireg3 = self._sigfig(100*(io3-(iout_nom_3*1000))/(iout_nom_3*1000), 3)
        except: ireg3 = "NaN"

        try: eff = self._sigfig(100*(po1+po2+po3)/pin, 2)
        except: eff = "NaN"

        total_po = po1 + po2 + po3 

        output_list = [vin, ac.set_freq(vin),
                       vac, iin, pin,
                       pf, thd,
                       duty, vo1, io1, po1, vreg1, ireg1,
                       vo2, io2, po2, vreg2, ireg2,
                       vo3, io3, po3, vreg3, ireg3,
                       total_po, eff]

        return output_list
    

    def COLLECT_DATA_2CV_1CC_cross_reg(self, vin, vout_nom_1, vout_nom_2, vout_nom_3,
                             iout_nom_1, iout_nom_2, iout_nom_3, load_1, load_2, load_3):

        vac, iin, pin, pf, thd, vo1, io1, po1 = self._pm_measurements()
        vo2, io2, po2 = self._pm_measurements2()
        vo3, io3, po3 = self._pm_measurements3()

        try: vreg1 = self._sigfig(100*(vo1-vout_nom_1)/vo1, 2)
        except: vreg1 = "NaN"
        try: ireg1 = self._sigfig(100*(io1-(iout_nom_1*1000))/(iout_nom_1*1000), 3)
        except: ireg1 = "NaN"

        try: vreg2 = self._sigfig(100*(vo2-vout_nom_2)/vo2, 2)
        except: vreg2 = "NaN"
        try: ireg2 = self._sigfig(100*(io2-(iout_nom_2*1000))/(iout_nom_2*1000), 3)
        except: ireg2 = "NaN"

        try: vreg3 = self._sigfig(100*(vo3-vout_nom_3)/vo3, 2)
        except: vreg3 = "NaN"
        try: ireg3 = self._sigfig(100*(io3-(iout_nom_3*1000))/(iout_nom_3*1000), 3)
        except: ireg3 = "NaN"

        try: eff = self._sigfig(100*(po1+po2+po3)/pin, 2)
        except: eff = "NaN"

        output_list = [vin, ac.set_freq(vin),
                       vac, iin, pin,
                       pf, thd,
                       vo1, io1, load_1, po1, vreg1, ireg1,
                       vo2, io2, load_2, po2, vreg2, ireg2,
                       vo3, io3, load_3, po3, vreg3, ireg3,
                       eff]

        return output_list
    
    def COLLECT_DATA_2CV_1CC_cross_reg_ripple(self, vin, vout_nom_1, vout_nom_2, vout_nom_3,
                             iout_nom_1, iout_nom_2, iout_nom_3, load_1, load_2, load_3, scope_channel_list):

        try:
            vac, iin, pin, pf, thd, vo1, io1, po1 = self._pm_measurements()
            vo2, io2, po2 = self._pm_measurements2()
            vo3, io3, po3 = self._pm_measurements3()
        except:
            pass

        try: vreg1 = self._sigfig(100*(vo1-vout_nom_1)/vo1, 2)
        except: vreg1 = "NaN"
        try: ireg1 = self._sigfig(100*(io1-(iout_nom_1*1000))/(iout_nom_1*1000), 3)
        except: ireg1 = "NaN"

        try: vreg2 = self._sigfig(100*(vo2-vout_nom_2)/vo2, 2)
        except: vreg2 = "NaN"
        try: ireg2 = self._sigfig(100*(io2-(iout_nom_2*1000))/(iout_nom_2*1000), 3)
        except: ireg2 = "NaN"

        try: vreg3 = self._sigfig(100*(vo3-vout_nom_3)/vo3, 2)
        except: vreg3 = "NaN"
        try: ireg3 = self._sigfig(100*(io3-(iout_nom_3*1000))/(iout_nom_3*1000), 3)
        except: ireg3 = "NaN"

        try: eff = self._sigfig(100*(po1+po2+po3)/pin, 2)
        except: eff = "NaN"



        output_list = [vin, ac.set_freq(vin),
                       vac, iin, pin,
                       pf, thd,
                       vo1, io1, load_1, po1, vreg1, ireg1,
                       vo2, io2, load_2, po2, vreg2, ireg2,
                       vo3, io3, load_3, po3, vreg3, ireg3,
                       eff]
        
        # output_list = [vin, 1,
        #                1, 1, 1,
        #                1, 1,
        #                1, 1, 1, 1, 1, 1,
        #                1, 1, 1, 1, 1, 1,
        #                1, 1, 1, 1, 1, 1,
        #                1]
        
        #CV1 - 1
        #CV2 - 2
        #LED - 3
        try:
            for channel in scope_channel_list:
                scope.stop()
                try:
                    labels, values = scope.get_measure(channel)
                    for i in range(len(values)):
                        output_list.append(values[i]*1000)
                except:
                    pass
        except:
            pass

        return output_list
    
    def COLLECT_DATA_SINGLE_OUTPUT_LED_LOAD_RESISTOR_DIM(self, vin, led, iout, dim):

        vac, iin, pin, pf, thd, vo1, io1, po1 = self._pm_measurements()

        try: vreg1 = self._sigfig(100*(vo1-led)/vo1, 2)
        except: vreg1 = "NaN"

        try: ireg1 = self._sigfig(100*(io1-(iout*1000)/io1, 2))
        except: ireg1 = "NaN"

        try: eff = self._sigfig(100*po1/pin, 2)
        except: eff = "NaN"

        percent = self._sigfig(io1*100/iout, 0)

        output_list = [percent, dim, led, vin, ac.set_freq(vin), vac, iin, pin, pf, thd, vo1, io1, po1, vreg1, ireg1, eff]

        return output_list
    
    def COLLECT_DATA_SINGLE_OUTPUT_LED_LOAD_PWM_DIM(self, vin, led, iout, dim, dim_freq):

        vac, iin, pin, pf, thd, vo1, io1, po1 = self._pm_measurements()

        try: vreg1 = self._sigfig(100*(vo1-led)/vo1, 2)
        except: vreg1 = "NaN"

        try: ireg1 = self._sigfig(100*(io1-(iout*1000)/io1, 2))
        except: ireg1 = "NaN"

        try: eff = self._sigfig(100*po1/pin, 2)
        except: eff = "NaN"

        percent = self._sigfig(io1*100/iout, 0)

        output_list = [percent, dim, dim_freq, led, vin, ac.set_freq(vin), vac, iin, pin, pf, thd, vo1, io1, po1, vreg1, ireg1, eff]

        return output_list

    def COLLECT_DATA_SINGLE_OUTPUT_CV_LOAD(self, vin, vout, iout, cv):

        vac, iin, pin, pf, thd, vo1, io1, po1 = self._pm_measurements()

        try: vreg1 = self._sigfig(100*(vo1-vout)/vo1, 2)
        except: vreg1 = "NaN"

        try: ireg1 = self._sigfig(100*(io1-(iout))/io1, 2)
        except: ireg1 = "NaN"

        try: eff = self._sigfig(100*po1/pin, 2)
        except: eff = "NaN"

        output_list = [cv, vin, ac.set_freq(vin), vac, iin, pin, pf, thd, vo1, io1, po1, vreg1, ireg1, eff]

        return output_list

    def COLLECT_DATA_SCOPE_VDS_STRESS(self, channel):

        labels, values = scope.get_measure(channel)
        max_value = self._sigfig(values[0], 4)
        return max_value

    def SET_LED(self, led):
        led_ctrl.voltage(led)

    def main_battery_discharge(self, target_level=18.2):
        self.AC_TURN_OFF()

        vout = self.OUTPUT_VOLTAGE_POWER_METER()
        while (vout > target_level):
            
            for i in range(10, 2, -1):
                while (vout > target_level):
                    self.ELOAD_CC_ON(7, i)
                    print(f"Vbat = {vout:.2f} V, Iout = {i} A")
                    soak(2)
                    vout = self.OUTPUT_VOLTAGE_POWER_METER()
                self.ELOAD_OFF(7)
                soak(10)
                vout = self.OUTPUT_VOLTAGE_POWER_METER()

            soak(30)
            vout = self.OUTPUT_VOLTAGE_POWER_METER()

    def FIND_TRIGGER(self, channel, trigger_delta):

        # scope.edge_trigger(channel, 0, 'POS')

        # finding trigger level
        scope.run_single()
        scope.trigger_mode('AUTO')
        soak(1)
        scope.trigger_mode('NORM')
        

        # get initial peak-to-peak measurement value
        labels, values = scope.get_measure(channel)
        max_value = float(values[0])
        max_value = float(f"{max_value:.4f}")

        # set max_value as initial trigger level
        trigger_level = max_value
        scope.edge_trigger(channel, trigger_level, 'POS')

        # check if it triggered within 3 seconds
        scope.run_single()
        sleep(1)
        trigger_status = scope.trigger_status()
        # print(trigger_level)

        # increase trigger level until it reaches the maximum trigger level
        while (trigger_status == 1):
            trigger_level += trigger_delta
            scope.edge_trigger(channel, trigger_level, 'POS')
            scope.run_single()
            sleep(0.5)
            trigger_status = scope.trigger_status()

        # decrease trigger level below to get the maximum trigger possible
        trigger_level -= 1*trigger_delta
        scope.edge_trigger(channel, trigger_level, 'POS')
        sleep(6)


    

    def SWITCH_STATE(self, vout, iout, no_load_state):
        power = vout*iout
        
        if power > 5 and not no_load_state:
            no_load_state = False
        elif power > 5 and no_load_state:
            prompt(">> Change switch to EFFICIENCY MODE")
            no_load_state = False
        elif power <= 5 and not no_load_state:
            prompt(">> Change switch to NO LOAD/LIGHT LOAD MODE")
            no_load_state = True
        elif power <= 5 and no_load_state:
            no_load_state = True
        else:
            pass

        return no_load_state

class TEST(EQUIPMENT_FUNCTIONS):
    def NORMAL_OPERATION_CC_LOAD_SCOPE_CAPTURE(self, vin_list, vout, iout, percent_list, filename, waveforms_folder, trigger_channel, trigger_delta):

        df = GENERAL_FUNCTIONS().CREATE_DF_WITH_HEADER(GENERAL_CONSTANTS.HEADER_LIST_CC_LOAD_VDS_STRESS)

        cc_list = [(iout*percent/100 if percent != 0 else 0) for percent in percent_list]
        self.DISCHARGE_OUTPUT(1)


        for vin in vin_list:
            for cc in cc_list:
                # TURN ON E-LOAD
                percent = cc*100/iout
                if cc != 0: self.ELOAD_CC_ON(EQUIPMENT_ADDRESS.ELOAD_CHANNEL, cc)
                else: self.ELOAD_OFF(EQUIPMENT_ADDRESS.ELOAD_CHANNEL)

                # RUN SCOPE
                scope.run()
                soak(2)

                # TURN ON AC SOURCE
                self.AC_TURN_ON(vin)
                soak(3)

                # RUN SCOPE
                self.FIND_TRIGGER(trigger_channel, trigger_delta)
                scope.run_single()
                soak(3)
                scope.stop()

                output_list = EQUIPMENT_FUNCTIONS().COLLECT_DATA_SINGLE_OUTPUT_CC_LOAD(vin, vout, cc)
                output_list.append(EQUIPMENT_FUNCTIONS().COLLECT_DATA_SCOPE_VDS_STRESS(trigger_channel))
                excel_name = f"{vout}V, {filename}"
                export_to_excel(df, waveforms_folder, output_list, excel_name=excel_name, sheet_name=excel_name, anchor="B2")
                print(output_list)

                # SAVE SCREENSHOT
                self.SCOPE().SCOPE_SCREENSHOT(f"{filename}, {vin}Vac, {vout}V, {cc}A ({percent}%) Load", waveforms_folder)
        self.DISCHARGE_OUTPUT(4)