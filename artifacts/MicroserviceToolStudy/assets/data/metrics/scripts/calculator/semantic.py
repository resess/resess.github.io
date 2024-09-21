from pickle import FALSE, TRUE
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer
import sys
import csv
import math
import pandas as pd
import re
import nltk

from access.data_repository import DataRepository

nltk.download("wordnet")
nltk.download("omw-1.4")

"""
compute the class-class semantic value based on the short class name (without the package name)
only compute single direction:  c1-c2.  c2-c1 is not computed
"""

# generic stop words, apply for all apps
generic_stop_words = [
    # Task specific
    "Controller",
    "Response",
    "Handler",
    "Reference",
    "Exception",
    "Service",
    "Details",
    # Design Pattern specific
    "Singleton",
    "Multiton",
    "Factory",
    "Builder",
    "Prototype",
    "Adapter",
    "Composite",
    "Proxy",
    "Facade",
    "Bridge",
    "Decorator",
    "Mediator",
    "Observer",
    "Strategy",
    "Command",
    "State",
    "Visitor",
    "Iterator",
    "Interpreter",
    "Controller",
    "View",
    "Model",
    # JavaEE specfific
    "Servlet",
    "Bean",
    "JavaBean",
    "EnterpriseBean",
    "Socket",
    "WebSocket",
    "JSP",
    "Page",
    # 7ep-demo
    "Utils",
    "Enums",
    "Result",
    # JPetStore
    "Action",
    "Mapper",
    # PartsUnlimited
    "Repository",
    "Items",
    "Request",
    "Mongo",
    "Event",
    "Info",
    "Record",
    "Mock",
    "Filter",
    # spring-petclinic
    "Entity",
    # Methods
    # 7ep-demo
    "get",
    "set",
    "add",
    "find",
    "of",
    "by",
    "new",
    "print",
    "show",
    "trigger",
    "init",
    "is",
    "$",
    "$$",
    "$$$",
    "[]",
    "create",
    "return",
    "empty",
    "search",
    "delete",
    "clean",
    "save",
    "do",
    "post",
    "hash",
    "code",
    "list",
    "for",
    "by",
    "value",
    "values",
    "forward",
    "to",
    "string",
    "output",
    "must",
    "not",
    "be",
    "null",
    "or",
    "empty",
    "put",
    "in",
    "all",
    # JPetStore
    "status",
    "id",
    "message",
    "process",
    "init",
    "update",
    "form",
    "creation",
    "pagination",
    "paginated",
    "item"
]

# app specific stop words - populated as an argument
app_specific_words = []

# if a class name contains an ignore_word, the class is exlcuded in its entirety
ignore_words = ["package-info", "test"]


# split by hump
def splitByHump(name):
    resList = list()
    upperIndexList = list()
    upperIndexList.append(0)  # first index
    for index in range(0, len(name)):
        if name[index].isupper():
            previousLetter = name[index - 1] if index > 0 else ""
            nextLetter = name[index + 1] if index < len(name) - 1 else ""
            if (not previousLetter.isupper()) or (
                previousLetter.isupper() and nextLetter.islower()
            ):
                upperIndexList.append(index)

    upperIndexList.append(len(name))  # last index + 1

    for i in range(0, len(upperIndexList) - 1):
        index_start = upperIndexList[i]
        index_end = upperIndexList[i + 1]
        strstr = name[index_start:index_end]
        resList.append(strstr)

    resList = [each.lower() for each in resList]
    return resList


# prune word by lemmatization and removing numbers
def wordLemmatization(word):
    if re.search(r"[0-9]+", word):
        # search any-pos substring,  match from start
        m = re.search(r"[0-9]+", word)
        (start, end) = m.span()  # match pos
        if start < end:
            word = word[0:start] + word[start + 1 : end] + word[end + 1 : len(word)]
        elif start == end:
            word = word[0:start] + word[start + 1 : len(word)]

    # use a lemmatizer
    lemmatizer = WordNetLemmatizer()
    word = lemmatizer.lemmatize(word)

    if "fibonacci" in word:
        return "fib"
    if "ackermann" in word:
        return "ack"
    if "registration" in word:
        return "register"

    ## if desired, use a stemmer instead
    # stemmer = PorterStemmer()
    # word = stemmer.stem(temp)

    return word


