import requests
from bs4 import BeautifulSoup
import json

URL = "https://en.wikipedia.org/wiki/History_of_Mexico"


def get_citations_needed_count(URL): 
    ''' takes in a url and returns an integer'''
    ''' Counts how many 'citation needed' in the article. '''
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    results = soup.find(class_="mw-parser-output") ## this class have the whole things we want

    citation_needed=[]
    ## do loop to walk through the page and pick citation needed sentence from th articles
    for par in results:
        try:
            all_para = par.find_all('span', string = lambda text: 'citation' in text.lower())
            if all_para :
        ## we did this for loop because maybe there are more than one citation in the same paragraph
                for i in range(len(all_para)): 
                    citation_needed.append(all_para[i])
        except Exception as e:
            continue
    return len(citation_needed)


''' will return where each citation is needed, '''
'''and the paragragh(that needs citation) '''
'''and the line before the citation '''
''' then maybe we can send the returning string into new file '''
def get_citations_needed_report(URL): # takes in a url and returns a string , string must formatted for each citation to find it 

    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    results = soup.find(class_="mw-parser-output")

    all_paragraphs  = []
    all_lines = []

    # trying to find paragraphs with span tag , because it ccontains 'citation needed' that we wanr
    resultsss = results.find_all('p')
    for i in resultsss:
        try:
            all_para = i.find_all('span', string = lambda text: 'citation' in text.lower())
            if all_para:
                for j in range(len(all_para)):

                        #  paragraph
                        all_paragraphs.append(i.text) 

                        # line
                        pos = i.text.index('citation') 
                        line = i.text[:pos-1].split(". ")
                        all_lines.append(line[-1])

                        
        except Exception as e:
            continue

    # Store all what we want in external txt file
    output = ''
    for p in range(len(all_paragraphs)):
        output += f'cita Num: {p+1} \n'
        output += f'{all_paragraphs[p]} \n'
        output += f'So , we need citation after the below line: \n'
        output += f'{all_lines[p]} \n'

    f = open("citation.txt", "w")
    f.write(output)
    f.close()

    return output 


if __name__ == "__main__":
    

    print(get_citations_needed_report(URL))
    print(get_citations_needed_count(URL))