""" ascl.php-out_1.0.py - program for downloading and processing the ascl.php webpage of ASCL journal
entries for a user defined date (yy/mm), and outputting a structed txt file of journal entry fields
grouped and sorted for ADS submission, as well as an xls file of the fields for the user's use. Program
assumes that the php file accessed will adhere to the coding conventions used and identified in this
application.
"""
import os
import urllib
import xlwt
import time

# User interface
print "_________________________________________________________________________\n"  
print "|* ____________________________________________________________________ *|\n" 
print "|*|                ASCL.PHP To ADS Report + Workbook                   |*|\n"
print "|*|                            Version 1.0                             |*|\n" 
print "|*|___________________________________________________________________ |*|\n" 
print "|************************************************************************|\n"

year  = raw_input("                           Enter year to query:")
while(year.isdigit() == False or int(year) < 0 or int(year) > 99 or len(year) != 2):
   print "\n                           Please enter the year as an integer"
   print "                           in the format YY ...\n"
   year  = raw_input("                           Enter year to query:")
   
month = raw_input("\n                           Enter month to query:")
while(month.isdigit() == False or int(month) < 1 or int(month) > 12 or len(month) != 2):
   print "\n                           Please enter the month as an integer"
   print "                           in the format MM \n"
   month = raw_input("\n                           Enter month to query:")
   
# Starts timer
start = time.clock()

print "\n\n                           Downloading ascl.php...\n"                              

# Open url, read in php source to .txt and close file.
datasource = urllib.urlopen("http://asterisk.apod.com/ascl.php")

f = open('workfile.txt', 'w')

while 1:
        line = datasource.readline()
        f.write(line)
        if line == "</table>": break
f.close()

print "                           Workfile.txt created...\n"

#Open source file for reading 
f = open('workfile.txt', 'r')

# Initialize list to hold entry string in order 
array = []

# Reads in first line
line = f.readline()

# While loop runs until line read in is end of php table tag. 
while(line != "</table>"):
   
    # Read in line
    line = f.readline()

    # If line is element of fields
    if(line.find("<tr><td>") != -1):

       # Check if readline read in end of entry '</a>'
       while(line.find("</td></tr>") == -1):
           tmp = f.readline()
           line += tmp

       # Parse string to form 4 list elements
       par = line.split("ascl:")
       par = par[1].split("</td><td>")
       
       # If parsed year and month match, append entry to list of unsorted entries.
       if(par[0][0:2] == year and par[0][2:4] == month):
         array.append([int(par[0][5:]), par])

# If no entries found matching date, exit. 
if(len(array) == 0):
   print             "                           No entries matching query."
   wait = input("                           Press Enter to exit.")
   exit()

# If there are entries in array, create and/or change directory
if(os.path.exists("Output") != True):
  os.mkdir("Output")
os.chdir("Output")
if(os.path.exists("ascl." + year + month) != True):
  os.mkdir("ascl." + year + month)
os.chdir("ascl." + year + month)

# If there are entries in array, open .txt and .xls reports for writing.
o = open('ACLS_ADS_data_build_file.' + year + month + '.txt'  , 'w')
print "                           ACLS_ADS_data_build_file." + year + month + ".txt Created"
ss = xlwt.Workbook(encoding="utf-8")
page = ss.add_sheet("sheet",cell_overwrite_ok=True)
print "                           ACLS_ADS_data_build_file." + year + month + ".xls Created"

# Sort array of unsorted entries.
array.sort()

