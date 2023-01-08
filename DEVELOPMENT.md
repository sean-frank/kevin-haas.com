# Creating a Web Application from Scratch

This setup process is a handful of best practices when it comes to setting up, deploying, releasing, and developing a large web application on _most **shared hosting platforms**_.

As most of the shared hosting platforms are strictly user premitted and don't allow you to install necessary dependencies that would usually install globally or require sudo permissions to install.

Before proceeding, I would highly recommend getting a solid understanding of the following sections.
- [Creating a Flask Example Application](#)
- [Setting Up Phusion Passenger](#)



# Creating a Flask Example Application

For example purposes, you can use the following ["Hello World"](https://github.com/phusion/passenger-python-flask-demo) demo that uses [Flask](http://flask.pocoo.org/).

```
git clone https://github.com/phusion/passenger-python-flask-demo.git
cd passenger-python-flask-demo/
```

Many of the Python web frameworks already have a builtin web server which is activated by simply running the application itself and for this example we run do that as such using.
```
python3 app.py
```

If you run into issues running that, you may need to install the python Flask package.
```
python3 -m pip install Flask
```
**- or -**
```
pip3 install Flask
```

Now once you are running the sample Flask web application, you should be able to view it from your browser at `http://SERVER_PUBLIC_IP:5000/` with no issue.

There's a chance you may run into the following issues when trying to connect...

- `The connection has timed out` usually means your firewall rules or security groups are improperly configured to  allow for inbound traffic on port `5000`.
- `Unable to connect` this can usually happen when trying to connect from another device not on the same IP address. As `127.0.0.1` means localhost/loopback and means you can only be connected to it through itself, so you will need to change the last line in the `app.py` from `MyApp.run()` to `MyApp.run(host='0.0.0.0')` and then you should be able to connect from another computer.




# Setting Up Phusion Passenger

## What is Phusion Passenger?

**Passenger** can be used to serve up Ruby on Rails and Python web applications that use the [WSGI](https://www.python.org/dev/peps/pep-3333/) interface, including any application which uses the **Django** framework.

**Django** is a web development framework for Python in the same way Rails is a framework for Ruby. It is used by a number of major web sites, including Google (i.e., for the Google Application Engine), which can make developing rich web applications much easier.

Django is not an application on its own. You will need proficiency in Python programming in order to write an application using Django.

Passenger allows your application to temporarily reside in memory while it is being actively used. This makes it possible for your site to respond significantly faster than is otherwise possible.

## Installing Passenger

**Info**: If you are using a web hosting provider like _**Dreamhost**, Hostgator, etc_ then you can just enable to allow for your website to run your own application which will typically uses Passenger, so you can skip this step.

The corresponding installation steps were implemented for use on CentOS, so you may have to lookup the appropriate commands for your OS of choice.

- [Enabling EPEL](#)
- [Repair Potential System Issues](#)
- [Installing Passenger with EPEL](#)

### Enable EPEL

This installation walkthrough is intended for CentOS, so you will have to lookup the appropriate commands for your OS flavor.
```
$ sudo yum install -y epel-release yum-utils
$ sudo yum-config-manager --enable epel
$ sudo yum clean all && sudo yum update -y
```

### Repair Potential System Issues

Ensure curl and nss/openssl are sufficiently up-to-date to ensure we can communicate with the repository before running the following.
```
$ sudo yum update -y
$ sudo yum install curl
```

Check to see if your system date is correct using the date command.
```
$ date
```

If the output is incorrect, then we can use ntp to synchronize your system clock.
```
$ sudo yum install -y ntp
$ sudo chkconfig ntpd on
$ sudo ntpdate pool.ntp.org
$ sudo service ntpd start
```

### Installing Passenger with EPEL

Install necessary prerequisites for Passenger.
```
sudo yum install pygpgme
```

Now we can actually install Passenger itself.
```
sudo yum install -y --enablerepo=epel passenger
```

<mark>**WARNING**</mark>: If the above fails, saying that the package is missing or does not exist, you can use the following to add the el7 repository to your yum source lists.

Thusly, paste the following and then rerun the above `yum install` again.
```
sudo curl --fail -sSLo /etc/yum.repos.d/passenger.repo https://oss-binaries.phusionpassenger.com/yum/definitions/el-passenger.repo
```

Now install Passenger Nginx.
```
sudo yum install -y nginx passenger || sudo yum-config-manager --enable cr && sudo yum install -y nginx passenger
```

Validate the installation was successful.
```
$ passenger-config validate-install
 * Checking whether this Phusion Passenger install is in PATH... ✓
 * Checking whether there are no other Phusion Passenger installations... ✓
```

### Configuring Nginx and Passenger

Now it's time to configure Nginx so that Passenger knows how to serve your app.

To do that we need to create an Nginx configuration file and setup a host entry that points toward your application and this will allow for us to both tell Nginx and Passenger where your application is.

So let's just create the basic config for just this application.

```
sudo nano /etc/nginx/conf.d/nginx.conf
```

It's okay if the file does not exist as you can replace or paste the following -
```
# /etc/nginx/conf.d/nginx.conf
server {
    listen 80;
    server_name yourserver.com;

    # Tell Nginx and Passenger where your app's 'public' directory is
    root /var/www/myapp/code/public;

    # Tell Passenger that your app is a Python app
    passenger_app_type wsgi;
    passenger_startup_file passenger_wsgi.py;

    # Turn on Passenger
    passenger_enabled on;
    passenger_python /path/to/python;
}
```

For the above you need to replace a few properties as follows -
- Replace `yourserver.com` with your server's host name.
- Replace `passenger_wsgi.py` with your app's WSGI entry point file.
- Replace `/var/www/myapp/code` with your application's code directory path. However, make sure that nginx is configured to point to the `public` subdirectory inside it!
- Replace `/path/to/python` with the location of the Python binaries for the version which the application is built, this is most likely to be the folder containing the virtual environment.


Once finished, we can now restart Nginx:
```
sudo service nginx restart
```

Your web application should now be running and reachable from your servers hostname. You can quickly verify by running this following command, replacing yourserver.com with your server's hostname, exactly as it appears in the Nginx config file's server_name directive

```
curl "http://yourserver.com:5000/"
```


## Using Passenger with Python Flask Application

**NOTE**: The following example is a continuation from the above [Creating a Flask Example Application](#).

So to be able to use Passenger with Flask, it doesn't have the ability to run it like one typically would by just calling from the command line `python3 app.py` and it just run.

Instead Passenger does it a little differently by using something called [Python WSGI](https://wsgi.readthedocs.io/en/latest/), which defines a standard interface for web applications allowing any application that implements WSGI to work with any server that supports it.

This method of using WSGI is actually used on nearly every modern day Python web application implements the use of WSGI like Flask, Django, etc. In fact, majority of frameworks in general use WSGI like Apache, Ruby, NodeJS, and so on.

With that aside, for use to allow for Passenger to run our application, we must create a `passenger_wsgi.py` file.

### Creating a Passenger WSGI File

Firstly, when trying to run Passenger it just off the bat **assumes** that the directory you are calling it from contains that `passenger_wsgi.py` file.

So your example project files will look something like the below.
```
+-- passenger-python-flask-demo/
    +-- templates/
    |   +-- index.html
    +-- app.py
    +-- passenger_wsgi.py <
```

Paste the below contents to the `passenger_wsgi.py`.

**NOTE**: The contents of your `passenger_wsgi.py` file will change depending on your application and the projects web framework, but for this example we're using a simple Flask app.


```
# passenger_wsgi.py
from app import MyApp as application
```

### Running the Server

```
passenger start
# => ======= Phusion Passenger Standalone web server started =======
# => PID file: /Users/phusion/myapp/passenger.3000.pid
# => Log file: /Users/phusion/myapp/passenger.3000.log
# => Environment: development
# => Accessible via: http://0.0.0.0:3000/
# =>
# => You can stop Phusion Passenger Standalone by pressing Ctrl-C.
# => ===============================================================
```

As you can see in the output, Passenger is now serving your app on http://0.0.0.0:3000/. So if you go to that URL, you will should see your application:


