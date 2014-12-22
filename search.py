import re

# A search result
class Result(object):
    def __init__(self, name, magnet, size, se, le):
        # Result info
        self.name = name
        self.magnet = magnet
        self.size = size
        self.se = se
        self.le = le


class Search(object):
    def __init__(self, file_name):
        self.file_name = file_name

    def search(self, search_terms):
        # Compile regex
        regex = re.compile('"(.+)"\|([0-9]*)\|(\w+)\|([0-9])\|(\w+)\|([0-9]*)\|([0-9]*)')

        # Open database
        f = open(self.file_name, 'r')

        result_list = []

        print 'Performing search (it can take a while)...'
        for line in f:
            # Split the line
            m = regex.match(line[:-1])

            if not m:
                continue

            parts = m.groups()

            name = parts[0]
            size = parts[1]

            # If there's no hash (happens sometimes), ignore the result
            magnet = parts[2]
            if magnet == '':
                continue

            le = int(parts[5])
            se = parts[6]

            # If there's a search with more than one
            # word, eg. "David Bowie", we should split
            # "David" and "Bowie" and search for both
            # terms anywhere in the name
            all_terms = search_terms.lower().split(' ')
            filtered_terms = [t for t in all_terms if len(t) > 2]

            # Lowercase everything
            name_lower = name.lower()

            # If all the terms are in the name, add the result
            # to the result list
            if all(t in name_lower for t in filtered_terms):
                result_list.append(Result(name, magnet, size, se, le))

        f.close()

        print 'Done!'

        print 'Sorting by leecher count...'
        result_list.sort(key=lambda r: r.le, reverse=True)
        print 'Done!'

        return result_list
