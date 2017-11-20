from Bio import Entrez
import json
import config
# save pubmed xmls return by a query  as json
def search(query,num):
    print('search')
    Entrez.email = 'your.email@example.com'
    handle = Entrez.esearch(db='pubmed',
                            sort='relevance',
                            retmax='%d'%(num),
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
    results = search('flu',500)##
    id_list = results['IdList']
    papers = fetch_details(id_list)
    for i, paper in enumerate(papers['PubmedArticle']):
        print(i)
        with open("%s/%d.json"%(config.DATA_DIR,i), mode='w',encoding='utf-8') as f:
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
                print('exception')
                print(e)