# Process array of entries and send to files.
for j in range(0,len(array)):
   
    line = array[j][1]
          
    # Search and replace html tags 
    for i in range(0,4):
        line[i] = str(line[i]) 
        # Search and replace various html tags
        line[i] = line[i].replace("<ul><li>", "  ")
        line[i] = line[i].replace("</li><li>", "\n  ")
        line[i] = line[i].replace("</li></ul>", "\n  ")
        line[i] = line[i].replace("&gt;", ">")
        line[i] = line[i].replace("&lt;", "<")
        line[i] = line[i].replace("&quot;", '"')
        line[i] = line[i].replace("&amp;", "&")
        line[i] = line[i].replace("<ul>", "    ")
        line[i] = line[i].replace("</ul>", "")
        line[i] = line[i].replace('</span>', "")
        line[i] = line[i].replace('<sup>', "^")
        line[i] = line[i].replace('</sup>', "")
        line[i] = line[i].replace('<sub>', "")
        line[i] = line[i].replace('</sub>', "")
        line[i] = line[i].replace('</div>', "")

        # Search and replace unicode entities with ascii chars
        while(line[i].find("&#") != -1):
            a = line[i].find("&#")
            b = line[i][a:].find(';')
            num = int(line[i][a+2:a+b])
            ch = unichr(num)
            line[i] = line[i][0:a] + ch + line[i][a+3+b:]
        
        # Search for hyperlinks and replace until there are none.
        while(line[i].find("<a href") != -1):

            # Parses tags around hyperlink text and saves text field.
            tmp = line[i].split("<a href=")
            tmp = tmp[1].split(">")
            tmp = tmp[1].split("</a")
            tmp = tmp[0]

            # Locates indices of beginning and end of url and cuts it from line[i]
            a = line[i].find("f=") + 1
            b = line[i].find("class") - 1
            line[i] = line[i][0:a] + line[i][b:]
            # Locates name field within hyperlink and replaces link tags with only text
            loc = line[i].find(">" + tmp + "<") + 1
            a = line[i].find("<a href")
            b = line[i].find(tmp + "</a>")
            line[i] = line[i][0:a] + tmp + line[i][loc+len(tmp)+4:]

        # Searches for parenthesized hyperlinks and replaces with url text.
        while(line[i].find("<!-- m -->") != -1):
           
            # Parse tags around url to extract it
            tmp = line[i].split('"postlink" href="')
            tmp = tmp[1].split('">http:')
            tmp = tmp[0]
            
            # Replace tag with just url in field.
            a = line[i].find("<!-- m -->")
            b = line[i].find("</a><!-- m -->")
            line[i] = line[i][0:a] + tmp + line[i][b+14:]

        # Searches for span tags
        while(line[i].find("<span style=") != -1):
            a = line[i].find("<span style=")
            b = line[i][a:].find(">")
            line[i] = line[i][0:a] + line[i][a+b+1:]

        # Searches for ol tags
        while(line[i].find("<ol style=") != -1):
            a = line[i].find("<ol style=")
            b = line[i].find("<li>") + 4
            c = line[i].find("</li></ol>")
            line[i] = line[i][0:a] + line[i][b:]
            loc = b - (b-a)
            count = 1
            while(line[i][loc:].find("</li></ol>") != -1):
                period = line[i][loc:].find('.') + loc
                if(count==1):
                   line[i] = line[i][0:loc] + str(count) + ".   " + line[i][loc:]
                else: line[i] = line[i][0:loc] + str(count) + ". " + line[i][loc:]
                loc = period + 4 + len(str(count))
                count += 1
            line[i] = line[i][0:loc-5] + line[i][loc+10:]

        # Searches for fiv tags
        while(line[i].find("<div style=") != -1):
            a = line[i].find("<div style=")
            b = line[i][a:].find(">") + a
            line[i] = line[i][0:a] + line[i][b+1:]
                
            


    # Write output to ADS file according to upload file template.  
    o.write("%T " + line[1] + "\n")
    o.write("%A " + line[3] + "\n")
    o.write("%J Astrophysics Source Code Library, record ascl:" + year + month + line[0][4:] + "\n")
    o.write("%D " + month + "/20" + year + "\n")
    o.write("%B " + line[2] + "\n")
    o.write("%I ELECTR: http://ascl.net/" + year + month + line[0][9:21] + line[0][4:])
    o.write("\n\n")
    
    # Spreadsheet commands
    page.write(j, 0, line[1])
    page.write(j, 1, line[3])
    page.write(j, 2, "Astrophysics Source Code Library, record " + year + month + line[0][4:])
    page.write(j, 3, month + "/20" + year)
    page.write(j, 4, "http://ascl.net/" + year + month + line[0][9:21]+ line[0][4:])

# Save Spreadsheet
ss.save("ACLS_ADS_data_build_file." + year + month + ".xls")
print "                           ACLS_ADS_data_build_file." + year + month + ".xls Finished"

# Close input and output.
o.close()
f.close()
print "                           ACLS_ADS_data_build_file." + year + month + ".txt Finished"
# Ends timer and prints final output.
elapsed = (time.clock() - start)
elapsed = "%.2f" % elapsed
elapsed = str(elapsed)
print "\n                           Done! Finished in " + elapsed + " seconds."
wait = input("                           Press Enter to exit.")
