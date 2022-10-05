


def Group_list(targetlist , split=4 , main_image = None , mode = False):
    list_help = []
    list_asli = []
    n = 0
    for i in targetlist:
        n += 1
        list_help.append(i)
        if n % split == 0:
            list_asli.append(list_help)
            list_help = []
    if list_help != []:
        if mode == True:
            return list_asli
        if main_image is not None:
            list_help.append({'image':main_image})
        list_asli.append(list_help)
    else:
        if main_image is not None:
            list_help.append({'image':main_image})
            list_asli.append(list_help)
    return list_asli