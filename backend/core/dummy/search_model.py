
def dummy_search(seacrh_Data:str) -> list:
    return_list = []
    if seacrh_Data != "FAKE":
        return_list = [{"doi_" + str(i): i} for i in range(1, 41)]
        
    return return_list
