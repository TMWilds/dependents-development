import json
from collections import defaultdict

import utils

"""
createTreeFromEdges constructs a directed graph structure from a set of directed edges and a set of vertices. The set
of edges and vertices used must contain a single root vertex.
"""
def createTreeFromEdges(edges, vertices, group, project, sub_node_label, sub_node_id):
    nodes = {}
    forest = []

    driver = utils.get_neo4j()
    with driver.session() as session:
        result = session.read_transaction(dependent_method_usage, group, project, sub_node_label, sub_node_id)

        node_usages = {}
        for record in result:
            node = record.get('node')

            object_to_return = {}
            object_to_return['label'] = list(getattr(node, '_labels'))[0]
            object_to_return['id'] = getattr(node, '_properties').get('id')
            object_to_return['usage'] = record.get("usage")
            object_to_return['project'] = getattr(record.get("proj"), '_properties').get('id')
            object_to_return['distinct_usage'] = record.get("usage_dist")
            object_to_return['properties'] = getattr(node, '_properties')
            object_to_return['name'] = "{}: {}".format(
                object_to_return.get('label'), object_to_return.get('id'))
            node_usages[object_to_return['id']] = object_to_return

    driver.session().close()

    for node_id in vertices.keys():
        nodes[node_id] = { 'id': node_id, "name": getattr(vertices[node_id], '_properties').get('id'), "properties": getattr(vertices[node_id], '_properties'), "label": list(getattr(vertices[node_id], '_labels'))[0], "size": 1,  "children": [] }
        id = nodes[node_id]["properties"]["id"]
        nodes[node_id]["id"] = getattr(vertices[node_id], '_properties').get('id')
        nodes[node_id]["name"] = nodes[node_id]["id"].split('.')[-1]
        nodes[node_id]["size"] = node_usages[id]["usage"]
        nodes[node_id]["value"] = node_usages[id]["usage"]
        nodes[node_id]["usage"] = node_usages[id]["usage"]
        nodes[node_id]["distinct_usage"] = node_usages[id]["distinct_usage"]
        nodes[node_id]["label"] = node_usages[id]["label"]
        nodes[node_id]["project"] = node_usages[id]["project"]
        forest.append(nodes[node_id])

    # Must remove shortest paths to ensure there is no duplication. Java hiearchy naming can be used to ensure only direct children are linked.
    # The issue is that project names at the top level don't follow this pattern, so extra work must be done to identify which children are direct children of the
    # project level.
    roots = []
    for i in edges:
        parent_id, child_id = i
        if nodes[parent_id]["project"] == nodes[parent_id]["id"]:
            roots.append(nodes[child_id]["id"])

    tmp = roots.copy()
    for outer_root in tmp:
        roots = [root for root in roots if not root.startswith(outer_root) or root == outer_root]

    for i in edges:
        parent_id, child_id = i

        if nodes[parent_id]["project"] == nodes[parent_id]["id"] and nodes[child_id]["id"] in roots or nodes[parent_id]["id"] + '.' + nodes[child_id]["id"].split(".")[-1] == nodes[child_id]["id"]:

            node = nodes[child_id]
            parent = nodes[parent_id]

            parent['children'].append(node)

            if (node in forest):
                forest.remove(node)

    #forest is now a graph, with a single root vertex
    return forest

"""Returns the total and distinct usage of methods for all dependents for given group and project"""
def dependent_method_usage(tx, group, project, sub_node_label, sub_node_id):
    match = '''
        MATCH p = (proj:Project)-[r:Contains*0..]->(x)-[l:Contains*0..]->(i:Method)-[:Calls]->(m:Method)<-[:Contains*0..]-(y:{2} {{id: "{3}"}})<-[:Contains*0..]-(:Project {{id: "{0}/{1}"}})
        RETURN proj as proj, x as node, count(distinct m) as usage_dist, count(m) as usage
        UNION
        MATCH p = (proj:Project)-[r:Contains*0..]->(i:Method)-[:Calls]->(m:Method)<-[:Contains*0..]-(y:{2} {{id: "{3}"}})<-[:Contains*0..]-(:Project {{id: "{0}/{1}"}})
        RETURN proj as proj, i as node, count(distinct m) as usage_dist, count(m) as usage
        '''.format(group, project, sub_node_label, sub_node_id)
    print(match)
    return tx.run(match)


