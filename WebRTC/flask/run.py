#!/usr/bin/env python3
from app import app

# forever serve
app.secret_key='secret'
app.run(debug=True)
