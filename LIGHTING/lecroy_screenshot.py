import pyvisa
import time
import math

#Eload chan 3,
#input PM GPIB2,
#output PM GPIB1,
#Chroma AC source ac_source.write("SOUR:VOLT:LEV:DC %s" %(acs))
#CRL max value=5000 ohms
#Please include additional soak time

def main():
    

    # z = [412,393,373,314] #Line Voltages
    # #conditions = [20] #knee voltages
    # # Vstart = float(raw_input("Enter start up voltage in (Vdc): "))
    # full_load = float(input("Enter full load in Amps: "))
    # load_increment_pct = float(raw_input("Enter increment of load in (%): "))
    # load_increment= full_load*load_increment_pct/100
    # load = 0
    # soak_time = float(input("Enter time interval per load condition in (sec): "))

#Equipment initialization
    rm = pyvisa.ResourceManager()
    # dc_source = rm.open_resource("GPIB0::10::INSTR")
    # eload = rm.open_resource("GPIB0::8::INSTR")
    # input_pm = rm.open_resource("GPIB0::2::INSTR")
    # output_pm = rm.open_resource("GPIB0::1::INSTR")
    scope = rm.open_resource("TCPIP::169.254.94.235::INSTR")
    print("hello")

    
    
    
# #Power meter settings
#     input_pm.write("*RST")
#     input_pm.write(":INPUT:VOLTAGE:AUTO ON")
#     input_pm.write(":INPUT:CURRENT:AUTO ON")
#     input_pm.write(":MEASURE:AVERAGING:TYPE LINEAR")
#     input_pm.write(":MEASURE:AVERAGING:COUNT 8")
#     input_pm.write(":MEASURE:AVERAGING:STATE ON")
#     input_pm.write(":INPUT:MODE RMS")
#     input_pm.write(":NUMERIC:FORMAT ASCII")
#     input_pm.write(":NUMERIC:NORMAL:ITEM1 U,1")
#     input_pm.write(":NUMERIC:NORMAL:ITEM2 I,1")
#     input_pm.write(":NUMERIC:NORMAL:ITEM3 P,1")
#     input_pm.write(":NUMERIC:NORMAL:ITEM4 LAMBDA,1")
#     input_pm.write(":NUMERIC:NORMAL:ITEM5 ITHD,1")

#     output_pm.write("*RST")
#     output_pm.write(":INPUT:VOLTAGE:AUTO ON")
#     output_pm.write(":INPUT:CURRENT:AUTO ON")
#     output_pm.write(":MEASURE:AVERAGING:TYPE LINEAR")
#     output_pm.write(":MEASURE:AVERAGING:COUNT 8")
#     output_pm.write(":MEASURE:AVERAGING:STATE ON")
#     output_pm.write(":INPUT:MODE DC")
#     output_pm.write(":NUMERIC:FORMAT ASCII")
#     output_pm.write(":NUMERIC:NORMAL:ITEM1 U,1")
#     output_pm.write(":NUMERIC:NORMAL:ITEM2 I,1")
#     output_pm.write(":NUMERIC:NORMAL:ITEM3 P,1")
#     output_pm.write(":NUMERIC:NORMAL:ITEM4 LAMBDA,1")

#Scope Setting
    scope.write("C1:TRACE OFF") 
    scope.write("C2:TRACE OFF")
    scope.write("C3:TRACE OFF")
    scope.write("C4:TRACE ON")
    scope.write("Z4:TRACE ON")

    scope.write("C4:COUPLING A1M")
    scope.write("C4:VOLT_DIV 200mV")
    scope.write("Z4:VOLT_DIV 200m")
    scope.write("C4:OFFSET 0V")
    scope.write("TIME_DIV 5mS")
    scope.write("PARM CUST")
    scope.write("TRMD AUTO")
    scope.write("PACU 7,PKPK,C4")
    scope.write("GRID DUAL")
    scope.write("Z4:HOR_MAGNIFY 250")
    scope.write("HOFacR_POSITION 5")
    scope.write("TRSE EDGE,SR,C4,HT,OFF")
    scope.write("C4:TRSL POS")

    scope.write("HCSU DEV, JPEG, AREA, DSOWINDOW, PORT, NET")
    scope.write("SCDP")
    screen_data = scope.read_raw()
    filename = ("C:/Users/ccayno/Downloads/hello.jpg")
    g = open(filename,'wb+')
    g.write(screen_data)
    g.close