"""
ast_tree_dependent retrieves the complete AST tree of a specified dependent project, which is dependent on a specified node of a project under analysis
"""
def ast_tree_dependent_new(tx, group, project, sub_node_label, sub_node_id):

    if (sub_node_label != None and sub_node_id != None):
        match = '''
            MATCH p = (proj:Project)-[r:Contains*]->(x)
            WHERE (x)-[:Calls]->(:Method)<-[:Contains*0..]-(:{} {{id: "{}"}})<-[:Contains*0..]-(:Project {{id: "{}/{}"}})
            UNWIND nodes(p) AS Vertex
            WITH proj as proj, collect(DISTINCT Vertex) as nodes, collect(relationships(p)) as paths
            UNWIND paths AS Edges
            UNWIND Edges as Edge
            WITH proj as proj, nodes, [r in collect(distinct Edge) | [id(startNode(r)),id(endNode(r))]] as rels
            RETURN proj, size(nodes),size(rels),nodes,rels
            '''.format(sub_node_label, sub_node_id, group, project)

        print(match)
    else:
        match = '''
            MATCH p = (proj:Project)-[r:Contains*0..]->(x)-[l:Contains*0..]->(i:Method)-[:Calls]->(:Method)<-[:Contains*0..]-(:Project {{id: "{}/{}"}})
            WITH proj as proj, collect(DISTINCT x) as nodes, collect(DISTINCT i) as other_nodes, [r in collect(distinct last(r)) | [id(startNode(r)),id(endNode(r))]] as rels, [l in collect(distinct last(l)) | [id(startNode(l)),id(endNode(l))]] as other_rels
            RETURN proj, size(nodes),size(rels), size(other_nodes), size(other_rels), nodes, rels, other_nodes, other_rels
            '''.format(group, project)

    print(match)
    result = tx.run(match)

    dependents = []
    for record in result:
        rels = []
        nodes = {}
        rels = rels + [x for x in record.get("rels") if x not in rels]

        for node in record.get("nodes"):
            nodes[node.id] = node

        dependents.append(createTreeFromEdges(rels, nodes, group, project, sub_node_label, sub_node_id)[0])

    return {"id": project, "name": project, "children": dependents, "size": 2, "value": 2}

"""
ast_tree_dependent retrieves the complete AST tree of a specified dependent project, which is dependent on a specified node of a project under analysis
"""
def ast_tree_dependent(tx, group, project, dependent_group, dependent_project, sub_node_label, sub_node_id):

    if (sub_node_label != None and sub_node_id != None):
        match = '''
            MATCH p = (:Project {{id: "{}/{}"}})-[r:Contains*0..]->(x)-[l:Contains*0..]->(i:Method)-[:Calls]->(:Method)<-[:Contains*0..]-(y:{} {{id: "{}"}})<-[:Contains*0..]-(:Project {{id: "{}/{}"}})
            WITH collect(DISTINCT x) as nodes, collect(DISTINCT i) as other_nodes, [r in collect(distinct last(r)) | [id(startNode(r)),id(endNode(r))]] as rels, [l in collect(distinct last(l)) | [id(startNode(l)),id(endNode(l))]] as other_rels
            RETURN size(nodes),size(rels), size(other_nodes), size(other_rels), nodes, rels, other_nodes, other_rels
            UNION
            MATCH p = (:Project {{id: "{}/{}"}})-[r:Contains*0..]->(x)-[l:Contains*0..]->(i:Method)-[:Calls]->(y:{} {{id: "{}"}})<-[:Contains*0..]-(:Project {{id: "{}/{}"}})
            WITH collect(DISTINCT x) as nodes, collect(DISTINCT i) as other_nodes, [r in collect(distinct last(r)) | [id(startNode(r)),id(endNode(r))]] as rels, [l in collect(distinct last(l)) | [id(startNode(l)),id(endNode(l))]] as other_rels
            RETURN size(nodes),size(rels), size(other_nodes), size(other_rels), nodes, rels, other_nodes, other_rels
            '''.format(dependent_group, dependent_project, sub_node_label, sub_node_id, group, project, dependent_group, dependent_project, sub_node_label, sub_node_id, group, project)

        print(match)
        result = tx.run(match)
    else:
        match = '''
            MATCH p = (:Project {{id: "{}/{}"}})-[r:Contains*0..]->(x)-[l:Contains*0..]->(i:Method)-[:Calls]->(:Method)<-[:Contains*0..]-(:Project {{id: "{}/{}"}})
            WITH collect(DISTINCT x) as nodes, collect(DISTINCT i) as other_nodes, [r in collect(distinct last(r)) | [id(startNode(r)),id(endNode(r))]] as rels, [l in collect(distinct last(l)) | [id(startNode(l)),id(endNode(l))]] as other_rels
            RETURN size(nodes),size(rels), size(other_nodes), size(other_rels), nodes, rels, other_nodes, other_rels
            '''.format(dependent_group, dependent_project, group, project)

    print(match)
    result = tx.run(match)

    to_return = []
    rels = []
    nodes = {}
    for record in result:
        rels = rels + [x for x in record.get("rels") if x not in rels]
        rels = rels + [x for x in record.get("other_rels") if x not in rels]

        for node in record.get("nodes"):
            nodes[node.id] = node

        for node in record.get("other_nodes"):
            nodes[node.id] = node

    return createTreeFromEdges(rels, nodes)

    # return to_return

