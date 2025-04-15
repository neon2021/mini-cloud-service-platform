def lambda_handler(event, context):
    name = event.get('name', 'World')
    return {
        'statusCode': 200,
        'body': {
            'message': f'Hello, {name}!',
            'event': event
        }
    } 