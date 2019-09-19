from flask_wtf import FlaskForm
from wtforms import FieldList, FormField, StringField, TextField, RadioField, SelectField, SubmitField, IntegerField, BooleanField

class TestType(FlaskForm):
	radio = RadioField('Type', default='page', choices=[('page','Une page au choix'), ('whole','La totalité')])
	choices = [('0', 'Aléatoire'), ('1','1'), ('2','2'), ('3','3'), ('4','4'), ('5','5'), ('6','6'), ('7','7'), ('8','8'), ('9','9'), ('10','10'), ('11','11'), ('12','12'), ('13','13'), ('14','14')]
	important = BooleanField('Seulement les mots obligatoires', default=False)
	select = SelectField('Page : ', choices=choices)
	nbmot = IntegerField('Nombre de mots : ', default=10)
	submit = SubmitField('Démarrer')
