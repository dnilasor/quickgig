from flask_table import Table, Col

class Results(Table):
    id = Col('Id', show=False)
    neighborhood = Col('Neighborhood')
    detail = Col('Details')
