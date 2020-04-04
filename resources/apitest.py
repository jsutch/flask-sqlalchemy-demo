from flask_restful import Resource

class Test(Resource):
    """
    test harness. return whatever name passed
    """
    def get(self, name):
        return {'test':name}