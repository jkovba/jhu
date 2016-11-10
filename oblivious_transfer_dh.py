import hashlib
import random

###############################################################################

# given a group, find a generator (if one exists)
def get_generator(group):

    print "\nFinding a generator for Z*_" + str(len(group)+1) + "..."

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

k_bob = 0
k_alice = 0

cyclic_groups = []

cyclic_groups.append([1, 2, 3, 4, 5, 6])

# Alice and Bob agree on a cyclic group to use
z_star = cyclic_groups[random.randint(0, len(cyclic_groups)-1)]

print "Z = " + str(z_star)

# randomly select a generator 'g' from cyclic group
g = get_generator(z_star)

a = z_star[random.randint(0, len(z_star)-1)] # randomly select a value 'a' from Z* (Alice)

# calculate g^a to be sent to Bob
A = pow(g, a)

print "\nAlice has selected a value of a = " + str(a) + " and calculated g^a = " + str(A)

# randomly select a value 'b' from Z* (Bob)
b = z_star[random.randint(0, len(z_star)-1)]

# calculate g^b to be sent to Alice
B = pow(g, b)

print "\nBob has selected a value of b = " + str(b) + " and calculated g^b = " + str(B)

g_ab_alice = pow(B, a) # the shared value = B^a = (g^b)^a (Alice)
g_ba_bob = pow(A, b)   # the shared value = B^a = (g^b)^a (Bob)

# Bob chooses a choice bit c in {0, 1}
c = random.randint(0, 1)

if c == 0:
    k_bob = B # if choice bit is 0, Bob chooses g^b as his key

else:
    k_bob = A * B # if choice bit is 1, Bob chooses A * g^b

print "Bob now chooses a random bit c in {0, 1} = " + str(c)

# based on c, Bob generates either B = g^b or B = Ag^b, and sends it to Alice
if c == 0:
    B = pow(g, b)

elif c == 1:
    B = A * pow(g, b)

k0 = pow(B, a) # Alice computers k0 = B^a
k1 = pow((B/A), a) # Alice computes k1 = (B/A)^a

kr = pow(A, b)

# Bob computes (the hash of) A^b (the "receiver" key)
h_kr = hashlib.md5()
h_kr.update(str(k0))
h_kr = h_kr.hexdigest()
print "\nBob generates H(k_r): " + h_kr

# Alice gets B from Bob and derives (the hash of) two keys (to get a fixed length output)
h_k0 = hashlib.md5()
h_k0.update(str(k0))
h_k0 = h_k0.hexdigest()
print "\nAlice generates H(k_0): " + h_k0

h_k1 = hashlib.md5()
h_k1.update(str(k1))
h_k1 = h_k1.hexdigest()
print "Alice generates H(k_1): " + h_k1

# two random messages
m0 = 123
m1 = 456

# syntax is scary, but we're converting k1 to an 'int' and XOR'ing with m0 to encrypt
e_m0 = int(h_k0, 16) ^ int(m0)

print "\nAlice encrypts m0 (" + str(m0) + ") with h_k0 and gets: " + str(e_m0)

# more scary syntax, but we're encrypting m1 by XOR'ing with k1
e_m1 = int(h_k1, 16) ^ int(m1)

print "Alice encrypts m1 (" + str(m1) + ") with h_k1 and gets: " + str(e_m1)

# Alice sends both encrypted messages to Bob who then decrypts with H(k_r)

d_m0 = e_m0 ^ int(h_kr, 16)
d_m1 = e_m1^ int(h_kr, 16)

# Bob decrypts both messages
print "\nBob decrypts e_m0 (" + str(e_m0) + ") with h_kr and gets: " + str(d_m0)
print "Bob decrypts e_m1 (" + str(e_m1) + ") with h_kr and gets: " + str(d_m1)