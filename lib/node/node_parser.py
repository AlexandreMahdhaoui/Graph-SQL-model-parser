from lib.schema.schema import Schema


def _get_types() -> dict:
    import os
    import importlib
    from lib.utils.string_converter import StringConverter as sc
    """
    Function `_get_types()` returns all class types stored in `/lib/node/types`
    The class describing the `node_type` must have the same name as its `.py` file.
    
    !! PLEASE NAME THE FILE AND THE CLASS RESPECTIVELY IN SNAKE AND PASCAL CASE !! 
    
    :return: dict
    """
    type_dict = dict()
    type_list = [x.name.replace('.py', '')
                 for x in os.scandir(os.path.join('lib', 'node', 'types'))
                 if not x.name.startswith('_')]
    for t in type_list:
        type_dict[t] = importlib.import_module('lib.node.types.{}'.format(t)).__dict__.get('{}'.format(sc.snake_to_pascal(t)))
    return type_dict


class NodeParser:
    type_dict: dict = _get_types()
    schema = Schema()

    @classmethod
    def parse(cls, nodes, edges):
        """
        
        :param nodes: list from json.load(request-data.json)['nodes']
        :param edges: list from json.load(request-data.json)['edges']
        :return: parsed query
        """
        nodes = cls._refactor_nodes(nodes)
        input_keys = cls._get_inputs(nodes)
        schemas = dict()
        parsed = list()

        schemas, parsed = cls._compute_inputs(input_keys, nodes, schemas, parsed)
        schemas, parsed = cls._compute_edged_nodes(edges, nodes, schemas, parsed)

        return cls._join(parsed)

    @classmethod
    def _parse_node(
            cls,
            node_dict: dict,
            current_node: str,
            origin_node: str,
            origin_schema: list,
            is_input=False,
            is_output=False
    ):
        node_type = node_dict.get('type')
        node_class = cls.type_dict.get(node_type)
        schema, parsed = node_class.parsed(origin_node=origin_node,
                                           origin_schema=origin_schema,
                                           **node_dict)
        return (schema, cls._format_node(current_node=current_node,
                                         parsed=parsed,
                                         is_input=is_input,
                                         is_output=is_output))

    @classmethod
    def _compute_inputs(
            cls,
            input_keys: list,
            nodes: dict,
            schemas: dict,
            parsed: list
    ):
        schemas, parsed = schemas.copy(), parsed.copy()
        for k in input_keys:
            node_dict = nodes.get(k)
            table_name = node_dict.get('transformObject').get('tableName')
            origin_schema = cls.schema[table_name]
            s, p = cls._parse_node(node_dict=node_dict,
                                   current_node=k,
                                   origin_node=table_name,
                                   origin_schema=origin_schema,
                                   is_input=True)
            schemas[k] = s
            parsed.append(p)
        return schemas, parsed

    @classmethod
    def _compute_edged_nodes(
            cls,
            edges: list,
            nodes: dict,
            schemas: dict,
            parsed: list
    ):
        schemas, parsed = schemas.copy(), parsed.copy()
        len_ = (len(edges) - 1)
        for i, e in enumerate(edges):
            origin_node = e.get('from')
            origin_schema = schemas.get(origin_node)
            current_node = e.get('to')
            s, p = cls._parse_node(node_dict=nodes.get(current_node),
                                   current_node=current_node,
                                   origin_node=origin_node,
                                   origin_schema=origin_schema,
                                   is_output=(len_ == i))
            schemas[current_node] = s
            parsed.append(p)
        return schemas, parsed

    @classmethod
    def _format_node(
            cls,
            current_node,
            parsed,
            is_input=False,
            is_output=False
    ):
        if is_input:
            "WITH {} as ({})".format(current_node, parsed)
        if is_output:
            return "{} as ({})\n SELECT * FROM {};".format(current_node, parsed, current_node)
        return "{} as ({})".format(current_node, parsed)

    @classmethod
    def _join(cls, parsed_nodes):
        template = ",\n"
        return template.join(parsed_nodes)

    @classmethod
    def _refactor_nodes(cls, nodes):
        return {x.get('key'): x for x in nodes}

    @classmethod
    def _get_inputs(cls, nodes) -> list:
        return [k for k, v in nodes.items() if v.get('type') == 'INPUT']
