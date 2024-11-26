
def dummy_search(seacrh_Data:str) -> list:
    return_list = []
    if seacrh_Data != "FAKE":
        return_list = [{"doi_" + str(i): i} for i in range(1, 41)]
        
    return return_list

def dummy_transformation(keyword_Data:str) -> list:
    return_list = []
    if keyword_Data != "FAKE":
        return_list = [{"keyword_" + str(i): ["doi_"+ str(i), "doi_"+ str(i+1), "doi_"+ str(i)]} for i in range(1, 41)]
        
    return return_list

def dummy_summary(paper_Data:str) -> list:
    return_list = []
    if paper_Data != "FAKE":
        return_list = [{"doi_" : "summary"}]
        
    return return_list

def dummy_referencelist(paper_Data:str) -> list:
    return_list = []
    if paper_Data != "FAKE":
        return_list = ["doi_" + str(i) for i in range(1, 41)]
        
    return return_list