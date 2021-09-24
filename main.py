import os
from lib.lib_api import LibApi
from util import get_data


if __name__ == '__main__':
    query, schema, results = get_data()
    # Unit Testing the "lib" library
    os.system('python -m pytest')

    # Testing if "LibApi" expectedly resolve the task
    if LibApi.parse() == results:
        print('Alexandre Mahdhaoui\'s solution works expectedly')
    pass
