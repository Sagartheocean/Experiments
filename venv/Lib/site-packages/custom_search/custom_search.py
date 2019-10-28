import re
import string


def pre_processing(list_of_keywords):

    list_keywords = []
    list_of_keywords = list_of_keywords.lower()

    # for removing braces
    m = re.findall(r"\(.*?\)", list_of_keywords)
    for element in m:
        list_of_keywords = remove_all(element, list_of_keywords)
        element = remove_all("(", element)
        element = remove_all(")", element)
        list_keywords.append(element)

    # for removing ""
    m = re.findall(r"\".*?\"", list_of_keywords)
    for element in m:
        list_of_keywords = remove_all(element, list_of_keywords)
        element = remove_all("\"", element)
        list_keywords.append(element)

    # for adding rest of the keywords in the list
    for element in list_of_keywords.split():
        list_keywords.append(element)

    return list_keywords


def search_with_criteria(list_keywords, string):
    string = string.lower()
    string_present = True
    matching_rule = []
    for keyword in list_keywords:
        if "or" in keyword:
            or_string = keyword.split(" or ")
            or_string_present = False
            for key in or_string:
                if key in string:
                    matching_rule.append(key)
                    or_string_present = True
            if not or_string_present:
                string_present = False
        else:
            if keyword in string:
                matching_rule.append(keyword)
            else:
                string_present = False
    if string_present:
        return matching_rule
    else:
        return False


def search_matching_rules(list_of_keywords, string):
    matching_rules = []
    for keyword_string in list_of_keywords:
        keyword_string = pre_processing(keyword_string)
        matching_rule = search_with_criteria(keyword_string,string)
        if matching_rule != False:
            matching_rules.append(" ".join(matching_rule))
    print matching_rules
    return matching_rules


def remove_all(substr, str):
    while string.find(str, substr) != -1:
        index = string.find(str, substr)
        str = str[0:index] + str[index+len(substr):]
    return str
