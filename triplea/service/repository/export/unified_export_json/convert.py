

import click
from triplea.schemas.article import Article

from triplea.service.repository.export.unified_export_json import json_converter_01
from triplea.utils.general import pretty_print_dict, safe_csv

def convert_unified2csv_dynamically(list_output):
    one_to_one = []
    one_to_many = []
    d = list_output[0]
    keys= d.keys()
    for k in keys:
        if isinstance(d[k],str):
            one_to_one.append(k)
        elif isinstance(d[k],int):
            one_to_one.append(k)
        elif isinstance(d[k],list):
            dic = {"Table" : k}
            one_to_many.append(dic)
        elif d[k] is None:
            value = click.prompt(f"""What is type of column {k}?
(str, int, list)""", type=str)
            if value == 'str':
                one_to_one.append(k)
            elif value == 'int':
                one_to_one.append(k)
            elif value =='list':
                dic = {"Table" : k}
                one_to_many.append(dic)
            else:
                print("value is out of range.")
                exit()
        else:
            print(type(d[k]))
            raise NotImplementedError


    # Main Part of filename
    mf = "main111"

    #---------------------Create Header of all csv files----------------------
    # Create Header of main csv file - for one_to_one fields
    main = ""
    main = "ID,"
    for i in one_to_one:
        main = main + i + ','
    main = main[0:len(main)-1] + '\n'
    print(main)
    with open(f"{mf}.csv", "w", encoding="utf-8") as file1:
        file1.write(main)

    # Create Header of othr csv files - for one_to_many fields
    # for t in one_to_many:
        

    def deep_check():
        i=0
        exit_loop=False
        while exit_loop==False:
            i=i+1
            if i>=len(list_output):
                print(f"""All values of variable '{lf}' are empty and this variable is removed from the output.""")
                #-------------------------Delete Title from one_to_many----
                # for one_to_many.remove(lf)
                for i_one_to_many in range(len(one_to_many)):
                    if one_to_many[i_one_to_many]['Table'] == lf:
                        one_to_many.pop(i_one_to_many)
                        # break
                        return True # means delete coloumn
                #-------------------------Delete Title from one_to_many----                       
                exit_loop=True
            else:
                d = list_output[i]
                if d[lf] is not None:
                    exit_loop==True
        return False

    num=0
    while num<len(one_to_many):
    # for num in range(len(one_to_many)-1):
        # lf = t['Table']
        lf = one_to_many[num]['Table']
        # print(lf)
        if d[lf] is not None:
            if len(d[lf]) != 0:
                if isinstance(d[lf][0],dict):
                    keys= d[lf][0].keys()
                    star = ""
                    star = "ID,"
                    for k in keys:
                        star = star + k + ','
                    star = star[0:len(star)-1] + '\n'
                    one_to_many[num]['keys'] = list(keys)
                elif isinstance(d[lf][0],str):
                    star = f"ID,{lf}\n"
                    one_to_many[num]['keys'] = [lf]
                elif isinstance(d[lf][0],int):
                    star = f"ID,{lf}\n"
                    one_to_many[num]['keys'] = [lf]
                else:
                    raise NotImplementedError
                
                with open(f"{mf}_{lf}.csv", "w", encoding="utf-8") as file1:
                        file1.write(star)
            else: # len(d[lf]) = 0
                r = deep_check()
                if r is True: # Delete Column
                    num = num - 1


        else: # d[lf] is None
            r = deep_check()
            if r is True: # Delete Column
                num = num - 1

        num=num+1
    #---------------------Create Header of all csv files---------------------- 
        
    #---------------------Create Data of all csv files------------------------ 
    files = []
    for i in range(0,len(list_output)):
        data = list_output[i]
        # Write Value in main Table
        f_main = open(F"{mf}.csv", "a", encoding="utf-8") 
        main = ""
        main = f"{i},"
        for col_name in one_to_one:
            col_value = ""
            if col_name in data:
                if data[col_name] is None:
                    col_value = ""
                else:
                    col_value = safe_csv(data[col_name])
            else:
                col_value = ""            
            main = main + str(col_value) + ','
        main = main[0:len(main)-1] + '\n'
        f_main.write(main)
        f_main.close()


        # Write Value in Multiple Table
        # for t in one_to_many:
        for j in range(0,len(one_to_many)):
            t = one_to_many[j]
            lf = t['Table']
            value_dict = data[lf]
            file = open(F"{mf}_{lf}.csv", "a", encoding="utf-8")
            main = ""
            main = f"{i},"
            if isinstance(value_dict,list):
                for value in value_dict:
                    # print(value)
                    if isinstance(value,str):
                        pass
                        col_value= safe_csv(value)
                        main = main + str(col_value) + ','                      
                    elif isinstance(value,list):
                        raise NotImplementedError
                    elif isinstance(value,dict):
                        main = ""
                        main = f"{i},"                        
                        for col_name in t['keys']:
                            if isinstance(value[col_name],list):
                                pass
                                # print(f"Not Implement. {col_name} Table in sub Table")
                            elif isinstance(value[col_name],str):
                                col_value= safe_csv(value[col_name])
                                main = main + str(col_value) + ',' 
                        main = main[0:len(main)-1] + '\n'
                        file.write(main)
                        main = ""                       
                    else:
                        print("nabilam")


            elif isinstance(value_dict, dict):
                print("chamedonam")
            elif value_dict is None:
                main = main + "" + ','
            else:
                print("chamedonam else")
                print(type(value_dict))

            if main != "":
                main = main[0:len(main)-1] + '\n'
                file.write(main)    
 
    #---------------------Create Data of all csv files------------------------       

        

