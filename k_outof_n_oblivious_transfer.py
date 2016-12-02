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

print "\nAlice has a list of secret messages M = " + str(M)

# number of messages in M
n = len(M)

# Bob selects a list of alpha values corresponding to the messages in M he'd like to receive from Alice
num_list = list(range(len(M) - 1))
alphas = num_list[0:random.randint(2, len(M)-1)]

k = len(alphas) # length of 'alphas'

print "\nBob (randomly) selects a list of messages he wishes to receive: " + str(alphas)

R = [] # list of r_l values
Y = [] # list of y_l values

for l in range(k):

    # Bob randomly chooses r_l from Z_q
    r_l = z_star[random.randint(0, len(z_star)-1)]

    # keep a list of the r_l's to be used later for decryption
    R.append(r_l)

    # y_l = g^(r_l) * h^(alpha_l)
    Y.append(pow(g, r_l) * pow(h, alphas[l]))

print "\nBob sends a list of y_l's to Alice: " + str(Y)


# Alice creates a list C = {c_0, c_1,...,c_n} containing encrypted versions of messages in M
C = []

print "\nAlice encrypts the messages of M and sends the resulting list, C, to Bob: "

for i in range(k):

    # Alice randomly chooses k_i in Z_q, 1 <= i <= n for each message in M
    k_i = M[random.randint(0, len(M)-1)]

    # Alice encrypts each message c_i as follows: c_i = (g^k_i, m_i(y_l/h^i)^k_i) and sends them to Bob
    C.append((pow(g, k_i), M[i] * pow((Y[i] / (pow(h, i))), k_i)))

D = [] # set of decrypted messages

# Bob decrypts the k # of messages he's able to (c_alpha = (a, b) into m_alpha = b/a^r)
for i in range(len(C)):
    D.append(int(C[i][1]/pow(C[i][0], R[i])))

print "\nBob requested, from Alice, messages with indices: " + str(alphas)

print "\nAlice had the following values for these messages:" + str(M[0:len(alphas)])

print "\nAlice encrypted these values and sent them to Bob: " + str(C)

print "\nBob decrypted these messages into: " + str(D)

print "\nSo, we see that Bob has successfully obtained " + str(k) + "(k) out of " + str(n) + "(n) items using oblivious transfer!"
