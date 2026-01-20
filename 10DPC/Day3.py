#Conditional statements:
score= int(input("Enter mark: "))
if score>100 :
      print("Invalid mark")
elif score>=90 :
      print("Grade A")
elif score>=70 and score<90 :
      print("Grade B")
elif score>=50 and score<70 :
      print("Grade C")
else :
      print("Fail")
#Nested if
#Multiple condition variables to check

#Ternary:
Status="Good" if score>= 70 else "Needs improvement"
print(Status)