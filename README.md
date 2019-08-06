# TheRiddlerSolution-CircularTrain
This is my solution to 538's Circular train puzzle published on August 2, 2019

Link: https://fivethirtyeight.com/features/how-many-cars-are-on-this-circular-train/

# Puzzle Text:
Riddler Classic
From Ben Tupper, ‘round and ‘round the railroad:

You find yourself in a train made up of some unknown number of connected train cars that join to form a circle. It’s the ouroboros of transportation. Don’t think too hard about its practical uses.

From the car you’re in, you can walk to a car on either side — and because the train is a circle, if you walk far enough eventually you’ll wind up back where you started. Each car has a single light that you can turn on and off. Each light in the train is initially set on or off at random.

What is the most efficient method for figuring out how many cars are in the train?

(Assume that you can’t mark or otherwise deface a train car, and that each car’s light is only visible from within that car. The doors automatically close behind you, too. There are only two actions you can take: turning on or off a light and walking between cars.)

# Solution

Walk around the train, every time you find a light that matches the starting light, change it and return to start while keeping track of the number of cars you went through to get there.
- If the starting car's light has changed when you get back then you know you were just in the starting car and
  can return the number of cars in the train.
- If the starting car's light is unchanged then repeat the process.

Time Complexity:
- Worst Case: All of the lights on the train are the same. For each new car you see you have to
            backtrack all the way to the start for:
            
      __ i           
      \            2i 
      /__ num cars     



- Average Case: We already know lights which are different than the start can't be the start and so there is no reason to backtrack in this case. On average 1/2 of the new lights seen will be different and not require backtracking for a better a total moves of:

        __ i                
       \            3i  /  2
       /__ num cars         


- Best Case: First light different than every other light. In this case you can make one complete loop. Find the
           first light and immediately backtrack for a total of:
          
          2(num cars)   
           
           
## Improvements to the strategy: 
After returning to start we can do the same strategy but instead in the opposite direction. This saves time because it splits the problem in half, where we are solving the left side of the train and the right side of the train seperately and then adding up the result. This avoids the having to backtrack the entire train for cars which are close to the starting car in the opposite direction significantly improving the efficiency of the search.
  
The new better time complexities are now:

- Worst Case: Since on average we will finish the first half of the loop from the left, and the other half from the right the new time complexity will be:

      (  __ i             )
      (  \            2i  ) * 2
      (  /__ num cars / 2 )
    
- Average Case: Same as in the worst case. We can add up how long it takes to do half the loop for both sides.



      (  __ i               )
      (  \            3i/2  ) * 2
      (  /__ num cars / 2   )
    
- Best Case: Best case will be the same as before since it consists of only the one loop there and one loop back.

To test and show both strategies I coded both strategies under all cases in Python.

![](simulation_result.png?raw=true)

