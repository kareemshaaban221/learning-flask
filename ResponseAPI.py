class ResponseAPI:
    @staticmethod
    def notFound(message=none):
        if message:
            return {
                'message': message
            }, 404
        else:
            return {}, 404
        
    @staticmethod
    def ok(data=none, message=none):
        response = {}
        if data:
            response.update(data)
        if message:
            response.update({
                'message': message
            })
            
        return response, 200
    
    @staticmethod
    def created(data=none, message=none):
        response = {}
        if data:
            response.update(data)
        if message:
            response.update({
                'message': message
            })
            
        return response, 201
    
    @staticmethod
    def serverError(message=none):
        response = {}
        if message:
            response.update({
                'message': message
            })
            
        return response, 201