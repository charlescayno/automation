import sys

def truncate(f, n):
    '''Truncates/pads a float f to n decimal places without rounding'''
    s = '{}'.format(f)
    if 'e' in s or 'E' in s:
        return '{0:.{1}f}'.format(f, n)
    i, p, d = s.partition('.')
    return '.'.join([i, (d+'0'*n)[:n]])

P = float(sys.argv[1]) # puhunan
i = float(sys.argv[2]) # entry price
o = float(sys.argv[3]) # exit price

bal = float(P*(o/i)-P)
bal = truncate(bal,4)
bal = float(bal)
percent = float(bal/P*100)
percent = truncate(percent,2)
percent = float(percent)

print()

if bal > 0:
	print(f'Earnings: {bal}')
	print(f'%Earnings: {percent}%')
else:
	print(f'Losses: {bal}')
	print(f'%Losses: {percent}%')



