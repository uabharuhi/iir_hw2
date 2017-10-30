from Bio import Entrez
import json
# save pubmed xmls return by a query  as json
def search(query):
    print('search')
    Entrez.email = 'your.email@example.com'
    handle = Entrez.esearch(db='pubmed',
                            sort='relevance',
                            retmax='2000',
                            retmode='xml',
                            term=query)
    results = Entrez.read(handle)
    print('search end')
    return results

def fetch_details(id_list):
    print('fetch')
    ids = ','.join(id_list)
    Entrez.email = 'your.email@example.com'
    handle = Entrez.efetch(db='pubmed',
                           retmode='xml',
                           id=ids)
    results = Entrez.read(handle)
    print('fetch end')
    return results

if __name__ == '__main__':
    results = search('gene')
    id_list = results['IdList']
    papers = fetch_details(id_list)
    for i, paper in enumerate(papers['PubmedArticle']):
        print(i)
        with open("./data/%d.json"%(i), mode='w',encoding='utf-8') as f:
            try :
                title  =  paper['MedlineCitation']['Article']['ArticleTitle']
                articles = paper['MedlineCitation']['Article']['Abstract']
                l = []
                texts = articles['AbstractText']
                for text in texts:
                    l.append(text)
                obj = {"title":title,"texts":l}
                f.write(json.dumps(obj,ensure_ascii=False))
            except Exception as e:
                print(e)

            #print("%d %s" % (i+1, paper['MedlineCitation']['Article']['ArticleTitle']))
    # Pretty print the first paper in full to observe its structure
    #import json
    #print(json.dumps(papers[0], indent=2, separators=(',', ':')))
