import os
from lib.lib_api import LibApi
from util import get_data


if __name__ == '__main__':
    query, schema, results = get_data()
    # Unit Testing the "lib" library
    # NOT ATM os.system('python -m pytest')

    # Testing if "LibApi" expectedly resolve the task
    solution = LibApi.parse(query)
    if solution == results:
        print('_________________\n')
        print('Hoora, Alexandre Mahdhaoui\'s solution works expectedly!')
        print('_________________\n{}\n_________________'.format(solution))