# retrieves dependent projects of the specific node
def dependents_from_node(tx, group, project, node_label, node_id):
    if (node_label != None and node_id != None):
        match = '''
            MATCH (:Project {{ id: '{}/{}' }})-[:Contains*]->(:{} {{id: '{}'}})-[:Contains*]->(m:Method)<-[:Calls]-(:Method)<-[:Contains*]-(d:Project)
            RETURN d, COUNT(DISTINCT m) as v
            UNION
            MATCH (:Project {{ id: '{}/{}' }})-[:Contains*]->(m:{} {{id: '{}'}})<-[:Calls]-(:Method)<-[:Contains*]-(d:Project)
            RETURN d, COUNT(DISTINCT m) as v
            '''.format(group, project, node_label, node_id, group, project, node_label, node_id)

        print(match)
        result = tx.run(match)
    else:
        match = '''
            MATCH (:Project {{ id: '{}/{}' }})-[:Contains*]->(m:Method)<-[:Calls]-(:Method)<-[:Contains*]-(d:Project)
            RETURN d, COUNT(DISTINCT m) as v
            '''.format(group, project)

        print(match)
        result = tx.run(match)


    to_return = []
    for record in result:
        node = record.get('d')
        
        object_to_return = {}
        object_to_return['label'] = list(getattr(node, '_labels'))[0]
        object_to_return['id'] = getattr(node, '_properties').get('id')
        object_to_return['value'] = record.get("v")
        object_to_return['properties'] = getattr(node, '_properties')
        object_to_return['name'] = "{}: {}".format(object_to_return.get('label'), object_to_return.get('id'))

        to_return.append(object_to_return)

    return to_return

