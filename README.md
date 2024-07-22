A python script that scrapes the content of [Billboard Charts](https://www.billboard.com/charts/hot-100/) for a given date and creates a Spotify Playing with these songs. Ideal for a birthday gift to your friends.

Developed during Angela Yu's class [100 Days of Code](https://www.udemy.com/course/100-days-of-code). 
## Setup
1. Create a virtual environment: `python -m venv myproject_env`
2. Activate the virtual environment
3. Install dependencies: `pip install -r requirements.txt`

Python version 3.12.3

## How to
- You need a spotify account for this
- Fork the Github project and clone the forked repository to your local machine using the ```git clone command```
- Create a .env file in the project to store your environmental login values
- Go to the [developer dashboard](https://developer.spotify.com/dashboard), create an app and copy the Client ID and Client Secret to your .env file
- Use the [Spotipy documentation](https://spotipy.readthedocs.io/en/2.13.0/#) to authenticate your project access to your Spotify. You will need to call the get_token function for the first time that you do this: 
```
token = get_token(CLIENT_ID, CLIENT_SECRET)
print(token)
```
