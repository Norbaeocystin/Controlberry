# Controlberry
Application to control Raspberry Pi 3 B+ sensors,
it works by watching changes in MongoDB collections, what means you can use database which is running localy or on server for remote connections.
 
 For remote control it is possible to use free tier [MongoDB Atlas](https://www.mongodb.com/cloud/atlas) ( you cant use free tier [mlab](https://mlab.com/) because it doesn't support .watch()).
 
 ## Notes:
   * if you want Flask app deploy change in main.py app.run(debug=True) to app.run()
   * [how to install mongodb](https://docs.mongodb.com/manual/installation/)
   * also it is good to install [TTL index](https://docs.mongodb.com/manual/core/index-ttl/) on Timestamp field in documents in Temperature collection
   * How to install and run:
``` 
sudo apt-get update
sudo pip3 install git+git://github.com/Norbaeocystin/Controlberry.git
#write connection MongoDB URI and Database to config.json, for pasting URI or Database string via putty use shift + insert 
controlberry #or via terminal remotely use screen controlberry
```
 
 ## To do list
 - [ ] documentation
 - [ ] add more sensors
 - [ ] add timing options