def project_hierarchy(tx, group, project):
    """Returns the project hierarchy, excluding methods that are not used by any other projects.
    Useful for retrieving a filtered down representation of the analysed project that is relevent to dependent analysis."""
    dependent_project_string = ""
    match = '''
        MATCH (p:Project {{ id: '{}/{}' }})-[:Contains*]->(c)-[:Contains*]->(:Method)<-[:Calls]-(:Method)<-[:Contains*]-(d:Project {})
        RETURN c, COUNT(DISTINCT d) as v, COUNT(d) as w
        UNION
        MATCH (p:Project {{ id: '{}/{}' }})-[:Contains*]->(c:Method)<-[:Calls]-(:Method)<-[:Contains*]-(d:Project {})
        RETURN c, COUNT(DISTINCT d) as v, COUNT(d) as w
        '''.format(group, project, dependent_project_string, group,
                   project, dependent_project_string)
    print(match)
    result = tx.run(match)

    tmp = []
    for node in result.graph().nodes:
        print(node)
        print(node)

    print(result.graph())
    print(result.graph().nodes)
    print(result.graph().relationships)
    for record in result:
        print(record)
        node = record.get('c')

        object_to_return = {}
        object_to_return['label'] = list(getattr(node, '_labels'))[0]
        object_to_return['id'] = getattr(node, '_properties').get('id')
        object_to_return['value'] = record.get("w")
        object_to_return['size'] = record.get("w")
        object_to_return['dependent_projects'] = record.get("v")
        object_to_return['properties'] = getattr(node, '_properties')
        object_to_return['name'] = "{}: {}".format(
            object_to_return.get('label'), object_to_return.get('id'))
        object_to_return['children'] = []
        object_to_return[
            'retrieve_children_url'] = "{}/project/{}/{}/retrieve/children?label={}&id={}".format(
            utils.get_domain(), group, project, object_to_return.get('label'),
            object_to_return.get('id'))

        tmp.append(object_to_return)

    payload = {}
    current_layer = payload
    print(json.dumps(tmp))
    for obj in tmp:
        found = False
        while found:
            if obj["id"].startswith(current_layer["name"]):
                current_layer["children"].append({
                    "id": obj["id"],
                    "value": obj["value"],
                    "size": obj["size"],
                    "label": obj["label"],
                    "children": [],
                    "dependent_projects": obj["dependent_projects"]
                })
    to_return = tmp.copy()

    # Query returns relevant artifacts in the project, but contains no inherent
    # hierarchical data. Construct this hierarchical data structure from the
    # artifact's name.

    output = {}
    for data in to_return:
        if not output.get("id", None):
            output = {
                "id": data["id"],
                "name": data["id"].split('.')[-1],
                "value": data["value"],
                "size": data["size"],
                "label": data["label"],
                "children": [],
                "dependent_projects": data["dependent_projects"]
            }
        else:
            print("did we even get here")
            not_placed = True
            current_layer = output
            while not_placed:
                for child in current_layer["children"]:
                    print(child)
                    if data["id"].startswith(child["id"]):
                        current_layer = child
                        break
                else:
                    current_layer["children"].append({
                        "id": data["id"],
                        "name": data["id"].split('.')[-1],
                        "value": data["value"],
                        "size": data["size"],
                        "label": data["label"],
                        "children": [],
                        "dependent_projects": data["dependent_projects"]
                    })
                    not_placed = False
    return output

def all_project_dependencies(tx, group, project):
    """Return """
    match = '''
        MATCH (proj:Project)-[:Contains*]->(i:Method)-[:Calls*0..]->(m:Method)<-[:Contains*]-(:Project {{id: "{}/{}"}})
        RETURN m, i, proj
        '''.format(group, project)
    print(match)
    result = tx.run(match)
    results_list = []
    for record in result:
        callee = record.get('m')
        caller = record.get('i')
        caller_project = record.get('proj'),

        results_list.append([{
            "id": getattr(callee, '_properties').get('id'),
            "name": getattr(callee, '_properties').get('name'),
            "project": "{}/{}".format(group, project),
        }, {
            "id": getattr(caller, '_properties').get('id'),
            "name": getattr(caller, '_properties').get('name'),
            "project": getattr(caller_project[0], '_properties').get('id'),
        }])

    output = defaultdict(lambda: defaultdict())
    for pair in results_list:
        output[pair[0]['id']]['name'] = 'root.' + pair[0]['id']
        output[pair[0]['id']]['project'] = pair[0]['project']
        output[pair[0]['id']]['size'] = 1
        output[pair[0]['id']]['imports'] = []

        output[pair[1]['id']]['name'] = 'root.' + pair[1]['id']
        output[pair[1]['id']]['project'] = pair[1]['project']
        output[pair[1]['id']]['size'] = 1

        if 'root.' + pair[0]['id'] not in output[pair[1]['id']].get(
                'imports', []):
            if not output[pair[1]['id']].get('imports', None):
                output[pair[1]['id']]['imports'] = []
            output[pair[1]['id']]['imports'].append(
                'root.' + pair[0]['id']),

    return list(output.values())


