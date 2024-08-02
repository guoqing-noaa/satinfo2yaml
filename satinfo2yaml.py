#!/usr/bin/env python
# read satinfo and write channels,iuses,icld_dets ect into a yaml template
# usage: satinfo2yaml <satinfo> <yamlfile_in> <yamlfile_out> [sis]
#
def list_to_delimited_string(lst, spaces='  ', delimiter=', ', elements_per_line=20):
  # Convert the list to a comma-separated string with the specified delimiter
  joined_string = delimiter.join(map(str, lst))
  # Split the joined string into chunks of elements_per_line
  elements = joined_string.split(delimiter)
  # Create lines of up to elements_per_line elements
  lines = [delimiter.join(elements[i:i + elements_per_line]) for i in range(0, len(elements), elements_per_line)]
  # Add a comma at the end of each line except the last line
  formatted_lines = [spaces+line + delimiter if i < len(lines) - 1 else spaces+line for i, line in enumerate(lines)]
  return formatted_lines

##-------------------------------------------------
import sys

args=sys.argv
nargs=len(args)-1
if nargs <3:
  print(f"Usage: {args[0]} <satinfo> <yamlfile_in> <yamlfile_out> [sis]")
  exit()

satinfofile=args[1]
yamlfile_in=args[2]
yamlfile_out=args[3]
sis_in="all"
if nargs ==4:
  sis_in=args[4]

# read satinfo
dcSatinfo={}
with open(satinfofile,'r') as sfile:
  for line in sfile:
    if not line.strip().startswith("!"):
      fields=line.split() 
      if len(fields) == 11:
        sis=fields[0]  #sensor/instr/sat
        if sis in dcSatinfo:
          dcSIS=dcSatinfo[sis]
        else:
          dcSIS={'channels':[],'iuses':[],'icld_dets':[],'errors':[]}
        #
        dcSIS['channels'].append(fields[1]) 
        dcSIS['iuses'].append(fields[2]) 
        dcSIS['errors'].append(fields[3]) 
        dcSIS['icld_dets'].append(fields[8]) 
        dcSatinfo[sis]=dcSIS
      else:
        print(f"Warning: expected 11 fields\n{line}")

# Read the input yaml template
with open(yamlfile_in, 'r') as yfile:
  file_contents = yfile.read()

if sis_in == "all":
  dcForYaml=dcSatinfo
else:
  dcForYaml={sis_in:dcSatinfo[sis_in]}

# write out a new yaml file
for sis,dcSIS in dcForYaml.items():
  old_string=f'@@{sis}_channels@@'
  lines = list_to_delimited_string(dcSIS['channels'])
  new_string='\n'.join(map(str, lines))
  file_contents = file_contents.replace(old_string, new_string)
  #
  old_string=f'@@{sis}_iuses@@'
  lines = list_to_delimited_string(dcSIS['iuses'])
  new_string='\n'.join(map(str, lines))
  file_contents = file_contents.replace(old_string, new_string)
  #
  old_string=f'@@{sis}_icld_dets@@'
  lines = list_to_delimited_string(dcSIS['icld_dets'])
  new_string='\n'.join(map(str, lines))
  file_contents = file_contents.replace(old_string, new_string)
  #
  old_string=f'@@{sis}_errors@@'
  lines = list_to_delimited_string(dcSIS['errors'])
  new_string='\n'.join(map(str, lines))
  file_contents = file_contents.replace(old_string, new_string)

# Write the modified contents back to the file
with open(yamlfile_out, 'w') as yfile:
  yfile.write(file_contents)
