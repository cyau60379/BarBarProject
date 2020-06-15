import math
import random


def grasp_sr(loc_list, max_path_len):
    path = [loc_list[0], loc_list[0]]  # initial path
    indexes = [0, 0]
    prev_path = []
    blocked_index = -1
    while prev_path != path:  # construction phase, repeat until path is unchanged
        prev_path = path.copy()
        path, indexes, blocked_index = add_location(loc_list, path, indexes, max_path_len)
    path, indexes = local_search(loc_list, path, indexes, max_path_len, blocked_index)  # local search phase
    return path, path_rewards(path), path_length(path)


def add_location(loc_list, path, indexes, max_path_len, blocked_index=-1):
    updated_path, updated_indexes = path.copy(), indexes.copy()
    candidate_list = []  # a candidate list of solutions
    for i in range(len(loc_list)):
        if i not in indexes and i != blocked_index:
            path_2, indexes_2 = insertion(loc_list, path, indexes, i)
            if path_length(path_2) <= max_path_len:
                candidate_list.append((path_2, indexes_2))
            else:  # segment remove phase
                beta = 1
                for alpha in range(1, len(path_2) - 2):
                    if beta < alpha:
                        beta = alpha
                    path_3 = path_2[:alpha] + path_2[beta + 1:]
                    indexes_3 = indexes_2[:alpha] + indexes_2[beta + 1:]
                    while (beta + 1 < len(path_2)) and (path_length(path_3) > max_path_len):
                        beta += 1
                        path_3 = path_2[:alpha] + path_2[beta + 1:]
                        indexes_3 = indexes_2[:alpha] + indexes_2[beta + 1:]
                    if path_length(path_3) <= max_path_len:
                        if (path_rewards(path_3) > path_rewards(path)) \
                                or (path_rewards(path_3) == path_rewards(path)
                                    and path_length(path_3) < path_length(path)):
                            candidate_list.append((path_3, indexes_3))
        if candidate_list:
            candidate_list_2 = restrict(candidate_list)
            updated_path, updated_indexes = random.choice(candidate_list_2)
    return updated_path, updated_indexes, blocked_index


def local_search(loc_list, path, indexes, max_path_len, blocked_index):
    updated_path, updated_indexes = path.copy(), indexes.copy()
    prev_updated_path = []
    while prev_updated_path != updated_path:  # repeat until updated_path is unchanged
        prev_updated_path = updated_path.copy()
        for i in range(1, len(path) - 1):
            path_2, indexes_2 = remove(updated_path, updated_indexes, i)
            path_2, indexes_2 = two_opt(path_2, indexes_2)
            blocked_location_index = blocked_index  # index of blocked location from updated_indexes
            prev_path_2 = []
            while prev_path_2 != path_2:  # repeat until path_2 is unchanged
                prev_path_2 = path_2.copy()
                path_2, indexes_2, blocked_index = add_location(loc_list, path_2, indexes_2, max_path_len,
                                                                blocked_location_index)
            if (path_rewards(path_2) > path_rewards(updated_path)) \
                    or (path_rewards(path_2) == path_rewards(updated_path)
                        and path_length(path_2) < path_length(updated_path)):
                updated_path = path_2.copy()
                updated_indexes = indexes_2.copy()
    return updated_path, updated_indexes


def insertion(loc_list, path, indexes, i):
    path_2 = path[:1] + [loc_list[i]] + path[1:]
    indexes_2 = indexes[:1] + [i] + indexes[1:]
    diff = path_length(path_2) - path_length(path)
    for j in range(2, len(path)):
        path_2_test = path[:j] + [loc_list[i]] + path[j:]
        indexes_2_test = indexes[:j] + [i] + indexes[j:]
        diff_test = path_length(path_2_test) - path_length(path)
        if diff_test < diff:
            path_2 = path_2_test.copy()
            indexes_2 = indexes_2_test.copy()
    return path_2, indexes_2


def remove(path, indexes, i):
    path_2 = path[:i] + path[i + 1:]
    indexes_2 = indexes[:i] + indexes[i + 1:]
    return path_2, indexes_2


def path_length(path):
    result = 0
    for i in range(1, len(path)):
        result += euclidean_distance(path[i - 1][0], path[i][0])
    return result


def euclidean_distance(x, y):
    return math.sqrt(sum([(a - b) ** 2 for a, b in zip(x, y)]))


def path_rewards(path):
    result = 0
    for elem in path:
        result += elem[1]
    return result


def restrict(candidate_list, c_best=0.2):
    max_reward = 0
    for path, indexes in candidate_list:
        rewards_test = path_rewards(path)
        if rewards_test > max_reward:
            max_reward = rewards_test

    # only keep the candidates which have at least c_best% of the max reward, here 20%
    candidate_list_2 = [(p, i) for p, i in candidate_list if path_rewards(p) >= c_best * max_reward]
    return candidate_list_2


def two_opt(path, indexes):
    current_distance = path_length(path)
    best_distance = current_distance - 1
    while best_distance < current_distance:
        current_distance = best_distance
        start_again = True
        while start_again is True:
            start_again = False
            best_distance = path_length(path)
            for i in range(1, len(path) - 2):
                for k in range(i + 1, len(path) - 1):
                    new_path = two_opt_swap(path, i, k)
                    new_indexes = two_opt_swap(indexes, i, k)
                    new_distance = path_length(new_path)
                    if new_distance < best_distance:
                        path = new_path.copy()
                        indexes = new_indexes.copy()
                        start_again = True
                        break
                if start_again is True:
                    break
    return path, indexes


def two_opt_swap(route, i, k):
    new_route = route[:i - 1] + route[i - 1:k][::-1] + route[k:]
    return new_route


if __name__ == '__main__':
    locations = [((0, 0), 0), ((0, 1), 5), ((0, 2), 5),
                 ((1, 0), 5), ((1, 1), 5), ((1, 2), 5),
                 ((2, 0), 5), ((2, 1), 5), ((2, 2), 1)]
    max_len = 9
    final_path, reward, length = grasp_sr(locations, max_len)
    print(f'with max_len {max_len}\nfinal_path: {final_path}\nreward: {reward}\nlength: {length}')
