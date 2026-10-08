# Prompts used with Claude Code

These are the prompts I gave Claude Code (in VS Code) while working on this assignment, in order.

1. /init (asked Claude Code to analyze the project folder and create a CLAUDE.md file with guidance for the project)

2. Add to CLAUDE.md: always use seed=1 in delivery_times calls, and always add markdown cells in the notebook explaining each step.

3. (Pasted Part I(a) from the assignment)

   Write Python code for the following tasks.
   a. (10 points) For any provided promised delivery time and each pair of specified zone and time block, write a function that returns the percentage of late orders.
   - If a particular zone and time block is provided, it returns the percentage of late orders in that zone and time block.
   - If the zone is 'all' and a specific time block is provided, it returns the percentage of late orders in that time block across all zones.
   - If a specific zone is provided and the time block is 'all', it returns the percentage of late orders in that zone across all time blocks.
   - If both the zone and time block are 'all', it returns the overall percentage of late orders.

   edit the rosa_analysis.ipynb

4. okay. i did the the pip command but i ran it in the terminal since i am working in the jupyter notebook and not colab. but i guess i can just add it without running in at the top.

   next part: With the current promised delivery time of 45 minutes, rank the pairs of zone and time block in the descending order of late arrival rate.

5. (Pasted Part I(c) from the assignment)

   c. (7 points) For any provided promised delivery time and each pair of specified zone and time block, write a function that returns the average delivery time.
   - If a particular zone and time block is provided, it returns the average delivery time in that zone and time block.
   - If the zone is 'all' and a specific time block is provided, it returns the average delivery time in that time block across all zones.
   - If a specific zone is provided and the time block is 'all', it returns the average delivery time in that zone across all time blocks.
   - If both the zone and time block are 'all', it returns the overall average delivery time.

   okay now do this. also, i cannot see the pip install cell

6. d. (3points) With the current promised delivery time of 45 minutes, rank the pairs of zone and time block in the descending order of average delivery time.
   e. (10 points) Which measure, the late rate (b) or the average delivery time (d), is more relevant to Rosa's decisions? Explain why, using your results from b and d.

   okay gotcha thanks, now d and e please

7. okay now part 2, do a and b both

8. okay now part 3. if there is anything that i have to do manually for this part then let me know the steps for it

9. remove all the extra red and blue and extra editing in the markdown. it looks very AI generated.

10. also, all the prompts i have given you, put it in the prompts.md file
