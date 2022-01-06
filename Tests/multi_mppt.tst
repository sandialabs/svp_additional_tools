<scriptConfig name="multi_mppt" script="multi_mppt_analysis">
  <params>
    <param name="das.opal.sample_interval" type="int">0</param>
    <param name="pvsim_1.terrasas.channel" type="string">1</param>
    <param name="pvsim_2.terrasas.channel" type="string">2</param>
    <param name="pvsim_3.terrasas.channel" type="string">3</param>
    <param name="pvsim_4.terrasas.channel" type="string">4</param>
    <param name="pvsim_5.terrasas.channel" type="string">5</param>
    <param name="test.n_pv" type="int">6</param>
    <param name="pvsim_6.terrasas.channel" type="string">6</param>
    <param name="test.n_meas" type="int">12</param>
    <param name="pvsim_1.terrasas.ipaddr" type="string">192.168.0.167</param>
    <param name="pvsim_2.terrasas.ipaddr" type="string">192.168.0.167</param>
    <param name="pvsim_3.terrasas.ipaddr" type="string">192.168.0.167</param>
    <param name="pvsim_4.terrasas.ipaddr" type="string">192.168.0.167</param>
    <param name="pvsim_5.terrasas.ipaddr" type="string">192.168.0.167</param>
    <param name="pvsim_6.terrasas.ipaddr" type="string">192.168.0.167</param>
    <param name="pvsim_1.terrasas.vmp" type="float">600.0</param>
    <param name="pvsim_2.terrasas.vmp" type="float">600.0</param>
    <param name="pvsim_3.terrasas.vmp" type="float">600.0</param>
    <param name="pvsim_4.terrasas.vmp" type="float">600.0</param>
    <param name="pvsim_5.terrasas.vmp" type="float">600.0</param>
    <param name="pvsim_6.terrasas.vmp" type="float">600.0</param>
    <param name="pvsim_1.terrasas.overvoltage" type="float">1000.0</param>
    <param name="pvsim_2.terrasas.overvoltage" type="float">1000.0</param>
    <param name="pvsim_3.terrasas.overvoltage" type="float">1000.0</param>
    <param name="pvsim_4.terrasas.overvoltage" type="float">1000.0</param>
    <param name="pvsim_5.terrasas.overvoltage" type="float">1000.0</param>
    <param name="pvsim_6.terrasas.overvoltage" type="float">1000.0</param>
    <param name="pvsim_1.terrasas.pmp" type="float">5500.0</param>
    <param name="pvsim_2.terrasas.pmp" type="float">5500.0</param>
    <param name="pvsim_3.terrasas.pmp" type="float">5500.0</param>
    <param name="pvsim_4.terrasas.pmp" type="float">5500.0</param>
    <param name="pvsim_5.terrasas.pmp" type="float">5500.0</param>
    <param name="pvsim_6.terrasas.pmp" type="float">5500.0</param>
    <param name="test.p_max" type="float">33000.0</param>
    <param name="hil.opal.hil_stop_time" type="float">80000.0</param>
    <param name="hil.opal.workspace_path" type="string">C:\Users\DETLDAQ\OPAL-RT/RT-LABv2020.4_Workspace</param>
    <param name="das.opal.wfm_dir" type="string">C:\Users\DETLDAQ\OPAL-RT\RT-LABv2020.4_Workspace\CoreONE_Test\models\CoreONE_Test\coreone_test_sm_source\OpREDHAWKtarget</param>
    <param name="hil.opal.project_dir" type="string">CoreONE_Test</param>
    <param name="hil.opal.rt_lab_model" type="string">CoreONE_Test</param>
    <param name="hil.opal.project_name" type="string">CoreONE_Test.llp</param>
    <param name="der.mode" type="string">Disabled</param>
    <param name="pvsim_1.terrasas.curve_type" type="string">EN50530</param>
    <param name="pvsim_2.terrasas.curve_type" type="string">EN50530</param>
    <param name="pvsim_3.terrasas.curve_type" type="string">EN50530</param>
    <param name="pvsim_4.terrasas.curve_type" type="string">EN50530</param>
    <param name="pvsim_5.terrasas.curve_type" type="string">EN50530</param>
    <param name="pvsim_6.terrasas.curve_type" type="string">EN50530</param>
    <param name="hil.opal.hil_config" type="string">False</param>
    <param name="hil.opal.hil_config_compile" type="string">No</param>
    <param name="das.mode" type="string">Opal</param>
    <param name="hil.mode" type="string">Opal-RT</param>
    <param name="das.opal.map" type="string">Opal_Phase_Jump</param>
    <param name="das.opal.wfm_chan_list" type="string">PhaseJump</param>
    <param name="das.opal.data_name" type="string">SVP_Data.mat</param>
    <param name="hil.opal.target_name" type="string">Target_3</param>
    <param name="pvsim_1.mode" type="string">TerraSAS</param>
    <param name="pvsim_2.mode" type="string">TerraSAS</param>
    <param name="pvsim_3.mode" type="string">TerraSAS</param>
    <param name="pvsim_4.mode" type="string">TerraSAS</param>
    <param name="pvsim_5.mode" type="string">TerraSAS</param>
    <param name="pvsim_6.mode" type="string">TerraSAS</param>
    <param name="hil.opal.hil_config_open" type="string">Yes</param>
    <param name="hil.opal.hil_config_stop_sim" type="string">Yes</param>
    <param name="hil.opal.hil_config_load" type="string">Yes</param>
    <param name="hil.opal.hil_config_execute" type="string">Yes</param>
  </params>
</scriptConfig>
