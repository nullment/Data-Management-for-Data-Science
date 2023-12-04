# --- PART 1: READING DATA ---
import pandas as pd
# 1.1
def read_movies_data(f):
    movies = pd.read_csv(f, sep='|', header=None, names=['title', 'year', 'genre'], index_col= 0)
    #movies = movies.set_index('ID')
    movies = movies.sort_index(ascending = True)

    #movies = movies.drop(columns=['ID'])
    #movies.columns = ['title', 'year', 'genre']
    #movies.drop('ID', axis=1)
    #movies.reset_index(drop=True, inplace=True)
    #movies.index += 1
    return movies
    #print(movies)
    pass

# 1.2
def read_ratings_data(f):
    ratings_dict = {}
    
    with open(f, 'r') as file:
        for line in file:
            user, movie, rating = line.strip().split(',')
            movie = int(movie)
            rating = float(rating)
            
            if movie in ratings_dict:
                ratings_dict[movie].append(rating)
            else:
                ratings_dict[movie] = [rating]

        

    return ratings_dict
    #print(ratings_dict)
    pass

# --- PART 2: PROCESSING DATA ---

# 2.1
def get_movie(movies_df, movie_id):
    pass

# 2.2
def create_genre_dict(movies_df):
    genre_dict = {}
    for i, row in movies_df.iterrows():
        genre = row['genre']
        movie_id = row.name
        if genre in genre_dict:
            genre_dict[genre].append(movie_id)
        else:
            genre_dict[genre] = [movie_id]
    return genre_dict
    
    #print(genre_dict)

    pass

# 2.3
def calculate_average_rating(ratings_dict, movies_df): 
    average_ratings = pd.Series(index=movies_df.index, dtype=float)
    for id, ratings in ratings_dict.items():
        if id in average_ratings.index:
            average = sum(ratings) / len(ratings)
            average_ratings.at[id] = average
    #print(average_ratings)
    return average_ratings


    pass

# --- PART 3: RECOMMENDATION ---

# 3.1
def get_popular_movies(avg_ratings, n=10):
    sorted_ratings = avg_ratings.sort_values(ascending=False)
    return sorted_ratings.head(n)
    pass

# 3.2
def filter_movies(avg_ratings, thres_rating=3):
    return avg_ratings[avg_ratings >= thres_rating]
    pass

# 3.3
def get_popular_in_genre(genre, genre_to_movies, avg_ratings, n=5):
    if genre in genre_to_movies:
        movies_in_genre = genre_to_movies[genre]
        genre_ratings = avg_ratings.loc[movies_in_genre].sort_values(ascending=False)
        return genre_ratings.head(n)
    pass

# 3.4
def get_genre_rating(genre, genre_to_movies, avg_ratings):
    if genre in genre_to_movies:
        movies = genre_to_movies[genre]
        genre_avg_rating = avg_ratings.loc[movies].mean()
        return genre_avg_rating
    pass

# 3.5
def get_movie_of_the_year(year, avg_ratings, movies_df):
    #best_movie = movies_df[movies_df['year']==year]
    #highest_rating = avg_ratings[(movies_df[movies_df['year']==year]).index].idxmax()
    #highest_rating = movies_df.loc[(avg_ratings[(movies_df[movies_df['year']==year]).index].idxmax()), 'title']
    return movies_df.loc[(avg_ratings[(movies_df[movies_df['year']==year]).index].idxmax()), 'title']
    pass


# --- PART 4: USER FOCUSED ---

# 4.1
def read_user_ratings(f):
    user_dict = {}
    
    with open(f, 'r') as file:
        for line in file:
            user, movie, rating = line.strip().split(',')
            user = int(user)
            movie = int(movie)
            rating = float(rating)

            if user in user_dict:
                user_dict[user].append((movie, rating))
            else:
                user_dict[user] = [(movie, rating)]
    
    return user_dict

    pass

# 4.2
def get_user_genre(user_id, user_to_movies, movies_df):
    user_dict = user_to_movies.get(user_id, [])
    genre_ratings = {}
    avg = {}
    
    for movie, rating in user_dict:
        genre = movies_df.loc[movie, 'genre']
        if genre in genre_ratings:
            genre_ratings[genre].append(rating)
        else:
            genre_ratings[genre] = [rating]
            
    for genre, ratings in genre_ratings.items():
        if len(ratings) > 0:
            avg_rating = sum(ratings) / len(ratings)
    
        avg[genre] = avg_rating
    return max(avg, key=avg.get)
    pass

# 4.3
def recommend_movies(user_id, user_to_movies, movies_df, avg_ratings):
    user_genre = get_user_genre(user_id, user_to_movies, movies_df)
    #print(user_genre)

    genre_dict = create_genre_dict(movies_df)
    #print(genre_dict)

    movies_in_genre = genre_dict[user_genre]
    #print(user_genre)

    top_genre_movies = avg_ratings.loc[movies_in_genre].sort_values(ascending=False).head(3)
    return top_genre_movies
    
    pass
