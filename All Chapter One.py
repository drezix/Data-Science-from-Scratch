# Data Science from Scratch - Second Edition - Joel Grus

users = [
    { "id": 0, "name": "Hero" },
    { "id": 1, "name": "Dunn" },
    { "id": 2, "name": "Sue" },
    { "id": 3, "name": "Chi" },
    { "id": 4, "name": "Thor" },
    { "id": 5, "name": "Clive" },
    { "id": 6, "name": "Hicks" },
    { "id": 7, "name": "Devin" },
    { "id": 8, "name": "Kate" },
    { "id": 9, "name": "Klein" }
]

friendship_pairs = [(0, 1), (0, 2), (1, 2), (1, 3), (2, 3), (3, 4),
(4, 5), (5, 6), (5, 7), (6, 8), (7, 8), (8, 9)]

# Initialize the dict with an empty list for each user id:
friendships = {user["id"]: [] for user in users}
# And loop over the friendship pairs to populate it:
for i, j in friendship_pairs:
    friendships[i].append(j) # Add j as a friend of user i
    friendships[j].append(i) # Add i as a friend of user j


# First we find the total number of connections, by summing up the lengths of all the friends lists:
def number_of_friends(user):
    """How many friends does _user_ have?"""
    user_id = user["id"]
    friend_ids = friendships[user_id]
    return len(friend_ids)
    
total_connections = sum(number_of_friends(user)for user in users) # 24
    
# And then we just divide by the number of users:
num_users = len(users) # length of the users list
avg_connections = total_connections / num_users # 24 / 10 == 2.4

# It’s also easy to find the most connected people—they’re the people who have the largest numbers of friends. Since there aren’t very many users, we can simply sort them from “most friends” to “least friends”:
# Create a list (user_id, number_of_friends).
num_friends_by_id = [(user["id"], number_of_friends(user)) for user in users]
    
num_friends_by_id.sort( # Sort the list
    key=lambda id_and_friends: id_and_friends[1], # by num_friends
    reverse=True) # largest to smallest
# Each pair is (user_id, num_friends):
# [(1, 3), (2, 3), (3, 3), (5, 3), (8, 3),
# (0, 2), (4, 2), (6, 2), (7, 2), (9, 1)]

print(total_connections)
print(num_users)
print(avg_connections)

print("------------------------------")
# Data Scientists You May Know

def foaf_ids_bad(user):
# foaf is short for "friend of a friend"
    return [foaf_id
    for friend_id in friendships[user["id"]]
    for foaf_id in friendships[friend_id]]
    
print(foaf_ids_bad(users[0]))
# When we call this on users[0] (Hero), it produces: [0, 2, 3, 0, 1, 3]
print("------------------------------")
# It includes user 0 twice, since Hero is indeed friends with both of his friends. It includes users 1 and 2, although they are both friends with Hero already. And it includes user 3 twice, as Chi is reachable through two different friends:

print(friendships[0]) # [1, 2]
print(friendships[1]) # [0, 2, 3]
print(friendships[2]) # [0, 1, 3]

print("------------------------------")
# We should probably exclude people already known to the user:
from collections import Counter # not loaded by default

def friends_of_friends(user):
    user_id = user["id"]
    return Counter(
        foaf_id
        for friend_id in friendships[user_id] # For each of my friends,
        for foaf_id in friendships[friend_id] # find their friends
        if foaf_id != user_id # who aren't me
        and foaf_id not in friendships[user_id] # and aren't my friends.
    )
    
print(friends_of_friends(users[3])) # Counter({0: 2, 5: 1})

# This correctly tells Chi (id 3) that she has two mutual friends with Hero (id 0) but only one mutual friend with Clive (id 5).

print("------------------------------")

# List of pairs (user_id, interest):

interests = [
    (0, "Hadoop"), (0, "Big Data"), (0, "HBase"), (0, "Java"),
    (0, "Spark"), (0, "Storm"), (0, "Cassandra"),
    (1, "NoSQL"), (1, "MongoDB"), (1, "Cassandra"), (1, "HBase"),
    (1, "Postgres"), (2, "Python"), (2, "scikit-learn"), (2, "scipy"),
    (2, "numpy"), (2, "statsmodels"), (2, "pandas"), (3, "R"), (3,
    "Python"),
    (3, "statistics"), (3, "regression"), (3, "probability"),
    (4, "machine learning"), (4, "regression"), (4, "decision trees"),
    (4, "libsvm"), (5, "Python"), (5, "R"), (5, "Java"), (5, "C++"),
    (5, "Haskell"), (5, "programming languages"), (6, "statistics"),
    (6, "probability"), (6, "mathematics"), (6, "theory"),
    (7, "machine learning"), (7, "scikit-learn"), (7, "Mahout"),
    (7, "neural networks"), (8, "neural networks"), (8, "deep learning"),
    (8, "Big Data"), (8, "artificial intelligence"), (9, "Hadoop"),
    (9, "Java"), (9, "MapReduce"), (9, "Big Data")
]

