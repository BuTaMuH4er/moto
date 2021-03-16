from flask_restful import Resource
from flask import Flask, render_template, request
from api.model import db, Motocycle

class ProductAPI(Resource):

    def get(self):
        motocycle = Motocycle.query.all()
        return render_template('index.html',motocycle=motocycle)

