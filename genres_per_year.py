import re, csv
import matplotlib.pyplot as plt

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
            # Check if the information between the brackets is the year or not. If it is not the year, replace the brackets with commas
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

            lst[i] = lst[i].replace('}','')
            lst[i] = lst[i].replace('{','')
        lst[i] = lst[i].split(',')
        new_ls.append(lst[i])
    return new_ls


gen_ls = lst_sieve(open_files("analysis.py/genres.list"))

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

def create_dict_genres(lst):
    """
    list(tuple) -> list(tuple)
    Creates the dictionary, the key is the year and the value is all the found genres. 
    From this dictionary the function returns the list of tuples consisting of the year and the most popular genre(s)

    >>> create_dict_genres([['"#Besties" ', '2014', 'Short'], ['"#Bikerlive" ', '2014', 'Short']])
    {'2014': 'Short'}
    >>> create_dict_genres([['"#Besties" ', '2014', ' Short'], ['"#Bikerlive" ', '2014', ' Short'], ['"#ByMySide" ', '2012', 'Comedy']])
    {'2014': 'Short', '2012': 'Comedy'}
    """
    new_dict = {}
    final_dict = {}
    genres = ['Drama', 'Comedy', 'Horror', 'Documentary', 'Short', 'Crime', 'Biography', 'Animation', 'Thriller', 
            'Adventure', 'Mystery', 'Romance', 'Family', 'Music', 'Talk-Show', 'Reality-TV', 'Western', 'Action', 
            'History', 'Sci-Fi', 'Game-Show', 'Sport']
    for line in lst:
        count = True
        ln = line[1][:4]
        int_ln = int(ln)
        # Checks the year and creates the dictionary and by looping through the list of genres, copes with the problematic data
        if int_ln > 1873 and int_ln < 2017:
            if ln not in new_dict.keys():
                new_dict[ln] = []
            for genre in genres:
                if genre in line[len(line) - 1]:
                    new_dict[ln].append(genre)
                    count = False
            if count:
                new_dict[ln].append(line[len(line) - 1])
    # Finds the most common elements
    for el in new_dict:
        final_dict[el] = most_popular(new_dict[el])
        final_dict[el] = final_dict[el][0][0]
    return final_dict

result = create_dict_genres(gen_ls)
# print(result)

def write_csv_file(dct):
    """
    lst -> ()
    Returns the csv file columns for which are the year and the genre(s)
    """
    with open('result.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Year', 'Genre'])
        keys = sorted(dct.keys())
        for key in keys:
            writer.writerow([key, dct[key]])
    return writer

# print(write_csv_file(result))

def genres_for_all_years(dct):
    """
    dict -> dict
    Counts how many times the genre occurs and returns the dictionary containing the genre and the number

    >>> genres_for_all_years({'2014': 'Short', '2012': 'Comedy', '2013': 'Short'})
    {'Short': 2, 'Drama': 0, 'Documentary': 0}
    """
    # Looking at csv file, there are three most common genres and here I count how many years there are
    final_dct = {}
    final_dct["Short"] = list(dct.values()).count("Short")
    final_dct["Drama"] = list(dct.values()).count("Drama")
    final_dct["Documentary"] = list(dct.values()).count("Documentary")
    return final_dct

genres = genres_for_all_years(result)

def draw_a_graph(dct):
    """
    dict -> ()
    Prints the graph using matplotlib library
    """
    plt.bar(2, genres["Short"])
    plt.bar(3, genres["Drama"])
    plt.bar(4, genres["Documentary"])
    plt.xticks([2, 3, 4], ("Short", "Drama", "Documentary"))
    plt.xlabel("Genres")
    plt.ylabel("Number of years")
    return plt.show()

# print(draw_a_graph(genres))