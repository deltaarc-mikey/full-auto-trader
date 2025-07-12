def option_filter(option_data):
    return (
        option_data['price'] <= 1.50 and
        option_data['pop_score'] >= 8 and
        option_data['type'] == 'call'
    )