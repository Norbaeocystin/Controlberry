# Controlberry
Application to control Raspberry Pi 3 B+ sensors,
it works by watching changes in MongoDB collections, what means you can use database which is running localy or on server for remote connections.

  
To download zip to your raspberry https://codeload.github.com/Norbaeocystin/Controlberry/zip/master
 and unzip master
 
 or install it via pip
 
 For remote control it is possible to use free tier [MongoDB Atlas](https://www.mongodb.com/cloud/atlas) ( you cant use free tier [mlab](https://mlab.com/) because it doesn't support .watch()).
 
 ## Notes:
   * [how to install mongodb](https://docs.mongodb.com/manual/installation/)
   * also it is good to install [TTL index](https://docs.mongodb.com/manual/core/index-ttl/) on Timestamp field in documents in Temperature collection
   * Example how to set up Controlberry (via raspberry terminal), do it in your preferred folder:
     * sudo apt-get update
     * sudo apt-get install screen
     * pip3 install pymongo
     * wget https://codeload.github.com/Norbaeocystin/Flaskberry/zip/master
     * unzip master
     * cd Controlberry-master
     * cd Controlberry
     * sudo nano config.json #write your values
     * screen python3 control.py
 
 ## To do list
 - [ ] documentation
 - [ ] add more sensors
 - [ ] add timing options

