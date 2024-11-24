Guidelines to run the entire code are given below  

This notebook is to be run on a jupyter kernel

1. Add your HuggingFace and Cohere API keys in the respective placeholders 
2. Install redis server.
3. Run the following command to install the needed python dependencies - pip install -r requirements.txt
4. Additional installations which are needed are present in the cells of the jupyter notebook.


Run the following commands in the terminal

1. cd project/ (Alternatively, open a terminal window in the project folder)
2. redis-server 
3. celery -A tasks.celery worker --loglevel=info
4. celery -A tasks.celery beat --loglevel=info



Run all the commands 2,3,4 in 3 different terminal windows at the same time.
Make sure all the terminal windows are in the same path (in the project folder)

In order to change the frequency of file downloads, change the time in the celery.py file locted in the project/tasks folder. 
