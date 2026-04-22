import json

# def hex_to_binary(hex_str):
#     hex_str = hex_str.lstrip("0x")
#     binary_str = bin(int(hex_str, 16))[2:]
#     binary_str = binary_str.zfill(len(hex_str) * 4)
#     return binary_str
# hex_code_trim = "000F02612D030000000001E0E636CD86140000000000"

# # Convert to binary
# binary_result = hex_to_binary(hex_code_trim)
# print(binary_result)

binary_trim_code_string = "00000000000011110000001001100001001011010000001100000000000000000000000000000000000000011110000011100110001101101100110110000110000101000000000000000000000000000000000000000000"
trim_code = binary_trim_code_string[:160]

size_list = [5, 3, 2, 2, 3, 1, 5, 3, 10, 10, 11, 1, 1,
             1, 1, 1, 2, 2, 1, 3, 2, 2, 1, 1, 1, 1, 1, 3, 2, 2, 2, 1, 1, 2, 1, 1, 1, 1, 3,
             3, 3, 1, 8, 5, 5, 2, 2, 2, 2, 4, 1, 1, 2, 2, 2, 1, 1, 1, 4, 3, 8]

parameter_name_list = ["trim_iref", "trim_vref", "trim_bias", "trim_clk", "unused", "trim_led_range", "trim_led_offset", "trim_fb_cap", "trim_fb_cv1", "trim_fb_cv2", "trim_fb_led", "sr_zvs_en", "inno4_pri",
             "cv3_en", "cv2_en", "sr_en", "drv_refresh_sel", "startup_ramp_sel", "warmstart_dch_en", "fwd_peak_adv", "ccm_sel", "top_turnoff_sel", "pulse_sharing_en", "holdoff_en", "shunt_en", "shut_down_sig_en", "latchoff_en", "led_reg_min_sel", "led_reg_rng_sel", "led_reg_gain_sel", "led_dim_mode", "dim2_en", "pwm_stretch_en", "pwm_min_sel", "led_short_det_en", "led_fault_en", "led_doze_en", "i2c_addr_sel", "avg_freq_lim_1",
             "avg_freq_lim_2", "avg_freq_lim_3", "dopl_mode", "ops_byte", "trim_lv_shunt", "trim_hv_shunt", "fb_az_sel", "vesr_cv_r_gain", "vesr_led_i_gain", "led_shr_sel", "mm_debug_sel", "ext_fb_en", "sr_detect_en", "vesr_led_r_gain", "cv_shr_sel", "req_filt_sel", "bps_dpm_en", "bps_dpm_latch", "uvcc_reg_en", "trim_led_gain", "unused2", "spare_out"]




parameters = {}
initial_length = 160
for idx, size in enumerate(size_list):
    parameters[parameter_name_list[idx]] = trim_code[-size:]
    initial_length = initial_length - size
    trim_code = trim_code[:initial_length]

# print(parameters)

parameter_pretty = json.dumps(parameters, indent=4)
print()
print(parameter_pretty)