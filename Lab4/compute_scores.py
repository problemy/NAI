import argparse
import json
import numpy as np


# method calculates euclidean distance between user1 and user2
# returns 0 < e < 1 closer to 1 means user 1 match user 2 more
def euclidean_score(dataset, user1, user2):
    '''
     Function checking similarity of users movies using euclidean distance
    :param dataset: json
    :type dataset:
    :param user1: first user
    :type user1:
    :param user2: second user to compare
    :type user2:
    :return: euclidean distance
    :rtype:
    '''
    if user1 not in dataset:
        raise TypeError('Cannot find ' + user1 + ' in the dataset')

    if user2 not in dataset:
        raise TypeError('Cannot find ' + user2 + ' in the dataset')

    # Movies rated by both user1 and user2
    common_movies = {}
    for item in dataset[user1]:
        if item in dataset[user2]:
            common_movies[item] = 1

    # If there are no common movies between the users,
    # then the score is 0
    if len(common_movies) == 0:
        return 0

    squared_diff = []

    for item in dataset[user1]:
        if item in dataset[user2]:
            squared_diff.append(np.square(dataset[user1][item] - dataset[user2][item]))

    return 1 / (1 + np.sqrt(np.sum(squared_diff)))


# nie wiem jak to działa
def pearson_score(dataset, user1, user2):
    """
        Function checking similarity of users movies using pearson correlation
    :param dataset: data in json file
    :type dataset:
    :param user1: first user
    :type user1:
    :param user2: second user to compare
    :type user2:
    :return: pearson correlation
    :rtype:
    """
    if user1 not in dataset:
        raise TypeError('Cannot find ' + user1 + ' in the dataset')

    if user2 not in dataset:
        raise TypeError('Cannot find ' + user2 + ' in the dataset')

    # Movies rated by both user1 and user2
    common_movies = {}
    for item in dataset[user1]:
        if item in dataset[user2]:
            common_movies[item] = 1

    num_ratings = len(common_movies)
    # If there are no common movies between user1 and user2, then the score is 0
    if num_ratings == 0:
        return 0
    # Calculate the sum of ratings of all the common movies
    user1_sum = np.sum([dataset[user1][item] for item in common_movies])
    user2_sum = np.sum([dataset[user2][item] for item in common_movies])

    # Calculate the sum of squares of ratings of all the common movies
    user1_squared_sum = np.sum([np.square(dataset[user1][item]) for item in common_movies])
    user2_squared_sum = np.sum([np.square(dataset[user2][item]) for item in common_movies])

    # Calculate the sum of products of the ratings of the common movies
    sum_of_products = np.sum([dataset[user1][item] * dataset[user2][item] for item in common_movies])

    # Calculate the Pearson correlation score
    Sxy = sum_of_products - (user1_sum * user2_sum / num_ratings)
    Sxx = user1_squared_sum - np.square(user1_sum) / num_ratings
    Syy = user2_squared_sum - np.square(user2_sum) / num_ratings

    if Sxx * Syy == 0:
        return 0

    return Sxy / np.sqrt(Sxx * Syy)


