# (semi-failed), more complicated version of 1-out-of-N oblivious transfer
# https://arxiv.org/pdf/0909.2852v1.pdf

import random

###############################################################################

# given a group, find a generator (if one exists)
def get_generator(group):

    #print "\nFinding a generator for Z*_" + str(len(group)+1) + "..."

    random.shuffle(group) # randomize the elements in the group so the choice of generator is randomized
    generated_values = []

    # iterate over each element in the group passed in
    for i in range(len(group)-1):

        generated_values = [] # maintain list of generated values

        # raise the candidate generator to all powers of j, j < n; add to list
        for j in range(len(group)):
            generated_values.append(pow(group[i], j+1, len(group)+1))

        # if the sorted list of generated values matches the sorted input group, we've found a generator
        if sorted(generated_values) == sorted(group):
            print str(group[i]) + " is a generator for Z*_" + str(len(group)+1)

            return group[i]

    return 0

###############################################################################

cyclic_groups = []

cyclic_groups.append([1, 2, 3, 4, 5, 6])

# Alice and Bob agree on a cyclic group to use
z_star = cyclic_groups[random.randint(0, len(cyclic_groups)-1)]

print "Z_q = " + str(z_star)

# randomly select a generator 'g' from cyclic group
g = get_generator(z_star)
print "g = " + str(g)

h = g

# small trick to choose h as another generator in Z*_q
while g == h:
    h = get_generator(z_star)

print "h = " + str(h)

# list of secret messages that Alice has
M = [10, 20, 30, 40, 50, 60]

# number of messages in M
n = len(M)

# Bob (in this case randomly) selects the index of the message he'd like to receive
alpha = random.randint(0, len(M)-1)

print "\nBob (randomly) selects a message he wishes to receive: " + str(alpha)
print "This corresponds to m_" + str(alpha) + " in M which Alice knows = " + str(M[alpha])

# Bob randomly chooses r from Z_q
r = z_star[random.randint(0, len(z_star)-1)]

print "\nBob randomly chooses r in Z_q: " + str(r)

# Bob generates y = g^r * h^alpha
y = pow(g, r) * pow(h, alpha)

print "\nBob calculates y = g^r * h^alpha = " + str(y) + "\n"

# Alice creates a list C = {c_0, c_1,...,c_n} containing encrypted versions of messages in M
C = []

print "Alice encrypts all of the messages of M and sends the resulting list, C, to Bob: "

for i in range(n):

    # randomly choose k_i in Z_q, 1 <= i <= n for each message in M
    k_i = M[random.randint(0, len(M)-1)]

    # encrypt each message c_i as follows: c_i = (g^k_i, m_i(y/h^1)^k_i)
    C.append((pow(g, k_i), M[i] * pow((y / (pow(h, i))), k_i)))

# output the list of c_i's that Alice will send to Bob
for i in range(len(C)):
    print C[i]

# Bob selects the one message he is interested in out of the list of encrypted messages
c_alpha = C[alpha]

# Bob decrypts c_alpha = (a, b) into m_alpha = b/a^r
m_alpha = c_alpha[1] / pow(c_alpha[0], r)

print "\nBob decrypts m_alpha into: " + str(m_alpha)

print "\nWe can check that Alice's value for c_alpha [" + str(M[alpha]) + "] matches Bob's decrypted value of c_i [" + str(m_alpha) + "]!"
