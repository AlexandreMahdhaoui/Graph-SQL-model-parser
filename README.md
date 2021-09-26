# Alexandre Mahdhaoui's Solution:
Please note my dedication at providing clean, documented, 
maintainable and object oriented code designed as a library API
with unit testing.

Sharing knowledge is a mindset I truly cherish and my work at your company
will always be documented and oriented to my coworkers.\
I'm a team player!

## Usage:
- #### Parse `request-data` into `result.sql`:
  - ###### Parsing a `.json` file:
      ```python
      parsed_query = LibApi.parse('/data/request-data.json', from_path=True)
      ```
  - ###### Parsing a python dictionary:
    ```python
    query = json.load(json_query)
    parsed_query = LibApi.parse(query)
    ```

  - ###### Parsing a raw json query:
    ```python
    parsed_query = LibApi.parse(json_query, is_json=True)
    ```
  - #### Adding new `NodeType`s:
    ```python
    # in `/lib/data/types`, create new file called `new_type.py`
    # Please respect snake_case for file name and PascalCase for class name.
    class NewType(NodeType):
        @classmethod
        def resolve(cls, transform_object, __origin_schema__, *args, **kwargs) -> str:
            return 'SELECT * FROM `{}`'.format(transform_object['tableName'])
    ```
- #### Adding/Removing SQL Schema:
    ```python
    >>> sql_schema = """CREATE TABLE `cheese` (
        `id`	int(11) NOT NULL,
        `name`	varchar(50) NOT NULL,
        `price`	float(11) DEFAULT NULL,
        PRIMARY KEY (`id`)
        )"""
    >>> LibApi.add_schema(sql_schema)
    Schema `cheese` has been added succesfully.
    >>> LibApi.remove_schema('cheese')
    Schema `cheese` has been deleted succesfully.
    ```
    NB: SQL schemas get parsed to retrieve their fields and types.
    SQL types get converted to python types to provide validation.

  

## Architecture decision: 
- ### Node parsing flow:
  - First step: parsing `INPUT` nodes:
    - Get `key`s of all nodes of type `INPUT`
    - Get `tableName`s and retrieve their schemas with the help of the \
    `class Schema(Subscriptable, metaclass=Singleton)`.
    Then parse those schemas into `origin_schema`s.
    - Compute all nodes `current_schemas` for further nodes
    and return their parsed SQL queries.
  - Compute `edge defined` nodes:
    - following the list of `edges` we compute each node and
    validation with the help of pre-computed `origin_schema`s. 
    - Returns parsed queries.
  - Join all parsed queries and return the `result.sql`
- ### Node types and Validation: 
  - Each columns get validated within a `node` according to the 
  `node_type` specification
  - Extendability: 
    - The `_get_types()` function in `/lib/node/node_parser.py`
    fetches all `node_type` defined in the `/lib/node/types/` folder.
    - Therefore `node_types` are easily extendable: Just create a new class 
    inheriting from `NodeType` and it will automatically be integrated.
    - Please make sure to provide the same name for the class and its file !\
    E.g.: `class TextTransformation(NodeType)` defined in 
    `text_transformation.py`.
    - Note that `_get_types()` will understand that a snake cased file
    `text_transformation` refers to the pascal cased class `TextTransformation`.
      (Please respect snake and pascal casing when dealing with `node_types`).
- ### Fields, Schemas and Validation:
  - The API access schema definitions through a `subscriptable class` provider.
  - SQL schema definitions get parsed and thus, are ready for validation.
  - `class SchemaValidator` and `class TypingValidator` are helper class used
  during `node parsing` to ensure 
  - During `node parsing`, a schema of the `current_node` data structure
  gets computed from the `origin_schema` and will be used to validate 
  further parsing stages.
  - Extendability: this API allows adding and removing schemas `LibApi.add_schema()`
  and `LibApi.remove_schema()`
    - It will also allow extendability to retrieve schema definition from database
    directly. At the moment, schemas are retrieved from a `.json` file.
- ### Bonus Point: 'Extendable structure which allows to add more types easily in the future.'
  - We discussed a bit about it, but let's discuss how the current
  structure allows extendability.
  - 
  - More complex queries: The current `A -> B -> C -> D -> E` flow 
  of example is quite "simple". \
  The way I designed the parsing stages allow us to create a `concatenate`\
  node-type, allowing us to compute parallel and complex SQL queries
  with several input nodes.
  - Adding more node-types:
    - Create a `new_nodetype.py` file in `lib/node/types/`
    - In this file: create a `NewNodetype` class implementing 
    the `NodeType` class.
- ### Bonus Point: 'Suggestion on how to validate the columns used inside the nodes'
  - Allowed schema validation by parsing SQL schemas, stored in 
  `lib/data/schema_definitions.json` at the moment.
  - Allowed validation during a `NodeType` parsing stage using the 
  `.validate()` method.
  - Also, we ensure in `NodeParser` only fields described 
  in the `origin_schema` of the `current_node` can be selected to prevent
  errors.
- ### Bonus Point: 'Optimize `request-data.json` json structure/schema.'
  - One change of structure I deemed mandatory is the `variable_field_name`
  of `transformObject` in the `FILTER` node-type. \
  Changed to `var_fields` and made it a `list` of `string`, even if only
  one field is selected.\
  Usage:`for f, o in  zip(var_fields, operations)`
    - `len(var_fields)` will be equal to `len(operations)`. For each
    element of `var_fields`, we will apply the corresponding operation
    described in `operations`.


NB: From `nodes` and `edges` graph theory's keywords, I've guessed the 
task might be part of a Graph Query backend engine.
I designed this API to be integrable in a whole graph query environment.

___

#### ** ATTENTION ** Please do not publicly fork this repository.

### Task

- Parse `request-data.json` into the query similar to `result.sql`. 

Inside `request-data.json` you have two properties `nodes` and `edges`, `nodes` contains all the required information to apply the transformation into Table/Query and `edges` represents how they are linked together. In each node there is a property `transformObject` which is different for each `type`
There are 5 different types of nodes used in this request

	- INPUT		-> it contains information about table and which fields to select from original table. 
	- FILTER	-> contains SQL "where" settings 
	- SORT		-> contains SQL "order by" settings 
	- TEXT_TRANSFORMATION	    -> contains information about applying some text SQL function on any column. For example UPPER, LOWER (see the digram for actual use case)
	- OUTPUT	-> contains SQL "limit" settings

Graphical representation of actual use-case:
![graphical representation](https://github.com/goes-funky/modeling-test/blob/master/graphical-representation.png?raw=true)

Use your imagination to fill in the missing information however you like to achieve the result.

### Bonus Points
 - Optimize `request-data.json` json structure/schema.
 - Extendable structure which allows to add more types easily in the future.
 - Suggestion on how to validate the columns used inside the nodes.
