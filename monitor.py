# =========================================
#  PROJECT: PySentinel
#  PURPOSE: System Health Monitoring
# ==========================================


import os
import shutil
from datetime import datetime 

# Function no. 1:- To check disk usage 
def disk_usage (path):
    usage = shutil.disk_usage(path) #gives storage information

    #store total , used and free space
    total = usage.total
    used = usage.used
    free= usage.free
    return total,used,free

# testing the disk_usage function 
result = disk_usage (".")
print (result)

#Function no. 2:- Calculate Folder Size 
def folder_size (path):

    #initiate total size 
    total_size = 0 
    #walk through all the folder and files 

    for root, folders, files in os.walk(path):
        for file in files:

            file_path = os.path.join(root , file)
            try:

                #get file size and add it 
                total_size += os.path.getsize(file_path)

            except (PermissionError, OSError):

             continue

    return total_size




#Function no. 3:-find the largest files 

def largest_files (path, n ):
    #now create empty list 
    file_list = []

    for root , folders , files in os.walk(path):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                size = os.path.getsize(file_path)

                file_list.append((size,file_path))
            except (PermissionError, OSError):
                continue
    #sort files from largest to smallest 
    file_list.sort(key=lambda item: item[0], reverse = True)
    return file_list[:n]

# Function no. 4 :- Human Readable Size 
#(convert bytes into readable units)
def human_size(num_bytes):
    if num_bytes < 1024:
        return f"{num_bytes} Bytes"

    elif num_bytes < 1024 ** 2:
        return f"{num_bytes/ 1024:.2f} KB"
    
    elif num_bytes < 1024 **3:
        return f"{num_bytes / (1024**2):.2f} MB"

    else :
        return f"{num_bytes / (1024**3):.2f} GB"

print (human_size(5242880))


#Function no. 5 :- Generate system heakth report 
def generate_report (path):
    #get disk information 
    total , used,  free = disk_usage (path)
    size = folder_size (path)
    biggest = largest_files (path, 5)


    #caculate free disk percentage 
    free_percent = (free / total)* 100


    #print health report 
    print("\n ====== SYSTEM HEALTH REPORT======")
    print("Date & Time:", datetime.now())

    print("\n DISK INFORMATION")

    print("Total Storage:",human_size(total))
    print("Used Storage:",human_size(used))
    print("Free Storage:",human_size(free))

    print("Free Space:", round(free_percent , 2), "%")
    print("\n DISK INFORMATION")
    print("Folder Size:",human_size(size))
    print("\n TOP 5 LARGETS FILES")

    if biggest:
        for file_size, file_path in biggest:
            print(file_path, "." , human_size(file_size))

    else:
        print("No files are found")

    print ("===============================")
    return free_percent , size, biggest


#Function no:-6 Save report summary in log file 
def save_log(free_percent, size, biggest):
    current_time = datetime.now()
    with open("health_log.txt", "a", encoding="utf-8") as file:
       file.write("\n========== SYSTEM HEALTH REPORT ==========\n")
       file.write(f"Time: {current_time}\n")
       file.write(f"Free Disk: {free_percent:.2f}%\n")
       file.write(f"Folder Size: {human_size(size)}\n")
           
       file.write("\nTOP 5 LARGEST FILES:\n")   
           
       for file_size, file_path in biggest:
           file.write(f"{file_path} - {human_size(file_size)}\n")

       file.write("==========================================\n")




#MAIN FUNCTION :RUN COMPLETE PROGRAM 

def main():
    path=input(
    "Enter folder path (Press Enter for current folder):"
    )
    if path.strip()=="":
        path = os.getcwd()
    if not os.path.exists(path):
            print("Error: Folder does not exist." )
            return 
    if not os.path.isdir(path):
            print("Error: Please enter a folder path.")
            return 
    try:
        free_percent ,size, biggest = generate_report (path)

        save_log(free_percent ,size, biggest)
        print ("\n Health report saved successfully!")

    except OSError as error:
        print ("An error occured:", error )

if __name__ == "__main__":
    main()


    




    