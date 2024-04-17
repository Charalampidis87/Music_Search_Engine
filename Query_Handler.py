import json
import re


def clean(text):
    text = (text.encode('ascii', 'ignore')).decode("utf-8")
    text = re.sub("&.*?;", "", text)
    text = re.sub(">", "", text)
    text = re.sub("[\]\|\[\@\,\$\%\*\&\\\(\)\":]", "", text)
    text = re.sub("-", " ", text)
    text = text.replace("'", "")
    text = text.replace("|", "")
    text = text.replace("\n", " ")
    text = re.sub("\.+", "", text)
    text = re.sub("^\s+", "", text)
    text = text.lower()
    text = text.replace("/", "")
    while "  " in text:
        text = text.replace("  ", " ")
    return text


def find_similar_term(query_term, index):  # Compare query term letters to index terms letters to find close match.
    similar_term = ''
    similar_term_score = 0
    query_letters = list(query_term)
    for index_term in index:
        matching_ordered_letters = 0
        matching_unordered_letters = 0
        index_term_letters = list(index_term)
        for position, letter in enumerate(index_term_letters):
            try:
                if letter in query_letters[position]:
                    matching_ordered_letters += 1
            except:
                continue
            if letter in query_letters:
                matching_unordered_letters += 1
        ordered_score = matching_ordered_letters / len(query_letters)
        unordered_score = matching_unordered_letters / len(query_letters) / 2
        if max(ordered_score, unordered_score) > similar_term_score:
            similar_term = index_term
            similar_term_score = max(ordered_score, unordered_score)
    return (similar_term, similar_term_score)


def search(query):
    result_list = {}
    quality_score = 0.002
    quality_results = {}
    suggestion = []
    query = str(query)
    query = clean(query).split(' ')
    query = list(filter(None, query))
    index = json.load(open('inverted_index.json'))
    i = -1 # Index i is used to create new result list for every query term which includes the results that are common with the previous term. Final results come from the last result list created
    for term in query:
        i += 1
        result_list[i] = {}
        if len(term) < 2:
            continue
        if term not in index:
            new_term = find_similar_term(term, index)
            if new_term[1] > 0.5:
                suggestion.append(new_term[0])
            else:
                suggestion.append(term)
        else:
            suggestion.append(term)
        try:
            for document in index[term]:
                if i == 0:
                    result_list[i].update({document['url']: document['score']})
                else:
                    if document['url'] in result_list[i - 1]:
                        result_list[i].update({document['url']: document['score']})
                        result_list[i][document['url']] += result_list[i-1][document['url']]
        except:
            continue
    for url, score in result_list[i].items():
        if score > quality_score:
            quality_results[url] = score
    # Sort results by score in descending order
    quality_results = dict(sorted(quality_results.items(), reverse=True, key=lambda item: item[1]))
    if suggestion == query:
        suggestion.clear()
    return (quality_results, suggestion)


if __name__ == '__main__':
    results = search(' mockingbird')
    print(results)