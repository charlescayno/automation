##################################################################################
"""IMPORT DEPENDENCIES"""
from time import sleep
from powi.equipment import ACSource, PowerMeter, ElectronicLoad, Oscilloscope, LecroyScope, LEDControl, Keithley_DC_2230G, RnS_DC_HMPSeries
from powi.equipment import headers, create_folder, footers, waveform_counter, soak, convert_argv_to_int_list, tts, prompt, roundup
from misc_codes.equipment_address import *
from misc_codes.general_settings import *
from itertools import permutations
##################################################################################

ac = ACSource(EQUIPMENT_ADDRESS.AC_SOURCE)
pms = PowerMeter(EQUIPMENT_ADDRESS.POWER_METER_SOURCE)
pml = PowerMeter(EQUIPMENT_ADDRESS.POWER_METER_LOAD_1)
pml2 = PowerMeter(EQUIPMENT_ADDRESS.POWER_METER_LOAD_2)
pml3 = PowerMeter(EQUIPMENT_ADDRESS.POWER_METER_LOAD_3)
# pml4 = PowerMeter(EQUIPMENT_ADDRESS.POWER_METER_LOAD_4)
eload = ElectronicLoad(EQUIPMENT_ADDRESS.ELOAD)
dimmer = RnS_DC_HMPSeries(EQUIPMENT_ADDRESS.DC_SOURCE_DIMMER)

# try: 
#     ac = ACSource(EQUIPMENT_ADDRESS.AC_SOURCE)
#     pms = PowerMeter(EQUIPMENT_ADDRESS.POWER_METER_SOURCE)
#     pml = PowerMeter(EQUIPMENT_ADDRESS.POWER_METER_LOAD_1)
#     pml2 = PowerMeter(EQUIPMENT_ADDRESS.POWER_METER_LOAD_2)
#     pml3 = PowerMeter(EQUIPMENT_ADDRESS.POWER_METER_LOAD_3)
#     pml4 = PowerMeter(EQUIPMENT_ADDRESS.POWER_METER_LOAD_4)
#     eload = ElectronicLoad(EQUIPMENT_ADDRESS.ELOAD)
    
# except:
#     pass

