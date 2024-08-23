from . import api_blueprint

@api_blueprint.route('/handle-query',methods=['POST'])
def handle_query():
    pass