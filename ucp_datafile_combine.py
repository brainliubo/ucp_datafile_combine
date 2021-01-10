import re
import os
import time
import fileinput
import datetime






combine_filelist = []
process_lineno = 0
nowTime = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')

def read_cfg_file():
    global cfg_dict
    try:
        with open("datafile_list.cfg","r") as f:
            lines = f.readlines()
            for item in lines:
                item_r = item.strip(' ').strip('\n') #delete space and "\n"
                if (len(item_r) != 0): #delete the space line
                    combine_filelist.append(item_r)
        #print(combine_filelist)
    except Exception as err:
        print("error:  ",str(err))



def formatwrite_tofile(file_f, *info_list):
    combine_filename_max = max(len(item) for item in info_list[0]) + 5
    file_totalline_max = max(len(str(item)) for item in info_list[1]) + 5
    file_validline_max = max(len(str(item)) for item in info_list[2]) +5
    start_addr_max = max(len(str(item)) for item in info_list[3]) + 5
    length_max = max(len(str(item)) for item in info_list[4]) + 5
 #   invalid_max = max(len(str(item)) for item in info_list[3]) + 5
 #  blank_max = max(len(str(item)) for item in info_list[4]) + 5
 #   comment_max = max(len(str(item)) for item in info_list[5]) + 5
  #  rate_max = max(len(str(item)) for item in info_list[6]) + 5
  #  ziped = (zip(info_list[0], info_list[1], info_list[2], info_list[3], info_list[4], info_list[5], info_list[6]))
    print("%s%s%s%s%s" % (str(info_list[0][-1]).rjust(combine_filename_max), str(info_list[1][-1]).rjust(file_totalline_max),\
                      str(info_list[2][-1]).rjust(file_validline_max),str(info_list[3][-1]).rjust(start_addr_max),\
                      str(info_list[4][-1]).rjust(length_max)),file=file_f)
    info_list[0].pop()
    info_list[1].pop()
    info_list[2].pop()
    info_list[3].pop()
    info_list[4].pop()
    ziped = (zip(info_list[0],info_list[1],info_list[2],info_list[3],info_list[4]))
    for item in ziped:
        print("%s%s%s%s%s" % (str(item[0]).rjust(combine_filename_max), str(item[1]).rjust(file_totalline_max), str(item[2]).rjust(file_validline_max), \
                           str(item[3]).rjust(start_addr_max),str(item[4]).rjust(length_max)),file=file_f)

def  ProcessLine(fp,line):
    global  process_lineno
    temp = line.strip(" ").strip("\n")

    if(len(temp) == 0): #delete space line
        return
    if(temp.startswith("//")):
       pass
    else:
        data_list = temp.split(";")
        fp.writelines(str(data_list[0]).strip(" "))
        fp.writelines('\n')
        process_lineno = process_lineno + 1



if __name__ == "__main__":
    read_cfg_file()
    output_filename_in = input('please enter the output file name: ')
    output_filename = output_filename_in.strip(" ").strip("\n")
    try:
        fp = open(output_filename, "w")
        log_filename = "combine-"+str(nowTime)+".log"
        fp_log = open(log_filename,"w")
    except Exception as e:
        print("create file {0} error\n".format(output_filename))

    file_linenum = []
    file_procecelineno= []
    # prccess lineno
    total_lineno = []
    valid_lineno = []
    start_addr = []
    length = []
    try:
        for line in fileinput.input(combine_filelist):
            #record each file's info
            if(fileinput.isfirstline()):
                print("process the file: {0}".format(fileinput.filename()))
                file_linenum.append(fileinput.lineno()-1)
                file_procecelineno.append(process_lineno)
                start_addr.append(hex(process_lineno * 4))
            #process each line
            ProcessLine(fp, line)
        file_linenum.append(fileinput.lineno())
        file_procecelineno.append(process_lineno)


        for i in range(len(file_linenum)-1):
            total_lineno.append(file_linenum[i+1]-file_linenum[i])
            valid_lineno.append(file_procecelineno[i+1]- file_procecelineno[i])
            length.append(hex(valid_lineno[i] * 4))

        ##生成log文件


        #print(file_linenum)
        #print(file_procecelineno)
        #print(total_lineno)
        #print(valid_lineno)
        #print(start_addr)
        #print(length)
        combine_filelist.append("combined files name ")
        total_lineno.append("total_line_no.")
        valid_lineno.append("valid_line_no.")
        start_addr.append("start_address(0x)_in_output_file")
        length.append("length(0x)_in_output_file ")
        formatwrite_tofile(fp_log,combine_filelist,total_lineno,valid_lineno,start_addr,length)
        fp.close()
        fp_log.close()
        print("-----check the combine_log.log for details -------\n")
        print("-----combine is done! -------\n")
        os.startfile(log_filename) #auto open the log file

    except Exception as err:
        print("error :", str(err))

    a = input("input enter to exit!")