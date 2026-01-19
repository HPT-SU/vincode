length = 17
symbols = 'ABCDEFGHJKLMNPRSTUVWXYZ'
numbers = ''.join([str(num) for num in range(10)])
correct_chars = symbols + numbers

trans_russian = str.maketrans(*(
    # VIN              KEY      WRONG  TO-RUS
    'АВСЕНКМОРТХУOI' + 'ДФГП' + 'ШЩЯ' + 'cgо' + '!@#$%^&',
    'ABCEHKM0PTXY01' + 'DFGP' + 'IOZ' + 'спо' + '1234567',
))

chars_weights = {
    1: 8, 2: 7, 3: 6, 4: 5, 5: 4, 6: 3, 7: 2, 8: 10,
    10: 9, 11: 8, 12: 7, 13: 6, 14: 5, 15: 4, 16: 3, 17: 2,
}
