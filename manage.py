#!/usr/bin/env python
# -*- coding: utf-8 -*-
from app import create_app
from flask.ext.script import Manager

app=create_app()
manager=Manager(app)

if __name__ == '__main__':
    manager.run()