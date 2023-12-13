# Secure E-Voting Mechanism using Blind Signature and Digital Signature

## Introduction

With the exponential growth of computer networks and increased internet accessibility, there's a unique opportunity to enhance voter participation through E-Voting. Our system addresses key issues in authentication and privacy using a combination of digital and blind signatures. Digital signatures authenticate the voter's identity, while blind signatures ensure the confidentiality of their vote.

Digital signatures are used to verify the sender's identity and the message's integrity. This involves encrypting the message hash with the sender's private key, followed by decryption and verification using the sender's public key.

Blind signatures, ideal for privacy-sensitive protocols, ensure the signer cannot view the message content. In E-Voting, this allows an official to verify voter eligibility without seeing the vote itself. A blind signature effectively conceals the message content before it's signed, with the ability to be publicly verified against the original message.

## Objectives

1. To delve into digital and blind signatures, understanding their role in ensuring authentication and confidentiality in E-Voting.

2. To develop a Python-based E-Voting application incorporating blind and digital signatures.

3. To execute and rigorously test the voting application, confirming the effectiveness and security of the cryptographic scheme employed.

## Project Deliverables

Our deliverable is a Python-implemented E-Voting application using blind and digital signatures. It meticulously records key usage and demonstrates the cryptographic mechanisms at work, affirming the use of cryptography in the system.

## Relevant Research

- [Secure E-Voting With Blind Signature](https://core.ac.uk/download/pdf/11779635.pdf)

- [Blind Signatures for Untraceable Payments](https://sceweb.sce.uhcl.edu/yang/teaching/csci5234WebSecurityFall2011/Chaum-blind-signatures.PDF)

## Workflow

###### 1. Key Generation by the Signing Authority:

    (a) Generation of random numbers p and q.
    (b) Calculation of n=pq and ϕ(n)=(p-1)(q-1).
    (c) Selection of e with gcd(ϕ(n),e)=1 & 1< e <ϕ(n).
    (d) Computation of d, the inverse of e modulo ϕ(n).
    (e) Public announcement of the Public key: (n,e) while securing the private keys.

<img width="1139" alt="Digital Signature Authentication - 1" src="https://github.com/vineela350/crypto/assets/60750419/554ef75b-3818-422c-91e2-590414b07ca2">

<img width="1138" alt="Digital Signature Authentication - 2" src="https://github.com/vineela350/crypto/assets/60750419/17be0826-822e-48f8-a939-8fa50baa8877">


###### Digital Signature Authentication via RSA:

    (a) Selection of two large prime numbers p and q.
    (b) Calculation of n=p*q and the totient of n.
    (c) Public_key choice with gcd(ϕ(n),public_key)=1 & 1 < public_key < ϕ(n).
    (d) Computation of private_key as the inverse of public_key modulo ϕ(n), alongside voter ID entry.
    (e) Hashing the message (idNumber).
    (f) Voter's creation of Digital Signature using s=(message_hash)^(private key) mod n.
    (g) Availability of Digital Signature, s, and the original message, idNumber, to the Verifier.
    (h) Verification involves comparing the decrypted message and Hash(idNumber).
    (i) Calculation of the Hash(idNumber) and decrypting the message using (digital_signature s)^(public key)mod n.
    (j) Hash of the message ie, Hash(idNumber) is calculated
    (k) Decrypting the message(without Hash) using 
           (digital_signature s)^(public key)mod n 
         = (message_hash)^((private key)*(public key))mod n 
         = (message_hash)^1 mod n 
         = (message_hash)

<img width="1117" alt="Digital Signature Authenticated" src="https://github.com/vineela350/crypto/assets/60750419/7fc06633-2948-4ab5-b0e5-cc1f78ec2058">



###### 2. Voter's Ballot Preparation:

    (a) Generation of a random number x within the range 1<=x<=n.
    (b) Voter's choice of candidate and ballot marking.
    (c) Creation of a message combining poll_answer + x and hashing it, denoted by m.
    (d) Generation of r, a relative prime to n in the range 2<= r <=(n-1).
    (e) Computation of the blinded message m' = (m* (r^e)) mod n.
    (f) Submission of m' to the signing authority.


<img width="1122" alt="Voter's Ballot Preparation" src="https://github.com/vineela350/crypto/assets/60750419/1e27c50d-101f-4278-a196-35724935f964">


###### 3. Signing Authority's Ballot Authorization:

    (a) Receipt of m' by the signing authority.
    (b) Verification of voter eligibility.
    (c) Signing of the ballot if eligibility is confirmed.
        sign = ((blinded message)^d)mod n 
             = ((m* (r^e))^d) mod n 
             = (m^d * r^(ed)) mod n 
             = (m^d * r^1) mod n 
             = (m^d * r) mod n    (where d is the private key of the signing authority)
    (d) Return of the signed ballot s' to the voter.


<img width="1130" alt="Signing Authority's Ballot Authorization" src="https://github.com/vineela350/crypto/assets/60750419/8cdda70b-538a-4bdb-86f0-0518704010b4">


###### 4. Voter's Unblinding of Ballot:

    (a) Receipt and unblinding of s' by the voter.
    (b) Computation of s = (s')*(rInv) mod n.
        = (s')*(rInv) mod n 
        = (m^d * r)*(rInv) mod n 
        = (m^d * 1) mod n 
        = (m^d) mod n

    (c) Sending the signature s to the ballot receiving location.

<img width="1107" alt=" Voter's Unblinding of Ballot" src="https://github.com/vineela350/crypto/assets/60750419/5b8f8746-517c-45e6-86c8-a8c20c8a99c1">



###### 5. digital signature: 

    - The ballot includes the voter's choice and a number x, alongside the hash of this concatenated vote signed by the authority.
    - Verification is done by decrypting the signed hash message using the authority's public key.
    - A match between the hash and decrypted message confirms the signing authority's
          (s^e) mod n 
        = (m^d)^e mod n 
        = (m^1) mod n 
        = m mod n (since m < n)
        = m  

Hash Computation: Calculate the hash of the combined message, denoted as hash(concatenated message).

Authentication Verification: Compare the calculated hash with the decrypted message. A match indicates that the message has been authenticated by the signing authority.

Vote Extraction: If the verification is successful, extract the vote as the first element of the concatenated message. This is done using the publicly known hash algorithm.


<img width="1126" alt="Ballot Verification" src="https://github.com/vineela350/crypto/assets/60750419/c825a1b0-5a6f-40c3-b6cf-2b94fc2b8aac">


## Use

- Go to folder code in terminal.

- Run using `python3 main.py`
# crypto
