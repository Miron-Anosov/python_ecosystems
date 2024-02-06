author_del = {
    'summary': 'This is an endpoint for delete author and his book too.',
    'tags': ['Authors'],
    'parameters': [
        {
            'in': 'path',
            'name': 'id',
            'schema': {
                'fav_number': {
                    'type': 'integer'
                }
            },
            'required': True,
            'description': "author's ID",
        }
    ],
    'responses': {
        '204': {
            'description':  "author's ID"
        },
        '400': {
            'description': 'Validation Error.'
        }
    },
    'deprecated': True,
    'description': "You can delete an author by ID, and the author's books will be deleted as well."
}