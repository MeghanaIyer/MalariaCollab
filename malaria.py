#!/usr/bin/python3

"""
o	Title: Running Exercise 1

o	Date: 09.10.2020

o	Author: Mara Vizitiu

o	Description: A common task for bioinformaticians is to merge data from several
        files into one. You have a FASTA file (malaria.fna) with multiple DNA sequences. 
        You want to annotate them, that is, know which protein sequence they relate to. 
        You used a blastx-run (using the gene sequences as queries and the UniProt database 
        as target), the results of which are saved in malaria.blastx.tab. Your task in 
        this exercise is to insert the information about the protein description 
        (hitDescription) from the blastx results to the fasta file. If the gene 
        doesn't have a Blastx hit, indicated by null in the blast-file, it should 
        not be included in the output file.
        
o	List of user defined functions (if any): No user defined functions were used.

o	List of modules used that are not explained in the course material: No modules were used.

o	Procedure:
        1. Make a dictionary that includes all the gene IDs in the Blastx result file
        (malaria.blastx.tab) and the names of the corresponding encoded proteins.
    
        2. Make a list of all the gene IDs in the FASTA file (malaria.fna), that is
        then used to look for the corresponding protein names in the dictionary.
        By making this list we can ensure that we keep the original order that the
        genes appear in in the FASTA file.
    
        3. Write into a new file the FASTA file headers, including the names of the
        encoded proteins, and the sequences for each of the genes, but only keeping the
        sequences for genes that have a non-null result in the Blastx analysis.
        
o	Usage: python malaria.py malaria.fna malaria.blastx.tab output.txt

"""

f=open("malaria.blastx.tab", "r")
my_dict={} #Empty dictionary for the IDs and protein names
ID=[] #List of the gene IDs
Desc=[] #List of the names of the encoded proteins
header=f.readline() #Do not add header line into dictionary
for line in f:
    data=line.split("\t")
    for i in data: #Add the protein IDs to the keys of the dictionary
        i=data[0] #i wil be the IDs in every line
        ID.append(">"+i) #Add the IDs to a list in the same format as in FASTA file
    for j in data: #Add the protein names to the values of the dictionary
        j=data[9] #j is the hitDescription in every line
        Desc.append(j)
for key in ID: #Adding IDs and corresponding names to the dictionary
    for value in Desc:
        my_dict[key]=value
        Desc.remove(value) #We need to remove a value once it was added, to move on to the next one
        break #Go back to grabbing the next i and the corresponding j
f.close()

FASTA_ID=[] #List of all the gene IDs taken from the FASTA file (malaria.fna)
f1=open("malaria.fna", "r")
for line in f1:
    if line.startswith(">"): #Only look at header lines
        data1=line.split("\t") #Split the header into different sections
        k=data1[0] #k is the ID of the gene in each line
        FASTA_ID.append(k)
f1.close()

f1=open("malaria.fna", "r") #Open file again, to start reading from the first line
f2=open("output.txt", "w") #The file we are creating and writing the output in
l=False #Variable that we use to only write sequences for the genes that have non-null results
for m in FASTA_ID: #Check each gene ID in malaria.fna
    for line in f1:
        if line.startswith(m): #If the line starts with the ID
            if my_dict[m] == "null": #Genes that have null blast results are not written
                break
            else:
                f2.write(line.strip("\n")+"\tProtein = "+str(my_dict[m])+"\n") #Write a new header line that includes the protein name
                l=True #Make l true when the header line is written
            break
        else:
            if l: #If a header line has been written
                f2.write(line) #Write the next line (the sequence)
                l=False #Make l false again to re-start the process
f1.close()
f2.close()
