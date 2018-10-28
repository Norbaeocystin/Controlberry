# Controlberry
Application to control Raspberry Pi 3 B+ sensors,
it works by watching changes in MongoDB collections, what means you can use database which is running localy or on server for remote connections.
 
 For remote control it is possible to use free tier [MongoDB Atlas](https://www.mongodb.com/cloud/atlas) ( you cant use free tier [mlab](https://mlab.com/) because it doesn't support .watch()).
 
 To fully use Controlberry you need to install:
    * install [MongoDB](https://docs.mongodb.com/manual/installation/) locally or on server
    * install [Controlberry](https://github.com/Norbaeocystin/Controlberry) on your PCs or you can deploy it as web app on [Pythonanywhere](https://www.pythonanywhere.com/)
 
 ## Notes:
   * if you want Flask app deploy change in main.py app.run(debug=True) to app.run()
   * [how to install mongodb](https://docs.mongodb.com/manual/installation/)
   * also it is good to install [TTL index](https://docs.mongodb.com/manual/core/index-ttl/) on Timestamp field in documents in Temperature collection
   * How to install and run:
``` 
sudo apt-get update
sudo pip3 install git+git://github.com/Norbaeocystin/Controlberry.git
#first time will ask for MongoDB URI and Database name 
sudo controlberry #or via terminal remotely use screen controlberry
#in case you want change something in config.json
cd /usr/local/lib/python3*/dist*/Controlberry/Config
sudo nano config.json
```
 
 ## To do list
 - [ ] documentation
 - [ ] add more sensors
 - [ ] add timing options

