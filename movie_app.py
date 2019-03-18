
import requests
import urllib

class OMDBError(Exception):
    """
    OMDBError represents an error returned by the OMDb API.
    """
    pass



def get_apikey():
    file = open("omdb-api-key.txt", "r")
    key = file.read()
    return key.strip()


#Define class Media & Movie
class Media:
    def __init__(self, publisher = "Universal Studios", market = "USA"):
        self.publisher = publisher
        self.market = market

    def get_media_info(self):
        print(self.publisher, self.market)
        return None

class Movie(Media):
    def __init__(self, movie_data, publisher = "Universal Studios", market = "USA"):
        super().__init__(publisher, market)
        self.omdb_data = movie_data


    def get_movie_title(self):
        return self.omdb_data["Title"]
    
    # get_movie_rating is a getter function that returns the rating.
    def get_movie_rating(self, source="Rotten Tomatoes"):

        # Loop through each rating and return it if the source is "Hard Coded".
        for ratings in self.omdb_data["Ratings"]:
            if ratings["Source"] == source:
                return ratings["Value"]
       
        return "- Wait - Rating for source {0} was not found!".format(source)




class OMDB(object):
    def __init__(self, apikey):
        self.apikey = apikey

    def build_url(self, **kwargs):
      """
      build_url returns a properly formatted URL to the OMDb API including the
      API key.
      """

      # Add API key to dictionary of parameters to send to OMDb.
      kwargs["apikey"] = self.apikey

      ######Why are we defining self.apikey here if apikey is not part of the function's variable?

      # Start building URL.
      url = "http://www.omdbapi.com/?"

      # urlencode the API parameters dictionary and append it to the URL.
      url += urllib.parse.urlencode(kwargs)

      # Return the complete URL.
      return url
    

    def call_api(self, **kwargs):
        url = self.build_url(**kwargs)
        response = requests.get(url)
        response_data_decoded = response.json()

        # Check for an error and throw an exception if needed.
        if "Error" in response_data_decoded:
            raise OMDBError(response.json()['Error'])

        return response_data_decoded


    def get_movie(self, movie_query):
        movie_data = self.call_api(t = movie_query)

        return Movie(movie_data)


    def search(self, movie_query):
        movie_dictionaries = self.call_api(s = movie_query)
        return movie_dictionaries["Search"]



def return_single_movie_object(movie_query):
    apikey = get_apikey()
    omdb = OMDB(apikey)

    try:
        my_movie_object = omdb.get_movie(movie_query)
        return my_movie_object
    except OMDBError as err:
        print("OMDB Error: {0}".format(err))
        return


def print_single_movie_rating(movie_query):
    movie = return_single_movie_object(movie_query)
    print("The rating for \"{0}\" is {1}.".format(movie.get_movie_title(), movie.get_movie_rating()))


#Define all ratings function: for each movie in the movie list, print that the movie has great rating
def print_all_ratings(movie_list):
    for movie_title in movie_list:
        movie = return_single_movie_object(movie_title)
        print("The movie", movie.get_movie_title(), "has a rating of", movie.get_movie_rating())    


#Define function to list search results: for each title in the movie titles, give it an empty string in front
def list_search_results(movie_query):
    apikey = get_apikey()
    omdb = OMDB(apikey)

    try:
        matching_movie_list = omdb.search(movie_query)
        movie_titles = [each_movie["Title"] for each_movie in matching_movie_list]
    except OMDBError as err:
        print("OMDB Error: {0}".format(err))
        return



    # To call the API, we'll need the API key.
    # Call `get_apikey()` and save it as `apikey`.

    # Then, we'll need to make an API client to call the API. We'll also need to search for the actual movie. This might look something like:
    # omdb_results = OMDB_call(apikey, movie_query)
    # But, we aren't really sure until we actually call the API.
    # When we do make this, we should probably put it in a try/except block in case the API call fails.

    # Once we have our results, we can loop through them and print them.
    # We know from the example call on the website that each movie object is a dictionary with a "Title" key. We can use list comprehensions to make a list from this. If we save it in `movie_titles`, we don't need to change the `for` loop below, and we can delete the list parameter in the function declaration:
    # movie_titles = [each_movie["Title"] for each_movie in matching_movie_list]


    for each_title in movie_titles:
        print ("    ", each_title)



#Define the default list of movies
default_movie_list = ["Back to the Future", "Blade", "Spirited Away"]


#Define the main function as: print that each  movie has great ratings
def main():
    print_all_ratings(default_movie_list)

    search_or_ratings = int(input("Would you like to search for a movie (1) or find the rating of a specific movie (2)?"))


    while True:
        if search_or_ratings == 1:

            movie_query = input("Enter the movie title: ")

            # If search_or_ratings is 1, call list_search_results().
            list_search_results(movie_query)

            break

        elif search_or_ratings == 2:

            movie_query = input("Enter the movie title: ")

            # If search_or_ratings is 2, call print_movie_rating().
            print_single_movie_rating(movie_query)

            break

        else:
            # If search_or_ratings is otherwise, give an error.
            print("Error: Your input must be 1 or 2!")



#Main is the entry point into the program, and it calls into the search orratings functions depending on what the user decides to do.
if __name__ == "__main__":
    main()