# Function that finds users with a certain interest

def data_scientists_who_like(target_interest):
# Find the ids of all users who like the target interest.
    return [user_id
    for user_id, user_interest in interests
    if user_interest == target_interest]

print("data scientists who like Java: " + str(data_scientists_who_like("Java")))

print("------------------------------")
# Building an index from interests to users

from collections import defaultdict
# Keys are interests, values are lists of user_ids with that interest
user_ids_by_interest = defaultdict(list)
for user_id, interest in interests:
    user_ids_by_interest[interest].append(user_id)

# Users to interests

interests_by_user_id = defaultdict(list)
for user_id, interest in interests:
    interests_by_user_id[user_id].append(interest)

print("interests by user: " + str(interests_by_user_id[0]))
print("------------------------------")
print("user id by interest: " + str(user_ids_by_interest["Java"]))
print("------------------------------")
# Finding who has the most interests in common with a given user

def most_common_interests_with(user):
    return Counter(
    interested_user_id
    for interest in interests_by_user_id[user["id"]]
    for interested_user_id in user_ids_by_interest[interest]
    if interested_user_id != user["id"]
)

print(most_common_interests_with(users[0]))
print("------------------------------")

# Salaries and Experience

salaries_and_tenures = [
    (83000, 8.7), (88000, 8.1),
    (48000, 0.7), (76000, 6),
    (69000, 6.5), (76000, 7.5),
    (60000, 2.5), (83000, 10),
    (48000, 1.9), (63000, 4.2)
]

# Average salary for each tenure

# Keys are years, values are lists of the salaries for each tenure.
salary_by_tenure = defaultdict(list)
for salary, tenure in salaries_and_tenures:
    salary_by_tenure[tenure].append(salary)

# Keys are years, each value is average salary for that tenure.
average_salary_by_tenure = {
    tenure: sum(salaries) / len(salaries)
    for tenure, salaries in salary_by_tenure.items()
}

print(average_salary_by_tenure)
print("------------------------------")

# Grouping the tenures

def tenure_bucket(tenure):
    if tenure < 2:
        return "less than two"
    elif tenure < 5:
        return "between two and five"
    else:
        return "more than five"


# Keys are tenure buckets, values are lists of salaries for that bucket.
salary_by_tenure_bucket = defaultdict(list)
for salary, tenure in salaries_and_tenures:
    bucket = tenure_bucket(tenure)
    salary_by_tenure_bucket[bucket].append(salary)
    
# Computing the average salary for each group:
# Keys are tenure buckets, values are average salary for that bucket.
average_salary_by_bucket = {
    tenure_bucket: sum(salaries) / len(salaries)
    for tenure_bucket, salaries in salary_by_tenure_bucket.items()
}

print(average_salary_by_bucket)
print("------------------------------")
# Paid Accounts
'''
Correspondence between years of experience and paid accounts:
    0.7 paid
    1.9 unpaid
    2.5 paid
    4.2 unpaid
    6.0 unpaid
    6.5 unpaid
    7.5 unpaid
    8.1 unpaid
    8.7 paid
    10.0 paid
'''

# Creating a model to predict “paid” for users with very few and very many years of experience, and “unpaid” for users with middling amounts of experience:

def predict_paid_or_unpaid(years_experience):
    if years_experience < 3.0:
        return "paid"
    elif years_experience < 8.5:
        return "unpaid"
    else:
        return "paid"
        
print("predict to someone with 4 years of experience: " + str(predict_paid_or_unpaid(4.0)))
print("------------------------------")
# Simple way to find the most popular interests

words_and_counts = Counter(word
    for user, interest in interests
    for word in interest.lower().split())

print(words_and_counts)
print("------------------------------")
# List out the words that occur more than once

for word, count in words_and_counts.most_common():
    if count > 1:
        print(word, count)