def contains_from_node_legacy(tx, group, project, node_label, node_id, dependent_project_group, dependent_project_repo):
    if (dependent_project_group != None and dependent_project_repo != None):
        dependent_project_string = "{{ id: '{}/{}' }}".format(dependent_project_group, dependent_project_repo)
    else:
        dependent_project_string = ""
    
    if (node_label != None and node_id != None):
        match = '''
            MATCH (p:Project {{ id: '{}/{}' }})-[:Contains*]->(:{} {{id: '{}'}})-[:Contains]->(c)-[:Contains*]->(:Method)<-[:Calls]-(:Method)<-[:Contains*]-(d:Project {})
            RETURN c, COUNT(DISTINCT d) as v
            UNION
            MATCH (p:Project {{ id: '{}/{}' }})-[:Contains*]->(:{} {{id: '{}'}})-[:Contains]->(c:Method)<-[:Calls]-(:Method)<-[:Contains*]-(d:Project {})
            RETURN c, COUNT(DISTINCT d) as v
            '''.format(group, project, node_label, node_id, dependent_project_string, group, project, node_label, node_id, dependent_project_string)
        print(match)
        result = tx.run(match)
    else:
        match = '''
            MATCH (p:Project {{ id: '{}/{}' }})-[:Contains]->(c)-[:Contains*]->(:Method)<-[:Calls]-(:Method)<-[:Contains*]-(d:Project {})
            RETURN c, COUNT(DISTINCT d) as v
            UNION
            MATCH (p:Project {{ id: '{}/{}' }})-[:Contains]->(c:Method)<-[:Calls]-(:Method)<-[:Contains*]-(d:Project {})
            RETURN c, COUNT(DISTINCT d) as v
            '''.format(group, project, dependent_project_string, group, project, dependent_project_string)
        print(match)
        result = tx.run(match)

    tmp = []
    for record in result:
        node = record.get('c')

        object_to_return = {}
        object_to_return['label'] = list(getattr(node, '_labels'))[0]
        object_to_return['id'] = getattr(node, '_properties').get('id')
        object_to_return['value'] = record.get("v")
        object_to_return['properties'] = getattr(node, '_properties')
        object_to_return['name'] = "{}: {}".format(object_to_return.get('label'), object_to_return.get('id'))
        object_to_return['children'] = []
        object_to_return['retrieve_children_url'] = "{}/project/{}/{}/retrieve/children?label={}&id={}".format(utils.get_domain(), group, project, object_to_return.get('label'), object_to_return.get('id'))
        
        if (dependent_project_group != None and dependent_project_repo != None):
            object_to_return['retrieve_children_url'] = "{}&dependent_group={}&dependent_repo={}".format(object_to_return['retrieve_children_url'], dependent_project_group, dependent_project_repo)

        tmp.append(object_to_return)

    to_return = tmp.copy()

    for this_record in tmp:
        for other_record in tmp:
            if (other_record.get('id') != this_record.get('id')):
                # If this record is a child of another record
                if (this_record.get('id').startswith(other_record.get('id'))):
                    print(this_record.get('id') + "is child of " + other_record.get('id'))

                    # remove this record
                    try:
                        to_return.remove(this_record)
                    except:
                        pass

    return to_return

def is_package_parsed(tx, groupId, artifactId):
    result = tx.run("MATCH (a:ArtifactAttribute {{id: '{}.{}.parsed', name: 'parsed'}}) RETURN a.value".format(groupId, artifactId))
    if (result == None):
            return False

    single = result.single()
    if (single == None):
            return False
    
    if (single[0] == "True"):
        return True
    
    return False

def project_exists(tx, group, project):
    result = tx.run("MATCH (p:Project {{id:'{}/{}'}}) RETURN p".format(group, project))
    if (result == None):
            return False

    single = result.single()
    if (single == None):
            return False
  
    return True

def artifact_exists(tx, groupId, artifactId):
    result = tx.run("MATCH (a:Artifact {{id:'{}.{}'}}) RETURN a".format(groupId, artifactId))
    if (result == None):
            return False

    single = result.single()
    if (single == None):
            return False
    
    return True

def get_project_packages(tx, group, repo):
    query_string = "MATCH (p:Project {{id:'{}/{}'}})-[:Contains]->(a:Artifact) RETURN a.group, a.artifact".format(group, repo)
    print (query_string)

    to_return = []
    result = tx.run(query_string)
    for record in result:
        print (record)
        to_return.append({'group': record.get('a.group'), 'artifact': record.get('a.artifact')})
    
    return to_return

