from bs4 import BeautifulSoup
import requests
import csv

#Open CSV File Movie Details
csv_file = open('cms_scrape_movies_.csv', 'w', newline='')
csv_writer = csv.writer(csv_file, delimiter='¤')

#Sequence of the exported Information in the CSV File
csv_writer.writerow([   'movie_name',
                        'movie_name_original',
                        'movie_genres',
                        'move_genre_id',
                        'movie_release',
                        'movie_cover_link_HQ',
                        'movie_cover_link_LQ',
                        'movie_presentation',
                        'movie_stars'
                                                ])

#Genre Sequence, the index corresponds to its genre ID
movie_all_genres=["",
                    "Action",
                    "Adventure",
                    "Animation",
                    "Biography",
                    "Comedy",
                    "Crime",
                    "Documentary",
                    "Drama",
                    "Family",
                    "Fantasy",
                    "Film Noir",
                    "History",
                    "Horror",
                    "Music",
                    "Musical",
                    "Mystery",
                    "Romance",
                    "Sci-Fi",
                    "Short",
                    "Sport",
                    "Superhero",
                    "Thriller",
                    "War",
                    "Western"]

#Get the URLs
for x in range (1, 5):
    x = x*50 +1
    print('Working on movie page from '+str(x))
    #Get a signle URL
    url_list = requests.get(f'https://www.imdb.com/search/title/?title_type=feature&genres=action&start={x}&explore=genres&ref_=adv_nxt').text
    soup1= BeautifulSoup(url_list, 'lxml')

    #Create the Movie List HTML
    for movie_item in soup1.find_all('div', class_='lister-item mode-advanced'):

        #Find the Link to the Movie
        movie_link = movie_item.find(class_='lister-item-image float-left').a['href']
        

        #Find the Genres of the Movie
        movie_genres = movie_item.find('span', class_='genre').text.split('\n')[1].rstrip()
        movie_first_genre=movie_genres.split(',')[0]
        movie_genre_id = 0
        for x in range(1,25):
            if movie_first_genre == movie_all_genres[x]:
                movie_genre_id= movie_all_genres.index(movie_all_genres[x])
                continue 
               
        #Create Soup for the Movie Page
        url_movie = requests.get('https://www.imdb.com'+str(movie_link)).text
        soup2 = BeautifulSoup(url_movie, 'lxml')

        try:
            movie_name = soup2.find('h1', attrs={'data-testid': 'hero-title-block__title'}).text
        except Exception as e:
            print('Fehler in ' + movie_link)
            continue


        #Find the Original Name
        try:
            movie_name_original = soup2.find('div', attrs={'data-testid': 'hero-title-block__original-title'}).text.split('Original title: ')[1]
        except Exception as e:
            movie_name_original = movie_name
            pass

        #Find the release Year
        try:
            movie_release = soup2.find('a', attrs={'href': str(movie_link)+'releaseinfo?ref_=tt_ov_rdat'}).text
        except Exception as e:
            movie_release = 'unknown'
            pass

        #Find the Cover Reference Link and then Find the Cover Link in HQ and LQ 
        try:
            movie_cover_ref = soup2.find('a', class_='ipc-lockup-overlay ipc-focusable')['href']
            soup3 = BeautifulSoup(requests.get('https://www.imdb.com'+movie_cover_ref).text, 'lxml')
            movie_cover_link_HQ = soup3.find('img')['src']
            movie_cover_link_LQ= soup3.find('img')['srcset'].split(' ')[0]
        except Exception as e:
            movie_cover_link_HQ = 'no cover'
            movie_cover_link_LQ = 'no cover'
            pass

        # Find a short presentation of the movie
        try:
            movie_presentation = soup2.find('span', attrs={'data-testid': 'plot-xl'}).text 
        except Exception as e:
            movie_presentation = 'no presentation'
            pass

        # Find the main artists in the movie
        try:
            movie_stars_row = movie_item.find(class_='text-muted').find_next(class_='text-muted').find_next(class_='text-muted').find_next().text
            movie_stars_list = movie_stars_row.split('Stars:')[1].split('\n')
            movie_stars = "".join(movie_stars_list)
        except Exception as e:
            movie_stars = 'unknown'
            pass

        print('https://www.imdb.com'+str(movie_link))
        print(movie_name)
        print(movie_name_original)
        print(movie_genres)
        print(movie_genre_id)
        print(movie_release)
        print(movie_cover_link_HQ)
        print(movie_cover_link_LQ)
        print(movie_presentation)
        print(movie_stars)
        print('--------------------------------------------------------------------------')

        try:
            csv_writer.writerow([   movie_name,
                                    movie_name_original,
                                    movie_genres,
                                    movie_genre_id,
                                    movie_release,
                                    movie_cover_link_HQ,
                                    movie_cover_link_LQ,
                                    movie_presentation,
                                    movie_stars,
                                                            ])
        except Exception as e:
            print('ERROR in ' + str(movie_name))
            pass

csv_file.close()
# csv_file_pictures.close()