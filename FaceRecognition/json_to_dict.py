def jsonify(data):
    resp = []
    for i in data:
            obj = {}
            for j in i.keys():
                obj[j] = str(i[j])
            resp.append(obj)
    return resp

def jsonify_one(data):
    obj = {}
    for j in data.keys():
        obj[j] = str(data[j])
    
    return obj