#
class RecommendationSystem:

    def __init__(self, data, user):
        self.users_and_scores = {}
        self.most_compatible_users = []
        self.data = data
        self.user = user

    def compatibleness(self, user1):
        """
            Function checking compatibleness of user's movie lists
        :param user1:
        :type user1:
        :return:
        :rtype: int
        """
        u1_score = self.users_and_scores.get(user1)
        return (u1_score / 2) * 100

    def get_nearest_user(self, user_to_compare):
        '''
        Function getting the most similar user to compared one.
        :param user_to_compare:
        :type user_to_compare:
        :return: nearest_user
        :rtype:
        '''
        user_list = list(self.data.keys())
        user_list.remove(user_to_compare)
        highestScore = 0
        for u in user_list:
            score = pearson_score(data, user_to_compare, u) + euclidean_score(data, user_to_compare, u)
            self.users_and_scores[u] = score
            if score >= highestScore:
                highest_score = score
                nearest_user = u
        return nearest_user

    def get_nearest_users_list(self, user_to_compare):
        '''
        Function getting list of most similar users to compared one.
        :param user_to_compare:
        :type user_to_compare:
        :return: nearest_users_list
        :rtype:
        '''
        nearest = self.get_nearest_user(user_to_compare)
        sorted_nearest_users_dict = {k: v for k, v in sorted(self.users_and_scores.items(), key=lambda item: item[1])}
        for v in list(sorted_nearest_users_dict.values()):
            if v == 'orange':
                del sorted_nearest_users_dict[v]
        nearest_users_list = list(sorted_nearest_users_dict.keys())
        nearest_users_list.reverse()
        return nearest_users_list

    def get_common_movies(self, user_to_compare, nearest_user):
        '''
        Function getting movies common for compared users
        :param user_to_compare:
        :type user_to_compare:
        :param nearest_user:
        :type nearest_user:
        :return: common_movies
        :rtype:
        '''
        common_movies = []
        i = 0
        for item in self.data[user_to_compare]:
            i += 1

            if item in self.data[nearest_user]:

                common_movies.append(item)
        return common_movies

    def recommended_movies(self):
        '''
         Function getting 7 movies worth to recommend
        :return: recommended_movies
        :rtype:
        '''
        iterator = 0
        recommended_movies = []
        nearest_list = self.get_nearest_users_list(self.user)
        while len(recommended_movies) < 7:
            nearest = nearest_list[iterator]
            if nearest not in self.most_compatible_users:
                self.most_compatible_users.append(nearest)
            common = self.get_common_movies(self.user, nearest)
            for key, value in data[nearest].items():
                if key not in common and value > 8 and key not in recommended_movies:
                    recommended_movies.append(key)
            iterator += 1
        return recommended_movies[:7]

    def not_recommended_movies(self):
        '''
         Function getting 7 movies not worth to recommend
        :return: not_recommended_movies
        :rtype:
        '''
        iterator = 0
        not_recomended_movies = []
        nearestList = self.get_nearest_users_list(self.user)
        while len(not_recomended_movies) < 7:
            nearest = nearestList[iterator]
            if nearest not in self.most_compatible_users:
                self.most_compatible_users.append(nearest)
            common = self.get_common_movies(self.user, nearest)
            for key, value in self.data[nearest].items():
                if key not in common and value < 3:
                    not_recomended_movies.append(key)
            # if(iterator-1 >= len(not_recomended_movies)):
            #     print("Te filmy nie podobały się użytkownikom, który mają podobny gust do twojego:\n",
            #           not_recomended_movies)
            #     return not_recomended_movies
            iterator += 1
        return not_recomended_movies[:7]

    def immutable_remove_spaces(self, item):
        return item.replace(" ", "")

    def get_most_compatible_users(self):
        '''
        Function getting most compatible users.
        :return:most_compatible_users
        :rtype:
        '''
        return self.most_compatible_users

    def toString(self, dataList):
        '''
        Function
        :param dataList:
        :type dataList:
        :return:
        :rtype:
        '''
        i = 1
        for item in dataList:
            print(i, ". ", item)
            i += 1


def build_arg_parser():
    """
    Function building arguments parser
    :return:parser
    :rtype:
    """
    parser = argparse.ArgumentParser(description='Compute similarity score')
    parser.add_argument('--user1', dest='user1', required=True,
                        help='First user')
    # parser.add_argument('--sensitivity', dest='sensitivity', required=True,
    #                     help='Rates sensitivity')
    # parser.add_argument("--score-type", dest="score_type", required=True,
    #                     choices=['Euclidean', 'Pearson'], help='Similarity metric to be used')
    return parser


if __name__ == '__main__':
    # args = build_arg_parser().parse_args()
    # user_from_input = args.user1
    ratings_file = 'ratings2.json'

    with open(ratings_file, 'r', encoding="utf-8") as f:
        data = json.loads(f.read())
        '''
         Opening json file 
        '''
    user = input("Podaj imie i nazwisko użytkownika, któremu chcesz rekomendować filmy:")

    while user not in data.keys():
        print("Użytkownika nie ma w naszej bazie, podaj jednego z:")
        for i in data.keys():
            print("", i, ", ", end="")
        user = input()

    rSystem = RecommendationSystem(data, user)

    print("Filmy, które podobały się osobom, mającym zbliżony gust do wskazanego użytkownika: ")
    rSystem.toString(rSystem.recommended_movies())
    print("Filmy, które nie podobały się osobom, mającym zbliżony gust do wskazanego użytkownika: ")
    rSystem.toString(rSystem.not_recommended_movies())
    print("Osoby o podobnym guście do wskazanego użytkownika:")
    rSystem.toString(rSystem.get_most_compatible_users())
