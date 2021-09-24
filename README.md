# Alexandre Mahdhaoui's Solution:
Please note my dedication at providing clean, documented, 
maintainable and object oriented code designed as a library API
with unit testing.

Sharing knowledge is a mindset I truly cherish and my work at your company
will always be documented and oriented to my coworkers.\
I'm a team player!

NB: From "nodes" and "edges" graph theory's keywords, I've guessed the 
task might be part of a Graph Query backend engine.
I designed this API to integrate a whole graph query environment.


## Architecture decision: 
- ### Node types and Validation: 
  - Each node gets validated from their respective node_types 
  defined in node_types.json
  - Extendability: LibApi.add_node_type() and LibApi.remove_node_type()
    - Node types could be retrieved from a database.
- ### Fields, Schemas and Validation:
  - The API access schema definitions through
  a subscriptable class provider.
  - Then schemas gets parsed to create validator. I designed the validation
  flow to be extendable.
  - Extendability: this API allows adding and removing schemas LibApi.add_schema()
  and LibApi.remove_schema()
    - It also allows extendability to retrieve schema definition from database
    directly. At the moment, schemas are retrieved from a json file.



## ** ATTENTION **
Please do not publicly fork this repository.

# Task

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

# Bonus Points
 - Optimize `request-data.json` json structure/schema.
 - Extendable structure which allows to add more types easily in the future.
 - Suggestion on how to validate the columns used inside the nodes.
