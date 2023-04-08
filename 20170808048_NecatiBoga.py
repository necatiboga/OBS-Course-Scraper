# Author: Necati Boga
# Since: 2023-04-08

import requests
from bs4 import BeautifulSoup

url = "https://obs.akdeniz.edu.tr/oibs//bologna/progCourses.aspx?lang=en&curSunit=1040"
response = requests.get(url)

if response.status_code == 200:
    html = response.content
    soup = BeautifulSoup(html, 'html.parser')

    # Select all the semester titles
    semesters = soup.select('tr[align="right"] td span[id*="grdBolognaDersler_lblDersKod"]')

    for i, semester_title in enumerate(semesters, start=1):
        # Break the loop after the second semester
        if i ==2:
            break
        # Get all the rows in the current semester table
        rows = semester_title.find_parent('table').select('tr')[1:]  # exclude header row
        num_courses = len(rows)
        print(f"All Semester has {num_courses} courses.")
        count = 0
        file_count = 1
        file = None
        
        for row in rows:
            
            cols = row.select('td')
            tek = cols[4].text.strip()
            # Create a new file for each semester if it's the first course in the current semester
            if count == 0:
                semester_file = f'Semester_{file_count}.txt'
                file = open(semester_file, 'w')
                file_count += 1
                print(f"Created {semester_file}")

            # If the current course is the total ECTS row, close the file and create a new one
            if tek == "Total ECTS":
                if file is not None:
                    file.close()
                
                # Stop creating files after the 8th semester
                if file_count == 9:
                    break
                semester_file = f'Semester_{file_count}.txt'
                file = open(semester_file, 'w')
                file_count += 1
                print(f"Created {semester_file}")
            
            # Extract the course information from the current row
            code = cols[0].text.strip()
            name = cols[1].text.strip()
            name2 = cols[2].text.strip()
            ects = cols[5].text.strip()
            line = "{:<10}{:<20}{:<50}{}".format(code, name, name2, ects)

            # Write the course information to the current semester file
            file.write(line + "\n")
            count += 1
        # Close the current semester file if it exists    
        if file is not None:
            file.close()
            
     
else:
    print(f"Error: {response.status_code}")

