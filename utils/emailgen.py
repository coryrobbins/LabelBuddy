#generate random fake emails
import csv
import random


with open('email_body.csv', mode='w', newline='') as file:
    
    #create csv writer
    writer = csv.writer(file)
    
    #write header
    writer.writerow(['body', 'label' ])

    for i in range(100):
        #generate random email body
        body_text = ''
        for j in range (random.randint(5, 15)):
            #generate random email sentence from 5 to 15 words
            sentence = ' '.join(random.choice(['hello', 'world', 'this', 'is', 'a', 'test', 'for', 'the', 'email', 'body', 'text']) for _ in range(random.randint(5, 15)))
            body_text += sentence.capitalize() + '. '
            #write to csv

        writer.writerow([body_text, ''])
    
   #close file 
    file.close()

    