def get_project_dependents(tx, groupId, artifactId):
    query_string_parsed = "MATCH (p:Project {{id:'{}/{}'}})-[:Contains]->(:Artifact)<-[:Depends]-(:Artifact)<-[:Contains]-(d:Project)-[:Contains]->(:Artifact)-[:Attribute]-(a:ArtifactAttribute {{name:'total_count'}}) RETURN DISTINCT d.id, SUM(DISTINCT toInteger(a.value)) as v".format(groupId, artifactId)
    query_string_unparsed = "MATCH (p:Project {{id:'{}/{}'}})-[:Contains]->(:Artifact)<-[:Depends]-(:Artifact)<-[:Contains]-(d:Project) RETURN DISTINCT d.id".format(groupId, artifactId)
    
    to_return = []
    size = 0
    result_parsed = tx.run(query_string_parsed)
    result_unparsed = tx.run(query_string_unparsed)
    for record in result_parsed:
        print (record)
        to_return.append({'github_short_url': record.get('d.id'), 'dependents_count': record.get('v')})
        size = size + 1

    for record in result_unparsed:
        print (record)
        to_return.append({'github_short_url': record.get('d.id'), 'dependents_count': "Unknown"})
        size = size + 1
    
    return {'count': size, 'projects': to_return}

def get_project_dependencies(tx, groupId, repoId):
    query_string = "MATCH (p:Project {{id:'{}/{}'}})-[:Contains]->(:Artifact)-[:Depends]->(d:Artifact) RETURN d.group, d.artifact".format(groupId, repoId)
    print (query_string)

    to_return = []
    size = 0
    result = tx.run(query_string)
    for record in result:
        print (record)
        to_return.append({'group': record.get('d.group'), 'artifact': record.get('d.artifact')})
        size = size + 1
    
    return {'count': size, 'artifacts': to_return}

def get_project_dependents_total_cached(tx, groupId, artifactId):
    query_string = "MATCH (p:Project {{id:'{}/{}'}})-[:Contains]->(:Artifact)-[:Attribute]-(d:ArtifactAttribute {{name:'total_count'}}) RETURN SUM(toInteger(d.value))".format(groupId, artifactId)
    print (query_string)
    
    result = tx.run(query_string)
    if (result == None):
        return 0

    single = result.single()
    if (single == None):
        return 0

    return single[0]

def get_artifact_dependents(tx, groupId, artifactId):
    query_string = "MATCH (a:Artifact {{id:'{}.{}'}})<-[:Depends]-(d:Artifact) RETURN d.group, d.artifact".format(groupId, artifactId)
    print (query_string)

    to_return = []
    size = 0
    result = tx.run(query_string)
    for record in result:
        print (record)
        to_return.append({'group': record.get('d.group'), 'artifact': record.get('d.artifact')})
        size = size + 1
    
    return {'count': size, 'artifacts': to_return}

def get_artifact_dependents_count(tx, groupId, artifactId):
    query_string = "MATCH (a:Artifact {{id:'{}.{}'}})<-[:Depends]-(d:Artifact) RETURN COUNT (DISTINCT d)".format(groupId, artifactId)
    print (query_string)
    result = tx.run(query_string)
    if (result == None):
        return 0

    single = result.single()
    if (single == None):
        return 0

    return single[0]

def get_transitive_artifact_dependents(tx, groupId, artifactId):
    query_string = "MATCH (a:Artifact {{id:'{}.{}'}})<-[:Depends*2]-(d:Artifact) RETURN d.group, d.artifact".format(groupId, artifactId)
    print (query_string)

    to_return = []
    size = 0
    result = tx.run(query_string)
    for record in result:
        print (record)
        to_return.append({'group': record.get('d.group'), 'artifact': record.get('d.artifact')})
        size = size + 1
    
    return {'count': size, 'artifacts': to_return}

def get_artifact_dependents_total_cached(tx, groupId, artifactId):
    query_string = "MATCH (a:Artifact {{id:'{}.{}'}})-[:Attribute]-(d:ArtifactAttribute {{name:'total_count'}}) RETURN d.value".format(groupId, artifactId)
    result = tx.run(query_string)

    if (result == None):
        return 0

    single = result.single()
    if (single == None):
        return 0

    return single[0]

def retrieve_project_attribute_value(tx, github_short_url, attribute_name):
    result = tx.run("MATCH (a:ProjectAttribute {{id: '{}.{}'}}) RETURN a.value AS value;".format(github_short_url, attribute_name))

    if (result == None):
        return None

    single = result.single()
    if (single == None):
        return None
        
    return single[0]

def retrieve_artifact_attribute_value(tx, groupId, artifactId, attribute_name):
    result = tx.run("MATCH (a:ArtifactAttribute {{id: '{}.{}.{}'}}) RETURN a.value AS value;".format(groupId, artifactId, attribute_name))

    if (result == None):
        return None

    single = result.single()

    if (single == None):
        return None

    return single[0]