def isAllBigLetter(word):
    if re.match(r"[A-Z_0-9]+", word):  # all capitalized
        m = re.match(r"[A-Z_0-9]+", word)
        if len(m.group()) == len(word):
            return True
    return False


def processIdentifierFile(fileName, granularity):
    classWordDict = dict()  # [classname] = [w1,w2]
    nltk.download("stopwords")
    stopWords = nltk.corpus.stopwords.words("english")
    del stopWords[stopWords.index("on")]
    stopWords.extend(generic_stop_words)
    stopWords.extend(app_specific_words)

    with open(fileName, "r") as fp:
        reader = csv.reader(fp)
        for each in reader:  # each line corresponds to a class
            longClassName = each[0]

            if "Servlet" in longClassName:
                x = 1

            # # exclude class if it is in a test directory
            # if ("test" in longClassName.lower()):
            #     continue

            tmpList = longClassName.split(".")

            if "method" in granularity:
                className = tmpList[len(tmpList) - 2] + "_" + tmpList[len(tmpList) - 1]
            else:
                className = tmpList[len(tmpList) - 1]

            # if words are all capitalized, make lowercase
            if isAllBigLetter(className):
                className = className.lower()

            # check if the class name is in the ignore_words array
            # or if any ignoreWord is a substring of className
            if (className in ignore_words) or any(
                (ignoreWord.lower() in className.lower()) for ignoreWord in ignore_words
            ):
                continue

            # split by _ and -
            # if no _ or - splits, uScoreSplitList contains only the className
            uScoreSplitList = list()
            tmpList = re.split("-|_", className)
            uScoreSplitList.extend(tmpList)

            # split by hump
            humpSplitList = list()
            for word in uScoreSplitList:
                tmpList = splitByHump(word)
                humpSplitList.extend(tmpList)

            if "entity" in humpSplitList:
                x = 1

            # filter
            wordList = list()
            for word in humpSplitList:
                if word in (stopWord.lower() for stopWord in stopWords):
                    continue
                word = wordLemmatization(word)
                if (word != "") and (len(word) > 1):
                    wordList.append(word)
            classWordDict[longClassName] = wordList
            print(className, wordList)
    return classWordDict


def writeCSV(listList, fileName):
    pd.DataFrame.from_records(listList).to_csv(fileName)
    print(f'write to file {fileName}')


# calculate class name similarity
# assume class name 1 was tokenized to a list [k1, k2]
# class name 2 tokenize to a list [k2, k3]
# then similarity = ([k1, k2] INTERSECTS [k2, k3]) / ([k1, k2] UNION [k2, k3]) = 1/3
def computedep(classWordDict):
    classdepdict = dict()  # [class1][class2] = dep
    classList = list(classWordDict.keys())
    for id1 in range(0, len(classList) - 1):
        className1 = classList[id1]
        set1 = set(classWordDict[className1])
        if className1 not in classdepdict:
            classdepdict[className1] = dict()

        for id2 in range(id1 + 1, len(classList)):
            className2 = classList[id2]
            set2 = set(classWordDict[className2])
            if len(set1 | set2) == 0:
                jaccard = 0
            else:
                jaccard = (len(set1 & set2)) / float(len(set1 | set2))
            classdepdict[className1][className2] = jaccard

    return classdepdict


# load app_specific_stopwords with provided stop words in fileName


def loadAppSpecificStopWords(fileName):
    with open(fileName, "r") as fp:
        reader = csv.reader(fp)
        for each in reader:  # each line corresponds to a stop word
            stopWord = each[0]
            app_specific_words.append(stopWord)


