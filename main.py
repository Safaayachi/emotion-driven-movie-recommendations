from bs4 import BeautifulSoup as SOUP
import re
import requests as HTTP


# Main Function for scraping
def main(emotion):
    # Map emotions to IMDb genres
    emotion_to_genre = {
        "sad": "drama",
        "disgust": "musical",
        "anger": "family",
        "anticipation": "thriller",
        "fear": "sport",
        "enjoyment": "thriller",
        "trust": "western",
        "surprise": "film_noir",
    }

    # Check if the emotion is in the mapping
    if emotion.lower() not in emotion_to_genre:
        print("Invalid emotion. Please choose a valid emotion.")
        return []

    genre = emotion_to_genre[emotion.lower()]
    urlhere = f'http://www.imdb.com/search/title?genres={genre}&title_type=feature&sort=moviemeter, asc'

    print(f"Fetching data from: {urlhere}")

    # HTTP request to get the data of the whole page
    response = HTTP.get(urlhere)

    # Check if the request was successful
    if response.status_code != 200:
        print(f"Failed to fetch data. Status code: {response.status_code}")
        return []

    data = response.text

    # Parsing the data using BeautifulSoup
    soup = SOUP(data, "lxml")

    # Extract movie titles from the data using regex
    titles = [str(i).split('>;')[1][:-3] for i in soup.find_all("a", attrs={"href": re.compile(r'\/title\/tt+\d*\/')})
              if len(str(i).split('>;')) == 3]

    return titles


# Driver Function
if __name__ == '__main__':
    emotion = input("Enter the emotion: ")
    recommended_movies = main(emotion)

    if recommended_movies:
        print("Recommended Movies:")
        for movie in recommended_movies:
            print(movie)
    else:
        print(f"No movies found for the emotion: {emotion}")
