import os
import sys

script_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
folder_name = os.path.basename(script_dir)

file_list = os.listdir(script_dir)

motions = {}

for file_name in file_list:
    if file_name.endswith('.txt'):
        file_name = file_name[:-4]  # Remove the '.skp' extension
        motion_name = file_name.split('_ext_skp_')[0].upper()
        if motion_name not in motions:
            motions[motion_name] = []
        motions[motion_name].append(file_name)

def custom_sort_key(s):
    parts = s.split('_')
    try:
        return int(parts[0])
    except ValueError:
        return parts[0]

script = ''
script += f"farc_list.0={folder_name}.farc\n" # set farc_list to use the name of the folder the script is in 
script += "farc_list.length=1\n" # length should always be 1

for motion_index, motion_name in enumerate(motions.keys()):
    motion_files = motions[motion_name]
    script += f"motion.{motion_index}.name={motion_name}\n" # motion line bs
    for i, motion_file in enumerate(motion_files):
        if "_ext_skp_" in motion_file:
            obj_name = motion_file.split('_ext_skp_')[1].upper()
            script += f"motion.{motion_index}.skp.{i}.farc=0\n"
            script += f"motion.{motion_index}.skp.{i}.obj={obj_name}\n"
    script += f"motion.{motion_index}.skp.length={len(motion_files)}\n" 

script += f"motion.length={len(motions)}\n"
script += "pv.length=0\n"

output_file = "mod_osage_setting.txt" # export to mod_osage_setting.txt
with open(output_file, "w") as file:
    file.write(script)

# Read the script from the output file and sort it lexicographically
with open(output_file, "r") as file:
    script_lines = file.readlines()
sorted_script_lines = sorted(script_lines)

with open(output_file, "w") as file:
    file.write("".join(sorted_script_lines))

print(f"Output written to {output_file}")
