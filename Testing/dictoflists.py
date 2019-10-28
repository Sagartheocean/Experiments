#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright 2015 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# "Copyright 2018 Google LLC. This software is provided as-is, without warranty or representation for any use or purpose.
# Your use of it is subject to your agreements with Google."

"""This script grabs tweets from a PubSub topic, and stores them in BiqQuery
using the BigQuery Streaming API.


TODO://

1. If there is not data for a specified time , and we have some data in buffer
And flush it after some time.

"""


import csv
import logging
import re
import string


import custom_search_local


def read_csv_file(csv_file_name):
    """function: read_csv_file

        This function reads the first column of the csv file
        Input args:
            csvFileName: fully qualified name of the csv file
        Output:
            csv_as_list: returns the list object holding the value of first column of all rows present in csv file
    """
    internal_list = []
    external_list = []

    with open(csv_file_name, 'r')as f:
        reader = csv.reader(f)
        for row in reader:
            if str(row[1]) == "Internal":
                internal_list.append(row[0].strip())
            elif str(row[1]) == 'External':
                external_list.append(row[0].strip())
    dict_list = {"internal": internal_list, "external": external_list}

    if "bracer after shave" in dict_list.get("internal"):
        print("element in internal list")
    elif "bracer after shave" in dict_list.get("external"):
        print("element in external list")
    print(dict_list)
    return dict_list


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


def search_within(list_of_keywords, string):
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

if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    input_list = [
        "(hills OR hill's) balance",
        "\"irish spring\" travel",
        "afta pre shave",
        "(oral-b OR oralb) (anti-microbial OR antimicrobial)",
        "\"oral-b white pro\"",
        "(oral-b OR oralb) black",
        "\"dove refresh\""
    ]

    list_of_lists = [
        ["colgate palmolive", "internal", "colgate-brand"],
        ["oralb", "external", "oralb brand"],
        ["alta md", "internal", "alta md brand"]
    ]
    custom_search_local.search_matching_rules(list_of_lists, "Colgate and oralb both compete for alta md but palmolive wins")
    search_string ="(oral-b OR oralb) (anti-microbial OR antimicrobial) black"
    str1= "1 Dove refresh has been phenomenal after shave braun when you compare it with oral-b black, even if better that anti-microbial products"
    search_within(input_list,str1)
    str1 = "2 Dove has been refresh phenomenal braun when you compare it with oral-b black, even if better that anti-microbial products"
    search_within(input_list, str1)
    str1 = "3 Dove refresh has been phenomenal when you compare it with oralb black, even if better that anti-microbial products"
    search_within(input_list, str1)
    str1 = "4 Dove refresh has been phenomenal  braun when you compare it with oral-b, even if better that antimicrobial products"
    search_within(input_list, str1)
    str1 = "5 Nothing matching has been passed here"
    search_within(input_list, str1)
    str1 = "6 Dove and antimicrobial black is performing well with oral-b"
    search_within(input_list, str1)

    #read_csv_file("C:\Users\Sagar Raythatha\Downloads\EnterpriseTwitterRules.csv")