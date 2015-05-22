ascl.php-out.exe version 1.1
Windows compiled
Author: Joseph Conenna 
Date: 07/10/2013

Summary: 

ascl.php-out.exe is a program to generate a text file of Astrophysical Source Code Library (ASCL) entries for a certain year and month for submission to the Astrophysics Data System (ADS), as well as an xls file of fields for the entries.
The source code for the dynamic report of ASCL code entries is downloaded from (http://asterisk.apod.com/ascl.php) and saved to a work file. The file is then parsed and searched for the date queried, and the entry fields are stored in a list. 
The list of entries is then sorted. Then the fields for the entries are parsed and html tags are removed to reveal the human readable fields. The entries are then written to the output files and the program execution ends. 

The ADS takes the information from the file generated and then crates standard ADS entries for the codes. The ASCL is treated as a publication, and each code is a paper or article within the publication. The combination of a unique ID for each code entry and the record in the ADS allows codes to be cited independent of a published paper. The benefits of this system are that being able to track citations to a code could potentially help a coder build a record of publication and use for his/her code, and that there is transparency in the methods used, to know what codes were used (because they are cited) and being able to look at them.

Instructions:

Execute ascl.php-out.exe and enter year to query in the format YY, then enter the month to query in the format MM. A directory exists inside the ascl.php-out directory named 'Output', or will be created upon first execution. If there 
are entries found then a directory inside Output is created named ascl.YYMM 
where the two output files will be saved. Once the parsing algorithm finishes 
the two files are saved. If there are no entries in ascl.php matching the date 
queried, then a message will appear and no directory or files will be created. 

Deliverables: 

ACLS_ADS_data_build_file.YYMM.txt (submission files in ADS formatting)
ACLS_ADS_data_build_file.YYMM.xls (Workbook of specified entry fields)
workfile.txt                      (acls.php source code file)