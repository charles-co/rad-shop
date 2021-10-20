# Project Setup

## Table of Contents

- [Project Setup](#project-setup)
  - [Table of Contents](#table-of-contents)
    - [Local Installation](#local-installation)

### Local Installation

- clone project and checkout to `optimized` branch

        git clone https://github.com/charles-co/rad-shop.git

        git checkout optimized

- create virtualenv, activate it & install requirements

        python -m venv venv

        source venv/bin/activate
        
        pip install -r requirements.txt

- runserver

        python manage.py runserver

Check out live implementation [here](https://rad.pythonanywhere.com/)