# kevin-haas.com

A repository for my website at [kevin-haas.com](https://kevin-haas.com/).


## Install Python3

```bash
$ mkdir ~/py3_tmp
$ cd ~/py3_tmp/
$ wget https://www.python.org/ftp/python/3.8.2/Python-3.8.2.tgz
$ tar zxvf Python-3.8.2.tgz 
$ cd Python-3.8.2
$ ./configure --prefix=$HOME/opt/python-3.8.2
$ make
$ make install
$ echo 'export PATH=$HOME/opt/python-3.8.2/bin:$PATH' >> ~/.bash_profile
$ source ~/.bash_profile
$ rm -rf ~/py3_tmp
```

### Verify Installation

```bash
$ which python3
$ python3 --version
$ pip3 --version
```

## Create a Virtual Environment

```
$ python3 -m pip install --upgrade pip
$ pip3 install virtualenv
$ which virtualenv
$ which python3
$ virtualenv -p /usr/bin/python3 venv
$ . venv/bin/activate
(venv) $ python -V
```

To exit the virtual environment:
```
(venv) $ deactivate
$ 
```


## Install Flask within the Virtual Environment

```bash
$ . venv/bin/activate
(venv) $ pip3 install --upgrade pip
(venv) $ pip3 install Flask Flask-SQLAlchemy Flask-Login Flask-Caching python-dotenv requests
```


