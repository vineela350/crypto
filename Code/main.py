import BlindSig as bs
import hashlib
import random
import cryptomath

# Color codes for output formatting
yellow_text = '\u001b[33;1m'
reset_text = '\u001b[0m'
red_text = '\u001b[31m'
pink_text = '\u001b[35;1m'
green_text = '\u001b[32;1m'

class VotingPoll:
    def __init__(self):
        self.signature_authority = bs.Signer()
        self.public_key_info = self.signature_authority.getPublicKey()
        self.modulus_n = self.public_key_info['n']
        self.exponent_e = self.public_key_info['e']
        
    def handle_poll_response(self, voter_choice, is_eligible):
        if is_eligible == 0:
            eligibility_status = "n"
        elif is_eligible == 1:
            eligibility_status = "y"
        
        print('\n\n' + '-'*100) 
        print(' '*50 + red_text + "MODULE 2" + reset_text)
        print('-'*100 + '\n\n')    
        
        print(yellow_text + "2. Voter Prepares Ballot for signing by Authority:" + reset_text + '\n')
        random_number = random.randint(1, self.modulus_n)
        print(pink_text + "(a) Generates random x within 1 and n" + reset_text)
        print(yellow_text + "x: " + reset_text, random_number, "\n")
        
        print(pink_text + "(b) Voter selects a candidate on the ballot" + reset_text)
        ballot_message = voter_choice
        print(yellow_text + "Voter choice: " + reset_text, voter_choice, "\n")

        # Concatenating message and producing its hash
        concatenated_msg = str(ballot_message) + str(random_number)
        print(pink_text + "(c) Concatenating choice with x and hashing" + reset_text)
        print(yellow_text + "Concatenated message: " + reset_text, concatenated_msg, "\n")
        message_hash = int(hashlib.sha256(concatenated_msg.encode('utf-8')).hexdigest(), 16)
        print(yellow_text + "Hash of concatenated message: " + reset_text, message_hash, "\n")
        
        voter_instance = bs.Voter(self.modulus_n, eligibility_status)
        blinded_msg = voter_instance.blindMessage(message_hash, self.modulus_n, self.exponent_e)
        print(pink_text + "(f) Sends blinded message to authority" + reset_text)
        signed_blinded_msg = self.signature_authority.signMessage(blinded_msg, voter_instance.getEligibility())

        if signed_blinded_msg == None:
            print(red_text + "INELIGIBLE VOTER... VOTE NOT AUTHORIZED!" + reset_text)
        else:
            print(yellow_text + "Signed blinded message: " + reset_text, signed_blinded_msg, "\n")
            signed_message = voter_instance.unwrapSignature(signed_blinded_msg, self.modulus_n)
            
            print('\n\n' + '-'*100) 
            print(' '*50 + red_text + "MODULE 5" + reset_text)
            print('-'*100 + '\n\n')    
            
            print(yellow_text + "5. Ballot Received and Verification" + reset_text + '\n')
            print(pink_text + "A voter's vote shall consist of:" + reset_text)
            print(yellow_text + "(a) Vote concatenated with x: " + reset_text, concatenated_msg)
            print(yellow_text + "(b) Hash of vote signed by authority:" + reset_text, signed_message, "\n")
            
            verification_status, decoded_message = bs.verifySignature(ballot_message, random_number, signed_message, self.exponent_e, self.modulus_n)
            print(yellow_text + "Verification status: " + reset_text, verification_status, "\n")
            if verification_status:
                print(pink_text + "Since verification is true, the vote is the first digit of the concatenated message: " + reset_text, decoded_message, "\n\n\n")


class VotingMachine:
    def __init__(self):
        self.poll = VotingPoll()  # Assuming VotingPoll is already defined as per previous modifications
        print(yellow_text + "Make your selection:" + reset_text)
        print("\n(1) Cryptography     (2) Biometrics      (3) Intro to ML      (4) ML for Security    (5) DADT")
        choice = int(input())
        
        while choice < 1 or choice > 5:
            print(red_text + f"Input {choice} is not a valid option. Please enter a valid option:" + reset_text)
            choice = int(input())
        
        print('\n\n' + '-'*100)
        print(' '*30 + red_text + "Digital Signature Authentication" + reset_text)
        print('-'*100 + '\n\n')

        prime_p = cryptomath.generate_prime()
        print(yellow_text + "Prime p: " + reset_text, prime_p, "\n")

        prime_q = cryptomath.generate_prime()
        print(yellow_text + "Prime q: " + reset_text, prime_q, "\n")

        modulus_n = prime_p * prime_q
        print(pink_text + "Calculate n=p*q:" + reset_text)
        print(yellow_text + "n: " + reset_text, modulus_n, "\n")

        totient_phi = (prime_p - 1) * (prime_q - 1)
        print(pink_text + "Calculate the totient of n (ϕ(n)):" + reset_text)
        print(yellow_text + "ϕ(n): " + reset_text, totient_phi, "\n")

        public_key, private_key = self.find_keys(totient_phi)
        print(yellow_text + "Public key (e): " + reset_text, public_key)
        print(yellow_text + "Private key (d): " + reset_text, private_key, "\n")

        id_number = int(input(yellow_text + "Enter ID Number: " + reset_text))
        signature, verification_hash = self.create_signature(id_number, private_key, modulus_n)
        print(yellow_text + "Digital Signature (s): " + reset_text, signature, "\n")

        decrypted_message = pow(signature, public_key, modulus_n)
        print(pink_text + "Decrypting the message using public key:" + reset_text)
        print(yellow_text + "Decrypted Message: " + reset_text, decrypted_message, "\n")
        if decrypted_message == verification_hash:
            print(green_text + "Voter Authenticated" + reset_text)
            self.poll.handle_poll_response(choice, 1)

    def find_keys(self, phi):
        public_key = 0
        private_key = 0
        found = False
        while not found:
            public_key = random.randint(2, phi - 1)
            if cryptomath.calculate_gcd(public_key, phi) == 1:
                private_key = cryptomath.calculate_mod_inverse(public_key, phi)
                found = True
        return public_key, private_key

    def create_signature(self, id_number, private_key, n):
        id_number_str = str(id_number)
        id_number_hash = int(hashlib.sha256(id_number_str.encode('utf-8')).hexdigest(), 16)
        signature = pow(id_number_hash, private_key, n)
        return signature, id_number_hash

# To create an instance of VotingMachine and start the process
voting_machine = VotingMachine()