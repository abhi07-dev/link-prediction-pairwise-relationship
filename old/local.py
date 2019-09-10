def calculate_simple_features(instances, inbound, outbound, returning_list = None):
    """
    This function will create 4 simple features in a given order: inbound edges of A, outbound edges of A,
    inbound edges of B and outbound edges of B
    :param instances: list of instances (A, B)
    :param inbound: dict {base node <- list of inner nodes}
    :param outbound: dict {base node -> list of outer nodes}
    :param returning_list: list of instances with dict {feature => value}. If None, will be created one
    :return: list of instances with dict {feature => value} updated
    """
    is_return_created = False
    if returning_list is None:
        is_return_created = True
        returning_list = list()

    for i in range(len(instances)):
        a, b = instances[i]

        if a in inbound:
            a_in = len(inbound[a])
        else:
            a_in = 0

        if a in outbound:
            a_out = len(outbound[a])
        else:
            a_out = 0

        if b in inbound:
            b_in = len(inbound[b])
        else:
            b_in = 0

        if b in outbound:
            b_out = len(outbound[b])
        else:
            b_out = 0

        if is_return_created:
            returning_list.append({
                'a_in': a_in,
                'a_out': a_out,
                'b_in': b_in,
                'b_out': b_out
            })
        else:
            returning_list[i].update({
                'a_in': a_in,
                'a_out': a_out,
                'b_in': b_in,
                'b_out': b_out
            })

    return returning_list


def calculate_common_outbound_neighbours(instances, inbound, outbound, returning_list = None):
    """
    This function will create a feature which shows length of intersection of outbounds of A and B
    :param instances: list of instances (A, B)
    :param inbound: dict {base node <- list of inner nodes}
    :param outbound: dict {base node -> list of outer nodes}
    :param returning_list: list of instances with dict {feature => value}. If None, will be created one
    :return: list of instances with dict {feature => value} updated
    """
    is_return_created = False
    if returning_list is None:
        is_return_created = True
        returning_list = list()

    for i in range(len(instances)):
        a, b = instances[i]

        outbound_neighbours = 0
        if a in outbound and b in outbound:
            outbound_neighbours = len(list(set(outbound[a]) & set(outbound[b])))

        if is_return_created:
            returning_list.append({
                'num_common_outbound_neighbours': outbound_neighbours,
            })
        else:
            returning_list[i].update({
                'num_common_outbound_neighbours': outbound_neighbours,
            })

    return returning_list


def calculate_common_inbound_neighbours(instances, inbound, outbound, returning_list = None):
    """
    This function will create a feature which shows length of intersection of inbounds of A and B
    :param instances: list of instances (A, B)
    :param inbound: dict {base node <- list of inner nodes}
    :param outbound: dict {base node -> list of outer nodes}
    :param returning_list: list of instances with dict {feature => value}. If None, will be created one
    :return: list of instances with dict {feature => value} updated
    """
    is_return_created = False
    if returning_list is None:
        is_return_created = True
        returning_list = list()

    for i in range(len(instances)):
        a, b = instances[i]

        inbound_neighbours = 0
        if a in inbound and b in inbound:
            inbound_neighbours = len(list(set(inbound[a]) & set(inbound[b])))

        if is_return_created:
            returning_list.append({
                'num_common_inbound_neighbours': inbound_neighbours,
            })
        else:
            returning_list[i].update({
                'num_common_inbound_neighbours': inbound_neighbours,
            })

    return returning_list


def calculate_common_a_out_b_in_neighbours(instances, inbound, outbound, returning_list = None):
    """
    This function will create a feature which shows length of intersection of inbounds of A and B
    :param instances: list of instances (A, B)
    :param inbound: dict {base node <- list of inner nodes}
    :param outbound: dict {base node -> list of outer nodes}
    :param returning_list: list of instances with dict {feature => value}. If None, will be created one
    :return: list of instances with dict {feature => value} updated
    """
    is_return_created = False
    if returning_list is None:
        is_return_created = True
        returning_list = list()

    for i in range(len(instances)):
        a, b = instances[i]

        a_out_b_in_neighbours = 0
        if a in outbound and b in inbound:
            a_out_b_in_neighbours = len(list(set(outbound[a]) & set(inbound[b])))

        if is_return_created:
            returning_list.append({
                'num_common_a_out_b_in_neighbours': a_out_b_in_neighbours,
            })
        else:
            returning_list[i].update({
                'num_common_a_out_b_in_neighbours': a_out_b_in_neighbours,
            })

    return returning_list

def does_edge_b_to_a_exist(instances, inbound, outbound, returning_list = None):
    """
    This function will check if edge from B to A exists. Yes=1, No=0
    :param instances: list of instances (A, B)
    :param inbound: dict {base node <- list of inner nodes}
    :param outbound: dict {base node -> list of outer nodes}
    :param returning_list: list of instances with dict {feature => value}. If None, will be created one
    :return: list of instances with dict {feature => value} updated
    """
    is_return_created = False
    if returning_list is None:
        is_return_created = True
        returning_list = list()

    for i in range(len(instances)):
        a, b = instances[i]

        exist = 0
        if b in outbound and a in outbound[b]:
            exist = 1

        if is_return_created:
            returning_list.append({
                'b_to_a_exists': exist,
            })
        else:
            returning_list[i].update({
                'b_to_a_exists': exist,
            })

    return returning_list

def calculate_mutual_two_way_edges_for_a(instances, inbound, outbound, returning_list = None):
    """
    Count how many mutual following B node has
    :param instances: list of instances (A, B)
    :param inbound: dict {base node <- list of inner nodes}
    :param outbound: dict {base node -> list of outer nodes}
    :param returning_list: list of instances with dict {feature => value}. If None, will be created one
    :return: list of instances with dict {feature => value} updated
    """
    is_return_created = False
    if returning_list is None:
        is_return_created = True
        returning_list = list()

    for i in range(len(instances)):
        a, _ = instances[i]

        mutual = 0
        if a in outbound:
            for node in outbound[a]:
                if node in outbound and a in outbound[node]:
                    mutual += 1

        if is_return_created:
            returning_list.append({
                'mutual_following_a': mutual,
            })
        else:
            returning_list[i].update({
                'mutual_following_a': mutual,
            })

    return returning_list