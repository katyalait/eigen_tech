# Eigen Tech
## How To
1. To begin, ensure you have Python, Django, Pip set up on your machine.
2. Next, you will need to download the contents of the git using your preferred method (git clone or downloading the zip).
3. Open a console window and navigate to hashtag_maker directory.
4. Ensure you have virtualenv set up, if not, then run the command `pip3 install virtualenv`.
5. Run the virtualenv by entering the command `source bin/activate`.
6. Install the required packages by running `pip3 install -r requirements.txt`.
7. Navigate to hashtag_maker directory inside your current directory.
8. Run the command `python3 manage.py migrate`.
9. Run the server by calling `python3 manage.py runserver`.
10. Open up your preferred browser and go to `localhost:8000/main/`.
11. You are now running and can use the Hashtag Maker.

## Functions
1. Upload a document.
  a) Select the upload document option in the navbar.
  b) Type in a file name
  c) Choose a file to upload.
  d) Give it some time while it parses the data and updates the database.
2. Filter Words
  a) Type in how many top words you wish to see (suggested:10)
  b) Select the files you want it to consider by ticking the checkboxes.
  c) Click 'Filter'
  d) Scroll down and observe the results.
  
## Infastructure
In order for the words to be parsed, the appropriate files must be uploaded. The system will only work when files are provided via the form. You can upload as many files as you please. 
When a file is uploaded, the web app creates objects for each of the words and entences and one for the document itself. This system makes filtering much easier later on in the running of web app. I opted for this method as the idea of a persistent system was more appealing to me than a once-off model that would take a long time to run every time a query for popular words was made. This way, one can make many queries one after the other without being held back by processing time. 

## Testing
All tests have been run and verified. To analyse my test coverage open the index.html file in the hashtag_maker/htmlcov/ directory. To verify all tests are OK, run the command `coverage run manage.py test main -v 2` inside of hashtag_maker/hashtag_maker. 
  