# #Eload setting
#     eload.write("*RST")
#     eload.write("CHAN 3")
#     eload.write("CHAN:ACT 1")
#     eload.write("MODE CCH")
#     eload.write("CURR:STAT:L1 %s" %(load_increment))
    

# #Eload ON
#     eload.write("LOAD ON")

#     time.sleep(2)

# #DC ON
#     dc_source.write("SOUR:VOLT %s" %(Vstart))
#     dc_source.write("CONF:OUTP ON")

        
#     f = open("PFS_Ripple.csv", "w")

# #Printing of headers
#     headers = ["Vin", "Iin", "PF", "Vout", "Iout","Pout","Efficiency", "Avg Ripple_pkpk(V)", "\n"]
#     f.write(",".join(headers))
#     print "\n", "============================  START  ============================", "\n"
#     print "Vin", "     Iin", "      PF", "    Vout", "    Iout", "  Pout", "    Eff", "    Avg Ripple_pkpk(V)"
    

# #Load Increment with Power measurement

    # ######### line voltage iteration##########

    # for x in z:
    #     Vin=x

            
    #     dc_source.write("SOUR:VOLT %s" %(Vin))
    #     time.sleep(2)

    #     load = 0

    #     #############load increment###############
    #     while load < full_load:
    #         load = load + load_increment
    #         eload.write("CURR:STAT:L1 %s" %(load))
            
            
    # #soak time
    #         scope.write("CLEAR_SWEEPS")
    #         scope.write("TRMD AUTO")
    #         time.sleep(soak_time)

    #         input_pm.write("HOLD ON")
    #         output_pm.write("HOLD ON")

    #         input_voltage = float(input_pm.query("NUM:NORM:VAL? 1").strip())
    #         ####### nan check##########################
    #         while (1):
    #                 if math.isnan (input_voltage):
    #                     input_pm.write("HOLD OFF")
    #                     time.sleep(0.5)
    #                     input_pm.write("HOLD ON")
    #                     input_voltage = float(input_pm.query("NUM:NORM:VAL? 1").strip())
    #                 else:
    #                     break
    #         ####### nan check##############################
    #         input_current = float(input_pm.query("NUM:NORM:VAL? 2").strip())
    #         pf = float(input_pm.query("NUM:NORM:VAL? 4").strip())
    #         output_voltage = float(output_pm.query("NUM:NORM:VAL? 1").strip())
    #         ####### nan check##########################
    #         while (1):
    #                 if math.isnan (output_voltage):
    #                     output_pm.write("HOLD OFF")
    #                     time.sleep(0.5)
    #                     output_pm.write("HOLD ON")
    #                     output_voltage = float(output_pm.query("NUM:NORM:VAL? 1").strip())
    #                 else:
    #                     break
    #         ####### nan check##############################
    #         output_current = float(output_pm.query("NUM:NORM:VAL? 2").strip())
    #         pout = output_voltage*output_current
            

    #         scope.write("TRMD STOP")
    #         time.sleep(2)
    #         ripple_ave = float(scope.query("PARAMETER_STATISTICS? CUST, P7").replace(" V","").split("AVG,",1)[1].split(",")[0])
            
          
                       
            

#     #Formulas:
            
#             efficiency = (pout)*100/(input_voltage*input_current*pf)

            
            
#     #printing of measured values
            

#             row = [input_voltage, input_current, pf, output_voltage, output_current, pout, efficiency,ripple_ave, "\n"]
#             row = [str(r) for r in row]
#             f.write(",".join(row))
#             print "%.2f" %input_voltage, " |", "%.2f" %input_current," |", "%.2f" %pf,"|", "%.2f" %output_voltage," |", "%.2f" %output_current," |", "%.2f" %pout," |", "%.2f" %efficiency, " |", "%.2f" %ripple_ave

#             input_pm.write("HOLD OFF")
#             output_pm.write("HOLD OFF")
        
        
# #DC source off
#     dc_source.write("CONF:OUTP OFF")
#     #eload.write("CURR:STAT:L1 %s" %(full_load))
#     time.sleep(5)

#     #ac_source.write("*RST")
#     input_pm.write("*RST")
#     eload.write("*RST")
#     output_pm.write("*RST")
    
#     dc_source.close()
#     eload.close()
#     input_pm.close()
#     output_pm.close()

    
#     f.close()


#     print "\n", "=============================  END  =============================", "\n"


if __name__ == "__main__":
    main()


