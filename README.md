# Quizzer

[quizzer.niallg.ie](https://quizzer.niallg.ie)

Take on your friends in a quiz game.

Create a quiz with your own questions and act as quizmaster while your friends battle it out for first place.

The idea for this stemmed from the lockdown-induced Zoom quizzes of March/April 2020. The app is designed to be played with the quizmaster talking to participants, and eases the hassle of collecting answers and correcting.

## Details

Python/Flask backend which serves a [frontend](https://github.com/gniall12/quiz-frontend) written in Angular.

This is a work in progress - I will be adding unit testing next.

Makes use of [Flask-SSE](https://pypi.org/project/Flask-SSE/), a package which enables server-sent events from Flask applications. 
This allows the quizmaster to notify participants when the quiz progresses to the next stage
    
## Running Code

1. Create python virtual environment python3 -m venv env
2. Activate virtual environment source env/bin/activate
3. Run `pip install -r requirements.txt` to install packages
4. Follow instructions at https://redis.io/ to install redis and run a redis server (this is needed for Flask server-sent events)
4. Create .env file with environment variables:  
   export QUIZ_SECRET_KEY=\<your-secret-key\> 
   export DATABASE_URL=\<your-database-url\>
   export REDIS_URL=\<your-redis-url\>
5. Run code using `gunicorn --worker-class=gevent --bind 127.0.0.1:5000 "quiz_app:create_app()"`  
   
Pull requests and suggestions for features are welcome
