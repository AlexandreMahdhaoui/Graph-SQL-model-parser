# Alexandre Mahdhaoui's Solution:
Please note my dedication at providing clean, documented, 
maintainable and object oriented code designed as a library API
with unit testing.

Sharing knowledge is a mindset I truly cherish and my work at your company
will always be documented and oriented to my coworkers.\
I'm a team player!


## Architecture decision: 
- ### Node parsing flow:
- ### Node types and Validation: 
  - Each columns get validated within a `node` according to the 
  `node_type` specification
  - Extendability: 
    - The `_get_types()` function in `/lib/node/node_parser.py`
    fetches all `node_type` defined in the `/lib/node/types/` folder. \
    - Therefore `node_types` are easily extendable: Just create a new class 
    inheriting from `NodeType` and it will automatically be integrated.\
    - Please make sure to provide the same name for the class and its file.
    E.g.: `class TextTransformation(NodeType)` defined in `text_transformation.py` \
    - Note that `_get_types()` will automatically understand that the snake
    cased `text_transformation` refers to the pascal cased `TextTransformation`.
      (Please respect snake and pascal casing when dealing with `node_types`).
- ### Fields, Schemas and Validation:
  - The API access schema definitions through a `subscriptable class` provider.
  - SQL schema definitions get parsed and thus are ready for validation.
  - `class SchemaValidator` and `class TypingValidator` are helper class used
  during `node parsing` to ensure 
  - During `node parsing`, a schema of the current outputed data structure
  gets computed and will be used to validate further parsing stages.
  - Extendability: this API allows adding and removing schemas `LibApi.add_schema()`
  and `LibApi.remove_schema()`
    - It also allows extendability to retrieve schema definition from database
    directly. At the moment, schemas are retrieved from a `.json` file.
- ### Bonus Point: 'Suggestion on how to validate the columns used inside the nodes'
  - More than a suggestion I took the initiative to code a validation 
  flow for columns


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
