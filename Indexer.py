import json
import math

def index():
    data = open("output.json").read()
    # list_data = data.split("\n")
    list_data = json.loads(data)
    tf = {}
    idf = {}
    documents_with_term = {}  # Store the number of documents that each term exists
    tf_idf = {}
    for page in list_data:
        temp_tf = {}
        line_terms = page['page'].split(' ')
        for term in line_terms:
            if term in temp_tf:
                temp_tf[term] += 1
            else:
                temp_tf[term] = 1
                if term in documents_with_term:
                    documents_with_term[term] += 1
                else:
                    documents_with_term[term] = 1
        total_words_in_document = len(line_terms)
        for term in temp_tf:
            temp_tf[term] = temp_tf[term] / total_words_in_document
        tf[page['url']] = temp_tf

    n = len(list_data)  # Total number of crawled web pages
    for df_term in documents_with_term:
        tf_idf[df_term] = []
        idf[df_term] = 1 + math.log10(n / (documents_with_term[df_term] + 0.1))
        for url, content in tf.items():
            if df_term in content.keys():
                score = content[df_term] * idf[df_term]
                tf_idf[df_term].append({'url': url, 'score': score})

    with open('inverted_index.json', 'w') as output:
        output.write(json.dumps(tf_idf))
    return

if __name__=='__main__':
    index()
