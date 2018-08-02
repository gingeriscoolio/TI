import sys
import os
import time
import re
from urllib.request import urlopen


def restart_program():
    python = sys.executable
    os.execl(python, python, *sys.argv)


try:
    id_file_name = input("\nWhat is the name of the file containing your user IDs? \n \n")
    id_number_file = open(id_file_name, "r+")

    print_file_name = input("\nName the new file in which you would like to print your results: \n\n")
    print_file = open(print_file_name, "w+")

    url_response = input("\nWould you like to use the stored Talent Insights url to retrieve user data? \n \n")
    if url_response == "yes" or url_response == "y":
        url = "http://devportal.talentinsights.com/iapi/reporting/confidence/"
    elif url_response == "no" or url_response == "n":
        url = input("\nPlease enter the url that you would like to use (excluding the user-specific suffix) \n \n")
    else:
        print("\nError: Invalid input")
        restart_program()

    num_ids = sum(1 for line in id_number_file)
    id_number_file.seek(0, 0)

    counter_max = input("\nHow many IDs would you like to process in each interval? \n "
                        "WARNING: For TI, numbers higher than 100 are more likely to overload the server.\n")
    line_counter = 1
    wait_time = input("\nHow many seconds would you like in between intervals? \n"
                      "WARNING: For TI, numbers lower than 3 are more likely to overload the server.\n\n")

    print_file.write(" \n \n ID,EI_page,SN_page,TF_page,PJ_page,EI_percentage,SN_percentage,TF_percentage,PJ_percentage,EI_confidence,SN_confidence,TF_confidence,PJ_confidence \n")

    for ids in range(1, num_ids):
        print_file.truncate()

        id_raw = id_number_file.readline()
        id_number = id_raw.replace("\n", "")

        part_info = (url + id_number)
        response = urlopen(part_info)
        content = str(response.read())

        start = content.index("\"EI_page\"")
        confidence_info = ("\"ID\":" + id_number + "," + content[start:-3] + ",")

        make_list = re.findall(r':(.*?),', confidence_info)
        make_string = str(make_list)

        refine_results = make_string.replace("\"", "")
        refine_results1 = refine_results.replace("[", "")
        refine_results2 = refine_results1.replace("]", "")
        final_results = refine_results2.replace("'", "")

        print_file.write(final_results + "\n")
        print(final_results)

        if int(line_counter) % int(counter_max) != 0:
            line_counter += 1
        else:
            line_counter += 1
            time.sleep(int(wait_time))
except OSError as a:
    print(a)
except EOFError as b:
    print(b)
except IOError as c:
    print(c)
except ValueError as d:
    print(d)
