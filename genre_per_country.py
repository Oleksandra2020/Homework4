import csv
import re

def open_files(file):
    """
    () -> list
    Returns the converted file into the list 
    """
    # Open the file and put in the list only the films and not the intro info
    with open(file, encoding='utf-8', errors='ignore') as f_g:
        data = f_g.readline()
        while "!Next?" not in data:
            data = f_g.readline()
        lst = []
        while "�� (2012)|" not in data:
            data = f_g.readline().strip()
            lst.append(data)
    return lst

def lst_sieve(lst):
    r"""
    list -> list
    Returns the list without tabs and other unnecessary elements

    >>> lst_sieve(['\"#Besties\" (2014) USA'])
    [['"#Besties" ', '2014', ' USA']]
    >>> lst_sieve(['\"#Bikerlive\" (2014) USA'])
    [['"#Bikerlive" ', '2014', ' USA']]
    """
    # Take the necessary information from each line
    digits = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', 'I', 'V', 'X']
    new_ls = []
    for i in range(len(lst)):
        if '????' in lst[i]:
            continue
        else:
            lst[i] = lst[i].replace("\t", '')
            lst[i] = lst[i].replace('(V)', '')
            lst[i] = lst[i].replace('(TV)', '')
            lst[i] = lst[i].replace('(VG)', '')
            lst[i] = lst[i].replace('{{SUSPENDED}}','')
            lst[i] = lst[i].replace(',', '')
            lst[i] = re.sub("/\\{.*\\}/", '', lst[i])

            par = True
            # Check if the information between the brackets is the year or not. If it is not the year, move on
            for letter in range(len(lst[i])):
                if lst[i][letter] == '(':
                    if ((lst[i][letter+1] == '1' and (lst[i][letter+2] == '9' or lst[i][letter+2] == '8')) \
                    or (lst[i][letter+1] == '2' and (lst[i][letter+2] == '0' or lst[i][letter+2] == '1'))) \
                    and (lst[i][letter+3] in digits) and (lst[i][letter+4] in digits):
                        lst[i] = list(lst[i])
                        lst[i][letter] = ","
                        lst[i] = ''.join(lst[i])
                        count = letter
                        par = True
                    else:
                        par = False
                if lst[i][letter] == ')' and par == True:
                    if letter - count >= 5:
                        if lst[i][letter-1] in digits:
                            lst[i] = list(lst[i])
                            lst[i][letter] = ","
                            lst[i] = ''.join(lst[i])

            lst[i] = lst[i].replace('}',',')
            lst[i] = lst[i].replace('{',',')
        lst[i] = lst[i].split(',')
        while len(lst[i]) > 3:
            lst[i].remove(lst[i][len(lst[i]) - 2])
        new_ls.append(lst[i])
    return new_ls

# print(lst_sieve(open_files("countries.list")))

def remove_repetition_countries(lst):
    """
    list -> list
    Checks the list of countries for identical names and countries and removes them, leaving only the first line

    >>> remove_repetition_countries([['"#Besties" ', '2014', ' USA'], ['"#Besties" ', '2014', ' USA'], ['"#Bikerlive" ', '2014', ' USA']])
    [['"#Besties" ', '2014', ' USA'], ['"#Bikerlive" ', '2014', ' USA']]
    >>> remove_repetition_countries([['"#Besties" ', '2014', ' USA'], ['"#Besties" ', '2014', ' USA']])
    [['"#Besties" ', '2014', ' USA']]
    """
    st = set()
    final_ls = []
    for i in range(len(lst)):
        if lst[i][0] not in st:
            final_ls.append(lst[i])
            st.add(lst[i][0])
    return final_ls

def create_dict_genres(lst):
    """
    list -> list
    Creates the dictionary, the key is the name of the film and the value are all its genres. 
    From this dictionary the function returns the list of tuples consisting of the year and the most popular genre(s)

    >>> create_dict_genres([['"#Besties" ', '2014', 'Short'], ['"#Besties" ', '2014', 'Comedy'], ['"#Bikerlive" ', '2014', 'Short']])
    {'"#Besties" ': ['Short', 'Comedy'], '"#Bikerlive" ': ['Short']}
    >>> create_dict_genres([['"#Besties" ', '2014', 'Short'], ['"#Besties" ', '2014', 'Comedy']])
    {'"#Besties" ': ['Short', 'Comedy']}
    """
    new_dict = {}
    for line in lst:
        if line[0] not in new_dict.keys():
            new_dict[line[0]] = []
        new_dict[line[0]].append(line[len(line) - 1])
    return new_dict

