# @cfcayno
from powi.equipment import ACSource, PowerMeter, ElectronicLoad, Oscilloscope, truncate
from time import sleep, time

# USER INPUT STARTS HERE
#########################################################################################
ac_source_address = 5
source_power_meter_address = 1
load_power_meter_address = 2
eload_address = 8
eload_channel = 1

scope_address_2 = '10.125.10.139' #portA
scope_address_1 = '10.125.11.20' #portB

# trigger settings
trigger_level = 3       # A
trigger_source = 2            # channel

# INPUT
voltages = [100,132]
frequencies = [60,60]

# OUTPUT
# port A (45W)
Vo1 = [20]
Imax1 = [2.25]
Po1 = 45
current_name_1 = [100]

# Vo1 = [9]
# Imax1 = [3]

# port B (20W)
Vo2 = [5, 9, 12, 15, 20]
Imax2 = [3, 2.22, 1.66, 1.33, 1]
Po2 = 20
current_name_2 = [100]

# 65W Configuration at Port B
Vo3 = [5, 9, 12, 15, 20]
Imax3 = [3, 3, 3, 3, 3.25]


waveforms_folder = 'waveforms/SR FET Normal Operation'

print()
print('SR FET Normal Operation:')
#########################################################################################
# USER INPUT ENDS HERE

start = time()

# Equipment Address
ac = ACSource(ac_source_address)
pms = PowerMeter(source_power_meter_address)
pml = PowerMeter(load_power_meter_address)
eload = ElectronicLoad(eload_address)
scope1 = Oscilloscope(scope_address_1)
scope2 = Oscilloscope(scope_address_2)

# Trigger Settings
scope1.edge_trigger(trigger_source=trigger_source, trigger_level=trigger_level, trigger_slope='POS')
scope1.trigger_mode(mode='NORM')
scope2.edge_trigger(trigger_source=trigger_source, trigger_level=trigger_level, trigger_slope='POS')
scope2.trigger_mode(mode='NORM')

# initialization
waveform_counter = 0
current_index_1 = 0
current_index_2 = 0

def config60W():

    global waveform_counter

    # for 60W configuration
    port = input("Enter Port to capture...")
    if port == 'A':
      input('Remove Port B connection.')
    if port == 'B':
      input('Remove Port A connection.')

    for vout3, iout3 in zip(Vo3, Imax3):
      print('='*80)
      print(f'Vin = {voltage}Vac')
      print('='*80)
            
      input(f'Set Port {port} to >>> {vout3}V')
      print(f'{port}: {vout3}V {iout3}A')

      if port == 'A':
        eload.channel[3].cc = iout3
        eload.channel[3].turn_on()
      if port == 'B':
        eload.channel[1].cc = iout3
        eload.channel[1].turn_on()

      sleep(5)
      
      if port == 'A':
        waveforms_folder = 'waveforms/SR FET Normal Operation/A 65W B 0W'

        scope1.run_single()
        scope2.run_single()
        input("Press ENTER to capture...")
        # sleep(6)
        
        scope1.get_screenshot(filename=f'{voltage}Vac___A [65W] {vout3}V {iout3}A 100Load___B [0W]___PortA.png', path=f'{waveforms_folder}')
        print(f'{voltage}Vac___A [65W] {vout3}V {iout3}A 100Load___B [0W]___PortA.png')
        waveform_counter = waveform_counter + 1
        scope2.get_screenshot(filename=f'{voltage}Vac___A [65W] {vout3}V {iout3}A 100Load___B [0W]___PortB.png', path=f'{waveforms_folder}')
        print(f'{voltage}Vac___A [65W] {vout3}V {iout3}A100Load___B [0W]___PortB.png')
        waveform_counter = waveform_counter + 1

      if port == 'B':
        waveforms_folder = 'waveforms/SR FET Normal Operation/A 0W B 65W'

        scope1.run_single()
        scope2.run_single()
        input("Press ENTER to capture...")
        # sleep(6)

        scope1.get_screenshot(filename=f'{voltage}Vac___A [0W]___B [65W] {vout3}V {iout3}A 100Load___PortA.png', path=f'{waveforms_folder}')
        print(f'{voltage}Vac___A [0W]___B [65W] {vout3}V {iout3}A 100Load___PortA.png')
        waveform_counter = waveform_counter + 1
        scope2.get_screenshot(filename=f'{voltage}Vac___A [0W]___B [65W] {vout3}V {iout3}A 100Load___PortB.png', path=f'{waveforms_folder}')
        print(f'{voltage}Vac___A [0W]___B [65W] {vout3}V {iout3}A 100Load___PortB.png')
        waveform_counter = waveform_counter + 1


      # eload.channel[1].turn_off()
      # eload.channel[3].turn_off()

      print()

def config45W20W():

  global waveform_counter

  for vout1, iout1 in zip(Vo1, Imax1):
    print('='*80)
    print(f'Vin = {voltage}Vac')

    print('='*80)
    input(f'Set Port A to >>> {vout1}V')
    print(f'A: {vout1}V {iout1}A')
    eload.channel[3].cc = iout1
    eload.channel[3].turn_on()

    for vout2, iout2 in zip(Vo2, Imax2):
      print()
      input(f'Set Port B to >>> {vout2}V')
      print(f'B: {vout2}V {iout2}A')
      print()
      

      eload.channel[1].cc = iout2
      eload.channel[1].turn_on()
      sleep(5)

      # get screenshot
      scope1.run_single()
      scope2.run_single()
      
      input("Press ENTER to capture...")
      # sleep(6)
      # 100Vac__A [45W] 20V 2.25A (100Load)___B [20W] 5V 3A (100Load).png
      scope1.get_screenshot(filename=f'{voltage}Vac___A [{Po1}W] {vout1}V {iout1}A ({current_name_1[0]}Load)___B [{Po2}W] {vout2}V {iout2}A ({current_name_2[0]}Load)___PortA.png', path=f'{waveforms_folder}')
      print(f'{voltage}Vac___A [{Po1}W] {vout1}V {iout1}A ({current_name_1[0]}Load)___B [{Po2}W] {vout2}V {iout2}A ({current_name_2[0]}Load)___PortA.png')
      waveform_counter = waveform_counter + 1
      # sleep(1)
      scope2.get_screenshot(filename=f'{voltage}Vac___A [{Po1}W] {vout1}V {iout1}A ({current_name_1[0]}Load)___B [{Po2}W] {vout2}V {iout2}A ({current_name_2[0]}Load)___PortB.png', path=f'{waveforms_folder}')
      print(f'{voltage}Vac___A [{Po1}W] {vout1}V {iout1}A ({current_name_1[0]}Load)___B [{Po2}W] {vout2}V {iout2}A ({current_name_2[0]}Load)___PortB.png')
      waveform_counter = waveform_counter + 1
      # current_index_1 = current_index_1 + 1
      # current_index_2 = current_index_2 + 1
      
      print('='*80)
      eload.channel[eload_channel].turn_off()


def footers(waveform_counter=0, time=0):
  ac.turn_off()
  eload.channel[1].turn_off()
  eload.channel[3].turn_off()
  print(f'{waveform_counter} waveforms captured.')
  print('test complete.')  
  print()
  print(f'test time: {(end-start)/60} mins.')

















# main code
for voltage, frequency in zip(voltages, frequencies):
  
  ac.voltage = voltage
  ac.frequency = frequency
  ac.turn_on()
  eload.channel[1].turn_off()
  eload.channel[3].turn_off()
  
  config45W20W()
  # config60W()

end = time()
footers(waveform_counter, end-start)
