def api_response(data, status, message, status_code):
    result = {
        "statusCode": status_code,
        "status": status,
        "data": data,
        "message": str(message),
    }
    return result