def create_dict_countries(lst):
    """
    list -> dict
    Creates the dictionary, the key is the country and the value are the films. 

    >>> create_dict_countries([['"#Besties" ', '2014', ' USA'], ['"#Besties" ', '2014', ' USA']])
    {'USA': ['"#Besties" ', '"#Besties" ']}
    >>> create_dict_countries([['"#Besties" ', '2014', ' USA'], ['"#Besties" ', '2014', ' Italy'], ['"#Bikerlive" ', '2014', ' USA']])
    {'USA': ['"#Besties" ', '"#Bikerlive" '], 'Italy': ['"#Besties" ']}
    """
    new_dict = {}
    for line in lst:
        line[2] = line[2].strip()
        if line[2] != '':
            if line[2] not in new_dict.keys():
                new_dict[line[2]] = []
            new_dict[line[2]].append(line[0])
    return new_dict

gen_dct = create_dict_genres(lst_sieve(open_files("analysis.py/genres.list")))
count_dct = create_dict_countries(remove_repetition_countries(lst_sieve(open_files("analysis.py/countries.list"))))

def most_popular(lst):
    """
    (list) -> list(tuple)

    Looks from the most common element in the list and returns the list of tuple containing the element
    and the number of times it occurs

    >>> most_popular(['Comedy', 'Comedy', 'Comedy', 'Documentary', 'Documentary', 'Biography'])
    [('Comedy', 3)]
    >>> most_popular(['Comedy', 'Comedy', 'Comedy', 'Documentary', 'Documentary', 'Documentary', 'Biography'])
    [('Comedy', 3), ('Documentary', 3)]
    """
    dct = {}
    ls = []
    count = 0
    # Creates the dictionary. Keys are the elements and values are the numbers that represent how many times the item occurs
    for el in lst:
        if el not in dct.keys():
            dct[el] = count
        dct[el] += 1
    max_val = max(dct.values())
    for key in dct:
        if dct[key] == max_val:
            tp = key, max_val
            ls.append(tp)
    return ls

def genre_for_country(count_dct, gen_dct):
    """
    dict, dict -> dict
    Returns the dictionary with the country and the genre

    >>> genre_for_country({'USA': ['"#Besties" ', '"#Bikerlive" '], 'Italy': ['"#Besties" ']}, {'"#Besties" ': ['Short']})
    {'USA': 'Short', 'Italy': 'Short'}
    >>> genre_for_country({'USA': ['"#Besties" ', '"#Bikerlive" '], 'Italy': ['"#Besties" ']}, {'"#Besties" ': ['Comedy'], '"#Bikerlive" ': ['Short']})
    {'USA': 'Comedy', 'Italy': 'Comedy'}
    """
    new_dict = {}
    final_dict = {}
    # Loops through the dictionary and sets the country as a key with films as values, which are the keys to the dictionary with genres.
    # Takes the value of each film and substitutes the film with genre(s)
    for key in count_dct:
        if key not in new_dict.keys():
            new_dict[key] = []
        for item in count_dct[key]:
            if item in gen_dct.keys():
                new_dict[key].append(gen_dct[item][0])
    # Calculates the most common elements
    for el in new_dict:
        if new_dict[el] != []:
            final_dict[el] = most_popular(new_dict[el])
            final_dict[el] = final_dict[el][0][0] 
    return final_dict

result = genre_for_country(count_dct, gen_dct)
print(result)

def write_csv_file(dct):
    """
    lst -> ()
    Returns the csv file columns for which are the year and the genre(s)
    """
    with open('result2.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Country', 'Genre'])
        keys = sorted(dct.keys())
        for key in keys:
            writer.writerow([key, dct[key]])
    return writer

# print(write_csv_file(result))