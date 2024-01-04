from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, SubmitField
from wtforms.validators import DataRequired
from Main_data import columns_list

placeholder_option = [("None", "Select an option")]
string_data_types = [("2", "Name"), ("1", "Date"), ("0", "Other")]
yes_no_choices = [("1", "Yes"), ("0", "No")]
data_list = [("0", "Float"), ("1", "String")]

class Main_Form(FlaskForm):
    field_name = SelectField('Field/Column Name', choices=placeholder_option+columns_list, validators=[DataRequired()])
    data_type = SelectField('Data Type', choices=placeholder_option+data_list, validators=[DataRequired()])
    data = SelectField("Define the type of data", choices= placeholder_option+string_data_types, validators=[DataRequired()])
    op = SelectField("Mathematical Operations", choices= placeholder_option+yes_no_choices, validators= [DataRequired()])
    Enum = StringField('Lower Bound', render_kw={"placeholder": "Auto", "value": "Auto"})
    num = StringField('Upper Bound', render_kw={"placeholder": "Auto", "value": "Auto"})
    thresh = StringField('Threshold', render_kw={"placeholder": "9 (default)", "value": "9 (default)"})
    mobile = SelectField("Is Data Mobile Number", choices= placeholder_option+yes_no_choices, validators=[DataRequired()])
    submit = SubmitField("Submit")


