# Shor's algorithm for factoring N = 21
# P(y) = 0 when m*y*r is an integer multiple of q

q = 512
r = 6
y = 0

# the m = 85 case
m = 85

for y in range(q):
	if (m*y*r) % q == 0 and not isinstance(float(y*r)/q, int) and not y == 0:
		print "P(y) = 0 for y = " + str(y) + " when m = " + str(m)
		
	y += 1
	
# the m = 86 case
m = 86
y = 0 # reset y

for y in range(q):
	if (m*y*r) % q == 0 and not isinstance(float(y*r)/q, int) and not y == 0:
		print "P(y) = 0 for y = " + str(y) + " when m = " + str(m)

	y += 1
