<p align="center">
  <img src="https://github.com/5sControl/.github/assets/131950264/d65c5be1-1cca-46a1-b564-ef4364f0dbc6" alt="5controlS" height = "320" />
</p>

[![Contributor Covenant](https://img.shields.io/badge/Contributor%20Covenant-2.1-4baaaa.svg)](CODE_OF_CONDUCT.md)

**[5controlS](https://5controls.com/)** is a video monitoring system with AI analysis and ERP Integration (Open Source) that helps companies improve productivity, eliminate waste, and enhance workplace safety using computer vision (CV) and machine learning (ML). 

The platform generates detailed reports to provide insights on how processes can be optimized.

Plug-in your ML-algorithms or some of the Official 5s algorithms and get a ready-to-use software for manufacturing monitoring.

# **Project repositories**

The connections between the project repositories are illustrated by the following diagram. 

> Please note that to ensure system stability and perfomance you can use one of the Official 5S algorithms instead of Your Algorithm.

<p align="center">
  <img src="https://github.com/5sControl/5s-user-documentation/blob/main/assets/5S%20scheme%20(1).png" alt="5controlS-diagram" />
</p>


**5controlS Platform:**
1. [5s-webserver](https://github.com/5sControl/5s-webserver)
2. [5s-backend](https://github.com/5sControl/5s-backend)
3. [5s-frontend](https://github.com/5sControl/5s-frontend)
4. [5s-algorithms-controller](https://github.com/5sControl/5s-algorithms-controller)
5. [5s-onvif](https://github.com/5sControl/5s-onvif)
6. [5s-onvif-finder](https://github.com/5sControl/5s-onvif-finder)
   

**Official Algorithms:**
1. [min-max](https://github.com/5sControl/min-max)
2. [idle-control](https://github.com/5sControl/idle-control)
3. [operation-control-js](https://github.com/5sControl/operation-control-js)
4. [machine-control](https://github.com/5sControl/machine-control)
5. [machine-control-js](https://github.com/5sControl/machine-control-js)

**Algorithms Servers:**
1. [inference-server-js](https://github.com/5sControl/inference-server-js)

# To install, do the following

The first thing to do is to clone the repository:
```sh
git clone https://github.com/5sControl/5s-backend.git
cd 5s-backend
```
Create a virtual environment to install dependencies in and activate it:

```sh
python3 -m venv venv
source venv/bin/activate
```
Note the `(venv)` in front of the prompt. This indicates that this terminal
session operates in a virtual environment set up by `venv`.

Then install the dependencies:
```sh
pip install -r requirements.txt
```

Create .env file in 5s-backend root folder:
```sh
touch .env
```
All variables and how they should look can be seen in the file `.env.example`

Your secret key should be in .env file like this:
```
SECRET_KEY = asddsad231jsfjp32ojrjpfjsdoivzoidvhoxic
```
Debug mode enabled `DEBUG=True`
```
DEBUG=True
```
Create an IP variable.
This is the IP address of your machine in the network
```
IP=192.168.1.101
SERVER_URL=http://192.168.1.101
PRODUCTION=False
LICENSE_ACTIVE=False
```
Add connection parameters to the DB:
```
DB_ENGINE=django.db.backends.postgresql
DB_NAME=your name db
DB_USER=your username db
DB_PASSWORD=your password db
DB_HOST=your host db
DB_PORT=your port db
```

Execute the command that will create migrations in the DB, superuser and start the server

```sh
make all
```
If the command is executed successfully, you will see in the terminal navigate to `http://127.0.0.1:8000/`

You can go to the address 
```sh
http://127.0.0.1:8000/api/swagger/
```
Swagger will open where you will see a list of available URLs.

# **Documentation**

[Documentation for Developers](https://github.com/5sControl/5s-dev-documentation/wiki)

[User Documentation](https://github.com/5sControl/Manufacturing-Automatization-Enterprise/wiki)

[Installation Guide Pt.1](https://5controls.com/blog/installing-5s-control-software)

[Installation Guide Pt.2](https://5controls.com/blog/installing-5s-control-software-part-2-docker)

# **Contributing**
Thank you for considering contributing to 5controlS. We truly believe that we can build an outstanding product together!

We welcome a variety of ways to contribute. Read below to learn how you can take part in improving 5controlS.

## **Code of conduct**

Please note that this project is released with a [Contributor Code of Conduct](CODE_OF_CONDUCT.md). By participating in this project you agree to abide by its terms.

## Code contributing

If you want to contribute, read  our [contributing guide](CONTRIBUTING.md) to learn about our development process and pull requests workflow.

We also have a list of [good first issues](https://github.com/5sControl/5s-backend/issues?q=is%3Aopen+is%3Aissue+label%3A%22good+first+issue%22) that will help you make your first step to beсoming a 5S contributor.

# **License**

[GNU GPL-3.0](LICENSE)
> 5controlS uses third party libraries that are distributed under their own terms (see [LICENSE-3RD-PARTY.md](https://github.com/5sControl/5s-backend/blob/main/LICENSE-3RD-PARTY.md)).<br>

<br>
<div align="center">
  <a href="https://5controls.com/" style="text-decoration:none;">
    <img src="https://github.com/5sControl/Manufacturing-Automatization-Enterprise/blob/3bafa5805821a34e8b825df7cc78e00543fd7a58/assets/Property%201%3DVariant4.png" width="10%" alt="" /></a> 
  <img src="https://github.com/5sControl/5s-backend/assets/131950264/d48bcf5c-8aa6-42c4-a47d-5548ae23940d" width="3%" alt="" />
  <a href="https://github.com/5sControl" style="text-decoration:none;">
    <img src="https://github.com/5sControl/Manufacturing-Automatization-Enterprise/blob/3bafa5805821a34e8b825df7cc78e00543fd7a58/assets/github.png" width="4%" alt="" /></a>
  <img src="https://github.com/5sControl/5s-backend/assets/131950264/d48bcf5c-8aa6-42c4-a47d-5548ae23940d" width="3%" alt="" />
  <a href="https://www.youtube.com/@5scontrol" style="text-decoration:none;">
    <img src="https://github.com/5sControl/Manufacturing-Automatization-Enterprise/blob/ebf176c81fdb62d81b2555cb6228adc074f60be0/assets/youtube%20(1).png" width="5%" alt="" /></a>
</div>

