import os, json
import multiprocessing
import sys

dir_path = os.path.dirname(os.path.realpath(__file__))

def grep_generator_1(search_folder, pattern_list, max_concurrent, output_file, files_per_proc=40,file_type="None"):
    max_con = max_concurrent
    file_setter=""
    if file_type != "None":
        file_setter=f' --include="*.{file_type}" '
    if max_concurrent == 0:
        max_con = multiprocessing.cpu_count()
    pattern_string = ""
    for pattern in pattern_list:
        pattern_string += f'-e {pattern} '
    grep_string = f'find {search_folder} -type f -print0 | xargs -0 -P {max_con} -n {files_per_proc} grep -n -R {file_setter}{pattern_string} > {output_file}'
    return grep_string

def grep_generator_2(search_file, pattern_list, output_file):
    pattern_string=""
    for pattern in pattern_list:
        pattern_string += f'-e {pattern} '
    grep_string = f'grep -n -R {pattern_string} {search_file} >> {output_file}'
    return grep_string


def pattern_list_gen(severity=None,file_type=None):
    pattern_list=[]
    with open(f'{dir_path}/sus.txt',"r") as sus:
        patterns=sus.read()
    for line in patterns.splitlines()[1:]:
        splitted=line.rsplit("|",3)
        if severity is None:
            pattern_list.append(splitted[0])
        elif severity == int(splitted[1]):
            pattern_list.append(splitted[0])
    return pattern_list

def sus_finder(arg=None):
    conf_path=f'{dir_path}/config.json'
    if arg is not None:
        conf_path=arg
    with open(conf_path) as con:
        data = json.load(con)
    config = data["config"]
    services = data["services"]
    results_path = config["results_path"]
    if not os.path.isdir(results_path):
        results_path = f'{dir_path}/results/'
        if not os.path.isdir(results_path):
            os.mkdir(results_path)
        print(f"{config['results_path']} does not exist! \nResults will be in {results_path}")
    for ser in services.keys():
        if not os.path.isdir(services[ser]["full_path"]):
            print(f'Path {services[ser]["full_path"]} for {ser} is not existent!')
            exit(-1)
    max_concurrent = config["max_concurrent"]
    for ser in services.keys():
        search_folder=services[ser]["full_path"]
        pattern_list=pattern_list_gen()
        output_file=f'{results_path}{ser}_full.txt'
        grep_string=grep_generator_1(search_folder,pattern_list,max_concurrent,output_file)
        #print(grep_string)
        os.system(grep_string)
    for ser in services.keys():
        #print("s")
        search_file=f'{results_path}{ser}_full.txt'
        output_file=f'{results_path}{ser}.txt'
        os.system(f'echo "" > {output_file}')
        for severity in range(10,0,-1):
            pattern_list=pattern_list_gen(severity=severity)
            if pattern_list == []:
                continue
            grep_string=grep_generator_2(search_file,pattern_list,output_file)
            #print(grep_string)
            os.system(f'echo "=========SEVERITY:{severity}================" >> {output_file}')
            os.system(grep_string)
        os.remove(search_file)


if __name__ == '__main__':
    arg=None
    if len(sys.argv) > 1:
        arg=sys.argv[1]
    sus_finder(arg)
