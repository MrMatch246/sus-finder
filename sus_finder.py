import os,json


dir_path = os.path.dirname(os.path.realpath(__file__))

#class SUSFinder:
#    pass



def sus_finder():
    with open(f'{dir_path}/config.json') as con:
        data=json.load(con)
    config=data["config"]
    services=data["services"]
    results_path=config["results_path"]
    if not os.path.isdir(results_path):
        results_path=f'{dir_path}/results/'
        os.mkdir(results_path)
        print(f"{config['results_path']} does not exist! \n Results will be in {results_path}")
    for ser in services.keys():
        if not os.path.isdir(services[ser]["full_path"]):
            print(f'Path {services[ser]["full_path"]} for {ser} is not existent!')
            exit(-1)
    max_concurrent=config["max_concurrent"]
    #TODO
    # do it in two layers
    # first get all results into files(one per service)
    # then grep these files once for every severity and sort them by appending
    # to final results file










if __name__ == '__main__':
    sus_finder()