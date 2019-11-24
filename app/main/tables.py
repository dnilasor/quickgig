from flask_table import Table, Col

class Results(Table):
    id = Col('Id', show=False)
    neighborhood_id = Col('Neighborhood', show=False)
    detail = Col('Details')