try: scope = Oscilloscope(EQUIPMENT_ADDRESS.SCOPE)
except: pass

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

    def ANALOG_DC_ON(self, channel, voltage, current):
        dimmer.set_volt_curr(channel, voltage, current)
        dimmer.channel_state(self, channel, 'ON')

    
    def ANALOG_DC_OFF(self):
        dimmer.channel_state_all('OFF')


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

        def TIME_SCALE(self, time_scale):
            """
            Parameters:
            <TimeScale> Range: 25E-12 to 50
                        Increment: 1E-12
                        *RST: 10E-9
                        Default unit: s/div
            """
            scope.time_scale(time_scale)

        def CHANNEL_SCALE(self, channel, channel_scale):
            scope.channel_scale(channel, channel_scale)

        def CHANNEL_POSITION(self, channel, channel_position):
            scope.channel_position(channel, channel_position)

        def EDGE_TRIGGER(self, trigger_channel, trigger_level, trigger_edge):
            scope.edge_trigger(trigger_channel, trigger_level, trigger_edge)

    def ELOAD_CR_ON(self, channel, cr_load, von):
        eload.channel[channel].von = von
        eload.channel[channel].cr = cr_load
        eload.channel[channel].turn_on()

    def ELOAD_CC_ON(self, channel, cc_load):
        eload.channel[channel].cc = cc_load
        eload.channel[channel].turn_on()
    
    def ELOAD_CV_ON(self, channel, cv):
        eload.channel[channel].cv = cv
        eload.channel[channel].turn_on()

    def ELOAD_OFF(self, channel):
        eload.channel[channel].turn_off()
    
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
                eload.channel[i].cr = 100
                # eload.channel[i].short_on()
                eload.channel[i].turn_on()
            sleep(0.5)

            for i in range(1,9):
                eload.channel[i].turn_off()
                # eload.channel[i].short_off()
            sleep(0.5)

    def _sigfig(self, number, sigfig):
        try: a = float(f"{number:.{sigfig}f}")
        except: a = "NaN"
        return a

    def _pm_measurements(self):

        vac = self._sigfig(pms.voltage, 6)
        iin = self._sigfig(pms.current, 10)*1000
        pin = self._sigfig(pms.power, 6)
        pf = self._sigfig(pms.pf, 6)
        thd = self._sigfig(pms.thd, 6)
        vo1 = self._sigfig(pml.voltage, 6)
        io1 = self._sigfig(pml.current, 6)*1000
        po1 = self._sigfig(pml.power, 6)
        
        return vac, iin, pin, pf, thd, vo1, io1, po1
    
    def _pm_measurements2(self):
        vo2 = self._sigfig(pml2.voltage, 6)
        io2 = self._sigfig(pml2.current, 6)*1000
        po2 = self._sigfig(pml2.power, 6)
        
        return vo2, io2, po2

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

        return output_list
    
    def COLLECT_DATA_SINGLE_OUTPUT_CC_LOAD_1_PDEL(self, vin, vout, cc, percent):

        vac, iin, pin, pf, thd, vo1, io1, po1 = self._pm_measurements()

        try: vreg1 = self._sigfig(100*(vo1-vout)/vo1, 6)
        except: vreg1 = "NaN"

        try: ireg1 = self._sigfig(100*(io1-(cc*1000))/io1, 6)
        except: ireg1 = "NaN"

        try: eff = self._sigfig(100*po1/pin, 6)
        except: eff = "NaN"

        # scope_measurement = scope.get_measure_dict(1)
        # pkpk = EQUIPMENT_FUNCTIONS()._sigfig(scope_measurement['Peak to peak'], 4)
        pkpk = 0

        output_list = [percent, vin, ac.set_freq(vin), vac, iin, pin, pf, thd, vo1, io1, po1, vreg1, eff, pkpk]

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
            label = f"{scope.query_channel_label(channel)} {labels[i]}"
            # label = f"CH{(channel)} {labels[i]}"

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
    
    def COLLECT_DATA_SINGLE_OUTPUT_LED_LOAD_DIM(self, vin, led, iout, dim, percent):

        vac, iin, pin, pf, thd, vo1, io1, po1 = self._pm_measurements()

        try: vreg1 = self._sigfig(100*(vo1-led)/vo1, 2)
        except: vreg1 = "NaN"

        try: ireg1 = self._sigfig(100*(io1-(iout*1000)/io1, 2))
        except: ireg1 = "NaN"

        try: eff = self._sigfig(100*po1/pin, 2)
        except: eff = "NaN"

        output_list = [percent, dim, led, vin, ac.set_freq(vin), vac, iin, pin, pf, thd, vo1, io1, po1, vreg1, ireg1, eff]

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
        soak(3)
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

            # check trigger status
            scope.run_single()
            sleep(0.5)
            trigger_status = scope.trigger_status()

            # # get initial peak-to-peak measurement value
            # labels, values = scope.get_measure(channel)
            # max_value = float(values[0])
            # max_value = float(f"{max_value:.4f}")

            # # set max_value as initial trigger level
            # trigger_level = max_value
            # scope.edge_trigger(channel, trigger_level, 'POS')



        # decrease trigger level below to get the maximum trigger possible
        trigger_level -= 1*trigger_delta
        scope.edge_trigger(channel, trigger_level, 'POS')
        sleep(6)
        # trigger_status = scope.trigger_status()
        # while (trigger_status != 1):
        #     # decrease trigger level below to get the maximum trigger possible
        #     trigger_level -= 1*trigger_delta
        #     scope.edge_trigger(channel, trigger_level, 'POS')

        #     # check trigger status
        #     scope.run_single()
        #     soak(3)
        #     trigger_status = scope.trigger_status()

    

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