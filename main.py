import os
from lib.lib_api import LibApi
from lib.schema.schema import Schema
from util import get_data

cheese = """CREATE TABLE `cheese` (
  `id`		int(11) NOT NULL,
  `name`	varchar(50) NOT NULL,
  `price`	float DEFAULT NULL,
  PRIMARY KEY (`id`)
)"""

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

    # Adding/removing new Schemas
    LibApi.add_schema(cheese)
    print(Schema()['cheese'])
    LibApi.remove_schema('cheese')
