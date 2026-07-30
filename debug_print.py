from src.decode_lab import validation

print('PROFANITY_LIST:', validation._PROFANITY_LIST)
print(validation.check_and_sanitize_profanity('This is foo and BAR in text'))
