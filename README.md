# yaml_finalize 
This tool will read [**satinfo**](https://github.com/guoqing-noaa/satinfo2yaml/blob/main/satinfo) to get the `channel`, `iuse`, `icld_det`, `error`, `ermax` etc values for each SIS and then automatically replace the corresponding anchors in the JEDI configuration YAML files.

##### 1. Set up correct anchors in a YAML file    
The anchors should be placed between `obs space.name` and `obs space.distribution`. Here is an example:
```
     - obs space:
         name: cris-fsr_n20 
         _anchor_channel: &cris-fsr_n20_channel [1]
         _anchor_iuse: &cris-fsr_n20_iuse [1]
         _anchor_icld_det: &cris-fsr_n20_icld_det [1]
         _anchor_error: &cris-fsr_n20_error [1]
         _anchor_ermax: &cris-fsr_n20_ermax [1]
         distribution:
           name: "RoundRobin"
           halo size: 100e3
```
You can check [cris-fsr_n20.yaml](https://github.com/guoqing-noaa/satinfo2yaml/blob/main/cris-fsr_n20.yaml#L73-L79) or [cris-fsr_n20_finalized.yaml](https://github.com/guoqing-noaa/satinfo2yaml/blob/main/cris-fsr_n20_finalized.yaml#L73-L189)    
Rules:   
- (1) each anchor is a value paired with a non-functional key, which has no impact on the JEDI DA functionality. The key starts with `_anchor_` and is followed by a field name (`channel`, `iuse`, etc)    
- (2) The anchor name starts with the SIS name (eg. `cirs-fsr_n20`, `atms_npp`, etc) and is followed by the corresponding field name.
- (3) To start, one can add ` [1]` after each anchor name as a placeholder. `yaml_finalize` will read the correct values from satinfo and put them at the placeholder location. Check the above two cris-fsr_n20 yaml files for an example.    
- (4) No `s` after each anchor name, i.e. use `channel`, `iuse` directly instead of `channels`, `iuses`.
- (5) To be consistent with convinfo and satinfo, we use `ermax`, `ermin` instead of `errmax`, `errmin`

##### 2. Copy satinfo to current directory
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
