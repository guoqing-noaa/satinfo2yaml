# yaml_finalize 
This tool will read [**satinfo**](https://github.com/guoqing-noaa/satinfo2yaml/blob/main/satinfo) to get the `channels`, `use_flag`, `use_flag_cld_det`, `error`, `obserr_bound_max` etc values for each SIS and then automatically replace the corresponding anchors in the JEDI configuration YAML files.

##### 1. Set up correct anchors in a YAML file    
The anchors should be placed between `obs space.name` and `obs space.distribution`. Here is an example:
```
     - obs space:
         name: cris-fsr_n20 
         _anchor_channels: &cris-fsr_n20_channels 1
         _anchor_use_flag: &cris-fsr_n20_use_flag [1]
         _anchor_use_flag_clddet: &cris-fsr_n20_use_flag_clddet [1]
         _anchor_error: &cris-fsr_n20_error [1]
         _anchor_obserr_bound_max: &cris-fsr_n20_obserr_bound_max [1]
         distribution:
           name: "RoundRobin"
           halo size: 100e3
```
You can check [cris-fsr_n20.yaml](https://github.com/guoqing-noaa/satinfo2yaml/blob/main/cris-fsr_n20.yaml#L73-L79) or [cris-fsr_n20_finalized.yaml](https://github.com/guoqing-noaa/satinfo2yaml/blob/main/cris-fsr_n20_finalized.yaml#L73-L189)    
Rules:   
- (1) each anchor is a value paired with a non-functional key, which has no impact on the JEDI DA functionality. The key starts with `_anchor_` and is followed by a field name (`channels`, `use_flag`, etc)    
- (2) The anchor name starts with the SIS name (eg. `cirs-fsr_n20`, `atms_npp`, etc) and is followed by the corresponding field name.
- (3) To start, one can add ` [1]` after each anchor name as a placeholder (1 for channels). `yaml_finalize` will read the correct values from satinfo and put them at the placeholder location. Check the above two cris-fsr_n20 yaml files for an example.    
- (4) No `s` after each anchor name except `channels`.

##### 2. Copy satinfo to current directory and touch a fake ioda file
`yaml_finalize` assumes the `satinfo` file is available under the current directory. NOTE: it is `satinfo` without any suffixes.    

##### 3. Get `yaml_finalize`
```
wget https://raw.githubusercontent.com/guoqing-noaa/satinfo2yaml/refs/heads/main/yaml_finalize
```
##### 4. Run `yaml_finalize`
```
./yaml_finalize <yaml_file>
```
##### 5. A Practice case
```
git clone https://github.com/guoqing-noaa/satinfo2yaml.git
cd satinfo2yaml
./yaml_finalize cris-fsr_n20.yaml
vimdiff cris-fsr_n20.yaml cris-fsr_n20_old001.yaml
```
You can see the simple templates ` [1]` have been replaced by the actual values from satinfo.  
You can further change some fields for cris-fsr_n20 channels in satinfo, run `yaml_finalize` again. Then the changes will be reflected in the updated `cris-fsr_n20.yaml`
```
vi satinfo
./yaml_finalize cris-fsr_n20.yaml
vimdiff cris-fsr_n20.yaml cris-fsr_n20_old002.yaml
```
