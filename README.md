# LinearCryptanalysisExperiment

*********
*Authors*
*********
Subhabrata Samajder, Indraprastha Institute of Information Technology, Delhi, India

Palash Sarkar, Indian Statistical Institute, Kolkata, India


**********************
*About the experiment* 
**********************
The code here presents an implementation of a linear cryptanalysis experiment on the scaled version of Present called Small Present (see https://eprint.iacr.org/2010/143). It randomly selects an n-bit input mask and an n-bit output mask for the input to the second last round of the Small Present cipher. The output mask determines the number of subkey bits m, i.e., the number of key bits that needs to be guessed in the key recovery attack using linear cryptanalysis. The output mask is selected in such a way that m <= 32. A 80-bit key K is then randomly selected and the key scheduling algorithm for Small Present is applied to it to generate the rounds keys. For the purpose of our experiment we take the number of rounds to be 10. A wrong key guess is made for the m subkey bits of the last rounds. The setup phase of the experiment ends here. 

After the setup phase, N plaintexts are randomly generated and their corresponding ciphertexts are obtained by encryption under Small Present using the key K. For each plaintext-ciphertext pair, the ciphertext is inverted over the last and the last but one rounds using the wrong key guess and the linear approximation is evaluated. The experiment counts the number of ones out of these N plaintext-ciphertext pairs, which is a number between 0 to N. This corresponds to one observation of the experiment. We independently repeat the experiment S times to generate S such observations. From these S observations, the empirical distribution, i.e., the number of times the value i (lying between 0 to N) occurs out of S iterations divided by S, is computed and these are plotted in a graph.

*************************  
*Contents of this folder*
*************************
1. aes.py: We have borrowed this aes implementation from https://github.com/boppreh/aes. We have used AES in CTR mode for generating random numbers in the experiment. We would like to thank the authors of this code for their code public.

2. SmallPresent.py: This contains a Python implementation of SmallPresent. Note that only the encryption algorithm is implemented as our experiment does not require the decryption algorithm.

3. TestSmallPresent.py: When executed this program outputs the test vectors given in the table at the end of https://eprint.iacr.org/2010/143.

4. LinearCryptanalysis.py: It contains the following three modules required by the experiment.
   (a) FindMasksSubKey: This randomly generates an input mask and an output mask. It also ensures that m <= 32.
   (b) KeyGuess: Makes a wrong key guess for the subkey bits involved in the experiment and returned by FindMaskSubkey.
   (c) LinearCryptanalysis: This is the main program. It corresponds to one observation of the experiment. This module randomly generates N plaintext-ciphertext pairs, inverts the ciphertexts by two rounds and ultimately computes the number of times the linear approximation equals 1 out of these N plaintext-ciphertext pairs.

5. Experiment.py: This records S observations by making S calls to LinearCryptanalysis function. It then outputs a data file containing the counts and a graph plot of the empirical distribution. The data files are named as n%s-N%s-S%s.txt, n%s-N%s-S%s_1.txt, ... and the graph plots are named as n%s-N%s-S%s.pdf, n%s-N%s-S%s_1.pdf, ....

6. Plot.py: It takes the data file which is one of the outputs of Experiment.py and reconstructs the graph plot containing the empirical distribution.

7. MultExp.sh: This is a bash file which takes in two arguments n and R. It generates R independent copies of Experiment.py using the nohup function with parameters n, N = 2^(n - 1)/2^(n - 2)/2^(n - 3)/... and S = 100*N.

***********************************
*Instruction for running the files*
***********************************
1. TestSmallPresent.py: python3 TestSmallPresent.py

2. Experiment.py: python3 Experiment.py -i n N S

3. Plot.py: python3 Plot.py -i n N S CounterLow CounterUpp, where CounterLow and CounterHigh denote the range (both inclusive) of files which one wants to reconstruct. That is it reconstructs the data files from n%s-N%s-S%s_CounterLow.txt to n%s-N%s-S%s_CounterHigh.txt, where CounterLow = 0 implies the file named n%s-N%s-S%s.txt.

**************
*Requirements*
**************
The program requires python3 with the following libraries.
1. numpy
2. mpmath
3. scipy
4. matplotlib
5. seaborn