def getAllClassNames(fileName, granularity):
    classNames = []
    with open(fileName, "r") as fp:
        reader = csv.reader(fp)
        for each in reader:  # each line corresponds to a class
            longClassName = each[0]

            # # exclude class if it is in a test directory
            # if ("test" in longClassName.lower()):
            #     continue

            tmpList = longClassName.split(".")
            if "method" in granularity:
                # Get {class name}.{method name}
                className = tmpList[len(tmpList) - 2] + tmpList[len(tmpList) - 1]
            else:
                className = tmpList[len(tmpList) - 1]

            classNames.append(longClassName)

    return classNames


def getNodeQuality(graph, total_nodes, from_node_col_name, to_node_col_name):
    """
    graph: list
    total_nodes: int
    from_node_col_name: str
    to_node_col_name: str
    return: float

    calculate node quality of a given relationship graph. The given graph should be a list, with each row
    describe an edge. The edge is from node in col from_node_col_name to node in col to_node_col_name.
    e.g., for class names relationship, from_node_col_name = "className1" and to_node_col_name = "className2"
    """
    observed_nodes = set()
    for node in graph:
        from_node = node[from_node_col_name]
        to_node = node[to_node_col_name]
        observed_nodes.add(from_node)
        observed_nodes.add(to_node)
    total_observed_nodes = len(set(observed_nodes))
    node_quality = float(total_observed_nodes) / float(total_nodes)

    print("total_nodes: " + str(total_nodes) + "\n")
    print("total_observed_nodes: " + str(total_observed_nodes) + "\n")
    return node_quality


def getEdgeQuality(graph, total_nodes):
    """
    graph: list
    total_nodes: int
    return: float

    calculate edge quality of a given relationship graph. The given graph should be a list, with each row
    describe an edge.
    """
    total_possible_edges = (float(total_nodes) * (float(total_nodes) - 1)) / 2
    total_observed_edges = len(graph)
    edge_quality = float(total_observed_edges) / float(total_possible_edges)
    print("total_nodes: " + str(total_nodes) + "\n")
    print("total_possible_edges: " + str(total_possible_edges) + "\n")
    print("total_observed_edges: " + str(total_observed_edges) + "\n")
    return edge_quality


# python generateClassNameGraph.py classNameList.txt  classNameDependencyGraph.csv additionalAppSpecificStopWords.txt
def calculate(classFileName, classDepFileName, granularity):
    # extract arguments - file name containing class names, and the destination dependency file
    # classFileName = sys.argv[1]  # file with all Java class names
    # classDepFileName = sys.argv[2]  # the output file

    # add app specific stop words if provided
    # if len(sys.argv) == 4:
    #     appStopWordsFileName = sys.argv[3]
    #     loadAppSpecificStopWords(appStopWordsFileName)

    # generate a dictionary of all words found in the class names
    classWordDict = processIdentifierFile(classFileName, granularity)
    classDepDict = computedep(classWordDict)

    alist = list()
    for className1 in classDepDict:
        for className2 in classDepDict[className1]:
            dep = classDepDict[className1][className2]
            if float(dep) != 0.0:
                alist.append(
                    {
                        "className1": className1,
                        "className2": className2,
                        "ClassNameRel": dep,
                    }
                )

    writeCSV(alist, classDepFileName)

    # calculate quality metrics
    total_nodes = len(getAllClassNames(classFileName, granularity))
    node_quality = getNodeQuality(alist, total_nodes, "className1", "className2")
    edge_quality = getEdgeQuality(alist, total_nodes)

    print("\n========= quality metrics ==========\n")
    print("class-names, node quality = %.4f" % node_quality)
    print("class-names, edge quality = " + str(edge_quality) + "\n")


class SemanticExtractor:
    def __init__(self, data_repository: DataRepository):
        self.data_repository = data_repository

    def calculate_all(self, applications):
        for application in applications:
            for granularity in ["class_level", "method_level"]:
                node_names_file = self.data_repository.get_node_list_path(application, granularity)
                output_file = self.data_repository.get_relationship_path(application, "semantic_names", granularity)
                calculate(node_names_file, output_file, granularity)
